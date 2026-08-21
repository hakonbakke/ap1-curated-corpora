# TASKS — August 2026 maintenance pass

**Transient working file. Delete when all tasks are done.**

Written 2026-08-03 as an execution spec for an implementing agent. All curatorial
judgement calls have already been made and are written out explicitly below —
**apply them as specified, do not re-derive them.**

Scope: maintenance and validation only. This pass deliberately does **not** touch
project direction; those decisions are pending a meeting on 2026-08-05.

---

## Ground rules for the implementing agent

1. **Do not invent data.** Where a value is unknown, stop and ask. Task 4 has a
   hard stop of this kind.
2. **Do not re-derive the mappings in Task 2.** They are curatorial judgements
   made against `TAXONOMY.md` and the inclusion log. Apply them verbatim.
3. **No OpenAI API calls** in any task except Task 7, which is explicitly opt-in
   and costs money. Do not run `scripts/ingest.py` (it re-embeds), do not run
   `scripts/add_paper.py`, `ai_curate_document.py`, `ai_verify_document.py`, or
   `expand_summaries_from_extract.py`.
4. **Never edit `extracted.md`.** It is the extraction of record that
   `qa_report.json` was verified against.
5. `git` is not on PATH in this environment. Prepend it per session:
   `$env:PATH += ";C:\Program Files\Git\cmd"`
6. Shell is PowerShell, not bash. `ls -la`, `cat`, `grep` will fail.
7. Commit after each task with a message naming the task. Do not push.

### Explicitly out of scope — do not do these

| Not now | Why |
|---|---|
| Deleting the two stub corpora | Depends on whether they are in the AP1 mandate. Unresolved. |
| Writing anything into `corpora/*/synthesis/` | Content decision, pending the meeting. |
| Any retrieval work: BM25, reranking, contextual embeddings, GraphRAG | Gated on benchmark evidence that retrieval is actually failing. None exists yet. |
| Deleting `scripts/regrade_qa_reports.py` | One-shot migration; confirm it is a no-op first (Task 6). |
| Moving or deleting `BASWE-15-RAG-Concepts-Guide.pdf` | Currently open in the user's editor. Leave it. |
| Re-running ingest to refresh embeddings | Costs API budget. Task 5 only *flags* staleness. |
| Deleting anything under `_archive/` | Contains the only copies of the benchmark protocol and reference notes. |

---

## Task 0 — already done (2026-08-03)

Deleted, all gitignored build/scratch output, nothing tracked affected:

- `_odl_output/` (7 files, 1.4 MB)
- `_tmp_extracts/` (11 files, 165 KB)
- `app/__pycache__/` (6 files, incl. stale Python 3.13 bytecode)
- `scripts/__pycache__/` (4 files)

No action needed. Recorded for continuity.

---

## Task 1 — machine-readable vocabulary + validator

**Why:** `TAXONOMY.md` defines controlled vocabularies and nothing enforces them.
The corpus has drifted (Task 2 lists the damage). `retrieve_routed()` and metadata
filtering are shipped features that depend on these values matching. This is the
cheapest high-leverage control missing from the repo.

### 1a. Create `corpora/salmon-lice-and-mortality-of-wild-salmonids/vocabulary.json`

Single machine-readable source of truth, derived from `TAXONOMY.md` plus the
comment blocks in that corpus's `metadata_template.yaml`. Structure:

```json
{
  "_source": "Derived from TAXONOMY.md and metadata_template.yaml. If those change, change this.",
  "scalar_fields": { "field_name": ["allowed", "values"] },
  "list_fields": { "field_name": ["allowed", "values"] },
  "required_fields": ["..."],
  "free_text_fields": ["..."]
}
```

**Scalar (single-value) controlled fields:**

