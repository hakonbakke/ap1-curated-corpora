# STATUS - AP1 Curated Corpora

Last updated: 2026-10-19 (Robertsen 2014 and Pettersen 2015 extracted; not curated)  
Owner: Thord Hakon Bakke

## Purpose of this file
Working handoff. Read first for current state, blockers, next actions.

## Agent persona
Agents in this repo act as **Senior RAG Engineers** — see `SENIOR_RAG_ENGINEER.md` and `.cursor/rules/senior-rag-engineer.mdc`. Eval-driven retrieval; no vibe-only shipping; Honest Broker constraints unchanged.

## Trust model
| Role | Responsibility |
|------|----------------|
| Human | Inclusion (which PDFs enter) — recorded in `inclusion_decided_by` |
| AI / Cursor | Extract, curate, verify against the fail-closed gate |
| OpenAI API key | **RAG runtime only** (embeddings + synthesis for testers) |
| Expert | Optional named override or sign-off as `expert_approved` |

Before hardening, all 27 villaks records were labelled `ai_verified`. The known
Jonsson discrepancy is corrected and now `ai_draft`; its runtime record was re-embedded.
The 2026-09-15 hardened-gate audit flags 14 additional villaks records for source
review without silently reclassifying them. It also flags 3/39 area records for
incomplete claim checks. Use `ai_verify_document.py --audit-existing` to reproduce
the read-only audit.

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

A-C rewritten 2026-09-15 for Friday demo, then A-B rewritten again 2026-09-16 from Thord's introduction draft. A was rewritten again 2026-09-17 from Thord's own full intro. Visible A is the paradox and the three area quantities. Split governance, three growth diagnoses, uneven trade-off knowledge, municipal will and where cases die sit behind **Les mer**. The villaks Typisk god støtte block and the competing-use inventory are out of A. SNL left-panel excerpt remains as figure. C is **Åpne spørsmål**. Subtitle: der veksten stopper, og der kunnskapen mangler. UI Ask example questions shortened 2026-09-17. Canonical A0-A6 sentences stay in `PRIORITY_QUESTIONS.md`. B treats good sites as one diagnosis, names the case-file gap, and states that Havbruksfondet and the production fee are untested as a gate. Wild-salmon expander is gate and lid only. Soy/feed cut from A. D remains **Spør kildene**.

AREA_ROOM_FRAME and areal freeform prompts rewritten the same day. Traffic-light is a growth lid. Do not open as a wild-fish impact controversy. Second Ask smoke `eval/areal_smoke_runs/2026-09-15T132500Z_areal_ask_smoke.json`: FAIL 0, WARN 2 (A0, A4 coverage), PASS 5. All seven `opener_drift=false`. A2 now opens on licences and where the case dies, with lice and traffic-light as a capacity lid. A4 still likes to wrap the file question in the four scarcity diagnoses before it reaches knowledge. One extra FRAME line added after that run: answer the question asked, do not default every query to the four forks.

Standing split (Thord 2026-09-15): wild salmon is in this room when it gates expansion, above all via the traffic-light on 13 production areas and via lice as a reason for site refusal. The villaks room keeps the causal chain from lice on out-migrating smolt to mortality estimates. Do not strip TLS from areal answers. Do not let every areal question open as the wild-fish impact controversy.

A0-A6 are a working set. Ragnar Tveterås, Marit Schei Olsen and Tonje Osmundsen can change the questions, drop codes, add codes, or rewrite the wording as they go through the innspill pack. Do not treat today's codes, `_AREAL_ROUTE_RULES`, the 15 Sep smoke must-hits, or the tags on the original 33 as a ranking contract. Hybrid route boost is a temporary overlay on unrebalanced tags. After they land: retag, then rewrite the route list and the Ask-smoke. Not before.

### Codex (2026-09-15 and 2026-09-18)
Grounded in git plus Codex session logs. Not the Cursor demo/innspill work.

