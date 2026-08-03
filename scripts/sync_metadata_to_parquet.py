"""
Sync selected metadata.yaml fields into data/corpus.parquet WITHOUT re-embedding.

No OpenAI API calls. Use after offline status / evidence_direction edits.

Usage:
    python scripts/sync_metadata_to_parquet.py
    python scripts/sync_metadata_to_parquet.py --strict
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_paths import DATA_FILE, list_doc_ids, doc_dir, strip_yaml_comments  # noqa: E402
from ingest import RETRIEVAL_TEXT_FIELDS  # noqa: E402 — keep in sync with build_retrieval_text

SYNC_STR = [
    "evidence_direction",
    "effect_scale",
    "consensus_signal",
    "controversy_role",
    "quality_signal",
    "relevance_signal",
    "curator_review_status",
    "rag_summary",
    "included_because",
    "coi_declared",
    "inclusion_decided_by",
    "added_by",
]
SYNC_LIST = [
    "priority_questions",
    "key_claims",
    "related_documents_supporting",
    "related_documents_contrasting",
    "related_documents_reply_to",
    "should_be_read_with",
]
LIST_COL = {
    "related_documents_supporting": "related_supporting",
    "related_documents_contrasting": "related_contrasting",
    "related_documents_reply_to": "related_reply_to",
    "should_be_read_with": "should_read_with",
}

STALE_FILE = DATA_FILE.parent / "stale_embeddings.txt"


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync metadata into corpus.parquet without re-embedding")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any synced change affects retrieval_text fields (stale embeddings).",
    )
    args = parser.parse_args()

    if not DATA_FILE.exists():
        print(f"ERROR: missing {DATA_FILE}", file=sys.stderr)
        return 1
    df = pd.read_parquet(DATA_FILE)
    # Ensure optional trust columns exist
    for col in ("inclusion_decided_by", "added_by"):
        if col not in df.columns:
            df[col] = ""

    updated = 0
    stale_ids: list[str] = []

    for doc_id in list_doc_ids():
        meta_path = doc_dir(doc_id) / "metadata.yaml"
        if not meta_path.exists():
            continue
        meta = yaml.safe_load(strip_yaml_comments(meta_path.read_text(encoding="utf-8"))) or {}
        idx = df.index[df["doc_id"] == doc_id]
        if len(idx) == 0:
            print(f"SKIP {doc_id}: not in parquet")
            continue
        i = idx[0]
        changed = False
        retrieval_affecting = False

        for key in SYNC_STR:
            if key not in meta:
                continue
            val = meta.get(key)
            new = "" if val is None else str(val)
            old = str(df.at[i, key] if key in df.columns else "")
            if old != new:
                if key not in df.columns:
                    df[key] = ""
                df.at[i, key] = new
                changed = True
                if key in RETRIEVAL_TEXT_FIELDS:
                    retrieval_affecting = True

        for key in SYNC_LIST:
            if key not in meta:
                continue
            col = LIST_COL.get(key, key)
            if col not in df.columns:
                continue
            v = meta.get(key) or []
            if not isinstance(v, list):
                v = [v]
            new = json.dumps([str(x) for x in v if x])
            if df.at[i, col] != new:
                df.at[i, col] = new
                changed = True
                if key in RETRIEVAL_TEXT_FIELDS:
                    retrieval_affecting = True

        summary_path = doc_dir(doc_id) / "summary.md"
        if summary_path.exists() and "summary_text" in df.columns:
            text = summary_path.read_text(encoding="utf-8").strip()
            if df.at[i, "summary_text"] != text:
                df.at[i, "summary_text"] = text
                changed = True
                # summary_text only feeds embeddings when rag_summary is empty
                rag = (meta.get("rag_summary") or "").strip()
                if not rag:
                    retrieval_affecting = True

        if changed:
            updated += 1
            print(f"updated {doc_id}")
            if retrieval_affecting:
                stale_ids.append(doc_id)

    df.to_parquet(DATA_FILE, index=False)
    print(f"Saved {DATA_FILE} ({updated} docs changed; embeddings untouched)")

    if stale_ids:
        STALE_FILE.write_text("\n".join(stale_ids) + "\n", encoding="utf-8")
        print("")
        print("WARNING: retrieval_text source fields changed; embeddings may be STALE for:")
        for doc_id in stale_ids:
            print(f"  - {doc_id}")
            print(f"    fix: python scripts/ingest.py --doc {doc_id}")
        print(f"Listed in {STALE_FILE}")
        if args.strict:
            return 1
    elif STALE_FILE.exists():
        # Clear when this sync introduced no new staleness (file may be stale itself)
        pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
