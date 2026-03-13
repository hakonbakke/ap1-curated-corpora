# Context and Problem Statement

## The problem this project addresses

In Norwegian aquaculture governance, decisions about production capacity,
regulation, and environmental management depend on a body of scientific evidence
that is large, contested, and difficult to navigate.

The problem is not a lack of knowledge. Considerable research exists on topics
such as sea lice pressure, delousing-related mortality, wild salmon interactions,
fish welfare, and the environmental performance of different production systems.

The problem is **how that knowledge is used** — or not used — in practice.

### Three compounding challenges

**1. Fragmented and inaccessible evidence**

Relevant knowledge is distributed across peer-reviewed journals, institute
reports, regulatory documents, white papers, and grey literature. No single
actor has the capacity to maintain a systematic overview. This creates an
uneven playing field: those with resources to commission synthesis have more
influence over what "the evidence says" than those who do not.

**2. Contested interpretations without visible structure**

On many central questions — such as the mortality effects of delousing
treatments, or the magnitude of lice-induced wild salmon mortality — different
studies reach different conclusions. This is not primarily a sign of poor science.
It reflects genuine variation in methods, contexts, production stages, and
geographies. However, without a structured way to represent this variation,
contested evidence tends to collapse into two rhetorical positions: "the science
is clear" and "the science is uncertain." Both are typically oversimplifications.

**3. Low institutional trust between key actors**

Industry, regulatory authorities, and the research community operate with
different knowledge hierarchies and different levels of trust in each other's
evidence claims. This makes it difficult to build shared understanding even
when the underlying evidence is compatible. Disagreements over policy are
frequently also disagreements over which evidence counts.

---

## Why generic AI does not solve this

A natural response is to ask: can't we just feed the documents to a large
language model and ask it what the evidence says?

This is technically possible. It is scientifically and institutionally
problematic.

Generic AI systems tend to:
- **prioritize confident summaries over nuanced methodological detail**,
  often missing key qualifications buried in methods or results sections
- **smooth over genuine disagreement** by defaulting to majority positions
  in their training data
- **provide no provenance**: it is not possible to verify which sources a
  claim is based on, or whether the model has accurately represented them
- **conflate empirical findings with normative assessments**, treating
  regulatory thresholds or precautionary judgements as factual conclusions

In a domain where evidence is contested and trust is low, these properties
are not merely inconvenient — they are counterproductive. A system that
produces authoritative-sounding summaries without traceable sources risks
hardening disagreement rather than clarifying it.

---

## What this project is trying to do

This repository is part of an effort to build a **transparent, traceable
evidence infrastructure** for use in contested aquaculture governance contexts.

The goal is not to build a better chatbot.

The goal is to establish a methodological foundation for AI-supported evidence
synthesis that is:

- **Traceable**: every claim links back to a specific document and passage
- **Contextualised**: findings are interpreted in light of production stage,
  system type, geography, and time period — not averaged across them
- **Honest about disagreement**: contradictory findings are preserved and
  made visible, not reconciled artificially
- **Accountable**: curatorial decisions are documented and open to challenge

The underlying assumption is that the value of this work lies in the **corpus
and the methodology**, not in the AI layer on top. Models will change. A
carefully curated, well-documented evidence base retains its value regardless
of which model queries it.

---

## What this project is not trying to do

- **Not a policy recommendation tool.** The system does not recommend
  regulatory thresholds, production limits, or management responses.
- **Not a neutral arbiter.** Curation involves human judgement. That judgement
  is made explicit and open to scrutiny, not hidden behind algorithmic authority.
- **Not a replacement for domain expertise.** The system supports researchers
  and analysts who already understand the domain. It does not substitute for
  that understanding.
- **Not claiming completeness.** The corpus is intentionally selective. It
  aims for representative coverage of key perspectives, not exhaustive coverage
  of all literature.

---

## The intended contribution

If successful, this approach demonstrates that:

1. Genuine scientific disagreement can be **structured rather than suppressed**
2. Evidence can be made **accessible without being simplified**
3. Curatorial choices can be made **transparent and contestable**
4. AI can support evidence synthesis in high-stakes policy contexts **without
   replacing human judgement or responsibility**

This is relevant not only for aquaculture governance, but for any domain where
large bodies of contested evidence must be navigated by multiple stakeholders
with different interests and different standards of proof.

---

*This repository is a working MVP. The corpora are incomplete.
The methodology is evolving. Contributions and critiques are welcome.*
