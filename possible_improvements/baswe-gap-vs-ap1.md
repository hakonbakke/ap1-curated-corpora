# BASWE 15 RAG concepts — what remains for AP1

**Updated:** 2026-08-03  
Source: `BASWE-15-RAG-Concepts-Guide.pdf`

## Already in place (or just shipped)

| # | Concept | AP1 |
|---|---------|-----|
| 03 | Embeddings | `text-embedding-3-large` |
| 04 | Vector DB | Parquet + numpy (correct at 27 docs) |
| 05 | Similarity | Cosine |
| 06 | Top-k | UI slider |
| 08 | Metadata filtering / routing | `retrieve_routed()` Q7–Q10 |
| 12 | Small-to-big (partial) | Short retrieve text → longer `summary_text` in synthesis |
| 14 | Grounding & citations | Honest Broker prompts + confidence rules + DOI UI |
| 15 | Evaluation (partial) | Offline routing eval; full recall@k still needs runtime smoke in app |

## Worth implementing next (priority order)

| # | Concept | Why for AP1 | Needs OpenAI API? |
|---|---------|-------------|-------------------|
| **07** | Hybrid BM25 + vector | Best remaining quality jump for TLS/PIM/VPS exact terms | No for BM25; yes only to *test* live queries |
| **11** | Rerank (retrieve 20 → keep 8) | Improves order into the prompt | Yes (or local cross-encoder, no OpenAI) |
| **13** | Contextual embed prefix | Prepend title/year/Q-tags before embed at ingest | Yes (re-embed once) |
| **15** | Full recall@k on smoke set | Prove routing helped | Yes (embedding of smoke queries) |

## Skip / defer

| # | Concept | Reason |
|---|---------|--------|
| 01–02 | Chunking / overlap | Curated summaries already; revisit at 50+ papers |
| 09 | Query rewriting | Nice for NO↔EN; optional later |
| 10 | HyDE | Guide says specialist; hybrid first |
| 04 upgrade | Pinecone/pgvector | Overkill at current scale |

## Recommendation

Next engineering sprint after deploy: **hybrid BM25 (local) + optional local reranker**. Keep OpenAI key for app query/synthesis only.
