# Loops, harness, and evaluation

**Status:** Ideas · **Updated:** 2026-07-03  
**Cross-ref:** `AI_R&D/01_Knowledge_Base/Techniques/2026-06-20_loop-engineering.md`

---

## What “loops” are (and are not)

**Loop** = trigger → act → observe → repeat until **objective stop condition** + **hard cap**.

| Is | Is not |
|----|--------|
| Process for finishing work | A replacement for wiki or RAG |
| Solo agent in Cursor with verification | 24/7 multi-agent fleet (hype) |
| Maker-checker for curator QA | “Loop until satisfied” (token burn) |

**Key insight (Nate Herk):** verification beats architecture. One loop with a good done-check beats five agents without criteria.

---

## Recommended loops for AP1

### 1. Curator QA (maker-checker)

| Field | Value |
|-------|-------|
| Goal | N papers moved `pending` → `approved` (TLS core set) |
| Builder | Agent drafts/checks YAML against extract |
| Checker | Human expert (or rubric: required fields, evidence_direction justified) |
| Verify | `ingest.py` run; paper appears correctly in app |
| Cap | N papers per session (e.g. 5) |

### 2. RAG smoke test (solo loop)

| Field | Value |
|-------|-------|
| Goal | 4/4 smoke queries pass criteria in `rag-retrieval-synthesis.md` |
| Act | Adjust retrieval weights or synthesis prompt |
| Verify | Re-run queries; checklist |
| Cap | 3 iteration cycles |

### 3. Obsidian COMPILE (external vault)

| Field | Value |
|-------|-------|
| Goal | New AP1 summaries reflected in wiki concept pages |
| Trigger | After corpus batch ingest |
| Verify | `prompts/COMPILE.md` lint; `log.md` entry |
| Cap | 1 compile batch |

---

## Minimal harness (no new platform)

```
Cursor (agent)
  ├── read STATUS.md, possible_improvements/
  ├── skill (optional): “Query AP1 corpus”
  ├── tool: python scripts/query_corpus.py "..."   [not built yet]
  └── Streamlit for human demo
```

**Deferred:** MCP server, ngrok/tunnel (use Streamlit Cloud for demo), full orchestrator.

**MCP note (from AI_R&D feeds):** MCP’s main win may be auth outside context window — only needed when integrating external APIs at scale.

---

## Evaluation and production patterns (community 2026)

From RAG production discourse (not all applicable at AP1 scale):

| Pattern | AP1 fit |
|---------|---------|
| Hybrid BM25 + vector | Consider if embedding-only misses exact terms (TLS, PIM, VPS) |
| Reranker (cross-encoder) | P2 — adds latency/complexity |
| Citation verification post-gen | P1 — check cited doc_ids ⊆ retrieved set |
| Retrieval observability | Log top-k + scores per query in dev mode |
| Governance before generation | Already aligned with Honest Broker; strengthen rules |

---

## Scale-up path (only after solo loops work)

1. Solo loop (QA, smoke test) ✓ start here  
2. Maker-checker (curator + agent)  
3. Agentic retrieval lite (second pass)  
4. Manager + helpers (e.g. Bluetalk batch transcription) — **not AP1 priority**

---

## Example `/goal` prompt (RAG smoke test)

```
Goal: All 4 AP1 smoke-test queries in possible_improvements/rag-retrieval-synthesis.md pass their draft criteria.

Verify: Run each query via app or query_corpus CLI; record pass/fail in a table; fail if any criterion unmet.

Constraints: Max 3 edit cycles on retrieval.py and synthesis.py. Do not change metadata.yaml content.

When done: Update STATUS.md if any fix shipped; note results in possible_improvements/improvement-backlog.md.
```
