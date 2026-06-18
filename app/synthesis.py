"""
synthesis.py — Turn retrieved documents into an evidence synthesis.

Dimensions:
  - mode: researcher | non_researcher
  - answer_format: structured (fixed sections) | freeform (question-shaped)
  - output_language: passed as full instruction string (e.g. English, Norwegian Bokmål)
"""

from __future__ import annotations

from openai import OpenAI

OUTPUT_LANGUAGE_RULE = """\
Write the entire synthesis in **{output_language}**.
Use clear, complete sentences. Be thorough rather than terse."""


DEPTH_RESEARCHER = """\
**Depth:** Give a substantive synthesis, not a brief summary.
- Aim for roughly **900–1,400 words** for broad questions; **600–900** for narrow factual questions.
- Include **numbers, effect sizes, thresholds, or dates** whenever they appear in the retrieved evidence.
- Explain **why** studies disagree (methods, geography, assumptions), not only that they disagree."""


DEPTH_FREEFORM_RESEARCHER = """\
**Depth:** Write a **synthesised argument**, not a catalogue of papers.
- Aim for roughly **700–1,100 words** for broad questions; **450–700** for narrow questions.
- **Do not give every retrieved document its own paragraph.** Select and combine: cite only studies that materially move the answer forward.
- Typical structure: 3–5 body paragraphs organised by **theme or tension** (mechanism, field experiments, models, counter-evidence, management context) — not by author order.
- In a broad answer, mentioning **4–6 studies by name** is usually enough; others can be folded in as "several field studies" if they say the same thing.
- Include **numbers** where they sharpen the argument; skip repeating the same point from multiple papers.
- Distinguish **individual / cohort / model / population** evidence levels explicitly."""


DEPTH_NON_RESEARCHER = """\
**Depth:** Explain fully in plain language — not a one-paragraph skim.
- Aim for roughly **650–1,000 words** for broad questions; **450–650** for simple questions.
- Use short examples or analogies where they clarify; avoid unexplained jargon."""


DEPTH_FREEFORM_NON_RESEARCHER = """\
**Depth:** Tell one clear story — not a list of studies.
- Aim for roughly **550–900 words** for broad questions.
- **Do not walk through every paper one by one.** Pick the most important examples (often 3–5) and weave them into the narrative.
- Group ideas: what we know, what is disputed, why it is hard to be sure."""


# ── Researcher: freeform (question-shaped) ───────────────────────────────────

RESEARCHER_FREEFORM_PROMPT = """\
You are an evidence synthesis assistant for contested scientific questions about salmon aquaculture and wild fish populations.

Your role follows the Honest Broker principle: present the range of evidence and positions clearly, without advocating for any regulatory or policy outcome.

{output_language_rule}

{depth}

## Retrieved evidence

{evidence_block}

## Query

{query}

## How to write the answer

Write **one coherent essay** that answers the question. The reader should feel you **thought across the evidence**, not that you **reported each file in turn**.

### Anti-pattern (do NOT do this)
- One paragraph per author in retrieval order ("Folk et al. … Forseth et al. … Fjelldal et al. …")
- Mentioning every retrieved document because it appeared in the bundle
- Repeating the same conclusion from several similar studies in separate paragraphs

### Good pattern
- **Paragraph 1:** Direct answer to the query in 2–4 sentences (what is supported, what is contested).
- **Middle paragraphs:** Develop the argument by **theme** — e.g. causal chain, experimental returns, modelled mortality, observational/population links, qualifying counter-evidence. Within each paragraph, **combine** studies that support the same point; **contrast** studies that tension each other.
- **Final paragraph:** Confidence (**High / Medium / Low**) and what would change your assessment — woven into prose, not a labelled box.

Use **parenthetical citations** (Jansen et al. 2025) inside sentences. It is fine to write: "Randomised release experiments in Norway (Bøhn et al. 2020) and PIM–return analyses (Jansen et al. 2025) both suggest …" without dedicating a full paragraph to each.

**Selectivity:** {n} documents were retrieved; you need not name all {n}. Prioritise studies that directly address the query. Skip or briefly group peripheral lab studies unless they add a distinct mechanism.

**Evidence levels:** When citing models, say they are model outputs and note assumptions. When citing lab work, do not treat it as population proof unless the study itself does.

Headings are optional — use at most 2–3, only when the topic genuinely shifts.

## Rules
- Use ONLY the retrieved evidence; do not invent studies or findings.
- Preserve genuine disagreement — do not paper over it.
- Distinguish empirical findings, model outputs, and normative/policy claims.
- No bullet lists unless comparing 3+ numeric results in one glance.
"""


# ── Researcher: structured (fixed sections) ────────────────────────────────────

