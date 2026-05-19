#!/usr/bin/env python3
"""
Upload retrieval-optimised *.summary.md files to Ragie partition ap1-curated-summaries.

Ragie creates a NEW document on each POST; it does not replace by filename. By default this
script **deletes** existing documents in the partition that match our bundle (same
`external_id` as a local .summary.md stem, or name ending in `.summary.md`), then uploads.

Requires:
  - RAGIE_API_KEY in the environment

Usage:
  python scripts/upload_ap1_curated_summaries_to_ragie.py
  python scripts/upload_ap1_curated_summaries_to_ragie.py --dry-run
  python scripts/upload_ap1_curated_summaries_to_ragie.py --no-delete   # append only (may duplicate)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

API_BASE = "https://api.ragie.ai"
PARTITION = "ap1-curated-summaries"
CORPUS = "salmon-lice-and-mortality-of-wild-salmonids"


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def summaries_bundle_dir() -> Path:
    return (
        _repo_root()
        / "corpora"
        / "salmon-lice-and-mortality-of-wild-salmonids"
        / "ragie_partition_ap1_curated_summaries"
    )


def _headers(api_key: str, *, partition: str | None = PARTITION) -> dict[str, str]:
    h = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }
    if partition:
        h["partition"] = partition
    return h


def list_documents_page(
    api_key: str, *, cursor: str | None, page_size: int = 100
) -> dict:
    q = f"page_size={page_size}"
    if cursor:
        q += f"&cursor={quote(cursor, safe='')}"
    url = f"{API_BASE}/documents?{q}"
    req = Request(url, headers=_headers(api_key), method="GET")
    with urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def delete_document(api_key: str, document_id: str, dry_run: bool) -> None:
    if dry_run:
        print(f"  [dry-run] DELETE document {document_id}")
        return
    url = f"{API_BASE}/documents/{document_id}"
    req = Request(url, headers=_headers(api_key), method="DELETE")
    with urlopen(req, timeout=120) as resp:
        resp.read()


def collect_local_external_ids(files: list[Path]) -> set[str]:
    return {p.name.removesuffix(".summary.md") for p in files}


def delete_stale_summaries(
    api_key: str,
    local_ids: set[str],
    expected_names: set[str],
    dry_run: bool,
) -> int:
    """Remove Ragie docs in PARTITION that belong to this bundle (avoid duplicates)."""
    to_delete: list[str] = []
    cursor = None
    while True:
        data = list_documents_page(api_key, cursor=cursor, page_size=100)
        docs = data.get("documents") or []
        for d in docs:
            part = d.get("partition")
            if part is not None and part != PARTITION:
                continue
            name = d.get("name") or ""
            meta = d.get("metadata") or {}
            ext = d.get("external_id") or meta.get("external_id")
            if name in expected_names:
                to_delete.append(d["id"])
            elif ext and str(ext) in local_ids:
                to_delete.append(d["id"])
            elif name.endswith(".summary.md"):
                stem = name.removesuffix(".summary.md")
                if stem in local_ids:
                    to_delete.append(d["id"])
        pag = data.get("pagination") or {}
        cursor = pag.get("cursor")
        if not cursor:
            break

    seen: set[str] = set()
    unique_delete: list[str] = []
    for i in to_delete:
        if i not in seen:
            seen.add(i)
            unique_delete.append(i)
    print(f"Deleting {len(unique_delete)} existing document(s) in partition {PARTITION!r} …")
    errors = 0
    for doc_id in unique_delete:
        try:
            delete_document(api_key, doc_id, dry_run)
            print(f"  deleted {doc_id}")
        except HTTPError as e:
            err = e.read().decode("utf-8", errors="replace")
            print(f"  ERROR delete {doc_id}: HTTP {e.code} {err}", file=sys.stderr)
            errors += 1
        except URLError as e:
            print(f"  ERROR delete {doc_id}: {e}", file=sys.stderr)
            errors += 1
    return errors


def build_multipart(file_path: Path, partition: str, metadata: dict) -> tuple[bytes, str]:
    boundary = f"----RagieUpload{uuid.uuid4().hex}"
    crlf = b"\r\n"
    body = bytearray()

    def add_field(name: str, value: str) -> None:
        body.extend(f"--{boundary}".encode())
        body.extend(crlf)
        body.extend(f'Content-Disposition: form-data; name="{name}"'.encode())
        body.extend(crlf)
        body.extend(crlf)
        body.extend(value.encode("utf-8"))
        body.extend(crlf)

    add_field("mode", "fast")
    add_field("partition", partition)
    add_field("name", file_path.name)
    add_field("metadata", json.dumps(metadata, ensure_ascii=False))

    file_bytes = file_path.read_bytes()
    body.extend(f"--{boundary}".encode())
    body.extend(crlf)
    disp = f'Content-Disposition: form-data; name="file"; filename="{file_path.name}"'
    body.extend(disp.encode())
    body.extend(crlf)
    body.extend(b"Content-Type: text/markdown; charset=utf-8")
    body.extend(crlf)
    body.extend(crlf)
    body.extend(file_bytes)
    body.extend(crlf)
    body.extend(f"--{boundary}--".encode())
    body.extend(crlf)

    content_type = f"multipart/form-data; boundary={boundary}"
    return bytes(body), content_type


def upload_one(
    api_key: str, file_path: Path, metadata_extra: dict, dry_run: bool
) -> int:
    external_id = file_path.name.removesuffix(".summary.md")
    metadata = {
        "layer": "curated_summaries",
        "corpus": CORPUS,
        "project": "ap1",
        "external_id": external_id,
        "doc_type": "evidence_summary",
        **metadata_extra,
    }
    body, ct = build_multipart(file_path, PARTITION, metadata)
    if dry_run:
        print(f"[dry-run] would upload {file_path.name} ({len(body)} bytes)")
        return 0

    req = Request(
        f"{API_BASE}/documents",
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": ct,
            "Accept": "application/json",
        },
    )
    try:
        with urlopen(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"ERROR {file_path.name}: HTTP {e.code} {err_body}", file=sys.stderr)
        return 1
    except URLError as e:
        print(f"ERROR {file_path.name}: {e}", file=sys.stderr)
        return 1

    print(f"OK {file_path.name}: {raw[:200]}{'...' if len(raw) > 200 else ''}")
    return 0


def priority_questions_for_file(stem: str) -> list[str]:
    """Mirror of metadata.yaml priority_questions (single source for Ragie metadata)."""
    m: dict[str, list[str]] = {
        "1997_icesjms_dawson-seatrout-salmon-susceptibility": ["Q4", "Q6"],
        "2017_icesjms_forseth-major-threats-norway": ["Q9", "Q10"],
        "2021_aei_seatrout-risk-assessment": ["Q1", "Q2", "Q3", "Q5", "Q8"],
        "2021_icesjms_jansen-comment-vps-mortality": ["Q5", "Q7", "Q8", "Q10"],
        "2021_rcn_traffic-light-evaluation": ["Q7", "Q8", "Q9", "Q10"],
        "2021_rfsa_dadswell-atlantic-salmon-collapse": ["Q9"],
        "2022_aei_stige-model-sensitivity-calibration": ["Q5", "Q7", "Q8", "Q10"],
        "2022_rfbf_gillson-marine-stressors-salmon": ["Q9"],
        "2024_raq_vannes-critical-review-tls": ["Q1", "Q2", "Q5", "Q7", "Q8", "Q10"],
        "2025_aquaculture_gjerde-seatrout-lice-prediction": ["Q5", "Q7", "Q10"],
        "2025_jae_jansen-lice-effects-returns": ["Q4", "Q6", "Q9", "Q10"],
        "2025_raq_stige-comment-vannes": ["Q5", "Q7", "Q8", "Q10"],
        "2025_raq_vannes-response-to-stige": ["Q5", "Q7", "Q8", "Q10"],
        "2025_scientificdata_bc-sealice-dataset-2001-2023": ["Q1", "Q5"],
        "2026_prslb_folk-parasites-high-host-density": ["Q2", "Q6"],
    }
    return m.get(stem, [])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync AP1 curated summaries to Ragie (delete matching + upload)"
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--no-delete",
        action="store_true",
        help="Do not delete existing .summary.md / matching external_id in partition",
    )
    args = parser.parse_args()

    api_key = os.environ.get("RAGIE_API_KEY", "").strip()
    if len(api_key) >= 2 and api_key[0] == "<" and api_key[-1] == ">":
        api_key = api_key[1:-1].strip()
    if not api_key and not args.dry_run:
        print(
            "Missing RAGIE_API_KEY. Set it in the environment, then re-run.\n"
            "PowerShell:  $env:RAGIE_API_KEY = 'your-key'",
            file=sys.stderr,
        )
        return 2

    bundle = summaries_bundle_dir()
    if not bundle.is_dir():
        print(f"Summaries folder not found: {bundle}", file=sys.stderr)
        return 2

    files = sorted(bundle.glob("*.summary.md"))
    if not files:
        print(f"No *.summary.md files in {bundle}", file=sys.stderr)
        return 2

    local_ids = collect_local_external_ids(files)
    expected_names = {p.name for p in files}
    print(f"Partition: {PARTITION}")
    print(f"Local summary files: {len(files)}")

    rc = 0
    if not args.no_delete:
        if not api_key and args.dry_run:
            print(
                "[dry-run] Skipping delete/list (set RAGIE_API_KEY to simulate full sync)."
            )
        else:
            rc |= delete_stale_summaries(
                api_key or "", local_ids, expected_names, args.dry_run
            )

    for fp in files:
        stem = fp.name.removesuffix(".summary.md")
        pq = priority_questions_for_file(stem)
        meta_extra: dict = {}
        if pq:
            meta_extra["priority_questions"] = pq
        rc |= upload_one(api_key or "", fp, meta_extra, args.dry_run)

    return min(rc, 1)


if __name__ == "__main__":
    raise SystemExit(main())
