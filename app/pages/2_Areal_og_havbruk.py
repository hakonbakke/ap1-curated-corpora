"""
Evidensrom: Areal og havbruk (working draft).

Orientering (A til C) + Spør kildene (D) mot isolert parquet
data/area-and-aquaculture.parquet.
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
    AREAL_DATA_FILE,
    load_corpus,
    reload_corpus,
    retrieve,
    is_out_of_scope,
)
from synthesis import synthesise
from ui import brand_header, inject_css, paper_chips, section_header

st.set_page_config(
    page_title="Areal og havbruk · Evidensrom",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

LANG_OPTIONS = ["en", "no"]


def tr(lang: str, en: str, no: str) -> str:
    return no if lang == "no" else en


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


def _last_name(authors: str) -> str:
    if not authors:
        return "?"
    first = str(authors).split(";")[0].strip()
    parts = first.split()
    return parts[-1] if parts else "?"


# ── Fault lines (C) ───────────────────────────────────────────────────────────

FAULTS = {
    "no": [
        (
            "1. Hva begrenser vekst i havbruk på norskekysten: mangel på sjøflate, tillatelser, kommunal utpeking, eller biologi?",
            "Hvis merden tar så lite plass, hva er det da som mangler? Hersoug, Mikkelsen "
            "og Osmundsen (2020) svarer at grensen nasjonalt går ved produksjonstillatelser "
            "og trafikklys, ikke ved mangel på ledig sjøflate, selv om noen regioner er "
            "fulle og avstandskrav krymper det brukbare. Trafikklyset fargelegger 13 "
            "produksjonsområder etter lus på vill laksefisk og styrer om kapasiteten der "
            "kan økes, fryses eller kuttes. Sandersen og Kvalvik (2015) og Gullestad "
            "(2011) ser knappheten i gode lokaliteter og i kommunens vilje til å peke ut "
            "sjø. Sand (2025) og Kulmambetova og Tveterås (2025) setter lus, sykdom, "
            "velferd og nærhet mellom anlegg først. Jentoft og Buanes (2005) kaller "
            "bildet av nesten ubegrenset kystplass en myte: fra luften er merdene prikker, "
            "på bakken gjør sikkerhetssoner næringen plasskrevende. Diagnosene er skrevet "
            "forbi hverandre. Ingen tekst prøver dem mot samme kyst og samme år.",
            "Hva begrenser vekst i havbruk på norskekysten: mangel på sjøflate, tillatelser, kommunal utpeking, eller biologi?",
        ),
        (
            "2. Hva avgjør utpekingen av sjøareal til havbruk: plankartet, senere dispensasjon, eller avslag etter vedtak?",
            "Siden 1989-revisjonen er det kommunen som peker ut sjøareal til havbruk. Vedtatt "
            "plankart er likevel ikke siste ord. Kvalvik og Robertsen (2017) og SALT 1065 "
            "viser at dispensasjon og daglig forvaltning kan åpne sjø planen ikke pekte "
            "ut. Sand (2025) viser kombinert formål som ser stort ut på kartet og likevel "
            "faller i søknad. Innsigelse og avslag fra sektormyndighet kan stanse saken "
            "etter at kartet er vedtatt. Sørdahl og Kvalvik (2024) og Sørdahl (2026) leser "
            "fem generasjoner Tromsø-planer: tykkere og mer helhetlige dokumenter avgjør "
            "ikke i seg selv hvilken sjø som pekes ut. Det åpne spørsmålet er hvor saken "
            "stopper etter at kommunen har sagt ja eller nei: i kartet, i senere "
            "dispensasjon, eller i innsigelse og avslag.",
            "Hva avgjør utpekingen av sjøareal til havbruk: plankartet, senere dispensasjon, eller avslag etter vedtak?",
        ),
        (
            "3. Hvor i tillatelsesstabelen dør en lokalitetssak: tildeling, smitteavstand, eller sektoravslag?",
            "Et anlegg trenger produksjonstillatelse og lokalitetstillatelse. Fra 2010 "
            "samordner fylkeskommunen lokalitetssaken. Sandersen og Kvalvik (2014) "
            "beskriver den reformen som oppgaver uten reell myndighet: flere og mindre "
            "enheter. Osmundsen og Olsen (2025) skiller fylkeskoordinering, kommunal "
            "utpeking og avslag fra sektormyndighet, og finner at fylket mangler verktøy til å legge om "
            "den strukturen som finnes. SALT 1110 leser 251 avslag fra 2020-2025. "
            "Mattilsynet er den hyppigst registrerte avslagsinstansen, og lus er den "
            "største kodede grunnen der. Fakta, skjønn og føre var løper ofte sammen. "
            "Schütz og Slater (2019) beskriver produksjonsområder og veien fra plan til "
            "tillatelse som et forutsigbarhetsproblem. Det åpne spørsmålet er om saken dør i "
            "tildelingsrunder, i smitteavstand, eller i ugjennomsiktige avslag.",
            "Hvor i tillatelsesstabelen dør en lokalitetssak: tildeling, smitteavstand, eller sektoravslag?",
        ),
        (
            "4. Når sjø går til havbruk, hva må vike: annen bruk, levende natur, eller anlegget?",
            "Når sjø går til anlegg, må noe annet vike: en annen bruk (fiskeri, ferdsel, "
            "friluftsliv, forsvar, havvind), eller villaks, kysttorsk og natur på bunnen som "
            "allerede er der. Noen ganger er det anlegget som må vike. Evenset og "
            "medforfattere (2023) fant ingen publisert litteratur om at andre kystnæringer "
            "skader anlegg, så ekspertskårer fyller det hullet. Mikkelsen og medforfattere "
            "(2025) viser at naturmangfoldloven § 10 krever samlet belastning som "
            "retningslinje, mens akvakulturloven ikke har noen uttrykkelig plikt eller "
            "metode for det. Sandersen og Kvalvik (2015) behandler miljødebatten og "
            "arealavgiftsdebatten som to spor. Meld. St. 35 (2023-2024) plasserer havbruk "
            "som én sektor i bruk og bevaring av natur, og sier at trafikklys og "
            "kvalitetsnorm for villaks ikke styrer mot samme mål. Dette er en strid om "
            "bruk og verdier, ikke et andre villaks-rom.",
            "Når sjø går til havbruk, hva må vike: annen bruk, levende natur, eller anlegget?",
        ),
        (
            "5. Hvordan brukes, mangler eller utsettes kunnskap i plan og lokalitetsbehandling av havbruk?",
            "Hvis det er omstridt hva som er knapt, er planen og søknaden stedet der "
            "striden skulle avgjøres. Ofte skjer det ikke der. SALT 1065 skiller mellom "
            "det som hører hjemme i kommunens konsekvensutredning og det som hører hjemme "
            "i akvakulturlovsaken, og viser til Sivilombudets saker om usikkerhet i "
            "planfilen. SALT 1110 leser 251 avslag og finner at fakta, faglig skjønn og "
            "føre var ofte løper sammen, og at terskler for korall ikke er standardisert. "
            "Sørdahl (2024, 2026) argumenterer for at mer helhet i dokumentet ikke er mer "
            "avgjørelse. Mikkelsen (2025) og Evenset (2023) peker begge på samlet "
            "belastning som manglende kunnskap og svak praksis. Hullet er hvordan "
            "usikkerhet og føre var skal inn i vedtaket. Det er ikke først et spørsmål "
            "om hvilken studie som mangler.",
            "Hvordan brukes, mangler eller utsettes kunnskap i plan og lokalitetsbehandling av havbruk?",
        ),
        (
            "6. Er mer areal feil grep hvis tetthet og biologi begrenser først?",
            "Smitteavstand og smitte mellom naboanlegg legger beslag på langt mer "
            "sjø enn merden, og både Hersoug (2020) og Sand (2025) gjentar det. "
            "Kulmambetova og Tveterås (2025) finner at tettere naboer henger sammen med "
            "høyere produksjonskostnad. Gullestad (2011) foreslo produksjonsområder og "
            "samordnet brakklegging, uten å fastsette sonestørrelse. Rapporten om "
            "bærekraftig arealbruk (2023) vil ha tetthetsregler og bestrider "
            "trafikklyskutt, mens HI (2026) beskriver bæreevnen per produksjonsområde som "
            "lite kjent. Hvis det er biologi og avstand som begrenser, er «mer areal» feil politisk "
            "setning. Trafikklyset er da et lokk på vekst, ikke et argument for mer "
            "sjøflate. Aldrin (2011-2017), Qviller (2024) og Moldal (2026) ligger i "
            "mappen som nabotekster om spredning.",
            "Er mer areal feil grep hvis tetthet og biologi begrenser først?",
        ),
        (
            "7. Åpner skatt og fond mer sjøareal i kommunene, eller kan de ta pengene uten å peke ut mer?",
            "Kommunen peker ut sjøen, så nasjonale vekstmål hviler på lokal vilje. Penger "
            "er grepet som oftest foreslås. Sandersen og Kvalvik (2015) kaller "
            "arealavgiften et wicked problem: miljøkonflikt, annen bruk og lav lokal "
            "avkastning etter at eierskapet ble konsentrert. De beskriver et verstefall "
            "der kommunen tar pengene og likevel ikke vil peke ut mer sjø. Arealavgift "
            "ble funnet uegnet som instrument, og senere kom eiendomsskatt på sjøanlegg, "
            "produksjonsavgift og Havbruksfondet (Hersoug 2020). Rosendal (2025) kobler "
            "kommunal økonomi til miljøhensyn. Om penger faktisk åpner mer sjøareal, har "
            "ingen av tekstene testet.",
            "Åpner skatt og fond mer sjøareal i kommunene, eller kan de ta pengene uten å peke ut mer?",
        ),
    ],
    "en": [
        (
            "1. What limits aquaculture growth on the Norwegian coast: unused sea, licences, municipal designation, or biology?",
            "If the pen takes so little room, what is it that runs out? Hersoug, "
            "Mikkelsen and Osmundsen (2020) answer that the national limit sits with "
            "production licences and the traffic-light rule, not with a lack of unused "
            "sea surface, even though some regions are full and spacing requirements "
            "shrink what is usable. The traffic-light colours 13 production areas by "
            "lice on wild salmonids and decides whether capacity there can grow, freeze "
            "or be cut. Sandersen and Kvalvik (2015) and Gullestad (2011) locate "
            "scarcity in good sites and in the municipality's willingness to designate "
            "sea. Sand (2025) and Kulmambetova and Tveterås (2025) put lice, disease, "
            "welfare and proximity between farms first. Jentoft and Buanes (2005) name "
            "the picture of almost unlimited coastal space as a myth: from the air the "
            "pens are dots, on the ground security zones make aquaculture "
            "space-consuming. The diagnoses are written past one another. No text tests "
            "them on the same coast and the same years.",
            "What limits aquaculture growth on the Norwegian coast: unused sea, licences, municipal designation, or biology?",
        ),
        (
            "2. What decides designation of sea for aquaculture: the plan map, later dispensation, or refusal after the map?",
            "Since the 1989 revision it is the municipality that designates sea area for "
            "aquaculture. An adopted plan map is still not the last word. Kvalvik and Robertsen "
            "(2017) and SALT 1065 show that dispensation and day-to-day management can "
            "open sea the plan did not designate. Sand (2025) shows combined-purpose "
            "zoning that looks large on the map and still fails at application. Sector "
            "objection and refusal can stop the case after the map is adopted. Sørdahl "
            "and Kvalvik (2024) and Sørdahl (2026) read five generations of Tromsø "
            "plans: thicker, more comprehensive documents do not by themselves settle "
            "which sea is designated. The open question is where the case stops after the "
            "municipality has said yes or no: in the map, in later dispensation, or in "
            "objection and refusal.",
            "What decides designation of sea for aquaculture: the plan map, later dispensation, or refusal after the map?",
        ),
        (
            "3. Where in the permit stack does a locality case die: allocation, sanitary spacing, or sector refusal?",
            "A farm needs a production licence and a locality licence. From 2010 the "
            "county coordinates the locality case. Sandersen and Kvalvik (2014) describe "
            "that reform as tasks without real authority: more units, and smaller ones. "
            "Osmundsen and Olsen (2025) separate county coordination, municipal "
            "designation and sector vetoes, and find that the county lacks tools to "
            "recast the structure that exists. SALT 1110 reads 251 refusals from "
            "2020-2025. The Food Safety Authority is the most frequent recorded refuser, "
            "and lice is the largest coded ground there. Facts, judgement and "
            "precaution often run together. Schütz and Slater (2019) treat production "
            "areas and the path from plan to permit as a predictability problem. The "
            "open question is whether the case dies in allocation rounds, in sanitary "
            "spacing, or in opaque refusals.",
            "Where in the permit stack does a locality case die: allocation, sanitary spacing, or sector refusal?",
        ),
        (
            "4. When sea goes to aquaculture, what must yield: other use, living nature, or the farm?",
            "When sea goes to a farm, something else has to yield: another use "
            "(fisheries, shipping, recreation, defence, offshore wind), or wild salmon, "
            "coastal cod and seabed nature already living there. Sometimes it is the "
            "farm that has to yield. Evenset and colleagues (2023) found no published "
            "literature on other coastal industries harming farms, so expert scores fill "
            "that gap. Mikkelsen and colleagues (2025) show that Nature Diversity Act "
            "section 10 requires cumulative load as a guideline, while the Aquaculture "
            "Act has no explicit duty or method for it. Sandersen and Kvalvik (2015) "
            "treat the environmental debate and the area-rent debate as two tracks. "
            "Meld. St. 35 (2023-2024) places aquaculture as one sector in use and "
            "conservation of nature, and says that the traffic-light and the quality "
            "standard for wild salmon do not steer toward the same goal. This is a "
            "dispute over use and values, not a second wild-salmon room.",
            "When sea goes to aquaculture, what must yield: other use, living nature, or the farm?",
        ),
        (
            "5. How is knowledge used, missing or postponed in plans and locality processing of aquaculture?",
            "If what is scarce is disputed, the plan and the application are where that "
            "dispute should be settled. Often it is not settled there. SALT 1065 "
            "separates what belongs in the municipal impact assessment from what belongs "
            "in the Aquaculture Act case, and points to Ombudsman cases on uncertainty in "
            "the plan file. SALT 1110 reads 251 refusals and finds that facts, "
            "professional judgement and precaution often run together, and that "
            "thresholds for coral are not standardised. Sørdahl (2024, 2026) argue that "
            "more holism in the document is not more decision. Mikkelsen (2025) and "
            "Evenset (2023) both point to cumulative load as missing knowledge and weak "
            "practice. The gap is how uncertainty and precaution should enter the "
            "decision. It is not first a question of which study is missing.",
            "How is knowledge used, missing or postponed in plans and locality processing of aquaculture?",
        ),
        (
            "6. Is more area the wrong move if density and biology limit growth first?",
            "Sanitary distances and infection between neighbouring farms claim far more "
            "sea than the pen, and both Hersoug (2020) and Sand (2025) repeat the point. "
            "Kulmambetova and Tveterås (2025) find that closer neighbours are associated "
            "with higher production cost. Gullestad (2011) proposed production areas and "
            "coordinated fallowing, without setting a zone size. The 2023 report on "
            "sustainable area use calls for density rules and disputes traffic-light "
            "cuts, while HI (2026) describes carrying capacity per production area as "
            "little known. If biology and distance limit first, more area is the wrong "
            "policy sentence. The traffic-light is then a lid on growth, not an argument "
            "for more sea surface. Aldrin (2011-2017), Qviller (2024) and Moldal (2026) "
            "sit in the file as neighbouring texts on spread.",
            "Is more area the wrong move if density and biology limit growth first?",
        ),
        (
            "7. Do tax and funds open more sea area in municipalities, or can they take the money without designating more?",
            "The municipality designates the sea, so national growth targets rest on "
            "local will. Money is the fix most often proposed. Sandersen and Kvalvik "
            "(2015) call the area rent a wicked problem: environmental conflict, other "
            "uses, and low local return after ownership became concentrated. They "
            "describe a worst case in which the municipality takes the money and still "
            "declines to designate more sea. Area rent was found unsuited as an instrument, "
            "and property tax on sea installations, a production fee and Havbruksfondet "
            "followed (Hersoug 2020). Rosendal (2025) links municipal finances to "
            "environmental concern. Whether money actually opens more sea area is "
            "something none of the texts has tested.",
            "Do tax and funds open more sea area in municipalities, or can they take the money without designating more?",
        ),
    ],
}

FAULT_PAPERS = [
    [
        "2020_hersoug_whats-the-clue",
        "2015_sandersen_access-to-sites",
        "2011_gullestad_arealbruk-havbruk",
        "2025_sand_havbrukets-arealbehov-trondelag",
        "2025_kulmambetova_spatial-density-productivity",
        "2005_jentoft_challenges-myths-czm",
    ],
    [
        "2017_kvalvik_intermunicipal-coastal-planning",
        "2021_sandersen_kystsone-helgeland",
        "2019_mikkelsen_arealplanlegging-sjo",
        "salt_1065_ku-arealplanlegging",
        "2025_sand_havbrukets-arealbehov-trondelag",
        "2024_sordahl_when-all-you-have-is-a-hammer",
    ],
    [
        "2022_hersoug_ten-licensing-systems",
        "2025_osmundsen_fylkeskommune-akvakulturloven",
        "salt_1110_lokalitetssoknader",
        "2015_rettslig_rammeverk-havbruk",
        "2014_sandersen_administrative-reform",
        "2019_schutz_strategic-marine-planning",
    ],
    [
        "2023_evenset_sameksistens",
        "2025_mikkelsen_samlet-pavirkning-nord",
        "2025_sand_arealbruk-bionaringer-trondelag",
        "2015_sandersen_access-to-sites",
        "2019_schutz_strategic-marine-planning",
        "2024_meldst35_baerekraftig-bruk-natur",
    ],
    [
        "salt_1065_ku-arealplanlegging",
        "salt_1110_lokalitetssoknader",
        "2023_evenset_sameksistens",
        "2025_mikkelsen_samlet-pavirkning-nord",
        "2024_sordahl_when-all-you-have-is-a-hammer",
        "2026_sordahl_nar-alt-skal-med",
    ],
    [
        "2025_kulmambetova_spatial-density-productivity",
        "2020_hersoug_whats-the-clue",
        "2011_gullestad_arealbruk-havbruk",
        "undated_baerekraftig-arealbruk-havbruk",
        "2026_hi_risikorapport",
        "2025_sand_havbrukets-arealbehov-trondelag",
    ],
    [
        "2015_sandersen_access-to-sites",
        "2020_hersoug_whats-the-clue",
        "2025_rosendal_municipal-environment-economy",
        "2015_rettslig_rammeverk-havbruk",
        "2025_osmundsen_fylkeskommune-akvakulturloven",
        "2019_mikkelsen_arealplanlegging-sjo",
    ],
]

EXAMPLE_QUESTIONS = {
    "en": [""] + [f[2] for f in FAULTS["en"]],
    "no": [""] + [f[2] for f in FAULTS["no"]],
}

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("Havbruksløftets Evidensrom")
    st.page_link("app.py", label="← Alle evidensrom", icon="🏠")
    lang = st.radio(
        "Language",
        options=LANG_OPTIONS,
        format_func=lambda x: "English" if x == "en" else "Norsk",
        horizontal=True,
    )
    st.caption(tr(lang, "Area and aquaculture", "Areal og havbruk"))
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
                "**Researcher:** Technical language, full citations and stated findings. "
                "The answer follows the shape of your question.\n\n"
                "**Non-specialist:** Plain language without unnecessary jargon. "
                "The structure is adapted to what you asked.",
                "**Forsker:** Teknisk språk, fulle referanser og funn som står i kildene. "
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
                "Answers use plain language. They show the open questions, competing "
                "diagnoses of what limits growth, and where knowledge is missing.",
                "Svarene bruker enkelt språk. De viser de åpne spørsmålene, konkurrerende "
                "diagnoser av hva som begrenser vekst, og der kunnskap mangler.",
            )
        )
    answer_format = "freeform"
    output_language = "Norwegian Bokmål" if lang == "no" else "English"

    st.divider()

    try:
        df = load_corpus(AREAL_DATA_FILE)
        n_total = len(df)
        corpus_ready = True
    except FileNotFoundError:
        df = None
        n_total = 0
        corpus_ready = False
        st.warning(
            tr(
                lang,
                "Areal parquet is not built yet. Run scripts/ingest.py with the area corpus.",
                "Areal-parqueten er ikke bygget ennå. Kjør scripts/ingest.py med arealkorpuset.",
            )
        )

    if corpus_ready:
        st.subheader(tr(lang, "Documents in corpus", "Dokumenter i korpuset"))
        st.caption(tr(lang, f"{n_total} documents in database", f"{n_total} dokumenter i databasen"))
        if st.button(
            tr(lang, "Reload corpus from disk", "Last inn korpus på nytt"),
            help=tr(
                lang,
                "Use after ingest if the document count looks wrong.",
                "Bruk etter ingest hvis antall dokumenter ser feil ut.",
            ),
            width="stretch",
        ):
            df = reload_corpus(AREAL_DATA_FILE)
            st.rerun()
        # Use stable document IDs as widget values. Display labels are not
        # unique (the two retained Kvalvik records describe the same paper),
        # so using labels as keys silently dropped one record.
        option_rows = []
        for _, row in df.sort_values(["year", "doc_id"]).iterrows():
            first_author = _last_name(row.get("authors", ""))
            title = str(row.get("title") or row["doc_id"])
            label = f"{first_author} {row['year']} · {title[:55]}"
            option_rows.append((str(row["doc_id"]), label))
        label_counts = {}
        for _, label in option_rows:
            label_counts[label] = label_counts.get(label, 0) + 1
        doc_options = {
            doc_id: (f"{label} · {doc_id}" if label_counts[label] > 1 else label)
            for doc_id, label in option_rows
        }
        all_doc_ids = list(doc_options)
        if "areal_selected" not in st.session_state:
            st.session_state["areal_selected"] = all_doc_ids
        else:
            # Migrate a pre-fix session that stored display labels. If no
            # stable IDs survive, restore the safe all-documents default.
            stored_ids = st.session_state.get("areal_selected") or []
            valid_ids = [doc_id for doc_id in stored_ids if doc_id in doc_options]
            if stored_ids and not valid_ids:
                st.session_state["areal_selected"] = all_doc_ids
        col_sel, col_clr = st.columns(2)
        if col_sel.button(tr(lang, "Select all", "Velg alle"), width="stretch"):
            st.session_state["areal_selected"] = all_doc_ids
        if col_clr.button(tr(lang, "Clear all", "Tøm"), width="stretch"):
            st.session_state["areal_selected"] = []
        selected_doc_ids = st.multiselect(
            tr(lang, "Include these documents", "Inkluder disse dokumentene"),
            options=all_doc_ids,
            default=[
                doc_id
                for doc_id in st.session_state.get("areal_selected", all_doc_ids)
                if doc_id in doc_options
            ],
            format_func=lambda doc_id: doc_options[doc_id],
            label_visibility="collapsed",
        )
        st.session_state["areal_selected"] = selected_doc_ids
        if not selected_doc_ids:
            st.warning(tr(lang, "Select at least one document.", "Velg minst ett dokument."))
        else:
            st.caption(
                tr(
                    lang,
                    f"{len(selected_doc_ids)} / {n_total} documents active",
                    f"{len(selected_doc_ids)} / {n_total} aktive dokumenter",
                )
            )
    else:
        selected_doc_ids = None

    st.divider()
    top_k = st.slider(
        tr(lang, "Documents to retrieve", "Antall dokumenter å hente"),
        3,
        12,
        8,
        help=tr(
            lang,
            "Number of documents ranked by similarity. This room does not yet add contrast links on top.",
            "Antall dokumenter rangert etter likhet. Dette rommet legger ennå ikke til kontrastlenker oppå treffene.",
        ),
    )
    st.divider()
    st.caption(
        tr(
            lang,
            "Corpus: area-and-aquaculture (39 documents, draft room)  \n"
            "Method: Honest Broker (Pielke 2007)  \n"
            "Funded by FHF / Havbruksløftet AP1",
            "Korpus: area-and-aquaculture (39 dokumenter, utkast-rom)  \n"
            "Metode: Honest Broker (Pielke 2007)  \n"
            "Finansiert av FHF / Havbruksløftet AP1",
        )
    )

# ── Brand + hero ──────────────────────────────────────────────────────────────

brand_header(tr(lang, "Evidence room · area and aquaculture", "Evidensrom · areal og havbruk"))

try:
    year_min = int(df["year"].min())
    year_max = int(df["year"].max())
    span = f"{year_min}-{year_max}"
except Exception:
    span = "2005-2026"

hero_left, hero_right = st.columns([1.5, 0.9])
with hero_left:
    st.markdown(
        tr(
            lang,
            '<h1 class="hl-h1">Area and aquaculture</h1>'
            '<p class="hl-lede">The pens occupy a vanishingly small share of the coastal zone, and yet area scarcity remains a persistent dispute. A distinguishes pen area, locality area and plan area. B shows the split governing system. C and D show the open questions.</p>',
            '<h1 class="hl-h1">Areal og havbruk</h1>'
            '<p class="hl-lede">Merdene tar en forsvinnende liten del av kystsonen, og likevel er knapphet på areal et vedvarende stridsspørsmål. A skiller merdareal, lokalitetsareal og planareal. B viser det delte styringssystemet. C og D viser de åpne spørsmålene.</p>',
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
  <div class="hl-stat"><strong>{n_total or 39}</strong><span>documents in corpus</span></div>
  <div class="hl-stat"><strong>{span}</strong><span>time span</span></div>
  <div class="hl-stat"><strong>{len(FAULTS['en'])}</strong><span>open questions</span></div>
  <div class="hl-stat"><strong>17.09</strong><span>last reviewed</span></div>
</div>
""",
                f"""
<div class="hl-stats">
  <div class="hl-stat"><strong>{n_total or 39}</strong><span>dokumenter i korpuset</span></div>
  <div class="hl-stat"><strong>{span}</strong><span>tidsrom</span></div>
  <div class="hl-stat"><strong>{len(FAULTS['no'])}</strong><span>åpne spørsmål</span></div>
  <div class="hl-stat"><strong>17.09</strong><span>sist gjennomgått</span></div>
</div>
""",
            ),
            unsafe_allow_html=True,
        )