| Field | Allowed values |
|---|---|
| `language` | `english`, `norwegian`, `other` |
| `source_type` | `peer_reviewed`, `report`, `government_report`, `expert_group_report`, `white_paper`, `thesis`, `conference_paper`, `dataset`, `commentary`, `response` |
| `document_type` | `research_article`, `review_article`, `systematic_review`, `meta_analysis`, `modelling_study`, `methods_paper`, `commentary`, `response`, `policy_report`, `risk_assessment`, `monitoring_report`, `thesis`, `dataset_description` |
| `abstract_available` | `yes`, `no`, `unclear` |
| `wild_or_farmed_focus` | `wild`, `farmed`, `both`, `not_applicable` |
| `evidence_type` | `empirical_experimental`, `empirical_observational`, `model`, `review`, `systematic_review`, `meta_analysis`, `methods`, `commentary`, `response`, `policy_assessment`, `mixed` |
| `evidence_direction` | `supports_effect`, `weak_support`, `mixed_within_study`, `no_effect_detected`, `contradicts_effect`, `critiques_methodology`, `not_applicable` |
| `effect_scale` | `individual_level`, `population_level`, `both`, `not_applicable` |
| `uncertainty_emphasis` | `low`, `moderate`, `high`, `very_high`, `not_stated` |
| `consensus_signal` | `high_agreement`, `moderate_agreement`, `mixed`, `context_dependent`, `contested`, `insufficient_evidence` |
| `quality_signal` | `strong`, `medium`, `weak` |
| `controversy_role` | `foundational`, `supportive`, `critical`, `rebuttal`, `bridge_between_positions`, `peripheral`, `not_applicable` |
| `relevance_signal` | `high`, `medium`, `low` |
| `transferability` | `high`, `medium`, `low` |
| `coi_declared` | `yes`, `no`, `unclear` |
| `curator_review_status` | `ai_draft`, `ai_verified`, `expert_approved` |

`coi_declared` note: bare `yes`/`no` in YAML parse as booleans. The validator must
coerce Python `True`/`False` back to `"yes"`/`"no"` before comparing, and must not
report those as violations.

`curator_review_status` note: `pending`, `reviewed`, `approved` are legacy. The
validator should accept them but emit a **warning** telling the operator to migrate.

**List-valued controlled fields:**

| Field | Allowed values |
|---|---|
| `priority_questions` | `Q1`–`Q10` |
| `causal_chain_stage` | `farm_lice_abundance`, `lice_reproduction`, `larval_production`, `larval_dispersal`, `environmental_drivers`, `host_exposure`, `infestation`, `physiological_effects`, `behaviour`, `individual_mortality`, `population_impacts`, `monitoring_methods`, `model_calibration`, `model_validation`, `regulatory_assessment` |
| `host_species` | `atlantic_salmon`, `sea_trout`, `arctic_char`, `pacific_salmon`, `chum_salmon`, `pink_salmon`, `coho_salmon`, `chinook_salmon`, `mixed_salmonids`, `not_species_specific` |
| `life_stage` | `egg`, `fry`, `parr`, `smolt`, `post_smolt`, `juvenile`, `adult`, `returning_adult`, `mixed`, `not_applicable` |
| `parasite_species` | `lepeophtheirus_salmonis`, `caligus_clemensi`, `caligus_elongatus`, `mixed_lice`, `not_specified` |
| `environment` | `freshwater`, `estuary`, `fjord`, `coastal`, `archipelago`, `shelf_sea`, `open_ocean`, `laboratory`, `mesocosm`, `modelled_environment` |
| `seasonality_focus` | `spring`, `summer`, `autumn`, `winter`, `full_year`, `migration_period`, `not_applicable` |
| `regulatory_context` | `Norway_TLS`, `Norway_expert_group`, `Canada_management`, `Scotland_management`, `Ireland_management`, `none` |
| `study_design` | `laboratory_challenge`, `field_sampling`, `trawl_sampling`, `sentinel_cage`, `telemetry`, `genetic_assignment`, `farm_monitoring`, `statistical_analysis`, `hydrodynamic_modelling`, `particle_tracking`, `virtual_post_smolt_modelling`, `population_modelling`, `literature_review`, `expert_assessment`, `mixed` |
| `data_source` | `wild_fish_sampling`, `farm_lice_counts`, `sentinel_cages`, `trawl_data`, `trap_net_data`, `telemetry_tracking`, `genetic_assignment`, `hydrodynamic_model_output`, `particle_tracking_output`, `expert_group_reports`, `published_literature`, `mixed` |
| `model_type` | `none`, `hydrodynamic_model`, `lice_particle_tracking_model`, `infestation_model`, `virtual_post_smolt_model`, `statistical_regression_model`, `threshold_model`, `population_model`, `risk_assessment_model`, `ensemble_or_multi_model`, `conceptual_model` |
| `observation_unit` | `individual_fish`, `fish_group`, `river`, `production_area`, `farm`, `farm_month`, `site`, `grid_cell`, `model_particle`, `study`, `mixed` |
| `comparison_type` | `exposed_vs_unexposed`, `treated_vs_untreated`, `farm_present_vs_removed`, `high_vs_low_infestation`, `observed_vs_modelled`, `trawl_vs_sentinel`, `before_after`, `among_regions`, `among_years`, `none`, `mixed` |
| `outcome_domain` | `lice_abundance_on_farms`, `larval_density_in_water`, `infestation_on_wild_fish`, `infestation_pressure`, `migration_timing`, `migration_route`, `physiological_stress`, `skin_damage`, `osmoregulatory_effects`, `behaviour_change`, `survival`, `mortality`, `marine_survival`, `adult_returns`, `population_abundance`, `regulatory_classification`, `model_performance`, `uncertainty_estimation` |
| `main_uncertainty_sources` | `migration_timing`, `migration_duration`, `larval_production`, `hydrodynamics`, `calibration_data`, `infestation_to_mortality_thresholds`, `observational_bias`, `sampling_representativeness`, `model_structure`, `parameter_uncertainty`, `transferability`, `none_highlighted` |

