You are reviewing an existing project called **Havbruksløftets Evidensrom**, contained in this repository.

Your first task is NOT to change the code.

Your first task is to understand what this project is fundamentally trying to achieve.

The repository has been developed iteratively, and you should expect to find traces of experimentation, abandoned ideas, temporary decisions, revisions, workarounds, and the owner changing direction over time.

Do not assume that every statement in `STATUS.md`, every existing implementation choice, every old comment, or every historical design decision represents the final product intent.

Instead, distinguish between:

1. **Durable product objectives**
2. **Durable methodological principles**
3. **Current implementation**
4. **Temporary or pragmatic decisions**
5. **Historical experiments / superseded approaches**
6. **Open questions and unfinished work**

Your job is to reconstruct the project's underlying intent first, and then evaluate whether the current implementation serves that intent well.

---

# 1. UNDERSTAND THE PROJECT BEFORE AUDITING IT

Start by reading the repository broadly.

At minimum inspect:

- `STATUS.md`
- `README.md`
- `SENIOR_RAG_ENGINEER.md`
- `.cursor/rules/senior-rag-engineer.mdc`
- relevant architecture/workflow documentation
- corpus structure and schemas
- retrieval implementation
- synthesis implementation
- evaluation code and evaluation datasets
- Streamlit application
- both existing evidensrom
- deployment/configuration
- recent Git history if available and useful

Also inspect the actual code rather than relying only on documentation.

The documentation may contain historical residue.

Where documentation and implementation differ, investigate why rather than automatically deciding that one is correct.

---

# 2. RECONSTRUCT THE MAIN OBJECTIVES

Before performing a technical audit, give me your interpretation of the project's main objectives.

Separate them into:

## A. Product objective

What is Havbruksløftets Evidensrom fundamentally supposed to be?

Who is it for?

What user problem is it solving?

What should a user be able to understand or do after using it?

## B. Evidence / epistemic objective

How is this different from a normal RAG chatbot?

What does the project mean by an Honest Broker approach?

How should scientific disagreement, uncertainty, evidence quality, provenance and competing interpretations be represented?

## C. Technical objective

What does the technical system need to do reliably to support the product?

For example:

- curate bounded corpora
- preserve provenance
- retrieve relevant evidence
- expose disagreements
- synthesise without smoothing disagreements away
- provide transparent sources
- support multiple evidensrom
- evaluate retrieval and synthesis systematically

But infer these from the repository rather than blindly adopting this list.

## D. Scalability objective

Determine whether this is intended to remain two bespoke rooms or become a reusable platform for multiple evidence rooms.

Look for evidence in the repository.

## E. Current short-term objective

Identify what appears to matter immediately, such as:

- demo readiness
- deployment
- stability
- quality of the area room
- source presentation

Distinguish short-term delivery needs from long-term architecture.

---

# 3. IDENTIFY HISTORICAL NOISE

The project has evolved through experimentation.

Actively identify places where the repository shows evidence of the owner going back and forth.

Examples might include:

- competing framings
- old prompts
- superseded terminology
- partially abandoned features
- duplicate approaches
- obsolete scripts
- comments that no longer match behaviour
- old UI concepts
- old retrieval strategies
- temporary workarounds
- TODOs that are no longer relevant

For each significant example, classify it as:

- clearly superseded
- probably superseded
- still active
- unclear

Do not treat historical residue as a requirement simply because it exists.

Likewise, do not remove something simply because it looks old.

Use the overall product objective to judge it.

---

# 4. IDENTIFY THE NON-NEGOTIABLE PRINCIPLES

Based on the repository, determine which constraints appear fundamental rather than incidental.

I expect some of these may include:

- Honest Broker behaviour
- evidence transparency
- preserving disagreement
- avoiding manufactured consensus
- human responsibility for corpus inclusion
- traceable source provenance
- eval-driven development
- not changing retrieval based purely on intuition
- clear separation between scientific evidence and AI interpretation

But determine this independently from the repository.

Explicitly tell me:

### These should probably be treated as hard constraints

and

### These currently look like implementation choices that can be reconsidered

This distinction is important.

---

# 5. THEN AUDIT THE PROJECT

Only after you have reconstructed the intended product should you evaluate the implementation.

Audit the project against its **objectives**, not simply against generic software-engineering best practices.

Review:

## Product

- Does the application actually deliver the intended user experience?
- Is the purpose obvious to a new user?
- Does it feel like an evidence exploration tool or merely a chatbot with sources?
- Is disagreement understandable?
- Is evidence quality understandable?
- Is provenance understandable?
- Are the different evidensrom sufficiently clear?
- Is `Spør kildene` doing the right job?

## Information architecture

Evaluate:

- home page
- room structure
- orientation sections
- evidence framing
- source cards
- question interface
- researcher/non-specialist modes
- progressive disclosure
- terminology

Look for complexity that reflects development history rather than user needs.

## Retrieval

Review:

- corpus selection
- query handling
- ranking
- similarity
- debate-link expansion
- top-k
- room-specific behaviour
- false positives
- false negatives
- duplicate evidence
- ranking quality

Do not recommend a more sophisticated retrieval stack merely because one exists.

Only recommend changes when there is a demonstrated problem or a strong architectural reason.

## Synthesis

Evaluate whether answers:

- answer the actual question
- remain grounded in retrieved sources
- preserve disagreement
- avoid artificial consensus
- distinguish evidence from interpretation
- make uncertainty legible
- avoid repetitive framing
- use important sources rather than just mentioning them
- avoid letting system prompts dominate the user's question

Pay particular attention to prompt complexity.

Determine whether years of incremental prompt additions have created brittle behaviour.

## Evidence model / corpus

Review:

