"""
Bootstrap the area-and-aquaculture corpus from PDFs already in documents/PDFs/.

Does NOT touch the villaks parquet.

Stages per document:
  1. Extract PDF -> extracted.md
  2. Lite curate -> metadata.yaml + summary.md (areal draft questions)
  3. After all docs: ingest.py --corpus area-and-aquaculture

Usage (from repo root):
    python scripts/bootstrap_areal_corpus.py
    python scripts/bootstrap_areal_corpus.py --skip-extract --skip-curate
    python scripts/bootstrap_areal_corpus.py --doc 2011_gullestad_arealbruk-havbruk
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

import yaml
from dotenv import load_dotenv
from openai import OpenAI

sys.path.insert(0, str(Path(__file__).resolve().parent))
from convert_pdfs_odl import convert_one, convert_one_pymupdf  # noqa: E402
from corpus_paths import AREAL_SLUG, REPO_ROOT, STATUS_AI_DRAFT, get_corpus  # noqa: E402

# Large illustrated reports: ODL is slow and often loses the output path on Windows.
LARGE_PDF_BYTES = 12 * 1024 * 1024

load_dotenv(REPO_ROOT / ".env", override=True)

CURATE_MODEL = os.getenv("AP1_AREAL_CURATE_MODEL", "gpt-4o-mini")
EXTRACT_CHAR_CAP = int(os.getenv("AP1_CURATE_EXTRACT_CHARS", "35000"))

SYSTEM = """\
You curate documents for Havbruksløftets Evidensrom, room:
Area and aquaculture (Areal og havbruk).

The room is about dilemmas of area use and aquaculture activity.
It is NOT the salmon-lice / wild-salmon mortality room.

Working draft questions (not expert-confirmed):
A1 Allocation and use of coastal or sea area for aquaculture
A2 Trade-offs with environment, wild fish, other industries, municipalities, public values
A3 Knowledge used or missing in siting, impact assessment, licence or locality decisions
A4 How licensing and coastal planning shape access to sites
A5 Spatial density, productivity, and environmental or disease consequences of area use

Rules:
1. Use ONLY the extract. Do not invent findings, numbers, or citations.
2. If a value is missing, use empty string, empty list, or omit. Do not guess.
3. Prefix uncertain free text with [UNVERIFIED].
4. Preserve disagreement. Do not advocate a policy outcome.
5. priority_questions: subset of A1-A5 only, if the extract actually speaks to them.
6. evidence_direction: use not_applicable unless the paper clearly claims or
   contests a specific causal effect. Allowed values:
   supports_effect | weak_support | mixed_within_study | no_effect_detected |
   contradicts_effect | critiques_methodology | not_applicable
7. Write rag_summary and summary_md in English.
8. Output valid JSON only.
"""

USER = """\
Document id: {doc_id}
Source filename: {pdf_name}

Extract (may be truncated):
---
{extract}
---

