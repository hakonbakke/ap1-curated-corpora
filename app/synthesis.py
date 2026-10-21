"""
synthesis.py — Turn retrieved documents into an evidence synthesis.

Dimensions:
  - mode: researcher | non_researcher
  - answer_format: structured (fixed sections) | freeform (question-shaped)
  - output_language: passed as full instruction string (e.g. English, Norwegian Bokmål)
"""

from __future__ import annotations

import re
import unicodedata

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
**Depth:** Tell one clear explanation that keeps the fault lines visible — not a list of studies, and not a smoothed consensus.
- Aim for roughly **550–900 words** for broad questions.
- **Do not walk through every paper one by one.** Name the main camps with 3–5 concrete examples; if two camps conflict, keep both even if that makes the story messier.
- Group ideas: what most evidence points to, where serious researchers disagree, and why we cannot be sure yet."""


AREA_DEPTH_FREEFORM_NON_RESEARCHER = """\
**Depth:** Tell one clear explanation that keeps competing diagnoses visible — not a list of studies, and not a smoothed consensus.
- Aim for roughly **400–600 words** for broad questions and **250–400** for simple ones, not counting the short answer. Readers may be on a phone.
- **Do not walk through every paper one by one.** Name the main diagnoses with 3–5 concrete examples. If two diagnoses conflict, keep both even if that makes the story messier.
- Group ideas: what the question is actually about, where the texts disagree on the problem definition, and why the file does not close it.
- Do not recast every answer as researcher camps on whether farming threatens wild fish."""

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

Your job is an honest broker for non-experts: make disagreement understandable. Never invent a middle ground that the studies do not support. If camps conflict, say so in plain words.

{output_language_rule}

{depth}

## Retrieved evidence (from scientific studies)

{evidence_block}

Treat policy details mentioned in this prompt as framing only. State them as facts only when they are supported by the retrieved evidence; otherwise omit them.

## Question asked

{query}

## How to write the answer

Write **flowing prose** — like a short feature article — that answers the question in plain language.

**Do NOT** go through each study in order ("First, Smith and colleagues … Then, Jones and colleagues …"). That reads like a list, not an explanation.

Instead:
- Start with a **plain answer** that states both (a) the main claim and (b) that scientists still disagree, when they do. Do **not** open with false consensus phrases like "there is agreement that…" / «det er enighet om…» when the retrieved evidence is contested.
- Build **2–4 paragraphs** by idea, and **require one full paragraph on the opposing or qualifying camp** (what they claim, and why they think the other side is wrong), in everyday language.
- Name **both sides** with concrete examples. You may group similar papers, but **do not** fold a conflicting paper into "other research."
- Keep disagreement inside the narrative, but make the camps impossible to miss (e.g. "One group of studies says … Another group says …").
- End with **High / Medium / Low** confidence, a simple reason, and **one concrete thing that would change the picture**.

## Rules
- Use ONLY the retrieved evidence; do not make up studies.
- Preserve real disagreement — do not paper it over or invent a compromise.
- Cite as "Researcher Name and colleagues (year)" when naming a study.
- Say when a result is from a lab study, a computer model, or real-world fish counts; do not treat them as the same kind of proof.
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

_SYNTHESIS_STOPWORDS = {
    "and", "are", "for", "from", "how", "the", "what", "when", "where", "which",
    "with", "eller", "for", "fra", "har", "hva", "hvordan", "hvor", "med", "når",
    "og", "om", "som", "til", "ved", "det", "den",
}


def _query_tokens(text: str) -> set[str]:
    normalized = unicodedata.normalize("NFKC", text or "").casefold()
    return {
        token for token in re.findall(r"[^\W_]+", normalized, flags=re.UNICODE)
        if len(token) > 1 and token not in _SYNTHESIS_STOPWORDS
    }


def _rank_evidence_items(items: list[str], query: str, limit: int) -> list[str]:
    query_tokens = _query_tokens(query)
    scored = []
    for position, item in enumerate(items or []):
        clean = str(item).strip()
        if not clean:
            continue
        overlap = len(query_tokens.intersection(_query_tokens(clean)))
        scored.append((overlap, -position, clean))
    scored.sort(reverse=True)
    return [item for _, _, item in scored[:limit]]


def _relevant_summary_excerpt(text: str, query: str, max_chars: int) -> str:
    """Select query-matched paragraphs instead of taking the start of the brief."""
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text or "") if p.strip()]
    ranked = _rank_evidence_items(paragraphs, query, 3)
    if not ranked:
        return ""
    excerpt = "\n\n".join(ranked)
    return truncate_summary_text(excerpt, max_chars)


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


def citation_label(authors: str, year: object, title: str = "") -> str:
    """Short citation the model copies: "Myklebust 2018", "Osmundsen & Olsen 2025", "Robertsen et al. 2014".

    Two-author works must not become "et al."; reports without authors fall back to the title.
    """
    surnames = [a.split()[-1] for a in (authors or "").split(";") if a.strip()]
    if not surnames:
        who = (title or "Unknown").strip()[:60]
    elif len(surnames) == 1:
        who = surnames[0]
    elif len(surnames) == 2:
        who = f"{surnames[0]} & {surnames[1]}"
    else:
        who = f"{surnames[0]} et al."
    return f"{who} {year}".strip()


def build_evidence_block(results: list[dict], *, compact: bool = False, query: str = "") -> str:
    """Format retrieved documents into the context block for the synthesis prompt."""
    parts = []
    for i, r in enumerate(results, 1):
        citation = citation_label(r.get("authors") or "", r.get("year", ""), r.get("title") or "")

        selected_claims = _rank_evidence_items(r.get("key_claims") or [], query, 4)
        claims = "\n".join(f"  - {c}" for c in selected_claims)
        rag = r["rag_summary"].strip() if r["rag_summary"] else ""
        effect_scale = r.get("effect_scale") or ""
        doc_type = r.get("document_type") or ""
        controversy = r.get("controversy_role") or ""

        source_type = r.get("source_type") or r.get("document_type") or "—"
        study_design = ", ".join(r.get("study_design") or []) or "—"
        geography = ", ".join(r.get("geography") or []) or "—"
        meta_line = (
            f"Evidence direction: {r['evidence_direction']} | Quality: {r['quality_signal']}"
            f" | Effect scale: {effect_scale or '—'} | Type: {source_type} / {doc_type or '—'}"
            f" | Study design: {study_design} | Geography: {geography}"
        )
        if controversy and str(controversy).strip() and controversy not in ("none", "not_applicable"):
            meta_line += f" | Role: {controversy}"

        block = f"""[{i}] **{citation}** — {r['title']}
{meta_line}
Retrieval summary: {rag if rag else "(see key claims)"}
Key claims:
{claims if claims else "  (see retrieval summary)"}"""

        for label, key, limit in (
            ("Methodological limitations", "methodological_limitations", 2),
            ("Uncertainty", "claims_about_uncertainty", 2),
            ("Policy/management claims", "claims_about_policy_or_management", 2),
        ):
            items = _rank_evidence_items(r.get(key) or [], query, limit)
            if items:
                block += f"\n{label}:\n" + "\n".join(f"  - {item}" for item in items)

        verification = r.get("curator_review_status") or "unknown"
        block += f"\nVerification status: {verification}"
        if r.get("evidence_family") and r.get("evidence_family") != f"family:{r.get('doc_id')}":
            block += f"\nEvidence family: {r['evidence_family']} (do not count family members as independent corroboration)"

        summary_raw = (r.get("summary_text") or "").strip()
        if summary_raw:
            if compact:
                cap = FREEFORM_SUMMARY_MAX_CHARS if i <= FREEFORM_FULL_BRIEF_TOP_N else 500
                excerpt = _relevant_summary_excerpt(summary_raw, query, cap)
                if excerpt:
                    block += f"\n\nQuery-relevant evidence excerpt:\n{excerpt}"
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


CONFIDENCE_RULES = """\
## Confidence calibration (mandatory)
- Rate confidence **High / Medium / Low** only as allowed below.
- If any central retrieved source has `evidence_direction: critiques_methodology`,
  or `consensus_signal: contested`, or the query is about disagreement / robustness /
  Traffic Light legitimacy: **do not conclude High**. Use **Medium** or **Low**,
  and name the disagreement explicitly.
