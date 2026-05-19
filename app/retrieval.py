"""
retrieval.py — Load the corpus and retrieve relevant documents for a query.

Two-stage retrieval:
  1. Optional metadata pre-filter (evidence direction, quality, etc.)
  2. Cosine similarity search over embeddings of rag_summary + key_claims
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from openai import OpenAI

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "corpus.parquet"
EMBEDDING_MODEL = "text-embedding-3-large"


@st.cache_resource(show_spinner=False)
def load_corpus() -> pd.DataFrame:
    """Load the parquet file once and cache for the session."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Corpus not found at {DATA_FILE}. Run: python scripts/ingest.py"
        )
    df = pd.read_parquet(DATA_FILE)
    # Parse embedding column from JSON string to numpy arrays
    df["_embedding"] = df["embedding"].apply(lambda x: np.array(json.loads(x), dtype=np.float32))
    return df


def get_embedding(client: OpenAI, text: str) -> np.ndarray:
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=[text])
    return np.array(response.data[0].embedding, dtype=np.float32)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))


def json_list_contains(json_str: str, values: list[str]) -> bool:
    """Check if any of the given values appear in a JSON-encoded list column."""
    if not json_str or not values:
        return True
    try:
        items = json.loads(json_str)
        return any(v in items for v in values)
    except (json.JSONDecodeError, TypeError):
        return True


def retrieve(
    client: OpenAI,
    query: str,
    top_k: int = 8,
    filter_priority_questions: list[str] | None = None,
    filter_evidence_direction: list[str] | None = None,
    filter_quality: list[str] | None = None,
    selected_doc_ids: list[str] | None = None,
) -> list[dict]:
    """
    Retrieve the top_k most relevant documents for a query.

    Returns a list of dicts with document metadata + similarity score,
    sorted by descending relevance.
    """
    df = load_corpus()
    query_vec = get_embedding(client, query)

    # Metadata pre-filtering
    mask = pd.Series([True] * len(df), index=df.index)

    if selected_doc_ids is not None:
        mask &= df["doc_id"].isin(selected_doc_ids)

    if filter_priority_questions:
        mask &= df["priority_questions"].apply(
            lambda x: json_list_contains(x, filter_priority_questions)
        )

    if filter_evidence_direction:
        mask &= df["evidence_direction"].isin(filter_evidence_direction)

    if filter_quality:
        mask &= df["quality_signal"].isin(filter_quality)

    filtered = df[mask].copy()

    if filtered.empty:
        return []

    # Cosine similarity
    filtered["_score"] = filtered["_embedding"].apply(
        lambda emb: cosine_similarity(query_vec, emb)
    )

    top = filtered.nlargest(top_k, "_score")

    results = []
    for _, row in top.iterrows():
        results.append({
            "doc_id": row["doc_id"],
            "title": row["title"],
            "year": row["year"],
            "doi": row["doi"],
            "url": row.get("url", ""),
            "authors": row["authors"],
            "journal": row["journal"],
            "document_type": row["document_type"],
            "evidence_direction": row["evidence_direction"],
            "effect_scale": row["effect_scale"],
            "consensus_signal": row["consensus_signal"],
            "controversy_role": row["controversy_role"],
            "quality_signal": row["quality_signal"],
            "relevance_signal": row["relevance_signal"],
            "priority_questions": json.loads(row["priority_questions"] or "[]"),
            "causal_chain_stage": json.loads(row["causal_chain_stage"] or "[]"),
            "outcome_domain": json.loads(row["outcome_domain"] or "[]"),
            "key_claims": json.loads(row["key_claims"] or "[]"),
            "rag_summary": row["rag_summary"],
            "summary_text": row["summary_text"],
            "related_supporting": json.loads(row["related_supporting"] or "[]"),
            "related_contrasting": json.loads(row["related_contrasting"] or "[]"),
            "related_reply_to": json.loads(row["related_reply_to"] or "[]"),
            "should_read_with": json.loads(row["should_read_with"] or "[]"),
            "included_because": row["included_because"],
            "coi_declared": row["coi_declared"],
            "score": round(row["_score"], 4),
        })

    return results


def build_debate_map(results: list[dict], all_docs: pd.DataFrame) -> list[dict]:
    """
    Identify explicit disagreement chains from the retrieved documents.
    Returns a list of (source_doc, target_doc, relation) tuples.
    """
    doc_ids_in_results = {r["doc_id"] for r in results}
    id_to_title = dict(zip(all_docs["doc_id"], all_docs["title"]))

    edges = []
    for r in results:
        for contrasting in r["related_contrasting"]:
            contrasting = contrasting.strip()
            if contrasting and contrasting in doc_ids_in_results:
                edges.append({
                    "from": r["doc_id"],
                    "from_title": r["title"],
                    "to": contrasting,
                    "to_title": id_to_title.get(contrasting, contrasting),
                    "relation": "contradicts",
                })
        for reply in r["related_reply_to"]:
            reply = reply.strip()
            if reply and reply in doc_ids_in_results:
                edges.append({
                    "from": r["doc_id"],
                    "from_title": r["title"],
                    "to": reply,
                    "to_title": id_to_title.get(reply, reply),
                    "relation": "replies_to",
                })
    return edges
