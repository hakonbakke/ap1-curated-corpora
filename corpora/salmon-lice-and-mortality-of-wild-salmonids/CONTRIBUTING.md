# Slik legger du til et dokument

> Dette er guiden for deg som legger til artikler i korpuset.
> Du trenger kun å forholde deg til denne filen og `documents/`-mappen.

---

## Oversikt over workflowen

```
1. Finn artikkel
      ↓
2. Last opp PDF til SharePoint → Publications_candidates
      ↓
3. Flytt til Publications_selected (når du har vurdert at den er relevant)
      ↓
4. Bruk Claude til å fylle ut metadata
      ↓
5. Last opp metadata + PDF til GitHub
      ↓
6. Logg i inclusion_log.md
```

---

## Steg 1: Finn en relevant artikkel

Bruk søkeordene i `KEYWORDS.md` mot Google Scholar, Scopus eller
Web of Science.

Sjekk at artikkelen bidrar til minst ett av spørsmålene Q1–Q10
i `PRIORITY_QUESTIONS.md`.

Sjekk også at den oppfyller minstekravene i `CORPUS_CRITERIA.md`:
peer-reviewed artikkel, instituttrapport eller tilsvarende.
Ikke medieartikler eller presentasjoner uten metode.

---

## Steg 2: Last opp til SharePoint — Publications_candidates

Gå til SharePoint-gruppen **RAG_Salmon lice and wild salmonid mortality**.

Last opp PDF-en til mappen:
`Publications_candidates`

Dette er holdestedet for artikler du vurderer, men ennå ikke har
besluttet å inkludere.

---

## Steg 3: Flytt til Publications_selected

Når du har bestemt deg for at artikkelen skal inkluderes, flytt
PDF-en til:
`Publications_selected`

Artikler i denne mappen er besluttet inkludert og skal behandles
videre i GitHub.

> **Merk:** Hvis Ragnar Tveterås er tilgjengelig, kan han gjerne
> se over kandidatene i `Publications_candidates` før du velger ut.
> Hans faglige vurdering veier tyngre enn den automatiske.

---

## Steg 4: Lag AI-sammendrag med Claude

Åpne claude.ai og send denne meldingen:

---

```
Skriv et strukturert sammendrag av dette dokumentet for et vitenskapelig
evidenskorpus om lakselus og villaks. Inkluder disse seksjonene:
- Bakgrunn
- Metode
- Hovedfunn
- Usikkerhet og begrensninger
- Relevans for dette korpuset
- Relasjon til andre dokumenter

Vær nøytral og presis. Merk sammendraget som AI-generert.
[legg ved PDF-en]
```

---

Lagre Claude-svaret som `summary.md` i dokumentmappen på GitHub
(samme mappe som `metadata.yaml` og `original.pdf`).

---

## Steg 5: Fyll ut metadata med Claude

Åpne claude.ai og send denne meldingen:

---

*Kopier og lim inn dette til Claude:*

```
Du er kurator for et vitenskapelig evidenskorpus om lakselus og villaks.

Her er metadata-templaten vi bruker:
[lim inn hele innholdet fra metadata_template.yaml]

Her er dokumentet:
[legg ved PDF-en]

Fyll ut ALLE felt i templaten basert på dokumentet og din kunnskap om feltet.
Del A, B og C fyller du direkte fra dokumentet.
Del D og E fyller du som et informert faglig førsteutkast — disse vil bli
verifisert av en fagperson etterpå.
Vær nøytral og presis. Hvis du er usikker på et felt, skriv "unclear".
```

---

Les gjennom disse feltene selv før du laster opp:

- **`key_claims`** — er påstandene presise og nøytrale?
- **`coi_notes`** — sjekk at finansiering er nevnt (se bakerst i PDF-en)
- **`evidence_direction`** — støtter, utfordrer eller kritiserer studien
  påstanden om at lusepresset fra oppdrett skader villaks?
- **`consensus_signal`** og **`controversy_role`** — virker Claude sin
  plassering av dokumentet i litteraturen rimelig?

> **Husk:** Del D og E er Claude sitt førsteutkast — ikke fasit.
> Ragnar kan oppdatere disse feltene når han er tilgjengelig.
> Sett `curator_review_status: reviewed` når du har lest gjennom.

---

## Steg 6: Last opp til GitHub

Gå til:
`corpora/salmon-lice-and-mortality-of-wild-salmonids/documents/`

Klikk **Add file → Create new file**

Skriv filnavnet slik (opprett mappe automatisk med `/`):
```
2021_jfd_delousing-mortality/metadata.yaml
```

Lim inn det ferdigutfylte YAML-innholdet. Skriv en kort commit-melding:
```
Add 2021 JFD delousing mortality (Q7, Q8)
```

Last deretter opp PDF-en via **Add file → Upload files** til samme mappe.

---

## Steg 7: Logg beslutningen

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
    ├── metadata.yaml     ← fylt ut av Claude, verifisert av deg
    └── original.pdf      ← PDF-en fra Publications_selected
```

---

## Spørsmål?

Se `PRIORITY_QUESTIONS.md` for spørsmålene Q1–Q10.
Se `KEYWORDS.md` for søkeord til å finne nye artikler.
