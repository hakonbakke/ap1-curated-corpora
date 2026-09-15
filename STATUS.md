# STATUS - AP1 Curated Corpora

Last updated: 2026-09-15 (Areal lede tightened, D labelled Spør kildene)  
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

### Areal draft (2026-09-13)
Thord included the full received set (33) as a first draft. Working questions A0 plus A1-A6 are unconfirmed.

Selected by (Thord confirmed 2026-09-13, from SharePoint Endret av):
- Ragnar Tveterås 16
- Marit Schei Olsen 11
- Tonje Osmundsen 6
- Source: `corpora/area-and-aquaculture/filed_by.json`. That name is `inclusion_decided_by`.

Full Cursor curate (2026-09-13): `extracted.md` already existed for all 33. `metadata.yaml` and `summary.md` rewritten from extracts. Status `ai_draft`. No `qa_report` verify pass yet.

Priority questions rewritten 2026-09-13 after page-verify, then rebalanced 2026-09-14: disagreement about the conflict leads, gaps are the second beat. A0 is the lead Ask (what is actually scarce). It is not a metadata tag. A1-A6 stay as tags. Existing tags on the 33 files were not changed. Room page, home card and areal synthesis frame updated. Not confirmed by the three selectors.
- PDFs: `corpora/area-and-aquaculture/documents/PDFs/`
- Isolated parquet: `data/area-and-aquaculture.parquet` (39 rows after 2026-09-15 ingest of six Thord-added papers; 33 rows were the 2026-09-13 set). Villaks `data/corpus.parquet` still 27 rows.
- Room: `app/pages/2_Areal_og_havbruk.py` now mirrors villaks A-C plus Ask as D: introduction and three diagnoses, stacked Norwegian framework, five dividing lines, then live Ask. Ask still uses `retrieve`, not lice routing. No orientation figures yet.
- First-pass metadata was `ai_draft` from front matter. That pass is superseded.
- Extract: OpenDataLoader failed on many Windows filenames with special characters. Those (and the large reports) were taken out with PyMuPDF. `convert_one` now copies to `source.pdf` first so a later ODL pass is safer.
- Retrieval smoke (siting/licensing question): top hits were Mikkelsen 2019, rettslig rammeverk 2015, Gullestad 2011, SALT 1075, Sand 2025, Hersoug 2022. In scope. Do not run villaks `add_paper.py` on these PDFs.
- Two Kvalvik/Robertsen 2017 PDFs were both kept. Curate gave them the same title.
- Eight large area reports rewritten 2026-09-13 (Gullestad 2011, SALT 1065/1075/1110, Sand 2025 pair, bærekraftig 2023, Evenset 2023). Gold style, `ai_draft`, `inclusion_decided_by` from the map. `extracted.md` not edited. Folder `undated_baerekraftig-arealbruk-havbruk` is dated 20 November 2023 in the preface.
- Seven more rewritten 2026-09-13 (Osmundsen 2025 county evaluation, Rosendal 2025 municipalities, Kulmambetova 2025 density, Qviller 2024 lice redistribution, Gismervik 2020 welfare law, Metier 2023 marine maps, Mikkelsen 2025 cumulative north). Gold style. Gismervik and Qviller filed as adjacent, not siting papers.

### Areal page-verify (2026-09-13, done)
All 33 documents have `qa_report.json` (`verify_model: cursor_grok_page_verify`) and `curator_review_status: ai_verified`. Claims were walked against `extracted.md`, not against sammendrag alone. `extracted.md` was not edited. API `ai_verify_document.py` was not used for this pass (it still caps extract length).

Ingest: `python scripts/ingest.py --corpus area-and-aquaculture` wrote 33 rows to `data/area-and-aquaculture.parquet`. Villaks parquet still 27 rows.

YAML footgun: `strip_yaml_comments` drops lines that start with `#`, including a `# ai_verify` line left inside a quoted `curator_note`. That uncloses the quote. Stamps now sit after the quoted block. Unquoted `word:` inside list items also breaks parse. Ingest dry-run before a full rebuild.

Unread remnants: image-only figures and some table colour cells. SALT 1110 Table 7. HI Table 1.1 colours. Metier tornado bars.

### Areal add (2026-09-15)
Thord dropped six PDFs in `corpora/area-and-aquaculture/documents/`. Copied to `PDFs/`. Extracted with PyMuPDF. Gold curate plus Cursor page-verify (`verify_model: cursor_grok_page_verify`). `inclusion_decided_by: Thord Håkon Bakke`. Original 33 not retagged.

Filename trap: `Sandersen and Kvalvik_ 2014_ Challenges and Myths...pdf` is Jentoft and Buanes 2005. Keep `2015_sandersen_access-to-sites` as the area-rent paper. Hammer article filename year 2023, publication 2024. Dissertation Paper II is that article. Both folders kept. Meld. St. 35 is a partial walk (sammendrag, sea/coast, fisheries-aquaculture, traffic-light subsection).

The high A0 (Norway allocating land, sea and living resources, aquaculture as one use) was rejected. Room object stays aquaculture's claim on coastal area. Working precision sheet: `corpora/area-and-aquaculture/PRIORITY_QUESTIONS_PRECISION.md`. Sentences accepted as good for now and written into `PRIORITY_QUESTIONS.md` (Norwegian plus English). Original 33 not retagged.

A-C rewritten 2026-09-15 for Friday demo: hero and home card drop the land-and-sea allocation lede. Intro uses four scarcity answers (unused sea as myth, licences and traffic-light, municipal designation, biology). Framework stack keeps TLS as a capacity lid here. C has seven dividing lines A0-A6 with locked question sentences. New papers named where they belong (Jentoft, Sandersen 2014, Schütz, Sørdahl, Meld. St. 35). Hero lede tightened again the same afternoon. D is labelled **Spør kildene** (English: Ask the sources) in both rooms, not Ask.

AREA_ROOM_FRAME and areal freeform prompts rewritten the same day. Traffic-light is a growth lid. Do not open as a wild-fish impact controversy. Second Ask smoke `eval/areal_smoke_runs/2026-09-15T132500Z_areal_ask_smoke.json`: FAIL 0, WARN 2 (A0, A4 coverage), PASS 5. All seven `opener_drift=false`. A2 now opens on licences and where the case dies, with lice and traffic-light as a capacity lid. A4 still likes to wrap the file question in the four scarcity diagnoses before it reaches knowledge. One extra FRAME line added after that run: answer the question asked, do not default every query to the four forks.

Standing split (Thord 2026-09-15): wild salmon is in this room when it gates expansion, above all via the traffic-light on 13 production areas and via lice as a reason for site refusal. The villaks room keeps the causal chain from lice on out-migrating smolt to mortality estimates. Do not strip TLS from areal answers. Do not let every areal question open as the wild-fish impact controversy.

### Next
1. Cloud before Friday 2026-09-18 still open. Do not retag the original 33
2. After the demo: selectors on A1-A6 tags. Retrieval of Jentoft and Sørdahl only if the same questions still miss them

Standing leftovers:
1. Cloud share: app was `ap1-curated-corpora-test.streamlit.app` (Aug 21). Confirm secrets and send Ragnar the live URL
2. Re-run recall after any retrieval change; compare to `2026-08-11T123621Z_recall.json`
3. Hybrid BM25 only if a future recall run shows clear misses
4. Source panel items 7-10 (group by direction, camp summary, clickable citations, merge debate map)
5. Orientation figures (`mockup/figur-*.png`) still missing from the repo

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
