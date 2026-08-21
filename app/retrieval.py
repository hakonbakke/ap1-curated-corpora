"""
retrieval.py — Load the corpus and retrieve relevant documents for a query.

Retrieval:
  1. Optional metadata pre-filter (evidence direction, quality, etc.)
  2. Cosine similarity over embeddings of rag_summary + key_claims
  3. retrieve_routed(): infer Q7–Q10 from the query, prefer matching docs, then fill
  4. Light debate expansion via related_contrasting / should_read_with
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

# Cosine similarity floor for "in scope". Spot-checked 2026-08-12:
# on-topic golden queries top1 ≈ 0.42–0.69; clear off-topic top1 ≈ 0.05–0.19.
OUT_OF_SCOPE_SCORE_THRESHOLD = 0.28


def best_retrieval_score(results: list[dict]) -> float:
    """Highest cosine similarity among retrieved docs (ignore missing/zero debate fillers)."""
    if not results:
        return 0.0
    return max(float(r.get("score") or 0.0) for r in results)


def is_out_of_scope(results: list[dict], threshold: float = OUT_OF_SCOPE_SCORE_THRESHOLD) -> bool:
    """True when retrieval is empty or the best hit is below the in-scope floor."""
    return best_retrieval_score(results) < threshold


def corpus_parquet_mtime() -> float:
    """Modification time of corpus.parquet — used to invalidate Streamlit cache after ingest."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Corpus not found at {DATA_FILE}. Run: python scripts/ingest.py"
        )
    return DATA_FILE.stat().st_mtime


@st.cache_resource(show_spinner=False)
def _load_corpus_cached(corpus_mtime: float) -> pd.DataFrame:
    """Load parquet; cache key includes file mtime so re-ingest is picked up automatically."""
    df = pd.read_parquet(DATA_FILE)
    df["_embedding"] = df["embedding"].apply(
        lambda x: np.array(json.loads(x), dtype=np.float32)
    )
    return df


def load_corpus() -> pd.DataFrame:
    """Load corpus from disk (cached until corpus.parquet changes)."""
    return _load_corpus_cached(corpus_parquet_mtime())


def reload_corpus() -> pd.DataFrame:
    """Force reload from disk (e.g. after manual cache confusion)."""
    _load_corpus_cached.clear()
    return load_corpus()


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


# Query → priority-question routing (boost, not hard-only filter)
# Order: more specific population/regulation cues before generic physiology.
_ROUTE_RULES: list[tuple[list[str], list[str]]] = [
    # Population / adult returns (Q9) — must win over smolt/physiology wording
    (
        [
            "bestand", "bestandsnedgang", "population", "adult return", "adult returns",
            "returning adult", "stock decline", "stock collapse", "pre-fishery",
            "pfa", "gytebestand", "returns to spawn", "wild salmon stock",
            "voksne tilbake", "innsig", "innsiger", "dødsårsaker i havet",
            "andre marine", "marine faktorer", "marine stressors",
        ],
        ["Q9"],
    ),
    # Traffic Light System / regulation (Q10)
    (
        [
            "trafikklys", "traffic light", "tls", "produksjonsområde", "production area",
            "capacity regulation", "kapasitetsregulering", "klassifisering",
            "regulatory framework", "ekspertgruppe", "kunnskapsgrunnlag for kapasitet",
            "van nes", "stige et al", "stige mfl",
        ],
        ["Q10"],
    ),
    # Attribution / farm origin (Q1) — BC cessation natural experiments
    (
        [
            "british columbia", "broughton", "oppdrett ble fjernet",
            "aquaculture was removed", "aquaculture removal", "farm removal",
            "lice unchanged", "pacific salmon", "stillehavslaks",
            "opphav", "attribution of lice", "farm-origin", "fra oppdrett",
        ],
        ["Q1"],
    ),
    # Physiology / thresholds / lab–field (Q6) — often with Q7
    (
        [
            "terskel", "terskler", "threshold", "thresholds", "lusnivå", "lusenivå",
            "lab til felt", "laboratory", "osmoregulation", "osmoregulering",
            "dose–respons", "dose-response", "sea trout susceptibility",
            "overførbar", "transferred to sea trout",
        ],
        ["Q6", "Q7"],
    ),
    # Model / PIM / VPS / calibration (Q7–Q8)
    (
        [
            "pim", "vps", "kalibrering", "calibration", "modelldødelighet",
            "model mortality", "sentinel cage", "virtual postsmolt", "virtual post-smolt",
            "smolt mortality estimate", "postsmolt mortality",
            "lusemodell", "operative lusemodell", "overestimate", "overestimer",
            "trawl observation", "trålfanget", "måles på villfisk", "treffer",
        ],
        ["Q7", "Q8"],
    ),
]


