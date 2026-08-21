"""
Evidensrom: Lakselus og dødelighet hos ville laksefisk

Orientering (A til C) + live Ask (D) mot det kuraterte korpuset.
Layout speiler mockup/tema-villaks.html. All RAG-funksjonalitet er bevart.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

APP_DIR = Path(__file__).resolve().parent.parent
REPO = APP_DIR.parent
sys.path.insert(0, str(APP_DIR))
load_dotenv(REPO / ".env", override=True)

from retrieval import (
    load_corpus,
    reload_corpus,
    retrieve_routed,
    build_debate_map,
    is_out_of_scope,
    best_retrieval_score,
)
from synthesis import synthesise
from ui import brand_header, inject_css, paper_chips, section_header

st.set_page_config(
    page_title="Lakselus og villaks · Evidensrom",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

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
    "no_significant_effect": "⚪",  # legacy alias, taxonomy: no_effect_detected
    "contradicts_effect": "🔴",
    "critiques_methodology": "🔵",
    "not_applicable": "⚪",
}

CURATOR_STATUS_LABELS = {
    "en": {
        "ai_verified": "Metadata checked (AI)",
        "ai_draft": "Metadata draft (AI)",
        "expert_approved": "Expert-approved",
        "pending": "Metadata draft (legacy)",
        "reviewed": "Reviewed (legacy)",
        "approved": "Approved (legacy)",
    },
    "no": {
        "ai_verified": "Metadata sjekket (AI)",
        "ai_draft": "Metadata-utkast (AI)",
        "expert_approved": "Ekspertgodkjent",
        "pending": "Metadata-utkast (eldre)",
        "reviewed": "Gjennomgått (eldre)",
        "approved": "Godkjent (eldre)",
    },
}

CONTROVERSY_ROLE_LABELS = {
    "en": {
        "foundational": "foundational in the debate",
        "supportive": "supportive in the debate",
        "critical": "critical in the debate",
        "rebuttal": "a rebuttal",
        "bridge_between_positions": "a bridge between positions",
        "peripheral": "peripheral",
        "not_applicable": "",
    },
    "no": {
        "foundational": "grunnlag i debatten",
        "supportive": "støttende i debatten",
        "critical": "kritisk i debatten",
        "rebuttal": "replik",
        "bridge_between_positions": "bro mellom posisjoner",
        "peripheral": "perifer",
        "not_applicable": "",
    },
}

QUALITY_BADGE = {"strong": "●●●", "medium": "●●○", "weak": "●○○"}
CLAIMS_VISIBLE = 3


def _last_name(authors: str) -> str:
    if not authors:
        return "?"
    first = str(authors).split(";")[0].strip()
    parts = first.split()
    return parts[-1] if parts else "?"


def short_cite(authors: str, year) -> str:
    return f"{_last_name(authors)} {year}".strip()


def first_sentence(text: str, max_chars: int = 320) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    cut = text
    for sep in (". ", ".\n"):
        i = text.find(sep)
        if i > 40:
            cut = text[: i + 1]
            break
    if len(cut) > max_chars:
        cut = cut[: max_chars].rstrip() + "…"
    return cut


def source_role_line(r: dict, lang: str) -> str:
    role = (r.get("controversy_role") or "").strip()
    role_label = CONTROVERSY_ROLE_LABELS.get(lang, {}).get(role, "")
    because = first_sentence(str(r.get("included_because") or ""))
    parts = []
    if role_label:
        parts.append(
            tr(lang, f"Role in the corpus: {role_label}.", f"Rolle i korpuset: {role_label}.")
        )
    if because:
        parts.append(because)
    return " ".join(parts)


def citation_index(df) -> dict[str, str]:
    index: dict[str, str] = {}
    for _, row in df.iterrows():
        index[str(row["doc_id"])] = short_cite(row.get("authors", ""), row.get("year", ""))
    return index


def human_contrasts(doc_ids: list, cite_by_id: dict[str, str]) -> str:
    names = []
    for did in doc_ids or []:
        names.append(cite_by_id.get(str(did), str(did)))
    return ", ".join(names)


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


# ── Sidebar (kontrollpanel for D) ─────────────────────────────────────────────

with st.sidebar:
    st.title("Havbruksløftets Evidensrom")
    st.page_link("app.py", label="← Alle evidensrom", icon="🏠")

    lang = st.radio(
        "Language",
        options=LANG_OPTIONS,
        format_func=lambda x: "English" if x == "en" else "Norsk",
        horizontal=True,
    )

    st.caption(
        tr(lang, "Salmon lice & wild salmonid mortality", "Lakselus og dødelighet hos ville laksefisk")
    )

    st.subheader(tr(lang, "Audience", "Målgruppe"))
    mode = st.radio(
        tr(lang, "Choose your background", "Velg bakgrunn"),
        options=["researcher", "non_researcher"],
        format_func=lambda x: (
            tr(lang, "Researcher / expert", "Forsker / fagperson")
            if x == "researcher"
            else tr(lang, "Interested non-specialist", "Interessert ikke-spesialist")
        ),
        help=(
            tr(
                lang,
                "**Researcher:** Technical language, full citations and quantitative results. "
                "The answer follows the shape of your question.\n\n"
                "**Non-specialist:** Plain language without unnecessary jargon. "
                "The structure is adapted to what you asked.",
                "**Forsker:** Teknisk språk, fulle referanser og kvantitative resultater. "
                "Svaret formes etter spørsmålet ditt.\n\n"
                "**Ikke-spesialist:** Enkelt språk uten unødvendig fagjargon. "
                "Strukturen tilpasses det du spør om.",
            )
        ),
    )

    if mode == "non_researcher":
        st.info(
            tr(
                lang,
                "Answers use plain language. They explain both what researchers agree on "
                "and where they still disagree.",
                "Svarene bruker enkelt språk. De forklarer både hva forskere er enige om "
                "og hvor de fortsatt er uenige.",
            ),
            icon="🌊",
        )

    # Svarformat er låst til fritekst (formes etter spørsmålet).
    answer_format = "freeform"

    st.divider()

    try:
        df = load_corpus()
        n_total = len(df)
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

    st.subheader(tr(lang, "Papers in corpus", "Artikler i korpuset"))
    st.caption(tr(lang, f"{n_total} papers in database", f"{n_total} artikler i databasen"))

    if st.button(
        tr(lang, "Reload corpus from disk", "Last inn korpus på nytt"),
        help=tr(
            lang,
            "Use after running ingest.py if the paper count looks wrong.",
            "Bruk etter ingest.py hvis antall artikler ser feil ut.",
        ),
        width="stretch",
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
        label = f"{first_author} {row['year']} · {row['title'][:55]}{'…' if len(row['title']) > 55 else ''}"
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
    if col_sel.button(tr(lang, "Select all", "Velg alle"), width="stretch"):
        st.session_state["selected_labels"] = all_labels
    if col_clr.button(tr(lang, "Clear all", "Tøm"), width="stretch"):
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
        st.warning(tr(lang, "No papers selected, select at least one.", "Ingen artikler valgt, velg minst én."))
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
        help=tr(
            lang,
            "Number of papers ranked by similarity. Up to 3 contrasting or companion papers may be added on top.",
            "Antall artikler rangert etter likhet. Inntil 3 kontrasterende eller tilhørende artikler kan legges til i tillegg.",
        ),
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

# ── Fault lines (C) ───────────────────────────────────────────────────────────

FAULTS = {
    "no": [
        (
            "1. Opphav: forsvinner «oppdrettslusa» hvis oppdrettet forsvinner?",
            "Norske modeller antar i stor grad at oppdrettsoriginert lus dominerer infestasjonspresset "
            "på villfisk. To BC-studier (2025) rapporterer at lus på juvenil vill stillehavslaks ble "
            "værende uendret, eller høyere, etter nesten total fjerning av lokal oppdrettsbiomasse. "
            "Overførbarhet til Norge er omstridt (andre arter, *Caligus clemensi* viktig i BC).",
            "Hva skjedde med lus på villaks etter at oppdrett ble fjernet i British Columbia, og er det overførbart til Norge?",
        ),
        (
            "2. Kalibrering: er dødelighetsmodellen justert på riktige data?",
            "Stige og medforfattere mener estimatene er svært følsomme for kalibreringskilde "
            "(trål versus sentinel), og at kalibrering kan kompensere for skjevheter. "
            "Van Nes og medforfattere peker på systematisk overestimering via migrasjonstid, "
            "lusebiologi, kalibrering og terskler, og kritiserer også kalibreringsdataene selv.",
            "Hva er Van Nes et al. og Stige et al. egentlig uenige om når det gjelder kalibrering av lusemodeller?",
        ),
        (
            "3. Treffsikkerhet: treffer modellene det som observeres?",
            "Johnsen (2021) beskriver en operativ modell for virtuell postsmolt (VPS) som brukes for "
            "mange elver. Modellen er kalibrert mot lus talt på trålfanget postsmolt. "
            "Jansen, Gjerde og senere Gjerde (2025) rapporterer at VPS overestimerer lusnivåene "
            "sammenlignet med trålobservasjoner i 26 av 27 kombinasjoner av produksjonsområde og år. "
            "De finner også at en annen modellstørrelse, predikert gjennomsnittlig lusetetthet (PMLD), "
            "har svært svak evne til å forutsi det som måles på villfisk.",
            "Hvor godt treffer de operative lusemodellene det som faktisk måles på villfisk?",
        ),
        (
            "4. Fra smolt til innsig: blir det færre voksne?",
            "Jansen 2025 finner signifikant negativ PIM→1SW i 104 elver, men PIM er ikke den "
            "dominerende kovariaten. Dadswell, Jonsson og Gillson legger mer vekt på andre marine "
            "drivere. Om dødeligheten er additiv eller kompensatorisk er ikke avgjort.",
            "Gir luseindusert smoltdødelighet færre voksne tilbake, og hvordan står det mot andre dødsårsaker i havet?",
        ),
        (
            "5. Terskler: holder lab i felt?",
            "Fjelldal og Bøhn knytter lab- og feltfunn til skade og lav overlevelse ved høyt press. "
            "Van Nes utfordrer ekstrapolering. Hawley (sjøørret) viser stor heterogenitet mellom "
            "populasjoner. Terskler er ikke automatisk utbyttbare mellom arter (Dawson).",
            "Ved hvilke lusenivåer dør postsmolt faktisk, og hvor godt er den terskelen etablert fra lab til felt?",
        ),
    ],
    "en": [
        (
            "1. Origin: do farm lice vanish if farms vanish?",
            "Norwegian models largely assume farm-origin lice dominate infestation pressure on wild fish. "
            "Two BC studies (2025) report lice on juvenile wild Pacific salmon unchanged, or higher, "
            "after near-total removal of local farm biomass. Transferability to Norway is contested "
            "(different species, *Caligus clemensi* important in BC).",
            "Did sea lice on wild Pacific salmon decline after aquaculture was removed in British Columbia?",
        ),
        (
            "2. Calibration: is the mortality model tuned on the right data?",
            "Stige and colleagues argue that estimates are highly sensitive to calibration source "
            "(trawl versus sentinel), and that calibration can compensate for bias. "
            "Van Nes and colleagues point to systematic overestimation via migration time, lice biology, "
            "calibration and thresholds, and also criticise the calibration data themselves.",
            "How sensitive are Traffic Light System classifications to model assumptions and calibration data?",
        ),
        (
            "3. Fit: do models match what is observed?",
            "Johnsen (2021) describes an operational virtual post-smolt (VPS) model used for many "
            "rivers. The model is calibrated against lice counted on trawl-caught post-smolts. "
            "Jansen, Gjerde and later Gjerde (2025) report that VPS overestimates lice levels "
            "compared with trawl observations in 26 of 27 production-area and year combinations. "
            "They also find that another modelled quantity, predicted mean lice density (PMLD), "
            "has very weak power to predict what is measured on wild fish.",
            "Does the virtual post-smolt model overestimate lice-induced mortality compared with trawl observations?",
        ),
        (
            "4. Smolt to returns: fewer adults?",
            "Jansen 2025 finds a significant negative PIM→1SW relationship in 104 rivers, but PIM is "
            "not the dominant covariate. Dadswell, Jonsson and Gillson put more weight on other marine "
            "drivers. Whether mortality is additive or compensatory remains unresolved.",
            "What evidence links lice-induced mortality to reduced adult returns?",
        ),
        (
            "5. Thresholds: do lab values hold in the field?",
            "Fjelldal and Bøhn link lab and field findings to harm and low survival under high pressure. "
            "Van Nes challenges extrapolation. Hawley (sea trout) shows large heterogeneity between "
            "populations. Thresholds are not automatically interchangeable across species (Dawson).",
            "Can laboratory lice mortality thresholds for salmon be transferred to sea trout in the field?",
        ),
    ],
}

# Korpus-ID-er per skillelinje (samme på tvers av språk, hentet fra mockupen).
FAULT_PAPERS = [
    [
        "2025_dao_jones-broughton-lice-unchanged",
        "2025_jfd_jones-pacific-lice-cessation-bc",
        "2025_scientificdata_bc-sealice-dataset-2001-2023",
    ],
    [
        "2022_aei_stige-model-sensitivity-calibration",
        "2024_raq_vannes-critical-review-tls",
        "2025_raq_stige-comment-vannes",
        "2025_raq_vannes-response-to-stige",
    ],
    [
        "2021_icesjms_johnsen-vps-mortality-norway",
        "2021_icesjms_jansen-comment-vps-mortality",
        "2025_aquaculture_gjerde-seatrout-lice-prediction",
    ],
    [
        "2025_jae_jansen-lice-effects-returns",
        "2021_rfsa_dadswell-atlantic-salmon-collapse",
        "2016_jfb_jonsson-environmental-change-salmon",
        "2022_rfbf_gillson-marine-stressors-salmon",
    ],
    [
        "2020_conphys_fjelldal-lice-osmoregulation-salmon",
        "2020_jae_bohn-timing-survival-postsmolts",
        "2024_raq_vannes-critical-review-tls",
        "2024_ecosphere_hawley-anadromy-lice-mortality-trout",
        "1997_icesjms_dawson-seatrout-salmon-susceptibility",
    ],
]

# ── Brand-topplinje + breadcrumb ──────────────────────────────────────────────

brand_header(tr(lang, "Evidence room · salmon lice and wild salmon", "Evidensrom · lakselus og villaks"))

# ── Hero ──────────────────────────────────────────────────────────────────────

try:
    year_min = int(df["year"].min())
    year_max = int(df["year"].max())
    span = f"{year_min}-{year_max}"
except Exception:
    span = "1997-2026"

hero_left, hero_right = st.columns([1.5, 0.9])
with hero_left:
    st.markdown(
        tr(
            lang,
            '<h1 class="hl-h1">Salmon lice and wild salmonid mortality</h1>'
            '<p class="hl-lede">Wild salmon die for many reasons. The core question here is how much '
            'farm-origin salmon lice contribute. This room maps what academic publications say, '
            'where they disagree, and where the data gaps are. The page then moves through the '
            'regulatory framework, a disagreement map and Ask.</p>',
            '<h1 class="hl-h1">Lakselus og dødelighet hos ville laksefisk</h1>'
            '<p class="hl-lede">Villaks dør av mange årsaker. Kjernespørsmålet her er hvor mye lakselus '
            'fra oppdrett bidrar. Her kartlegges hva akademiske publikasjoner sier, hvor de er uenige, '
            'og hvor datahullene er. Deretter følger norsk rammeverk, et uenighetskart og Ask.</p>',
        ),
        unsafe_allow_html=True,
    )
with hero_right:
    with st.container(border=True):
        st.markdown(
            tr(
                lang,
                f"""
