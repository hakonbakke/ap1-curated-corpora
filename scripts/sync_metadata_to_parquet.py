"""
Sync selected metadata.yaml fields into data/corpus.parquet WITHOUT re-embedding.

No OpenAI API calls. Use after offline status / evidence_direction edits.

Usage:
    python scripts/sync_metadata_to_parquet.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_paths import DATA_FILE, list_doc_ids, doc_dir, strip_yaml_comments  # noqa: E402

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


def main() -> int:
    if not DATA_FILE.exists():
        print(f"ERROR: missing {DATA_FILE}", file=sys.stderr)
        return 1
    df = pd.read_parquet(DATA_FILE)
    updated = 0
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
        for key in SYNC_STR:
            if key not in meta:
                continue
            val = meta.get(key)
            new = "" if val is None else str(val)
            if str(df.at[i, key] if key in df.columns else "") != new:
                if key in df.columns:
                    df.at[i, key] = new
                    changed = True
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
        summary_path = doc_dir(doc_id) / "summary.md"
        if summary_path.exists() and "summary_text" in df.columns:
            text = summary_path.read_text(encoding="utf-8").strip()
            if df.at[i, "summary_text"] != text:
                df.at[i, "summary_text"] = text
                changed = True
        if changed:
            updated += 1
            print(f"updated {doc_id}")
    df.to_parquet(DATA_FILE, index=False)
    print(f"Saved {DATA_FILE} ({updated} docs changed; embeddings untouched)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
