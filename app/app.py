"""
app.py — AP1 Evidence Synthesis Tool (Streamlit)

Ask contested scientific questions about salmon lice and wild salmonid mortality.
Retrieves from the curated AP1 corpus and returns a question-shaped evidence synthesis.
"""

import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from retrieval import load_corpus, reload_corpus, retrieve, build_debate_map
from synthesis import synthesise

# ── i18n helpers ──────────────────────────────────────────────────────────────

LANG_OPTIONS = ["en", "no"]


def tr(lang: str, en: str, no: str) -> str:
    return no if lang == "no" else en


EVIDENCE_DIRECTION_LABELS = {
    "en": {
        "supports_effect": "Supports effect",
        "weak_support": "Weak support",
        "mixed_within_study": "Mixed within study",
        "no_effect_detected": "No effect detected",
        "contradicts_effect": "Contradicts effect",
        "critiques_methodology": "Critiques methodology",
        "not_applicable": "Not applicable",
    },
    "no": {
        "supports_effect": "Støtter effekt",
        "weak_support": "Svak støtte",
        "mixed_within_study": "Blandet i studien",
        "no_effect_detected": "Ingen effekt påvist",
        "contradicts_effect": "Motstrider effekt",
        "critiques_methodology": "Kritiserer metode",
        "not_applicable": "Ikke relevant",
    },
}


# Evidence direction icons (used in source list + legend)
DIRECTION_COLOUR = {
    "supports_effect": "🟢",
    "weak_support": "🟡",
    "mixed_within_study": "🟡",
    "no_effect_detected": "⚪",
    "contradicts_effect": "🔴",
    "critiques_methodology": "🔵",
    "not_applicable": "⚪",
}

QUALITY_BADGE = {"strong": "●●●", "medium": "●●○", "weak": "●○○"}


def render_retrieved_sources_legend(lang: str) -> None:
    """Legend for icons shown on each retrieved source."""
    st.caption(tr(lang, "**Evidence direction**", "**Evidensretning**"))
    direction_legend = [
        ("🟢", tr(lang, "Supports effect", "Støtter effekt")),
        ("🟡", tr(lang, "Weak or mixed support", "Svak eller blandet støtte")),
        ("🔴", tr(lang, "Contradicts effect", "Motstrider effekt")),
        ("🔵", tr(lang, "Critiques methodology", "Kritiserer metode")),
        ("⚪", tr(lang, "No effect / not applicable", "Ingen effekt / ikke relevant")),
    ]
    cols = st.columns(len(direction_legend))
    for col, (icon, label) in zip(cols, direction_legend):
        col.markdown(f"{icon} {label}")
    st.caption(
        tr(
            lang,
            "**Quality:** ●●● strong · ●●○ medium · ●○○ weak",
            "**Kvalitet:** ●●● sterk · ●●○ middels · ●○○ svak",
        )
    )


# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AP1 Evidence Synthesis",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── API client ────────────────────────────────────────────────────────────────

def _openai_api_key() -> str:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if key:
        return key
    try:
        return str(st.secrets["OPENAI_API_KEY"]).strip()
    except (KeyError, FileNotFoundError, AttributeError, TypeError):
        return ""