Shipped on `origin/main` (commit `0d9f01a`, Luna batch 1):
- Snapshot first: branch `backup-pre-audit-2026-09-15` at `2a708f3`, plus a local PDF zip under `ap1-curated-corpora-backups/2026-09-15`
- Kvalvik selector keyed on `doc_id` (duplicate titles no longer collide)
- `_odl_tmp/` in `.gitignore`; PyMuPDF in `requirements.txt`

Written locally, not committed, not on Cloud:
- 15 Sep, after the Luna commit: fail-closed `ai_verify_document.py` (every `key_claim` must be supported; `--audit-existing`), `offline_accept_qa.py` requires named override, `tests/test_verification_gates.py`, WORKFLOW/backlog, Jonsson 2016 corrected to `ai_draft` and re-embedded in villaks parquet
- 18 Sep then finish 19 Sep: hybrid retrieve, evidence-block synthesis, ingest/sync field list expanded, `eval/areal_retrieval_benchmark.json` plus runner and `tests/test_areal_rag.py`. Against the finish brief it still re-embedded all 39 (`text-embedding-3-large`). Working parquet embeddings differ from `HEAD` on every row (mean cosine ~0.955). `retrieval_text` changed on all 39 because extra YAML fields now enter the embed string. Stale marker gone because ingest caught up, not because the old index was broken. Default Ask `k` is 10. Their 10/10 is a self-written smoke at k=10 with OR-groups and OOS keywords taken from the same three fixture queries. Astra first said qualified pass (scope guard too blunt), then they added a planning-context carve-out. Astra also called the ten cases a development smoke, not answer-quality eval. Cursor reproduced 19/19 unit tests. No commit, no retag of the original 33, A-C and innspill untouched.

Audit write-up (read-only at the time it was written): `Astra_Audit_AP1_Curated_Corpora.md` (untracked).

Cursor, not Codex: A-C copy, C/D question length, Cloud demo commits `0679c33`/`955cb8e`/`3e6f11d`, `CORPUS_OVERVIEW.md`, innspill Word/Excel.

