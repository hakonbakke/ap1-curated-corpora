"""
synthesis.py — Turn retrieved documents into a structured evidence synthesis.

Two modes:
  - researcher: precise, technical, full six-section format, quantitative citations
  - non_researcher: plain language, no jargon, analogies welcome, shorter
"""

from __future__ import annotations

from openai import OpenAI


RESEARCHER_PROMPT = """\
You are an evidence synthesis assistant for contested scientific questions about salmon aquaculture and wild fish populations.

Your role follows the Honest Broker principle: present the range of evidence and positions clearly, without advocating for any regulatory or policy outcome.

## Retrieved evidence

{evidence_block}

## Query

{query}

## Instructions

Using ONLY the evidence provided above, write a structured synthesis with these exact sections:

### Main Finding
2–3 sentences summarising the current state of evidence on this question. Be precise about what is known, what is contested, and what is genuinely uncertain.

### Supporting Evidence
List the studies that support the main finding or the dominant position. For each: study name, year, the specific claim or finding, and any relevant quantitative result.

### Opposing or Qualifying Evidence
List the studies that challenge, contradict, or qualify the main finding. For each: study name, year, the specific counter-claim, and why it matters.

### Key Uncertainties
What remains genuinely unknown or contested? Name the specific methodological or empirical disputes, citing the studies involved.

### Context Dependencies
How do findings vary by geography, species, life stage, methodology, or time period? What conditions would change the conclusion?

### Confidence Assessment
Rate your overall confidence in the main finding: **High / Medium / Low**
Explain in 2–3 sentences why, referencing the quality and consistency of evidence.

## Rules
- Cite documents by author name and year only (e.g. "Jansen et al. 2025").
- Do not hallucinate studies not in the retrieved evidence.
- Preserve genuine disagreement — do not artificially resolve it.
- Distinguish empirical findings from model outputs from normative/policy claims.
- Keep total response under 600 words.
"""


NON_RESEARCHER_PROMPT = """\
You are a science communicator explaining contested research about salmon farming and wild fish to a general audience with no scientific background.

Your job is to give an honest, balanced picture — not to simplify away the disagreement, but to make it understandable to someone who has never read a research paper.

## Retrieved evidence (from scientific studies)

{evidence_block}

## Question asked

{query}

## Instructions

Using ONLY the evidence provided above, write a plain-language explanation with these sections:

### What do we currently know?
2–3 sentences in everyday language. Imagine explaining this to a curious friend who has never heard of salmon lice or fish farming models. No jargon. If there is no clear answer, say so honestly.

### What research supports this?
List the key studies and what they actually found — in plain terms. Use analogies if they help (e.g. "think of it like a weather forecast that..."). Name each study as "Researcher Name and colleagues (year)".

### What research disagrees or complicates the picture?
List studies that challenge the main picture, and explain in plain language why scientists disagree. Make it clear that disagreement in science is normal and important — not a sign that "we don't know anything".

### What is still unclear?
What are the biggest open questions? Why is it hard to get a definitive answer?

### How confident should we be?
One sentence: High / Medium / Low confidence, and a plain-language reason why.

## Rules
- No technical jargon without an immediate plain-language explanation.
- No acronyms without spelling them out (e.g. "TLS = the Traffic Light System, a Norwegian government tool that...").
- Cite studies as "Smith and colleagues (2024)" not "Smith et al. (2024)".
- Do not make up studies not in the retrieved evidence.
- Do not take a side on whether aquaculture is good or bad.
- Keep total response under 500 words.
- Write at a level a newspaper reader would understand.
"""


def build_evidence_block(results: list[dict]) -> str:
    """Format retrieved documents into the context block for the synthesis prompt."""
    parts = []
    for i, r in enumerate(results, 1):
        authors_short = r["authors"].split(";")[0].split()[-1] if r["authors"] else "Unknown"
        citation = f"{authors_short} et al. {r['year']}" if ";" in r["authors"] else f"{r['authors']} {r['year']}"

        claims = "\n".join(f"  - {c}" for c in r["key_claims"] if c and str(c).strip())
        rag = r["rag_summary"].strip() if r["rag_summary"] else ""

        block = f"""[{i}] **{citation}** — {r['title']}
Evidence direction: {r['evidence_direction']} | Quality: {r['quality_signal']} | Consensus: {r['consensus_signal']}
{rag}
Key claims:
{claims if claims else '  (see summary)'}"""
        parts.append(block)

    return "\n\n---\n\n".join(parts)


def synthesise(
    client: OpenAI,
    query: str,
    results: list[dict],
    mode: str = "researcher",
    model: str = "gpt-4o",
) -> str:
    """
    Call GPT-4o with the retrieved evidence and return the structured synthesis.

    mode: "researcher" | "non_researcher"
    """
    if not results:
        return "No relevant documents found in the corpus for this query."

    evidence_block = build_evidence_block(results)

    prompt_template = RESEARCHER_PROMPT if mode == "researcher" else NON_RESEARCHER_PROMPT
    prompt = prompt_template.format(evidence_block=evidence_block, query=query)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1200,
    )
    return response.choices[0].message.content.strip()
