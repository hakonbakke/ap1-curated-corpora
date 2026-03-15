# Slik legger du til et dokument

> Dette er guiden for deg som legger til artikler i korpuset.
> Du trenger kun å forholde deg til denne filen og `documents/`-mappen.

---

## Det du trenger

- Ein PDF du vil legge til
- Claude i nettleseren (claude.ai)
- GitHub-tilgang til dette repoet

---

## Steg for steg

### 1. Sjekk at dokumentet er relevant

Åpne `PRIORITY_QUESTIONS.md` og sjekk at dokumentet bidrar til
minst ett av spørsmålene Q1–Q10.

Sjekk også `CORPUS_CRITERIA.md` i rotmappen — dokumentet må være
peer-reviewed, en instituttrapport, eller tilsvarende.
Ikke medieartikler eller presentasjoner uten metode.

---

### 2. Be Claude fylle ut metadata

Åpne claude.ai. Send denne meldingen (tilpass siste linje):

---

*Kopier og lim inn dette til Claude:*

```
Du er kurator for et vitenskapelig evidenskorpus om lakselus og villaks.

Her er metadata-templaten vi bruker:
[lim inn hele innholdet fra metadata_template_mvp.yaml]

Her er dokumentet:
[legg ved PDF-en]

Fyll ut alle felt i templaten basert på dokumentet.
Vær nøytral og presis. Bruk bare informasjon som faktisk finnes i dokumentet.
Hvis du er usikker på et felt, skriv "unclear".
```

---

### 3. Les gjennom disse feltene selv

Før du laster opp, les gjennom og juster om nødvendig:

- **`included_because`** — gir begrunnelsen mening?
- **`key_claims`** — er påstandene presise og nøytrale?
- **`coi_notes`** — sjekk at finansiering er nevnt (se bakerst i PDF-en)
- **`evidence_direction`** — støtter, utfordrer eller kritiserer studien påstanden om at lusepresset fra oppdrett skader villaks?

---

### 4. Legg det inn i GitHub

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

### 5. Logg beslutningen

Legg til en rad i `inclusion_log.md`:

```
| 2026-03-10 | Forfatter et al. 2021 – tittel | INCLUDED | Relevant for Q7 | Erik |
```

---

## Mappestruktur per dokument

```
documents/
└── 2021_jfd_delousing-mortality/
    ├── metadata.yaml     ← fylt ut av Claude, verifisert av deg
    └── original.pdf      ← PDF-en
```

Det er alt. Ingen andre filer er nødvendig.

---

## Spørsmål?

Se `PRIORITY_QUESTIONS.md` for spørsmålene Q1–Q10.
Se `KEYWORDS.md` for søkeord til å finne nye artikler.
