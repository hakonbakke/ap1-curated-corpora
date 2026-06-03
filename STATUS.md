# STATUS - AP1 Curated Corpora

Last updated: 2026-06-03 (corpus expansion: 16 → 27 papers)  
Owner: Thord Hakon Bakke

## Purpose of this file
This file is the working handoff for the project.  
Any new agent should read this first to understand current state, blockers, and next actions.

## Project goal (current phase)
Get a stable, useful local Streamlit MVP for AP1 evidence synthesis before cloud deployment.

## Current state snapshot
- Repository: `ap1-curated-corpora`
- Active corpus: `corpora/salmon-lice-and-mortality-of-wild-salmonids`
- Corpus size in app data: **27 papers** (`data/corpus.parquet`)
- Newest batch added (2026-06-03): 11 papers — McCormick 1998, Helland 2015, Kristoffersen 2018, Fjelldal 2020, Bøhn 2020, Johnsen 2021, Lamberg 2022, Jonsson 2016, Hawley 2024, Jones 2025 (×2 BC natural experiments)
- App status: local app working; language toggle (English/Norsk) enabled

## Streamlit app status
Main app path: `app/app.py`

### Implemented UX features
- Language switch: English / Norsk
- Audience modes: researcher / non-specialist
- Answer format: structured / free text
- Free text prompt now question-driven (less rigid templating)
- Clickable example questions (left-aligned list + Use button)
- Sidebar simplified (metadata filters removed)
- Corpus reload button in sidebar

### Current run command (recommended)
Use this command to avoid watchdog/file-watcher crashes seen on this machine:

```powershell
cd "c:\Users\ThordHåkonBakke\OneDrive - Blue Planet AS\Koding\ap1-curated-corpora"
streamlit run app/app.py --server.fileWatcherType none
```

Then hard refresh browser with `Ctrl + F5`.

## Known issues / caveats
- Streamlit sessions can show stale data if an old process is still running.
- `corpus.parquet` is the runtime source of truth for retrieval. Re-run ingest after metadata edits.
- Linter in Cursor may show unresolved imports (`openai`, `dotenv`) even when runtime works.

## Data and curation status
- All 27 docs are present in `documents/*/metadata.yaml` and in `data/corpus.parquet`.
- `curator_review_status` is still `pending` across documents (expert validation not finished).
- Retrieval quality depends mostly on `rag_summary` + `key_claims` quality.
- New papers (2026-06-03 batch) added by agent with `curator_review_status: pending` — subject to expert QA.

### 2026-06-03 corpus expansion (+11 papers)
| Folder | Paper | Key Q |
|--------|-------|-------|
| 1998_cjfas_mccormick-smolting-migration | McCormick et al. 1998 — Smolting biology review | Q4 |
| 2015_aei_helland-monitoring-lice-challenges | Helland et al. 2015 — Monitoring challenges | Q5, Q10 |
| 2016_jfb_jonsson-environmental-change-salmon | Jonsson et al. 2016 — Ocean environment & salmon life history | Q9 |
| 2018_epidemics_kristoffersen-risk-assessment | Kristoffersen et al. 2018 — NVI risk assessment model | Q2-Q5, Q7, Q8, Q10 |
| 2020_conphys_fjelldal-lice-osmoregulation-salmon | Fjelldal et al. 2020 — Lab physiology dose-response | Q6, Q7 |
| 2020_jae_bohn-timing-survival-postsmolts | Bøhn et al. 2020 — Timing × lice density survival | Q4, Q8 |
| 2021_icesjms_johnsen-vps-mortality-norway | Johnsen et al. 2021 — IMR VPS model (TLS primary model) | Q3-Q5, Q7, Q8, Q10 |
| 2022_fishes_lamberg-pre-fishery-abundance | Lamberg & Imsland 2022 — Pre-fishery abundance metric | Q9, Q10 |
| 2024_ecosphere_hawley-anadromy-lice-mortality-trout | Hawley et al. 2024 — Individual anadromy × lice cost | Q4, Q5, Q7-Q9 |
| 2025_dao_jones-broughton-lice-unchanged | Jones et al. 2025 — Broughton natural experiment | Q1, Q9, Q10 |
| 2025_jfd_jones-pacific-lice-cessation-bc | Jones et al. 2025 — Discovery Islands cessation | Q1, Q9, Q10 |

## How to update corpus safely
1. Edit `metadata.yaml` and/or `summary.md` for target doc(s).
2. Rebuild embeddings:
   - single doc: `python scripts/ingest.py --doc <doc_id>`
   - full: `python scripts/ingest.py`
3. Restart Streamlit (or use Reload corpus button).
4. Verify paper count and retrieval behavior in app.

## Immediate next priorities
1. Metadata QA pass on highest-impact papers (TLS/model-debate core set).
2. Query smoke tests (English and Norwegian, structured and free text).
3. Decide deploy readiness criteria, then push and deploy to Streamlit Cloud.

## Suggested smoke-test queries
- How robust is the Norwegian Traffic Light System as a regulatory framework?
- What evidence links lice-induced mortality to reduced adult returns?
- Which studies disagree most on lice impact magnitude?
- What management measures are needed in Nordfjord to reach green-light levels?

## Agent handoff protocol
When an agent finishes meaningful work, update this file with:
- What changed
- What was verified
- What remains
- Any new risks/blockers

Keep entries short and factual.
