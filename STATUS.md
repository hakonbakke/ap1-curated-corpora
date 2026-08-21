# STATUS - AP1 Curated Corpora

Last updated: 2026-08-21 (Streamlit Cloud share)  
Owner: Thord Hakon Bakke

## Purpose of this file
Working handoff. Read first for current state, blockers, next actions.

## Agent persona
Agents in this repo act as **Senior RAG Engineers** — see `SENIOR_RAG_ENGINEER.md` and `.cursor/rules/senior-rag-engineer.mdc`. Eval-driven retrieval; no vibe-only shipping; Honest Broker constraints unchanged.

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
- `inclusion_decided_by` filled (human-confirmed); app caption ready
- `eval/benchmark_protocol_v2.md` retargeted at the Streamlit app; `scripts/eval_retrieval.py` added
- One-shot migration scripts archived to `_archive/scripts/`

## Eval status
- Golden set: `eval/smoke_queries.json` — **15 cases** (see `eval/GOLDEN_SET.md`); Thord draft; **no Ragnar confirm** (capacity) — working baseline
- `eval_routing.py`: **15/15** (2026-08-11) after expanding Norwegian / fault-line route keywords in `app/retrieval.py`
- `eval_retrieval.py`: **15/15** recall baseline saved → `eval/recall_runs/2026-08-11T123621Z_recall.json`
- Benchmark capture (Task 7c): **not run**

### Synthesis quality (2026-08-11)
- Hardened non-expert freeform prompts in `app/synthesis.py` (camps, anti-smoothing, evidence levels)
- Spotcheck script: `scripts/eval_synthesis_spotcheck.py`
- Run: `eval/synthesis_runs/2026-08-11T125000Z_nonexpert_freeform.json` — 3/4 PASS, 1 RISK (`fault4_returns_no`: smoothed «enighet om» opener; Jansen 2025 underused)
- Follow-up: anti-consensus opener clause added after spotcheck

### Human verification (2026-08-11)
- Thord reviewed all four synthesis spotcheck answers — **accepted as good**
- Golden-set must_include remains Thord draft (Ragnar skipped)

### Streamlit product (2026-08-11)
- `app/app.py` = **Havbruksløftets Evidensrom** home (room picker)
- `app/pages/1_Lakselus_og_villaks.py` = A–C orientation + live Ask (D)
- Figures from `mockup/figur-*.png`

### Naming (2026-08-18)
User-facing rooms are **evidensrom**, not kunnskapsrom. Copy frames each room as a map of what academic publications say, not a consensus «what we know».

### Source panel (2026-08-17)
Items 1-6 shipped in `app/pages/1_Lakselus_og_villaks.py`. Retrieval ranking unchanged.
- Full title inside the open card. Direction, quality and consensus as text, not `st.metric`
- Cosine score moved to **Tekniske detaljer** (not shown as a relevance percent)
- `ai_verified` label: «Metadata sjekket (AI)» / «Metadata checked (AI)». Expert-approved unchanged
- Contrasts shown as Lastname Year via a `doc_id` index from `load_corpus()`
- Q-codes visible in researcher mode. Hidden for non-specialists except inside technical details
- Open card: corpus role + first sentence of `included_because`, then 2-3 claims. Rest behind **Les mer**
- `inclusion_decided_by` passed through `_row_to_result` in `app/retrieval.py`
- Header splits similarity hits vs debate-linked extras (`_expand_debate_links` can add up to 3 beyond k)
- Full evidence brief only in researcher mode, collapsed. Non-specialist gets the short `rag_summary` if present

Deferred (7-10): group list by evidence direction, camp summary above the list, clickable citations in synthesis, merge debate map into cards.

### Next
1. Streamlit Cloud: create `ap1-evidensrom` from `main` (see `DEPLOY.md`); share `https://ap1-evidensrom.streamlit.app` with Ragnar
2. Re-run recall after any retrieval change; compare to `2026-08-11T123621Z_recall.json`
3. Optional: hybrid BM25 only if a future recall run shows clear misses
4. Items 7-10 when you want the list grouped and tied to the synthesis
5. Orientation figures (`mockup/figur-*.png`) are missing from the repo; A/B images will not show until they are added

## Parquet update rule
- Metadata / status / rationale only → `python scripts/sync_metadata_to_parquet.py`
- `rag_summary` / `key_claims` / new or removed docs → `python scripts/ingest.py --doc <id>` (API)

## Run locally
```powershell
streamlit run app/app.py --server.fileWatcherType none   # home + pages (villaks Ask)
python scripts/validate_corpus.py
python scripts/eval_routing.py
python scripts/eval_retrieval.py          # writes eval/recall_runs/
python scripts/eval_synthesis_spotcheck.py  # ~4 GPT calls; writes eval/synthesis_runs/
```

## Mockup (HTML reference)
- Brand: **Havbruksløftets Evidensrom**
- Path: `mockup/index.html` → `mockup/tema-villaks.html`
- Live Streamlit now mirrors this structure (see Streamlit product above)