Return JSON with keys:
title (string),
year (string, four digits if stated),
authors (list of strings),
journal (string),
document_type (string, e.g. research_article, policy_report, review_article, risk_assessment),
doi (string),
url (string),
rag_summary (string, 120-220 words, what the document says about area, aquaculture, or adjacent dilemmas),
key_claims (list of 3-8 short strings from the extract),
included_because (one or two sentences: why it belongs in an area-and-aquaculture draft corpus),
priority_questions (list of A1-A5),
evidence_direction (string),
controversy_role (foundational|supportive|critical|rebuttal|bridge_between_positions|peripheral|not_applicable),
quality_signal (strong|medium|weak),
quality_rationale (string),
summary_md (string, 400-900 words evidence brief from the extract only)
"""


def load_manifest(paths) -> list[dict]:
    raw = json.loads((paths.root / "manifest.json").read_text(encoding="utf-8"))
    return raw["items"]


def find_pdf(pdf_dir: Path, match: str) -> Path | None:
    hits = []
    needle = match.lower()
    for p in pdf_dir.iterdir():
        if p.suffix.lower() == ".pdf" and needle in p.name.lower():
            hits.append(p)
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        print(f"WARNING: match {match!r} hit {len(hits)} files; using first: {hits[0].name}")
        return hits[0]
    return None


def curate_one(client: OpenAI, doc_id: str, pdf_name: str, extract: str) -> dict:
    text = extract[:EXTRACT_CHAR_CAP]
    resp = client.chat.completions.create(
        model=CURATE_MODEL,
        temperature=0.1,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": USER.format(doc_id=doc_id, pdf_name=pdf_name, extract=text)},
        ],
    )
    return json.loads(resp.choices[0].message.content)


def write_outputs(doc_folder: Path, doc_id: str, data: dict) -> None:
    authors = data.get("authors") or []
    if isinstance(authors, str):
        authors = [authors]
    year = str(data.get("year") or "")
    meta = {
        "title": data.get("title") or doc_id,
        "year": year,
        "doi": data.get("doi") or "",
        "url": data.get("url") or "",
        "authors": authors,
        "journal": data.get("journal") or "",
        "language": "",
        "source_type": "",
        "document_type": data.get("document_type") or "",
        "corpus": AREAL_SLUG,
        "priority_questions": data.get("priority_questions") or [],
        "evidence_direction": data.get("evidence_direction") or "not_applicable",
        "controversy_role": data.get("controversy_role") or "not_applicable",
        "quality_signal": data.get("quality_signal") or "medium",
        "quality_rationale": data.get("quality_rationale") or "",
        "consensus_signal": "",
        "relevance_signal": "",
        "key_claims": data.get("key_claims") or [],
        "rag_summary": data.get("rag_summary") or "",
        "included_because": data.get("included_because") or "",
        "related_documents_supporting": [],
        "related_documents_contrasting": [],
        "related_documents_reply_to": [],
        "should_be_read_with": [],
        "coi_declared": "",
        "coi_notes": "",
        "curator_review_status": STATUS_AI_DRAFT,
        "inclusion_decided_by": "Thord Håkon Bakke",
        "added_date": str(date.today()),
        "source_pdf": data.get("_pdf_name") or "",
    }
    doc_folder.mkdir(parents=True, exist_ok=True)
    (doc_folder / "metadata.yaml").write_text(
        yaml.safe_dump(meta, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    brief = (data.get("summary_md") or data.get("rag_summary") or "").strip()
    (doc_folder / "summary.md").write_text(brief + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap area-and-aquaculture corpus")
    parser.add_argument("--doc", help="Only this doc_id")
    parser.add_argument("--skip-extract", action="store_true")
    parser.add_argument("--skip-curate", action="store_true")
    parser.add_argument("--skip-ingest", action="store_true")
    parser.add_argument("--force-curate", action="store_true")
    args = parser.parse_args()

    paths = get_corpus(AREAL_SLUG)
    items = load_manifest(paths)
    if args.doc:
        items = [i for i in items if i["doc_id"] == args.doc]
        if not items:
            print(f"ERROR: {args.doc} not in manifest", file=sys.stderr)
            return 1

    unresolved = []
    resolved = []
    for item in items:
        pdf = find_pdf(paths.pdf_dir, item["match"])
        if pdf is None:
            unresolved.append(item)
        else:
            resolved.append((item, pdf))
    if unresolved:
        print("ERROR: unmatched manifest rows:", file=sys.stderr)
        for u in unresolved:
            print(f"  {u['doc_id']} match={u['match']!r}", file=sys.stderr)
        return 1

    for item, pdf in resolved:
        doc_id = item["doc_id"]
        folder = paths.doc_dir(doc_id)
        folder.mkdir(parents=True, exist_ok=True)
        extract_path = folder / "extracted.md"
        if not args.skip_extract:
            if extract_path.exists() and extract_path.stat().st_size > 200:
                print(f"extract exists {doc_id}", flush=True)
            else:
                print(f"extract {doc_id} <- {pdf.name}", flush=True)
                try:
                    if pdf.stat().st_size >= LARGE_PDF_BYTES:
                        print(f"  large PDF, PyMuPDF first", flush=True)
                        convert_one_pymupdf(pdf, extract_path)
                    else:
                        try:
                            convert_one(pdf, extract_path)
                        except Exception as odl_err:
                            print(f"  ODL failed, PyMuPDF fallback: {odl_err}", flush=True)
                            convert_one_pymupdf(pdf, extract_path)
                    print(f"  wrote {extract_path.stat().st_size} bytes", flush=True)
                except Exception as e:
                    print(f"  EXTRACT FAILED {doc_id}: {e}", file=sys.stderr, flush=True)

    if not args.skip_curate:
        key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not key:
            print("ERROR: OPENAI_API_KEY missing", file=sys.stderr)
            return 1
        client = OpenAI(api_key=key)
        for item, pdf in resolved:
            doc_id = item["doc_id"]
            folder = paths.doc_dir(doc_id)
            meta_path = folder / "metadata.yaml"
            extract_path = folder / "extracted.md"
            if meta_path.exists() and not args.force_curate:
                print(f"curate skip {doc_id} (metadata exists)", flush=True)
                continue
            if not extract_path.exists():
                print(f"curate skip {doc_id} (no extract)", flush=True)
                continue
            extract = extract_path.read_text(encoding="utf-8", errors="replace")
            if len(extract.strip()) < 80:
                print(f"curate skip {doc_id} (extract too short)", flush=True)
                continue
            print(f"curate {doc_id} ({CURATE_MODEL})", flush=True)
            try:
                data = curate_one(client, doc_id, pdf.name, extract)
                data["_pdf_name"] = pdf.name
                write_outputs(folder, doc_id, data)
            except Exception as e:
                print(f"  CURATE FAILED {doc_id}: {e}", file=sys.stderr)

    if not args.skip_ingest:
        import subprocess

        cmd = [sys.executable, str(REPO_ROOT / "scripts" / "ingest.py"), "--corpus", AREAL_SLUG]
        if args.doc:
            cmd.extend(["--doc", args.doc])
        print(">", " ".join(cmd), flush=True)
        r = subprocess.run(cmd, cwd=str(REPO_ROOT))
        return r.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
