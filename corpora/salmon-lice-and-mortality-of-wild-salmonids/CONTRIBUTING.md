# Slik legger du til et dokument

> **Tillitsmodell:** Mennesket velger papirer. AI ekstraherer, kuraterer og verifiserer mot kildetekst.
> Du trenger `KEYWORDS.md`, `PRIORITY_QUESTIONS.md`, og kommandoene under.

---

## Workflow (anbefalt)

```
1. Finn artikkel (Scholar / Scopus / WoS) — sjekk Q1–Q10
      ↓
2. Last opp PDF til SharePoint → Publications_selected
      ↓
3. Velg stabil doc_id: YYYY_journal_keyword
      ↓
4. Kjør AI-pipeline (extract → curate → verify → ingest)
      ↓
5. Les qa_report.json (spot-check). Logg i inclusion_log.md
```

---

## Steg 1–2: Velg papir (eneste menneskesteg som er påkrevd)

- Bruk `KEYWORDS.md` og minst ett spørsmål i `PRIORITY_QUESTIONS.md`.
- Minstekrav: peer-reviewed / instituttrapport e.l. — ikke medieartikler.
- PDF i SharePoint-gruppen **RAG_Salmon lice and wild salmonid mortality**
  (`Publications_selected`). PDF skal **ikke** committes til GitHub.

---

## Steg 3–4: Kjør pipeline

Fra repo-roten, med `OPENAI_API_KEY` satt (`.env`):

```powershell
cd "c:\Users\ThordHåkonBakke\OneDrive - Blue Planet AS\Koding\ap1-curated-corpora"

# Ny artikkel fra lokal PDF-kopi
python scripts/add_paper.py --doc 2025_journal_keyword --pdf "C:\path\to\paper.pdf"

# Eller: PDF allerede i documents/PDFs/ og mappet i convert_pdfs_odl.py
python scripts/add_paper.py --doc 2025_journal_keyword
```

Pipeline-steg:

| Steg | Script | Output |
|------|--------|--------|
| Extract | ODL (`convert_pdfs_odl` / `--pdf`) | `extracted.md` |
| Curate | `ai_curate_document.py` | `summary.md`, `metadata.yaml` (`ai_draft`) |
| Verify | `ai_verify_document.py` | `qa_report.json` → `ai_verified` eller `ai_draft` |
| Index | `ingest.py` | oppdaterer `data/corpus.parquet` |

Nyttige flagg:

```powershell
python scripts/add_paper.py --doc ID --force-curate   # overskriv summary/metadata
python scripts/add_paper.py --doc ID --verify-only    # kun checker
python scripts/add_paper.py --doc ID --skip-ingest
```

---

## Steg 5: Spot-check og logg

Les `documents/<doc_id>/qa_report.json`:

- `pass: true` + `final_status: ai_verified` → klar for bruk i RAG
- `pass: false` → se `critical_issues`; kjør `--force-curate` på nytt eller rett YAML manuelt

Logg i `inclusion_log.md`:

```
| 2026-08-03 | Forfatter et al. 2025 – tittel | INCLUDED | Q9 | Thord | ai_verified |
```

---

## Statusverdier (`curator_review_status`)

| Status | Mening |
|--------|--------|
| `ai_draft` | AI-fylt; ikke checker-godkjent (eller checker feilet) |
| `ai_verified` | Checker passerte mot `extracted.md` |
| `expert_approved` | Valgfri menneskelig ekspertgodkjenning (bonus) |
| `pending` | Eldre synonym for `ai_draft` (eksisterende 27 papirer) |

---

## Mappestruktur

```
documents/
└── 2025_journal_keyword/
    ├── extracted.md      ← fra PDF (ODL)
    ├── summary.md        ← AI
    ├── metadata.yaml     ← AI (+ status fra verify)
    └── qa_report.json    ← AI checker-rapport
```

---

## Spørsmål?

Se `PRIORITY_QUESTIONS.md`, `KEYWORDS.md`, og `WORKFLOW.md`.
Pipeline-detaljer: `possible_improvements/ai-curation-pipeline.md`.
