# AI curation pipeline (human = select only)

**Status:** implemented (scripts) · **Updated:** 2026-08-03

## Decision

Expert field-by-field QA is capacity-blocked. Trust model:

- **Human:** chooses which papers enter the corpus
- **AI:** extract → summary + metadata → verify against extract → ingest
- **Expert approval:** optional (`expert_approved`), not a gate

## Commands

```powershell
python scripts/add_paper.py --doc YYYY_journal_keyword --pdf path\to\paper.pdf
python scripts/ai_verify_document.py --doc YYYY_journal_keyword
python scripts/ai_verify_document.py --all   # backfill checks on existing 27
```

Env (optional): `AP1_CURATE_MODEL`, `AP1_VERIFY_MODEL` (default `gpt-4o`).

## Files

| Script | Role |
|--------|------|
| `scripts/add_paper.py` | Orchestrator |
| `scripts/ai_curate_document.py` | Maker: summary + metadata |
| `scripts/ai_verify_document.py` | Checker: faithfulness vs extract |
| `scripts/corpus_paths.py` | Shared paths + status constants |
| `scripts/convert_pdfs_odl.py` | PDF → extracted.md |
| `scripts/ingest.py` | Embeddings → parquet |

## What “verified” means

`ai_verified` = second model pass found no critical faithfulness failures on
`key_claims` / `evidence_direction` / COI relative to `extracted.md`.

It is **not** expert endorsement of scientific interpretation (Del D).

## Next (related)

- Run `--all` verify on existing 27; triage failures
- Wire retrieval routing + eval (separate from this pipeline)
- Show `curator_review_status` badge in Streamlit source list
