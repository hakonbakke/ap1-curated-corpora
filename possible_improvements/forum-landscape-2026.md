# Forum & industry landscape — RAG alternatives (2026)

**Status:** Reference / ideas · **Updated:** 2026-07-03  
**Sources:** Reddit-adjacent builder discourse (r/LocalLLaMA, r/Rag, r/LangChain), X/influencer narratives, HN, ACL 2026, production guides (Anthropic, NVIDIA, Weaviate). Synthesised from multi-agent research — not primary Reddit thread text.

**Takeaway for AP1:** Forums are not saying “drop RAG.” They say **naive vector-only RAG is obsolete**; mature stacks combine **hybrid retrieval, routing, governance, and optional compile layers**. AP1 already has governance (Honest Broker); gaps are mostly **retrieval depth and eval**.

---

## Meta-consensus (2025–2026)

| Claim in hype | What builders actually mean |
|---------------|----------------------------|
| “RAG is dead” | Chunk → embed → top-k → generate **without grading or rerank** is dead |
| “Context engineering” | Umbrella skill: what enters the context window (RAG is one **Select** mechanism) |
| “Agentic RAG” | Retrieval is a **tool** the agent may skip, repeat, or route — not a fixed pre-step |
| “Karpathy killed RAG” | **Overhyped** — LLM Wiki is compile-at-ingest for personal/small scale; hybrid with RAG is the pragmatic read |
| “Long context replaces RAG” | **Debunked** for enterprise: cost, context rot, stale data; hybrid “retrieve narrow → reason wide” wins |

**Pushback voices worth noting:** Hamel Husain (“Stop Saying RAG Is Dead”), Simon Willison (RAG ⊂ context engineering), Jerry Liu (“RAG 1.0 dead; document/context layer matters more”).

---

## Named patterns — what they are and AP1 fit

| Pattern | One-line description | AP1 fit | Suggested status |
|---------|---------------------|---------|------------------|
| **Production RAG 2.0** | Hybrid BM25+dense → RRF → cross-encoder rerank → grounded gen | Gap: embedding-only today | `consider` if smoke tests fail |
| **Contextual retrieval** | Prepend chunk context before embed (Anthropic) | Doc-level summaries partly do this | `idea` at ingest |
| **Adaptive RAG** | Router: simple path vs agentic path by query complexity | Maps to question-type routing (Q9 vs Q10) | `consider` — see P1-1 |
| **Agentic RAG lite** | retrieve → grade coverage → re-retrieve (cap 2 rounds) | Fixes Jansen-2025-in-list-not-prose | `consider` — see P2-1 |
| **CRAG** | Grade docs; rewrite query or fallback if weak | Optional after first retrieve fails QA | `deferred` |
| **Self-RAG** | Reflection tokens (retrieve? relevant? supported?) | High latency/cost for 27-doc corpus | `deferred` |
| **GraphRAG** | Entity graph + community summaries | YAML debate links ≈ light graph; full GraphRAG costly | `deferred` |
| **PageIndex / vectorless** | LLM navigates doc tree, no embeddings | Per-PDF niche; AP1 is multi-doc corpus | `rejected` for corpus RAG |
| **Karpathy LLM Wiki** | Compile at ingest → markdown wiki | **Obsidian vault** — external L1 | `deferred` link only |
| **CAG / KV cache** | Stuff static corpus in context | 27 papers changing; wrong model | `rejected` |
| **Context engineering** | Write / Select / Compress / Isolate | Two-tier `rag_summary` + `summary.md` | **partially done** |
| **Governance before generation** | Control which sources may influence output | Honest Broker + evidence_direction | **core differentiator** |
| **MCP-wrapped retrieval** | RAG exposed as agent tool via MCP | Future harness; not needed for Streamlit demo | `deferred` |
| **Harness engineering** | Agent = model + tools + guardrails + memory | Cursor + STATUS + loops = minimal harness | `idea` |
| **Retrieval–generation gap** | Relevant chunks ≠ useful reasoning context | Explains benchmark “retrieved but not used” | Informs synthesis prompts |

---

## Production reference stack (2026 forum consensus)

Not a mandate — a pattern map for where AP1 could grow:

```
Query
  └─► Router (question type / complexity)
        ├─► Hybrid BM25 + vector + rerank     [AP1: vector only today]
        ├─► Metadata filter (priority_questions) [AP1: partial]
        ├─► Agentic second pass (optional)     [AP1: not yet]
        └─► Pre-authored synthesis/ (demo)     [AP1: empty folder]
  └─► Context builder (dedupe, cite, budget)
  └─► Generator (Honest Broker prompts)        [AP1: yes]
  └─► Verifiers (confidence vs 🔵 sources)     [AP1: gap]
  └─► Governance (curator status, inclusion)   [AP1: yes, pending QA]
  └─► Eval (RAGAS / smoke protocol)            [AP1: manual only]
```

---

## What forums say fails in vanilla RAG

Useful checklist when debugging AP1 retrieval:

1. **Similarity ≠ relevance** — embeddings miss exact terms (TLS, PIM, VPS).
2. **Single-pass retrieval** — no retry for multi-hop or under-specified queries.
3. **Chunking destroys structure** — AP1 mitigates via **doc-level** bundles (not arbitrary chunks).
4. **No verification loop** — confident wrong answers with citations.
5. **Silent retrieval failure** — wrong docs in → plausible answer out.
6. **Retrieval–generation gap** — good retrieve, poor use in prose (observed in FHF benchmark).

---

## Hype vs defer for AP1 specifically

| Trend | Forum hype level | AP1 action |
|-------|------------------|------------|
| Hybrid + rerank | High adoption | Measure first; add if smoke tests fail |
| Agentic RAG | High | Lite version (2-pass + coverage check) only |
| GraphRAG | Medium, mixed results | Defer — use metadata graph |
| PageIndex | High GitHub, niche use | Defer |
| LLM Wiki | Viral Apr 2026 | Obsidian already; link don’t rebuild |
| Full agent orchestrator | High hype | Rejected — solo loops enough |
| RAGAS in CI | Rising standard | Consider after smoke protocol exists |

---

## Key external references

| Topic | Link |
|-------|------|
| Karpathy LLM Wiki gist | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f |
| Anthropic contextual retrieval | https://www.anthropic.com/engineering/contextual-retrieval |
| Agentic RAG 2.0 overview | https://www.agentvsai.com/agentic-rag-2-0-graphrag-tool-routing-context-engineering/ |
| ACL 2026 retrieval–generation gap (R2U) | https://aclanthology.org/2026.findings-acl.1513/ |
| GraphRAG-Bench (when graphs help / hurt) | https://github.com/GraphRAG-Bench/GraphRAG-Benchmark |
| RAG Radar (Reddit signal summary, May 2026) | https://medium.com/@ebysslabs_23/rag-radar-weekly-signals-013262685143 |
| Simon Willison on context engineering | https://simonwillison.net/ (Jun 2025 posts) |

---

## Related AP1 docs

- [`improvement-backlog.md`](improvement-backlog.md) — prioritised items derived from this landscape
- [`rag-retrieval-synthesis.md`](rag-retrieval-synthesis.md) — concrete fixes from FHF vs AP1 test
- [`architecture-hybrid-stack.md`](architecture-hybrid-stack.md) — L1 wiki + L2 RAG positioning
