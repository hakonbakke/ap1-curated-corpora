"""
routing.py — Use the priority questions A0–A8 as a funnel for Areal retrieval.

Every Areal document carries A0–A8 tags (`priority_questions`, assigned by an AI
and not yet validated by the selectors). A question is first routed to the
priority question(s) it belongs to; documents tagged with those codes are taken
first, ranked by semantic similarity, and the remaining places are filled with
the best untagged semantic hits. Questions that fit no priority question fall
back to plain semantic search.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
from openai import OpenAI

import enrichment
from retrieval import (
    AREAL_DATA_FILE,
    _json_list,
    _row_to_result,
    cosine_similarity,
    get_embedding,
    load_corpus,
)

ROUTER_MODEL = "gpt-6-luna"

# Short English titles from corpora/area-and-aquaculture/PRIORITY_QUESTIONS.md.
PQ_TITLES = {
    "A0": "Balance, governance and trade-offs",
    "A1": "Bottlenecks and development",
    "A2": "The site application process",
    "A3": "Cumulative effects in planning and siting",
    "A4": "Economic instruments and area use",
    "A5": "Knowledge base and technology",
    "A6": "Conflicts, legitimacy and process",
    "A7": "What the industry itself can do",
    "A8": "Biosecurity, disease and water contact",
}

# Official context documents (white papers, government and international reports).
# They frame the rules and the official picture rather than answer a priority
# question, so they carry no PQ tag in the funnel and compete for their own places.
CONTEXT_DOC_IDS = frozenset({
    "2024_meldst35_baerekraftig-bruk-natur",
    "2026_hi_risikorapport",
    "2026_moldal_fiskehelserapporten",
    "2022_ipbes_values-assessment",
    "2022_ipbes_spm-values",
})
CONTEXT_SLOTS = 2
# A large report has 8-53 chapter summaries, and its best chapter is nearly always
# closer to a question than the report as a whole (by 0.05-0.20 on the nine PQs).
# A chapter lifts its report only by what it beats the report by beyond this margin,
# so a report rises when one chapter stands out, not merely because it is long.
# Calibrated 2026-10-24 on the nine PQs and seven free questions: at 0.15 two of
# sixteen lists change (A8 gains the fish-health report's biosecurity chapter).
CHAPTER_LIFT_MARGIN = 0.15
# A context document joins only when it is close to the best research hit:
# at least this share of the best evidence score, and never below the floor.
# Calibrated 2026-10-23 on the nine PQs and four free questions.
CONTEXT_RELATIVE = 0.75
CONTEXT_FLOOR = 0.38

PQ_TITLES_NO = {
    "A0": "Balanse, styring og avveiing",
    "A1": "Flaskehalser og utvikling",
    "A2": "Søknadsprosessen for lokaliteter",
    "A3": "Samlet påvirkning i plan og lokalisering",
    "A4": "Økonomiske virkemidler og arealbruk",
    "A5": "Kunnskapsgrunnlag og teknologi",
    "A6": "Konflikter, legitimitet og prosess",
    "A7": "Hva næringen selv kan gjøre",
    "A8": "Biosikkerhet, smitte og vannkontakt",
}

ROUTER_PROMPT = """\
You sort a user's question about aquaculture and coastal area in Norway into the \
project's priority questions. Reply with JSON only: {{"codes": [...]}} with zero, \
one or two codes, the most relevant first.

Choose a code only when the question is clearly about that priority question. \
Choose A0 only for broad questions about what overall determines where and how much \
aquaculture can be established, or how environment, industry and other uses are \
weighed against each other; a question about one slice (a fee, disease spread, the \
application process) gets that slice's code instead. Return {{"codes": []}} when the \
question fits none of them.

Priority questions:
{catalogue}