- Distinguish evidence levels: lab / individual ≠ modelled smolt mortality ≠ population /
  adult returns. Do not treat model outputs as observed stock decline.
- If the query asks about population / bestand / adult returns, prioritise Q9-tagged
  sources in the argument; do not let peripheral physiology papers dominate the conclusion.
- Cite only studies present in the retrieved evidence block. If evidence is thin, say so.
"""


def confidence_guidance(results: list[dict]) -> str:
    """Extra prompt constraints derived from retrieved metadata."""
    directions = {r.get("evidence_direction") for r in results}
    consensus = {r.get("consensus_signal") for r in results}
    contested = (
        "critiques_methodology" in directions
        or "contested" in consensus
        or "contradicts_effect" in directions
        or "no_effect_detected" in directions
        or "no_significant_effect" in directions
    )
    if contested:
        return (
            CONFIDENCE_RULES
            + "\n**This retrieval set is contested or mixed.** "
            + "Maximum confidence for a unified causal claim: **Medium**.\n"
        )
    return CONFIDENCE_RULES + "\n"


AREA_ROOM_FRAME = """\
**Room:** Area and aquaculture (Areal og havbruk).
The object is aquaculture's claim on coastal sea. Other uses and living
nature enter only when they block, compete with, or force a trade-off of
that claim. Answer the specific question asked and use only factual claims
present in the retrieved evidence below.

