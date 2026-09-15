"""
Evidensrom: Areal og havbruk (working draft).

Orientering (A til C) + live Ask (D) mot isolert parquet
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
            "1. Knapphet: hva er det som binder vekst?",
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
            "Hva begrenser vekst i havbruk på norskekysten: mangel på ledig sjøflate, produksjons- og lokalitetstillatelser, kommunal utpeking av brukbar sjø, eller biologi (lus, sykdom, tetthet, velferd)?",
        ),
        (
            "2. Plan: hva avgjør utpekingen av sjøareal?",
            "Siden 1989-revisjonen er det kommunen som peker ut akvakultursjø. Vedtatt "
            "plankart er likevel ikke siste ord. Kvalvik og Robertsen (2017) og SALT 1065 "
            "viser at dispensasjon og daglig forvaltning kan åpne sjø planen ikke pekte "
            "ut. Sand (2025) viser kombinert formål som ser stort ut på kartet og likevel "
            "faller i søknad. Innsigelse og avslag fra sektormyndighet kan stanse saken "
            "etter at kartet er vedtatt. Sørdahl og Kvalvik (2024) og Sørdahl (2026) leser "
            "fem generasjoner Tromsø-planer: tykkere og mer helhetlige dokumenter avgjør "
            "ikke i seg selv hvilken sjø som pekes ut. Uenigheten er hvor konflikten "
            "sitter etter at kommunen har sagt ja eller nei.",
            "Når kommunen peker ut, eller nekter å peke ut, sjøareal til havbruk, hva avgjør dette: selve plankartet, senere dispensasjon, eller innsigelse og avslag fra sektormyndighet etter at kartet er vedtatt?",
        ),
        (
            "3. Tillatelser: hvor i stabelen dør saken?",
            "Et anlegg trenger produksjonstillatelse og lokalitetstillatelse. Fra 2010 "
            "samordner fylkeskommunen lokalitetssaken. Sandersen og Kvalvik (2014) "
            "beskriver den reformen som oppgaver uten reell myndighet: flere og mindre "
            "enheter. Osmundsen og Olsen (2025) skiller fylkeskoordinering, kommunal "
            "utpeking og sektornedlegg, og finner at fylket mangler verktøy til å legge om "
            "den strukturen som finnes. SALT 1110 leser 251 avslag fra 2020-2025. "
            "Mattilsynet er den hyppigst registrerte avslagsinstansen, og lus er den "
            "største kodede grunnen der. Fakta, skjønn og føre var løper ofte sammen. "
            "Schütz og Slater (2019) beskriver produksjonsområder og veien fra plan til "
            "lisens som et forutsigbarhetsproblem. Uenigheten er om knappheten sitter i "
            "tildelingsrunder, i veterinært avstandspress, eller i ugjennomsiktige avslag.",
            "Hvordan former produksjonstillatelse, lokalitetstillatelse og fylkesbehandling etter akvakulturloven hvem som får en lokalitet, og hvor i den stabelen saken dør?",
        ),
        (
            "4. Avveiing: hvilken bruk og hvilke verdier skal vike?",
            "Når sjø går til anlegg, må noe annet vike: en annen bruk (fiskeri, ferdsel, "
            "friluftsliv, forsvar, havvind), eller villaks, kysttorsk og bunnnatur som "
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
            "Når sjø går til havbruksanlegg, hva må vike (annen bruk, levende natur, eller anlegget), og hvordan tas samlet belastning inn når merden kommer i sjø som allerede brukes?",
        ),
        (
            "5. Saksfilen: hvordan brukes, mangler eller utsettes kunnskap?",
            "Hvis det er omstridt hva som er knapt, er planen og søknaden stedet der "
            "striden skulle avgjøres. Ofte skjer det ikke der. SALT 1065 skiller mellom "
            "det som hører hjemme i kommunens konsekvensutredning og det som hører hjemme "
            "i akvakulturlovsaken, og viser til Sivilombudets saker om usikkerhet i "
            "planfilen. SALT 1110 leser 251 avslag og finner at fakta, faglig skjønn og "
            "føre var ofte løper sammen, og at terskler for korall ikke er standardisert. "
            "Sørdahl (2024, 2026) argumenterer for at mer helhet i dokumentet ikke er mer "
            "avgjørelse. Mikkelsen (2025) og Evenset (2023) peker begge på samlet "
            "belastning som manglende kunnskap og svak praksis. Uenigheten gjelder "
            "hvordan usikkerhet skal inn i vedtaket, ikke hvilken studie som mangler.",
            "Hvilken kunnskap brukes, mangler, utsettes eller brukes skjevt i plan, KU og lokalitetsbehandling av havbruk, og hvordan skal usikkerhet og føre var inn i vedtaket?",
        ),
        (
            "6. Tetthet: er «mer areal» feil grep hvis biologien binder først?",
            "Veterinære avstander og smitte mellom naboanlegg legger beslag på langt mer "
            "sjø enn merden, og både Hersoug (2020) og Sand (2025) gjentar det. "
            "Kulmambetova og Tveterås (2025) finner at tettere naboer henger sammen med "
            "høyere produksjonskostnad. Gullestad (2011) foreslo produksjonsområder og "
            "samordnet brakklegging, uten å fastsette sonestørrelse. Rapporten om "
            "bærekraftig arealbruk (2023) vil ha tetthetsregler og bestrider "
            "trafikklyskutt, mens HI (2026) beskriver bæreevnen per produksjonsområde som "
            "lite kjent. Binder biologi og avstand først, er «mer areal» feil politisk "
            "setning. Trafikklyset er da et lokk på vekst, ikke et argument for mer "
            "sjøflate. Aldrin (2011-2017), Qviller (2024) og Moldal (2026) ligger i "
            "mappen som nabotekster om spredning.",
            "Hva følger av hvor og hvor tett havbruksanleggene ligger for produktivitet, sykdom, lus og belastning, og er «mer areal» feil grep hvis avstand og biologi binder først?",
        ),
        (
            "7. Penger: åpner skatt og fond den kommunale porten?",
            "Kommunen peker ut sjøen, så nasjonale vekstmål hviler på lokal vilje. Penger "
            "er grepet som oftest foreslås. Sandersen og Kvalvik (2015) kaller "
            "arealavgiften et wicked problem: miljøkonflikt, annen bruk og lav lokal "
            "avkastning etter at eierskapet ble konsentrert. De beskriver et verstefall "
            "der kommunen tar pengene og likevel ikke vil peke ut mer sjø. Arealavgift "
            "ble funnet uegnet som instrument, og senere kom eiendomsskatt på sjøanlegg, "
            "produksjonsavgift og Havbruksfondet (Hersoug 2020). Rosendal (2025) kobler "
            "kommunal økonomi til miljøhensyn. Om penger faktisk åpner mer sjøareal, har "
            "ingen av tekstene testet.",
            "Hvordan påvirker skatt, fond og arealavgiftsdebatten kommunenes vilje til å huse havbruksanlegg, og kan kommunen ta pengene uten å åpne mer sjøareal?",
        ),
    ],
    "en": [
        (
            "1. Scarcity: what is it that binds growth?",
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
            "What limits aquaculture growth on the Norwegian coast: lack of unused sea surface, production and locality licences, municipal designation of usable sea, or biology (lice, disease, density, welfare)?",
        ),
        (
            "2. Plans: what decides designation of sea area?",
            "Since the 1989 revision it is the municipality that designates aquaculture "
            "sea. An adopted plan map is still not the last word. Kvalvik and Robertsen "
            "(2017) and SALT 1065 show that dispensation and day-to-day management can "
            "open sea the plan did not designate. Sand (2025) shows combined-purpose "
            "zoning that looks large on the map and still fails at application. Sector "
            "objection and refusal can stop the case after the map is adopted. Sørdahl "
            "and Kvalvik (2024) and Sørdahl (2026) read five generations of Tromsø "
            "plans: thicker, more comprehensive documents do not by themselves settle "
            "which sea is designated. The disagreement is where the conflict sits after "
            "the municipality has said yes or no.",
            "When a municipality designates, or refuses to designate, sea area for aquaculture, what decides this: the plan map itself, later dispensation, or sector objection and refusal after the map is adopted?",
        ),
        (
            "3. Licences: where in the stack does the case die?",
            "A farm needs a production licence and a locality licence. From 2010 the "
            "county coordinates the locality case. Sandersen and Kvalvik (2014) describe "
            "that reform as tasks without real authority: more units, and smaller ones. "
            "Osmundsen and Olsen (2025) separate county coordination, municipal "
            "designation and sector vetoes, and find that the county lacks tools to "
            "recast the structure that exists. SALT 1110 reads 251 refusals from "
            "2020-2025. The Food Safety Authority is the most frequent recorded refuser, "
            "and lice is the largest coded ground there. Facts, judgement and "
            "precaution often run together. Schütz and Slater (2019) treat production "
            "areas and the path from plan to licence as a predictability problem. The "
            "disagreement is whether scarcity sits in allocation rounds, in veterinary "
            "spacing pressure, or in opaque refusals.",
            "How do production licences, locality licences and county administration of the Aquaculture Act shape who gets a site, and where in that stack does the case die?",
        ),
        (
            "4. Trade-off: whose use and which values must give way?",
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
            "When sea goes to an aquaculture farm, what must yield (other use, living nature, or the farm), and how is cumulative load taken in when the pen enters sea that is already in use?",
        ),
        (
            "5. The case file: how is knowledge used, missing, or postponed?",
            "If what is scarce is disputed, the plan and the application are where that "
            "dispute should be settled. Often it is not settled there. SALT 1065 "
            "separates what belongs in the municipal impact assessment from what belongs "
            "in the Aquaculture Act case, and points to Ombudsman cases on uncertainty in "
            "the plan file. SALT 1110 reads 251 refusals and finds that facts, "
            "professional judgement and precaution often run together, and that "
            "thresholds for coral are not standardised. Sørdahl (2024, 2026) argue that "
            "more holism in the document is not more decision. Mikkelsen (2025) and "
            "Evenset (2023) both point to cumulative load as missing knowledge and weak "
            "practice. The disagreement is about how uncertainty should enter the "
            "decision, not which study is missing.",
            "What knowledge is used, missing, postponed or applied unevenly in plans, impact assessment and locality processing of aquaculture, and how should uncertainty and precaution enter the decision?",
        ),
        (
            "6. Density: is more area the wrong move if biology binds first?",
            "Sanitary distances and infection between neighbouring farms claim far more "
            "sea than the pen, and both Hersoug (2020) and Sand (2025) repeat the point. "
            "Kulmambetova and Tveterås (2025) find that closer neighbours are associated "
            "with higher production cost. Gullestad (2011) proposed production areas and "
            "coordinated fallowing, without setting a zone size. The 2023 report on "
            "sustainable area use calls for density rules and disputes traffic-light "
            "cuts, while HI (2026) describes carrying capacity per production area as "
            "little known. If biology and distance bind first, more area is the wrong "
            "policy sentence. The traffic-light is then a lid on growth, not an argument "
            "for more sea surface. Aldrin (2011-2017), Qviller (2024) and Moldal (2026) "
            "sit in the file as neighbouring texts on spread.",
            "What follows from how densely and where aquaculture farms sit for productivity, disease, lice and load, and is more area the wrong move if distance and biology bind first?",
        ),
        (
            "7. Money: do tax and funds open the municipal gate?",
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
            "How do taxes, funds and the area-rent debate affect municipalities' willingness to host aquaculture farms, and can the municipality take the money without opening more sea area?",
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
                "Answers use plain language. They show both where the texts agree "
                "and where the diagnosis of the conflict still differs.",
                "Svarene bruker enkelt språk. De viser både der tekstene er enige, "
                "og der diagnosen av konflikten fortsatt skiller.",
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
        st.subheader(tr(lang, "Papers in corpus", "Artikler i korpuset"))
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
            tr(lang, "Include these papers", "Inkluder disse artiklene"),
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
            '<p class="hl-lede">Aquaculture needs coastal sea for farms. This room maps '
            "what the publications say binds growth and coexistence, and what must yield. "
            "Wild salmon belongs when it gates expansion in an area, including through "
            "the traffic-light.</p>",
            '<h1 class="hl-h1">Areal og havbruk</h1>'
            '<p class="hl-lede">Havbruk krever sjøareal til anlegg. Her kartlegges hva '
            "publikasjonene sier binder vekst og sameksistens, og hva som må vike. "
            "Villaks er med når den styrer om et område kan utvide, blant annet gjennom "
            "trafikklyset.</p>",
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
  <div class="hl-stat"><strong>{len(FAULTS['en'])}</strong><span>open dividing lines</span></div>
  <div class="hl-stat"><strong>15.09</strong><span>last reviewed</span></div>
</div>
""",
                f"""
<div class="hl-stats">
  <div class="hl-stat"><strong>{n_total or 39}</strong><span>dokumenter i korpuset</span></div>
  <div class="hl-stat"><strong>{span}</strong><span>tidsrom</span></div>
  <div class="hl-stat"><strong>{len(FAULTS['no'])}</strong><span>åpne skillelinjer</span></div>
  <div class="hl-stat"><strong>15.09</strong><span>sist gjennomgått</span></div>
</div>
""",
            ),
            unsafe_allow_html=True,
        )

