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
import math
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from openai import OpenAI

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "corpus.parquet"
AREAL_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "area-and-aquaculture.parquet"
EMBEDDING_MODEL = "text-embedding-3-large"

# Cosine similarity floor for "in scope". Spot-checked 2026-08-12:
# on-topic golden queries top1 ≈ 0.42–0.69; clear off-topic top1 ≈ 0.05–0.19.
OUT_OF_SCOPE_SCORE_THRESHOLD = 0.28


def best_retrieval_score(results: list[dict]) -> float:
    """Highest cosine similarity among retrieved docs (ignore missing/zero debate fillers)."""
    if not results:
        return 0.0
    return max(float(r.get("semantic_score", r.get("score")) or 0.0) for r in results)


def is_out_of_scope(results: list[dict], threshold: float = OUT_OF_SCOPE_SCORE_THRESHOLD) -> bool:
    """True when retrieval is empty or the best hit is below the in-scope floor."""
    return best_retrieval_score(results) < threshold


_AREAL_EXCLUSION_TERMS = (
    "antibiotik", "boligutbygging", "parkeringskrav", "utvandrende villaksesmolt",
    "smoltdødelighet", "smoltdodelighet", "dødelighet for villaks", "dodelighet for villaks",
)
_AREAL_CONTEXT_TERMS = (
    "sjøareal", "sea area", "arealplan", "area planning", "lokalitet", "locality",
    "site", "tillatelse", "permit", "designation", "utpeking",
)


def is_areal_out_of_scope(query: str, results: list[dict], threshold: float = OUT_OF_SCOPE_SCORE_THRESHOLD) -> bool:
    """Apply the semantic floor plus explicit non-Areal topic guards."""
    normalized = unicodedata.normalize("NFKC", query or "").casefold()
    if is_out_of_scope(results, threshold):
        return True
    has_areal_context = any(term in normalized for term in _AREAL_CONTEXT_TERMS)
    return any(term in normalized for term in _AREAL_EXCLUSION_TERMS) and not has_areal_context


def corpus_parquet_mtime(data_file: Path | None = None) -> float:
    """Modification time of a corpus parquet. Used to invalidate Streamlit cache after ingest."""
    path = Path(data_file) if data_file is not None else DATA_FILE
    if not path.exists():
        raise FileNotFoundError(
            f"Corpus not found at {path}. Run ingest for that corpus."
        )
    return path.stat().st_mtime


@st.cache_resource(show_spinner=False)
def _load_corpus_cached(path_str: str, corpus_mtime: float) -> pd.DataFrame:
    """Load parquet; cache key includes path and mtime so rooms stay isolated."""
    df = pd.read_parquet(path_str)
    df["_embedding"] = df["embedding"].apply(
        lambda x: np.array(json.loads(x), dtype=np.float32)
    )
    return df


def load_corpus(data_file: Path | None = None) -> pd.DataFrame:
    """Load a corpus parquet (cached until that file changes)."""
    path = Path(data_file) if data_file is not None else DATA_FILE
    return _load_corpus_cached(str(path), corpus_parquet_mtime(path))


def reload_corpus(data_file: Path | None = None) -> pd.DataFrame:
    """Force reload from disk (e.g. after manual cache confusion)."""
    _load_corpus_cached.clear()
    return load_corpus(data_file)


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


def _json_list(value: object) -> list[str]:
    """Decode a parquet JSON-list cell without failing on missing legacy columns."""
    if isinstance(value, list):
        return [str(v) for v in value if v]
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    try:
        parsed = json.loads(str(value) or "[]")
    except (json.JSONDecodeError, TypeError):
        return []
    if not isinstance(parsed, list):
        parsed = [parsed]
    return [str(v) for v in parsed if v]


_TOKEN_RE = re.compile(r"[^\W_]+", re.UNICODE)
_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "how",
    "in", "is", "it", "of", "on", "or", "that", "the", "to", "what", "when",
    "where", "which", "who", "with", "og", "i", "på", "av", "er", "et", "en",
    "for", "fra", "har", "hva", "hvordan", "hvor", "med", "når", "om", "som",
    "til", "ved", "eller", "den", "det", "de",
}