st.caption(
    tr(
        lang,
        "A introduces the paradox and the three area quantities. "
        "B shows the split governing system, with links to statutes and public sources. "
        "C collects the open questions. D searches the corpus. "
        "Working draft. Priority questions are not confirmed by the three selectors. "
        "The corpus is 39 documents: 33 from the received set plus six added by Thord Håkon Bakke on 15 September 2026. "
        "Some files are neighbouring texts on farm-to-farm spread, fish health, welfare law and valuation. They do not answer designation.",
        "A innfører paradokset og de tre arealbegrepene. B viser det delte styringssystemet, med lenker til lover og offentlige kilder. "
        "C samler de åpne spørsmålene. D søker i korpuset. "
        "Arbeidsutkast. Prioritetsspørsmål er ikke bekreftet av de tre utvelgerne. "
        "Korpuset er 39 dokumenter: 33 fra den mottatte bunken pluss seks som Thord Håkon Bakke la inn 15. september 2026. "
        "Noen filer er nabotekster om smitte mellom anlegg, fiskehelse, velferdsrett og verdsetting. De svarer ikke på utpeking.",
    )
)

st.write("")

# ── A: Introduksjon ───────────────────────────────────────────────────────────

section_header(
    tr(lang, "A · Introduction", "A · Introduksjon"),
    tr(lang, "Editorial overview", "Redaksjonell oversikt"),
)
with st.container(border=True):
    col_a, col_fig = st.columns([1.7, 0.7])
    with col_a:
        st.markdown(
            tr(
                lang,
                """
Norwegian aquaculture runs along a coastline that is, internationally, almost unreal in length and fragmentation, and yet scarcity of area has become one of the most persistent disputes in the industry's governance. The paradox is clear when the figures are set side by side. Inside the baseline there is on the order of 76 000 to 80 000 square kilometres of sea, while the pens themselves occupy a vanishingly small share of this, estimated at half a percent of the coastal zone. At the same time, farmers report year after year that they cannot get the localities they need. Already in 2005, Jentoft and Buanes called the idea of almost unlimited coastal space a myth: from the air the pens look like dots on an empty surface, but on the ground moorings, safety zones and spacing requirements between farms make the industry far more space-consuming than the footprint suggests.

The key to the disagreement is that when people talk about how much area aquaculture occupies, it is described by three different quantities.

**Pen area.** The farm's physical surface in the sea.

**Locality area.** Also includes the mooring system and the safety zone.

**Plan area.** The sea the municipality has designated for the purpose, often as a combined purpose where aquaculture is only one of several permitted uses.

When infection distances between farms are counted in, the occupation grows sharply, and in some production areas it ties up a substantial share of available sea. Debates about whether the coast is full or empty therefore easily become meaningless if the parties are each talking about a different one of these quantities.
""",
                """
Norsk havbruk drives langs en kystlinje som i internasjonal sammenheng er nesten uvirkelig lang og oppstykket, og likevel er knapphet på areal blitt et av de mest vedvarende stridsspørsmålene i næringens forvaltning. Paradokset trer tydelig frem når tallene settes ved siden av hverandre. Innenfor grunnlinjen ligger det i størrelsesorden 76 000 til 80 000 kvadratkilometer sjø, mens selve merdene legger beslag på en forsvinnende liten del av dette, anslagsvis en halv prosent av kystsonen. Samtidig melder oppdrettere år etter år at de ikke får tilgang til de lokalitetene de trenger. Allerede i 2005 kalte Jentoft og Buanes forestillingen om nærmest ubegrenset kystplass for en myte: fra luften ser merdene ut som prikker på en tom flate, men på bakken gjør fortøyninger, sikkerhetssoner og krav til avstand mellom anlegg næringen langt mer plasskrevende enn fotavtrykket tilsier.

Nøkkelen til uenigheten ligger i at når man snakker om hvor mye areal havbruk beslaglegger, beskrives det av tre ulike størrelser.

**Merdareal.** Anleggets fysiske flate i sjøen.

**Lokalitetsareal.** Omfatter i tillegg fortøyningssystem og sikkerhetssone.

**Planareal.** Den sjøen kommunen har avsatt til formålet, ofte som kombinert formål der havbruk bare er én av flere tillatte bruksmåter.

Når smitteavstander mellom anlegg regnes inn, vokser beslaget kraftig, og i enkelte produksjonsområder binder det opp en betydelig andel av tilgjengelig sjø. Diskusjoner om hvorvidt kysten er full eller tom blir derfor lett meningsløse dersom partene snakker om hver sin av disse størrelsene.
""",
            )
        )
        with st.expander(tr(lang, "Read more", "Les mer")):
            st.markdown(
                tr(
                    lang,
                    """
**Split governance.** Governance is split between levels that each have their own logic. The municipality designates sea area under the Planning and Building Act, out to one nautical mile beyond the baselines, and thus holds a key role that national growth targets depend on. A farm then needs both a production licence and a locality licence, and after the 2010 administrative reform it is the county that coordinates the locality case. Sector authorities can still refuse under their own statutes, so an application can survive the plan process and stop somewhere else entirely. Above this sits the traffic-light system with its thirteen production areas, which is a lid on capacity and not a map of where farms may stand.

**Three answers on what stops growth.** What actually stops growth is the central disputed question, and there are at least three competing answers. One points to the licence regime: the constraint is not sea surface, but production licences and capacity limits. The second points to the municipality, where good localities are a limited resource and the political will to designate sea decides what is available at all. The third points to biology, where lice, disease, fish welfare and proximity between farms set the limit long before the map does. The explanations do not rule one another out, but they lead to different political conclusions, and they have not been tested against one another on the same coast in the same year.

**Uneven knowledge base.** When sea goes to a farm, something else must yield, and the knowledge base for that trade-off is strikingly uneven. Organic load on soft seabed and the consequences of escape are thoroughly documented, while effects on hard seabed and the impacts of noise, light and physical structures are thinly covered. The duty to assess cumulative load follows from the Nature Diversity Act and the impact-assessment rules, but practice repeatedly shows weak treatment of how stressors act together.

**Municipal will.** All of this hangs on the municipalities' own interests. Because designation happens locally, national growth ambitions rest on local will, and the question of what municipalities get in return has followed the debate for decades. An area rent, a production fee and Havbruksfondet have changed the money flows, but whether that actually leads to more sea being designated remains unanswered. So does the question of where in the decision chain cases most often die: in the plan, in the sector refusal, or in the county's discretion. It is in this space of competing diagnoses, different area concepts and unsettled causal chains that the discussion of aquaculture's coastal area takes place.
""",
                    """
**Delt forvaltning.** Forvaltningen er delt mellom nivåer som hver har sin logikk. Kommunen peker ut sjøareal etter plan- og bygningsloven, ut til én nautisk mil utenfor grunnlinjene, og har dermed en nøkkelrolle som nasjonale vekstmål er avhengige av. Et anlegg trenger deretter både produksjonstillatelse og lokalitetstillatelse, og etter forvaltningsreformen i 2010 er det fylkeskommunen som samordner lokalitetssaken. Sektormyndighetene kan likevel avslå etter sine egne lover, slik at en søknad kan overleve planprosessen og stoppe et helt annet sted. Over dette ligger trafikklyssystemet med sine tretten produksjonsområder, som er et lokk på kapasitet og ikke et kart over hvor anleggene kan stå.

**Tre svar på hva som stopper veksten.** Hva som egentlig stopper veksten, er det sentrale stridsspørsmålet, og det finnes minst tre konkurrerende svar. Det ene peker på tillatelsesregimet: det står ikke på sjøflaten, men på produksjonstillatelser og kapasitetsgrenser. Det andre peker på kommunen, der gode lokaliteter er en begrenset ressurs og den politiske viljen til å avsette sjø avgjør hva som overhodet er tilgjengelig. Det tredje peker på biologien, der lus, sykdom, fiskevelferd og nærhet mellom anlegg setter grensen lenge før kartet gjør det. Forklaringene utelukker ikke hverandre, men de leder til ulike politiske konklusjoner, og de er ikke prøvd mot hverandre på samme kyst i samme år.

**Skjevt kunnskapsgrunnlag.** Når sjø går til anlegg, må noe annet vike, og kunnskapsgrunnlaget for den avveiingen er påfallende skjevt. Organisk belastning på bløtbunn og konsekvenser av rømming er grundig dokumentert, mens effekter på hardbunn og virkninger av støy, lys og fysiske strukturer er tynt belagt. Kravet om å vurdere samlet belastning følger av naturmangfoldloven og reglene om konsekvensutredning, men praksis viser gjentatte ganger svak behandling av hvordan påvirkningsfaktorer virker sammen.

**Kommunal vilje.** Alt henger sammen med kommunenes egne interesser. Fordi utpekingen skjer lokalt, hviler nasjonale vekstambisjoner på lokal vilje, og spørsmålet om hva kommunene får igjen har fulgt debatten i flere tiår. Arealavgift, produksjonsavgift og Havbruksfondet har endret pengestrømmene, men om det faktisk fører til at mer sjø blir pekt ut, står ubesvart. Det samme gjør spørsmålet om hvor i beslutningskjeden sakene oftest dør, i planen, i sektoravslaget eller i fylkets skjønn. Det er i dette rommet av konkurrerende diagnoser, ulike arealbegreper og uavklarte årsakskjeder at diskusjonen om havbrukets kystareal foregår.
""",
                )
            )
    with col_fig:
        fig_areal = REPO / "mockup" / "figur-arealbruk-snl.png"
        if fig_areal.exists():
            st.image(
                str(fig_areal),
                width=220,
                caption=tr(
                    lang,
                    "Land use, not the influence zone.",
                    "Arealbruk, ikke påvirkningssonen.",
                ),
            )
            st.caption(
                tr(
                    lang,
                    "Cited excerpt of the left panel at [SNL, Business in Norway](https://snl.no/næringsliv_i_Norge) (KF).",
                    "Sitert utdrag av venstre panel hos [SNL, Næringsliv i Norge](https://snl.no/næringsliv_i_Norge) (KF).",
                )
            )

