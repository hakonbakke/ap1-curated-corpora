# AP1 Pilot Benchmark Protocol v1.0

## Purpose
Test whether curated RAG delivers better decision-support than generic AI on contested salmon lice questions, across different user expertise levels.

## Test Questions

### Q9: Population-level impact of lice-induced mortality
**Query:** "Even where lice increase individual smolt mortality, does this translate to reduced adult returns and impaired population viability? How does lice-induced mortality compare to other sources of marine mortality?"

**Why this question:** 
- Genuinely contested in the literature (Stige vs. Van Nes camps)
- Generic AI will likely give oversimplified "lice harm populations" answer
- Requires distinguishing additive vs. compensatory mortality
- Critical for Traffic Light System justification

### Q10: Robustness of the Norwegian Traffic Light System
**Query:** "How robust is the Norwegian Traffic Light System as a regulatory framework? How sensitive are its classifications to model assumptions, calibration data, and monitoring design?"

**Why this question:**
- Central regulatory controversy in your corpus
- Generic AI lacks access to recent Stige/Van Nes/Jansen exchanges
- Requires nuanced treatment of model uncertainty
- Different user groups need this for different decisions

### Q7: Dose-response relationships (backup)
**Query:** "How can infestation levels observed on wild fish be translated into mortality estimates, and how robust are the dose–response relationships used for this?"

**Why this question:**
- Mechanistic core of the mortality models
- Heavy methodological disagreement in corpus
- Generic AI will miss the calibration data limitations

## Systems Under Test

### Baseline A: ChatGPT-4
- Standard ChatGPT interface
- No additional context provided
- Query asked directly as written above

### Baseline B: NotebookLM (raw PDFs)
- Upload all 15 PDFs from Publications_selected
- Same query as above
- Standard NotebookLM interface

### Treatment: Curated RAG (Ragie.ai)
- Dual-pass retrieval: **`ap1-curated-summaries`** (retrieval-optimised `*.summary.md` only; see `corpora/salmon-lice-and-mortality-of-wild-salmonids/RAGIE_PARTITION_AP1_CURATED_SUMMARIES.md`) + **`ap1-pdf`**
- Structured synthesis prompt (see below)
- Suggested retrieval: `top_k` 12–18, `max_chunks_per_document` 2–3, `rerank` on (fallback off if empty chunks)

## Ragie Synthesis Prompt Template

```
You are an evidence synthesis assistant for contested scientific questions. 

Query: [INSERT QUESTION]

Based on the retrieved evidence, provide a structured response with these sections:

## Main Finding
[2-3 sentences summarizing the current state of evidence]

## Supporting Evidence
[What evidence supports the main finding, with specific citations]

## Opposing/Qualifying Evidence  
[What evidence challenges or qualifies the main finding, with specific citations]

## Key Uncertainties
[What remains unknown or contested, with specific citations to disagreements]

## Context Dependencies
[How findings vary by geography, methodology, time period, etc.]

## Confidence Assessment
[Your confidence in the main finding: High/Medium/Low and why]

## What Could Change This Assessment
[What new evidence or analysis would significantly alter the conclusion]

Requirements:
- Every claim must link to a specific document and page/section
- Highlight explicit disagreements between named researchers
- Distinguish between absence of evidence and evidence of absence
- Flag methodological limitations that affect interpretation
```

## Scoring Rubric

Each response scored 1-3 on four dimensions:

### 1. Traceability
- **3 (High):** Every major claim linked to specific document + section/page. Citations accurate and verifiable.
- **2 (Medium):** Most claims have citations, some are general or imprecise.
- **1 (Low):** Few or no specific citations. Claims cannot be verified.

### 2. Disagreement Surfacing
- **3 (High):** Explicitly identifies conflicting findings between named researchers/studies. Shows both sides of contested issues.
- **2 (Medium):** Acknowledges some disagreement but doesn't clearly identify sources or nature of conflicts.
- **1 (Low):** Presents consensus view or ignores disagreements entirely.

### 3. Uncertainty Handling
- **3 (High):** Clearly distinguishes what is known, unknown, and contested. Flags methodological limitations and their implications.
- **2 (Medium):** Acknowledges some uncertainty but doesn't systematically identify sources or implications.
- **1 (Low):** Presents findings as more certain than evidence supports.

### 4. Decision Usefulness
- **3 (High):** Provides information structured for decision-making. Clear about implications and confidence levels.
- **2 (Medium):** Relevant information but requires additional interpretation for decision use.
- **1 (Low):** Academic summary that doesn't connect to decision needs.

## User Group Testing

### Groups
1. **Domain experts** (AP1 members, lice researchers)
2. **Policy/regulatory** (government, management consultants)  
3. **Industry practitioners** (aquaculture operations, consultants)
4. **Students/novices** (graduate students, new professionals)

### User Testing Protocol
1. Each group receives outputs from all three systems (anonymized as System A, B, C)
2. Users rate each output on:
   - **Usefulness for my role** (1-5 scale)
   - **Trustworthiness** (1-5 scale) 
   - **Clarity** (1-5 scale)
3. Users identify which system they would prefer for future queries
4. Brief interview: What did you find most/least helpful about each response?

## Success Criteria

**Technical validation:** Curated RAG scores higher than both baselines on at least 3/4 rubric dimensions for both test questions.

**User validation:** Curated RAG preferred by majority in at least 3/4 user groups.

**Differentiation:** Different user groups show different patterns of preference/usage, demonstrating system serves multiple needs.

## Output Documentation

For each test run, capture:
- Full query and response from each system
- Timestamp and system configuration
- Rubric scores with brief justification
- User group ratings and comments
- Any system failures or errors

## Next Steps After Benchmark

If successful:
1. Expand to remaining priority questions (Q1, Q4, Q5)
2. Test on second theme corpus
3. Develop user interface for AP1 group access

If mixed results:
1. Analyze failure modes by rubric dimension
2. Adjust Ragie configuration or prompt design
3. Re-test with improved setup

If unsuccessful:
1. Document lessons learned
2. Assess whether corpus needs expansion
3. Consider alternative RAG architectures