**`geography` is a special case.** `TAXONOMY.md` says free text with standardised
terms and gives `PO1`–`PO13`; `metadata_template.yaml` says `Norway_PO[1-13]`.
The two governing documents disagree. **Resolution: the template wins.** Canonical
token set:

`Norway`, `Norway_PO1` … `Norway_PO13`, `Hardangerfjord`, `British_Columbia`,
`Discovery_Islands`, `Broughton_Archipelago`, `Scotland`, `Ireland`,
`North_Atlantic`, `Pacific_Canada`, `England`, `not_applicable`

Add tokens to this list only if a real corpus value cannot be expressed with the
existing ones, and record the addition in `vocabulary.json`. After fixing, update
`TAXONOMY.md`'s `geography` section to match the template rather than leaving the
contradiction in place.

**Fields that are genuinely free text** (validator checks presence, never value):
`title`, `doi`, `url`, `authors`, `journal`, `publisher`, `time_period`,
`primary_endpoint`, `secondary_endpoints`, `key_claims`, `claims_about_uncertainty`,
`claims_about_policy_or_management`, `methodological_limitations`, `rag_summary`,
`coi_notes`, `quality_rationale`, `relevance_rationale`, `transferability_notes`,
`included_because`, `related_documents_supporting`, `related_documents_contrasting`,
`related_documents_reply_to`, `should_be_read_with`, `retrieval_tags`,
`curator_note`, `added_by`, `added_date`, `inclusion_decided_by`, `corpus`, `year`.

### 1b. Create `scripts/validate_corpus.py`

Requirements:

- Import paths from `scripts/corpus_paths.py`. **Do not** re-hardcode the corpus
  slug — four scripts already do that and it is a known problem.
- Use `corpus_paths.list_doc_ids()` for iteration (it correctly excludes `PDFs/`
  and `_`-prefixed folders).
- Reuse `corpus_paths.strip_yaml_comments()` rather than writing a fifth copy of
  that logic.
- No API calls. No network. Fully deterministic.
- Checks per document:
  1. All four expected files present: `extracted.md`, `summary.md`,
     `metadata.yaml`, `qa_report.json`.
  2. `metadata.yaml` parses as YAML.
  3. Every key present in `metadata_template.yaml` is present in the document
     (missing key = violation, empty value = separate lower-severity warning).
  4. No keys present in the document that are absent from the template.
  5. Every controlled field's value(s) appear in `vocabulary.json`.
  6. `doc_id` folder name matches the `YYYY_outlet_keyword` pattern.
