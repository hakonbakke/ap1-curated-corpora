# STATUS - AP1 Curated Corpora

Last updated: 2026-08-03 (TASKS.md maintenance pass in progress)  
Owner: Thord Hakon Bakke

## Purpose of this file
Working handoff. Read first for current state, blockers, next actions.

## Trust model
| Role | Responsibility |
|------|----------------|
| Human | Inclusion (which PDFs enter) — record in `inclusion_decided_by` |
| AI / Cursor | Extract, curate, verify, offline accept |
| OpenAI API key | **RAG runtime only** (embeddings + synthesis for testers) |
| Expert | Optional `expert_approved` |

Status: **27/27 `ai_verified`**. Vocabulary validator exits 0. Routing eval 5/5.

## Shipped this session (TASKS.md)
- Task 1: `vocabulary.json` + `scripts/validate_corpus.py`
- Task 2: taxonomy drift fixes + `sync_metadata_to_parquet.py` (no re-embed)
- Task 3: `TAXONOMY.md` reconciled (geography `Norway_PO*`; production_stage/system_type scoped)
- Task 5: stale-embedding warning in sync; ingest uses `list_doc_ids()` + drop guard
- Task 6: README/WORKFLOW/requirements/welfare stub/backlog accuracy; regrade script archived
- Curate prompt: `controversy_role` ≠ `evidence_direction` (prevent recurrence)

## Blocked — needs Thord
1. **Task 4 — `inclusion_decided_by`:** Were all 26 remaining papers (besides Stige 2022, which was yours) Ragnar's selections, or a mix?
2. **Confirm model_type:** Lamberg 2022 → `statistical_regression_model`, Hawley 2024 → `population_model` (applied provisionally from TASKS note).
3. **Tasks 7–8** (benchmark + retrieval recall): opt-in; costs some API.

## Parquet update rule
- Metadata / status / rationale only → `python scripts/sync_metadata_to_parquet.py`
- `rag_summary` / `key_claims` / new or removed docs → `python scripts/ingest.py --doc <id>` (API)

## Run locally
```powershell
streamlit run app/app.py --server.fileWatcherType none
python scripts/validate_corpus.py
python scripts/eval_routing.py
```

## Add paper (uses API for curate/verify/ingest — avoid unless needed)
```powershell
python scripts/add_paper.py --doc YYYY_journal_keyword --pdf path\to.pdf
```
Prefer Cursor offline edits + `sync_metadata_to_parquet.py` when possible.

## Next after Task 4 answer
1. Fill `inclusion_decided_by` + split inclusion_log columns; sync parquet
2. Redeploy Streamlit Cloud so Ragnar gets routing + confidence + inclusion caption
3. Tasks 7–8 only with explicit API go-ahead
4. Delete `TASKS.md` when definition of done is met