RESEARCHER_STRUCTURED_PROMPT = """\
You are an evidence synthesis assistant for contested scientific questions about salmon aquaculture and wild fish populations.

Your role follows the Honest Broker principle: present the range of evidence and positions clearly, without advocating for any regulatory or policy outcome.

{output_language_rule}

{depth}

## Retrieved evidence

{evidence_block}

## Query

{query}

## Instructions

Using ONLY the evidence provided above, write a structured synthesis with these **exact** section headings (in this order). **Each section should be fully developed** — typically one short overview paragraph plus detailed points; do not write one-line sections.

### Main Finding
A concise overview (1 short paragraph), then 1–2 paragraphs on what is known, contested, and uncertain.

### Supporting Evidence
For **each** relevant supporting study: author and year, study type, specific finding, quantitative detail if available, and how it fits the overall picture. Use multiple paragraphs or a substantive bullet per study.

### Opposing or Qualifying Evidence
For **each** relevant challenging study: author and year, the counter-claim or qualification, methodological reason it matters, and how it interacts with supporting evidence.

### Key Uncertainties
Name specific disputes (calibration, migration, thresholds, causation, etc.) and which studies embody each side. Be explicit about what would reduce uncertainty.

### Context Dependencies
Geography, species, life stage, methodology, time period, regulatory context — with examples from the retrieved evidence.

### Confidence Assessment
Rate: **High / Medium / Low**. Explain in a full paragraph referencing quality, consistency, and gaps across the retrieved set.

## Rules
- Cite documents by author name and year only (e.g. "Jansen et al. 2025").
- Do not hallucinate studies not in the retrieved evidence.
- Preserve genuine disagreement.
- Distinguish empirical findings from model outputs from normative/policy claims.
- Target roughly **1,000–1,400 words** total unless the query is very narrow.
"""


# ── Non-researcher: freeform ─────────────────────────────────────────────────

NON_RESEARCHER_FREEFORM_PROMPT = """\
You are a science communicator explaining contested research about salmon farming and wild fish to a general audience with no scientific background.

Your job is to give an honest, balanced picture — not to simplify away disagreement, but to make it understandable.

{output_language_rule}

{depth}

## Retrieved evidence (from scientific studies)

{evidence_block}

## Question asked

{query}

## How to write the answer

Write **flowing prose** — like a short feature article — that answers the question in plain language.

**Do NOT** go through each study in order ("First, Smith and colleagues … Then, Jones and colleagues …"). That reads like a list, not an explanation.

Instead:
- Start with a **plain answer** in everyday language.
- Build **2–4 paragraphs** grouped by **ideas** (how lice from farms reach wild fish; what experiments show; why some researchers disagree; how sure we can be).
- Use **only the clearest examples** (often 3–5 studies named); group the rest as "other research" when they repeat the same point.
- Explain disagreements **inside** the story, not in a separate list of "opposing papers".
- End with **High / Medium / Low** confidence and a simple reason why.

## Rules
- Use ONLY the retrieved evidence; do not make up studies.
- Cite as "Researcher Name and colleagues (year)" when naming a study.
- No unexplained jargon — spell out terms on first use.
- Do not argue that aquaculture is good or bad overall.
"""


# ── Non-researcher: structured ─────────────────────────────────────────────────

NON_RESEARCHER_STRUCTURED_PROMPT = """\
You are a science communicator explaining contested research about salmon farming and wild fish to a general audience with no scientific background.

{output_language_rule}

{depth}

## Retrieved evidence (from scientific studies)

{evidence_block}

## Question asked

{query}

## Instructions

Using ONLY the evidence provided above, write a plain-language explanation with these **exact** section headings (in this order). **Each section should be substantive** — not a single sentence.

### What do we currently know?
2–3 paragraphs in everyday language. If there is no clear answer, explain why honestly.

### What research supports this?
For each relevant study: name as "Researcher Name and colleagues (year)", what they found, and why it matters — 2–4 sentences per study.

### What research disagrees or complicates the picture?
Same level of detail for studies that push back or add nuance. Explain why scientists disagree.

### What is still unclear?
The biggest open questions, in plain language, with enough context that the reader understands the stakes.

### How confident should we be?
**High / Medium / Low** plus a short paragraph (not one sentence) explaining why.

## Rules
- No technical jargon without an immediate plain-language explanation.
- Spell out acronyms on first use.
- Do not make up studies not in the retrieved evidence.
- Do not take a side on whether aquaculture is good or bad.
- Target roughly **750–1,100 words** total unless the query is very narrow.
"""


PROMPTS: dict[tuple[str, str], str] = {
    ("researcher", "freeform"): RESEARCHER_FREEFORM_PROMPT,
    ("researcher", "structured"): RESEARCHER_STRUCTURED_PROMPT,
    ("non_researcher", "freeform"): NON_RESEARCHER_FREEFORM_PROMPT,
    ("non_researcher", "structured"): NON_RESEARCHER_STRUCTURED_PROMPT,
}

