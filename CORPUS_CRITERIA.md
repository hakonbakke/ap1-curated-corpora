# Corpus Inclusion Criteria

These criteria apply to **all three corpora** in this repository.
Each corpus may additionally define narrower scope criteria in its own
`PRIORITY_QUESTIONS.md`.

---

## Document types included

| Type | Examples |
|---|---|
| Peer-reviewed articles | Journal of Fish Diseases, Aquaculture, ICES Journal |
| Research institute reports | Havforskningsinstituttet (HI), Nofima, Veterinærinstituttet |
| Public authority reports | Mattilsynet, Fiskeridirektoratet, NOU reports |
| Widely cited project reports | FHF project reports with documented methodology |
| Grey literature (selected) | NGO reports, industry white papers — only where explicitly relevant and methodologically documented |

---

## Document types excluded

- Media articles and news coverage
- Opinion pieces without documented empirical basis
- Presentations or slides without accompanying methodology
- Internal or confidential material
- Documents without date or attributable authorship

---

## Minimum requirements

A document must:
1. Have a **clear methodological basis** or explicit empirical/experiential grounding
2. Be relevant to at least one **priority question** in the corpus it enters
3. Be **dated and attributable** (author/institution, year)
4. Be **publicly accessible** or archived in this repository

---

## Discovery strategy

Candidate documents are identified through:
- Targeted searches in **Scopus**, **Google Scholar**, and **Web of Science**
- Review of reference lists from already-included documents
- Monitoring of **HI**, **Nofima**, and **Veterinærinstituttet** publication archives
- Suggestions from domain experts

Search terms and dates are recorded in each corpus's `inclusion_log.md`.

---

## Intentional balance

The corpus is constructed to include:
- Studies with **different conclusions** on contested questions
- Evidence from **different system types** and geographic contexts
- Both **older foundational work** and more recent studies
- Perspectives from **research, industry, and regulatory** sources where available

This is done explicitly to avoid false consensus and to enable structured
representation of genuine disagreement.

---

## Conflict of interest

The `coi_declared` field in document metadata records whether funding sources
and conflict-of-interest statements are present, absent, or unclear.

Documents with undisclosed industry or advocacy funding are not excluded,
but are flagged and interpreted with appropriate caution.

---

## Updating the corpus

Documents may be added at any time. Each addition must:
- Complete the full `metadata.yaml` template
- Be recorded in the corpus `inclusion_log.md` with date and rationale
- Be reviewed by at least one person other than the original curator
  (where possible)
