# Corpus: Area and aquaculture

Norwegian room name: **Areal og havbruk**

Folder slug (English, used in paths and scripts): `area-and-aquaculture`

## Scope

What academic publications say about allocating coastal area to aquaculture:
environment, wild fish, other industries, capacity and regulation.

Priority questions are not fixed yet. They should be written before papers
are treated as a standing corpus.

## Where to put papers

Drop PDFs here (do not put them in the villaks corpus):

`corpora/area-and-aquaculture/documents/PDFs/`

Use the original filename for now. Stable `doc_id` folders
(`YYYY_journal_keyword`) come when a paper is included and extracted.

PDFs are gitignored. They stay local (OneDrive), not on GitHub.

## Ingest

Use the corpus flag. Do not ingest these PDFs into villaks.

```
python scripts/ingest.py --corpus area-and-aquaculture --doc <doc_id>
```

## Status

`39 documents in the draft corpus (33 from the 2026-09-13 SharePoint set, 6 added by Thord Håkon Bakke on 2026-09-15). Parquet: data/area-and-aquaculture.parquet. Do not ingest into villaks.`

Lesbar oversikt over hva settet handler om, uenighet og hull: `CORPUS_OVERVIEW.md`.