### Next
1. Second read of labels is finished 19 Oct 2026. The C-section bodies in `app/pages/2_Areal_og_havbruk.py` were rewritten the same day so each explanation matches the settled A0-A8 question. Chips under each question follow the labels. The page is local only. Cloud still shows the old questions until a push to main. On 19 Oct 2026 the 11 papers missing from the index were embedded with text-embedding-3-large and upserted. The parquet is 50 rows. The original 39 vectors were not rebuilt. priority_questions for all 50 were synced into the parquet without a new embedding. Robertsen 2014 and Pettersen 2015 now have summary.md, key_claims and rag_summary written from the extracts. Laws were not embedded. Villaks parquet was not touched. A0 to A8 are all possible tags. A0 only when the paper's subject is the overall balance of where and how far aquaculture can be established. A second read from the extracts is underway (19 Oct 2026) and is written into metadata and `updates_files_19_10_26/Documents_tags_and_weight.xlsx`. Narrowed so far: Mikkelsen, Karlsen and Osmundsen 2019 lost A0 (now A1, A4, A5, A6); Schütz and Slater 2019 lost A0 (now A1, A6); Aanesen and Mikkelsen 2020 lost A6 (now A4); Jentoft and Buanes 2005 is now A6 only; Sandersen 2021 Helgeland lost A0 (now A1, A3, A6); Sandersen and Kvalvik 2014 lost A0 (now A1, A6, both spreadsheet rows); Misund and others 2023 lost A1 (now A4). Pettersen and others 2015 lost A7 (now A8). Myklebust 2014 stays A1, A6. Robertsen and others 2014 stays A1, A5, A6. Aldrin and others 2015 stays A8. The 2015 legal framework report stays A0, A1, A2, A4, A6. Meld. St. 35, the 2026 risk report and the IPBES values volumes have no area code. Moldal 2026 stays A8. Sørdahl 2026 stays A6. Evenset 2023 is A1, A2, A3, A5, A8. SALT 1065 is A3, A5, A6. SALT 1075 stays A1, A5. SALT 1110 stays A2, A5, A8. The 2023 sustainable-area report is A0, A1, A4, A5, A7, A8. Metier 2023 is A5. Sand and Misund 2025 on area need is A1, A2, A5, A6, A8. Sand and others 2025 on bio-industries stays A6. Rosendal and others 2025 is A6. Myklebust 2021 is A1, A6. Hersoug 2022 is A1, A4. Iversen and others 2025 stays A4. Osmundsen and Olsen 2025 stays A2. Mikkelsen and others 2025 on cumulative impact stays A3. Kept after this read: Sandersen and Kvalvik 2015 (A0, A1, A4, A6), Gullestad and others 2011 (A0, A1, A2, A3, A5, A6, A7, A8), Aldrin and others 2011 (A8), Qviller and others 2024 (A8), Iversen and others 2025 (A4), Mikkelsen, Sørdahl and Solås 2022 (A5, A6). Hersoug, Mikkelsen and Osmundsen 2020 stays A0, A1, A4, A5, A6. Both Kvalvik 2017 folders stay A1, A6. Myklebust 2018 stays A1, A6. Karlsen and others 2019 stays A7, A8. Bjørkan and Eilertsen 2020 stays A6. Gismervik and others 2020 stays empty. Aldrin and others 2017 stays A8. The other folders still have the first labeling pass and are not certified by this re-read. Labels are not embedded and do not change search. A7 is what the industry itself can do. A8 is biosecurity, disease and water contact between farms. Laws and regulations stay context and are not embedded. Pettersen and others 2015 and Robertsen and others 2014 are extracted, not fully curated, and not embedded. Workshop 29 Oct.
2. Cloud share: `https://ap1-evidensrom.streamlit.app` tracks `main`. Confirm OpenAI secret, then send the live URL. Cloud still uses cosine `retrieve`, not the local hybrid
3. A1 drop was the route formula, not missing tags. The smoke query infers A1+A2 because it contains «avslag». Codex scored `intersection / all inferred codes`, so A1-only papers (Kvalvik, Helgeland) got half the boost of kitchen-sink A1+A2 tags. Cosine-only still had Helgeland at 5 and Kvalvik at 8. Fix: `areal_route_match_score` gives full credit for any matching A1-A6 code. After the fix, hybrid A1 k=8 returns Helgeland 6 and one Kvalvik 8 (the two files stay one publication). Still local. Do not push until you want another full Ask-smoke.

Standing leftovers:
1. Cloud share: `https://ap1-evidensrom.streamlit.app` (tracks `main`). Confirm secrets after push and send Ragnar the live URL
2. Re-run recall after any retrieval change; compare to `2026-08-11T123621Z_recall.json`
3. Hybrid Areal retrieve is investigate-first, not ship. Astra asked to categorize A0/A4 misses before a new retriever. Route boost on unrebalanced A1-A6 tags on the original 33 is the risk. Keep the evidence-block change (existing YAML into synthesis). Do not re-embed 39 because `RETRIEVAL_TEXT_FIELDS` grew.
4. Source panel items 7-10 (group by direction, camp summary, clickable citations, merge debate map)
5. Areal A is Thord's own intro (2026-09-17). Visible: paradox plus labeled merd/lokalitet/plan. Les mer has four headings (governance, three answers, knowledge, municipal will). SNL/KF left-panel excerpt remains as figure (`mockup/figur-arealbruk-snl.png`).
6. Areal C renamed 2026-09-17 to **Åpne spørsmål**. A-B hinges shipped.
7. Readable areal corpus overview: `corpora/area-and-aquaculture/CORPUS_OVERVIEW.md` (what the 39 documents are about, where they disagree, where the file is empty). Villaks not included.

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
