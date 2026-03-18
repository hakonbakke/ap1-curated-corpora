# Slik legger du til et dokument

> Guiden for deg som legger til artikler i korpuset.
> Du trenger kun denne filen, `KEYWORDS.md` og `PRIORITY_QUESTIONS.md`.

---

## Workflow

```
1. Finn artikkel (Google Scholar / Scopus / Web of Science)
      ↓
2. Last opp PDF til SharePoint → Publications_candidates
      ↓
3. Flytt til Publications_selected (når den er vurdert relevant)
      ↓
4. Gi Claude PDF + template → får summary.md og metadata.yaml
      ↓
5. Last opp summary.md og metadata.yaml til GitHub
      ↓
6. Logg i inclusion_log.md
```

---

## Steg 1: Finn en relevant artikkel

Bruk søkeordene i `KEYWORDS.md` mot Google Scholar, Scopus eller
Web of Science.

Sjekk at artikkelen bidrar til minst ett av spørsmålene Q1–Q10
i `PRIORITY_QUESTIONS.md`.

Minstekrav: peer-reviewed artikkel, instituttrapport eller tilsvarende.
Ikke medieartikler eller presentasjoner uten metode.

---

## Steg 2–3: SharePoint

Last opp PDF-en til SharePoint-gruppen
**RAG_Salmon lice and wild salmonid mortality**:

- `Publications_candidates` — artikler du vurderer
- `Publications_selected` — artikler besluttet inkludert

> Hvis Ragnar er tilgjengelig, kan han se over kandidatene
> i `Publications_candidates` før du velger ut.

PDF-ene lagres i SharePoint — de skal **ikke** lastes opp til GitHub.

---

## Steg 4: Lag summary og metadata med Claude

Åpne claude.ai og send **én melding** med to oppgaver:

```
Du er kurator for et vitenskapelig evidenskorpus om lakselus og villaks.
Jeg gir deg et dokument og en metadata-template.

Oppgave 1: Skriv et strukturert sammendrag (summary.md) med seksjonene:
- Bakgrunn
- Metode
- Hovedfunn
- Usikkerhet og begrensninger
- Relevans for dette korpuset
- Relasjon til andre dokumenter
Merk sammendraget som AI-generert.

Oppgave 2: Fyll ut ALLE felt i metadata-templaten.
Del A, B og C fyller du direkte fra dokumentet.
Del D og E fyller du som et informert faglig førsteutkast.
Hvis du er usikker på et felt, skriv "unclear".

Her er metadata-templaten:
[lim inn hele innholdet fra metadata_template.yaml]

Her er dokumentet:
[legg ved PDF-en]
```

---

**Les gjennom før du laster opp:**

- **`key_claims`** — presise og nøytrale?
- **`coi_notes`** — sjekk finansiering (se bakerst i PDF-en)
- **`evidence_direction`** — støtter, utfordrer eller kritiserer studien?
- **`consensus_signal`** og **`controversy_role`** — rimelig plassering?

> Del D og E er Claude sitt førsteutkast — ikke fasit.
> Sett `curator_review_status: reviewed` når du har lest gjennom.

---

## Steg 5: Last opp til GitHub

Gå til: `corpora/salmon-lice-and-mortality-of-wild-salmonids/documents/`

Klikk **Add file → Create new file**

Opprett `summary.md` med filnavnet:
```
2021_jfd_delousing-mortality/summary.md
```

Gjenta for `metadata.yaml`:
```
2021_jfd_delousing-mortality/metadata.yaml
```

Skriv en kort commit-melding:
```
Add 2021 JFD delousing mortality (Q7, Q8)
```

---

## Steg 6: Logg beslutningen

Legg til en rad i `inclusion_log.md`:

```
| 2026-03-10 | Forfatter et al. 2021 – tittel | INCLUDED | Relevant for Q7 | Erik |
```

---

## Mappestruktur per dokument i GitHub

```
documents/
└── 2021_jfd_delousing-mortality/
    ├── summary.md        ← AI-generert sammendrag
    └── metadata.yaml     ← fylt ut av Claude, verifisert av deg
```

PDF-en ligger i SharePoint under `Publications_selected`.

---

## Spørsmål?

Se `PRIORITY_QUESTIONS.md` for spørsmålene Q1–Q10.
Se `KEYWORDS.md` for søkeord til å finne nye artikler.
