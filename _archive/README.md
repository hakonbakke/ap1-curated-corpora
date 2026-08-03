# Archive

Earlier experiments and duplicate bundles that are **not** used by the active Streamlit app (`app/app.py`) or `scripts/ingest.py`.

## Active pipeline (for reference)

The app reads only:

- `corpora/salmon-lice-and-mortality-of-wild-salmonids/documents/<doc_id>/metadata.yaml`
- `corpora/salmon-lice-and-mortality-of-wild-salmonids/documents/<doc_id>/summary.md`
- `data/corpus.parquet` (built by `python scripts/ingest.py`)

---

## `phase1_experiment/`

NotebookLM phase 1 testing (March 2026). Compared PDF-only vs curated metadata+summaries vs generic ChatGPT. Includes `Test_phase1_ap1_extracted.txt`, `phase1_notebooklm_full/`, `phase1_notebooklm_md/`.

---

## `ragie/`

Ragie.ai managed RAG (superseded by local app).

| Path | Contents |
|------|----------|
| `RAGIE_PARTITION_AP1_CURATED_SUMMARIES.md` | Upload instructions |
| `upload_ap1_curated_summaries_to_ragie.py` | Ragie API upload script |
| `SUMMARY_GENERATION_INSTRUCTIONS.md` | Template for `*.summary.md` Ragie bundle |
| `retrieval_summaries_bundle/summaries/` | 15 × `*.summary.md` (duplicate of retrieval text; **not** read by ingest) |

To improve the live app, edit `documents/*/metadata.yaml` (`rag_summary`, `key_claims`) and `documents/*/summary.md`, then re-run ingest.

---

## `benchmark/`

`benchmark_protocol_v1.md` — pilot comparison plan (ChatGPT, NotebookLM, Ragie). Not loaded by the app; useful when running a formal evaluation.

---

## `scripts/`

One-shot migrations from the 2026-08 maintenance pass. All completed and
verified; `scripts/validate_corpus.py` now enforces the end state they produced.
**Do not run any of these against a clean corpus** — they assume the pre-migration
data and are not idempotent.

| Script | What it did |
|---|---|
| `regrade_qa_reports.py` | Moved COI/funding false-positive `critical_issues` in `qa_report.json` to `soft_issues` and refreshed `curator_review_status`. Archived after confirming zero remaining COI items in `critical_issues` across all 27 documents. |
| `apply_tasks_drift_fixes.py` | Applied the named per-document taxonomy fixes: `quality_signal` `moderate`→`medium` (5 docs), `consensus_signal` (3 docs), `controversy_role` (9 docs, where `evidence_direction` values had leaked in). |
| `normalize_remaining_vocab.py` | Normalised `life_stage` hyphenation, `geography` and `regulatory_context` to canonical tokens (original prose preserved into `retrieval_tags`), free-text `causal_chain_stage`, and added missing `model_type` keys. |
| `apply_inclusion_decided_by.py` | Populated `inclusion_decided_by` across all 27 documents after human confirmation of who selected each paper. |

Kept rather than deleted so the corpus's edit history is reconstructable — the
metadata changes they made are curatorial, and the reasoning should stay
auditable. See `vocabulary.json` for the vocabulary they normalised to.

---

## `reference_materials/`

`reference_materials/` — methodology notes (e.g. Karpathy knowledge-base transcript). Not part of the evidence corpus.