- Cross-corpus check: every `doc_id` on disk appears in `data/corpus.parquet`, and
  every `doc_id` in the parquet still exists on disk. Report orphans both ways.
  Read the parquet with pandas; do not modify it.
- Output: grouped, human-readable report to stdout **and** a machine-readable
  `qa_vocabulary_violations.csv` at repo root with columns
  `doc_id,field,severity,found_value,expected`. Severity is `error` or `warning`.
- Exit code `1` if any `error`, `0` if only warnings. This is what makes it usable
  as a gate later.
- Support `--doc <doc_id>` to validate one document, and `--quiet` for CI use.

Add `validate_corpus.py` to the commands listed in `STATUS.md` and `WORKFLOW.md`.

**Verify:** run it. It must find the violations listed in Task 2. If it finds
substantially fewer, the validator is wrong, not the task list.

---

## Task 2 — fix the taxonomy drift

Apply these exact edits. Each is a curatorial judgement already made against
`TAXONOMY.md` and the rationales in
`corpora/salmon-lice-and-mortality-of-wild-salmonids/inclusion_log.md`.
**Do not substitute your own mapping.** Edit only the named field in the named
file; leave everything else alone.

### 2a. `quality_signal: moderate` → `medium` (5 documents)

`moderate` is not in the vocabulary; `medium` is the intended value.

- `2015_aei_helland-monitoring-lice-challenges`
- `2018_epidemics_kristoffersen-risk-assessment`
- `2022_fishes_lamberg-pre-fishery-abundance`
- `2025_dao_jones-broughton-lice-unchanged`
- `2025_jfd_jones-pacific-lice-cessation-bc`

### 2b. `consensus_signal` (3 documents)

| Document | From | To | Reason |
|---|---|---|---|
| `1998_cjfas_mccormick-smolting-migration` | `strong_agreement` | `high_agreement` | Same concept, wrong token. |
| `2016_jfb_jonsson-environmental-change-salmon` | `strong_agreement` | `high_agreement` | Same concept, wrong token. |
| `2022_fishes_lamberg-pre-fishery-abundance` | `unclear` | `insufficient_evidence` | Methods paper proposing a new metric; too few comparable studies to assess agreement. |

### 2c. `controversy_role` (9 documents)

**Root cause worth understanding:** `evidence_direction` values leaked into
`controversy_role`. They are different axes — `evidence_direction` is about the
paper's substantive thrust, `controversy_role` is about its position in a debate.
Several documents have the same value in both fields, which is the tell.

| Document | From | To | Reason |
|---|---|---|---|
| `1998_cjfas_mccormick-smolting-migration` | `neutral` | `foundational` | Inclusion log: "Foundational review on Atlantic salmon smolting biology… mechanistic basis for why migration timing determines lice exposure". |
| `2015_aei_helland-monitoring-lice-challenges` | `methodological` | `critical` | Raises statistical/power challenges to monitoring design. `critical` is the vocabulary term for exactly this. |
| `2016_jfb_jonsson-environmental-change-salmon` | `neutral` | `peripheral` | Contextual reference for non-lice marine drivers; not part of the lice debate itself. |
| `2018_epidemics_kristoffersen-risk-assessment` | `supports_effect` | `foundational` | Presents the NVI risk assessment model — one of the three operational TLS VPS models. Establishes a baseline others critique. |
| `2022_fishes_lamberg-pre-fishery-abundance` | `practical_implications` | `peripheral` | Population-metric methods paper; contextual to the debate. |
| `2024_ecosphere_hawley-anadromy-lice-mortality-trout` | `supports_effect` | `supportive` | Adds evidence in the dominant direction. Value copied from `evidence_direction`. |
| `2024_ijpara_stige-regional-lice-coordination` | `practical_implications` | `supportive` | NVI modelling of control scenarios within the TLS framework; adds evidence in the dominant direction. |
| `2025_dao_jones-broughton-lice-unchanged` | `challenges_effect` | `critical` | Natural experiment challenging farm-attribution. `challenges_effect` is not in either vocabulary. |
| `2025_jfd_jones-pacific-lice-cessation-bc` | `challenges_effect` | `critical` | Companion paper, same reasoning. |