def _tokens(text: object) -> set[str]:
    normalized = unicodedata.normalize("NFKC", str(text or "")).casefold()
    return {t for t in _TOKEN_RE.findall(normalized) if len(t) > 1 and t not in _STOPWORDS}


def lexical_scores(query: str, texts: list[str]) -> list[float]:
    """IDF-weighted query coverage in each document (0..1)."""
    query_tokens = _tokens(query)
    if not query_tokens:
        return [0.0] * len(texts)
    doc_tokens = [_tokens(text) for text in texts]
    n_docs = max(1, len(doc_tokens))
    idf = {
        token: math.log((n_docs + 1) / (1 + sum(token in tokens for tokens in doc_tokens))) + 1
        for token in query_tokens
    }
    denominator = sum(idf.values()) or 1.0
    return [sum(idf[t] for t in query_tokens.intersection(tokens)) / denominator for tokens in doc_tokens]
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


_AREAL_ROUTE_RULES: list[tuple[str, list[str]]] = [
    ("A1", ["plan", "plankart", "kystsoneplan", "utpeking", "avsatt", "designation", "dispensasjon", "dispensation", "innsigelse", "objection", "municipality"]),
    ("A2", ["tillatelse", "lokalitetssøknad", "lokalitetstillatelse", "akvakulturloven", "avslag", "permit", "licence", "license", "fylkeskommune"]),
    ("A3", ["sameksistens", "avveiing", "samlet belastning", "annen bruk", "naturverdi", "coexistence", "trade-off", "cumulative", "havvind"]),
    ("A4", ["kunnskap", "konsekvensutredning", "føre var", "usikkerhet", "saksfil", "grunnkart", "knowledge", "impact assessment", "precaution"]),
    ("A5", ["tetthet", "avstand", "biosikkerhet", "sykdom", "lus", "velferd", "bæreevne", "density", "spacing", "biosecurity", "disease", "welfare"]),
    ("A6", ["skatt", "fond", "havbruksfond", "arealavgift", "kommunal vilje", "økonomi", "tax", "fund", "municipal willingness", "local revenue"]),
]
_AREAL_A0_TERMS = [
    "hva begrenser", "begrense vekst", "arealknapphet", "ledig sjø", "mer areal",
    "what limits", "limit growth", "area scarcity", "unused sea", "more area",
]


def infer_areal_priority_questions(query: str) -> list[str]:
    """Map Areal questions to A0–A6. A0 remains a query route, not a document tag."""
    q = unicodedata.normalize("NFKC", query).casefold()
    hits = [code for code, terms in _AREAL_ROUTE_RULES if any(term in q for term in terms)]
    if any(term in q for term in _AREAL_A0_TERMS):
        return ["A0", *hits]
    return hits


def areal_route_match_score(priority_questions: object, tagged_routes: set[str]) -> float:
    """Full route credit if the paper matches any inferred A1-A6 code.

    Do not require every inferred code. An A1 designation question also
    contains «avslag», which adds A2. Papers tagged only A1 (Kvalvik,
    Helgeland) must not lose half the boost to kitchen-sink A1+A2 tags.
    """
    if not tagged_routes:
        return 0.0
    return 1.0 if tagged_routes.intersection(_json_list(priority_questions)) else 0.0


# Files in these groups must not be presented as independent corroboration.
_PUBLICATION_GROUPS = (
    frozenset({"2017_kvalvik_intermunicipal-coastal-planning", "2017_kvalvik_ocean-coastal-management"}),
    frozenset({"2022_ipbes_values-assessment", "2022_ipbes_spm-values"}),
)
_EVIDENCE_FAMILIES = (
    frozenset({"2024_sordahl_when-all-you-have-is-a-hammer", "2026_sordahl_nar-alt-skal-med"}),
)


def publication_group(doc_id: str) -> str:
    for group in _PUBLICATION_GROUPS:
        if doc_id in group:
            return "publication:" + sorted(group)[0]
    return "publication:" + doc_id


