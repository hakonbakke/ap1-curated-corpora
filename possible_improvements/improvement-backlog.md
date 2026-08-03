# Improvement backlog

Priorities are relative to **current phase:** deployable AP1 demo + curator QA on TLS core set.

| ID | Item | Priority | Status | Effort | Notes |
|----|------|----------|--------|--------|-------|
| P0-1 | Streamlit Cloud deploy | P0 | done | Low | Deployed and shared with Ragnar; confirm still live + document URL |
| P0-2 | Expert QA on TLS core | P0 | rejected | — | No expert field-by-field QA capacity exists or is expected; available expert capacity is paper selection only. AI verify + offline accept is the trust model. |
| P0-2b | AI curation pipeline (add_paper / curate / verify) | P0 | done | Medium | See `ai-curation-pipeline.md`; human=select only |
| P0-2c | Backfill verify + offline accept all 27 | P0 | done | Low | 27/27 `ai_verified`; parquet sync without re-embed |
| P0-3 | RAG smoke-test protocol (EN/NO, 4 queries) | P0 | idea | Low | Document pass/fail; see `rag-retrieval-synthesis.md` |
| P1-1 | Question-type routing (population vs smolt vs TLS) | P1 | done | Medium | `retrieve_routed()` in `app/retrieval.py`; wired in `app.py` |
| P1-2 | Synthesis: no “high confidence” when 🔵 critique is central | P1 | done | Low | `confidence_guidance()` in `app/synthesis.py` |
| P0-3b | Offline routing smoke eval | P0 | done | Low | `scripts/eval_routing.py` + `eval/smoke_queries.json` (no API) |
| P1-3 | Pre-authored `synthesis/` for Q9, Q10 | P1 | idea | Medium | Human/AI drafts for demo stability |
| P1-4 | Extend benchmark: AP1 vs FHF KI-formidler vs ChatGPT | P1 | idea | Medium | Same question set; `_archive/benchmark/` |
| P1-5 | Solo loop: curator QA with maker-checker | P1 | idea | Low | Cursor `/goal`; see `loops-harness-evaluation.md` |
| P2-1 | Agentic retrieval lite (second pass if Q9 under-represented) | P2 | idea | Medium | Loop: retrieve → check coverage → re-retrieve |
| P2-2 | Link Obsidian wiki ↔ AP1 (export summaries, Q1–Q10 pages) | P2 | deferred | Medium | Wiki vault at `Obsidian/`; avoid duplicating `LLM_wiki/` |
| P2-3 | CLI `scripts/query_corpus.py` + Cursor skill | P2 | idea | Low | Minimal harness; no MCP yet |
| P2-4 | Hybrid retrieval (BM25 + embeddings + RRF) | P2 | consider | Medium | 2026 production default per forums; AP1 is vector-only — see `forum-landscape-2026.md` |
| P2-5 | Cross-encoder rerank after hybrid retrieve | P2 | deferred | Medium | Often paired with P2-4; e.g. Cohere / BGE / local cross-encoder |
| P2-6 | Adaptive router (simple vs agentic path by query) | P2 | idea | Medium | Forum pattern; overlaps P1-1 question-type routing |
| P2-7 | CRAG grader (rewrite / second retrieve if weak) | P2 | deferred | Medium | After agentic lite; avoid web fallback for AP1 |
| P2-8 | RAGAS metrics + CI smoke gate | P2 | idea | Low–Med | Faithfulness / context precision on 4-query set |
| P2-9 | Contextual retrieval at ingest (chunk context in embed text) | P2 | idea | Low | Anthropic pattern; may overlap `rag_summary` quality |
| P2-10 | GraphRAG / Microsoft GraphRAG | P2 | deferred | High | ICLR 2026: mixed vs vanilla RAG; YAML debate links enough |
| P2-11 | PageIndex / vectorless doc navigation | P2 | rejected | — | Single-doc niche; wrong fit for 27-paper corpus |
| P2-12 | CAG / long-context stuff entire corpus | P2 | rejected | — | Cost + rot; corpus evolves |
| P2-13 | MCP-wrapped corpus query tool | P2 | deferred | Low | Post-demo harness; see `loops-harness-evaluation.md` |
| — | Full multi-agent orchestrator | — | rejected | High | Loop hype; solo loop + verification sufficient |
| — | Rebuild knowledge in `Koding/LLM_wiki/` | — | rejected | — | Superseded by Obsidian vault (68 wiki articles, 223 raw) |

---

## Done (move rows here when shipped)

| ID | Item | Completed |
|----|------|-----------|
| P0-2b | AI curation pipeline scripts + docs | 2026-08-03 |
