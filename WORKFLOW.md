# Curation and Synthesis Workflow

This document describes the step-by-step process for adding documents
to a corpus and producing structured synthesis outputs.

The workflow applies to all three corpora. It follows Bjelland (2026)'s
pipeline principle: defined phases with explicit inputs and outputs,
human checkpoints at each stage boundary.

---

## Overview

```
IDENTIFY → FETCH → CONVERT → CURATE → VALIDATE → INDEX → SYNTHESISE
```

---

## Stage 1: IDENTIFY

**Goal**: Generate a list of candidate documents for a corpus.

**Input**: Priority questions from `PRIORITY_QUESTIONS.md`

**Actions**:
- Run targeted searches in Scopus, Google Scholar, Web of Science
- Review reference lists of already-included documents
- Check HI, Nofima, Veterinærinstituttet, and FHF publication archives
- Record search terms, databases, and date in `inclusion_log.md`

**Output**: List of candidate documents with title, author, year, DOI/URL

**Human checkpoint**: Curator reviews candidate list and makes initial
inclusion/exclusion decisions before proceeding.

---

## Stage 2: FETCH

**Goal**: Obtain the full document.

**Actions**:
- Download PDF from DOI, publisher, or open repository
- For paywalled content: use institutional access or contact authors
- Store original file as `original.pdf` in the document folder
- Generate a stable identifier (folder name = `YYYY_journal_keyword`)

**Output**: `original.pdf` in `documents/YYYY_journal_keyword/`

---

## Stage 3: CONVERT

**Goal**: Convert PDF to machine-readable text for AI-assisted analysis.

**Actions**:
- Convert PDF to Markdown using a PDF extraction tool
- Store as `document.md` in the same folder
- Flag any conversion quality issues (OCR problems, tables, figures)

**Output**: `document.md` alongside `original.pdf`

---

## Stage 4: CURATE

**Goal**: Complete the metadata record and document the inclusion decision.

**Actions**:
- Copy the corpus-specific `metadata_template.yaml` to `documents/YYYY_journal_keyword/metadata.yaml`
- Give Claude the template and the PDF; Claude fills all fields as a first draft
- Del A–C: Claude extracts from the document directly
- Del D–E: Claude provides an informed first draft; a human or expert reviews and corrects
- Record inclusion decision in `inclusion_log.md`

**Output**: Completed `metadata.yaml` with `curator_review_status: pending`

**Human checkpoint**: Review Del D (`consensus_signal`, `quality_signal`,
`controversy_role`) and Del E (`included_because`, `related_documents_*`)
before setting `curator_review_status: reviewed`. Expert sign-off sets it to `approved`.

---

## Stage 5: VALIDATE

**Goal**: Quality-check the metadata record before it enters the corpus.

**Actions**:
- Verify that `key_claims` accurately reflect the document content
- Check that `consensus_signal` is consistent with other documents
  on the same question
- Confirm `coi_declared` against the document's funding statement
- A second reviewer checks the record where possible

**Output**: Validated `metadata.yaml`, noted in `inclusion_log.md`

---

## Stage 6: INDEX

**Goal**: Ensure the document is discoverable and linked to priority questions.

**Actions**:
- Add document to the corpus `README.md` document list
- Tag with all relevant priority question IDs from `PRIORITY_QUESTIONS.md`
- Commit to repository with a clear commit message

**Output**: Document appears in corpus overview; retrievable by AI query layer

---

## Stage 7: SYNTHESISE

**Goal**: Produce structured outputs that answer priority questions
across multiple documents.

**Actions**:
- Use AI retrieval to identify passages relevant to a specific question
- Draft structured synthesis in `synthesis/` folder
- Each synthesis document must:
  - state which priority question it addresses
  - cite specific documents and passages
  - preserve disagreement (not resolve it artificially)
  - distinguish empirical findings from normative assessments
  - note confidence and transferability limitations

**Output**: Synthesis document in `synthesis/YYYY-MM-DD_Q[n]_[topic].md`

**Human checkpoint**: All synthesis outputs are reviewed and approved
by a human curator before being treated as corpus outputs.

---

## File naming conventions

| File | Convention | Example |
|---|---|---|
| Document folder | `YYYY_journal-abbrev_keyword` | `2021_jfd_delousing-mortality` |
| Original PDF | `original.pdf` | — |
| Converted text | `document.md` | — |
| Metadata | `metadata.yaml` | — |
| Synthesis output | `YYYY-MM-DD_Q[n]_[topic].md` | `2026-03-01_Q1_lice-smolt-mortality.md` |

---

## References

Bjelland, H. (2026). *Agentbasert dokumentanalyse: Metode, kvalitetssikring
og risikohåndtering*. Presentation, January 14, 2026.