# ── B: Norsk rammeverk ────────────────────────────────────────────────────────

section_header(
    tr(lang, "B · Current Norwegian framework", "B · Gjeldende norsk rammeverk"),
    tr(lang, "A split governing system", "Et delt styringssystem"),
)
with st.container(border=True):
    st.markdown(
        tr(
            lang,
            "Sea use is planned by the municipalities in the land-use part of the "
            "municipal master plan. The [Planning and Building Act](https://lovdata.no/dokument/NL/lov/2008-06-27-71) "
            "applies in the sea to **one nautical mile beyond the baselines** (section 1-2). "
            "Here sea is designated for aquaculture, fishing, navigation, nature and "
            "outdoor life, often as combined purposes.",
            "Arealbruken i sjø planlegges av kommunene i kommuneplanens arealdel. "
            "[Plan- og bygningsloven](https://lovdata.no/dokument/NL/lov/2008-06-27-71) "
            "gjelder i sjø ut til **én nautisk mil utenfor grunnlinjene** (§ 1-2). "
            "Her settes områder av til akvakultur, fiske, ferdsel, natur og friluftsliv, "
            "ofte som kombinerte formål.",
        )
    )
    st.markdown(
        tr(
            lang,
            "The permit to farm is given by the **county** under the "
            "[Aquaculture Act](https://lovdata.no/dokument/NL/lov/2005-06-17-79). From 2010 "
            "the county coordinates the locality case "
            "([coordination regulation](https://lovdata.no/dokument/SF/forskrift/2010-05-18-708)). "
            "Before a decision, the permits required by section 6 "
            "must be in place: the Food Safety Authority under the Food Act, the County "
            "Governor under the Pollution Control Act, the Coastal Administration under "
            "the Harbour and Fairway Act, and NVE under the Water Resources Act where "
            "relevant. The [Directorate of Fisheries comments on fisheries interests, "
            "including Sámi fisheries, and is the appeal body](https://mattilsynet.no/fisk-og-akvakultur/oppdrettsanlegg/saksgangen-i-etablering-og-utvidelse-av-akvakulturanlegg). "
            "It is not a section 6 permit authority. Sector authorities can also object "
            "to municipal plans. See the Directorate's "
            "[allocation process](https://www.fiskeridir.no/akvakultur/akvakultursoknader-hvordan-foregar-tildelingsprosessen).",
            "Tillatelsen til å drive havbruk gis av **fylkeskommunen** etter "
            "[akvakulturloven](https://lovdata.no/dokument/NL/lov/2005-06-17-79). Fra 2010 "
            "samordner fylket lokalitetssaken "
            "([samordningsforskriften](https://lovdata.no/dokument/SF/forskrift/2010-05-18-708)). "
            "Før vedtak må tillatelsene som kreves etter § 6 "
            "foreligge: Mattilsynet etter matloven, Statsforvalteren etter "
            "forurensningsloven, Kystverket etter havne- og farvannsloven, og NVE etter "
            "vannressursloven der det er aktuelt. [Fiskeridirektoratet uttaler seg om "
            "fiskeriinteresser, herunder samiske, og er klageorgan](https://mattilsynet.no/fisk-og-akvakultur/oppdrettsanlegg/saksgangen-i-etablering-og-utvidelse-av-akvakulturanlegg). "
            "Det er ikke tillatelsesmyndighet etter § 6. Sektormyndigheter kan også "
            "fremme innsigelse mot kommunale planer. Se direktoratets "
            "[tildelingsprosess](https://www.fiskeridir.no/akvakultur/akvakultursoknader-hvordan-foregar-tildelingsprosessen).",
        )
    )
    st.markdown(
        tr(
            lang,
            "The split means the municipality largely controls **where** aquaculture may "
            "take place, while the county and the state control **who** may produce and "
            "**how much**. Capacity in the production area is a separate lid. The system "
            "gives a broad professional review. It is also criticised as fragmented, "
            "slow and hard to predict. Because fjords, currents and infection do not "
            "follow municipal borders, municipalities have made intermunicipal coastal "
            "plans, including in Trøndelag and on Helgeland.",
            "Todelingen gjør at kommunen i stor grad styrer **hvor** havbruk kan "
            "ligge, mens fylket og staten styrer **hvem** som får produsere, og **hvor mye**. "
            "Kapasitet i produksjonsområdet er et eget lokk. Systemet gir bred faglig "
            "gjennomgang. Det kritiseres også for å være fragmentert, tidkrevende og "
            "uforutsigbart. Fordi fjorder, strøm og smitte ikke følger kommunegrenser, "
            "har kommuner laget interkommunale kystsoneplaner, blant annet i Trøndelag "
            "og på Helgeland.",
        )
    )
    st.markdown(
        tr(
            lang,
            """
<ol class="hl-chain">
  <li><strong>Municipal designation</strong>. Coastal-zone plans under the Planning and Building Act, to one nautical mile beyond the baselines. <a href="https://www.regjeringen.no/no/tema/plan-bygg-og-eiendom/plan_bygningsloven/planlegging/fagtema/planlegging_kyst/id2889076/">KDD on coastal sea planning</a>.</li>
  <li><strong>Production licence</strong>. The company's right to produce and the biomass it may hold (MTB). The stricter of company MTB and locality MTB binds.</li>
  <li><strong>Locality licence, county coordination</strong>. From 2010 the county runs the process and decides. <a href="https://lovdata.no/dokument/SF/forskrift/2010-05-18-708">Coordination regulation of 18 May 2010</a>.</li>
  <li><strong>Sector permits</strong>. Food Safety Authority, County Governor (pollution) and Coastal Administration can refuse under their own statutes, so no Aquaculture Act permit can be issued. NVE enters for freshwater intake. The County Governor's advice under the Nature Diversity Act is a guideline, not a veto.</li>
  <li><strong>Sanitary spacing</strong>. Infection control and recommended distance occupy far more sea than the pen. Live advice sits with the <a href="https://mattilsynet.no/fisk-og-akvakultur/oppdrettsanlegg/saksgangen-i-etablering-og-utvidelse-av-akvakulturanlegg">Food Safety Authority</a>.</li>
  <li><strong>Production areas and the traffic-light</strong>. The coast is coloured in 13 areas. Every other year, estimated lice impact on wild salmonids decides whether capacity can grow, freeze or be cut. <a href="https://www.fiskeridir.no/akvakultur/hva-er-trafikklyssystemet">Directorate of Fisheries</a>. <a href="https://lovdata.no/dokument/SF/forskrift/2017-01-16-61">Production area regulation</a>. Colour bands and mortality models belong in the wild-salmon room. The capacity lid belongs here.</li>
  <li><strong>Payment to the host municipality</strong>. Havbruksfondet, a production fee and resource-rent tax. See below.</li>
</ol>
""",
            """
<ol class="hl-chain">
  <li><strong>Kommunal utpeking</strong>. Kystsoneplaner etter plan- og bygningsloven, til én nautisk mil utenfor grunnlinjene. <a href="https://www.regjeringen.no/no/tema/plan-bygg-og-eiendom/plan_bygningsloven/planlegging/fagtema/planlegging_kyst/id2889076/">KDD om planlegging i kystnære sjøområder</a>.</li>
  <li><strong>Produksjonstillatelse</strong>. Selskapets rett til å produsere og biomassen det får holde (MTB). Den strengeste av selskaps-MTB og lokalitets-MTB binder.</li>
  <li><strong>Lokalitetstillatelse, fylket samordner</strong>. Fra 2010 kjører fylkeskommunen prosessen og fatter vedtak. <a href="https://lovdata.no/dokument/SF/forskrift/2010-05-18-708">Samordningsforskriften 18. mai 2010</a>.</li>
  <li><strong>Sektortillatelser</strong>. Mattilsynet, Statsforvalteren (forurensning) og Kystverket kan avslå etter egne lover, slik at tillatelse etter akvakulturloven ikke kan gis. NVE kommer inn ved ferskvannsinntak. Statsforvalterens råd etter naturmangfoldloven er retningslinje, ikke veto.</li>
  <li><strong>Smitteavstand</strong>. Smittevern og anbefalt avstand legger beslag på langt mer sjø enn merden. Levende råd ligger hos <a href="https://mattilsynet.no/fisk-og-akvakultur/oppdrettsanlegg/saksgangen-i-etablering-og-utvidelse-av-akvakulturanlegg">Mattilsynet</a>.</li>
  <li><strong>Produksjonsområder og trafikklys</strong>. Kysten fargelegges i 13 områder. Annethvert år avgjør beregnet lusepåvirkning på vill laksefisk om kapasiteten kan økes, fryses eller kuttes. <a href="https://www.fiskeridir.no/akvakultur/hva-er-trafikklyssystemet">Fiskeridirektoratet</a>. <a href="https://lovdata.no/dokument/SF/forskrift/2017-01-16-61">Produksjonsområdeforskriften</a>. Fargebånd og dødelighetsmodeller hører hjemme i villaks-rommet. Selve kapasitetslokket hører hjemme her.</li>
  <li><strong>Betaling til vertskommunen</strong>. Havbruksfondet, produksjonsavgift og grunnrenteskatt. Se under.</li>
</ol>
""",
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        tr(
            lang,
            "An adopted plan map and a granted permit do not automatically settle the "
            "case. Knowledge can be missing, postponed or applied unevenly in the "
            "municipal impact assessment and in the locality file. Precaution and "
            "professional judgement often run together, so the decisive ground can be "
            "hard to name. That is the strongest research gap in this corpus.",
            "Vedtatt plankart og gitt tillatelse avgjør ikke automatisk saken. Kunnskap "
            "kan mangle, utsettes eller brukes skjevt i kommunens konsekvensutredning og "
            "i lokalitetsfilen. Føre var og faglig skjønn løper ofte sammen, slik at den "
            "avgjørende grunnen kan være vanskelig å navngi. Det er det tyngste "
            "kunnskapshullet i dette korpuset.",
        )
    )
    st.markdown(
        tr(
            lang,
            "From the industry's side, **good localities** are often treated as the "
            "scarce input: depth, exchange, shelter and distance to other biomass. That "
            "is one diagnosis in the corpus. Others put production licences and the "
            "traffic-light first nationally, or lice, disease, welfare and proximity "
            "between farms. Climate change and warming sea water also shift where "
            "conditions are favourable. Area alone does not give growth. The traffic-light "
            "can freeze or cut capacity even where the plan has opened the sea. Green can "
            "offer up to 6 percent growth, yellow holds capacity, red can require a 6 "
            "percent cut "
            "([HI](https://www.hi.no/hi/temasider/akvakultur/trafikklyssystemet-hi-sin-kunnskap)). "
            "The system has been legally and scientifically contested, including because "
            "whole areas are treated collectively.",
            "Sett fra næringen behandles **gode lokaliteter** ofte som den knappeste "
            "innsatsfaktoren: dybde, vannutskifting, skjerming og avstand til annen "
            "biomasse. Det er én diagnose i korpuset. Andre setter produksjonstillatelser "
            "og trafikklys først nasjonalt, eller lus, sykdom, velferd og nærhet mellom "
            "anlegg. Klimaendring og oppvarming av sjøvann forskyver også hvor forholdene "
            "er gunstige. Areal alene gir ikke vekst. Trafikklyset kan fryse eller kutte "
            "kapasitet selv der planen har åpnet sjøen. Grønt kan gi inntil 6 prosent "
            "vekst, gult holder kapasiteten, rødt kan kreve 6 prosent kutt "
            "([HI](https://www.hi.no/hi/temasider/akvakultur/trafikklyssystemet-hi-sin-kunnskap)). "
            "Systemet har vært rettslig og faglig omstridt, blant annet fordi hele "
            "områder rammes kollektivt.",
        )
    )
    st.markdown(
        tr(
            lang,
            "**Sharing the value.** [Havbruksfondet](https://www.fiskeridir.no/akvakultur/havbruksfondet) "
            "was decided in 2015 and set up in 2016. It distributes municipal-sector "
            "income from sale of new capacity, and the production fee, mainly by cleared "
            "locality MTB. Payments swing with whether capacity is sold. A "
            "[production fee](https://www.skatteetaten.no/rettskilder/type/handboker/skatte-abc/gjeldende/a-11-akvakultur-havbruk/A-11.071/A-11.090/) "
            "from 1 January 2021 was meant to smooth that. The rate has been raised "
            "several times (98.5 øre per kilo slaughtered fish in 2026). "
            "[Resource-rent tax](https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p=93582) "
            "on salmon, trout and rainbow trout was adopted in 2023. The effective rate "
            "is 25 percent, with a 70 million kroner allowance per group. An earlier "
            "area-rent idea was found unsuited. Whether Havbruksfondet and the production "
            "fee actually get the municipality to designate more sea is untested in the "
            "research here.",
            "**Fordeling av verdiene.** [Havbruksfondet](https://www.fiskeridir.no/akvakultur/havbruksfondet) "
            "ble besluttet i 2015 og satt opp i 2016. Det fordeler kommunal sektors andel "
            "av inntekter fra salg av ny kapasitet, og produksjonsavgiften, i hovedsak "
            "etter klarert lokalitets-MTB. Utbetalingene svinger med om det selges "
            "kapasitet. En "
            "[produksjonsavgift](https://www.skatteetaten.no/rettskilder/type/handboker/skatte-abc/gjeldende/a-11-akvakultur-havbruk/A-11.071/A-11.090/) "
            "fra 1. januar 2021 skulle jevne det ut. Satsen er hevet flere ganger "
            "(98,5 øre per kilo sløyd fisk i 2026). "
            "[Grunnrenteskatt](https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p=93582) "
            "på laks, ørret og regnbueørret ble vedtatt i 2023. Effektiv sats er 25 "
            "prosent, med et bunnfradrag på 70 millioner kroner per konsern. En tidligere "
            "arealavgift ble funnet uegnet. Om Havbruksfondet og produksjonsavgiften "
            "faktisk får kommunen til å peke ut mer sjøareal, er uavklart i forskningen "
            "her.",
        )
    )
    with st.expander(
        tr(
            lang,
            "Read more: Havbruksutvalget, offshore, closed and land-based, and statutes",
            "Les mer: Havbruksutvalget, havbruk til havs, lukket og landbasert, og lover",
        )
    ):
        st.markdown(
            tr(
                lang,
                """
[NOU 2023: 23](https://www.regjeringen.no/no/dokumenter/nou-2023-23/id2995224/) (Havbruksutvalget, 28 September 2023) reviewed the permit and management system. It proposed, among other things, a clearer split of company licences and locality licences, **auction of company licences as the main rule**, locality licences on application without a fee, and a larger state role in sea-area planning. It did **not** propose an area tax or auction of the locality itself.

Three developments change the area picture, without solving it alone. They mainly change who must say yes, which interests collide, and where in the system the conflict sits.

**Aquaculture at sea.** Production moves out of the municipal plan area and into areas opened by the state. [Fiskeridirektoratet on allocation](https://www.fiskeridir.no/akvakultur/tildeling). On 27 February 2026 the King in Council decided that [Norskerenna sør, Frøyabanken nord and Trænabanken](https://www.regjeringen.no/no/aktuelt/kongelig-resolusjon-om-havbruk-til-havs-fastsatt/id3150415/) can be put out to tender. That can reduce local coastal conflict. It raises new questions about preparedness, welfare, cost, fisheries, and who receives the income when there is no host municipality.

**Closed and semi-closed farms at sea.** They can collect discharges and reduce lice pressure, and may give more production per unit of area. They need more energy, more infrastructure and larger investment. They are not yet at large scale.

**Land-based aquaculture.** It removes the sea-area conflict and moves it to the shoreline, the power grid, water intake and land discharge permits.

**Statutes**

- [Planning and Building Act](https://lovdata.no/dokument/NL/lov/2008-06-27-71) (LOV-2008-06-27-71)
- [Aquaculture Act](https://lovdata.no/dokument/NL/lov/2005-06-17-79) (LOV-2005-06-17-79)
- [Nature Diversity Act](https://lovdata.no/dokument/NL/lov/2009-06-19-100) (LOV-2009-06-19-100)
- [Production area regulation](https://lovdata.no/dokument/SF/forskrift/2017-01-16-61) (FOR-2017-01-16-61)
- [Pollution Control Act](https://lovdata.no/dokument/NL/lov/1981-03-13-6) (LOV-1981-03-13-6)
- [Harbour and Fairway Act](https://lovdata.no/dokument/NL/lov/2019-06-21-70) (LOV-2019-06-21-70)
- [Sámi Act chapter 4](https://lovdata.no/dokument/NL/lov/1987-06-12-56/KAPITTEL_4)
- [Quality standard for wild Atlantic salmon](https://lovdata.no/dokument/SF/forskrift/2013-09-20-1109) (FOR-2013-09-20-1109)
""",
                """
[NOU 2023: 23](https://www.regjeringen.no/no/dokumenter/nou-2023-23/id2995224/) (Havbruksutvalget, 28. september 2023) gjennomgikk tillatelses- og forvaltningssystemet. Utvalget foreslo blant annet en klarere splitting av selskaps- og lokalitetstillatelse, **auksjon av selskapstillatelser som hovedregel**, lokalitetstillatelser etter søknad uten vederlag, og en større statlig rolle i sjøarealplanlegging. Det foreslo **ikke** en arealavgift, og ikke auksjon av selve lokaliteten.

Tre utviklingstrekk endrer arealbildet, uten å løse det alene. De endrer først og fremst hvem som må si ja, hvilke interesser som settes opp mot hverandre, og hvor i systemet konflikten havner.

**Havbruk til havs.** Produksjon flyttes ut av kommunenes planområde og inn i områder staten åpner. [Fiskeridirektoratet om tildeling](https://www.fiskeridir.no/akvakultur/tildeling). 27. februar 2026 fastsatte Kongen i statsråd at [Norskerenna sør, Frøyabanken nord og Trænabanken](https://www.regjeringen.no/no/aktuelt/kongelig-resolusjon-om-havbruk-til-havs-fastsatt/id3150415/) kan lyses ut. Det kan redusere lokal kystkonflikt. Det reiser nye spørsmål om beredskap, velferd, kostnader, fiskeriene, og hvem som skal få inntektene når det ikke finnes vertskommune.

**Lukkede og semilukkede anlegg i sjø.** De kan samle utslipp og redusere lusepress, og kan gi mer produksjon per arealenhet. De krever mer energi, mer infrastruktur og større investeringer. De er foreløpig ikke i stor skala.

**Landbasert oppdrett.** Det fjerner sjøarealkonflikten og flytter den til strandsonen, kraftnettet, vannuttak og utslippstillatelser på land.

**Lover**

- [Plan- og bygningsloven](https://lovdata.no/dokument/NL/lov/2008-06-27-71) (LOV-2008-06-27-71)
- [Akvakulturloven](https://lovdata.no/dokument/NL/lov/2005-06-17-79) (LOV-2005-06-17-79)
- [Naturmangfoldloven](https://lovdata.no/dokument/NL/lov/2009-06-19-100) (LOV-2009-06-19-100)
- [Produksjonsområdeforskriften](https://lovdata.no/dokument/SF/forskrift/2017-01-16-61) (FOR-2017-01-16-61)
- [Forurensningsloven](https://lovdata.no/dokument/NL/lov/1981-03-13-6) (LOV-1981-03-13-6)
- [Havne- og farvannsloven](https://lovdata.no/dokument/NL/lov/2019-06-21-70) (LOV-2019-06-21-70)
- [Sameloven kapittel 4](https://lovdata.no/dokument/NL/lov/1987-06-12-56/KAPITTEL_4)
- [Kvalitetsnorm for vill atlantisk laks](https://lovdata.no/dokument/SF/forskrift/2013-09-20-1109) (FOR-2013-09-20-1109)
""",
            )
        )

# ── C: Åpne spørsmål ──────────────────────────────────────────────────────────

section_header(
    tr(lang, "C · Open questions", "C · Åpne spørsmål"),
    tr(
        lang,
        "Where growth stops, and where knowledge is missing",
        "Der veksten stopper, og der kunnskapen mangler",
    ),
)
with st.container(border=True):
    st.markdown(
        tr(
            lang,
            "A distinguishes pen area, locality area and plan area. B shows the split "
            "governing system, with public sources. "
            "This is not a room of two scientific camps on one estimate. The publications "
            "rarely rebut one another on a shared number. They write past one another on "
            "what limits growth, and the case file often postpones the hard part. The "
            "strongest gap in the set is knowledge in plans, impact assessment and "
            "locality processing. Pick an open question below.",
            "A skiller merdareal, lokalitetsareal og planareal. B viser det delte "
            "styringssystemet, med offentlige kilder. "
            "Dette er ikke et rom med to faglige leire om ett tall. Publikasjonene slår "
            "sjelden hverandre i hjel på et felles anslag. De skriver forbi hverandre om "
            "hva som begrenser vekst, og saksfilen utsetter ofte det harde. Det tyngste "
            "hullet i settet er kunnskap i plan, konsekvensutredning og "
            "lokalitetsbehandling. Velg et åpent spørsmål under.",
        )
    )

    fault_labels = [f[0] for f in FAULTS[lang]]
    fault_idx = st.selectbox(
        tr(lang, "Open question", "Åpent spørsmål"),
        options=list(range(len(fault_labels))),
        format_func=lambda i: fault_labels[i],
        key=f"areal_fault_long_{lang}",
    )

    st.markdown(FAULTS[lang][fault_idx][1])
    paper_chips(FAULT_PAPERS[fault_idx])

    st.write("")
    if st.button(tr(lang, "Ask the sources about this ↓", "Spør kildene om dette ↓")):
        st.session_state["areal_query"] = FAULTS[lang][fault_idx][2]
        st.rerun()

st.caption(
    tr(
        lang,
        "Editorial orientation · last reviewed 2026-09-17 · C and D search the active documents. "
        "Tagging codes A1-A6 sit in PRIORITY_QUESTIONS.md. A0 is the lead question, not a tag.",
        "Redaksjonell orientering · sist gjennomgått 2026-09-17 · C og D søker i de aktive dokumentene. "
        "Taggkodene A1-A6 står i PRIORITY_QUESTIONS.md. A0 er det ledende spørsmålet, ikke en tagg.",
    )
)

# ── D: Ask ────────────────────────────────────────────────────────────────────

section_header(
    tr(lang, "D · Ask the sources", "D · Spør kildene"),
    tr(lang, "Live synthesis", "Live syntese"),
)

if mode == "researcher":
    st.markdown(
        tr(
            lang,
            "Section C helps you see the open questions. Section D lets you ask a "
            "question. The tool retrieves from the curated set and returns a "
            "technical synthesis. Competing diagnoses are kept visible. Gaps are named "
            "when the file is empty.",
            "Seksjon C hjelper deg å se de åpne spørsmålene. Seksjon D lar deg stille "
            "et spørsmål. Verktøyet henter fra det kuraterte settet og returnerer "
            "en teknisk syntese. Konkurrerende diagnoser holdes synlige. Hull navngis når "
            "saksfilen er tom.",
        )
    )
else:
    st.markdown(
        tr(
            lang,
            "Section C helps you see the open questions. Section D lets you ask in plain "
            "language. The tool explains what the publications say, including where they "
            "write past one another, and where the file is empty.",
            "Seksjon C hjelper deg å se de åpne spørsmålene. Seksjon D lar deg spørre "
            "med enkelt språk. Verktøyet forklarer hva publikasjonene sier, også der de "
            "skriver forbi hverandre, og der saksfilen er tom.",
        )
    )

with st.container(border=True):
    examples = EXAMPLE_QUESTIONS[lang]
    pick = st.selectbox(
        tr(
            lang,
            "Example questions (mirror the points in C)",
            "Eksempelspørsmål (speiler punktene i C)",
        ),
        options=examples,
        format_func=lambda q: tr(lang, "Choose a question", "Velg et spørsmål") if q == "" else q,
        key=f"areal_example_long_{lang}",
    )
    if pick and st.session_state.get("_areal_example") != pick:
        st.session_state["areal_query"] = pick
        st.session_state["_areal_example"] = pick
    query = st.text_area(
        tr(lang, "Your question", "Spørsmålet ditt"),
        value=st.session_state.get("areal_query", ""),
        placeholder=tr(
            lang,
            "e.g. What limits aquaculture growth on the Norwegian coast: unused sea, licences, municipal designation, or biology?",
            "f.eks. Hva begrenser vekst i havbruk på norskekysten: mangel på sjøflate, tillatelser, kommunal utpeking, eller biologi?",
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
                f"Retrieves up to k = {top_k} by similarity among {len(selected_doc_ids) if selected_doc_ids else 0} active documents.",
                f"Henter opptil k = {top_k} etter likhet blant {len(selected_doc_ids) if selected_doc_ids else 0} aktive dokumenter.",
            )
        )

if run and query.strip():
    if not corpus_ready:
        st.error(tr(lang, "Corpus not ready.", "Korpuset er ikke klart."))
        st.stop()
    if not selected_doc_ids:
        st.error(
            tr(
                lang,
                "Select at least one document in the sidebar before querying.",
                "Velg minst ett dokument i sidepanelet før du spør.",
            )
        )
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
            data_file=AREAL_DATA_FILE,
        )
    if not results or is_out_of_scope(results):
        st.warning(
            tr(
                lang,
                "This question appears to fall outside this corpus. "
                "Try a question about sea area, locality or coastal-zone planning, or pick a point in section C.",
                "Spørsmålet ser ut til å ligge utenfor dette korpuset. "
                "Prøv et spørsmål om sjøareal, lokalitet eller kystsoneplan, eller velg et punkt i seksjon C.",
            )
        )
        st.stop()
    with st.spinner(tr(lang, "Writing synthesis...", "Skriver syntese...")):
        synthesis_text = synthesise(
            client,
            query.strip(),
            results,
            mode=mode,
            answer_format=answer_format,
            output_language=output_language,
            room="areal",
        )
    st.divider()
    st.subheader(tr(lang, "Synthesis", "Syntese"))
    st.markdown(synthesis_text)
    st.divider()
    st.subheader(tr(lang, f"Retrieved sources ({len(results)})", f"Hentede kilder ({len(results)})"))
    for r in results:
        cite = f"{_last_name(r.get('authors', ''))} {r.get('year', '')}".strip()
        title = r.get("title") or r.get("doc_id")
        with st.expander(f"**{cite}** · {title[:90]}"):
            st.markdown(f"**{title}**")
            doi_url = r.get("url") or (f"https://doi.org/{r['doi']}" if r.get("doi") else "")
            if doi_url:
                st.markdown(f"[DOI ↗]({doi_url})")
            if r.get("included_because"):
                st.markdown(r["included_because"])
            claims = [c for c in (r.get("key_claims") or []) if c and str(c).strip()]
            for claim in claims[:3]:
                st.markdown(f"- {claim}")
            if r.get("rag_summary"):
                with st.expander(tr(lang, "Summary", "Oppsummering"), expanded=False):
                    st.markdown(r["rag_summary"])
            qs = r.get("priority_questions") or []
            if qs:
                st.caption(" · ".join(str(q) for q in qs))
            st.caption(f"doc_id: `{r.get('doc_id', '')}`")

st.markdown(
    tr(
        lang,
        '<div class="hl-footer">Havbruksløftets Evidensrom. Draft room on area and aquaculture. '
        "Honest Broker: we show the open questions, competing diagnoses, and where the file is empty.</div>",
        '<div class="hl-footer">Havbruksløftets Evidensrom. Utkast-rom om areal og havbruk. '
        "Honest Broker: vi viser de åpne spørsmålene, konkurrerende diagnoser, og der saksfilen er tom.</div>",
    ),
    unsafe_allow_html=True,
)
