# Full-text enrichment

The curated summaries carry about 3 % of each full text. This folder holds what
`scripts/build_areal_enrichment.py` read from the full texts (`extracted.md`) so
the Areal room can use more of them without full passage search.

- `segments/<doc_id>.json`: raw model replies, one per segment of the full text
  (chapters where the extract has headings, about 50,000 characters each). Each
  segment has key figures, notes on all nine priority questions A0–A8 and, for the
  large reports, a chapter title and summary. Kept so a retag only needs
  `--reduce-only`.
- `data/area-enrichment.parquet` (built from these): one row per
  - `figure`: a verbatim quote with a number, its page where the extract has page
    markers, and an English statement of what it measures;
  - `chapter`: a summary of one chapter of a report of 290,000 characters or more,
    with its own embedding;
  - `pq_note`: what one document says about one of its A0–A8 tags, merged across
    segments.

Checks, all against `extracted.md`, not the PDF:
- a figure is kept only if its quote occurs in the full text (case, markdown,
  line breaks and hyphenation folded) and the statement's numbers occur in the quote;
- in notes and chapter summaries, a sentence with a number the full text does not
  contain is dropped. This catches invented or calculated numbers, not a real
  number attached to the wrong claim.

The notes follow the AI-assigned A0–A8 tags. After the tag review, update the tags
in `metadata.yaml` and run `python scripts/build_areal_enrichment.py --reduce-only`.
After a new or changed extract, run `--doc <doc_id>`.