<div class="hl-stats">
  <div class="hl-stat"><strong>{n_total}</strong><span>papers in corpus</span></div>
  <div class="hl-stat"><strong>{span}</strong><span>time span</span></div>
  <div class="hl-stat"><strong>{len(FAULTS['en'])}</strong><span>open dividing lines</span></div>
  <div class="hl-stat"><strong>07.08</strong><span>last reviewed</span></div>
</div>
""",
                f"""
<div class="hl-stats">
  <div class="hl-stat"><strong>{n_total}</strong><span>artikler i korpuset</span></div>
  <div class="hl-stat"><strong>{span}</strong><span>tidsrom</span></div>
  <div class="hl-stat"><strong>{len(FAULTS['no'])}</strong><span>åpne skillelinjer</span></div>
  <div class="hl-stat"><strong>07.08</strong><span>sist gjennomgått</span></div>
</div>
""",
            ),
            unsafe_allow_html=True,
        )

st.write("")

# ── A: Introduksjon ───────────────────────────────────────────────────────────

section_header(
    tr(lang, "A · Introduction", "A · Introduksjon"),
    tr(lang, "Editorial overview", "Redaksjonell oversikt"),
)
with st.container(border=True):
    col_a, col_fig = st.columns([1.35, 1])
    with col_a:
        st.markdown(
            tr(
                lang,
                "Wild salmonids die from climate and temperature, food, predation, disease, fishing, "
                "river interventions, and parasites such as salmon lice. The narrower question here is "
                "**what share of wild salmon mortality can reasonably be attributed to farm-origin lice**, "
                "and how sure are we?",
                "Ville laksefisk dør av mange årsaker: klima og temperatur, næring, predasjon, sykdom, "
                "fiske, vassdragsinngrep, og parasitter som lakselus. Temaet her er det snevrere "
                "spørsmålet: **hvor stor andel av dødeligheten hos villaks kan rimelig tilskrives "
                "lakselus fra oppdrett**, og hvor sikre er vi på det?",
            )
        )
        st.markdown(
            tr(
                lang,
                "Farming can raise local lice reproduction. The larvae drift with the current and may "
                "meet out-migrating smolts. Harm depends on overlap in time and space. This corpus shows "
                "both what is supported and where models, observations and interpretations diverge.",
                "Oppdrett kan heve lokal lusereproduksjon. Larvene driver med strømmen og kan møte "
                "utvandrende smolt. Skaden avgjøres av overlapping i tid og rom. Korpuset synliggjør "
                "både det vi har støtte for, og der modellene, observasjonene og tolkningene divergerer.",
            )
        )
        with st.expander(
            tr(lang, "Read more: mortality picture and knowledge gaps", "Les mer om dødelighetsbildet og kunnskapshull")
        ):
            st.markdown(
                tr(
                    lang,
                    """
