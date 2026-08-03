# Possible improvements — AP1 curated corpora

**Purpose:** Parking lot for methods, architecture ideas, and experiments that *may* improve AP1. Nothing here is committed work — items can be implemented, deferred, or rejected.

**Not:** current project state (see [`STATUS.md`](../STATUS.md)) or normative methodology (see [`METHOD.md`](../METHOD.md)).

**Last captured:** 2026-08-03 (AI curation pipeline: human selects papers; AI curates + verifies).

---

## How to use this folder

| Status | Meaning |
|--------|---------|
| `idea` | Worth remembering; no decision |
| `consider` | Likely valuable; needs scoping |
| `next` | Recommended after current MVP milestones |
| `deferred` | Valid but wrong timing |
| `rejected` | Decided against (with reason) |

When an item ships, move a one-line note to `STATUS.md` and mark it `done` here or delete the row.

---

## Files

| File | Contents |
|------|----------|
| [`improvement-backlog.md`](improvement-backlog.md) | Master list with priority and status |
| [`architecture-hybrid-stack.md`](architecture-hybrid-stack.md) | Wiki + RAG + positioning vs FHF KI-formidler |
| [`rag-retrieval-synthesis.md`](rag-retrieval-synthesis.md) | Concrete RAG fixes from benchmark test |
| [`loops-harness-evaluation.md`](loops-harness-evaluation.md) | Agent loops, minimal harness, eval |
| [`forum-landscape-2026.md`](forum-landscape-2026.md) | Reddit/X/HN RAG alternatives — patterns, hype vs AP1 fit |
| [`ai-curation-pipeline.md`](ai-curation-pipeline.md) | Human=select; AI extract/curate/verify/ingest |
| [`baswe-gap-vs-ap1.md`](baswe-gap-vs-ap1.md) | BASWE 15 concepts vs AP1 — done / next / skip |

---

## Strategic summary (one paragraph)

AP1’s differentiator is **governed Honest Broker evidence** for contested science — not generic formidling. Finish and deploy the Streamlit MVP first; improve RAG surgically (question-type routing, synthesis rules, benchmark). Treat the **Obsidian LLM wiki** (`../Obsidian/` vault, sibling to `Koding/`) as an optional **L1 compile layer**, not a replacement for AP1. Use **solo agent loops** with hard caps for QA and smoke tests — not multi-agent platforms. See linked files for detail.
