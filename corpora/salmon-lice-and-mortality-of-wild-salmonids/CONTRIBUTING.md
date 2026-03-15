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

## Steg 4: Fyll ut metadata med Claude

Åpne claude.ai og send denne meldingen:

---

*Kopier og lim inn dette til Claude:*

```
Du er kurator for et vitenskapelig evidenskorpus om lakselus og villaks.

Her er metadata-templaten vi bruker:
[lim inn hele innholdet fra metadata_template.yaml]

Her er dokumentet:
[legg ved PDF-en]

Fyll ut alle felt merket [CLAUDE] i templaten basert på dokumentet.
Feltene merket [FAGPERSON] og [KURATOR] skal du la stå tomme (null eller blank).
Vær nøytral og presis. Bruk bare informasjon som faktisk finnes i dokumentet.
Hvis du er usikker på et felt, skriv "unclear".
```

---

> **Merk:** Templaten har tre deler som Claude IKKE skal fylle ut:
> - **Del D** — `consensus_signal`, `quality_signal`, `controversy_role` osv.
>   Dette er syntesevurderinger som krever fagperson.
> - **Del E** — `related_documents_*`, `included_because`
>   Dette er kuratorvurderinger du fyller ut selv.

Les gjennom disse feltene selv før du fortsetter:

- **`included_because`** — skriv inn din egen begrunnelse for inkludering
- **`key_claims`** — er påstandene presise og nøytrale?
- **`coi_notes`** — sjekk at finansiering er nevnt (se bakerst i PDF-en)
- **`evidence_direction`** — støtter, utfordrer eller kritiserer studien
  påstanden om at lusepresset fra oppdrett skader villaks?

---

## Steg 5: Last opp til GitHub

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
    ├── metadata.yaml     ← fylt ut av Claude, verifisert av deg
    └── original.pdf      ← PDF-en fra Publications_selected
```

---

## Spørsmål?

Se `PRIORITY_QUESTIONS.md` for spørsmålene Q1–Q10.
Se `KEYWORDS.md` for søkeord til å finne nye artikler.