def infer_priority_questions(query: str) -> list[str]:
    """Heuristic mapping from user query text to priority question IDs."""
    q = query.lower()
    hits: list[str] = []
    for keywords, questions in _ROUTE_RULES:
        if any(k in q for k in keywords):
            for pq in questions:
                if pq not in hits:
                    hits.append(pq)
    return hits


def _row_to_result(row: pd.Series) -> dict:
    return {
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
        "curator_review_status": row.get("curator_review_status", "") or "",
        "inclusion_decided_by": row.get("inclusion_decided_by", "") or "",
        "added_as_debate_link": False,
        "score": round(float(row["_score"]), 4),
    }


def retrieve(
    client: OpenAI,
    query: str,
    top_k: int = 8,
    filter_priority_questions: list[str] | None = None,
    filter_evidence_direction: list[str] | None = None,
    filter_quality: list[str] | None = None,
    selected_doc_ids: list[str] | None = None,
    query_embedding: np.ndarray | None = None,
) -> list[dict]:
    """
    Retrieve the top_k most relevant documents for a query.

    Returns a list of dicts with document metadata + similarity score,
    sorted by descending relevance.
    """
    df = load_corpus()
    query_vec = query_embedding if query_embedding is not None else get_embedding(client, query)

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
    return [_row_to_result(row) for _, row in top.iterrows()]


def retrieve_routed(
    client: OpenAI,
    query: str,
    top_k: int = 8,
    selected_doc_ids: list[str] | None = None,
) -> tuple[list[dict], list[str]]:
    """
    Two-pass retrieval: prefer docs tagged with inferred priority questions,
    then fill remaining slots from the unfiltered pool.

    Returns (results, inferred_priority_questions).
    """
    routed_qs = infer_priority_questions(query)
    query_vec = get_embedding(client, query)

    if not routed_qs:
        return retrieve(
            client,
            query,
            top_k=top_k,
            selected_doc_ids=selected_doc_ids,
            query_embedding=query_vec,
        ), routed_qs

    # Pass 1: metadata-boosted pool
    primary = retrieve(
        client,
        query,
        top_k=top_k,
        filter_priority_questions=routed_qs,
        selected_doc_ids=selected_doc_ids,
        query_embedding=query_vec,
    )
    if len(primary) >= top_k:
        return _expand_debate_links(primary[:top_k], selected_doc_ids), routed_qs

    # Pass 2: fill from full corpus (exclude already picked)
    have = {r["doc_id"] for r in primary}
    filler = retrieve(
        client,
        query,
        top_k=top_k,
        selected_doc_ids=selected_doc_ids,
        query_embedding=query_vec,
    )
    for r in filler:
        if r["doc_id"] not in have:
            primary.append(r)
            have.add(r["doc_id"])
        if len(primary) >= top_k:
            break

    # Prefer routed docs first in prompt order, then by score
    def sort_key(r: dict) -> tuple:
        pq = set(r.get("priority_questions") or [])
        match = 1 if pq.intersection(routed_qs) else 0
        return (-match, -r["score"])

    primary = sorted(primary[:top_k], key=sort_key)
    return _expand_debate_links(primary, selected_doc_ids), routed_qs


def _expand_debate_links(
    results: list[dict],
    selected_doc_ids: list[str] | None,
) -> list[dict]:
    """Append up to 3 related_contrasting / should_read_with docs beyond top_k.

    These extras are marked added_as_debate_link so the UI can separate them
    from similarity hits. They still enter synthesis.
    """
    df = load_corpus()
    have = {r["doc_id"] for r in results}
    allowed = set(selected_doc_ids) if selected_doc_ids is not None else None
    extras: list[str] = []
    for r in results:
        for rel in (r.get("related_contrasting") or []) + (r.get("should_read_with") or []):
            rel = (rel or "").strip()
            if not rel or rel in have:
                continue
            if allowed is not None and rel not in allowed:
                continue
            if rel in set(df["doc_id"]):
                extras.append(rel)

    if not extras:
        return results

    id_to_row = {row["doc_id"]: row for _, row in df.iterrows()}
    for doc_id in extras[:3]:
        if doc_id in have:
            continue
        row = id_to_row.get(doc_id)
        if row is None:
            continue
        row = row.copy()
        row["_score"] = 0.0
        extra = _row_to_result(row)
        extra["added_as_debate_link"] = True
        results.append(extra)
        have.add(doc_id)
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