Salmon lice (*Lepeophtheirus salmonis*) are a natural marine parasite. At high densities they damage
skin and salt balance, especially in out-migrating smolts. When many hosts are held together in pens,
local larval production can rise above natural background.

**Typically well supported.** Lice can harm and kill individuals under high pressure.
Farming can increase local infestation pressure. Norwegian management models turn this into
estimated smolt mortality used in the traffic-light system.

**More uncertain.** How large a share of lice on wild fish actually comes from farms.
How well models match observations. Whether smolt mortality becomes fewer adult returns
(additive versus compensatory). How lice stand against other marine mortality causes.

**Recurring knowledge gaps.** Direct observation of migration timing and route.
Field validation of dose to response outside the lab. Calibration that does not hang on
the choice between trawl and sentinel cages. Sea trout is often used as a sentinel, but
thresholds are not automatically transferable to salmon.
""",
                    """
Lakselus (*Lepeophtheirus salmonis*) er en naturlig marin parasitt. Ved høye tettheter skader den hud
og saltbalanse, særlig hos den utvandrende smolten. Når mange verter holdes samlet i merder, kan
lokal larveproduksjon stige over naturlig bakgrunn.

**Typisk god støtte.** Lus kan skade og drepe individuelt under høyt trykk.
Oppdrett kan øke lokal infestasjonspress. Norske forvaltningsmodeller omsetter dette til
estimert smoltdødelighet brukt i trafikklyssystemet.

