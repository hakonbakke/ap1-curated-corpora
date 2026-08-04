# Theme page mockup (2026-08-05 demo)

## What this is

A **single-file, offline HTML prototype** of one AP1 theme page
(*lakselus og dødelighet hos ville laksefisk*), built from `MOCKUP_BRIEF.md`.

Open in Chrome/Edge:

`mockup/tema-villaks.html`

No server, no CDN, no API. Test with wifi off.

## What is real

- Hero: caught error from note v0.4 → v0.5 (Jansen 2025 year factor), quoted from
  `Villlaks_analyse/docs/litteratur_verifisering.md`
- Debate cards with real `doc_id`s from the corpus
- Two verification states: verified 2026-07-07 vs extracted/unverified
- Two regulatory facts only (PO3/PO4), check date 2026-07-27
- Disclosure lines checked against STATUS / funding metadata

## What is fake / unfinished

- Sections A and most of B: deliberate placeholders (`[innhold mangler]` /
  `[må hentes fra Lovdata]`)
- Section D answer: **canned** `Eksempelsvar`, not live synthesis
- “Ask about this” only pre-fills the text box — no retrieval

## What to delete afterwards

- This folder, or promote the design into Streamlit and delete the mockup
- `MOCKUP_BRIEF.md` in repo root once the meeting is done (or move to `docs/`)

## Do not confuse with

The live Streamlit app under `app/` — intentionally untouched.
