"""
ingest.py — Build or update the corpus embedding store.

Reads each document's metadata.yaml + summary.md from the documents/ folder,
builds a retrieval text, generates an OpenAI embedding, and saves everything
to data/corpus.parquet.

Usage (from repo root):
    python scripts/ingest.py

To update a single document after editing its metadata/summary:
    python scripts/ingest.py --doc 2025_jae_jansen-lice-effects-returns

Requires OPENAI_API_KEY in .env or environment.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

REPO_ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = REPO_ROOT / "corpora" / "salmon-lice-and-mortality-of-wild-salmonids" / "documents"
DATA_FILE = REPO_ROOT / "data" / "corpus.parquet"
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIM = 3072


def load_document(doc_dir: Path) -> dict | None:
    """Load metadata.yaml and summary.md for one document folder."""
    meta_path = doc_dir / "metadata.yaml"
    summary_path = doc_dir / "summary.md"

    if not meta_path.exists():
        print(f"  SKIP {doc_dir.name}: no metadata.yaml")
        return None

    with open(meta_path, encoding="utf-8") as f:
        raw = f.read()

    # Strip YAML comment lines so pyyaml doesn't choke
    clean = "\n".join(
        line for line in raw.splitlines()
        if not line.lstrip().startswith("#") or line.strip() == "#"
    )
    try:
        meta = yaml.safe_load(clean) or {}
    except yaml.YAMLError as e:
        print(f"  SKIP {doc_dir.name}: YAML parse error — {e}")
        return None

    summary_text = ""
    if summary_path.exists():
        summary_text = summary_path.read_text(encoding="utf-8").strip()

    return {"doc_id": doc_dir.name, "meta": meta, "summary_text": summary_text}


def build_retrieval_text(doc: dict) -> str:
    """
    Concatenate the fields most useful for semantic retrieval into one string.
    Order: rag_summary (most retrieval-optimised) → key_claims → summary_text excerpt.
    """
    meta = doc["meta"]
    parts: list[str] = []

    title = meta.get("title", "")
    year = meta.get("year", "")
    if title:
        parts.append(f"Title: {title} ({year})")

    rag_summary = meta.get("rag_summary", "")
    if rag_summary and rag_summary.strip():
        parts.append(rag_summary.strip())

    key_claims = meta.get("key_claims", []) or []
    if key_claims:
        claim_text = " ".join(str(c) for c in key_claims if c and str(c).strip())
        if claim_text:
            parts.append("Key claims: " + claim_text)

    uncertainty = meta.get("claims_about_uncertainty", []) or []
    if uncertainty:
        unc_text = " ".join(str(u) for u in uncertainty if u and str(u).strip())
        if unc_text:
            parts.append("Uncertainty: " + unc_text)

    policy_claims = meta.get("claims_about_policy_or_management", []) or []
    if policy_claims:
        pol_text = " ".join(str(p) for p in policy_claims if p and str(p).strip())
        if pol_text:
            parts.append("Policy relevance: " + pol_text)

    # Fall back to summary.md excerpt if rag_summary is missing
    if not rag_summary and doc["summary_text"]:
        parts.append(doc["summary_text"][:1500])

    return "\n\n".join(parts)


def embed_texts(client: OpenAI, texts: list[str]) -> list[list[float]]:
    """Call OpenAI embeddings API in one batch (max 2048 inputs)."""
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


def row_from_doc(doc: dict, embedding: list[float]) -> dict:
    """Flatten metadata + embedding into a single dict for a DataFrame row."""
    meta = doc["meta"]

    def listval(key: str) -> str:
        v = meta.get(key, []) or []
        if isinstance(v, list):
            return json.dumps([str(x) for x in v if x])
        return json.dumps([str(v)]) if v else "[]"

    def strval(key: str, default: str = "") -> str:
        v = meta.get(key, default)
        return str(v) if v else default

    authors = meta.get("authors", []) or []
    authors_str = "; ".join(str(a) for a in authors if a)

    return {
        "doc_id": doc["doc_id"],
        "title": strval("title"),
        "year": strval("year"),
        "doi": strval("doi"),
        "url": strval("url"),
        "authors": authors_str,
        "journal": strval("journal"),
        "document_type": strval("document_type"),
        "evidence_direction": strval("evidence_direction"),
        "effect_scale": strval("effect_scale"),
        "consensus_signal": strval("consensus_signal"),
        "controversy_role": strval("controversy_role"),
        "quality_signal": strval("quality_signal"),
        "relevance_signal": strval("relevance_signal"),
        "uncertainty_emphasis": strval("uncertainty_emphasis"),
        "wild_or_farmed_focus": strval("wild_or_farmed_focus"),
        "priority_questions": listval("priority_questions"),
        "causal_chain_stage": listval("causal_chain_stage"),
        "outcome_domain": listval("outcome_domain"),
        "host_species": listval("host_species"),
        "life_stage": listval("life_stage"),
        "geography": listval("geography"),
        "environment": listval("environment"),
        "regulatory_context": listval("regulatory_context"),
        "evidence_type": strval("evidence_type"),
        "time_period": strval("time_period"),
        "related_supporting": listval("related_documents_supporting"),
        "related_contrasting": listval("related_documents_contrasting"),
        "related_reply_to": listval("related_documents_reply_to"),
        "should_read_with": listval("should_be_read_with"),
        "retrieval_tags": listval("retrieval_tags"),
        "key_claims": listval("key_claims"),
        "rag_summary": strval("rag_summary"),
        "included_because": strval("included_because"),
        "quality_rationale": strval("quality_rationale"),
        "coi_declared": strval("coi_declared"),
        "coi_notes": strval("coi_notes"),
        "curator_review_status": strval("curator_review_status"),
        "summary_text": doc["summary_text"],
        "retrieval_text": build_retrieval_text(doc),
        "embedding": json.dumps(embedding),
    }


def load_existing() -> pd.DataFrame | None:
    if DATA_FILE.exists():
        return pd.read_parquet(DATA_FILE)
    return None


def save(df: pd.DataFrame) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(DATA_FILE, index=False)
    print(f"\nSaved {len(df)} documents -> {DATA_FILE}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest AP1 corpus documents into corpus.parquet")
    parser.add_argument(
        "--doc", metavar="DOC_ID",
        help="Process only this document folder name (upsert). Omit to process all."
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Parse and print documents without calling the API or writing output."
    )
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key and not args.dry_run:
        print("ERROR: OPENAI_API_KEY not set. Add it to .env or set it in the environment.", file=sys.stderr)
        return 1

    client = OpenAI(api_key=api_key) if not args.dry_run else None

    # Find document folders to process
    if args.doc:
        target = CORPUS_DIR / args.doc
        if not target.is_dir():
            print(f"ERROR: Document folder not found: {target}", file=sys.stderr)
            return 1
        doc_dirs = [target]
    else:
        doc_dirs = sorted(
            d for d in CORPUS_DIR.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        )

    print(f"Processing {len(doc_dirs)} document(s)...")

    # Load and parse
    docs = []
    for d in doc_dirs:
        doc = load_document(d)
        if doc:
            docs.append(doc)
            print(f"  loaded  {d.name}")

    if not docs:
        print("No documents loaded. Nothing to do.")
        return 0

    if args.dry_run:
        for doc in docs:
            print(f"\n=== {doc['doc_id']} ===")
            print(build_retrieval_text(doc)[:400])
        return 0

    # Embed
    print(f"\nEmbedding {len(docs)} document(s) with {EMBEDDING_MODEL}...")
    texts = [build_retrieval_text(doc) for doc in docs]
    t0 = time.time()
    embeddings = embed_texts(client, texts)
    print(f"  done in {time.time() - t0:.1f}s")

    # Build rows
    new_rows = [row_from_doc(doc, emb) for doc, emb in zip(docs, embeddings)]
    new_df = pd.DataFrame(new_rows)

    # Upsert into existing parquet
    existing = load_existing()
    if existing is not None and args.doc:
        # Remove the old row for this doc and append the new one
        existing = existing[existing["doc_id"] != args.doc].copy()
        final_df = pd.concat([existing, new_df], ignore_index=True)
        print(f"Upserted {args.doc} into existing store ({len(final_df)} total).")
    elif existing is not None and not args.doc:
        # Full rebuild: replace everything
        final_df = new_df
        print(f"Full rebuild: {len(final_df)} documents.")
    else:
        final_df = new_df
        print(f"Created new store: {len(final_df)} documents.")

    save(final_df)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
