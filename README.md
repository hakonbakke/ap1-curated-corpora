# AP1 Curated Corpora

This repository contains **three curated research corpora** developed as part of
Havbruksløftet AP1 — a synthesis project funded by FHF (2025–2027), led by the
University of Stavanger.

Each corpus addresses a distinct but related analytical question about salmon
aquaculture and its interactions with fish health, welfare, and wild populations.

---

## Repository structure

```
ap1-curated-corpora/
│
├── README.md               ← this file
├── Context.md              ← problem statement and project rationale
├── METHOD.md               ← methodological principles (Honest Broker approach)
├── CORPUS_CRITERIA.md      ← rules governing document inclusion
├── TAXONOMY.md             ← shared tagging vocabulary across all corpora
├── WORKFLOW.md             ← step-by-step curation and synthesis workflow
│
├── corpora/
│   └── salmon-lice-and-mortality-of-wild-salmonids/
│       ├── metadata_template.yaml   ← corpus-specific template
│       ├── PRIORITY_QUESTIONS.md
│       ├── KEYWORDS.md
│       ├── CONTRIBUTING.md
│       ├── inclusion_log.md
│       ├── documents/
│       │   └── YYYY_journal_keyword/
│       │       ├── summary.md       ← AI-generated summary
│       │       ├── metadata.yaml    ← filled by Claude, reviewed by human
│       │       └── original.pdf
│       └── synthesis/               ← cross-document syntheses (future)
│
└── shared/
    ├── tagging_guide.md
    └── templates/
        └── metadata_template.yaml   ← generic baseline for new corpora
```

---

## The three corpora

### 1. `salmon-lice-and-mortality-of-wild-salmonids`
Evidence on sea lice transmission from salmon farms to wild salmonids, and
its effects on wild population mortality. Directly relevant to the traffic
light system (trafikklyssystemet) and capacity regulation.

### 2. `salmon-lice-and-farmed-salmon-welfare-and-mortality`
Evidence on the effects of lice infestations and delousing treatments on
the welfare and survival of farmed Atlantic salmon. Relevant to production
risk, treatment regulation, and fish welfare standards.

### 3. `salmon-mortality`
Evidence on production mortality in farmed Atlantic salmon from all causes
(disease, handling, biological factors, systems). Provides the broader
production context within which lice-related mortality should be interpreted.

---

## Shared infrastructure

All three corpora share the same:
- **Tagging vocabulary** (`TAXONOMY.md` + `shared/tagging_guide.md`)
- **Methodological principles** (`METHOD.md`)
- **Inclusion criteria** (`CORPUS_CRITERIA.md`)

Each active corpus maintains its own **corpus-specific metadata template**
in `corpora/[corpus-name]/metadata_template.yaml`. These templates extend
the shared vocabulary with fields specific to the corpus's causal chain and
priority questions. `shared/templates/metadata_template.yaml` serves as
the baseline for new corpora not yet built.

This ensures findings can be compared and synthesised across corpora
where questions overlap, while allowing each corpus the flexibility to
capture evidence dimensions specific to its domain.

---

## Status

This repository is a **working MVP**. All corpora are incomplete and will
be expanded iteratively. Contributions, critiques, and suggested documents
are welcome via Issues.

> The corpus is the infrastructure. The AI is a query layer on top of it.
