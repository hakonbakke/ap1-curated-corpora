# Senior RAG Engineer — lessons for AP1

**Status:** Project standard · **Updated:** 2026-08-11  
**Source:** Industry job description (Senior RAG Engineer, Newcode.ai / Workable), adapted to Havbruksløftet AP1 curated corpora.  
**Agent persona:** `.cursor/rules/senior-rag-engineer.mdc`

This note translates production RAG expectations into **what AP1 should do**, without requiring a full rewrite to FastAPI/Qdrant tomorrow.

---

## The job in one sentence

Own the path from **query → correct passages → model context**, and prove with numbers that silent failures (fluent answer, wrong citation) are rare.

---

## Lessons → AP1 mapping

| Industry expectation | AP1 today | What “good” looks like here |
|----------------------|-----------|-----------------------------|
| End-to-end pipeline: parse → chunk → embed → index | Curate (`summary.md`, `metadata.yaml`) → `ingest.py` → `corpus.parquet` | Keep ingest honest; flag stale embeddings; no silent corpus drop |
| Pipeline stays current as material changes | Manual inclusion + sync scripts | Document “new paper → D live; A–C redactional refresh” (already the product contract) |
| FastAPI + background ingest/reindex | Streamlit ask path; scripts offline | Keep heavy embed/reindex **out of** the interactive path |
| Hybrid semantic + keyword (e.g. Qdrant) | Cosine on embeddings in parquet | Add BM25/hybrid **only if** `eval_retrieval` / golden set shows miss |
| Metadata filter + fuse + rerank | Routing + metadata fields exist | Use `priority_questions`, geography, controversy links before bigger infra |
| Agentic retrieval (decompose, tools, stop rules, budgets) | Single retrieve → synthesise | Optional later; cost/latency budget first; not default for board demo |
| Golden sets + retrieval metrics | Smoke queries, routing 5/5, recall script | Grow labelled golden set; trust recall@k / NDCG-style checks over anecdotes |
| Trace bad answer → chunk | Sources + doc ids in UI | Preserve source list; when debugging, name doc_id + field (`rag_summary` vs brief) |
| Multi-tenant isolation | One active corpus; more rooms planned | One evidensrom → one corpus; never mix embeddings across rooms by accident |
| Multilingual / morphology | NO + EN UI; Norwegian science terms | Test Norwegian queries in golden set; sparse/keyword plans must handle compounding |
| Don’t ship on 3 hand queries | Informal demos happen | Gate retrieval changes on eval scripts / saved `eval/recall_runs/` |
| Own boring maintenance | Sync, validate, vocabulary | Keep `validate_corpus.py` green; treat taxonomy drift as regression |

---

## Silent failure — AP1 definition

A failure that looks successful:

- Synthesis sounds balanced but **missed the opposing paper** that was in the corpus
- Citation / source list implies support the prose does not have
- “High confidence” after methodology-critique sources dominate
- Non-expert mode **smooths away** the disagreement the product exists to show

Mitigations already aligned with Honest Broker: debate map, evidence_direction, audience-mode caution, human inclusion. Strengthen with eval + tracing, not more model swagger.

---

## Evaluation standard (adopt)

Before changing retrieval or synthesis prompts in a material way:

1. **Golden / smoke set** — fixed queries; who labelled them; what “must retrieve” means  
2. **Metrics you trust** — at minimum recall@k / must_include hits; routing accuracy where relevant  
3. **Before/after numbers** — same script, saved artifact under `eval/`  
4. **Kill criterion** — if metrics drop or disagreement vanishes in prose, revert  

Existing hooks: `scripts/eval_routing.py`, `scripts/eval_retrieval.py`, `eval/benchmark_protocol_v2.md`.

---

## Stack reality check

| Stack item in the job ad | AP1 stance |
|--------------------------|------------|
| Python | Yes |
| FastAPI services | Optional later (Bluetalk / production); Streamlit OK for demo |
| Qdrant / vector DB ops | Optional at 27–100 docs; parquet is enough until eval fails |
| PostgreSQL / Redis | Not required for current scale |
| OCR-heavy ingest at scale | PDFs via extract pipeline; quality > volume |
| BM25 / NDCG / recall@k | Concepts yes; implement hybrid when evidence demands |

**Do not** rebuild to match the job ad’s stack for prestige. Rebuild when eval or multi-room ops force it.

---

## Priority order for this project

1. **Eval artifacts** — golden set 15; routing 15/15; recall baseline **15/15** in `eval/recall_runs/2026-08-11T123621Z_recall.json`  
2. **Traceability** — every demo answer explainable to doc_id + why retrieved  
3. **Non-expert mode risk** — validate simplified answers so nuance survives (human-in-the-loop)  
4. **Metadata-aware retrieval** — exploit fields you already curate before new infra  
5. **Hybrid / rerank / agentic** — only after (1) shows a clear miss pattern  
6. **Multi-room isolation** — when areal / welfare corpora leave stub state  

---

## What agents must not do

- Invent papers, legal facts, or consensus  
- Full re-embed “just in case”  
- Ship retrieval changes without a measurable check when scripts exist  
- Collapse contested evidence into a single clean narrative for either audience mode  
- Treat the HTML mockup and the live RAG as the same deployable without saying so  

---

## Related files

- Persona rule: `.cursor/rules/senior-rag-engineer.mdc`  
- Ideas backlog: `possible_improvements/rag-retrieval-synthesis.md`  
- Method: `METHOD.md`, `WORKFLOW.md`  
- Product mockup: `mockup/` (Havbruksløftets Evidensrom)  