Treat plans, permits, the case file, economics, density, competing uses and
scarcity as distinct questions. Compare diagnoses only when the retrieved
sources actually offer competing explanations. Do not manufacture opposing
camps, turn complementary findings into disagreement, or collapse real
disagreement into consensus.

Distinguish empirical findings, models, legal analysis, policy claims and
adjacent evidence. When two records belong to the same evidence family,
they may add detail but do not count as independent corroboration. State
material limitations and uncertainty that bear on the question. If the
retrieved evidence is insufficient, narrow or only adjacent, say so.
"""


# Short answer first: many workshop readers are on phones and skim. Joined into
# both Areal prompts below, so it must not contain format braces.
AREA_SHORT_ANSWER = """\
### Short answer first (mandatory)
Open with a bold label: **Kort svar** when writing Norwegian, **Short answer** when writing English. Under it, exactly **three bullets**, each one plain sentence of at most 25 words:
1. The direct answer to the question asked.
2. Where the retrieved sources disagree or offer competing diagnoses. If they do not disagree on this question, the most important condition or limit instead. Never invent a disagreement.
3. What remains uncertain or is missing from the evidence.
No citations in the bullets. Every bullet must be backed up, with citations, in the text that follows; do not put anything in the bullets that the text does not support. Then leave a blank line and write the full answer below. Its first paragraph should develop the short answer, not repeat it word for word.
"""


AREA_RESEARCHER_FREEFORM_PROMPT = """\
You are an evidence synthesis assistant for contested questions about \
aquaculture's claim on Norwegian coastal sea area.

Your role follows the Honest Broker principle: present the range of evidence and positions clearly, without advocating for any regulatory or policy outcome.

{output_language_rule}

{depth}

## Retrieved evidence

{evidence_block}

## Query

{query}

## How to write the answer

""" + AREA_SHORT_ANSWER + """
Below the short answer, write **one coherent essay** that answers the question. The reader should feel you **thought across the evidence**, not that you **reported each file in turn**.

### Anti-pattern (do NOT do this)
- One paragraph per author in retrieval order
- Mentioning every retrieved document because it appeared in the bundle
- Repeating the same conclusion from several similar studies in separate paragraphs
- Opening as a wild-fish impact controversy when the question is about plans, licences, the case file, money, density, or what limits growth

