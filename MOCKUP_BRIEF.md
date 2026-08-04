# MOCKUP BRIEF — clickable theme page prototype

**Transient working file. Delete after the demo, or promote to `docs/` if the design is adopted.**

Written 2026-08-04 as an execution spec for an implementing agent.
Design and content decisions have already been made and are written out below —
**apply them as specified, do not re-derive them.**

**Hard deadline: must be demo-ready 2026-08-05 morning.** Ship something complete and
plain rather than something ambitious and half-built.

---

## 1. What this is and who sees it

A single-file, clickable, offline HTML prototype of one theme page:
*salmon lice and mortality of wild salmonids*.

It is shown on a laptop, in person, to **Ragnar Tveterås** — the domain expert who
selected all 27 papers in the corpus. He is a researcher. He will read the content, not
just look at the layout. Assume he knows this literature better than anyone in the room.

**The argument the mockup must make, in this order:**

1. The corpus catches real errors that a general model produces confidently. *(Proof, not claim — see §5.1.)*
2. A reader gets oriented before being asked to type a question.
3. Scientific disagreement is shown as structure, not resolved into an answer.
4. Every claim can be opened to the sentence it came from.

**What it must not do:** look like a finished product, or imply content exists that
doesn't. Ragnar's trust is the asset. Overclaiming in a mockup spends it.

---

## 2. Ground rules

1. **Invent no content.** Every factual sentence about lice, salmon, models or
   regulation must come from a file listed in §4. If you need a claim you cannot
   source, render a visible grey placeholder box reading `[innhold mangler]` instead.
   A visible gap is fine. A plausible invention shown to a domain expert is not.
2. **Do not soften or paraphrase numbers.** Copy them exactly as they appear in the
   source, including the uncertainty. `ρ = −0.66` not "a strong correlation".
3. **No regulatory facts beyond the two in §4.4.** Everything else about Norwegian law
   goes in as a placeholder. This is the failure mode the page exists to prevent; do not
   reproduce it inside the mockup.
4. **No API calls, no network at runtime.** See §3.
5. **Do not modify the Streamlit app.** Nothing under `app/` changes. This prototype
   lives in its own folder and is disposable.
6. **Do not modify anything in `corpora/`.** Read-only. Never edit `extracted.md`.
7. Shell is PowerShell. `ls -la`, `cat`, `grep` will fail.
8. `git` is not on PATH. Prepend per session: `$env:PATH += ";C:\Program Files\Git\cmd"`

---

## 3. Technical constraints

| Constraint | Value | Why |
|---|---|---|
| Output | **One** file: `mockup/tema-villaks.html` | Emailable, copyable to a stick, no install |
| Dependencies | **None.** No npm, no build step, no CDN, no webfonts | Meeting-room wifi will fail. Assume offline. |
| CSS | Inline in `<style>` | Single file |
| JS | Inline vanilla, no framework | Single file; interactions are trivial |
| Fonts | System stack: `-apple-system, "Segoe UI", Roboto, sans-serif` | No network |
| Target | Chrome/Edge, laptop at 1280–1600px wide | Known display |
| Images | Only if inlined as base64, and only if genuinely needed | Single file |

Test by opening the file with wifi switched off. If anything fails to render, it is broken.

**Design fidelity note:** this deliberately is not built in Streamlit, so the design
conversation isn't constrained by Streamlit's layout limits. Keep the layout to things
Streamlit can plausibly reach later — columns, containers, expanders, tabs, buttons,
pills. **Do not** use hover-dependent interactions, sticky sidebars, animated
transitions, or anything requiring precise pixel control. If a layout choice would need
a custom React component to port, don't use it.

---

## 4. Content sources — the only places content may come from