**Mer usikkert.** Hvor stor andel av lusa på villfisk som faktisk kommer fra oppdrett.
Hvor godt modellene treffer observasjoner. Om smoltdødelighet slår ut i færre voksne tilbake
(additiv versus kompensatorisk). Hvordan lus står mot andre marine dødsårsaker.

**Kunnskapshull.** Direkte observasjon av migrasjonstid og rute.
Feltvalidering av dose til respons utenfor laboratoriet. Kalibrering som ikke henger på
valget mellom trål og sentinelbur. Sjøørret brukes ofte som sentinel, men terskler er ikke
automatisk overførbare til laks.
""",
                )
            )
    with col_fig:
        fig_smolt = REPO / "mockup" / "figur-smolt-lus.png"
        if fig_smolt.exists():
            st.image(
                str(fig_smolt),
                width="stretch",
                caption=tr(
                    lang,
                    "One mechanism, not the whole mortality picture (Jansen et al., sketch).",
                    "Én mekanisme, ikke hele dødelighetsbildet (Jansen et al., skisse).",
                ),
            )

# ── B: Norsk rammeverk / TLS ──────────────────────────────────────────────────

section_header(
    tr(lang, "B · Current Norwegian framework", "B · Gjeldende norsk rammeverk"),
    tr(lang, "Regulatory context", "Reguleringskontekst"),
)
with st.container(border=True):
    st.markdown(
        tr(
            lang,
            "Norway regulates growth in salmon farming partly through the **traffic-light system (TLS)**. "
            "The coast is divided into **13 production areas**. Each area gets **green / yellow / red** "
            "from estimated risk of lice-induced mortality in out-migrating wild salmon smolts, with "
            "consequences for whether capacity may grow, stay, or must be cut. Colours are often tied to "
            "bands around <10%, 10 to 30% and >30% estimated post-smolt mortality.",
            "Norge regulerer vekst i lakseoppdrett blant annet gjennom **trafikklyssystemet (TLS)**. "
            "Kysten er delt i **13 produksjonsområder**. Hvert område får **grønn / gul / rød** ut fra "
            "estimert risiko for luseindusert dødelighet hos utvandrende villaks-smolt, med konsekvenser "
            "for om kapasitet kan øke, stå stille eller må reduseres. Fargene knyttes ofte til bånd rundt "
            "<10%, 10 til 30% og >30% estimert postsmolt-dødelighet.",
        )
    )
    st.caption(
        tr(
            lang,
            "**Checked 2026-07-27:** Steering group: PO3 high, PO4 moderate (2024 to 25). "
            "NFD 2026: PO3 red (-6% capacity), PO4 yellow.",
            "**Sjekket 2026-07-27:** Styringsgruppen: PO3 høy, PO4 moderat (2024 til 25). "
            "NFD 2026: PO3 rød (-6% kapasitet), PO4 gul.",
        )
    )
    fig_tls = REPO / "mockup" / "figur-trafikklys.png"
    if fig_tls.exists():
        st.image(
            str(fig_tls),
            width="stretch",
            caption=tr(
                lang,
                "TLS over time (Government / Steering group). PO3 has been red in all shown periods. "
                "The 2024 to 2025 map shows more yellow areas further north.",
                "TLS over tid (Regjeringen / Styringsgruppen). PO3 har vært rød i alle viste perioder. "
                "Kartet for 2024 til 2025 viser flere gule områder lenger nord.",
            ),
        )
    with st.expander(tr(lang, "Read more: what TLS is actually built on", "Les mer om hva TLS faktisk bygges på")):
        st.markdown(
            tr(
                lang,
                "TLS is not one measurement. It is a **knowledge chain** that combines farm figures, "
                "models, field data and expert judgement. The corpus discusses the links in this chain.",
                "TLS er ikke én måling. Det er en **kunnskapskjede** som kombinerer oppdrettstall, "
                "modeller, felt og ekspertvurdering. Korpuset diskuterer leddene i denne kjeden.",
            )
        )
        st.markdown(
            tr(
                lang,
                """
