# Taxonomy: Shared Tagging Vocabulary

This taxonomy defines the controlled vocabulary used across all three corpora.
All metadata fields referencing these terms must use the exact values listed here.

**Note**: Some corpora define additional fields beyond this shared set.
The `salmon-lice-and-mortality-of-wild-salmonids` corpus uses an extended
schema (see `corpora/salmon-lice-and-mortality-of-wild-salmonids/metadata_template.yaml`)
with corpus-specific fields including `causal_chain_stage`, `host_species`,
`evidence_direction`, `controversy_role`, and others documented below.

Refer to `shared/tagging_guide.md` for guidance on applying ambiguous tags.

---

## `source_type`

| Value | Description |
|---|---|
| `peer_reviewed` | Published in peer-reviewed journal |
| `report` | Research institute report (HI, Nofima, Veterinærinstituttet, SINTEF, etc.) |
| `government_report` | Regulatory or government report (Mattilsynet, Fiskeridirektoratet, NOU) |
| `expert_group_report` | Report from an expert group (e.g. TLS expert group) |
| `white_paper` | Industry or NGO white paper |
| `thesis` | PhD or Master's thesis |
| `conference_paper` | Conference proceedings paper |
| `dataset` | Data descriptor or data paper |
| `commentary` | Commentary, letter, or opinion piece |
| `response` | Formal response or rebuttal to another publication |

---

## `evidence_type`

| Value | Description |
|---|---|
| `empirical_experimental` | Controlled experiment with treatment/control |
| `empirical_observational` | Field or production data without experimental control |
| `model` | Mathematical or simulation model |
| `review` | Narrative review of existing literature |
| `systematic_review` | Systematic review with defined search protocol |
| `meta_analysis` | Statistical synthesis across multiple studies |
| `methods` | Methodological paper, tool development |
| `commentary` | Commentary, opinion, letter |
| `response` | Formal response or rebuttal |
| `policy_assessment` | Regulatory document, threshold-setting, risk assessment |
| `mixed` | Combines more than one of the above |

---

## `production_stage`

| Value | Description |
|---|---|
| `broodstock` | Broodfish |
| `egg_fry` | Eggs and first feeding |
| `smolt` | Freshwater smolt phase |
| `post_smolt` | Early seawater phase |
| `grow_out` | Main production phase in sea |
| `pre_slaughter` | Final production phase |
| `wild` | Wild salmonids (not farmed) |

---

## `system_type`

| Value | Description |
|---|---|
| `open_cage` | Traditional open net-pen in sea |
| `semi_closed` | Partially enclosed sea-based system |
| `closed_containment` | Fully enclosed sea-based system |
| `ras` | Recirculating Aquaculture System (land-based) |
| `flow_through` | Flow-through land-based system |
| `natural` | Wild/natural environment (for wild salmonid studies) |

---

## `geography`

Free text, but use standardised terms where possible:
- Country: `Norway`, `Scotland`, `Canada`, `Chile`, etc.
- Norwegian production areas: `PO1` through `PO13`
  (matching the traffic light system zones)
- Region: `Northern Norway`, `Western Norway`, `Mid-Norway`, etc.

---

## `consensus_signal`

Curator's assessment of how this document fits the broader literature.
**This is a curatorial judgement, not a claim from the document itself.**

| Value | Description |
|---|---|
| `high_agreement` | Consistent with a clear majority of comparable studies |
| `moderate_agreement` | Broadly consistent but with notable variation |
| `mixed` | Results vary depending on context or sub-question |
| `context_dependent` | Findings are valid but highly contingent on specific conditions |
| `contested` | Findings are directly disputed by comparable studies |
| `insufficient_evidence` | Too few studies to assess agreement |

---

## `quality_signal`

Curator's overall assessment of methodological robustness.
**This is a curatorial judgement.**

| Value | Description |
|---|---|
| `strong` | Robust design, large dataset, transparent methods, peer-reviewed |
| `medium` | Adequate methods, some limitations, generally credible |
| `weak` | Notable methodological limitations, limited data, or unclear methods |

---

## `transferability`

How applicable are the findings beyond the specific study context?

| Value | Description |
|---|---|
| `high` | Findings likely applicable across many contexts |
| `medium` | Applicable with caution; context matters |
| `low` | Findings are highly context-specific |

---

## `coi_declared`

| Value | Description |
|---|---|
| `yes` | Conflict of interest statement present and clear |
| `no` | Explicitly states no conflict of interest |
| `unclear` | No statement found, or statement is ambiguous |

---

## Extended fields — `salmon-lice-and-mortality-of-wild-salmonids` corpus

The following fields are specific to the wild salmonids corpus and map
to the 10-step causal chain in that corpus's `PRIORITY_QUESTIONS.md`.

### `causal_chain_stage`

| Value | Causal chain position |
|---|---|
| `farm_lice_abundance` | Lice load on farmed fish |
| `lice_reproduction` | Egg production and reproductive output |
| `larval_production` | Nauplius/copepodid production |
| `larval_dispersal` | Hydrodynamic transport of larvae |
| `environmental_drivers` | Temperature, salinity, current effects |
| `host_exposure` | Smolt encounter with lice plumes |
| `infestation` | Attachment and lice load on wild fish |
| `physiological_effects` | Skin damage, osmoregulation, stress |
| `behaviour` | Avoidance, reduced performance |
| `individual_mortality` | Dose–response, lice-induced death |
| `population_impacts` | Marine survival, SAR, recruitment |
| `monitoring_methods` | Field sampling design and limitations |
| `model_calibration` | Fitting models to observational data |
| `model_validation` | Testing model predictions against data |
| `regulatory_assessment` | TLS classification, threshold evaluation |

### `evidence_direction`

Curator's assessment of the paper's substantive thrust relative to the
central proposition: *farm lice contribute to harmful effects or mortality
in wild salmonids.*

| Value | Meaning |
|---|---|
| `supports_effect` | Evidence supports the proposition |
| `weak_support` | Some support, but limited or equivocal |
| `mixed_within_study` | Results point in different directions within the study |
| `no_effect_detected` | No significant effect found |
| `contradicts_effect` | Evidence argues against the proposition |
| `critiques_methodology` | Challenges methods used to establish the effect |
| `not_applicable` | Not directly about this proposition |

### `controversy_role`

| Value | Description |
|---|---|
| `foundational` | Establishes a key concept, model, or baseline |
| `supportive` | Adds evidence in the dominant direction |
| `critical` | Raises methodological or empirical challenges |
| `rebuttal` | Directly responds to or refutes another study |
| `bridge_between_positions` | Connects or mediates opposing views |
| `peripheral` | Indirectly relevant, contextual |
| `not_applicable` | Not part of a recognised debate |

### `uncertainty_emphasis`

| Value | Description |
|---|---|
| `low` | Paper does not emphasise uncertainty |
| `moderate` | Some discussion of uncertainty or limitations |
| `high` | Uncertainty is a central theme |
| `very_high` | Paper's main contribution is uncertainty analysis |
| `not_stated` | No discussion of uncertainty |

### `wild_or_farmed_focus`

| Value | Description |
|---|---|
| `wild` | Study focuses on wild salmonids |
| `farmed` | Study focuses on farmed fish |
| `both` | Covers both wild and farmed fish |
| `not_applicable` | Neither |

### `relevance_signal`

| Value | Description |
|---|---|
| `high` | Central to one or more priority questions |
| `medium` | Relevant but not core |
| `low` | Peripheral — context only |
