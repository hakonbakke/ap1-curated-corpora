"""
app.py — AP1 Evidence Synthesis Tool (Streamlit)

Ask contested scientific questions about salmon lice and wild salmonid mortality.
Retrieves from the curated AP1 corpus and returns a structured evidence synthesis.
"""

import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from retrieval import load_corpus, retrieve, build_debate_map
from synthesis import synthesise

# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AP1 Evidence Synthesis",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── API client ────────────────────────────────────────────────────────────────

def get_client() -> OpenAI | None:
    key = os.environ.get("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", "")
    if not key:
        st.error("OPENAI_API_KEY not set. Add it to .env (local) or Streamlit Cloud secrets.")
        return None
    return OpenAI(api_key=key)

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("AP1 Evidence Corpus")
    st.caption("Salmon Lice & Wild Salmonid Mortality")

    # ── User mode selector ────────────────────────────────────────────────
    st.subheader("Who are you?")
    mode = st.radio(
        "Choose your background",
        options=["researcher", "non_researcher"],
        format_func=lambda x: "🔬 Researcher / Expert" if x == "researcher" else "🌊 Interested non-specialist",
        help=(
            "**Researcher:** Technical language, full citations, quantitative results, "
            "six-section structured synthesis.\n\n"
            "**Non-specialist:** Plain language, no jargon, analogies, "
            "accessible to anyone curious about the topic."
        ),
    )

    if mode == "non_researcher":
        st.info(
            "You'll get plain-language answers that explain both what researchers "
            "agree on and where they genuinely disagree — without the technical jargon.",
            icon="🌊",
        )

    st.divider()

    try:
        df = load_corpus()
        n_total = len(df)
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

    st.divider()
    st.subheader("Papers in corpus")

    # Build label → doc_id mapping, sorted by year then author
    doc_options = {}
    for _, row in df.sort_values(["year", "doc_id"]).iterrows():
        first_author = row["authors"].split(";")[0].split()[-1] if row["authors"] else "?"
        label = f"{first_author} {row['year']} — {row['title'][:55]}{'…' if len(row['title']) > 55 else ''}"
        doc_options[label] = row["doc_id"]

    all_labels = list(doc_options.keys())

    col_sel, col_clr = st.columns(2)
    if col_sel.button("Select all", use_container_width=True):
        st.session_state["selected_labels"] = all_labels
    if col_clr.button("Clear all", use_container_width=True):
        st.session_state["selected_labels"] = []

    selected_labels = st.multiselect(
        "Include these papers",
        options=all_labels,
        default=st.session_state.get("selected_labels", all_labels),
        label_visibility="collapsed",
    )
    st.session_state["selected_labels"] = selected_labels
    selected_doc_ids = [doc_options[l] for l in selected_labels] if selected_labels else None

    if not selected_labels:
        st.warning("No papers selected — select at least one.")
    else:
        st.caption(f"{len(selected_labels)} / {n_total} papers active")

    st.divider()
    st.subheader("Filters (optional)")

    filter_q = st.multiselect(
        "Priority questions",
        ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10"],
        default=[],
        help="Limit retrieval to documents tagged with these questions.",
    )

    filter_dir = st.multiselect(
        "Evidence direction",
        ["supports_effect", "weak_support", "mixed_within_study",
         "no_effect_detected", "contradicts_effect", "critiques_methodology"],
        default=[],
        help="Filter by how the document relates to lice-effect evidence.",
    )

    filter_qual = st.multiselect(
        "Minimum quality",
        ["strong", "medium", "weak"],
        default=[],
        help="Filter by curator quality assessment.",
    )

    top_k = st.slider("Documents to retrieve", min_value=3, max_value=12, value=8)

    st.divider()
    st.caption(
        "Corpus: [hakonbakke/ap1-curated-corpora](https://github.com/hakonbakke/ap1-curated-corpora)  \n"
        "Method: Honest Broker (Pielke 2007)  \n"
        "Funded by FHF / Havbruksløftet AP1"
    )

# ── Main ─────────────────────────────────────────────────────────────────────

st.title("AP1 Evidence Synthesis Tool")

if mode == "researcher":
    st.markdown(
        "Ask a contested scientific question about **salmon lice and wild salmonid mortality**. "
        "The tool retrieves from a curated corpus of 15 peer-reviewed studies and returns a "
        "structured technical synthesis that preserves scientific disagreement."
    )
else:
    st.markdown(
        "Ask a question about **salmon farming and wild fish** — in plain language. "
        "The tool searches 15 scientific studies and explains what researchers have found, "
        "where they agree, and where they genuinely disagree. No background knowledge needed."
    )