<ol class="hl-chain">
  <li><strong>Lice and biomass on farms</strong>: reported lice loads and fish in pens give a basis for estimated larval production.</li>
  <li><strong>Hydrodynamics and particle spread</strong>: models for how infectious larvae are transported along coast and fjord.</li>
  <li><strong>Smolt out-migration</strong>: assumed or modelled timing, duration and route for post-smolts (often virtual post-smolt / VPS).</li>
  <li><strong>Infestation to mortality</strong>: dose to response / thresholds that turn lice load into estimated mortality.</li>
  <li><strong>Calibration and field</strong>: models tuned against trawl, sentinel cages and genetic assignment. Different sources can give different outcomes.</li>
  <li><strong>Expert group and decision</strong>: combined assessment per production area. Capacity decisions are made administratively and politically.</li>
</ol>
""",
                """
<ol class="hl-chain">
  <li><strong>Lus og biomasse på oppdrett</strong>: rapporterte lusemengder og fisk i merd gir grunnlag for estimert larveproduksjon.</li>
  <li><strong>Hydrodynamikk og partikkelspredning</strong>: modeller for hvordan infeksiøse larver transporteres langs kyst og fjord.</li>
  <li><strong>Smoltens utvandring</strong>: antatt eller modellert tid, varighet og rute for postsmolt (ofte «virtuell postsmolt» / VPS).</li>
  <li><strong>Infestasjon til dødelighet</strong>: dose til respons og terskler som omsetter luselast til estimert dødelighet.</li>
  <li><strong>Kalibrering og felt</strong>: modeller justeres mot trål, sentinelbur og genetisk tilordning. Ulike datakilder kan gi ulike utfall.</li>
  <li><strong>Ekspertgruppe og beslutning</strong>: samlet vurdering per produksjonsområde. Kapasitetsvedtak fattes forvaltningsmessig og politisk.</li>
</ol>
""",
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            tr(
                lang,
                "Several model families appear in the Norwegian picture (incl. IMR VPS and NVI risk "
                "models discussed in the corpus). They are meant to *complement* field observations "
                "because full coverage in time and space is impossible. Disagreement sits in calibration, "
                "migration assumptions, thresholds, and how well predictions match wild fish measurements.",
                "Flere modellfamilier inngår i det norske bildet (bl.a. IMR VPS og NVI-risikomodeller "
                "omtalt i korpuset). De er ment å *utfylle* feltobservasjoner fordi full dekning i tid "
                "og rom er umulig. Uenigheten ligger i kalibrering, migrasjonsantakelser, terskler og "
                "hvor godt prediksjonene treffer det som måles på villfisk.",
            )
        )
        st.markdown(
            tr(
                lang,
                """
