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

## `reference_materials/`

`reference_materials/` — methodology notes (e.g. Karpathy knowledge-base transcript). Not part of the evidence corpus.