# (mode, answer_format) -> max_tokens
MAX_TOKENS: dict[tuple[str, str], int] = {
    ("researcher", "freeform"): 4000,
    ("researcher", "structured"): 4000,
    ("non_researcher", "freeform"): 2800,
    ("non_researcher", "structured"): 2800,
}

# Per-document cap for full evidence brief (structured mode; from summary.md)
SUMMARY_MAX_CHARS_PER_DOC = 5000
# Freeform: compact context — avoids "must mention every long brief" behaviour
FREEFORM_SUMMARY_MAX_CHARS = 1200
FREEFORM_FULL_BRIEF_TOP_N = 3


def truncate_summary_text(text: str, max_chars: int = SUMMARY_MAX_CHARS_PER_DOC) -> str:
    """Cap summary length for synthesis context; prefer cutting at paragraph boundary."""
    text = text.strip()
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars]
    last_break = cut.rfind("\n\n")
    if last_break > max_chars * 0.7:
        cut = cut[:last_break]
    return cut.rstrip() + "\n\n[… evidence brief truncated for context length …]"


def build_evidence_block(results: list[dict], *, compact: bool = False) -> str:
    """Format retrieved documents into the context block for the synthesis prompt."""
    parts = []
    for i, r in enumerate(results, 1):
        authors_short = r["authors"].split(";")[0].split()[-1] if r["authors"] else "Unknown"
        citation = f"{authors_short} et al. {r['year']}" if ";" in r["authors"] else f"{r['authors']} {r['year']}"

        claims = "\n".join(f"  - {c}" for c in r["key_claims"] if c and str(c).strip())
        rag = r["rag_summary"].strip() if r["rag_summary"] else ""
        effect_scale = r.get("effect_scale") or ""
        doc_type = r.get("document_type") or ""
        controversy = r.get("controversy_role") or ""

        meta_line = (
            f"Evidence direction: {r['evidence_direction']} | Quality: {r['quality_signal']}"
            f" | Effect scale: {effect_scale or '—'} | Type: {doc_type or '—'}"
        )
        if controversy and str(controversy).strip() and controversy not in ("none", "not_applicable"):
            meta_line += f" | Role: {controversy}"

        block = f"""[{i}] **{citation}** — {r['title']}
{meta_line}
Retrieval summary: {rag if rag else "(see key claims)"}
Key claims:
{claims if claims else "  (see retrieval summary)"}"""

        summary_raw = (r.get("summary_text") or "").strip()
        if summary_raw:
            if compact:
                if i <= FREEFORM_FULL_BRIEF_TOP_N:
                    cap = FREEFORM_SUMMARY_MAX_CHARS
                    label = "Evidence excerpt"
                else:
                    cap = 400
                    label = "Brief excerpt"
                block += f"\n\n{label}:\n{truncate_summary_text(summary_raw, cap)}"
            else:
                block += f"\n\nEvidence brief (curated from full paper):\n{truncate_summary_text(summary_raw)}"

        parts.append(block)

    return "\n\n---\n\n".join(parts)


def evidence_block_intro(n: int, answer_format: str) -> str:
    if answer_format == "freeform":
        return (
            f"**{n} documents** were retrieved. Use them selectively — synthesise by theme, "
            f"not as a checklist. You do not need to cite all {n}.\n\n"
        )
    return (
        f"**{n} documents** were retrieved as most relevant. "
        f"Your synthesis should draw substantively from each document that bears on the query.\n\n"
    )


def synthesise(
    client: OpenAI,
    query: str,
    results: list[dict],
    mode: str = "researcher",
    answer_format: str = "freeform",
    output_language: str = "English",
    model: str = "gpt-4o",
) -> str:
    """
    Call GPT-4o with the retrieved evidence and return a synthesis.

    mode: "researcher" | "non_researcher"
    answer_format: "structured" | "freeform"
    """
    if not results:
        return "No relevant documents found in the corpus for this query."

    if answer_format not in ("structured", "freeform"):
        answer_format = "freeform"

    n = len(results)
    compact = answer_format == "freeform"
    evidence_body = build_evidence_block(results, compact=compact)
    evidence_block = evidence_block_intro(n, answer_format) + evidence_body

    if mode == "researcher":
        depth = DEPTH_FREEFORM_RESEARCHER if answer_format == "freeform" else DEPTH_RESEARCHER
    else:
        depth = DEPTH_FREEFORM_NON_RESEARCHER if answer_format == "freeform" else DEPTH_NON_RESEARCHER
    lang_rule = OUTPUT_LANGUAGE_RULE.format(output_language=output_language)

    prompt_template = PROMPTS.get((mode, answer_format), RESEARCHER_FREEFORM_PROMPT)
    prompt = prompt_template.format(
        evidence_block=evidence_block,
        query=query,
        output_language_rule=lang_rule,
        depth=depth,
        n=n,
    )

    temperature = 0.2 if answer_format == "structured" else 0.35
    max_tokens = MAX_TOKENS.get((mode, answer_format), 2800)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()
