# STATUS - AP1 Curated Corpora

Last updated: 2026-08-03 (TASKS.md maintenance pass complete except API-gated runs)  
Owner: Thord Hakon Bakke

## Purpose of this file
Working handoff. Read first for current state, blockers, next actions.

## Trust model
| Role | Responsibility |
|------|----------------|
| Human | Inclusion (which PDFs enter) — recorded in `inclusion_decided_by` |
| AI / Cursor | Extract, curate, verify, offline accept |
| OpenAI API key | **RAG runtime only** (embeddings + synthesis for testers) |
| Expert | Optional `expert_approved` |

Status: **27/27 `ai_verified`**. Validator exit 0. Routing eval 5/5.

### Inclusion accountability
- **26/27** selected by **Ragnar Tveterås**
- **1/27** (`2022_aei_stige-model-sensitivity-calibration`) selected by **Thord Håkon Bakke**
- Log columns: `Selected by` / `Logged by` (split; do not conflate)

## Shipped (2026-08 TASKS pass)
- Vocabulary + `validate_corpus.py`; taxonomy drift fixed; TAXONOMY reconciled
- Stale-embedding warning in sync; ingest drop-guard + `list_doc_ids`
- Docs accuracy (README/WORKFLOW/requirements/welfare stub); P0-2 rejected
- Curate prompt: `controversy_role` ≠ `evidence_direction`
- `inclusion_decided_by` filled; app caption ready
- `eval/benchmark_protocol_v2.md` + `scripts/eval_retrieval.py` (ready; **not run** — API)

## Eval status
- `eval_routing.py`: **5/5** (API-free)
- `eval_retrieval.py`: **5/5** (2026-08-03; ~5 embedding calls) — must_include_any hits in top-k; BM25/rerank stays deferred with evidence
- Benchmark capture (Task 7c): not run (synthesis + NotebookLM / frontier+search)

## Parquet update rule
- Metadata / status / rationale only → `python scripts/sync_metadata_to_parquet.py`
- `rag_summary` / `key_claims` / new or removed docs → `python scripts/ingest.py --doc <id>` (API)

## Run locally
```powershell
streamlit run app/app.py --server.fileWatcherType none
python scripts/validate_corpus.py
python scripts/eval_routing.py
# when willing to spend ~5 embedding calls:
# python scripts/eval_retrieval.py
```

## Next
1. Redeploy Streamlit Cloud so Ragnar sees routing, confidence, inclusion caption
2. When API budget allows: `eval_retrieval.py` then optional B1–B4/C1 benchmark capture
3. Hybrid BM25 only if retrieval recall fails with evidence