def get_client() -> OpenAI | None:
    key = _openai_api_key()
    if not key:
        st.error(
            "OPENAI_API_KEY not set. Add it to .env (local) or Streamlit Cloud secrets."
        )
        return None
    return OpenAI(api_key=key)

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("AP1 Evidence Corpus")

    lang = st.radio(
        "Language",
        options=LANG_OPTIONS,
        format_func=lambda x: "English" if x == "en" else "Norsk",
        horizontal=True,
    )

    st.caption(
        tr(lang, "Salmon Lice & Wild Salmonid Mortality", "Lakselus og dødelighet hos vill laksefisk")
    )

    # ── User mode selector ────────────────────────────────────────────────
    st.subheader(tr(lang, "Audience", "Målgruppe"))
    mode = st.radio(
        tr(lang, "Choose your background", "Velg bakgrunn"),
        options=["researcher", "non_researcher"],
        format_func=lambda x: (
            tr(lang, "🔬 Researcher / Expert", "🔬 Forsker / fagperson")
            if x == "researcher"
            else tr(lang, " Interested non-specialist", " Interessert ikke-spesialist")
        ),
        help=(
            tr(
                lang,
                "**Researcher:** Technical language, full citations, quantitative results; answer shape follows your question.\n\n"
                "**Non-specialist:** Plain language, no jargon; structure adapted to what you asked.",
                "**Forsker:** Teknisk språk, fulle referanser, kvantitative resultater; svaret formes etter spørsmålet.\n\n"
                "**Ikke-spesialist:** Enkelt språk, ingen fagjargon; struktur tilpasset det du spør om.",
            )
        ),
    )

    if mode == "non_researcher":
        st.info(
            tr(
                lang,
                "You'll get plain-language answers that explain both what researchers agree on and where they genuinely disagree — without the technical jargon.",
                "Du får svar i enkelt språk som forklarer både hva forskere er enige om og hvor de faktisk er uenige — uten unødvendig fagjargon.",
            ),
            icon="🌊",
        )

    st.subheader(tr(lang, "Answer format", "Svarformat"))
    answer_format = st.radio(
        tr(lang, "How should the answer be organised?", "Hvordan skal svaret organiseres?"),
        options=["freeform", "structured"],
        format_func=lambda x: (
            tr(lang, "Free text — shaped by your question", "Fritekst — formes etter spørsmålet")
            if x == "freeform"
            else tr(lang, "Structured — fixed sections every time", "Strukturert — faste seksjoner hver gang")
        ),
        help=(
            tr(
                lang,
                "**Free text:** Headings and flow follow your question (good for exploration).\n\n"
                "**Structured:** Same section outline every time — comparable across queries "
                "(researcher: Main Finding, Supporting, Opposing, Uncertainties, Context, Confidence; "
                "non-specialist: five plain-language sections).",
                "**Fritekst:** Overskrifter og flyt følger spørsmålet (bra for utforsking).\n\n"
                "**Strukturert:** Samme disposisjon hver gang — lett å sammenligne mellom spørsmål "
                "(forsker: Hovedfunn, Støttende, Motstridende, Usikkerheter, Kontekst, Tillit; "
                "ikke-spesialist: fem enkle seksjoner).",
            )
        ),
    )

    st.divider()

    try:
        df = load_corpus()
        n_total = len(df)
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

    st.divider()
    st.subheader(tr(lang, "Papers in corpus", "Artikler i korpuset"))
    st.caption(tr(lang, f"{n_total} papers in database", f"{n_total} artikler i databasen"))

    if st.button(
        tr(lang, "Reload corpus from disk", "Last inn korpus på nytt"),
        help=tr(
            lang,
            "Use after running ingest.py if the paper count looks wrong.",
            "Bruk etter ingest.py hvis antall artikler ser feil ut.",
        ),
        use_container_width=True,
    ):
        df = reload_corpus()
        n_total = len(df)
        st.session_state["selected_labels"] = None
        st.session_state.pop("corpus_doc_count", None)
        st.rerun()

    # Build label → doc_id mapping, sorted by year then author
    doc_options = {}
    for _, row in df.sort_values(["year", "doc_id"]).iterrows():
        first_author = row["authors"].split(";")[0].split()[-1] if row["authors"] else "?"
        label = f"{first_author} {row['year']} — {row['title'][:55]}{'…' if len(row['title']) > 55 else ''}"
        doc_options[label] = row["doc_id"]

    all_labels = list(doc_options.keys())

    # If corpus grew (e.g. paper #16 added), re-select all when user previously had full set
    prev_count = st.session_state.get("corpus_doc_count")
    if prev_count is not None and n_total > prev_count:
        old_selected = st.session_state.get("selected_labels") or []
        if len(old_selected) >= prev_count:
            st.session_state["selected_labels"] = all_labels
    st.session_state["corpus_doc_count"] = n_total

    stored = st.session_state.get("selected_labels")
    if stored is not None:
        valid = [label for label in stored if label in doc_options]
        if len(valid) != len(stored):
            st.session_state["selected_labels"] = valid if valid else all_labels

    col_sel, col_clr = st.columns(2)
    if col_sel.button(tr(lang, "Select all", "Velg alle"), use_container_width=True):
        st.session_state["selected_labels"] = all_labels
    if col_clr.button(tr(lang, "Clear all", "Tøm"), use_container_width=True):
        st.session_state["selected_labels"] = []

    selected_labels = st.multiselect(
        tr(lang, "Include these papers", "Inkluder disse artiklene"),
        options=all_labels,
        default=st.session_state.get("selected_labels", all_labels),
        label_visibility="collapsed",
    )
    st.session_state["selected_labels"] = selected_labels
    selected_doc_ids = [doc_options[l] for l in selected_labels] if selected_labels else None

    if not selected_labels:
        st.warning(tr(lang, "No papers selected — select at least one.", "Ingen artikler valgt — velg minst én."))
    else:
        st.caption(
            tr(
                lang,
                f"{len(selected_labels)} / {n_total} papers active",
                f"{len(selected_labels)} / {n_total} aktive artikler",
            )
        )

    st.divider()

    top_k = st.slider(
        tr(lang, "Documents to retrieve", "Antall dokumenter å hente"),
        min_value=3,
        max_value=12,
        value=8,
    )

    st.divider()
    st.caption(
        tr(
            lang,
            "Corpus: [hakonbakke/ap1-curated-corpora](https://github.com/hakonbakke/ap1-curated-corpora)  \n"
            "Method: Honest Broker (Pielke 2007)  \n"
            "Funded by FHF / Havbruksløftet AP1",
            "Korpus: [hakonbakke/ap1-curated-corpora](https://github.com/hakonbakke/ap1-curated-corpora)  \n"
            "Metode: Honest Broker (Pielke 2007)  \n"
            "Finansiert av FHF / Havbruksløftet AP1",
        )
    )

