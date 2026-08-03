# STATUS - AP1 Curated Corpora

Last updated: 2026-08-03 (27/27 ai_verified; routing+confidence; ready to push)  
Owner: Thord Hakon Bakke

## Purpose of this file
Working handoff. Read first for current state, blockers, next actions.

## Trust model
| Role | Responsibility |
|------|----------------|
| Human | Inclusion (which PDFs enter) |
| AI / Cursor | Extract, curate, verify, offline accept |
| OpenAI API key | **RAG runtime only** (embeddings + synthesis for testers) |
| Expert | Optional `expert_approved` |

Status: **27/27 `ai_verified`** (parquet synced without re-embed).

## Shipped this session
- AI curation pipeline (`add_paper`, curate, verify, regrade, offline_accept, sync_metadata_to_parquet)
- Force-recurate Jansen / Van Nes / Fjelldal
- `retrieve_routed()` + Streamlit caption
- Synthesis confidence rules (no High when contested/🔵)
- Offline routing eval 5/5: `python scripts/eval_routing.py`
- Jones taxonomy fix; RCN → `critiques_methodology`; Stige 2024 zonation → `mixed_within_study`
- BASWE gap note: `possible_improvements/baswe-gap-vs-ap1.md`

## Next after push
1. Redeploy / reboot Streamlit Cloud so Ragnar gets routing + confidence
2. Hybrid BM25 (local) — highest remaining BASWE win
3. Optional local reranker; contextual re-embed only when willing to spend API on ingest

## Run locally
```powershell
streamlit run app/app.py --server.fileWatcherType none
python scripts/eval_routing.py
```

## Add paper (uses API for curate/verify/ingest — avoid unless needed)
```powershell
python scripts/add_paper.py --doc YYYY_journal_keyword --pdf path\to.pdf
```
Prefer Cursor offline edits + `sync_metadata_to_parquet.py` when possible.