### 2d. `life_stage` hyphenation (3 documents)

Normalise `post-smolt` and `postsmolt` → `post_smolt`. The validator's first run
will name the exact files; the fix is mechanical.

### 2e. `geography` and `regulatory_context` normalisation

**Rule — nothing may be lost.** For each entry that is not already a canonical
token:

1. Replace it with the canonical token(s) it implies.
2. Append the original prose string to that document's `retrieval_tags` list.

`retrieval_tags` exists in the template for exactly this purpose (extra RAG
retrieval terms), so place names like `"Hardangerfjord, Norway"` and
`"Norwegian national salmon lice monitoring programme"` stay searchable while the
controlled field becomes filterable. Do not delete prose outright.

Examples of the intended transformation:

- `geography: ["Norway (nationwide, 13 production zones)"]` →
  `geography: ["Norway"]`, and `"Norway (nationwide, 13 production zones)"`
  appended to `retrieval_tags`.
- `regulatory_context: ["Norwegian Traffic Light System (TLS)"]` →
  `regulatory_context: ["Norway_TLS"]`, prose appended to `retrieval_tags`.

There are roughly 43 distinct `geography` values across 27 documents. Work
document by document from the validator report. If a value cannot be mapped to
any existing token, **stop and ask** rather than inventing a token.

### 2f. `causal_chain_stage` free text

Several documents contain prose (`"fraction dying from lice"`,
`"translating infestation to mortality"`, `"smolt exposure to lice"`,
`"population-level impact"`, `"infestation_pressure"`,
`"management_intervention"`). Map each to the controlled stage list. Suggested
mappings for the values seen so far:

| Found | Use |
|---|---|
| `infestation_pressure` | `infestation` |
| `smolt exposure to lice…` | `host_exposure` |
| `fraction dying from lice` | `individual_mortality` |
| `translating infestation to mortality` | `individual_mortality` + `model_calibration` |
| `population-level impact` | `population_impacts` |
| `management_intervention` | `regulatory_assessment` |

Any value not in this table: **stop and ask.**

### 2g. `model_type` missing key (6 documents)

Add the key with the correct value. All six are non-modelling papers, so `none`
is expected — but confirm against each `summary.md` before writing, because
`2022_fishes_lamberg` uses mark-recapture estimation which may warrant
`statistical_regression_model`.

- `1998_cjfas_mccormick-smolting-migration`
- `2016_jfb_jonsson-environmental-change-salmon`
- `2022_fishes_lamberg-pre-fishery-abundance`
- `2024_ecosphere_hawley-anadromy-lice-mortality-trout`
- `2025_dao_jones-broughton-lice-unchanged`
- `2025_jfd_jones-pacific-lice-cessation-bc`

Note: `2024_ecosphere_hawley` is an individual-based simulation study, so it
likely needs `population_model` or `conceptual_model`, not `none`. Check the
summary.

### 2h. `2025_jae_jansen-lice-effects-returns` — 4 missing keys

This document alone is missing `comparison_type`, `outcome_domain`,
`primary_endpoint`, and `secondary_endpoints`. Fill from its `summary.md` and
`extracted.md`. Expected values given the study design (104 Norwegian rivers,
TLS PIM estimates vs observed adult returns): `comparison_type` includes
`observed_vs_modelled` and likely `among_regions`; `outcome_domain` includes
`adult_returns`. Confirm against the document; do not guess the endpoints.

### 2i. Propagate to the parquet

After all metadata edits: `python scripts/sync_metadata_to_parquet.py`

This is the correct tool here — none of the Task 2 fields feed `retrieval_text`,
so no re-embedding is needed and no API cost is incurred. Do **not** run
`ingest.py`.

**Verify:** `python scripts/validate_corpus.py` exits 0, and
`python scripts/eval_routing.py` still reports 5/5.