# ── Main ─────────────────────────────────────────────────────────────────────

st.title(tr(lang, "AP1 Evidence Synthesis Tool", "AP1 evidenssyntese"))

if mode == "researcher":
    st.markdown(
        tr(
            lang,
            "Ask a contested scientific question about **salmon lice and wild salmonid mortality**. "
            "The tool retrieves from a curated corpus of peer-reviewed studies and returns a "
            "technical synthesis shaped to your question, preserving scientific disagreement.",
            "Still et omstridt, vitenskapelig spørsmål om **lakselus og dødelighet hos vill laksefisk**. "
            "Verktøyet henter fra et kuratert korpus av fagfellevurderte studier og returnerer en "
            "teknisk syntese tilpasset spørsmålet — uten å skjule uenighet i forskningen.",
        )
    )
else:
    st.markdown(
        tr(
            lang,
            "Ask a question about **salmon farming and wild fish** — in plain language. "
            "The tool searches the curated studies and explains what researchers have found, "
            "in a form that matches your question. No background knowledge needed.",
            "Still et spørsmål om **oppdrett og villfisk** — med enkelt språk. "
            "Verktøyet søker i de kuraterte studiene og forklarer hva forskningen viser, "
            "i en form som passer spørsmålet. Du trenger ingen forkunnskaper.",
        )
    )

EXAMPLE_QUESTIONS_RESEARCHER = {
    "en": [
        "Does lice-induced smolt mortality translate to reduced adult returns and impaired population viability?",
        "How robust is the Norwegian Traffic Light System as a regulatory framework?",
        "How can lice infestation levels be translated into mortality estimates, and how robust are the dose–response relationships?",
        "What is the evidence that salmon lice from farms cause population-level decline in wild salmon?",
        "Which studies disagree on whether lice is the main driver of Atlantic salmon population collapse?",
    ],
    "no": [
        "Gir luseindusert smoltdødelighet færre voksenlaks i retur og svekket bestandslevedyktighet?",
        "Hvor robust er det norske Trafikklyssystemet som reguleringsrammeverk?",
        "Hvordan oversettes luseinfestasjon til dødelighet, og hvor robuste er dose–respons-forholdene?",
        "Hva er evidensen for at lakselus fra oppdrett gir bestandsnedgang hos villaks?",
        "Hvilke studier er uenige om lakselus er hoveddriveren bak bestandskollaps i Nord-Atlanteren?",
    ],
}

EXAMPLE_QUESTIONS_NON_RESEARCHER = {
    "en": [
        "Do salmon farms harm wild salmon?",
        "Can we trust the system Norway uses to regulate salmon farming?",
        "How do scientists measure whether salmon lice are killing wild fish?",
        "Why do some researchers say lice from farms are dangerous while others disagree?",
        "Is it proven that salmon farming causes wild salmon populations to collapse?",
    ],
    "no": [
        "Skader lakseoppdrett villaks?",
        "Kan vi stole på systemet Norge bruker for å regulere oppdrett?",
        "Hvordan måler forskere om lakselus dreper villfisk?",
        "Hvorfor mener noen forskere at lus fra oppdrett er farlig, mens andre er uenige?",
        "Er det bevist at oppdrett fører til bestandskollaps hos villaks?",
    ],
}

examples = (EXAMPLE_QUESTIONS_RESEARCHER if mode == "researcher" else EXAMPLE_QUESTIONS_NON_RESEARCHER)[lang]

with st.expander(tr(lang, "Example questions — click to use", "Eksempelspørsmål — klikk for å bruke")):
    for i, eq in enumerate(examples):
        col_q, col_use = st.columns([8, 1])
        with col_q:
            st.markdown(f"- {eq}")
        with col_use:
            if st.button(tr(lang, "Use", "Bruk"), key=f"eq_use_{i}_{lang}_{mode}"):
                st.session_state["user_query"] = eq
                st.rerun()
        st.caption("")

query = st.text_area(
    tr(lang, "Your question", "Spørsmålet ditt"),
    value=st.session_state.get("user_query", ""),
    placeholder=tr(
        lang,
        "e.g. How sensitive are Traffic Light System classifications to model assumptions and calibration data?",
        "f.eks. Hvor sensitive er klassifiseringene i Trafikklyssystemet for modellantakelser og kalibreringsdata?",
    ),
    height=90,
)

