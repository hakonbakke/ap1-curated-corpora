# Golden set (retrieval quality)

**Purpose:** Fixed questions with `must_include_any` so retrieval changes are measured, not vibe-checked.  
**File:** `eval/smoke_queries.json`  
**Run:** `python scripts/eval_retrieval.py` → artifact in `eval/recall_runs/`  
**Routing (API-free):** `python scripts/eval_routing.py`

## Status

| Item | Value |
|------|--------|
| Cases | 15 (5 baseline + 10 fault-line / trap / NO TLS) |
| Label draft | Thord 2026-08-11 |
| Expert confirm | **Skipped** — Ragnar no capacity; treat as working baseline, revisit if retrieval changes fail |
| Routing | **15/15** (2026-08-11, API-free) |
| Baseline recall run | **15/15** — `eval/recall_runs/2026-08-11T123621Z_recall.json` (top_k=8) |

## Rules

1. Every case that asserts quality must have non-empty `must_include_any`.
2. Pass = at least one listed `doc_id` appears in top-k (default 8).
3. Do not ship retrieval/synthesis ranking changes without a new saved recall run.
4. Norwegian queries are first-class (morphology / phrasing).

## Expanding

Add cases aligned to Evidensrom fault lines or `PRIORITY_QUESTIONS.md` Q1–Q10.  
Keep ids stable once used in a baseline artifact.