User question:
{query}
"""


def pq_code_for_text(text: str, pq_texts: list[str]) -> str | None:
    """The code of a priority question whose full text the query repeats verbatim."""
    clean = (text or "").strip()
    for i, pq in enumerate(pq_texts):
        if clean == pq.strip():
            return f"A{i}"
    return None


def classify_pq(client: OpenAI, query: str, pq_texts: list[str], model: str = ROUTER_MODEL) -> list[str]:
    """Route a free-text question to 0–2 of A0–A8. Any failure returns [] (plain search)."""
    catalogue = "\n".join(
        f"- A{i} ({PQ_TITLES[f'A{i}']}): {text}" for i, text in enumerate(pq_texts)
    )
    prompt = ROUTER_PROMPT.format(catalogue=catalogue, query=query.strip())
    kwargs = {"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0}
    if model.startswith("gpt-4"):
        kwargs["max_tokens"] = 60
    else:
        kwargs["max_completion_tokens"] = 60
        kwargs["reasoning_effort"] = "none"
    try:
        reply = client.chat.completions.create(**kwargs).choices[0].message.content or ""
        match = re.search(r"\{.*\}", reply, re.S)
        codes = json.loads(match.group(0)).get("codes", []) if match else []
    except Exception:
        return []
    valid = [c for c in codes if isinstance(c, str) and c in PQ_TITLES]
    return list(dict.fromkeys(valid))[:2]


def retrieve_funnel(
    client: OpenAI,
    query: str,
    codes: list[str],
    top_k: int = 12,
    selected_doc_ids: list[str] | None = None,
    query_embedding: np.ndarray | None = None,
    data_file: Path | None = None,
) -> list[dict]:
    """Research documents tagged with `codes` first (by similarity), then the best
    untagged research hits, plus up to CONTEXT_SLOTS official context documents.

    A large report is ranked by its best chapter when that chapter is closer to the
    question than the report as a whole (`score`); `semantic_score` stays the cosine
    of the document itself, which the out-of-scope check uses. Each result gets
    `via_pq` = the matching codes (empty for semantic fill and context),
    `corpus_role` = "context" or "evidence", and the full-text chapters, figures and
    priority-question notes from enrichment.attach. Context documents join only when
    they are close to the best research hit, and take places from the research list
    only then. Two files of the same publication never both take a place.
    """
    df = load_corpus(data_file or AREAL_DATA_FILE).copy()
    if selected_doc_ids is not None:
        df = df[df["doc_id"].isin(selected_doc_ids)].copy()
    if df.empty:
        return []
    query_vec = query_embedding if query_embedding is not None else get_embedding(client, query)
    df["_semantic_score"] = df["_embedding"].apply(lambda emb: cosine_similarity(query_vec, emb))
    chapter_best = enrichment.best_chapter_scores(query_vec)
    df["_score"] = [
        max(s, chapter_best.get(d, s) - CHAPTER_LIFT_MARGIN) for d, s in zip(df["doc_id"], df["_semantic_score"])
    ]
    wanted = set(codes or [])
    df["_via_pq"] = df["priority_questions"].apply(lambda v: [c for c in _json_list(v) if c in wanted])
    is_context = df["doc_id"].isin(CONTEXT_DOC_IDS)
    evidence, context = df[~is_context].copy(), df[is_context].copy()
    evidence["_tagged"] = evidence["_via_pq"].apply(bool)

    seen_publications: set[str] = set()

    def take(rows, limit: int, role: str) -> list[dict]:
        picked: list[dict] = []
        for _, row in rows.iterrows():
            if len(picked) >= limit:
                break
            result = _row_to_result(row)
            if result["publication_group"] in seen_publications:
                continue
            result["via_pq"] = list(row["_via_pq"]) if role == "evidence" else []
            result["corpus_role"] = role
            picked.append(result)
            seen_publications.add(result["publication_group"])
        return picked

    best_evidence = float(evidence["_score"].max()) if not evidence.empty else 0.0
    floor = max(CONTEXT_FLOOR, CONTEXT_RELATIVE * best_evidence)
    eligible = context[context["_score"] >= floor].sort_values("_score", ascending=False)
    context_results = take(eligible, min(CONTEXT_SLOTS, top_k), "context")
    ranked = evidence.sort_values(["_tagged", "_score"], ascending=[False, False])
    results = take(ranked, top_k - len(context_results), "evidence") + context_results
    return enrichment.attach(results, query_vec)