### Good pattern
- **Paragraph 1:** Direct answer to the query in 2–4 sentences (what is supported, what is contested). If wild salmon or the traffic-light limits capacity or a locality, say that as a growth lid, not as the mortality-chain debate.
- **Middle paragraphs:** Develop the argument by **theme or diagnosis** (licences, municipal designation, biology, competing use, knowledge in the file). Within each paragraph, **combine** studies that support the same point; **contrast** studies that tension each other.
- **Final paragraph:** Confidence (**High / Medium / Low**) and what would change your assessment — woven into prose, not a labelled box.

Use **parenthetical citations** inside sentences, in both Norwegian and English: (Robertsen et al., 2014) for three or more authors, (Sand og Misund, 2025) or (Sand and Misund, 2025) for two, (Myklebust, 2018) for one. Never write "og kolleger" or "and colleagues". Name only studies that appear in the retrieved evidence.

**Selectivity:** {n} documents were retrieved; you need not name all {n}. Prioritise studies that directly address the query.

**Evidence levels:** When citing models, say they are model outputs and note assumptions. When citing legal or policy texts, do not treat them as field measurements.

Headings are optional — use at most 2–3, only when the topic genuinely shifts.

## Rules
- Use ONLY the retrieved evidence; do not invent studies or findings.
- Preserve genuine disagreement — do not paper over it.
- Distinguish empirical findings, model outputs, and normative/policy claims.
- Apart from the short-answer bullets, no bullet lists unless comparing 3+ numeric results in one glance.
"""


AREA_NON_RESEARCHER_FREEFORM_PROMPT = """\
You are a science communicator explaining contested research on aquaculture's \
claim on Norwegian coastal sea to a general audience with no scientific background.

Your job is an honest broker for non-experts: make the open questions \
understandable (where growth stops, and where knowledge is missing). \
The live fight in this room is what limits or opens growth and \
coexistence for farms. Never invent a middle ground that the studies do not support. \
If diagnoses conflict, say so in plain words. Do not invent two scientific camps on \
one estimate.

This is not the salmon-lice / wild-salmon mortality room. Wild salmon belongs in \
the answer when it gates expansion: the traffic-light colours 13 production areas \
and can freeze, cut or allow capacity growth; lice can also be a reason to refuse \
a locality. Do not open with a debate about whether salmon farming threatens wild \
fish, and do not invent two researcher camps on that question, unless the user \
actually asked that.

{output_language_rule}

{depth}

## Retrieved evidence (from scientific studies)

{evidence_block}

## Question asked

{query}

## How to write the answer

""" + AREA_SHORT_ANSWER + """
Below the short answer, write **flowing prose** — like a short feature article — that answers the question in plain language.

**Do NOT** go through each study in order ("First, Smith and colleagues … Then, Jones and colleagues …"). That reads like a list, not an explanation.

Instead:
- Start with a **plain answer to the question that was asked**. If the retrieved papers disagree, state the competing diagnoses in the first paragraph. Do **not** open with false consensus phrases like "there is agreement that…" / «det er enighet om…» when the retrieved evidence is contested.
- Do **not** open with stock phrases such as "The debate about salmon farming and its impact on wild fish" / «Debatten om lakseoppdrett og påvirkningen på villfisk» when the question is about plans, licences, the case file, money, density, or what limits growth.
- Build **2–4 paragraphs** by idea. If the retrieved papers write past one another, explain each material diagnosis (what they claim is scarce, what must yield, or where the case dies). Do not force a disagreement when the evidence is complementary.
- Name each material diagnosis with concrete examples. You may group similar papers, but **do not** fold a conflicting paper into "other research."
- Keep disagreement inside the narrative. Make the diagnoses impossible to miss (e.g. "One group of studies says the limit is licences and the traffic-light … Another group says the municipality will not designate usable sea …").
- End with **High / Medium / Low** confidence, a simple reason, and **one concrete thing that would change the picture**.