- schema
- metadata
- provenance
- inclusion accountability
- verification
- document lifecycle
- QA
- ingest
- parquet generation
- duplicate handling
- stale data risks
- malformed metadata risks

Determine whether the system's evidence model is becoming too complicated or whether the complexity is justified.

## Evaluation

This is a high-priority part of the audit.

Determine whether the existing evaluations actually measure what matters.

Ask:

- Can retrieval tests pass while ranking is poor?
- Is recall alone sufficient?
- Are golden sets large/diverse enough?
- Can synthesis regress while automated checks still pass?
- Do we sufficiently test disagreement preservation?
- Do we sufficiently test source grounding?
- Do we test question adherence?
- Do we test room leakage?
- Is evaluation itself becoming overengineered?

Recommend additions only where they would materially increase confidence.

## Architecture

Determine whether the codebase is ready for more evidensrom.

Look for:

- duplicated room code
- hard-coded corpus assumptions
- growing conditionals
- shared abstractions that should exist
- abstractions that exist prematurely
- coupling between UI/retrieval/synthesis
- room configuration that belongs in data/config instead of code

Do not refactor simply for elegance.

## Reliability

Inspect:

- failure states
- missing secrets
- API failures
- empty retrieval
- malformed corpus records
- missing data files
- bad configuration
- Streamlit state
- caching
- deployment differences
- Windows vs Linux issues

## Performance

Identify real bottlenecks only.

Do not optimise theoretical problems.

## Security / configuration

Check:

- API keys
- secrets
- logging
- `.gitignore`
- config
- dependency risks
- accidental sensitive information

## Maintainability

Look for:

- dead code
- stale scripts
- old migration logic
- obsolete documentation
- duplicated implementations
- misleading comments
- historical residue
- overly complicated prompts
- brittle parsing

---

# 6. DO NOT IMPLEMENT ANYTHING YET

This is important:

**Do not modify any project files during this first pass.**

Do not fix issues as you find them.

Do not perform opportunistic refactoring.

Do not update documentation.

Do not alter prompts.

Do not change retrieval.

Do not change the UI.

Do not clean up files.

First complete the analysis and present your recommendations to me.

I want to decide what should be implemented.

---

# 7. DELIVERABLE 1 — YOUR UNDERSTANDING

First give me:

## What I think this project is

Explain the product in plain language.

## Main objectives

Rank the 5–8 most important objectives.

## Non-negotiable principles

What should almost certainly be preserved?

## Implementation choices

What current choices appear open to reconsideration?

## Historical residue

What parts of the repository appear to reflect previous directions rather than current intent?

## Uncertainties

Where could you not confidently infer my intent?

Do not manufacture certainty.

---

# 8. DELIVERABLE 2 — PROJECT AUDIT

Then give me a structured audit.

For every significant finding provide:

| Field | Description |
|---|---|
| Finding | The issue or opportunity |
| Evidence | What in the repository led you to it |
| Why it matters | Product/technical consequence |
| Priority | P0 / P1 / P2 / P3 |
| Confidence | High / medium / low |
| Recommendation | What you think should be done |
| Scope | Small / medium / large |
| Regression risk | Low / medium / high |

Priorities:

- **P0** — serious correctness, security, data-integrity or production issue
- **P1** — high-value improvement
- **P2** — useful but non-urgent
- **P3** — optional polish / speculative improvement

Be selective.

I prefer 10 strong findings over 40 generic suggestions.

---

# 9. DELIVERABLE 3 — RECOMMENDED IMPROVEMENT PLAN

After the audit, propose an implementation plan — but DO NOT execute it.

Divide recommendations into:

## Do now

Changes with:

- strong evidence
- high value
- low/moderate risk

## Probably do

Good ideas that need some judgment.

## Investigate first

Potential improvements where the evidence is not yet sufficient.

## Do not do

Ideas that may sound attractive but would add complexity without solving a demonstrated problem.

For each proposed improvement include:

- exact problem
- proposed change
- expected benefit
- affected files/components
- expected effort
- risk
- how we would validate that it improved the system

---

# 10. SPECIFIC QUESTIONS TO ANSWER

As part of the review, give me your judgment on these:

1. Is the core product concept coherent?

2. Does the current implementation actually support the Honest Broker goal?

3. Is the project becoming overcomplicated because of iterative development?

4. Are there places where old decisions should simply be removed?

5. Is the current RAG architecture appropriate for the problem?

6. Is retrieval quality actually good, or do the existing evaluations make it look better than it is?

7. Is synthesis too prompt-heavy or brittle?

8. Is the evidence/corpus model appropriately rigorous or unnecessarily complex?

9. Is the separation between the evidensrom architecturally clean?

10. Could a third and fourth room be added without significant duplication?

11. Is the Streamlit UX good enough for the intended users?

12. What are the three biggest things holding the project back?

13. What are the three strongest parts of the project that should not be disrupted?

14. If you were the senior engineer taking ownership of this project, what would you simplify?

15. What would you deliberately leave alone?

---

# 11. IMPORTANT MINDSET

Do not optimise for:

- number of recommendations
- amount of code changed
- sophistication
- trendy RAG architecture
- abstraction
- agentic complexity
- adding more AI

Optimise for:

- clarity of product
- evidence integrity
- trust
- retrieval quality
- synthesis quality
- transparency
- maintainability
- robustness
- ease of extending the platform

The best recommendation may sometimes be:

> Leave this alone. The existing solution is appropriate.

And another valid recommendation may be:

> This looks like historical complexity. Delete or simplify it.

Use engineering judgment.

---

# STOP POINT

After presenting:

1. your understanding of the project,
2. the audit,
3. the prioritised recommendations,
4. the proposed implementation plan,

**STOP.**

Do not implement anything.

Wait for me to review the recommendations and tell you which changes I want implemented.