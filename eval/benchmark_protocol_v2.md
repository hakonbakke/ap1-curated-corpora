# AP1 Pilot Benchmark Protocol v2.0

Retargeted from `_archive/benchmark/benchmark_protocol_v1.md` (2026-08).
Scoring rubric and user-group design are unchanged. Systems and questions are
updated for the live Streamlit app and the 27-paper corpus.

## Purpose

Test whether curated RAG delivers better decision-support than generic AI on
contested salmon lice questions — especially debate chains this corpus uniquely
holds — across different user expertise levels.

The project success bar is: **must produce more value than a general LLM**.
That claim has not yet been measured. This protocol is the instrument.

## Systems under test

### Baseline A: Frontier chat model with web search

- Current frontier chat model **with web search enabled**
- No corpus upload; query asked as written
- Testing against a search-disabled model would be a straw man

### Baseline B: NotebookLM (raw PDFs)

- Upload all **27** PDFs from
  `corpora/salmon-lice-and-mortality-of-wild-salmonids/documents/PDFs/`
  (v1 said 15 — corpus has grown)
- Same query as written
- Standard NotebookLM interface

### Treatment: Streamlit curated RAG (`app/app.py`)

Record for each run:

| Setting | Values to log |
|---|---|
| `top_k` | e.g. 8 |
| `mode` | `researcher` / `non_researcher` |
| `answer_format` | `structured` / `freeform` |

Run the treatment in **both modes**; dual-register capability is part of what
is being tested. Ragie is retired — do not use it.

## Question set

Broad questions favour a frontier model with search. Test the differentiator:
debate chains and contested TLS evidence this corpus uniquely holds.

| # | Question | Why it discriminates |
|---|---|---|
| B1 | What precisely do Van Nes et al. (2024) and Stige et al. (2025) disagree about regarding TLS calibration and lice mortality thresholds, and what evidence would resolve it? | Corpus holds all three papers in the exchange. A general model will hedge or invent specifics. |
| B2 | How well do the Norwegian TLS lice models predict observed post-smolt mortality, and what do the validation studies show? | Requires Johnsen 2021, Jansen & Gjerde comment, and Gjerde 2025 on PMLD predictive failure. |
| B3 | What happened to sea lice on wild Pacific salmon after farms were removed from the Broughton Archipelago, and what does that imply for farm-attribution models? | Two 2025 Jones papers — recent and low-profile. Strong hallucination bait. |
| B4 | Does lice-induced smolt mortality translate into reduced adult returns, and how does it compare with other marine mortality drivers? | Requires holding Jansen 2025 against Dadswell 2021, Jonsson 2016, Gillson 2022 without collapsing them. |
| **C1** | **What is the life cycle of *Lepeophtheirus salmonis*?** | **Deliberate control. Textbook material; the general model should win or tie.** |

C1 is required. A benchmark that only asks questions you expect to win is
marketing. Reporting a loss on C1 alongside wins on B1–B4 is what makes the
result credible — and sharpens the real claim: better on contested questions,
not better in general.

## Scoring rubric (unchanged from v1)

Each response scored 1–3 on four dimensions:

### 1. Traceability
- **3:** Every major claim linked to specific document + section/page; citations accurate
- **2:** Most claims have citations; some general or imprecise
- **1:** Few/no specific citations; claims not verifiable

### 2. Disagreement Surfacing
- **3:** Explicit conflicting findings between named researchers/studies; both sides
- **2:** Some disagreement acknowledged without clear sources/nature
- **1:** Consensus view or ignores disagreements

### 3. Uncertainty Handling
- **3:** Distinguishes known / unknown / contested; flags method limits and implications
- **2:** Some uncertainty; not systematic
- **1:** Overstates certainty

### 4. Decision Usefulness
- **3:** Structured for decision-making; clear implications and confidence
- **2:** Relevant but needs extra interpretation
- **1:** Academic summary disconnected from decisions

### Hallucination check (new in v2)

For every citation a system produces: verify the cited paper exists **and**
says what is claimed. Fabricated or misattributed citations are a hard fail
for that response on Traceability (score 1), regardless of prose quality.

## Capture and score

For each question × system, save verbatim output to:

`eval/benchmark_runs/YYYY-MM-DD_<system>_<question_id>.md`

with configuration in a YAML/header block (`top_k`, `mode`, `answer_format`,
model name for baselines).

Record scores in `eval/benchmark_runs/scores.csv` with columns:

`date,system,question_id,mode,traceability,disagreement,uncertainty,decision_usefulness,hallucination_fail,notes`

## User group testing (unchanged from v1)

Groups: domain experts; policy/regulatory; industry practitioners; students/novices.

Blind A/B/C presentation; rate usefulness / trustworthiness / clarity (1–5);
prefer-which-system; short interview.

## Success criteria

**Technical:** Treatment scores higher than both baselines on ≥3/4 rubric
dimensions for B1–B4 (C1 may lose — that is informative, not a failure of the
protocol).

**User:** Treatment preferred by majority in ≥3/4 user groups.

**Differentiation:** Preference patterns differ by user group.

## Cost note

Treatment arm calls OpenAI for query embedding + synthesis. Five questions ×
two modes ≈ ten synthesis calls — small, but confirm before running. Baselines
A/B are external UIs (no project API key). Retrieval-only smoke:
`python scripts/eval_retrieval.py` (~5 embedding calls).

## Status

Protocol ready. Capture/score runs **not** executed in the 2026-08 maintenance
pass (API budget reserved for RAG runtime for testers).