# Example questions — adapted to mode
with st.expander("Example questions"):
    if mode == "researcher":
        st.markdown("""
- Does lice-induced smolt mortality translate to reduced adult returns and impaired population viability?
- How robust is the Norwegian Traffic Light System as a regulatory framework?
- How can lice infestation levels be translated into mortality estimates, and how robust are the dose–response relationships?
- What is the evidence that salmon lice from farms cause population-level decline in wild salmon?
- Which studies disagree on whether lice is the main driver of Atlantic salmon population collapse?
""")
    else:
        st.markdown("""
- Do salmon farms harm wild salmon?
- Can we trust the system Norway uses to regulate salmon farming?
- How do scientists measure whether salmon lice are killing wild fish?
- Why do some researchers say lice from farms are dangerous while others disagree?
- Is it proven that salmon farming causes wild salmon populations to collapse?
""")

query = st.text_area(
    "Your question",
    placeholder="e.g. How sensitive are Traffic Light System classifications to model assumptions and calibration data?",
    height=90,
)

col1, col2 = st.columns([1, 5])
with col1:
    run = st.button("Synthesise", type="primary", use_container_width=True)

if run and query.strip():
    if not selected_labels:
        st.error("Select at least one paper in the sidebar before querying.")
        st.stop()

    client = get_client()
    if not client:
        st.stop()

    with st.spinner("Retrieving relevant documents..."):
        results = retrieve(
            client,
            query.strip(),
            top_k=top_k,
            filter_priority_questions=filter_q or None,
            filter_evidence_direction=filter_dir or None,
            filter_quality=filter_qual or None,
            selected_doc_ids=selected_doc_ids,
        )

    if not results:
        st.warning("No documents matched your filters. Try removing some filters.")
        st.stop()

    with st.spinner("Synthesising evidence..."):
        synthesis_text = synthesise(client, query.strip(), results, mode=mode)

    # ── Output ────────────────────────────────────────────────────────────────

    st.divider()
    if mode == "researcher":
        st.subheader("Evidence Synthesis")
    else:
        st.subheader("What the research says")
    st.markdown(synthesis_text)

    st.divider()

    # Source panel
    st.subheader(f"Retrieved sources ({len(results)})")

    direction_colour = {
        "supports_effect": "🟢",
        "weak_support": "🟡",
        "mixed_within_study": "🟡",
        "no_effect_detected": "⚪",
        "contradicts_effect": "🔴",
        "critiques_methodology": "🔵",
        "not_applicable": "⚪",
    }
    quality_badge = {"strong": "●●●", "medium": "●●○", "weak": "●○○"}

    for r in results:
        icon = direction_colour.get(r["evidence_direction"], "⚪")
        qual = quality_badge.get(r["quality_signal"], "?")
        doi_url = r["url"] or (f"https://doi.org/{r['doi']}" if r["doi"] else "")
        link = f"[DOI ↗]({doi_url})" if doi_url else ""

        with st.expander(
            f"{icon} **{r['authors'].split(';')[0].split()[-1]} {r['year']}** — "
            f"{r['title'][:80]}{'...' if len(r['title']) > 80 else ''} {link}"
        ):
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Evidence direction", r["evidence_direction"].replace("_", " "))
            col_b.metric("Quality", f"{qual} {r['quality_signal']}")
            col_c.metric("Consensus", r["consensus_signal"].replace("_", " ") if r["consensus_signal"] else "—")

            if r["key_claims"]:
                st.markdown("**Key claims:**")
                for claim in r["key_claims"]:
                    if claim and str(claim).strip():
                        st.markdown(f"- {claim}")

            if r["rag_summary"]:
                st.markdown("**Summary:**")
                st.markdown(r["rag_summary"])

            tags = r["priority_questions"]
            if tags:
                st.caption("Priority questions: " + " · ".join(tags))

            if r["related_contrasting"]:
                st.caption("Contrasts with: " + ", ".join(r["related_contrasting"]))

            score_pct = int(r["score"] * 100)
            st.caption(f"Retrieval relevance: {score_pct}%")

    # Debate map
    try:
        df_all = load_corpus()
        edges = build_debate_map(results, df_all)
        if edges:
            st.divider()
            st.subheader("Debate relationships")
            for e in edges:
                rel_label = "↔ contradicts" if e["relation"] == "contradicts" else "↩ replies to"
                from_short = e["from_title"][:50] + "..." if len(e["from_title"]) > 50 else e["from_title"]
                to_short = e["to_title"][:50] + "..." if len(e["to_title"]) > 50 else e["to_title"]
                st.markdown(f"**{from_short}** {rel_label} **{to_short}**")
    except Exception:
        pass

elif run and not query.strip():
    st.warning("Please enter a question.")