def evidence_family(doc_id: str) -> str:
    for group in (*_PUBLICATION_GROUPS, *_EVIDENCE_FAMILIES):
        if doc_id in group:
            return "family:" + sorted(group)[0]
    return "family:" + doc_id


def _row_to_result(row: pd.Series) -> dict:
    def value(name: str, default: str = "") -> str:
        v = row.get(name, default)
        if v is None or (isinstance(v, float) and pd.isna(v)):
            return default
        return str(v)

    doc_id = value("doc_id")
    return {
        "doc_id": doc_id,
        "title": value("title"),
        "year": value("year"),
        "doi": value("doi"),
        "url": value("url"),
        "authors": value("authors"),
        "journal": value("journal"),
        "document_type": value("document_type"),
        "source_type": value("source_type"),
        "language": value("language"),
        "evidence_type": value("evidence_type"),
        "study_design": _json_list(row.get("study_design")),
        "data_source": _json_list(row.get("data_source")),
        "geography": _json_list(row.get("geography")),
        "regulatory_context": _json_list(row.get("regulatory_context")),
        "time_period": value("time_period"),
        "evidence_direction": value("evidence_direction"),
        "effect_scale": value("effect_scale"),
        "consensus_signal": value("consensus_signal"),
        "controversy_role": value("controversy_role"),
        "quality_signal": value("quality_signal"),
        "quality_rationale": value("quality_rationale"),
        "relevance_signal": value("relevance_signal"),
        "priority_questions": _json_list(row.get("priority_questions")),
        "causal_chain_stage": _json_list(row.get("causal_chain_stage")),
        "outcome_domain": _json_list(row.get("outcome_domain")),
        "key_claims": _json_list(row.get("key_claims")),
        "claims_about_uncertainty": _json_list(row.get("claims_about_uncertainty")),
        "claims_about_policy_or_management": _json_list(row.get("claims_about_policy_or_management")),
        "methodological_limitations": _json_list(row.get("methodological_limitations")),
        "main_uncertainty_sources": _json_list(row.get("main_uncertainty_sources")),
        "retrieval_tags": _json_list(row.get("retrieval_tags")),
        "rag_summary": value("rag_summary"),
        "summary_text": value("summary_text"),
        "related_supporting": _json_list(row.get("related_supporting")),
        "related_contrasting": _json_list(row.get("related_contrasting")),
        "related_reply_to": _json_list(row.get("related_reply_to")),
        "should_read_with": _json_list(row.get("should_read_with")),
        "included_because": value("included_because"),
        "coi_declared": value("coi_declared"),
        "curator_review_status": value("curator_review_status"),
        "inclusion_decided_by": value("inclusion_decided_by"),
        "publication_group": publication_group(doc_id),
        "evidence_family": evidence_family(doc_id),
        "added_as_debate_link": False,
        "score": round(float(row["_score"]), 4),
        "semantic_score": round(float(row.get("_semantic_score", row["_score"])), 4),
        "lexical_score": round(float(row.get("_lexical_score", 0.0)), 4),
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
    data_file: Path | None = None,
) -> list[dict]:
    """
    Retrieve the top_k most relevant documents for a query.

    Returns a list of dicts with document metadata + similarity score,
    sorted by descending relevance.
    """
    df = load_corpus(data_file)
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


def _areal_lexical_text(row: pd.Series) -> str:
    fields = [
        row.get("title", ""), row.get("authors", ""), row.get("rag_summary", ""),
        row.get("retrieval_text", ""), row.get("included_because", ""),
    ]
    for column in (
        "key_claims", "claims_about_uncertainty", "claims_about_policy_or_management",
        "methodological_limitations", "retrieval_tags", "geography", "regulatory_context",
        "study_design",
    ):
        fields.extend(_json_list(row.get(column)))
    return "\n".join(str(v) for v in fields if v)