---

## Task 3 — update TAXONOMY.md to match reality

Two genuine contradictions between governing documents, discovered above:

1. `geography`: `TAXONOMY.md` says `PO1`–`PO13`; the template says
   `Norway_PO[1-13]`. Update `TAXONOMY.md` to the template form and state that
   `vocabulary.json` is the machine-readable source.
2. `TAXONOMY.md` defines `production_stage` and `system_type`, which the
   wild-salmonids corpus does not use (it uses `life_stage` and `environment`).
   Mark them as applying to the two other corpora only, so a future reader does
   not think they are missing fields.

Also add a line to `TAXONOMY.md` pointing at `scripts/validate_corpus.py` as the
enforcement mechanism. A controlled vocabulary with no validator is a suggestion.

---

## Task 4 — record the human checkpoint

**Why this matters more than it looks:** `WORKFLOW.md` states the one required
human checkpoint is paper selection. But `inclusion_decided_by` is empty or
missing in all 27 documents, and 26 of 27 rows in `inclusion_log.md` credit
"Claude" in the Curator column. As it stands, the repository contains no evidence
that a human selected anything — which undercuts the project's central
accountability claim. This is a recording failure, not a process failure, and it
is an hour of work.

### 4a. HARD STOP — requires input from Thord

Do **not** populate `inclusion_decided_by` by guessing. The inclusion log's
"Curator" column conflates *who decided* with *who wrote the entry*, so it cannot
be used to infer the decider.

Known from the log: `2022_aei_stige-model-sensitivity-calibration` was Thord's
own selection (2026-03-03).

Ask Thord for the decider of the remaining 26, then apply. Offer him the likely
shape of the answer to make it a one-minute question rather than an essay:
*"Were all 26 remaining papers Ragnar's selections, or was it a mix — and if
mixed, which ones were yours?"*

### 4b. Then apply

