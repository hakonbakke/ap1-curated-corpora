# Taxonomy: Shared Tagging Vocabulary

This taxonomy defines the controlled vocabulary used across all three corpora.
All metadata fields referencing these terms must use the exact values listed here.

Refer to `shared/tagging_guide.md` for guidance on applying ambiguous tags.

---

## `source_type`

| Value | Description |
|---|---|
| `peer_reviewed` | Published in peer-reviewed journal |
| `institute_report` | Research institute report (HI, Nofima, Veterinærinstituttet, SINTEF, etc.) |
| `public_authority_report` | Regulatory or government report (Mattilsynet, Fiskeridirektoratet, NOU) |
| `fhf_report` | FHF-funded project report |
| `white_paper` | Industry or NGO white paper |
| `grey_literature` | Other documented sources not fitting above categories |

---

## `evidence_type`

| Value | Description |
|---|---|
| `empirical_experimental` | Controlled experiment with treatment/control |
| `empirical_observational` | Field or production data without experimental control |
| `model` | Mathematical or simulation model |
| `review` | Systematic or narrative review of existing literature |
| `qualitative` | Interview, case study, expert assessment |
| `regulatory` | Regulatory document, threshold-setting, policy assessment |

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