def retrieve_areal_hybrid(
    client: OpenAI,
    query: str,
    top_k: int = 8,
    selected_doc_ids: list[str] | None = None,
    query_embedding: np.ndarray | None = None,
    data_file: Path | None = None,
) -> tuple[list[dict], list[str]]:
    """Hybrid Areal retrieval using current embeddings, lexical coverage and A0–A6 boosts.

    The semantic score is retained separately and remains the basis for out-of-scope
    detection. Related documents may add at most two query-relevant context items.
    """
    df = load_corpus(data_file or AREAL_DATA_FILE).copy()
    if selected_doc_ids is not None:
        df = df[df["doc_id"].isin(selected_doc_ids)].copy()
    if df.empty:
        return [], infer_areal_priority_questions(query)

    query_vec = query_embedding if query_embedding is not None else get_embedding(client, query)
    df["_semantic_score"] = df["_embedding"].apply(lambda emb: cosine_similarity(query_vec, emb))
    lexical_texts = [_areal_lexical_text(row) for _, row in df.iterrows()]
    df["_lexical_score"] = lexical_scores(query, lexical_texts)

    routed_qs = infer_areal_priority_questions(query)
    tagged_routes = {q for q in routed_qs if q != "A0"}
    if tagged_routes:
        route_scores = df["priority_questions"].apply(
            lambda value: areal_route_match_score(value, tagged_routes)
        )
    else:
        route_scores = pd.Series(0.0, index=df.index)
    df["_route_score"] = route_scores
    df["_score"] = (
        0.74 * df["_semantic_score"]
        + 0.14 * df["_lexical_score"]
        + 0.12 * df["_route_score"]
    )

    ranked_rows = [row for _, row in df.sort_values("_score", ascending=False).iterrows()]
    primary: list[dict] = []
    seen_publications: set[str] = set()
    for row in ranked_rows:
        result = _row_to_result(row)
        group = result["publication_group"]
        if group in seen_publications:
            continue
        primary.append(result)
        seen_publications.add(group)
        if len(primary) >= top_k:
            break

    # Add only explicit, query-relevant links; do not add another copy of a publication.
    ranked_results = {_row_to_result(row)["doc_id"]: _row_to_result(row) for row in ranked_rows}
    have_ids = {r["doc_id"] for r in primary}
    best_score = max((r["score"] for r in primary), default=0.0)
    extras: list[dict] = []
    for source in primary:
        contrasting = set(source.get("related_contrasting") or [])
        links = sorted(set(contrasting).union(source.get("should_read_with") or []))
        for doc_id in links:
            candidate = ranked_results.get(doc_id)
            if not candidate or doc_id in have_ids:
                continue
            if candidate["publication_group"] in seen_publications:
                continue
            relevant_enough = candidate["score"] >= best_score * 0.55
            if not relevant_enough:
                continue
            candidate = dict(candidate)
            candidate["added_as_debate_link"] = True
            extras.append(candidate)
            have_ids.add(doc_id)
            seen_publications.add(candidate["publication_group"])
            if len(extras) >= 2:
                break
        if len(extras) >= 2:
            break
    return primary + extras, routed_qs


def retrieve_routed(
    client: OpenAI,
    query: str,
    top_k: int = 8,
    selected_doc_ids: list[str] | None = None,
    data_file: Path | None = None,
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
            data_file=data_file,
        ), routed_qs

    # Pass 1: metadata-boosted pool
    primary = retrieve(
        client,
        query,
        top_k=top_k,
        filter_priority_questions=routed_qs,
        selected_doc_ids=selected_doc_ids,
        query_embedding=query_vec,
        data_file=data_file,
    )
    if len(primary) >= top_k:
        return _expand_debate_links(primary[:top_k], selected_doc_ids, data_file), routed_qs

    # Pass 2: fill from full corpus (exclude already picked)
    have = {r["doc_id"] for r in primary}
    filler = retrieve(
        client,
        query,
        top_k=top_k,
        selected_doc_ids=selected_doc_ids,
        query_embedding=query_vec,
        data_file=data_file,
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
    return _expand_debate_links(primary, selected_doc_ids, data_file), routed_qs


def _expand_debate_links(
    results: list[dict],
    selected_doc_ids: list[str] | None,
    data_file: Path | None = None,
) -> list[dict]:
    """Append up to 3 related_contrasting / should_read_with docs beyond top_k.

    These extras are marked added_as_debate_link so the UI can separate them
    from similarity hits. They still enter synthesis.
    """
    df = load_corpus(data_file)
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
