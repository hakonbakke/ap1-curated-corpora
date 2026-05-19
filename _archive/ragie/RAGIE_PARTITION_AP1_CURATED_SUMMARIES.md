# Ragie: partition `ap1-curated-summaries`

## Purpose

Separate **retrieval-optimised evidence summaries** from admin files and from dense YAML so curated retrieval competes fairly with the PDF partition.

## Automated upload (API)

From repo root `ap1-curated-corpora/`:

```powershell
# Paste the key exactly as Ragie shows it — no < > brackets around it.
$env:RAGIE_API_KEY = "tnt_..."
python scripts/upload_ap1_curated_summaries_to_ragie.py
```

Dry run (no API calls):

```powershell
python scripts/upload_ap1_curated_summaries_to_ragie.py --dry-run
```

The script POSTs each `*.summary.md` to `https://api.ragie.ai/documents` with `partition=ap1-curated-summaries`, `mode=fast`, and metadata (`layer`, `corpus`, `project`, `external_id`, `doc_type`).

**Replace vs duplicate:** Ragie **does not** overwrite by filename. The upload script **deletes** existing documents in `ap1-curated-summaries` whose `external_id` (or `.summary.md` name) matches the local bundle, then uploads again—so you keep **15 documents**, not 30. Use `python scripts/upload_ap1_curated_summaries_to_ragie.py --no-delete` only if you intentionally want duplicates.

## Create the partition (Ragie UI or API)

1. Create a new partition named exactly: **`ap1-curated-summaries`** (or rely on Ragie auto-creating it on first document upload to that partition name).
2. Upload **only** the files in:

   `corpora/salmon-lice-and-mortality-of-wild-salmonids/ragie_partition_ap1_curated_summaries/*.summary.md`

3. Do **not** upload into this partition: `README.md`, `PRIORITY_QUESTIONS.md`, `KEYWORDS.md`, `metadata_template.yaml`, `inclusion_log.md`, `00_FILE_INDEX.md`, or any `*.metadata.yaml`.

## Recommended document metadata (per uploaded file)

Set consistently when ingesting (names can match your existing AP1 convention):

| Field | Example |
|--------|---------|
| `layer` | `curated_summaries` |
| `corpus` | `salmon-lice-and-mortality-of-wild-salmonids` |
| `project` | `ap1` |
| `external_id` | `2025_jae_jansen-lice-effects-returns` (matches filename stem) |
| `doc_type` | `evidence_summary` |

Optional filters later: `priority_questions` (e.g. `$in: ["Q9","Q10"]`) if you add them as metadata on documents.

## Suggested retrieval settings (starting point)

- `partition`: `ap1-curated-summaries`
- `top_k`: 12–18
- `max_chunks_per_document`: 2–3
- `rerank`: `true`  
  If `scored_chunks` is often empty, retry with `rerank: false` for debugging.

## Dual-pass workflow (unchanged logic)

1. Retrieve from **`ap1-curated-summaries`**: claim map, disagreement, which studies matter.
2. Retrieve from **`ap1-pdf`**: quotes and numeric detail for grounding.
3. Synthesise with a template that forces support / opposition / uncertainty / confidence.

## Maintenance

When a document’s evidence changes in the corpus:

1. Update `documents/{id}/summary.md` if you keep a human-facing narrative version.
2. Regenerate or edit `ragie_partition_ap1_curated_summaries/{id}.summary.md` using `SUMMARY_GENERATION_INSTRUCTIONS.md`.
3. Re-ingest or replace the document in Ragie for that partition.
