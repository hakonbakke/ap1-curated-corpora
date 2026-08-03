# RAG, retrieval, and synthesis improvements

**Status:** Ideas from benchmark · **Updated:** 2026-07-03

Concrete fixes identified when comparing AP1 to FHF KI-formidler on the same question. None implemented unless noted in `STATUS.md`.

---

## Current AP1 pipeline (baseline)

```
metadata.yaml + summary.md (+ rag_summary, key_claims)
        ↓
scripts/ingest.py → data/corpus.parquet (embeddings)
        ↓
retrieval.py: cosine similarity on rag_summary + key_claims
        ↓
synthesis.py: GPT-4o, Honest Broker prompts, two-tier context (rag vs full summary)
```

---

## Observed gaps

### Retrieval

| Gap | Example | Possible fix |
|-----|---------|--------------|
| Question type not routed | “Bestandsnedgang” → smolt/model papers dominate | Detect Q9/Q10 keywords; boost `priority_questions` containing Q9; metadata pre-filter |
| Key paper retrieved but not ranked for synthesis | Jansen 2025 in source list, weak in prose | Pass `priority_questions` match score to synthesis ordering; cap with “must cite if Q9” |
| Counter-evidence missing | Jones 2025 BC, Dadswell 2021 not in top-k | Ensure in corpus (✓); boost for attribution/population queries; or agentic second pass |
| Calibration debate missing when models discussed | Stige 2022 not retrieved | Link via `related_documents` or Q8 boost when query mentions VPS/TLS/calibration |

### Synthesis

| Gap | Possible fix |
|-----|--------------|
| “High confidence” after 🔵 sources | Rule: if central sources include `critiques_methodology` or debate map edges, forbid unified high-confidence closing; use Honest Broker closure template |
| Smolt mortality (Q7–Q8) swamps population (Q9) | Prompt: when query mentions “bestand/population”, require Q9 sources in body paragraphs |
| Paper-by-paper listing | Already improved (freeform thematic); keep monitoring |

### Governance (pre-generation)

| Concept | AP1 today | Improvement |
|---------|-----------|-------------|
| Source allow-list | Implicit via top-k | Explicit: min 1 🔵 when query is “how robust / disagree” |
| Citation trace | DOI in UI | Add source → claim mapping in structured mode |
| Curator gate | All `pending` | Approved subset for “official demo” mode (optional UI toggle) |

---

## Agentic RAG lite (optional)

Single-agent loop — not a new platform:

```
1. Retrieve top-k
2. Check: does set include required question coverage? (Q9 papers for population query)
3. If no → second retrieve with metadata filter
4. Synthesize
5. Verify: closing confidence matches evidence_direction mix (rule-based or small LLM check)
```

Stop after 2 retrieval rounds (hard cap).

---

## Context engineering (already partial)

Industry term (2025–2026): curating what enters the model — RAG is one **Select** mechanism, not the whole system. See [`forum-landscape-2026.md`](forum-landscape-2026.md).

| Layer | AP1 field | Role |
|-------|-----------|------|
| Retrieval | `rag_summary`, `key_claims` | Small, embedding-optimised |
| Generation | `summary_text` (~5k cap) | Full evidence brief |
| Governance | `evidence_direction`, `consensus_signal`, debate metadata | Honest Broker |

**Idea:** Document this two-tier model in `METHOD.md` as intentional “context engineering” when stable.

### Forum-suggested upgrades (not implemented)

| Pattern | AP1 relevance |
|---------|---------------|
| Hybrid BM25 + vector + RRF | Better exact-term hits (TLS, PIM, author names) |
| Cross-encoder rerank | Top-20 → top-5 before synthesis |
| Contextual retrieval at ingest | Richer embed text than bare `rag_summary` |
| Retrieval–generation gap | Fix synthesis under-use of retrieved docs (Jansen 2025 case) |

---

## Smoke-test queries (repeatable)

Use after any retrieval/synthesis change:

1. *How robust is the Norwegian Traffic Light System?* (Q10, debate chain)
2. *What evidence links lice-induced mortality to reduced adult returns?* (Q9, Jansen 2025)
3. *Which studies disagree most on lice impact magnitude?* (debate map)
4. *Hva er evidensen for at lakselus fra oppdrett gir bestandsnedgang hos villaks?* (NO, population + counter-evidence)

**Pass criteria (draft):**

- Q9 query cites ≥1 population-level study in synthesis body (not only source list).
- Q10 query cites Van Nes and Stige chain or equivalent.
- No “high confidence” if ≥2 central 🔵/🔴 sources.
- EN and NO both run without error.

---

## Benchmark extension

Add **FHF KI-formidler** as baseline C in `_archive/benchmark/benchmark_protocol_v1.md`:

- Same 4 queries
- Score: source relevance, debate visibility, population vs smolt focus, false closure
- Manual run (no API access to Allegro backend)
