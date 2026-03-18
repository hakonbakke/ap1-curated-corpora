# Tagging Guide

This guide provides practical guidance for applying the metadata schema
to real documents. For the controlled vocabulary itself, see `TAXONOMY.md`.

---

## General principles

- Tag what the document **actually studies**, not what it mentions in passing
- When in doubt, use a **more conservative** tag (`unclear` for COI,
  `mixed` for consensus)
- Claude fills all fields as a first draft. Synthesis-level fields
  (`consensus_signal`, `quality_signal`, `controversy_role`, `included_because`)
  should be reviewed by a human or expert before setting `curator_review_status: reviewed`
- If a field is genuinely unclear, use the most conservative option and
  add a note in `curator_note`

---

## `evidence_type` — common ambiguous cases

**Model vs. empirical_observational**
If a study uses a mathematical model fitted to observational data, classify
as `model`. If it analyses field or production data directly without
a mechanistic model, classify as `empirical_observational`.

**Review vs. systematic review vs. meta-analysis**
Use `review` for narrative reviews, `systematic_review` for reviews with
a defined search protocol, and `meta_analysis` for statistical syntheses.
Note details in `quality_rationale`.

**Regulatory**
Use for documents whose primary purpose is to set, evaluate, or document
regulatory thresholds or standards. A scientific paper cited in a regulatory
context remains its original evidence type.

---

## `consensus_signal` — how to assign

This field describes the document in relation to the broader literature,
not the document's own conclusions. Ask:

> *If I placed this document alongside all other comparable studies,
> would it be consistent with the majority, or would it stand out?*

- `high_agreement` — consistent with clear scientific consensus
- `moderate_agreement` — broadly consistent, some variation
- `mixed` — results depend on sub-question or context within the paper
- `context_dependent` — findings are internally consistent but only valid
  under specific conditions (e.g. a specific temperature range or geography)
- `contested` — directly contradicted by comparable studies of similar quality
- `insufficient_evidence` — too few comparable studies to judge

When uncertain, default to `mixed` and explain in `quality_rationale`.

---

## `quality_signal` — how to assign

Ask:
> *How confident am I that the core findings are methodologically sound
> and reproducible?*

**Strong**
- Peer-reviewed in a credible journal
- Large dataset or robust experimental design
- Methods are transparent and replicable
- Results are clearly bounded with uncertainty estimates

**Medium**
- Peer-reviewed or credible institute report
- Some methodological limitations but not disqualifying
- Findings are plausible and internally consistent

**Weak**
- Limited data or sample size
- Methods not fully described
- Significant confounders not addressed
- Self-reported or industry-only data without independent verification
- Grey literature without peer review

---

## `included_because` — what to write

This is the most important field in the schema. A good entry:
- States the *role* the document plays in the knowledge landscape
- Explains *why* it is included relative to the priority questions
- Does NOT just summarise the document's conclusions

**Good example:**
> "Peer-reviewed observational study providing one of the few large-scale
> quantitative estimates of post-treatment mortality distributions across
> multiple delousing methods. Included as a central quantitative reference
> for Q1, and as a document frequently cited in regulatory discussions.
> Complements mechanistic welfare studies by providing population-level
> distributional data."

**Poor example:**
> "Relevant study about delousing and mortality."

---

## `key_claims` — how to write

- Write in **neutral, declarative language** — not "the authors claim" or
  "the study proves", but a direct factual statement
- Capture the **central empirical finding or contribution**, not every result
- Limit to 2–4 claims per document
- Do NOT paraphrase in a way that exaggerates certainty or downplays caveats

**Good example:**
> "Cage-level mortality following delousing shows substantial variation
> across treatment types, better described by distributions than by
> single average values."

**Poor example:**
> "Delousing causes significant mortality in salmon."
> *(Too vague; doesn't reflect the study's specific contribution)*

---

## Multiple corpora

A document may belong to more than one corpus. In that case:
- Include it in each relevant corpus folder
- Adjust `relevance_rationale`, `priority_questions`, and `included_because`
  to reflect the role in *that specific corpus*
- Core metadata fields (title, year, evidence_type, etc.) remain identical