Paths relative to workspace root
`C:\Users\ThordHåkonBakke\OneDrive - Blue Planet AS\Koding\`.

### 4.1 Verified quotes — the preferred source

`Villlaks_analyse\docs\litteratur_verifisering.md`

This file contains claim-by-claim verification of 10 papers against the corpus
extractions, with exact quotes and section references, checked 2026-07-07.
**Prefer these quotes over anything you extract yourself.** They are the only quotes in
the project that a human has already checked.

### 4.2 Corpus documents

`ap1-curated-corpora\corpora\salmon-lice-and-mortality-of-wild-salmonids\documents\<doc_id>\`

- `extracted.md` — source text. Quote from here **only** for papers absent from §4.1.
- `summary.md` — AI-written summary
- `metadata.yaml` — tags, `controversy_role`, `main_uncertainty_sources`, funding

### 4.3 Debate structure

`ap1-curated-corpora\corpora\salmon-lice-and-mortality-of-wild-salmonids\PRIORITY_QUESTIONS.md`

Every question Q1–Q10 has an **Expected disagreement** paragraph. These are the
pre-written fault lines. Use them as the framing text for the debate cards in §5.3.

### 4.4 The only two permitted regulatory facts

Both already externally verified in
`Villlaks_analyse\docs\audit_rettsrapport_forsvar.md` §2.5:

- Styringsgruppen rated **PO3 high** and **PO4 moderate** for 2024–25 *(checked against trafikklyssystemet.no)*
- NFD's 2026 decision: **PO3 red, −6% capacity; PO4 yellow** *(checked against regjeringen.no)*

Render both with a visible check date of 2026-07-27. Everything else regulatory is a placeholder.

### 4.5 Existing app behaviour to mirror

`ap1-curated-corpora\app\synthesis.py` — the researcher / non_researcher prompts and
output shape. The mockup's register toggle (§5.5) must reflect what the app actually
does, not an idealised version.

---

## 5. Sections to build, in page order

### 5.1 Hero — "why this exists" *(highest priority; build this first)*

The most persuasive thing on the page, because it is real, dated, and from Blue Planet's
own document. Two panels side by side:

| Left panel — "Hva en generell modell skrev" | Right panel — "Hva artikkelen faktisk sier" |
|---|---|
| The v0.4 claim: the 2024 drop in returns was attributed to marine conditions | 2024 enters the model as a separate year factor. Theoretical smolt production and previous-generation catches were the dominant covariates — not lice, and not marine conditions as an explanation of 2024. |

Below both, in smaller type: the verified quote
«significant negative effect of year 2024… 1- exp(−0.45)=36% fewer returning salmon in
2024 compared to 2019», attributed to `2025_jae_jansen-lice-effects-returns` §3, plus:
*Caught 2026-07-07. Corrected in note v0.5 before the document was sent.*

Exact wording of both panels is in `litteratur_verifisering.md` lines 19 and 47, and the
recommended formulation on line 49. Use it; do not rewrite it.

Do **not** label the left panel "ChatGPT". It was Blue Planet's own draft. Label it
honestly — that is what makes it land.

### 5.2 Page header

Title, one-sentence problem statement, `Sist gjennomgått: [dato]`, and three chips:
`Vitenskap` · `Regulering` · `Omstridte punkter`.
Document count and year range read from the corpus (27 documents, 1997–2026).

**No question box above the fold.** This is the central design claim; do not undermine it.

### 5.3 Section C — the debate cards *(second priority)*

Five cards. Structure per card: title as a question, two opposing positions side by side,
the paper IDs, a curator caveat, and an "Ask about this" button.

Framing text comes from the **Expected disagreement** paragraphs in
`PRIORITY_QUESTIONS.md`. Position text comes from the verified quotes in §4.1 where
available.

| # | Card title (NO) | Papers | Q |
|---|---|---|---|
| 1 | Forsvinner lusa hvis oppdrettet forsvinner? | `2025_dao_jones-broughton-lice-unchanged`, `2025_jfd_jones-pacific-lice-cessation-bc`, `2025_scientificdata_bc-sealice-dataset-2001-2023` | Q1, Q9 |
| 2 | Er dødelighetsmodellen kalibrert på riktige data? | `2022_aei_stige-model-sensitivity-calibration`, `2024_raq_vannes-critical-review-tls`, `2025_raq_stige-comment-vannes`, `2025_raq_vannes-response-to-stige` | Q5, Q7, Q8, Q10 |
| 3 | Treffer modellene det som faktisk observeres? | `2021_icesjms_johnsen-vps-mortality-norway`, `2021_icesjms_jansen-comment-vps-mortality`, `2025_aquaculture_gjerde-seatrout-lice-prediction` | Q5, Q8, Q10 |
| 4 | Gir smoltdødelighet færre voksne tilbake? | `2025_jae_jansen-lice-effects-returns`, `2021_rfsa_dadswell-atlantic-salmon-collapse`, `2016_jfb_jonsson-environmental-change-salmon`, `2022_rfbf_gillson-marine-stressors-salmon` | Q9 |
| 5 | Holder laboratorieterskler i naturen? | `2020_conphys_fjelldal-lice-osmoregulation-salmon`, `2020_jae_bohn-timing-survival-postsmolts`, `2024_raq_vannes-critical-review-tls`, `2024_ecosphere_hawley-anadromy-lice-mortality-trout`, `1997_icesjms_dawson-seatrout-salmon-susceptibility` | Q6, Q7 |

All 19 `doc_id`s above were checked against the `documents/` folder listing on 2026-08-04
and every one exists. If one now fails to resolve, something moved — report it, per §9.1.

Cards 2, 3, 4 and 5 have verified quotes available in §4.1. **Card 1 does not** — the BC
papers are not covered there. Quote card 1 from `extracted.md` and mark it unverified per
§5.4. Do not quietly present it as equivalent.

Two caveats that must survive into the cards, because a domain expert will check for them:

- Card 1: transferability is contested. Different host species; *Caligus clemensi* is a
  major contributor in BC but not in Norway.
- Card 5: Hawley et al. is **sea trout**, not salmon. `litteratur_verifisering.md` line 127
  says so explicitly. Relevant as an analogue for variable exposure, not directly
  transferable.

The Stige/Van Nes exchange also contains conflict-of-interest arguments. Present the
scientific content only. Do not adjudicate.

### 5.4 Provenance interaction *(third priority; this is the payoff)*

Any claim carrying a quote gets a small marker. Clicking it expands inline to show:

- the exact quote
- the `doc_id` and section reference
- a verification state, rendered visibly and differently:
  - **`Verifisert mot kilde 2026-07-07`** — quote from §4.1
  - **`Uttrukket, ikke verifisert`** — quote from `extracted.md`

Showing both states is a feature, not an inconsistency. The distinction *is* the product.
Resist the urge to make every card look equally solid.

### 5.5 Section D — "Dig deeper", with a canned answer

Placed at the **bottom** of the page. A question box pre-fillable by the "Ask about this"
buttons, a register toggle (`Forsker` / `Ikke-forsker`), and **one** pre-written answer.

Wire the toggle to swap between two pre-written versions of the same answer. No API, no
generation — it is a canned demo and must be labelled `Eksempelsvar` so nobody mistakes it
for live output.

Use debate card 4 as the worked example (returns and population effect): it is the most
contested, has the most verified quotes, and is where a naive answer is most obviously
wrong. The answer must carry inline citation markers that expand per §5.4, and must state
that the evidence is contested rather than resolving it.

The five starter questions (which pre-fill the box):

1. Hva skjedde med lus på villaks etter at oppdrett ble fjernet i British Columbia, og er det overførbart til Norge?
2. Hva er det egentlig Van Nes et al. og Stige et al. er uenige om når det gjelder kalibrering?
3. Hvor godt treffer de operative lusemodellene det som faktisk måles på villfisk?
4. Gir luseindusert smoltdødelighet færre voksne tilbake, og hvordan står det mot andre dødsårsaker i havet?
5. Ved hvilke lusenivåer dør postsmolt faktisk, og hvor godt er den terskelen etablert?

### 5.6 Trust label legend

Visible on the page, not buried. Three labels, each visually distinct, and each applied to
the sections it governs:

| Label | Applies to | Claim to the reader |
|---|---|---|
| `Redaksjonell oversikt` | Orientation, framework | Written by the project; cites law and official reports |
| `Fra kuratert korpus` | Debate cards, uncertainty | Traceable to an included paper |
| `Syntetisert fra kilder` | The answer in §5.5 | Generated from the corpus only |

If these three blur, the result is a more authoritative-looking black box than the current
chat app. Make them unmistakable.

### 5.7 Disclosure block *(short, and not optional)*

Near the foot of the page. Plain, factual, no defensiveness:

- Jansen et al. 2025, in this corpus, is funded by PO3/4 Kunnskapsinkubator.
- Blue Planet's own analysis on this question is commissioned by the same body.
- Blue Planet has produced an evidence note for legal use on a related question.

Verify each of these against `metadata.yaml` and `Villlaks_analyse\STATUS.md` before
writing it. If a detail doesn't check out, leave it out rather than approximating.

### 5.8 Sections A, B and E — placeholder treatment

Do **not** write orientation prose or regulatory prose for this mockup. Render each as a
labelled, visibly unfinished block showing the intended structure:

- **Section A (Orientering):** five bullet slots with one-line descriptions of what each
  bullet will say. Content pending.
- **Section B (Gjeldende rammeverk):** the two verified facts from §4.4 rendered properly
  with their check date; the remaining six as `[må hentes fra Lovdata]` rows.
- **Section E (Hva ville endret bildet):** three slots, drawn from
  `main_uncertainty_sources` in the metadata if it is populated; otherwise placeholders.

This is deliberate. Showing Section B honestly half-empty, with a visible review date,
demonstrates the governance problem better than any explanation — and it sets up the one
question Ragnar actually needs to answer: who owns that review date.

---

## 6. Scope control

**Must ship (in this order):** §5.1 hero · §5.3 debate cards · §5.4 provenance ·
§5.6 trust labels · §5.2 header · §5.8 placeholders

**Ship if time allows:** §5.5 canned answer with register toggle · §5.7 disclosure

**Cut without hesitation:** charts, maps, any data visualisation, search, filtering,
multiple themes, mobile layout, dark mode, print styles, real retrieval.

If you are running short, cut §5.5 before cutting anything above it. A page with strong
orientation and no answer box still makes the argument. A page with a chat box and weak
debate cards makes the opposite one.

---

## 7. Language

Build the interface and editorial text in **Norwegian**. Ragnar is Norwegian and the
intended readers are Norwegian professionals and non-professionals.

Keep in English: paper titles, `doc_id`s, and all verbatim quotes. Do not translate a
quote — a translated quote is no longer a quote.

*Switch: if the reviewer prefers English throughout, only chrome and section headings
change. Content sources are English either way.*

---

## 8. Definition of done

- [ ] `mockup/tema-villaks.html` opens correctly in Chrome **with wifi off**
- [ ] Every factual sentence traces to a file in §4; nothing invented
- [ ] No regulatory claim beyond the two in §4.4; the rest visibly placeholders
- [ ] Both verification states appear and are visually distinct (§5.4)
- [ ] Card 1 marked unverified; card 5 marked as sea trout
- [ ] All five debate cards have real `doc_id`s, spelled exactly as in the corpus folder
- [ ] The hero panel uses the wording from `litteratur_verifisering.md`, not a rewrite
- [ ] Nothing under `app/` or `corpora/` was modified — confirm with `git status`
- [ ] File is self-contained; no external requests in the network tab
- [ ] A short `mockup/README.md`: what this is, what is fake, what to delete afterwards

Commit as `mockup: clickable theme page prototype for 2026-08-05 demo`. Do not push.

---

## 9. Open questions — ask, do not guess

1. If a `doc_id` in §5.3 doesn't match a folder under `documents/`, **stop and report it.**
   Do not substitute a similar one.
2. If `main_uncertainty_sources` is empty or inconsistent across documents, use
   placeholders in §5.8 and say so. Do not synthesise the field.
3. If a §4.1 quote cannot be found in the corresponding `extracted.md`, that is a real
   finding about the verification file. Report it; do not silently fall back.