col1, col2 = st.columns([1, 5])
with col1:
    run = st.button(tr(lang, "Synthesise", "Syntetiser"), type="primary", use_container_width=True)

if run and query.strip():
    if not selected_labels:
        st.error(tr(lang, "Select at least one paper in the sidebar before querying.", "Velg minst én artikkel i sidepanelet før du spør."))
        st.stop()

    client = get_client()
    if not client:
        st.stop()

    with st.spinner(tr(lang, "Retrieving relevant documents...", "Henter relevante dokumenter...")):
        results = retrieve(
            client,
            query.strip(),
            top_k=top_k,
            selected_doc_ids=selected_doc_ids,
        )

    if not results:
        st.warning(tr(lang, "No relevant documents found for this query.", "Ingen relevante dokumenter funnet for dette spørsmålet."))
        st.stop()

    with st.spinner(tr(lang, "Synthesising evidence...", "Syntetiserer evidens...")):
        output_language = "Norwegian (Bokmål)" if lang == "no" else "English"
        synthesis_text = synthesise(
            client,
            query.strip(),
            results,
            mode=mode,
            answer_format=answer_format,
            output_language=output_language,
        )

    # ── Output ────────────────────────────────────────────────────────────────

    st.divider()
    st.subheader(tr(lang, "Synthesis", "Syntese"))
    st.markdown(synthesis_text)

    st.divider()

    # Source panel
    st.subheader(tr(lang, f"Retrieved sources ({len(results)})", f"Hentede kilder ({len(results)})"))
    render_retrieved_sources_legend(lang)

    for r in results:
        icon = DIRECTION_COLOUR.get(r["evidence_direction"], "⚪")
        qual = QUALITY_BADGE.get(r["quality_signal"], "?")
        doi_url = r["url"] or (f"https://doi.org/{r['doi']}" if r["doi"] else "")
        link = f"[DOI ↗]({doi_url})" if doi_url else ""

        with st.expander(
            f"{icon} **{r['authors'].split(';')[0].split()[-1]} {r['year']}** — "
            f"{r['title'][:80]}{'...' if len(r['title']) > 80 else ''} {link}"
        ):
            col_a, col_b, col_c = st.columns(3)
            dir_label = EVIDENCE_DIRECTION_LABELS.get(lang, {}).get(
                r["evidence_direction"], r["evidence_direction"].replace("_", " ")
            )
            col_a.metric(tr(lang, "Evidence direction", "Evidensretning"), dir_label)
            col_b.metric(
                tr(lang, "Quality", "Kvalitet"),
                f"{qual} {r['quality_signal']}",
            )
            col_c.metric(
                tr(lang, "Consensus", "Konsensus"),
                r["consensus_signal"].replace("_", " ") if r["consensus_signal"] else "—",
            )

            if r["key_claims"]:
                st.markdown(tr(lang, "**Key claims:**", "**Hovedpåstander:**"))
                for claim in r["key_claims"]:
                    if claim and str(claim).strip():
                        st.markdown(f"- {claim}")

            if r.get("summary_text"):
                with st.expander(tr(lang, "Evidence brief", "Evidensnotat"), expanded=False):
                    st.markdown(r["summary_text"][:8000])
            elif r["rag_summary"]:
                st.markdown(tr(lang, "**Summary:**", "**Oppsummering:**"))
                st.markdown(r["rag_summary"])

            tags = r["priority_questions"]
            if tags:
                st.caption(tr(lang, "Priority questions: ", "Prioriterte spørsmål: ") + " · ".join(tags))

            if r["related_contrasting"]:
                st.caption(tr(lang, "Contrasts with: ", "Kontrasterer med: ") + ", ".join(r["related_contrasting"]))

            score_pct = int(r["score"] * 100)
            st.caption(tr(lang, f"Similarity to query: {score_pct}%", f"Likhet med spørsmål: {score_pct}%"))

    # Debate map
    try:
        df_all = load_corpus()
        edges = build_debate_map(results, df_all)
        if edges:
            st.divider()
            st.subheader(tr(lang, "Debate relationships", "Debattforhold"))
            for e in edges:
                rel_label = (
                    tr(lang, "↔ contradicts", "↔ motsier")
                    if e["relation"] == "contradicts"
                    else tr(lang, "↩ replies to", "↩ svarer på")
                )
                from_short = e["from_title"][:50] + "..." if len(e["from_title"]) > 50 else e["from_title"]
                to_short = e["to_title"][:50] + "..." if len(e["to_title"]) > 50 else e["to_title"]
                st.markdown(f"**{from_short}** {rel_label} **{to_short}**")
    except Exception:
        pass

elif run and not query.strip():
    st.warning(tr(lang, "Please enter a question.", "Skriv inn et spørsmål."))
