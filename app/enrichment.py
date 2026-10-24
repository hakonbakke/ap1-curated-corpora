"""
enrichment.py — Full-text material for the Areal room, built by
scripts/build_areal_enrichment.py into data/area-enrichment.parquet:

  - figure:  a verbatim quote with a number from the full text, and an English
             statement of what it measures (page where the extract has markers);
  - chapter: a summary of one chapter of a large report, searchable on its own;
  - pq_note: what one document's full text says about one of its A0–A8 tags.

Retrieval lifts a large report when one of its chapters matches the question
better than the report as a whole, and attaches the matching chapters, figures
and notes to each result for the synthesis prompt.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

ENRICHMENT_FILE = Path(__file__).resolve().parent.parent / "data" / "area-enrichment.parquet"
FIGURES_PER_DOC = 6
CHAPTERS_PER_DOC = 2


@st.cache_resource(show_spinner=False)
def _load_cached(path_str: str, mtime: float) -> dict:
    df = pd.read_parquet(path_str)
    tables = {}
    for kind in ("figure", "chapter"):
        part = df[df["kind"] == kind].reset_index(drop=True)
        matrix = np.stack(part["embedding"].to_numpy()).astype(np.float32) if len(part) else np.zeros((0, 1))
        if len(part):
            matrix /= np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-10
        tables[kind] = (part.drop(columns=["embedding"]), matrix)
    notes = df[df["kind"] == "pq_note"]
    tables["pq_note"] = {(r.doc_id, r.pq): r.text for r in notes.itertuples()}
    return tables


def load_enrichment(path: Path | None = None) -> dict | None:
    """The enrichment tables, or None when the file has not been built."""
    path = Path(path or ENRICHMENT_FILE)
    if not path.exists():
        return None
    return _load_cached(str(path), path.stat().st_mtime)


def _page(value) -> int | None:
    return None if value is None or pd.isna(value) else int(value)


def _scores(table: tuple[pd.DataFrame, np.ndarray], query_vec: np.ndarray) -> pd.DataFrame:
    part, matrix = table
    if part.empty or matrix.shape[1] != len(query_vec):  # empty, or another embedding model
        return part.iloc[0:0].assign(sim=[])
    q = query_vec / (np.linalg.norm(query_vec) + 1e-10)
    return part.assign(sim=matrix @ q)


def best_chapter_scores(query_vec: np.ndarray, path: Path | None = None) -> dict[str, float]:
    """Best chapter cosine per large report."""
    tables = load_enrichment(path)
    if tables is None:
        return {}
    scored = _scores(tables["chapter"], query_vec)
    if scored.empty:
        return {}
    return scored.groupby("doc_id")["sim"].max().astype(float).to_dict()


def attach(results: list[dict], query_vec: np.ndarray, path: Path | None = None) -> list[dict]:
    """Add `chapter_hits`, `key_figures` and `pq_notes` (for the result's via_pq codes)."""
    tables = load_enrichment(path)
    if tables is None:
        return results
    doc_ids = {r["doc_id"] for r in results}
    chapters = _scores(tables["chapter"], query_vec)
    figures = _scores(tables["figure"], query_vec)
    chapters = chapters[chapters["doc_id"].isin(doc_ids)].sort_values("sim", ascending=False)
    figures = figures[figures["doc_id"].isin(doc_ids)].sort_values("sim", ascending=False)
    for r in results:
        doc_id = r["doc_id"]
        r["chapter_hits"] = [
            {"title": c.title, "text": c.text, "page_from": _page(c.page_from), "page_to": _page(c.page_to),
             "score": round(float(c.sim), 4)}
            for c in chapters[chapters["doc_id"] == doc_id].head(CHAPTERS_PER_DOC).itertuples()
        ]
        r["key_figures"] = [
            {"quote": f.quote, "statement": f.text, "page": _page(f.page_from)}
            for f in figures[figures["doc_id"] == doc_id].head(FIGURES_PER_DOC).itertuples()
        ]
        r["pq_notes"] = {
            code: tables["pq_note"][(doc_id, code)]
            for code in r.get("via_pq") or []
            if (doc_id, code) in tables["pq_note"]
        }
    return results
