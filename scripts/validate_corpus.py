"""
Validate salmon-lice corpus metadata against vocabulary.json + template.

No API / network. Exit 1 if any error-severity violation.

Usage:
    python scripts/validate_corpus.py
    python scripts/validate_corpus.py --doc 2025_jae_jansen-lice-effects-returns
    python scripts/validate_corpus.py --quiet
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_paths import (  # noqa: E402
    CORPUS,
    DATA_FILE,
    DOCS_DIR,
    TEMPLATE_PATH,
    doc_dir,
    list_doc_ids,
    strip_yaml_comments,
)

VOCAB_PATH = CORPUS / "vocabulary.json"
VIOLATIONS_CSV = Path(__file__).resolve().parent.parent / "qa_vocabulary_violations.csv"
DOC_ID_RE = re.compile(r"^\d{4}_[a-z0-9]+_[a-z0-9-]+$")
EXPECTED_FILES = ("extracted.md", "summary.md", "metadata.yaml", "qa_report.json")


def _coerce_scalar(val) -> str | None:
    if val is None:
        return None
    if isinstance(val, bool):
        return "yes" if val else "no"
    if isinstance(val, (int, float)) and not isinstance(val, bool):
        return str(val)
    s = str(val).strip()
    return s if s else None


def _as_list(val) -> list:
    if val is None:
        return []
    if isinstance(val, list):
        return val
    return [val]


def template_keys() -> list[str]:
    raw = TEMPLATE_PATH.read_text(encoding="utf-8")
    meta = yaml.safe_load(strip_yaml_comments(raw)) or {}
    return list(meta.keys())


def load_vocab() -> dict:
    return json.loads(VOCAB_PATH.read_text(encoding="utf-8"))


def validate_doc(doc_id: str, vocab: dict, tmpl_keys: list[str]) -> list[dict]:
    rows: list[dict] = []
    d = doc_dir(doc_id)

    if not DOC_ID_RE.match(doc_id):
        rows.append(
            {
                "doc_id": doc_id,
                "field": "doc_id",
                "severity": "error",
                "found_value": doc_id,
                "expected": "YYYY_outlet_keyword pattern",
            }
        )

    for fname in EXPECTED_FILES:
        if not (d / fname).exists():
            rows.append(
                {
                    "doc_id": doc_id,
                    "field": fname,
                    "severity": "error",
                    "found_value": "MISSING",
                    "expected": "file present",
                }
            )

    meta_path = d / "metadata.yaml"
    if not meta_path.exists():
        return rows

    try:
        meta = yaml.safe_load(strip_yaml_comments(meta_path.read_text(encoding="utf-8"))) or {}
    except yaml.YAMLError as e:
        rows.append(
            {
                "doc_id": doc_id,
                "field": "metadata.yaml",
                "severity": "error",
                "found_value": str(e)[:200],
                "expected": "valid YAML",
            }
        )
        return rows

    for key in tmpl_keys:
        if key not in meta:
            rows.append(
                {
                    "doc_id": doc_id,
                    "field": key,
                    "severity": "error",
                    "found_value": "MISSING_KEY",
                    "expected": "present in metadata_template.yaml",
                }
            )
        else:
            val = meta.get(key)
            empty = val is None or val == "" or val == [] or val == {}
            if empty and key in vocab.get("required_fields", []):
                rows.append(
                    {
                        "doc_id": doc_id,
                        "field": key,
                        "severity": "warning",
                        "found_value": "EMPTY",
                        "expected": "non-empty (recommended)",
                    }
                )

    for key in meta:
        if key not in tmpl_keys:
            rows.append(
                {
                    "doc_id": doc_id,
                    "field": key,
                    "severity": "error",
                    "found_value": "EXTRA_KEY",
                    "expected": "key in metadata_template.yaml",
                }
            )

    scalars = vocab.get("scalar_fields", {})
    lists = vocab.get("list_fields", {})
    legacy_status = set(vocab.get("legacy_curator_review_status", []))

    for field, allowed in scalars.items():
        if field not in meta:
            continue
        found = _coerce_scalar(meta.get(field))
        if found is None:
            continue
        if field == "curator_review_status" and found in legacy_status:
            rows.append(
                {
                    "doc_id": doc_id,
                    "field": field,
                    "severity": "warning",
                    "found_value": found,
                    "expected": "migrate to ai_draft|ai_verified|expert_approved",
                }
            )
            continue
        if found not in allowed:
            rows.append(
                {
                    "doc_id": doc_id,
                    "field": field,
                    "severity": "error",
                    "found_value": found,
                    "expected": "|".join(allowed),
                }
            )

    for field, allowed in lists.items():
        if field not in meta:
            continue
        for item in _as_list(meta.get(field)):
            found = _coerce_scalar(item)
            if found is None:
                continue
            if found not in allowed:
                rows.append(
                    {
                        "doc_id": doc_id,
                        "field": field,
                        "severity": "error",
                        "found_value": found,
                        "expected": "controlled vocabulary (see vocabulary.json)",
                    }
                )

    return rows


def parquet_orphans(doc_ids: list[str]) -> list[dict]:
    rows: list[dict] = []
    if not DATA_FILE.exists():
        rows.append(
            {
                "doc_id": "(corpus)",
                "field": "corpus.parquet",
                "severity": "error",
                "found_value": "MISSING",
                "expected": str(DATA_FILE),
            }
        )
        return rows
    df = pd.read_parquet(DATA_FILE)
    on_disk = set(doc_ids)
    in_pq = set(df["doc_id"].astype(str))
    for missing in sorted(on_disk - in_pq):
        rows.append(
            {
                "doc_id": missing,
                "field": "corpus.parquet",
                "severity": "error",
                "found_value": "NOT_IN_PARQUET",
                "expected": "row present",
            }
        )
    for orphan in sorted(in_pq - on_disk):
        rows.append(
            {
                "doc_id": orphan,
                "field": "corpus.parquet",
                "severity": "error",
                "found_value": "ORPHAN_IN_PARQUET",
                "expected": "folder on disk",
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    vocab = load_vocab()
    tmpl_keys = template_keys()
    docs = [args.doc] if args.doc else list_doc_ids()

    all_rows: list[dict] = []
    for doc_id in docs:
        all_rows.extend(validate_doc(doc_id, vocab, tmpl_keys))
    if not args.doc:
        all_rows.extend(parquet_orphans(list_doc_ids()))

    with VIOLATIONS_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f, fieldnames=["doc_id", "field", "severity", "found_value", "expected"]
        )
        w.writeheader()
        w.writerows(all_rows)

    errors = [r for r in all_rows if r["severity"] == "error"]
    warnings = [r for r in all_rows if r["severity"] == "warning"]

    if not args.quiet:
        print(f"Validated {len(docs)} document(s)")
        print(f"errors={len(errors)} warnings={len(warnings)}")
        print(f"Wrote {VIOLATIONS_CSV}")
        by_doc: dict[str, list] = {}
        for r in all_rows:
            by_doc.setdefault(r["doc_id"], []).append(r)
        for doc_id, items in sorted(by_doc.items()):
            print(f"\n## {doc_id}")
            for r in items:
                print(
                    f"  [{r['severity']}] {r['field']}: {r['found_value'][:80]}"
                )

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