**Primary legal sources (Lovdata)**

- [Produksjonsområdeforskriften](https://lovdata.no/dokument/SF/forskrift/2017-01-16-61)
  (FOR-2017-01-16-61). § 8 makes lice impact on wild salmonids the environmental indicator.
  The ministry assesses impact as acceptable, moderate or unacceptable.
  §§ 9 to 11 allow capacity to be reduced, held or increased. § 13 sets capacity increase at 6%.
- [Lakselusforskriften](https://lovdata.no/dokument/SF/forskrift/2012-12-05-1140)
  (FOR-2012-12-05-1140). § 8 sets operational lice limits on farmed fish:
  fewer than 0.2 adult female lice per fish in a spring window, otherwise fewer than 0.5.
  The week ranges differ south of Nordland and in Nordland, Troms and Finnmark.
- [Akvakulturloven](https://lovdata.no/dokument/NL/lov/2005-06-17-79)
  (LOV-2005-06-17-79). Framework act. Production-area and lice rules are issued under this act.
  The lice regulation is also grounded in the Food Act.

The green, yellow and red bands around estimated post-smolt mortality are scientific management
practice behind TLS colouring. They are not stated as numeric bands in the production-area
regulation itself. The TLS capacity track and the operational farm-lice limits are separate tracks.
""",
                """
**Primære rettskilder (Lovdata)**

- [Produksjonsområdeforskriften](https://lovdata.no/dokument/SF/forskrift/2017-01-16-61)
  (FOR-2017-01-16-61). § 8 gjør påvirkning av lakselus på vill laksefisk til miljøindikator.
  Departementet vurderer påvirkningen som akseptabel, moderat eller uakseptabel.
  §§ 9 til 11 åpner for at kapasitet kan nedjusteres, holdes eller økes. § 13 setter kapasitetsøkning til 6 %.
- [Lakselusforskriften](https://lovdata.no/dokument/SF/forskrift/2012-12-05-1140)
  (FOR-2012-12-05-1140). § 8 setter operative lusgrenser på oppdrettsfisk:
  færre enn 0,2 voksen hunnlus per fisk i et vårvindu, ellers færre enn 0,5.
  Ukeintervallene er ulike sør for Nordland og i Nordland, Troms og Finnmark.
- [Akvakulturloven](https://lovdata.no/dokument/NL/lov/2005-06-17-79)
  (LOV-2005-06-17-79). Rammeverkslov. Produksjonsområde- og luseregler er gitt med hjemmel i denne.
  Lakselusforskriften er også hjemlet i matloven.

Båndene rundt estimert postsmolt-dødelighet (grønn, gul og rød) er vitenskapelig
forvaltningspraksis bak TLS-fargene. De står ikke som tallbånd i
produksjonsområdeforskriften selv. TLS-kapasitetssporet og de operative lusgrensene på
oppdrettsfisk er to ulike spor.
""",
            )
        )

# ── C: Uenighetskart ──────────────────────────────────────────────────────────

section_header(
    tr(lang, "C · Where the corpus disagrees", "C · Hvor korpuset er uenig"),
    tr(lang, "Editorial disagreement map", "Redaksjonelt uenighetskart"),
)
with st.container(border=True):
    st.markdown(
        tr(
            lang,
            "The corpus is largely aligned that lice *can* harm out-migrating smolts under high pressure. "
            "Disagreement sits in what drives management and interpretation. Pick a dividing line below to "
            "see where the evidence diverges. The text orients you. It does not give a verdict.",
            "Korpuset er i hovedsak samstemt om at lakselus *kan* skade utvandrende smolt under høyt press. "
            "Uenigheten ligger i det som styrer forvaltning og tolkning. Velg en skillelinje under for å se "
            "hvor evidensen divergerer. Teksten orienterer. Den gir ikke en fasit.",
        )
    )

    fault_labels = [f[0] for f in FAULTS[lang]]
    fault_idx = st.selectbox(
        tr(lang, "Dividing line / contested question", "Skillelinje / omstridt spørsmål"),
        options=list(range(len(fault_labels))),
        format_func=lambda i: fault_labels[i],
    )

    st.markdown(f"**{fault_labels[fault_idx]}**")
    st.markdown(FAULTS[lang][fault_idx][1])
    paper_chips(FAULT_PAPERS[fault_idx])

    st.write("")
    if st.button(tr(lang, "Ask about this in D ↓", "Spør om dette i D ↓")):
        st.session_state["user_query"] = FAULTS[lang][fault_idx][2]
        st.rerun()

st.caption(
    tr(
        lang,
        "Editorial orientation · last reviewed 2026-08-07 · Ask in D searches the whole active corpus.",
        "Redaksjonell orientering · sist gjennomgått 2026-08-07 · Ask i D søker i hele det aktive korpuset.",
    )
)

# ── D: Ask (handlingsflate, live RAG) ─────────────────────────────────────────

section_header(
    tr(lang, "D · Go deeper (Ask)", "D · Gå dypere (Ask)"),
    tr(lang, "Live synthesis", "Live syntese"),
)

if mode == "researcher":
    st.markdown(
        tr(
            lang,
            "Section C helps you orient in the evidence. Section D lets you ask a contested scientific "
            "question. The tool retrieves from the curated corpus and returns a technical synthesis. "
            "Disagreement is kept visible.",
            "Seksjon C hjelper deg å orientere deg i evidensen. Seksjon D lar deg stille et omstridt "
            "vitenskapelig spørsmål. Verktøyet henter fra det kuraterte korpuset og returnerer en "
            "teknisk syntese. Uenighet holdes synlig.",
        )
    )
else:
    st.markdown(
        tr(
            lang,
            "Section C helps you orient in the evidence. Section D lets you ask in plain language. "
            "The tool explains what the studies show, including where researchers disagree.",
            "Seksjon C hjelper deg å orientere deg i evidensen. Seksjon D lar deg spørre med enkelt språk. "
            "Verktøyet forklarer hva studiene viser, også der forskerne er uenige.",
        )
    )

EXAMPLE_QUESTIONS = {
    "en": [
        "",
        "Did sea lice on wild Pacific salmon decline after aquaculture was removed in British Columbia?",
        "How sensitive are Traffic Light System classifications to model assumptions and calibration data?",
        "Does the virtual post-smolt model overestimate lice-induced mortality compared with trawl observations?",
        "What evidence links lice-induced mortality to reduced adult returns?",
        "Can laboratory lice mortality thresholds for salmon be transferred to sea trout in the field?",
        "How robust is the Norwegian Traffic Light System as a regulatory framework?",
    ],
    "no": [
        "",
        "Hva skjedde med lus på villaks etter at oppdrett ble fjernet i British Columbia, og er det overførbart til Norge?",
        "Hva er Van Nes et al. og Stige et al. egentlig uenige om når det gjelder kalibrering av lusemodeller?",
        "Hvor godt treffer de operative lusemodellene det som faktisk måles på villfisk?",
        "Gir luseindusert smoltdødelighet færre voksne tilbake, og hvordan står det mot andre dødsårsaker i havet?",
        "Ved hvilke lusenivåer dør postsmolt faktisk, og hvor godt er den terskelen etablert fra lab til felt?",
        "Hvor robust er det norske Trafikklyssystemet som kunnskapsgrunnlag for kapasitetsregulering?",
    ],
}

with st.container(border=True):
    examples = EXAMPLE_QUESTIONS[lang]
    pick = st.selectbox(
        tr(lang, "Example questions (mirror the dividing lines in C)", "Eksempelspørsmål (speiler skillelinjene i C)"),
        options=examples,
        format_func=lambda q: tr(lang, "Choose a question", "Velg et spørsmål") if q == "" else q,
        key=f"example_pick_{lang}",
    )
    if pick and st.session_state.get("_applied_example") != pick:
        st.session_state["user_query"] = pick
        st.session_state["_applied_example"] = pick

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

    col1, col2 = st.columns([1, 4])
    with col1:
        run = st.button(tr(lang, "Synthesise", "Syntetiser"), type="primary", width="stretch")
    with col2:
        st.caption(
            tr(
                lang,
                f"Retrieves up to k = {top_k} by similarity among {len(selected_labels) if selected_labels else 0} active papers. Contrasting papers may be added.",
                f"Henter opptil k = {top_k} etter likhet blant {len(selected_labels) if selected_labels else 0} aktive artikler. Kontrasterende artikler kan legges til.",
            )
        )

if run and query.strip():
    if not selected_labels:
        st.error(tr(lang, "Select at least one paper in the sidebar before querying.", "Velg minst én artikkel i sidepanelet før du spør."))
        st.stop()

    client = get_client()
    if not client:
        st.stop()

    with st.spinner(tr(lang, "Retrieving relevant documents...", "Henter relevante dokumenter...")):
        results, routed_qs = retrieve_routed(
            client,
            query.strip(),
            top_k=top_k,
            selected_doc_ids=selected_doc_ids,
        )

    if not results or is_out_of_scope(results):
        st.warning(
            tr(
                lang,
                "This question appears to fall outside this corpus. "
                "Try a question about salmon lice and wild salmonids, or pick a dividing line in section C.",
                "Spørsmålet ser ut til å ligge utenfor dette korpuset. "
                "Prøv et spørsmål om lakselus og ville laksefisk, eller velg en skillelinje i seksjon C.",
            )
        )
        st.caption(
            tr(
                lang,
                f"Best retrieval score: {best_retrieval_score(results):.2f} "
                "(below the in-scope threshold).",
                f"Beste treffscore: {best_retrieval_score(results):.2f} "
                "(under terskelen for å være innenfor korpuset).",
            )
        )
        st.stop()

    if routed_qs:
        st.caption(
            tr(
                lang,
                f"Question routing: preferred priority questions {' · '.join(routed_qs)}",
                f"Spørsmåls-routing: prioriterte spørsmål {' · '.join(routed_qs)}",
            )
        )

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
    n_extra = sum(1 for r in results if r.get("added_as_debate_link"))
    n_ranked = len(results) - n_extra
    if n_extra:
        st.subheader(
            tr(
                lang,
                f"Retrieved sources ({n_ranked} by similarity, {n_extra} debate-linked)",
                f"Hentede kilder ({n_ranked} etter likhet, {n_extra} debattlenker)",
            )
        )
        st.caption(
            tr(
                lang,
                "k is similarity rank. Debate-linked papers are contrasting or companion documents added so disagreement is not dropped from the set.",
                "k er likhetsrangering. Debattlenker er kontrasterende eller tilhørende artikler, lagt til slik at uenighet ikke faller ut av settet.",
            )
        )
    else:
        st.subheader(
            tr(lang, f"Retrieved sources ({len(results)})", f"Hentede kilder ({len(results)})")
        )
    render_retrieved_sources_legend(lang)

    try:
        cite_by_id = citation_index(load_corpus())
    except FileNotFoundError:
        cite_by_id = {}

    for r in results:
        icon = DIRECTION_COLOUR.get(r["evidence_direction"], "⚪")
        qual = QUALITY_BADGE.get(r["quality_signal"], "?")
        dir_label = EVIDENCE_DIRECTION_LABELS.get(lang, {}).get(
            r["evidence_direction"], r["evidence_direction"].replace("_", " ")
        )
        cite = short_cite(r.get("authors", ""), r.get("year", ""))
        doi_url = r["url"] or (f"https://doi.org/{r['doi']}" if r["doi"] else "")
        debate_tag = tr(lang, " · debate link", " · debattlenke") if r.get("added_as_debate_link") else ""

        with st.expander(f"{icon} **{cite}** · {dir_label}{debate_tag}"):
            st.markdown(f"**{r['title']}**")
            if doi_url:
                st.markdown(f"[DOI ↗]({doi_url})")
            if r.get("added_as_debate_link"):
                st.caption(
                    tr(
                        lang,
                        "Added as a debate link (contrast or companion), not a top-k similarity hit.",
                        "Lagt til som debattlenke (kontrast eller følgeartikkel), ikke et topp-k likhetstreff.",
                    )
                )

            consensus = (
                str(r["consensus_signal"]).replace("_", " ")
                if r.get("consensus_signal")
                else tr(lang, "not stated", "ikke angitt")
            )
            st.markdown(
                tr(
                    lang,
                    f"**Evidence direction:** {dir_label}  \n"
                    f"**Quality:** {qual} {r['quality_signal']}  \n"
                    f"**Consensus:** {consensus}",
                    f"**Evidensretning:** {dir_label}  \n"
                    f"**Kvalitet:** {qual} {r['quality_signal']}  \n"
                    f"**Konsensus:** {consensus}",
                )
            )

            role_line = source_role_line(r, lang)
            if role_line:
                st.markdown(role_line)

            claims = [c for c in (r.get("key_claims") or []) if c and str(c).strip()]
            if claims:
                st.markdown(tr(lang, "**Key claims:**", "**Hovedpåstander:**"))
                for claim in claims[:CLAIMS_VISIBLE]:
                    st.markdown(f"- {claim}")

            extra_claims = claims[CLAIMS_VISIBLE:]
            brief = (r.get("summary_text") or "").strip()
            rag = (r.get("rag_summary") or "").strip()
            if extra_claims:
                with st.expander(tr(lang, "Read more", "Les mer"), expanded=False):
                    st.markdown(tr(lang, "**Further claims:**", "**Flere påstander:**"))
                    for claim in extra_claims:
                        st.markdown(f"- {claim}")

            if mode == "researcher" and brief:
                with st.expander(tr(lang, "Evidence brief", "Evidensnotat"), expanded=False):
                    st.markdown(brief[:8000])
            elif rag:
                rag_label = (
                    tr(lang, "Summary", "Oppsummering")
                    if mode == "researcher"
                    else tr(lang, "Short summary", "Kort oppsummering")
                )
                with st.expander(rag_label, expanded=False):
                    st.markdown(rag)

            status = (r.get("curator_review_status") or "").strip()
            if status:
                status_label = CURATOR_STATUS_LABELS.get(lang, {}).get(status, status)
                st.caption(tr(lang, "Curation: ", "Kuratering: ") + status_label)

            decided_by = (r.get("inclusion_decided_by") or "").strip()
            if decided_by:
                st.caption(
                    tr(lang, "Inclusion decided by: ", "Inklusjon besluttet av: ")
                    + decided_by
                )

            if r.get("related_contrasting"):
                st.caption(
                    tr(lang, "Contrasts with: ", "Kontrasterer med: ")
                    + human_contrasts(r["related_contrasting"], cite_by_id)
                )

            tags = r.get("priority_questions") or []
            if tags and mode == "researcher":
                st.caption(
                    tr(lang, "Priority questions: ", "Prioriterte spørsmål: ")
                    + " · ".join(tags)
                )

            with st.expander(tr(lang, "Technical details", "Tekniske detaljer"), expanded=False):
                if tags and mode != "researcher":
                    st.caption(
                        tr(lang, "Priority questions: ", "Prioriterte spørsmål: ")
                        + " · ".join(tags)
                    )
                st.caption(f"doc_id: `{r.get('doc_id', '')}`")
                st.caption(
                    tr(
                        lang,
                        f"Retrieval score (cosine, not a relevance percent): {r['score']:.3f}",
                        f"Retrieval-score (cosinus, ikke en relevansprosent): {r['score']:.3f}",
                    )
                )

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

st.markdown(
    tr(
        lang,
        '<div class="hl-footer">Havbruksløftets Evidensrom. Evidence room on salmon lice and wild salmon. '
        "Honest Broker method: we show evidence, uncertainty and disagreement. "
        "We do not invent a consensus.</div>",
        '<div class="hl-footer">Havbruksløftets Evidensrom. Evidensrom om lakselus og villaks. '
        "Honest Broker-metode: vi viser evidens, usikkerhet og uenighet. "
        "Vi lager ikke en kunstig konsensus.</div>",
    ),
    unsafe_allow_html=True,
)
