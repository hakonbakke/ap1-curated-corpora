# Methodological Principles

This project follows an **Honest Broker** approach to research synthesis
(Pielke, 2007).

The purpose is not to recommend a single solution or to adjudicate scientific
disputes. It is to:
- structure available knowledge transparently
- make disagreement visible and contextualised
- clarify where uncertainty is genuine vs. where it is manufactured
- expand the decision space for users — not narrow it

---

## Core principles

### 1. Human curation first
All documents are selected and justified by humans.
AI is never used to decide what enters a corpus.
AI is used to retrieve, group, and support comparison — not to evaluate.

### 2. Explicit inclusion logic
Each document includes a short explanation of **why it is included**
and what role it plays in the broader knowledge landscape.
This is recorded in the document's `metadata.yaml` under `included_because`.

### 3. Context before conclusions
Findings are always interpreted in light of:
- production stage (smolt, post-smolt, grow-out)
- system type (open cage, semi-closed, RAS, land-based)
- geography and temperature regime
- time period and regulatory context

A finding is not portable across contexts unless that portability is
explicitly argued and evidenced.

### 4. Disagreement is a feature, not a bug
Contradictory findings are preserved and highlighted, not averaged away.
The `consensus_signal` field in metadata makes the degree of agreement
visible at the corpus level.

### 5. Normative and empirical claims are kept separate
Regulatory thresholds, precautionary judgements, and policy positions are
tagged and treated as normative — not as empirical findings. Conflating them
is a primary source of false consensus in contested policy domains.

### 6. AI as assistant, not authority
AI is used to:
- retrieve relevant passages across the corpus
- group findings thematically
- support structured comparative analysis

Final interpretation and responsibility remain with humans.

---

## Researcher role

This project operates in the tradition of the **Honest Broker** role as
defined by Pielke (2007): presenting the range of available options and
the evidence behind each, without advocating for a specific policy outcome.

This does not mean value-neutrality. Curation involves choices. Those choices
are made explicit, documented, and open to challenge.

---

## Transparency and accountability

All outputs are traceable to:
- specific documents (by filename and DOI)
- specific sections or passages
- explicit human curatorial decisions (recorded in `inclusion_log.md` per corpus)

This is essential for trust in contested policy and industry contexts.

---

## Known limitations

- **Single curator risk**: Where curation is performed by one person, decisions
  may reflect individual blind spots. This is documented and flagged.
- **Corpus incompleteness**: No corpus claims to be exhaustive. The corpus
  boundary is a methodological choice, not a claim about the full literature.
- **Model dependency**: AI-generated retrievals and summaries depend on the
  capabilities of the model used. These should be verified against source text.

---

## References

Pielke, R. A. (2007). *The Honest Broker: Making Sense of Science in Policy
and Politics*. Cambridge University Press.

Oliver, K. et al. (2014). A systematic review of barriers to and facilitators
of the use of evidence by policymakers. *BMC Health Services Research*, 14, 2.