## Rules
- Use ONLY the retrieved evidence; do not make up studies.
- Preserve real disagreement — do not paper it over or invent a compromise.
- Name at least three of the retrieved studies in the text (outside the short answer), so readers can check the sources.
- When naming a study in Norwegian, write «Robertsen mfl. (2014)» for three or more authors, «Sand og Misund (2025)» for two and «Myklebust (2018)» for one. Never write «og kolleger». In English, write "Robertsen and colleagues (2014)", "Sand and Misund (2025)", "Myklebust (2018)".
- Say when a result is from a plan study, a legal review, a computer model, or field data; do not treat them as the same kind of proof.
- No unexplained jargon — spell out terms on first use.
- Do not argue that aquaculture is good or bad overall.
"""


NO_RESULTS_MESSAGE = "No relevant documents found in the corpus for this query."


def _build_request(
    query: str,
    results: list[dict],
    mode: str = "researcher",
    answer_format: str = "freeform",
    output_language: str = "English",
    model: str = "gpt-4o",
    room: str = "villaks",
) -> dict:
    """Build the chat.completions kwargs (prompt, model, token limits) for one synthesis."""
    if answer_format not in ("structured", "freeform"):
        answer_format = "freeform"

    n = len(results)
    compact = answer_format == "freeform"
    evidence_body = build_evidence_block(results, compact=compact, query=query)
    if room == "areal":
        guidance = AREA_ROOM_FRAME + "\n"
    else:
        guidance = confidence_guidance(results)
    evidence_block = guidance + evidence_block_intro(n, answer_format) + evidence_body

    if room == "areal" and answer_format == "freeform":
        if mode == "researcher":
            depth = DEPTH_FREEFORM_RESEARCHER
            prompt_template = AREA_RESEARCHER_FREEFORM_PROMPT
        else:
            depth = AREA_DEPTH_FREEFORM_NON_RESEARCHER
            prompt_template = AREA_NON_RESEARCHER_FREEFORM_PROMPT
    else:
        if mode == "researcher":
            depth = DEPTH_FREEFORM_RESEARCHER if answer_format == "freeform" else DEPTH_RESEARCHER
        else:
            depth = DEPTH_FREEFORM_NON_RESEARCHER if answer_format == "freeform" else DEPTH_NON_RESEARCHER
        prompt_template = PROMPTS.get((mode, answer_format), RESEARCHER_FREEFORM_PROMPT)
    lang_rule = OUTPUT_LANGUAGE_RULE.format(output_language=output_language)
    prompt = prompt_template.format(
        evidence_block=evidence_block,
        query=query,
        output_language_rule=lang_rule,
        depth=depth,
        n=n,
    )

    temperature = 0.2 if answer_format == "structured" else 0.35
    max_tokens = MAX_TOKENS.get((mode, answer_format), 2800)
    # gpt-6 rejects max_tokens. Reasoning off keeps temperature and the areal writer test.
    token_key = "max_tokens" if model.startswith("gpt-4") else "max_completion_tokens"
    kwargs = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        token_key: max_tokens,
        "temperature": temperature,
    }
    if token_key == "max_completion_tokens":
        kwargs["reasoning_effort"] = "none"
    return kwargs


def synthesise(
    client: OpenAI,
    query: str,
    results: list[dict],
    mode: str = "researcher",
    answer_format: str = "freeform",
    output_language: str = "English",
    model: str = "gpt-4o",
    room: str = "villaks",
) -> str:
    """
    Call GPT-4o with the retrieved evidence and return a synthesis.

    mode: "researcher" | "non_researcher"
    answer_format: "structured" | "freeform"
    """
    if not results:
        return NO_RESULTS_MESSAGE

    kwargs = _build_request(query, results, mode, answer_format, output_language, model, room)
    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content.strip()


def synthesise_stream(
    client: OpenAI,
    query: str,
    results: list[dict],
    mode: str = "researcher",
    answer_format: str = "freeform",
    output_language: str = "English",
    model: str = "gpt-4o",
    room: str = "villaks",
):
    """Same request as synthesise(), but yield the answer as text deltas as they arrive."""
    if not results:
        yield NO_RESULTS_MESSAGE
        return

    kwargs = _build_request(query, results, mode, answer_format, output_language, model, room)
    stream = client.chat.completions.create(**kwargs, stream=True)
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