- Set `inclusion_decided_by` in all 27 `metadata.yaml` files to the named human.
- Set `added_by: ai_curate_pipeline` where the pipeline produced the record (this
  is the field's documented purpose and it is currently empty in most documents).
- In `inclusion_log.md`, replace the single `Curator` column with two:
  `Selected by` (the human) and `Logged by` (Claude / pipeline). Preserve every
  existing row; this is a column split, not a rewrite.
- Update the `How to use this log` section to require both.
- Re-run `sync_metadata_to_parquet.py`.

### 4c. Make the checkpoint visible in the app

In `app/app.py`, surface `inclusion_decided_by` in the per-document display
alongside the existing DOI and status caption. The claim "a named domain expert
selected every paper in this corpus" is the project's strongest trust asset and
it is currently invisible to testers.

---

## Task 5 — close the parquet staleness hole

**The bug:** `sync_metadata_to_parquet.py` updates `rag_summary`, `key_claims`
and `summary_text` in `data/corpus.parquet` but leaves `retrieval_text` and
`embedding` untouched. Retrieval scores against the stale embeddings, so semantic
search can match on text that no longer matches the displayed metadata. Worse,
`STATUS.md` currently recommends this path.

### 5a. `scripts/sync_metadata_to_parquet.py`

- Define a module-level constant naming the fields that feed `retrieval_text`
  (currently `rag_summary` and `key_claims` — read `ingest.py`'s
  retrieval-text builder to confirm the exact set rather than assuming).
- When a sync changes any of those fields for a document, collect its `doc_id`.
- At the end, if any were collected: print a prominent warning listing them and
  the exact command to fix (`python scripts/ingest.py --doc <id>`), and write
  them to `data/stale_embeddings.txt`.
- Add `--strict` which exits non-zero instead of warning, so it can gate CI.
- Status-only and rationale-only edits must stay silent — they do not affect
  embeddings, and this is the common case.

### 5b. `scripts/ingest.py`

- Extract the retrieval-text builder into a function importable by both scripts,
  so there is one definition of what gets embedded.
- On full rebuild (no `--doc`), if the resulting row count is **lower** than the
  existing parquet's, write the dropped `doc_id`s and the reason to
  `data/qa_ingest_skipped.csv` and refuse to write unless `--force` is passed.
  Currently a document with malformed YAML silently vanishes from the corpus with
  only a `SKIP` line on stdout.
- Align folder iteration with `corpus_paths.list_doc_ids()`. `ingest.py` currently
  walks every non-dot subdirectory, which includes `documents/PDFs/`.

### 5c. Documentation

Update `STATUS.md` and `WORKFLOW.md` with the decision rule:

> Metadata, status, or rationale edits → `sync_metadata_to_parquet.py`.
> Edits to `rag_summary` or `key_claims`, or any new/removed document →
> `ingest.py --doc <id>` (costs API).

Do not run a full re-embed as part of this task. Just make the tooling honest
about when one is needed.

---

## Task 6 — documentation accuracy

### 6a. `README.md` structure tree

The tree omits `app/`, `scripts/`, `data/`, `eval/`, `_archive/`,
`requirements.txt`, `DEPLOY.md`, `.devcontainer/`, and `.streamlit/`. It also
shows document folders as containing only `summary.md` and `metadata.yaml`, when
all 27 also contain `extracted.md` and `qa_report.json`. Bring it in line with
what is actually on disk, including `documents/PDFs/`.

### 6b. `possible_improvements/improvement-backlog.md`

Change row `P0-2` (expert QA on TLS core) from `deferred` to `rejected`, with the
reason recorded plainly: no expert verification capacity exists or is expected;
the available expert capacity is paper selection only. "Deferred" implies a
return that will not happen, and it keeps a dead item in the active priority list.

### 6c. Welfare stub corpus README

`corpora/salmon-lice-and-farmed-salmon-welfare-and-mortality/README.md` has an
inventory table listing two documents (`2021_jfd_delosing-mortality`,
`2025_jfd_post-delousing-mortality`) that do not exist on disk, and a status line
claiming "initial documents added". Correct the status to empty and remove the
phantom rows. Do **not** delete the corpus — that decision is pending.

### 6d. Confirm whether `regrade_qa_reports.py` is dead

Check whether any `qa_report.json` still contains a COI finding classified as
critical that the script would downgrade. If none do, the migration is complete:
move the script to `_archive/` with a one-line note in `_archive/README.md`
explaining what it did and when. If some do, leave it and report which documents.
Do not delete it outright either way.

### 6e. `requirements.txt`

`scripts/convert_pdfs_odl.py` imports `opendataloader_pdf`, which is not listed.
Add it. Pin versions consistently with the existing entries.

### 6f. Reconcile the PDF storage story

`WORKFLOW.md` Stage 2 says PDFs are stored in SharePoint, but 27 PDFs (57 MB)
live in `corpora/…/documents/PDFs/` and sync through OneDrive, plus one stray at
`documents/2022_aei_stige-model-sensitivity-calibration/original.pdf`. Move the
stray into `PDFs/` for consistency, then update `WORKFLOW.md` to describe where
they actually live. Both locations are gitignored, so this is a documentation fix,
not a data migration.

---

## Task 7 — retarget the benchmark protocol (opt-in, some API cost)

**Why:** the project's stated success bar is "must produce more value than a
general LLM." That has never been tested. The instrument to test it already
exists — `_archive/benchmark/benchmark_protocol_v1.md` — with a solid four-
dimension rubric, blind A/B/C presentation, and explicit failure criteria. It is
archived and points at Ragie, which was retired.

### 7a. Move and retarget

Copy to `eval/benchmark_protocol_v2.md`. Keep the scoring rubric and the user-
group design unchanged — they are good. Change:

- **Treatment arm:** the Streamlit app instead of Ragie. Record `top_k`, the
  `mode` (`researcher` / `non_researcher`), and `answer_format`
  (`structured` / `freeform`) used for each run. Run the treatment in both modes;
  the dual-register capability is part of what is being tested.
- **Baseline B:** NotebookLM with the 27 PDFs from `documents/PDFs/` (the v1
  protocol says 15 — the corpus has grown).
- **Baseline A:** a current frontier chat model with web search enabled. Testing
  against a search-disabled model would be a straw man and the result would not
  survive scrutiny.

### 7b. Replace the question set

This is the most important change. v1's questions are broad, and on broad
questions a frontier model with search will tie or win. Test the differentiator
instead — the debate chains the corpus uniquely holds.

| # | Question | Why it discriminates |
|---|---|---|
| B1 | "What precisely do Van Nes et al. (2024) and Stige et al. (2025) disagree about regarding TLS calibration and lice mortality thresholds, and what evidence would resolve it?" | Corpus holds all three papers in the exchange. A general model will hedge or invent specifics. |
| B2 | "How well do the Norwegian TLS lice models predict observed post-smolt mortality, and what do the validation studies show?" | Requires Johnsen 2021, the Jansen & Gjerde comment, and Gjerde 2025 on PMLD predictive failure. |
| B3 | "What happened to sea lice on wild Pacific salmon after farms were removed from the Broughton Archipelago, and what does that imply for farm-attribution models?" | Two 2025 Jones papers, recent and low-profile. Strong hallucination bait. |
| B4 | "Does lice-induced smolt mortality translate into reduced adult returns, and how does it compare with other marine mortality drivers?" | Requires holding Jansen 2025 against Dadswell 2021, Jonsson 2016, Gillson 2022 without collapsing them. |
| **C1** | **"What is the life cycle of *Lepeophtheirus salmonis*?"** | **Deliberate control. Textbook material; the general model should win or tie. Include it.** |

C1 is not optional. A benchmark that only asks questions you expect to win is
marketing, not evidence, and a reviewer will say so. Reporting a loss on C1
alongside wins on B1–B4 is what makes the result credible — and it also sharpens
the real claim, which is narrow: this system is better *on contested questions*,
not better in general.

### 7c. Capture and score

For each question × system, save the verbatim output to
`eval/benchmark_runs/YYYY-MM-DD_<system>_<question_id>.md` with the configuration
in a header. Score on the existing v1 rubric (traceability, disagreement
surfacing, uncertainty handling, decision usefulness — 1–3 each). Record scores in
`eval/benchmark_runs/scores.csv`.

Add an explicit **hallucination check** not in v1: for every citation a system
produces, verify the cited paper exists and says what is claimed. Fabricated or
misattributed citations are the failure mode that matters most in a low-trust
governance setting, and it is the one a general model is most prone to.

### 7d. Note on cost

The treatment arm calls the OpenAI API for embeddings and synthesis. Five
questions × two modes is roughly ten synthesis calls — small. Confirm with Thord
before running, per the general rule above.

---

## Task 8 — implement the unused recall assertions (optional, small API cost)

`eval/smoke_queries.json` defines `must_include_any` per query, but
`scripts/eval_routing.py` only checks `expect_route` and ignores it entirely. So
retrieval recall is currently unmeasured.

Add `scripts/eval_retrieval.py` (do not overload `eval_routing.py`, which is
deliberately API-free) that embeds each smoke query, runs `retrieve_routed()`, and
asserts at least one `must_include_any` doc_id appears in the top-k. Report
per-query pass/fail and overall recall.

This matters strategically: it is the only cheap way to find out whether
retrieval is actually failing, which is the gate on the entire hybrid-BM25 and
reranking backlog. A pass here means that work can be deferred with evidence
rather than by assertion.

---

## Suggested order

1, 2, 3 first — the validator and the drift fix are self-contained and everything
else reads better on a clean corpus. Then 6 (documentation), then 5 (the parquet
bug). Task 4 blocks on Thord's answer, so raise the question early even though
the work comes later. Tasks 7 and 8 are the explorative half and need a cost
go-ahead.

## Definition of done

- `python scripts/validate_corpus.py` exits 0
- `python scripts/eval_routing.py` still reports 5/5
- `streamlit run app/app.py --server.fileWatcherType none` starts and answers a query
- `git status` clean, one commit per task, nothing pushed
- `STATUS.md` updated with what changed and what is still open
- This file deleted