st.caption(
    tr(
        lang,
        "Working draft. Priority questions are not confirmed by the three selectors. "
        "The corpus is 39 documents: 33 from the received set plus six added by Thord Håkon Bakke on 15 September 2026. Metadata was walked against the extracts.",
        "Arbeidsutkast. Prioritetsspørsmål er ikke bekreftet av de tre utvelgerne. "
        "Korpuset er 39 dokumenter: 33 fra den mottatte bunken pluss seks som Thord Håkon Bakke la inn 15. september 2026. Metadata er sjekket mot extract.",
    )
)

st.write("")

# ── A: Introduksjon ───────────────────────────────────────────────────────────

section_header(
    tr(lang, "A · Introduction", "A · Introduksjon"),
    tr(lang, "Editorial overview", "Redaksjonell oversikt"),
)
with st.container(border=True):
    col_a, col_diag = st.columns([1.35, 1])
    with col_a:
        st.markdown(
            tr(
                lang,
                "A new locality needs designated sea, licences, and room in a production "
                "area that can take more biomass. Fisheries, shipping, recreation, defence "
                "or conservation can meet the case. Wild salmon enters as living nature in "
                "the fjord, and as what colours the traffic-light. The question here is "
                "**what actually limits growth and coexistence for aquaculture along the "
                "Norwegian coast**, and what has to give way when sea still goes to a farm.",
                "En ny lokalitet trenger utpekt sjø, tillatelser og plass i et "
                "produksjonsområde som kan tåle mer biomasse. Fiskeri, ferdsel, "
                "friluftsliv, forsvar eller vern kan møte saken. Villaks kommer inn som "
                "levende natur i fjorden, og som det som fargelegger trafikklyset. Temaet "
                "her er **hva som faktisk begrenser vekst og sameksistens for havbruk langs "
                "norskekysten**, og hva som må vike når sjø likevel går til anlegg.",
            )
        )
        st.markdown(
            tr(
                lang,
                "The pen itself takes very little room. Gullestad (2011), Hersoug (2020) "
                "and Sand (2025) describe pen surface as a very small share of the sea "
                "inside the baseline. Moorings take more, and the sanitary distances to "
                "neighbouring farms take far more than the pen. Jentoft and Buanes (2005) "
                "call the picture of almost unlimited coastal space a myth: from the air "
                "the pens are dots, on the ground security zones make the industry "
                "space-consuming. A fjord can therefore look empty on the map and still be "
                "full as application space. This is where the publications part ways: is "
                "it unused sea surface, licences and the traffic-light, municipal "
                "designation, or biology that binds first?",
                "Selve merden tar svært lite plass. Gullestad (2011), Hersoug (2020) og "
                "Sand (2025) beskriver merdflaten som en svært liten del av sjøen innenfor "
                "grunnlinjen. Fortøyningene tar mer, og de veterinære avstandene til "
                "naboanlegg tar langt mer enn merden. Jentoft og Buanes (2005) kaller "
                "bildet av nesten ubegrenset kystplass en myte: fra luften er merdene "
                "prikker, på bakken gjør sikkerhetssoner næringen plasskrevende. En fjord "
                "kan derfor se tom ut på kartet og likevel være full som søknadsområde. "
                "Det er her publikasjonene skiller lag: er det ledig sjøflate, tillatelser "
                "og trafikklys, kommunens utpeking eller biologien som binder først?",
            )
        )
        with st.expander(
            tr(
                lang,
                "Read more: four kinds of area, and what the file leaves open",
                "Les mer: fire slags areal, og det saksfilen lar stå åpent",
            )
        ):
            st.markdown(
                tr(
                    lang,
                    """
A farm can look large on the municipal map and still fail as an application.
The texts keep several kinds of area apart: the surface the pen covers, the
surface the moorings require, the sea the municipality has designated in its
plan, and the sea closed off by sanitary distances to neighbouring farms.

**Typically well supported.** Pen surface is a very small share of the sea
inside the baseline. The municipality designates aquaculture sea under the
Planning and Building Act. A site also needs a production licence, a locality
licence, and clearance from the sector authorities. Food Safety Authority
distance guidance shrinks usable water far more than the pen does. Production
areas and the lice traffic-light came after Gullestad (2011). Later capacity
growth in 13 areas is tied to lice on wild salmonids. That is a lid on growth
in this room.

**More uncertain.** What binds growth in which region. Whether a fee or a fund
makes municipalities designate more sea. What belongs in the coastal-zone plan
and what belongs in the Aquaculture Act file. How precaution and cumulative
load should enter a refusal. How much closed, land-based or offshore farming
would ease pressure on the coast. Whether thicker, more holistic plans settle
which sea is designated (Sørdahl 2024, 2026).

**Recurring gaps.** No text tests the four scarcity answers on the same coast
and the same years. Whether money opens designation is untested. Dispensations
can open sea the plan did not designate. Refusal grounds often mix facts,
judgement and precaution. The chain from activity to stressor to effect,
including cumulative load, is named as deficient. Evenset (2023) found no
published literature on other industries harming farms.

Jentoft and Buanes (2005) is the named argument that empty-looking sea is a
management myth. Sandersen and Kvalvik (2014) is the 2010-reform companion to
Osmundsen and Olsen (2025). Schütz and Slater (2019) places aquaculture beside
offshore wind in the same legal allocation problem. Meld. St. 35 (2023-2024)
places aquaculture as one sector in use and conservation, and says the
traffic-light and the wild-salmon quality standard do not share a goal.

Aldrin on the spread of ISA, PD and lice, Qviller (2024), Moldal (2026),
HI (2026), Gismervik (2020) and IPBES (2022) sit in the folder as neighbouring
texts on spread, health and values. Two Kvalvik and Robertsen 2017 PDFs are the
same article.
""",
                    """
Et anlegg kan se stort ut på kommunekartet og likevel falle som søknad.
Tekstene holder flere slags areal fra hverandre: flaten merden dekker, flaten
fortøyningen krever, sjøen kommunen har pekt ut i plan, og sjøen som er stengt
av veterinære avstander til naboanleggene.

**Typisk god støtte.** Merdflaten er en svært liten del av sjøen innenfor
grunnlinjen. Kommunen peker ut akvakultursjø etter plan- og bygningsloven. En
lokalitet trenger også produksjonstillatelse, lokalitetstillatelse og klarering
fra sektormyndighetene. Mattilsynets avstandsråd krymper brukbart vann langt
mer enn merden gjør. Produksjonsområder og lusetrafikklys kom etter Gullestad
(2011). Senere kapasitetsvekst i 13 områder knyttes til lus på vill laksefisk.
Det er et lokk på vekst i dette rommet.

**Mer usikkert.** Hva som binder vekst i hvilken region. Om avgift eller fond
får kommuner til å peke ut mer sjø. Hva som hører hjemme i kystsoneplanen, og
hva som hører hjemme i akvakulturlovsaken. Hvordan føre var og samlet
belastning skal inn i et avslag. Hvor mye lukket, landbasert eller havbasert
drift ville lettet presset på kysten. Om tykkere og mer helhetlige planer
avgjør hvilken sjø som pekes ut (Sørdahl 2024, 2026).

**Kunnskapshull.** Ingen tekst prøver de fire knapphetssvarene mot samme kyst
og samme år. Om penger åpner utpeking er utestet. Dispensasjoner kan åpne sjø
som planen ikke pekte ut. Avslagsgrunner blander ofte fakta, skjønn og føre
var. Kjeden fra aktivitet til påvirkning til effekt, inkludert samlet
belastning, navngis som mangelfull. Evenset (2023) fant ingen publisert
litteratur om at andre næringer skader anlegg.

Jentoft og Buanes (2005) er det navngitte argumentet for at sjø som ser tom ut
er en forvaltningsmyte. Sandersen og Kvalvik (2014) er 2010-reformens
følgetekst til Osmundsen og Olsen (2025). Schütz og Slater (2019) setter
havbruk ved siden av havvind i samme juridiske fordeling. Meld. St. 35
(2023-2024) plasserer havbruk som én sektor i bruk og bevaring, og sier at
trafikklys og kvalitetsnorm for villaks ikke styrer mot samme mål.

Aldrin om spredning av ILA, PD og lus, Qviller (2024), Moldal (2026), HI (2026),
Gismervik (2020) og IPBES (2022) ligger i mappen som nabotekster om spredning,
helse og verdier. To Kvalvik og Robertsen 2017-PDF-er er samme artikkel.
""",
                )
            )
    with col_diag:
        st.markdown(
            tr(
                lang,
                '<p class="hl-label">Four answers to what binds growth</p>',
                '<p class="hl-label">Fire svar på hva som binder vekst</p>',
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            tr(
                lang,
                "**Unused sea surface.** Jentoft and Buanes (2005) name the picture of "
                "almost unlimited coastal space as a myth. Hersoug, Mikkelsen and "
                "Osmundsen (2020) say lack of unused sea is not the national limit, even "
                "though some regions are full.",
                "**Ledig sjøflate.** Jentoft og Buanes (2005) kaller bildet av nesten "
                "ubegrenset kystplass en myte. Hersoug, Mikkelsen og Osmundsen (2020) "
                "sier at mangel på ledig sjø ikke er den nasjonale grensen, selv om noen "
                "regioner er fulle.",
            )
        )
        st.markdown(
            tr(
                lang,
                "**Licences and the traffic-light.** Hersoug, Mikkelsen and Osmundsen "
                "(2020) put production licences and the traffic-light first. The "
                "traffic-light colours 13 production areas by lice on wild salmonids and "
                "gates whether capacity there can grow.",
                "**Tillatelser og trafikklys.** Hersoug, Mikkelsen og Osmundsen (2020) "
                "setter produksjonstillatelser og trafikklys først. Trafikklyset "
                "fargelegger 13 produksjonsområder etter lus på vill laksefisk og styrer "
                "om kapasiteten der kan økes.",
            )
        )
        st.markdown(
            tr(
                lang,
                "**Good sites and municipal will.** Sandersen and Kvalvik (2015) and "
                "Gullestad (2011) locate scarcity in good sites and in municipal "
                "designation. Osmundsen and Olsen (2025) add that the county lacks tools "
                "to recast the site structure that already exists.",
                "**Gode lokaliteter og kommunal vilje.** Sandersen og Kvalvik (2015) og "
                "Gullestad (2011) ser knappheten i gode lokaliteter og i kommunens "
                "utpeking. Osmundsen og Olsen (2025) legger til at fylkeskommunen mangler "
                "verktøy til å legge om den lokalitetsstrukturen som allerede finnes.",
            )
        )
        st.markdown(
            tr(
                lang,
                "**Biology before pen space.** Sand (2025) and Kulmambetova and Tveterås "
                "(2025) put lice, disease, welfare and proximity between farms first. The "
                "2023 report on sustainable area use calls for density rules and disputes "
                "traffic-light cuts. HI (2026) describes carrying capacity per production "
                "area as little known.",
                "**Biologi før merdplass.** Sand (2025) og Kulmambetova og Tveterås (2025) "
                "setter lus, sykdom, velferd og nærhet mellom anlegg først. Rapporten om "
                "bærekraftig arealbruk (2023) vil ha tetthetsregler og bestrider "
                "trafikklyskutt. HI (2026) beskriver bæreevnen per produksjonsområde som "
                "lite kjent.",
            )
        )

# ── B: Norsk rammeverk ────────────────────────────────────────────────────────

section_header(
    tr(lang, "B · Current Norwegian framework", "B · Gjeldende norsk rammeverk"),
    tr(lang, "Regulatory context", "Reguleringskontekst"),
)
with st.container(border=True):
    st.markdown(
        tr(
            lang,
            "A farm needs more than a point on the map. The municipality designates "
            "aquaculture sea in the coastal-zone plan under the **Planning and Building "
            "Act**. The company needs a **production licence** and a **locality licence** "
            "under the **Aquaculture Act**. From 2010 it is the **county** that "
            "coordinates the locality case and takes the decision. Sandersen and Kvalvik "
            "(2014) describe that reform as tasks without real authority. Osmundsen and "
            "Olsen (2025) is the later account of how counties actually ran the Act. "
            "Along the way, several sector authorities can stop the case under their own "
            "statutes. **Capacity in the production area** is a separate lid: the "
            "traffic-light can freeze or cut growth even when the plan has opened the sea.",
            "Et anlegg trenger mer enn et punkt på kartet. Kommunen peker ut "
            "akvakultursjø i kystsoneplanen etter **plan- og bygningsloven**. Selskapet "
            "trenger **produksjonstillatelse** og **lokalitetstillatelse** etter "
            "**akvakulturloven**. Fra 2010 er det **fylkeskommunen** som samordner "
            "lokalitetssaken og fatter vedtak. Sandersen og Kvalvik (2014) beskriver den "
            "reformen som oppgaver uten reell myndighet. Osmundsen og Olsen (2025) er den "
            "senere beretningen om hvordan fylkene faktisk kjørte loven. Underveis kan "
            "flere sektormyndigheter stanse saken med hjemmel i egne lover. **Kapasitet i "
            "produksjonsområdet** er et eget lokk: trafikklyset kan fryse eller kutte "
            "vekst selv om planen har åpnet sjøen.",
        )
    )
    st.markdown(
        tr(
            lang,
            "Solås and colleagues (2015) point to what makes the system hard to read: "
            "**no body is assigned to weigh all interests for and against one site**. "
            "The municipality can open sea, leave it as multi-use area, or leave the plan "
            "unmade. A later refusal from the Food Safety Authority or the pollution "
            "authority can stop the site even if the plan has opened the water. Schütz "
            "and Slater (2019) add that production areas raise predictability for the "
            "company, while what decides a given case can still be unpredictable. Sørdahl "
            "(2024, 2026) finds that thicker coastal plans do not by themselves settle "
            "the designation.",
            "Solås og medforfattere (2015) peker på det som gjør systemet vanskelig å "
            "lese: **ingen instans er satt til å veie alle hensyn for og mot én "
            "lokalitet**. Kommunen kan åpne sjø, la den stå som flerbruksareal eller la "
            "planen ligge. Et senere avslag fra Mattilsynet eller "
            "forurensningsmyndigheten kan stanse lokaliteten selv om planen har åpnet "
            "sjøen. Schütz og Slater (2019) legger til at produksjonsområder øker "
            "forutsigbarheten for selskapet, mens det som avgjør en gitt sak likevel kan "
            "være uforutsigbart. Sørdahl (2024, 2026) finner at tykkere kystsoneplaner "
            "ikke i seg selv avgjør utpekingen.",
        )
    )
    st.markdown(
        tr(
            lang,
            """
<ol class="hl-chain">
  <li><strong>Municipal designation</strong>. Coastal-zone plans under the Planning and Building Act apply to one nautical mile beyond the baselines. Since the 1989 revision it is the municipality that opens sea for aquaculture (Sandersen and Kvalvik 2015, Hersoug 2020).</li>
  <li><strong>Production licence</strong>. The company's right to produce and the biomass it may hold. Hersoug (2022) maps ten licence systems that sit above the site.</li>
  <li><strong>Locality licence, county coordination</strong>. From 2010 the county runs the process and decides. Sandersen and Kvalvik (2014) find limited devolution: more units, little real authority. Osmundsen and Olsen (2025) find that counties largely met their delivery targets, but cannot sanction other agencies that overrun deadlines, and lack tools to recast the existing site structure.</li>
  <li><strong>Sector vetoes</strong>. Aquaculture Act section 6 gives the Food Safety Authority, the pollution authority, the Coastal Administration and (in freshwater) NVE an effective veto (Solås et al. 2015). The County Governor's advice under the Nature Diversity Act, including cumulative load in section 10, is a guideline, not a veto.</li>
  <li><strong>Sanitary distance</strong>. The recommended Food Safety Authority distances (2.5 km, or 5 km as a firebreak) appear as guidance in the 2015 map. They occupy far more sea than the pen.</li>
  <li><strong>Production areas and the traffic-light</strong>. Gullestad (2011) proposed production areas and coordinated fallowing. From 2016 the coast is coloured in 13 areas by lice on wild salmonids. Green, yellow and red gate whether capacity in that area can grow, freeze or be cut. That is a lid on growth in this room. The mortality estimates and the camps around them sit in the salmon-lice and wild-salmon room. Meld. St. 35 (2023-2024) says the traffic-light and the quality standard for wild salmon do not steer toward the same goal.</li>
  <li><strong>Payment to the host municipality</strong>. Property tax on sea installations, a production fee and Havbruksfondet came in place of a standing area rent. Whether money opens designation is something none of the texts has tested.</li>
</ol>
""",
            """
<ol class="hl-chain">
  <li><strong>Kommunal utpeking</strong>. Kystsoneplaner etter plan- og bygningsloven gjelder til én nautisk mil utenfor grunnlinjene. Siden 1989-revisjonen er det kommunen som åpner sjø for akvakultur (Sandersen og Kvalvik 2015, Hersoug 2020).</li>
  <li><strong>Produksjonstillatelse</strong>. Selskapets rett til å produsere og biomassen det får holde. Hersoug (2022) kartlegger ti tillatelsessystemer som ligger over lokaliteten.</li>
  <li><strong>Lokalitetstillatelse, fylket samordner</strong>. Fra 2010 kjører fylkeskommunen prosessen og fatter vedtak. Sandersen og Kvalvik (2014) finner begrenset delegering: flere enheter, liten reell myndighet. Osmundsen og Olsen (2025) finner at fylkene i stor grad innfridde leveransemålene, men at de ikke kan sanksjonere andre etater som sprenger frister, og at de mangler verktøy til å legge om eksisterende lokalitetsstruktur.</li>
  <li><strong>Sektorveto</strong>. Akvakulturloven § 6 gir Mattilsynet, forurensningsmyndigheten, Kystverket og (i ferskvann) NVE et reelt veto (Solås mfl. 2015). Statsforvalterens råd etter naturmangfoldloven, inkludert samlet belastning i § 10, er retningslinje, ikke veto.</li>
  <li><strong>Veterinær avstand</strong>. De anbefalte avstandene fra Mattilsynet (2,5 km, eller 5 km som branngate) står som veiledning i 2015-kartet. De legger beslag på langt mer sjø enn merden.</li>
  <li><strong>Produksjonsområder og trafikklys</strong>. Gullestad (2011) foreslo produksjonsområder og samordnet brakklegging. Fra 2016 fargelegges kysten i 13 områder etter lus på vill laksefisk. Grønt, gult og rødt styrer om kapasiteten i det området kan økes, fryses eller kuttes. Det er et lokk på vekst i dette rommet. Dødelighetsanslagene og leirene rundt dem ligger i rommet om lakselus og villaks. Meld. St. 35 (2023-2024) sier at trafikklys og kvalitetsnorm for villaks ikke styrer mot samme mål.</li>
  <li><strong>Betaling til vertskommunen</strong>. Eiendomsskatt på sjøanlegg, produksjonsavgift og Havbruksfondet kom i stedet for en stående arealavgift. Om penger åpner utpeking, har ingen av tekstene testet.</li>
</ol>
""",
        ),
        unsafe_allow_html=True,
    )
    with st.expander(
        tr(
            lang,
            "Read more: primary legal sources, and how practice has moved on",
            "Les mer: primære rettskilder, og hvordan praksisen har flyttet seg",
        )
    ):
        st.markdown(
            tr(
                lang,
                """
The chain above is the map the texts sit on. Osmundsen and Olsen (2025) is
the later account of county practice. SALT 1110 is the later account of
refusals. SALT 1065 is the planning-side account of knowledge in the file.

**Primary legal sources (Lovdata)**

- [Plan- og bygningsloven](https://lovdata.no/dokument/NL/lov/2008-06-27-71)
  (LOV-2008-06-27-71). Municipal designation in the coastal zone. Hersoug (2020)
  states that plans apply to one nautical mile beyond the baselines.
- [Akvakulturloven](https://lovdata.no/dokument/NL/lov/2005-06-17-79)
  (LOV-2005-06-17-79). Production licence, locality licence and sector
  clearance. Section 6 is the veto map in Solås et al. (2015). Mikkelsen et al.
  (2025) say the Act still has no explicit duty to assess cumulative load.
- [Naturmangfoldloven](https://lovdata.no/dokument/NL/lov/2009-06-19-100)
  (LOV-2009-06-19-100). Section 10 on cumulative load is a guideline. Other
  considerations may still decide. The assessment must be written down.
- [Produksjonsområdeforskriften](https://lovdata.no/dokument/SF/forskrift/2017-01-16-61)
  (FOR-2017-01-16-61). Thirteen production areas. Lice on wild salmonids is the
  environmental indicator for capacity. Colour bands and mortality models belong
  in the wild-salmon room. The capacity lid itself belongs here.
- [Forurensningsloven](https://lovdata.no/dokument/NL/lov/1981-03-13-6)
  (LOV-1981-03-13-6). Recipient capacity and nature in locality cases, including
  the refusals SALT 1110 reads.

In the 2015 map, 2.5 km and 5 km appear as guidance. Live distance advice
sits with the Food Safety Authority.

Meld. St. 35 (2023-2024) says the traffic-light and the quality standard for
wild salmon do not steer toward the same goal. That is a growth-target
conflict in this room, not a second lice-mortality question.
""",
                """
Kjeden over er kartet tekstene sitter på. Osmundsen og Olsen (2025) er
den senere beretningen om fylkespraksis. SALT 1110 er den senere beretningen om
avslag. SALT 1065 er plansidens beretning om kunnskap i saksfilen.

**Primære rettskilder (Lovdata)**

- [Plan- og bygningsloven](https://lovdata.no/dokument/NL/lov/2008-06-27-71)
  (LOV-2008-06-27-71). Kommunal utpeking i kystsonen. Hersoug (2020) sier at
  planene gjelder til én nautisk mil utenfor grunnlinjene.
- [Akvakulturloven](https://lovdata.no/dokument/NL/lov/2005-06-17-79)
  (LOV-2005-06-17-79). Produksjonstillatelse, lokalitetstillatelse og
  sektorklarering. § 6 er vetokartet hos Solås mfl. (2015). Mikkelsen mfl.
  (2025) sier at loven fortsatt mangler en uttrykkelig plikt til å vurdere
  samlet belastning.
- [Naturmangfoldloven](https://lovdata.no/dokument/NL/lov/2009-06-19-100)
  (LOV-2009-06-19-100). § 10 om samlet belastning er retningslinje. Andre
  hensyn kan likevel avgjøre. Vurderingen skal skrives ned.
- [Produksjonsområdeforskriften](https://lovdata.no/dokument/SF/forskrift/2017-01-16-61)
  (FOR-2017-01-16-61). Tretten produksjonsområder. Lus på vill laksefisk er
  miljøindikator for kapasitet. Fargebånd og dødelighetsmodeller hører hjemme i
  villaks-rommet. Selve kapasitetslokket hører hjemme her.
- [Forurensningsloven](https://lovdata.no/dokument/NL/lov/1981-03-13-6)
  (LOV-1981-03-13-6). Resipient og natur i lokalitetssaker, også i avslagene
  SALT 1110 leser.

I 2015-kartet står 2,5 km og 5 km som veiledning. Levende avstandsråd ligger
hos Mattilsynet.

Meld. St. 35 (2023-2024) sier at trafikklys og kvalitetsnorm for villaks ikke
styrer mot samme mål. Det er en målkonflikt for vekst i dette rommet, ikke et
andre lus-dødelighetsspørsmål.
""",
            )
        )

# ── C: Uenighetskart ──────────────────────────────────────────────────────────

section_header(
    tr(lang, "C · Where the publications disagree", "C · Hvor publikasjonene er uenige"),
    tr(lang, "Editorial disagreement map", "Redaksjonelt uenighetskart"),
)
with st.container(border=True):
    st.markdown(
        tr(
            lang,
            "The texts largely agree that pen surface is small, that the municipality "
            "designates the sea, and that a site can be stopped at several gates after "
            "the plan is adopted. They part ways when asked what binds: unused sea, "
            "licences and the traffic-light, the municipal map, biology, competing uses, "
            "the case file, or money. Pick a dividing line below.",
            "Tekstene er stort sett enige om at merdflaten er liten, at kommunen peker "
            "ut sjøen, og at en lokalitet kan stanses i flere porter etter planvedtaket. "
            "De skiller lag når de skal si hva som binder: ledig sjø, tillatelser og "
            "trafikklys, kommunens kart, biologi, konkurrerende bruk, saksfilen, eller "
            "penger. Velg en skillelinje under.",
        )
    )

    fault_labels = [f[0] for f in FAULTS[lang]]
    fault_idx = st.selectbox(
        tr(lang, "Dividing line / contested question", "Skillelinje / omstridt spørsmål"),
        options=list(range(len(fault_labels))),
        format_func=lambda i: fault_labels[i],
        key=f"areal_fault_{lang}",
    )

    st.markdown(f"**{fault_labels[fault_idx]}**")
    st.markdown(FAULTS[lang][fault_idx][1])
    paper_chips(FAULT_PAPERS[fault_idx])

    st.write("")
    if st.button(tr(lang, "Ask the sources about this ↓", "Spør kildene om dette ↓")):
        st.session_state["areal_query"] = FAULTS[lang][fault_idx][2]
        st.rerun()

st.caption(
    tr(
        lang,
        "Editorial orientation · last reviewed 2026-09-15 · Ask the sources searches the active documents. "
        "Tagging codes A1-A6 sit in PRIORITY_QUESTIONS.md. A0 is the lead question, not a tag.",
        "Redaksjonell orientering · sist gjennomgått 2026-09-15 · Spør kildene søker i de aktive dokumentene. "
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
            "Section C helps you orient in the evidence. Section D lets you ask a "
            "contested question. The tool retrieves from the curated set and returns a "
            "technical synthesis. Competing diagnoses are kept visible. Gaps are named "
            "when the file is empty.",
            "Seksjon C hjelper deg å orientere deg i evidensen. Seksjon D lar deg stille "
            "et omstridt spørsmål. Verktøyet henter fra det kuraterte settet og returnerer "
            "en teknisk syntese. Konkurrerende diagnoser holdes synlige. Hull navngis når "
            "saksfilen er tom.",
        )
    )
else:
    st.markdown(
        tr(
            lang,
            "Section C helps you orient in the evidence. Section D lets you ask in plain "
            "language. The tool explains what the publications say, including where they "
            "disagree on what the conflict is.",
            "Seksjon C hjelper deg å orientere deg i evidensen. Seksjon D lar deg spørre "
            "med enkelt språk. Verktøyet forklarer hva publikasjonene sier, også der de "
            "er uenige om hva konflikten er.",
        )
    )

with st.container(border=True):
    examples = EXAMPLE_QUESTIONS[lang]
    pick = st.selectbox(
        tr(
            lang,
            "Example questions (mirror the dividing lines in C)",
            "Eksempelspørsmål (speiler skillelinjene i C)",
        ),
        options=examples,
        format_func=lambda q: tr(lang, "Choose a question", "Velg et spørsmål") if q == "" else q,
        key=f"areal_example_{lang}",
    )
    if pick and st.session_state.get("_areal_example") != pick:
        st.session_state["areal_query"] = pick
        st.session_state["_areal_example"] = pick
    query = st.text_area(
        tr(lang, "Your question", "Spørsmålet ditt"),
        value=st.session_state.get("areal_query", ""),
        placeholder=tr(
            lang,
            "e.g. What limits aquaculture growth on the Norwegian coast: lack of unused sea surface, production and locality licences, municipal designation of usable sea, or biology (lice, disease, density, welfare)?",
            "f.eks. Hva begrenser vekst i havbruk på norskekysten: mangel på ledig sjøflate, produksjons- og lokalitetstillatelser, kommunal utpeking av brukbar sjø, eller biologi (lus, sykdom, tetthet, velferd)?",
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
                "Try a question about area, siting or coastal planning, or pick a dividing line in section C.",
                "Spørsmålet ser ut til å ligge utenfor dette korpuset. "
                "Prøv et spørsmål om areal, lokalitet eller kystsoneplan, eller velg en skillelinje i seksjon C.",
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
        "Honest Broker: we show where diagnoses and values differ, and where the file is empty.</div>",
        '<div class="hl-footer">Havbruksløftets Evidensrom. Utkast-rom om areal og havbruk. '
        "Honest Broker: vi viser der diagnoser og verdier skiller, og der saksfilen er tom.</div>",
    ),
    unsafe_allow_html=True,
)
