# Curation and Synthesis Workflow

This document describes the step-by-step process for adding documents
to a corpus and producing structured synthesis outputs.

The workflow applies to all three corpora. It follows Bjelland (2026)'s
pipeline principle: defined phases with explicit inputs and outputs.

**Trust model (2026-08):** The only required human checkpoint is **paper
selection (inclusion)**. Extraction, metadata, summary, and verification
against `extracted.md` are AI-driven (`scripts/add_paper.py`). Expert
sign-off (`expert_approved`) is optional, not a gate for corpus use.

---

## Overview

```
IDENTIFY → FETCH → CONVERT → AI-CURATE → AI-VERIFY → INDEX → SYNTHESISE
                ↑ human: select paper only
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
- Store PDF in SharePoint under `Publications_selected`
- Generate a stable identifier (folder name = `YYYY_journal_keyword`)

**Output**: PDF in SharePoint; document folder created in GitHub

---

## Stage 3–5: EXTRACT → AI-CURATE → AI-VERIFY (one command)

**Goal**: From selected PDF to indexed, checker-audited corpus record.

**Preferred command**:

```powershell
python scripts/add_paper.py --doc YYYY_journal_keyword --pdf path\to\paper.pdf
```

This runs:

1. **EXTRACT** — OpenDataLoader PDF → `extracted.md`
2. **AI-CURATE** — `scripts/ai_curate_document.py` → `summary.md` + `metadata.yaml` (`ai_draft`)
3. **AI-VERIFY** — `scripts/ai_verify_document.py` → `qa_report.json`; status `ai_verified` or `ai_draft`
4. **INDEX** — `scripts/ingest.py --doc …` → `data/corpus.parquet`

**Outputs per document folder**:
`extracted.md`, `summary.md`, `metadata.yaml`, `qa_report.json`

**Status values** (`curator_review_status`):

| Status | Meaning |
|--------|---------|
| `ai_draft` | AI-filled; checker not passed |
| `ai_verified` | Checker passed against extract |
| `expert_approved` | Optional human expert sign-off |
| `pending` | Legacy (= treat as `ai_draft`) |

**Human checkpoint**: Inclusion only (Stage 1–2). Spot-check `qa_report.json`
when adding high-stakes TLS/debate papers. Expert approval is bonus capacity,
not a required gate.

Optional — expand `summary.md` into a longer evidence brief:

```powershell
python scripts/expand_summaries_from_extract.py --min-chars 4500
python scripts/ingest.py
```

The Streamlit app passes `summary.md` (as `summary_text`) to GPT at answer time;
embeddings still use `rag_summary` + `key_claims`.

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
| AI summary | `summary.md` | — |
| Metadata | `metadata.yaml` | — |
| Original PDF | Stored in SharePoint `Publications_selected` | — |
| Synthesis output | `YYYY-MM-DD_Q[n]_[topic].md` | `2026-03-01_Q1_lice-smolt-mortality.md` |

---

## References

Bjelland, H. (2026). *Agentbasert dokumentanalyse: Metode, kvalitetssikring
og risikohåndtering*. Presentation, January 14, 2026.
