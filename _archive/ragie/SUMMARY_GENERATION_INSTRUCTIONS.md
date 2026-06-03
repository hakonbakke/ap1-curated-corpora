# Instructions: retrieval-optimised summaries (AP1 curated layer)

Use when writing or revising corpus summaries intended for **Ragie partition `ap1-curated-summaries`**.

## Role of this layer

These files are **not** general-audience abstracts. They are **retrieval targets**: short, claim-dense text so vector search returns explicit findings, disagreement, and population-level links—not boilerplate or YAML keys.

## Required file naming

- One file per document: `{document_id}.summary.md`
- Canonical upload bundle (archived): `_archive/ragie/retrieval_summaries_bundle/summaries/`

## Required markdown structure

```markdown
# [Full bibliographic title]

**Document ID:** `{document_id}`
**DOI:** https://doi.org/...  (or **Primary link:** for reports without DOI)
**Priority questions:** Q1, Q2, …  (from metadata.yaml)
**Provenance:** (only if needed — e.g. AI-assisted draft in corpus, COI, institutional authorship)

## Key findings
- Explicit claim (X → Y); quantitative results when the source states them
- Tie to mortality, returns, or population effects when applicable

## Evidence type
- empirical / model / review / critique / policy_assessment / dataset_description / commentary / response (as appropriate; can list multiple)

## Population-level relevance
- Mortality / returns / population viability: what the study says or does not say

## Competing or conflicting points
- How this work supports, contradicts, or qualifies other studies or TLS assumptions

## Uncertainty / limitations
- Methodological or interpretive limits stated or implied in the source

## Context
- Geography:
- Life stage:
- System type:
- Time period:
```

## LLM / author prompt (copy-paste)

```
Write the summary for retrieval and evidence synthesis, not for general reading.

Requirements:
- Use short, explicit claims.
- State findings directly (X causes Y / X is associated with Y / models show Z).
- Prefer quantitative results when available from the source only; do not invent numbers.
- Clearly state population-level relevance (mortality, adult returns, population viability) or state that the study does not address that scale.
- Explicitly include disagreement or critique if present in the document.
- Avoid generic phrases like "this paper is important because".
- Avoid long background sections.
- Follow the exact section headings: Key findings, Evidence type, Population-level relevance, Competing or conflicting points, Uncertainty / limitations, Context.
```

## Quality checks before ingest

- [ ] No pasted YAML or template keys as prose
- [ ] At least one bullet under **Competing or conflicting points** for contested TLS literature (or explicit "no direct critique of named studies" if truly absent)
- [ ] **Context** filled from `metadata.yaml` where available
