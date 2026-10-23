"""
Evidensrom: Areal og havbruk (prototype).

Bakgrunn (A og B) + åpne spørsmål som kort og Spør kildene (C) mot isolert
parquet data/area-and-aquaculture.parquet.
"""

from __future__ import annotations

import os
import sys
import time
import uuid
from pathlib import Path

import openai
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
    is_out_of_scope,
)
from routing import PQ_TITLES, PQ_TITLES_NO, classify_pq, pq_code_for_text, retrieve_funnel
import feedback
from regelverk import REGELVERK, render_regelverk
from synthesis import synthesise_stream
from ui import brand_header, inject_css, section_header

st.set_page_config(
    page_title="Areal og havbruk · Evidensrom",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()

LANG_OPTIONS = ["no", "en"]


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
    # Retries with backoff and a generous timeout ride out brief rate limits.
    return OpenAI(api_key=key, max_retries=3, timeout=120.0)


def _last_name(authors: str) -> str:
    if not authors:
        return "?"
    first = str(authors).split(";")[0].strip()
    parts = first.split()
    return parts[-1] if parts else "?"


def _surname(name: str) -> str:
    parts = name.split()
    if not parts:
        return ""
    # Organisations such as "Metier AS" keep their full name.
    return name if len(parts) > 1 and parts[-1].isupper() else parts[-1]


def _source_label(lang: str, authors, year, title) -> str:
    """Readable source name: "Hersoug mfl. 2020", "Sand og Misund 2025".
    Documents without authors (reports) get a short title instead."""
    try:
        yr = str(int(year))
    except (TypeError, ValueError):
        yr = ""
    names = [_surname(a.strip()) for a in str(authors or "").split(";") if a.strip()]
    if not names:
        short = str(title or "").strip()
        if len(short) > 40:
            short = short[:40].rsplit(" ", 1)[0].rstrip(",.:;") + "…"
        return f"{short} ({yr})" if short and yr else short or yr
    if len(names) == 1:
        who = names[0]
    elif len(names) == 2:
        who = f"{names[0]} {tr(lang, 'and', 'og')} {names[1]}"
    else:
        who = f"{names[0]} {tr(lang, 'et al.', 'mfl.')}"
    return f"{who} {yr}".strip()


# ── Open questions (C) ───────────────────────────────────────────────────────────

FAULTS = {
    "no": [
        (
            "1. Hva bestemmer hvor og i hvilket omfang havbruk kan etableres og utvikles, og hvordan avveies hensynet til miljø, næringsutvikling og annen arealbruk?",
            "Hvis merden tar så lite plass, hva er det da som setter grensen? Hersoug, "
            "Mikkelsen og Osmundsen (2020) svarer at den nasjonale grensen den gangen "
            "lå i produksjonstillatelser og trafikklys, selv om avstandskrav og andre "
            "bruk krymper det som kan brukes, og noen regioner er fulle. Sandersen og "
            "Kvalvik (2015) og Gullestad-utvalget (2011) legger knappheten i gode "
            "lokaliteter og i kommunens vilje til å peke ut sjø. Rapporten om "
            "bærekraftig arealbruk (2023) spør om en stor produksjonsøkning er mulig "
            "når miljø, fiskevelferd og økonomi veies sammen, og svarer at det ikke "
            "går med dagens teknologi og drift. Nofima-rapporten om det rettslige "
            "rammeverket (2015) finner at en isolert miljønektelse kan stoppe en "
            "lokalitet selv om en samlet avveining av næring, arbeidsplasser og smitte "
            "ville pekt en annen vei. Diagnosene er skrevet forbi hverandre. Ingen "
            "tekst prøver dem mot samme kyst og samme år.",
            "Hva bestemmer hvor og i hvilket omfang havbruk kan etableres og utvikles, og hvordan avveies hensynet til miljø, næringsutvikling og annen arealbruk i dagens arealforvaltning?",
        ),
        (
            "2. Hvilke faktorer påvirker muligheten for utvikling av havbruk langs kysten, og hvordan samvirker arealtilgang, tillatelser, planlegging og miljø- og fiskehelse?",
            "Utvikling langs kysten hviler på at flere ordninger treffer samme lokalitet. "
            "Hersoug (2022) skiller produksjonstillatelsen, som trafikklyset styrer, fra "
            "lokalitetstillatelsen, som må ligge i kommunens arealplan. Gullestad-utvalget "
            "(2011) og Hersoug, Mikkelsen og Osmundsen (2020) knytter arealstrukturen til "
            "lus, rømming, tap og avstand mellom anlegg. Sand og Misund (2025) viser at "
            "klarert lokalitetskapasitet i Trøndelag er langt større enn selskapskapasiteten, "
            "fordi brakklegging og flytterestriksjoner krever flere lokaliteter enn "
            "tillatelsene dekker. Kvalvik og Robertsen (2017) og Mikkelsen, Karlsen og "
            "Osmundsen (2019) viser at kommunens plan er porten, mens større planområder "
            "og felles kart likevel gir få sikre nye arealer til havbruk. Myklebust "
            "(2018, 2021) viser hvor langt kommunen kan gå med miljøvilkår i planen før "
            "lokalitetssaken etter akvakulturloven tar over. Det åpne spørsmålet er hvilken "
            "faktor som binder først, og hvor de trekker i hver sin retning.",
            "Hvilke faktorer påvirker muligheten for utvikling av havbruk langs kysten, og hvordan samvirker forhold som arealtilgang, tillatelsessystem, arealplanlegging, og miljø- og fiskehelsehensyn?",
        ),
        (
            "3. Hvordan praktiseres søknadsprosessen om lokaliteter, og hvor stopper, forsinkes eller konflikter den oftest?",
            "Spørsmålet gjelder lokalitetssaken. Søknaden går til fylkeskommunen, som "
            "ikke kan gi tillatelse hvis Mattilsynet, Statsforvalteren eller Kystverket "
            "avslår, eller hvis plasseringen strider mot planen. Osmundsen og Olsen "
            "(2025) finner at tidsfristene oftere ryker hos Mattilsynet og "
            "Statsforvalteren enn hos fylket, og at ufullstendige og strategiske "
            "søknader stopper køen. SALT 1110 gjennomgår 251 avslag fra 2020 til 2025. "
            "Smitterisiko dominerer Mattilsynets avslag. Evenset med flere (2023) "
            "beskriver den samme vetoretten og skjønnet i om lokaliteten er miljømessig "
            "forsvarlig. Sand og Misund (2025) gjengir at søknader i Osen ofte får "
            "avslag fordi kommunen ligger øverst i en smittevernsone. Nofima-rapporten "
            "fra 2015 viser at selv små justeringer kan kreve en full lokalitetssøknad. "
            "Det som fortsatt er åpent, er hvor mye av forsinkelsen som skyldes "
            "kunnskapsmangel, og hvor mye som skyldes at etatene verner hvert sitt hensyn.",
            "Hvordan praktiseres søknadsprosessen om lokaliteter, og i hvilke deler av prosessen oppstår søknadsstopp, forsinkelser eller konflikter oftest?",
        ),
        (
            "4. Hvordan vurderes kumulative effekter av akvakultur i arealplanlegging og lokaliseringsbeslutninger, og hvilke kunnskapsutfordringer beskrives?",
            "Samlet belastning er noe annet enn konflikten med én annen bruker. Mikkelsen "
            "med flere (2025) viser at konsekvensutredningsforskriften krever vurdering "
            "av samlede påvirkninger, men ikke sier hvordan, og at akvakulturloven har "
            "helhetlige vurderinger uten en uttrykkelig plikt til å vurdere samlet "
            "påvirkning. Evenset med flere (2023) går gjennom kumulative miljøvirkninger "
            "og finner metode- og datahull. Saksbehandlerne sliter særlig med å avveie "
            "vekst mot miljørisiko og med samlede virkninger. SALT 1065 finner at "
            "vurderingene av samlede virkninger over større arealer kunne vært bedre, "
            "og at smitte og lus i stor grad bør ligge hos andre enn kommuneplanens "
            "konsekvensutredning. Sandersen (2021) viser at omvendt planmetodikk på "
            "Helgeland flyttet konfliktavklaringen ut av planen og gjorde samlet "
            "belastning vanskelig å vurdere. Gullestad-utvalget (2011) foreslo "
            "produksjonsområder fordi anlegg påvirker hverandre på tvers av "
            "kommunegrenser. Hullet er metoden: lovene krever en samlet vurdering, mens "
            "tekstene er uenige om hvem som skal gjøre den, og med hvilket grunnlag.",
            "Hvordan vurderes kumulative effekter av akvakulturproduksjon i arealplanlegging og lokaliseringsbeslutninger for havbruk, og hvilke kunnskapsmessige og metodiske utfordringer beskrives?",
        ),
        (
            "5. Hvordan påvirker økonomiske virkemidler og regulering insentivene til arealbruk og lokaliseringsvalg, og hvordan fordeles gevinster og kostnader?",
            "Kommunen peker ut sjøen, og flere tekster spør om penger endrer den viljen. "
            "Sandersen og Kvalvik (2015) kaller arealavgiften et fastlåst problem: "
            "staten vil unngå et nytt skatteinstrument, næringen vil betale for vekst "
            "heller enn for eksisterende lokaliteter, og kommunene vil ha en stabil "
            "andel. De beskriver et verstefall der kommunen får pengene og likevel "
            "ikke peker ut mer sjø. Hersoug, Mikkelsen og Osmundsen (2020) følger det "
            "som kom etterpå: Havbruksfondet og en produksjonsavgift, og at legitimitet "
            "for mer areal hviler på en fordeling kommunene opplever som rimelig. "
            "Aanesen og Mikkelsen (2020) finner at overføringene fra fondet ofte ikke "
            "veier opp for husholdningenes verdsetting av å unngå mer havbruk, med "
            "mindre en del av produsentoverskuddet blir i regionen. Iversen med flere "
            "(2025) beskriver grunnrenteskatten og at auksjonsinntektene deles mellom "
            "vertskommuner og fylker. Misund med flere (2023) finner at folk i "
            "havbrukskommuner er mer positive til næringen, og likevel ikke mer fornøyde "
            "med fordelingen. Om pengene faktisk åpner mer sjø, er ikke testet i settet.",
            "Hvordan påvirker økonomiske virkemidler og regulering insentivene til arealbruk og lokaliseringsvalg, og hvordan fordeles gevinster og kostnader mellom aktørene?",
        ),
        (
            "6. Hvilket kunnskapsgrunnlag legges til grunn for arealbeslutninger, og hvordan kan ny teknologi endre arealbruk og lokalisering?",
            "Kunnskapsgrunnlaget for arealvedtak er ujevnt, og ny teknologi kan flytte "
            "hvor anlegg kan ligge. Robertsen med flere (2014) og SALT 1065 spør "
            "hvilket grunnlag kommunene bruker i kystsoneplanene, og finner at temadata "
            "er dårlig tilrettelagt og at vurderingene varierer. Mikkelsen, Sørdahl og "
            "Solås (2022) sammenligner konsekvensvurderinger av 143 foreslåtte "
            "havbruksområder og finner svak konsistens i hva som vektes. Metier (2023) "
            "anslår at marine grunnkart kan redusere risikoen ved nye lokaliteter, "
            "blant annet gjennom strøm og lus. SALT 1110 peker på kunnskapsbehov i "
            "avslagspraksisen. Hersoug, Mikkelsen og Osmundsen (2020) og rapporten om "
            "bærekraftig arealbruk (2023) går gjennom landbasert produksjon, havbasert "
            "produksjon, stor smolt og lukkede merder, og sier at behovet for skjermet "
            "kystareal avhenger av om disse konseptene blir lønnsomme. Sand og Misund "
            "(2025) gjengir forslaget om et forskningssenter for arealbruk og statlige "
            "planretningslinjer. Hvor mye den nye teknologien faktisk flytter "
            "lokaliteter, er fortsatt kvalitativt.",
            "Hvilket kunnskapsgrunnlag legges til grunn for arealbeslutninger i havbruk, og hvordan kan ny teknologi endre forutsetningene for arealbruk, miljøpåvirkning og lokaliseringsmuligheter?",
        ),
        (
            "7. Hvilke konflikter oppstår mellom havbruk og andre interesser i plan og lokalisering, og hva bidrar til legitime og forutsigbare prosesser?",
            "Konflikten står mellom havbruk og andre bruk av den samme sjøen, og mellom "
            "lokal utpeking og statlige sektorinteresser. Jentoft og Buanes (2005) "
            "kaller bildet av nesten ubegrenset kystplass en myte: fra luften er "
            "merdene prikker, på bakken gjør sikkerhetssoner næringen plasskrevende, og "
            "brukskonflikter kan ikke skyves unna. Kvalvik og Robertsen (2017) og "
            "Sandersen (2021) viser at interkommunal planlegging koordinerer prosessen, "
            "mens utpeking av sjø til havbruk ofte faller tilbake til den enkelte "
            "kommunen når interessene spriker. Bjørkan og Eilertsen (2020) finner et "
            "legitimitetsgap mot fiskere, mens innbyggerne i de samme kommunene er mer "
            "positive. Rosendal med flere (2025) viser at kommuner veier miljøbelastning "
            "mot næringsklynge når de peker ut sjø i arealdelen. Sørdahl og Kvalvik "
            "(2024) og Sørdahl (2026) argumenterer for at mer helhet i plandokumentet "
            "ikke i seg selv gjør utfallet mer avgjort. Mikkelsen, Sørdahl og Solås "
            "(2022) knytter legitimitet til om konsekvensvurderingene er gjennomsiktige "
            "og like fra sak til sak. Schütz og Slater (2019) beskriver spenningen "
            "mellom forutsigbarhet for tillatelsen og muligheten til å endre vilkår når "
            "miljøvirkningene endrer seg.",
            "Hvilke konflikter oppstår i plan- og lokaliseringsprosesser mellom havbruk og andre interesser, og hva bidrar til legitime, effektive og forutsigbare beslutningsprosesser?",
        ),
        (
            "8. Hvilke muligheter har næringen selv for å gjøre sin arealbruk mest mulig effektiv og bærekraftig?",
            "Tekstene som svarer her, handler om det oppdretterne kan gjøre sammen. "
            "Karlsen med flere (2019) finner at samarbeid om brakklegging, utsett og "
            "beredskap i stor grad er frivillig, eller frivillig under trussel om "
            "pålegg, og anbefaler at det forblir frivillig fordi pålagt samarbeid "
            "sjelden er nok. Osmundsen med flere (2021) studerer den samme "
            "selvreguleringen i felles farvann. Bjørnå med flere (2026) beskriver "
            "uformelle nettverk der selskapene tar biologisk risiko og regulatorisk "
            "press i fellesskap. Rapporten om bærekraftig arealbruk (2023) sier at "
            "produksjon i en åpen allmenning krever forretningsmodeller med koordinering "
            "av lokalitetsbruk, fordi ett selskaps drift treffer naboens resultat. "
            "Gullestad-utvalget (2011) la et sterkere ansvar på næringen i hvert "
            "produksjonsområde for de felles utfordringene. Om frivillig sonesamarbeid "
            "faktisk gir mer effektiv arealbruk, er omstridt: Karlsen gjengir at felles "
            "brakklegging har usikker effekt på lus.",
            "Hvilke muligheter har næringen selv for å gjøre sin arealbruk mest mulig effektiv og bærekraftig?",
        ),
        (
            "9. På hvilken måte er biosikkerhet, smittehensyn og vannkontakt mellom anlegg viktig for produksjon og drift?",
            "Åpne merder deler vann, og avstanden mellom anlegg er en driftsgrense like "
            "mye som en plangrense. Aldrin med flere (2011) modellerer spredning av "
            "ILA langs sjøvei mellom anlegg. Aldrin med flere (2015) finner at en stor "
            "del av PD-smitten kommer fra naboanlegg. Aldrin med flere (2017) modellerer "
            "lusepopulasjonen på det enkelte anlegget, inkludert rekruttering utenfra. "
            "Qviller med flere (2024) simulerer at færre og større anlegg, lenger fra "
            "hverandre, kan senke lusenivå og behandlingsbehov. Kulmambetova og Tveterås "
            "(2025) finner at tettere naboer henger sammen med høyere produksjonskostnad, "
            "via sykdom og lus som spres med strøm. Pettersen med flere (2015) beskriver "
            "brakklegging, flytterestriksjoner og forvaltningssoner som smitteverktøy i "
            "åpne merder. Moldal med flere (2026) knytter deler av ILA-utbruddene i 2025 "
            "til horisontal smitte mellom sjølokaliteter og til flytting av fisk. Det "
            "som gjenstår, er hvor stor avstand som faktisk bryter smittekontakten, og "
            "om felles brakklegging virker.",
            "På hvilken måte er biosikkerhet, smittehensyn og vannkontakt mellom anlegg viktig for produksjon og drift av akvakulturanlegg?",
        ),
    ],
    "en": [
        (
            "1. What determines where and to what extent aquaculture can be established, and how are environment, industry development and other uses weighed?",
            "If the pen takes so little room, what sets the limit? Hersoug, Mikkelsen "
            "and Osmundsen (2020) answer that the national limit at the time sat with "
            "production licences and the traffic-light rule, even though spacing "
            "requirements and other uses shrink what can be used, and some regions are "
            "full. Sandersen and Kvalvik (2015) and the Gullestad committee (2011) "
            "place the scarcity in good sites and in the municipality's willingness to "
            "designate sea. The 2023 report on sustainable area use asks whether a "
            "large production increase is possible when environment, fish welfare and "
            "economy are weighed together, and answers that it is not, with today's "
            "technology and operation. The 2015 Nofima report on the legal framework "
            "finds that an isolated environmental refusal can stop a site even when a "
            "joint weighing of industry, jobs and disease transmission would point "
            "another way. The diagnoses are written past one another. No text tests "
            "them on the same coast and the same years.",
            "What determines where and to what extent aquaculture can be established and developed, and how are environmental considerations, industry development and competing uses balanced in current spatial planning and area management?",
        ),
        (
            "2. Which factors affect the development of coastal aquaculture, and how do site access, licensing, planning, environment and fish health interact?",
            "Development along the coast depends on several regimes hitting the same site. "
            "Hersoug (2022) separates the production licence, which the traffic-light "
            "steers, from the locality licence, which must sit inside the municipal "
            "area plan. The Gullestad committee (2011) and Hersoug, Mikkelsen and "
            "Osmundsen (2020) tie the area structure to lice, escapes, losses and "
            "distance between farms. Sand and Misund (2025) show that cleared locality "
            "capacity in Trøndelag is far larger than company capacity, because "
            "fallowing and limits on moving fish require more localities than the "
            "licences cover. Kvalvik and Robertsen (2017) and Mikkelsen, Karlsen and "
            "Osmundsen (2019) show that the municipal plan is the gate, while larger "
            "planning areas and shared maps still yield few certain new areas for "
            "aquaculture. Myklebust (2018, 2021) shows how far the municipality can go "
            "with environmental conditions in the plan before the locality case under "
            "the Aquaculture Act takes over. The open question is which factor binds "
            "first, and where they pull in different directions.",
            "Which factors influence opportunities for development in coastal aquaculture, and how do factors related to site availability, licensing systems, spatial planning, environmental considerations and fish health interact?",
        ),
        (
            "3. How is the site application process practised, and where do stops, delays or conflicts most often occur?",
            "The question is the locality application. It goes to the county, which "
            "cannot grant a permit if the Food Safety Authority, the County Governor "
            "or the Coastal Administration refuses, or if the location conflicts with "
            "the plan. Osmundsen and Olsen (2025) find that deadlines are missed more "
            "often at the Food Safety Authority and the County Governor than at the "
            "county, and that incomplete and strategic applications stop the queue. "
            "SALT 1110 reviews 251 refusals from 2020 to 2025. Infection risk dominates "
            "the Food Safety Authority's refusals. Evenset and colleagues (2023) "
            "describe the same veto and the judgement of whether the site is "
            "environmentally sound. Sand and Misund (2025) report that applications in "
            "Osen are often refused because the municipality sits at the top of a "
            "disease-protection zone. The 2015 Nofima report shows that even small "
            "adjustments can require a full locality application. What remains open is "
            "how much of the delay comes from missing knowledge, and how much from each "
            "agency protecting its own concern.",
            "How does the site application process unfold, and at which stages of the process do delays, rejections or conflicts most commonly occur?",
        ),
        (
            "4. How are cumulative effects of aquaculture assessed in planning and siting, and what knowledge problems are described?",
            "Cumulative load is a different question from the conflict with one other "
            "user. Mikkelsen and colleagues (2025) show that the impact-assessment "
            "regulations require an assessment of combined pressures, without saying "
            "how, and that the Aquaculture Act speaks of holistic judgements without an "
            "explicit duty to assess cumulative pressure. Evenset and colleagues (2023) "
            "review cumulative environmental effects and find gaps in method and data. "
            "Case officers struggle in particular with weighing growth against "
            "environmental risk, and with combined effects. SALT 1065 finds that "
            "assessments of combined effects over larger areas could have been better, "
            "and that disease and lice largely belong with authorities other than the "
            "municipal impact assessment. Sandersen (2021) shows that reversed planning "
            "on Helgeland moved the conflict clarification out of the plan and made "
            "cumulative load hard to assess. The Gullestad committee (2011) proposed "
            "production areas because farms affect one another across municipal "
            "borders. The gap is the method: the statutes require a combined "
            "assessment, while the texts disagree on who should do it, and on what "
            "basis.",
            "How are cumulative-effect assessments of aquaculture production incorporated into spatial planning and site-selection decisions for aquaculture, and what knowledge-related and methodological challenges are identified?",
        ),
        (
            "5. How do economic instruments and regulation affect incentives for area use and siting, and how are benefits and costs shared?",
            "The municipality designates the sea, and several texts ask whether money "
            "changes that willingness. Sandersen and Kvalvik (2015) treat the area rent "
            "as a stuck problem: the state wants to avoid a new tax instrument, the "
            "industry wants to pay for growth rather than for existing sites, and the "
            "municipalities want a stable share. They describe a worst case in which "
            "the municipality receives the money and still declines to designate more "
            "sea. Hersoug, Mikkelsen and Osmundsen (2020) follow what came next: the "
            "Aquaculture Fund and a production fee, and the claim that legitimacy for "
            "more area rests on a distribution the municipalities experience as fair. "
            "Aanesen and Mikkelsen (2020) find that transfers from the fund often do not "
            "outweigh households' valuation of avoiding more aquaculture, unless some "
            "of the producer surplus stays in the region. Iversen and colleagues (2025) "
            "describe the resource rent tax and the split of auction income between "
            "host municipalities and counties. Misund and colleagues (2023) find that "
            "people in aquaculture municipalities are more positive toward the industry, "
            "and still no more satisfied with the distribution. Whether the money "
            "actually opens more sea is not tested in this set.",
            "How do economic instruments and regulatory arrangements influence incentives for area use and site selection, and how are benefits and costs distributed among stakeholders?",
        ),
        (
            "6. What knowledge base is used for area decisions, and how may new technology change area use and siting?",
            "The knowledge base for area decisions is uneven, and new technology can "
            "move where farms can sit. Robertsen and colleagues (2014) and SALT 1065 "
            "ask what basis the municipalities use in coastal zone plans, and find that "
            "thematic data are poorly prepared and that the assessments vary. Mikkelsen, "
            "Sørdahl and Solås (2022) compare impact assessments of 143 proposed "
            "aquaculture areas and find weak consistency in what is weighted. Metier "
            "(2023) estimates that marine base maps can reduce the risk of new "
            "locality decisions, including through currents and lice. SALT 1110 points "
            "to knowledge needs in refusal practice. Hersoug, Mikkelsen and Osmundsen "
            "(2020) and the 2023 report on sustainable area use review land-based "
            "production, offshore production, large post-smolt and closed pens, and say "
            "that the need for sheltered coastal area depends on whether these concepts "
            "become profitable. Sand and Misund (2025) report the proposal for a "
            "research centre on area use and for national planning guidelines. How far "
            "the new technology actually moves localities is still qualitative.",
            "What knowledge base underpins spatial decisions in aquaculture, and how may emerging technologies alter the conditions for area use, environmental impacts and siting opportunities?",
        ),
        (
            "7. What conflicts arise between aquaculture and other interests in planning and siting, and what makes the process legitimate and predictable?",
            "The conflict is between aquaculture and other uses of the same sea, and "
            "between local designation and national sector interests. Jentoft and Buanes "
            "(2005) call the picture of almost unlimited coastal space a myth: from the "
            "air the pens are dots, on the ground security zones make the industry "
            "space-consuming, and user conflicts cannot be set aside. Kvalvik and "
            "Robertsen (2017) and Sandersen (2021) show that inter-municipal planning "
            "coordinates the process, while designation of sea for aquaculture often "
            "falls back to each municipality when interests diverge. Bjørkan and "
            "Eilertsen (2020) find a legitimacy gap toward fishers, while residents in "
            "the same municipalities are more positive. Rosendal and colleagues (2025) "
            "show that municipalities weigh environmental load against the industry "
            "cluster when they designate sea in the area plan. Sørdahl and Kvalvik "
            "(2024) and Sørdahl (2026) argue that more holism in the plan document does "
            "not by itself make the outcome more settled. Mikkelsen, Sørdahl and Solås "
            "(2022) tie legitimacy to whether the impact assessments are transparent "
            "and consistent from case to case. Schütz and Slater (2019) describe the "
            "tension between predictability for the permit and the possibility of "
            "changing conditions when environmental effects change.",
            "What conflicts arise in planning and siting processes between aquaculture and other interests, and what contributes to legitimate, effective and predictable decision-making processes?",
        ),
        (
            "8. What can the industry itself do to make its area use more efficient and sustainable?",
            "The texts that answer here are about what the farmers can do together. "
            "Karlsen and colleagues (2019) find that cooperation on fallowing, stocking "
            "and preparedness is largely voluntary, or voluntary under the threat of an "
            "order, and recommend that it stay voluntary because ordered cooperation is "
            "rarely enough. Osmundsen and colleagues (2021) study the same "
            "self-regulation in shared waters. Bjørnå and colleagues (2026) describe "
            "informal networks in which companies take on biological risk and regulatory "
            "pressure together. The 2023 report on sustainable area use says that "
            "production in an open commons requires business models that coordinate "
            "locality use, because one company's operation hits the neighbour's result. "
            "The Gullestad committee (2011) placed a stronger responsibility on the "
            "industry in each production area for the shared problems. Whether voluntary "
            "zone cooperation actually makes area use more efficient is disputed: "
            "Karlsen reports that joint fallowing has an uncertain effect on lice.",
            "What measures may the industry itself apply to ensure that its spatial use is most efficient and sustainable?",
        ),
        (
            "9. How do biosecurity, disease and water contact between farms matter for production and operation?",
            "Open pens share water, and the distance between farms is an operational "
            "limit as much as a planning limit. Aldrin and colleagues (2011) model the "
            "spread of ISA along the seaway between farms. Aldrin and colleagues (2015) "
            "find that a large share of PD infection comes from neighbouring farms. "
            "Aldrin and colleagues (2017) model the lice population on the individual "
            "farm, including recruitment from outside. Qviller and colleagues (2024) "
            "simulate that fewer and larger farms, farther apart, can lower lice levels "
            "and treatment need. Kulmambetova and Tveterås (2025) find that closer "
            "neighbours are associated with higher production cost, through disease and "
            "lice carried by currents. Pettersen and colleagues (2015) describe "
            "fallowing, movement restrictions and management areas as disease-control "
            "tools in open pens. Moldal and colleagues (2026) tie part of the 2025 ISA "
            "outbreaks to horizontal infection between sea sites and to movement of "
            "fish. What remains is how large a distance actually breaks infection "
            "contact, and whether joint fallowing works.",
            "How are biosecurity, disease transmission and water connectivity between farms important for production and operation of aquaculture facilities?",
        ),
    ],
}

# ── Language (main area, so phone users see it) ───────────────────────────────

header_slot = st.container()  # brand header, filled below once `lang` is known
col_home, col_lang = st.columns([1, 1], vertical_alignment="center")
with col_home:
    st.page_link("app.py", label="← Alle evidensrom", icon="🏠")
with col_lang:
    lang = st.radio(
        "Språk / Language",
        options=LANG_OPTIONS,
        format_func=lambda x: "English" if x == "en" else "Norsk",
        horizontal=True,
        label_visibility="collapsed",
    )
answer_format = "freeform"
output_language = "Norwegian Bokmål" if lang == "no" else "English"

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("Havbruksløftets Evidensrom")
    st.page_link("app.py", label="← Alle evidensrom", icon="🏠")
    st.caption(tr(lang, "Area and aquaculture", "Areal og havbruk"))

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

    st.caption(
        tr(
            lang,
            f"Corpus: area and aquaculture ({n_total or 50} documents, prototype room)  \n"
            "Method: Honest Broker (Pielke 2007)  \n"
            "Funded by FHF / Havbruksløftet AP1",
            f"Korpus: areal og havbruk ({n_total or 50} dokumenter, prototype-rom)  \n"
            "Metode: Honest Broker (Pielke 2007)  \n"
            "Finansiert av FHF / Havbruksløftet AP1",
        )
    )

# ── Brand + hero ──────────────────────────────────────────────────────────────

with header_slot:
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
            '<p class="hl-lede">The pens occupy a vanishingly small share of the coastal zone, and yet area scarcity remains a persistent dispute. A distinguishes pen area, locality area and plan area. B shows the split governing system. C shows the open questions.</p>',
            '<h1 class="hl-h1">Areal og havbruk</h1>'
            '<p class="hl-lede">Merdene tar en forsvinnende liten del av kystsonen, og likevel er knapphet på areal et vedvarende stridsspørsmål. A skiller merdareal, lokalitetsareal og planareal. B viser det delte styringssystemet. C viser de åpne spørsmålene.</p>',
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
  <div class="hl-stat"><strong>19.10.2026</strong><span>last reviewed</span></div>
</div>
""",
                f"""
<div class="hl-stats">
  <div class="hl-stat"><strong>{n_total or 39}</strong><span>dokumenter i korpuset</span></div>
  <div class="hl-stat"><strong>{span}</strong><span>tidsrom</span></div>
  <div class="hl-stat"><strong>{len(FAULTS['no'])}</strong><span>åpne spørsmål</span></div>
  <div class="hl-stat"><strong>19.10.2026</strong><span>sist gjennomgått</span></div>
</div>
""",
            ),
            unsafe_allow_html=True,
        )

st.write("")

# ── A and B: two collapsed background boxes, so C is reached sooner ───────────
# ── A: Introduksjon ───────────────────────────────────────────────────────────

with st.expander(tr(lang, "A · Introduction", "A · Introduksjon"), key="areal_section_a"):
    st.caption(tr(lang, "Editorial overview", "Redaksjonell oversikt"))
    with st.container(border=True):
        col_a, col_fig = st.columns([1.0, 1.0])
        with col_a:
            st.markdown(
                tr(
                    lang,
                    """
Norwegian aquaculture runs along a coastline that is, internationally, almost unreal in length and fragmentation, and yet scarcity of area has become one of the most persistent disputes in the industry's governance. The paradox is clear when the figures are set side by side. The Gullestad committee put the total sea area from Vest-Agder to Finnmark at about 76 000 square kilometres (Gullestad et al. 2011), while the farms, moorings included, occupy just over half a percent of the inshore coastal area (Hersoug et al. 2020). At the same time, farmers report that they cannot get the localities they need (Robertsen et al. 2014; Sandersen and Kvalvik 2015). Already in 2005, Jentoft and Buanes called the idea of almost unlimited coastal space a myth: from the air the zone looks empty and the pens are hard to see, but on the ground safety zones and the need for alternative localities make the industry far more space-consuming than the footprint suggests (Jentoft and Buanes 2005).

Much of the disagreement comes from the fact that "the area aquaculture uses" can mean very different things. Count only the pens, and the footprint is small. Count moorings, safety zones and planned areas as well, and it becomes far larger, and largest of all when the infection distance between farms is included.

**Pen area.** The farm's physical surface in the sea.

**Locality area.** Also includes the mooring system and the safety zone.

**Plan area.** The sea the municipality has designated for the purpose, often as a combined purpose where aquaculture is only one of several permitted uses.

When infection distances between farms are counted in, the occupation grows sharply: Hersoug et al. (2020) illustrate that a five-kilometre zone around farms can cover about a fifth of the coastal zone. Debates about whether the coast is full or empty therefore easily talk past one another if the parties are each talking about a different one of these quantities.
""",
                    """
Norsk havbruk drives langs en kystlinje som i internasjonal sammenheng er nesten uvirkelig lang og oppstykket, og likevel er knapphet på areal blitt et av de mest vedvarende stridsspørsmålene i næringens forvaltning. Paradokset trer tydelig frem når tallene settes ved siden av hverandre. Gullestad-utvalget anslo det samlede sjøarealet fra Vest-Agder til Finnmark til om lag 76 000 kvadratkilometer (Gullestad mfl. 2011), mens anleggene, medregnet fortøyninger, legger beslag på drøyt en halv prosent av det kystnære sjøarealet (Hersoug mfl. 2020). Samtidig melder oppdrettere at de ikke får tilgang til de lokalitetene de trenger (Robertsen mfl. 2014; Sandersen og Kvalvik 2015). Allerede i 2005 kalte Jentoft og Buanes forestillingen om nærmest ubegrenset kystplass for en myte: fra luften ser sonen tom ut og merdene er vanskelige å se, men på bakken gjør sikkerhetssoner og behovet for alternative lokaliteter næringen langt mer plasskrevende enn fotavtrykket tilsier (Jentoft og Buanes 2005).

Mye av uenigheten skyldes at «arealet havbruket bruker» kan bety svært forskjellige ting. Regnes bare merdene, er beslaget lite. Regnes fortøyninger, sikkerhetssoner og planlagte områder med, blir det langt større, og størst når smitteavstanden mellom anlegg tas med.

**Merdareal.** Anleggets fysiske flate i sjøen.

**Lokalitetsareal.** Omfatter i tillegg fortøyningssystem og sikkerhetssone.

**Planareal.** Den sjøen kommunen har avsatt til formålet, ofte som kombinert formål der havbruk bare er én av flere tillatte bruksmåter.

Når smitteavstander mellom anlegg regnes inn, vokser beslaget kraftig: Hersoug mfl. (2020) illustrerer at en sone på fem kilometer rundt anleggene kan dekke om lag en femdel av kystsonen. Diskusjoner om hvorvidt kysten er full eller tom skriver derfor lett forbi hverandre dersom partene snakker om hver sin av disse størrelsene.
""",
                )
            )
            with st.expander(tr(lang, "Read more", "Les mer")):
                st.markdown(
                    tr(
                        lang,
                        """
**Split governance.** Governance is split between levels that each have their own logic. The municipality designates sea area under the Planning and Building Act, out to one nautical mile beyond the baselines, and thus holds a key role that national growth targets depend on. A farm then needs both a production licence and a locality licence, and after the 2010 administrative reform it is the county that coordinates the locality case. Sector authorities can still refuse under their own statutes, so an application can survive the plan process and stop somewhere else entirely. Above this sits the traffic-light system with its thirteen production areas, which is a lid on capacity and not a map of where farms may stand.

**Three answers on what stops growth.** What actually stops growth is the central disputed question, and there are at least three competing answers. One points to the licence regime: the constraint is not sea surface, but production licences and capacity limits (Hersoug et al. 2020). The second points to the municipality, where good localities are a limited resource and the political will to designate sea decides what is available at all (Sandersen and Kvalvik 2015; Gullestad et al. 2011). The third points to biology, where lice, disease, fish welfare and proximity between farms can set the limit before the sea runs out (Tveterås 2023; Qviller et al. 2024). The explanations do not rule one another out, but they lead to different political conclusions, and no text in the collection tests them against one another on the same coast in the same year.

**Uneven knowledge base.** When sea goes to a farm, something else must yield, and the knowledge base for that trade-off is uneven. Organic load on soft seabed is well studied, while effects on hard seabed are far less understood, and knowledge is lacking on dissolved nutrients and vulnerable species and habitats, among other things (Evenset et al. 2023). The duty to assess cumulative impact follows from the Nature Diversity Act and the impact-assessment rules (Mikkelsen et al. 2025), but reviews of plans and cases find that it is often treated weakly (Eriksen et al. 2023; Mikkelsen et al. 2025).

**Municipal will.** All of this hangs on the municipalities' own interests. Because designation happens locally, national growth ambitions rest on local will, and the question of what municipalities get in return has followed the debate for decades. Property tax on sea installations, Havbruksfondet and the production fee have changed the money flows; an area rent was considered but never introduced (Sandersen and Kvalvik 2015). Surveys of refusals and processing times show where the cases studied stop (Eriksen et al. 2026; Osmundsen and Olsen 2025), but not how often a case dies in the plan, in the sector refusal or in the county's discretion overall. The debate over aquaculture's coastal area is therefore rarely only about how much sea there is, but about who decides, what counts as area, and what municipalities get in return for designating it.
""",
                        """
**Delt forvaltning.** Forvaltningen er delt mellom nivåer som hver har sin logikk. Kommunen peker ut sjøareal etter plan- og bygningsloven, ut til én nautisk mil utenfor grunnlinjene, og har dermed en nøkkelrolle som nasjonale vekstmål er avhengige av. Et anlegg trenger deretter både produksjonstillatelse og lokalitetstillatelse, og etter forvaltningsreformen i 2010 er det fylkeskommunen som samordner lokalitetssaken. Sektormyndighetene kan likevel avslå etter sine egne lover, slik at en søknad kan overleve planprosessen og stoppe et helt annet sted. Over dette ligger trafikklyssystemet med sine tretten produksjonsområder, som er et lokk på kapasitet og ikke et kart over hvor anleggene kan stå.

**Tre svar på hva som stopper veksten.** Hva som egentlig stopper veksten, er det sentrale stridsspørsmålet, og det finnes minst tre konkurrerende svar. Det ene peker på tillatelsesregimet: det står ikke på sjøflaten, men på produksjonstillatelser og kapasitetsgrenser (Hersoug mfl. 2020). Det andre peker på kommunen, der gode lokaliteter er en begrenset ressurs og den politiske viljen til å avsette sjø avgjør hva som overhodet er tilgjengelig (Sandersen og Kvalvik 2015; Gullestad mfl. 2011). Det tredje peker på biologien, der lus, sykdom, fiskevelferd og nærhet mellom anlegg kan sette grensen før sjøen tar slutt (Tveterås 2023; Qviller mfl. 2024). Forklaringene utelukker ikke hverandre, men de leder til ulike politiske konklusjoner, og ingen av tekstene i korpuset prøver dem mot hverandre på samme kyst i samme år.

**Skjevt kunnskapsgrunnlag.** Når sjø går til anlegg, må noe annet vike, og kunnskapsgrunnlaget for den avveiingen er skjevt. Organisk belastning på bløtbunn er godt studert, mens påvirkningen på hardbunn er langt dårligere kjent, og det mangler blant annet kunnskap om løste næringssalter og om sårbare arter og habitater (Evenset mfl. 2023). Kravet om å vurdere samlet påvirkning følger av naturmangfoldloven og reglene om konsekvensutredning (Mikkelsen mfl. 2025), men gjennomganger av planer og saker finner at det ofte behandles svakt (Eriksen mfl. 2023; Mikkelsen mfl. 2025).

**Kommunal vilje.** Alt henger sammen med kommunenes egne interesser. Fordi utpekingen skjer lokalt, hviler nasjonale vekstambisjoner på lokal vilje, og spørsmålet om hva kommunene får igjen har fulgt debatten i flere tiår. Eiendomsskatt på anlegg i sjø, Havbruksfondet og produksjonsavgiften har endret pengestrømmene; en arealavgift ble vurdert, men aldri innført (Sandersen og Kvalvik 2015). Kartlegginger av avslag og saksbehandlingstid viser hvor de undersøkte sakene stopper (Eriksen mfl. 2026; Osmundsen og Olsen 2025), men ikke hvor ofte en sak dør i planen, i sektoravslaget eller i fylkets skjønn sett under ett. Diskusjonen om havbrukets kystareal handler derfor sjelden bare om hvor mye sjø som finnes, men om hvem som bestemmer, hva som regnes som areal, og hva kommunene får igjen for å avsette det.
""",
                    )
                )
        with col_fig:
            fig_areal = REPO / "mockup" / "figur-havbruk-og-areal.jpg"
            if fig_areal.exists():
                # Portrait map with a small-print legend: the column is wide enough to
                # read it, and the image has a fullscreen button for the rest.
                st.image(
                    str(fig_areal),
                    width="stretch",
                    caption=tr(
                        lang,
                        "Aquaculture and other interests along the coast. Sources are listed in the map.",
                        "Havbruk og andre interesser langs kysten. Kilder står i kartet.",
                    ),
                )

# ── B: Norsk rammeverk ────────────────────────────────────────────────────────

with st.expander(tr(lang, "B · The Norwegian framework", "B · Norsk rammeverk"), key="areal_section_b"):
    st.caption(
        tr(
            lang,
            "Current Norwegian framework: a split governing system",
            "Gjeldende norsk rammeverk: et delt styringssystem",
        )
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
                "The locality application goes to the **county**, which handles it under the "
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
                "Lokalitetssøknaden sendes til **fylkeskommunen**, som behandler den etter "
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
                "**how much**. Myklebust (2021) starts from municipal conditions on how farming "
                "is carried out, including a closed pen and limits on organic discharge, and "
                "asks where the legal limit of that power lies. Myklebust (2014, 2018) finds "
                "that the municipality cannot freely add its own conditions, and that the "
                "boundary with the sector authorities is unclear. Capacity in the production "
                "area is a separate lid. The arrangement lets several expert authorities review "
                "each case, but it is also described as fragmented (Sandersen and Kvalvik 2014; "
                "Solås et al. 2015) and slow (Osmundsen and Olsen 2025). Because fjords, "
                "currents and infection do not follow municipal borders, municipalities have "
                "made intermunicipal coastal plans, including in Trøndelag and on Helgeland. "
                "Robertsen et al. (2014) could not show that these plans improve access "
                "to sites. The municipal council still adopts the plan for its own sea, and "
                "firms report refusals even inside areas already zoned for aquaculture. In a "
                "survey with 54 replies from 111 firms, the conflicts named most often by firms "
                "that had joined a plan were conservation (57 percent), fisheries (54 percent) "
                "and wild salmon (36 percent) (Robertsen et al. 2014).",
                "Todelingen gjør at kommunen i stor grad styrer **hvor** havbruk kan "
                "ligge, mens fylket og staten styrer **hvem** som får produsere, og **hvor mye**. "
                "Myklebust (2021) tar utgangspunkt i kommunale vilkår om hvordan oppdrett skal "
                "drives, blant annet lukket merd og grenser for organisk utslipp, og spør hvor "
                "den rettslige grensen for den myndigheten går. Myklebust (2014, 2018) finner "
                "at kommunen ikke fritt kan legge på egne vilkår, og at grensen mot "
                "sektormyndighetene er uklar. Kapasitet i produksjonsområdet er et eget lokk. "
                "Ordningen gjør at flere fagmyndigheter vurderer hver sak, men den beskrives også "
                "som fragmentert (Sandersen og Kvalvik 2014; Solås mfl. 2015) og tidkrevende "
                "(Osmundsen og Olsen 2025). Fordi fjorder, strøm og smitte ikke "
                "følger kommunegrenser, har kommuner laget interkommunale kystsoneplaner, "
                "blant annet i Trøndelag og på Helgeland. Robertsen mfl. (2014) kunne "
                "ikke vise at slike planer gir bedre lokalitetstilgang. Kommunestyret vedtar "
                "fortsatt planen for egen sjø, og firmaer melder avslag også inne i områder som "
                "allerede er avsatt til havbruk. I en undersøkelse med 54 svar fra 111 firmaer "
                "var konfliktene som oftest ble oppgitt av firmaer som hadde deltatt i en plan, "
                "vern (57 prosent), fiskeri (54 prosent) og villaks (36 prosent) (Robertsen mfl. 2014).",
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
  <li><strong>Sector permits</strong>. Food Safety Authority, County Governor (pollution) and Coastal Administration can refuse under their own statutes, so no Aquaculture Act permit can be issued. NVE enters for freshwater intake. A permit cannot be granted in breach of adopted protection measures under the Nature Diversity Act (<a href="https://lovdata.no/dokument/NL/lov/2005-06-17-79">Aquaculture Act § 15</a>).</li>
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
  <li><strong>Sektortillatelser</strong>. Mattilsynet, Statsforvalteren (forurensning) og Kystverket kan avslå etter egne lover, slik at tillatelse etter akvakulturloven ikke kan gis. NVE kommer inn ved ferskvannsinntak. Tillatelse kan ikke gis i strid med vedtatte vernetiltak etter naturmangfoldloven (<a href="https://lovdata.no/dokument/NL/lov/2005-06-17-79">akvakulturloven § 15</a>).</li>
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
                "scarce input: depth, exchange, shelter and distance to other biomass "
                "(Sandersen and Kvalvik 2015). That is one diagnosis in the corpus. Others put "
                "production licences and the traffic-light first nationally (Hersoug et al. "
                "2020), or lice, disease, welfare and proximity between farms (Tveterås 2023). "
                "Climate change may also shift where conditions are favourable (Skrove et al. "
                "2023). Area alone does not give growth. The traffic-light "
                "can freeze or cut capacity even where the plan has opened the sea. Green can "
                "offer up to 6 percent growth, yellow holds capacity, red can require a 6 "
                "percent cut, with an exception for farms that document low lice counts "
                "([HI](https://www.hi.no/hi/temasider/akvakultur/trafikklyssystemet-hi-sin-kunnskap)).",
                "Sett fra næringen behandles **gode lokaliteter** ofte som den knappeste "
                "innsatsfaktoren: dybde, vannutskifting, skjerming og avstand til annen "
                "biomasse (Sandersen og Kvalvik 2015). Det er én diagnose i korpuset. Andre setter "
                "produksjonstillatelser og trafikklys først nasjonalt (Hersoug mfl. 2020), eller "
                "lus, sykdom, velferd og nærhet mellom anlegg (Tveterås 2023). Klimaendringer kan "
                "også forskyve hvor forholdene er gunstige (Skrove mfl. 2023). Areal alene gir "
                "ikke vekst. Trafikklyset kan fryse eller kutte "
                "kapasitet selv der planen har åpnet sjøen. Grønt kan gi inntil 6 prosent "
                "vekst, gult holder kapasiteten, rødt kan kreve 6 prosent kutt, med unntak for anlegg som dokumenterer lave lusetall "
                "([HI](https://www.hi.no/hi/temasider/akvakultur/trafikklyssystemet-hi-sin-kunnskap)).",
            )
        )
        st.markdown(
            tr(
                lang,
                "**Sharing the value.** [Havbruksfondet](https://www.fiskeridir.no/akvakultur/havbruksfondet) "
                "was decided by the Storting in 2015. It distributes the municipal sector's share "
                "of income from growth in the industry and from the production fee, mainly by cleared "
                "locality MTB; part goes to municipalities that have cleared new locality MTB. A "
                "[production fee](https://www.skatteetaten.no/rettskilder/type/handboker/skatte-abc/gjeldende/a-11-akvakultur-havbruk/A-11.071/A-11.090/) "
                "has applied from 1 January 2021. The rate has been raised several times and is "
                "98.5 øre per kilo of finished salmon, trout and rainbow trout in 2026 (96.5 øre in 2025). "
                "[Resource-rent tax](https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p=93582) "
                "on salmon, trout and rainbow trout was adopted in 2023. The rate is 32.1 percent of the "
                "resource-rent income after deducting the calculated corporate tax, about 25 percent "
                "effectively. The bottom deduction is set yearly by the Storting; for 2025 it is "
                "70 million kroner ([Skatteetaten](https://www.skatteetaten.no/rettskilder/type/handboker/skatte-abc/gjeldende/a-11-akvakultur-havbruk/A-11.019/A-11.020/)). An area rent "
                "was considered and rejected (Sandersen and Kvalvik 2015). Whether Havbruksfondet and the production "
                "fee actually get the municipality to designate more sea is untested in the "
                "research here. Aanesen and Mikkelsen (2020) find, in five Arctic municipalities, "
                "that transfers from the fund often do not outweigh the welfare loss households "
                "state for more aquaculture, and that a positive regional result needs some "
                "producer surplus to remain in the region. Their willingness-to-pay estimates "
                "were not statistically significant at 5 percent.",
                "**Fordeling av verdiene.** [Havbruksfondet](https://www.fiskeridir.no/akvakultur/havbruksfondet) "
                "ble besluttet av Stortinget i 2015. Det fordeler kommunal sektors andel "
                "av inntektene fra vekst i oppdrettsnæringen og fra produksjonsavgiften, i hovedsak "
                "etter klarert lokalitets-MTB; en del går til kommuner som har klarert ny "
                "lokalitets-MTB. En "
                "[produksjonsavgift](https://www.skatteetaten.no/rettskilder/type/handboker/skatte-abc/gjeldende/a-11-akvakultur-havbruk/A-11.071/A-11.090/) "
                "har gjeldt fra 1. januar 2021. Satsen er hevet flere ganger og er 98,5 øre "
                "per kilo ferdig produsert laks, ørret og regnbueørret i 2026 (96,5 øre i 2025). "
                "[Grunnrenteskatt](https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p=93582) "
                "på laks, ørret og regnbueørret ble vedtatt i 2023. Satsen er 32,1 prosent av "
                "grunnrenteinntekten etter fradrag for beregnet selskapsskatt, om lag 25 prosent "
                "effektivt. Bunnfradraget fastsettes årlig av Stortinget og er 70 millioner kroner "
                "for 2025 ([Skatteetaten](https://www.skatteetaten.no/rettskilder/type/handboker/skatte-abc/gjeldende/a-11-akvakultur-havbruk/A-11.019/A-11.020/)). Forslag om en "
                "arealavgift ble vurdert og forkastet (Sandersen og Kvalvik 2015). Om Havbruksfondet og produksjonsavgiften "
                "faktisk får kommunen til å peke ut mer sjøareal, er uavklart i forskningen "
                "her. Aanesen og Mikkelsen (2020) finner, i fem arktiske kommuner, at "
                "overføringer fra fondet ofte ikke veier opp for velferdstapet husholdningene "
                "oppgir ved mer havbruk, og at et positivt regionalt resultat krever at noe "
                "av produsentoverskuddet blir igjen i regionen. Anslagene for betalingsvilje "
                "var ikke statistisk signifikante på 5 prosent.",
            )
        )
        with st.expander(
            tr(
                lang,
                "Read more: Havbruksutvalget, offshore, closed and land-based",
                "Les mer: Havbruksutvalget, havbruk til havs, lukket og landbasert",
            )
        ):
            st.markdown(
                tr(
                    lang,
                    """
[NOU 2023: 23](https://www.regjeringen.no/no/dokumenter/nou-2023-23/id2995224/) (Havbruksutvalget, 2023) reviewed the permit and management system. It proposed, among other things, that every aquaculture permit consist of a company licence and a locality licence, **auction of company licences as the main rule**, locality licences on application without payment, a larger state role in sea-area planning, and a study of the Directorate of Fisheries as the body that grants locality licences.

Three developments change the area picture, without solving it alone. They mainly change who must say yes, which interests collide, and where in the system the conflict sits.

**Aquaculture at sea.** Production moves out of the municipal plan area and into areas opened by the state. [Fiskeridirektoratet on allocation](https://www.fiskeridir.no/akvakultur/tildeling). On 27 February 2026 the King in Council decided that [Norskerenna sør, Frøyabanken nord and Trænabanken](https://www.regjeringen.no/no/aktuelt/kongelig-resolusjon-om-havbruk-til-havs-fastsatt/id3150415/) can be put out to tender, with parts of Norskerenna sør and Trænabanken excluded where they overlap defence and particularly valuable areas. That can reduce local coastal conflict. It raises new questions about preparedness, welfare, cost, fisheries, and who receives the income when there is no host municipality.

**Closed and semi-closed farms at sea.** They can collect discharges and reduce lice pressure, and may give more production per unit of area. They need more energy, more infrastructure and larger investment. They are not yet at large scale.

**Land-based aquaculture.** It removes the sea-area conflict and moves it to the shoreline, the power grid, water intake and land discharge permits.
""",
                    """
[NOU 2023: 23](https://www.regjeringen.no/no/dokumenter/nou-2023-23/id2995224/) (Havbruksutvalget, 2023) gjennomgikk tillatelses- og forvaltningssystemet. Utvalget foreslo blant annet at alle akvakulturtillatelser skal bestå av en selskapstillatelse og en lokalitetstillatelse, **auksjon av selskapstillatelser som hovedregel**, lokalitetstillatelser etter søknad uten vederlag, en større statlig rolle i sjøarealplanlegging, og at Fiskeridirektoratet utredes som tildelingsmyndighet for lokalitetstillatelser.

Tre utviklingstrekk endrer arealbildet, uten å løse det alene. De endrer først og fremst hvem som må si ja, hvilke interesser som settes opp mot hverandre, og hvor i systemet konflikten havner.

**Havbruk til havs.** Produksjon flyttes ut av kommunenes planområde og inn i områder staten åpner. [Fiskeridirektoratet om tildeling](https://www.fiskeridir.no/akvakultur/tildeling). 27. februar 2026 fastsatte Kongen i statsråd at [Norskerenna sør, Frøyabanken nord og Trænabanken](https://www.regjeringen.no/no/aktuelt/kongelig-resolusjon-om-havbruk-til-havs-fastsatt/id3150415/) kan lyses ut, med unntak av deler av Norskerenna sør og Trænabanken som overlapper Forsvarets fareområde og særlig verdifulle områder. Det kan redusere lokal kystkonflikt. Det reiser nye spørsmål om beredskap, velferd, kostnader, fiskeriene, og hvem som skal få inntektene når det ikke finnes vertskommune.

**Lukkede og semilukkede anlegg i sjø.** De kan samle utslipp og redusere lusepress, og kan gi mer produksjon per arealenhet. De krever mer energi, mer infrastruktur og større investeringer. De er foreløpig ikke i stor skala.

**Landbasert oppdrett.** Det fjerner sjøarealkonflikten og flytter den til strandsonen, kraftnettet, vannuttak og utslippstillatelser på land.
""",
                )
            )
        with st.expander(
            tr(
                lang,
                f"Laws and regulations ({len(REGELVERK)})",
                f"Lover og forskrifter ({len(REGELVERK)})",
            )
        ):
            render_regelverk(lang)

# ── C: Spør kildene ───────────────────────────────────────────────────────────
# Rekkefølge: bakgrunn, dokumenter (lukket), eget spørsmål, åpent spørsmål som
# nedtrekksliste (fyller bare tekstfeltet), knappen, så svaret rett under.

section_header(
    tr(lang, "C · Ask the sources", "C · Spør kildene"),
    tr(lang, "Your own question, or an open one", "Ditt eget spørsmål, eller et åpent"),
)

# The audience comes first, so the button uses the chosen mode.
with st.container(border=True):
    mode = st.radio(
        tr(lang, "Choose your background", "Velg bakgrunn"),
        options=["researcher", "non_researcher"],
        format_func=lambda x: (
            tr(lang, "Researcher / expert", "Forsker / fagperson")
            if x == "researcher"
            else tr(lang, "Interested non-specialist", "Interessert ikke-spesialist")
        ),
        horizontal=True,
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

# ── Documents in the corpus (collapsed). Defaults: all documents, k = 10. ─────
# `selected_doc_ids` and `top_k` are defined here, before anything reads them.

if corpus_ready:
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
    # `areal_selected` is the multiselect's own state, so the expander label below
    # always shows the live count. Drop IDs that no longer exist (a pre-fix session
    # stored display labels); if none survive, restore the all-documents default.
    if "areal_selected" not in st.session_state:
        st.session_state["areal_selected"] = all_doc_ids
    else:
        stored_ids = st.session_state.get("areal_selected") or []
        valid_ids = [doc_id for doc_id in stored_ids if doc_id in doc_options]
        if stored_ids and not valid_ids:
            valid_ids = all_doc_ids
        st.session_state["areal_selected"] = valid_ids
    n_selected = len(st.session_state["areal_selected"])
else:
    all_doc_ids = []
    doc_options = {}
    n_selected = 0


def _select_docs(doc_ids: list[str]) -> None:
    """Button callback: runs before the rerun, so the widget and the label follow."""
    st.session_state["areal_selected"] = list(doc_ids)


with st.expander(
    tr(
        lang,
        f"Documents in the corpus ({n_selected} of {n_total} selected)",
        f"Dokumenter i korpuset ({n_selected} av {n_total} valgt)",
    ),
    key="areal_docs_expander",
):
    if corpus_ready:
        col_sel, col_clr = st.columns(2)
        col_sel.button(
            tr(lang, "Select all", "Velg alle"),
            on_click=_select_docs,
            args=(all_doc_ids,),
            width="stretch",
        )
        col_clr.button(
            tr(lang, "Clear all", "Tøm"),
            on_click=_select_docs,
            args=([],),
            width="stretch",
        )
        selected_doc_ids = st.multiselect(
            tr(lang, "Include these documents", "Inkluder disse dokumentene"),
            options=all_doc_ids,
            key="areal_selected",
            format_func=lambda doc_id: doc_options[doc_id],
            label_visibility="collapsed",
        )
        if not selected_doc_ids:
            st.warning(tr(lang, "Select at least one document.", "Velg minst ett dokument."))
    else:
        selected_doc_ids = None
    top_k = st.slider(
        tr(lang, "Documents to retrieve", "Antall dokumenter å hente"),
        3,
        15,
        12,
        help=tr(
            lang,
            "How many of the most relevant documents the answer is based on. "
            "Documents tagged with the linked open question come first. The search ranks documents by how similar their content is to your "
            "question. More documents give a broader answer, but it can take a "
            "little longer.",
            "Hvor mange av de mest relevante dokumentene svaret bygger på. "
            "Dokumenter merket med det koblede åpne spørsmålet kommer først. Søket rangerer dokumentene etter hvor lik innholdet er spørsmålet "
            "ditt. Flere dokumenter gir et bredere svar, men kan ta litt lengre tid.",
        ),
    )

# ── Open questions: a dropdown that only fills the text area ──────────────────

def _open_q_key(key_lang: str) -> str:
    """One selectbox state per language, so a language switch never mixes them."""
    return f"areal_open_q_{key_lang}"


def _fill_from_open_question(key_lang: str) -> None:
    """Selectbox callback (runs before the rerun): put the full priority question in
    the text area and drop the old answer. Asks nothing. The placeholder does nothing."""
    n = st.session_state.get(_open_q_key(key_lang))
    if not n:
        return
    st.session_state["areal_query"] = FAULTS[key_lang][n - 1][2]
    st.session_state.pop("areal_last", None)  # never leave an old answer under a new question


def _open_q_label(n: int) -> str:
    """The full priority question, verbatim, as the selectors settled it."""
    return FAULTS[lang][n - 1][2]


# ── Your own question ─────────────────────────────────────────────────────────

with st.container(border=True):
    query = st.text_area(
        tr(lang, "Your question", "Spørsmålet ditt"),
        key="areal_query",
        placeholder=tr(
            lang,
            "e.g. What limits aquaculture growth on the Norwegian coast: available sites, licences, municipal planning, or biological and environmental considerations?",
            "f.eks. Hva begrenser vekst i havbruk på norskekysten: tilgjengelige lokaliteter, tillatelser, kommunal planlegging, eller biologiske og miljømessige hensyn?",
        ),
        height="content",
    )
    st.caption(
        tr(
            lang,
            "Questions, answers and ratings are stored anonymously for research on the tool. No names are collected.",
            "Spørsmål, svar og vurderinger lagres anonymt for forskning på verktøyet. Ingen navn samles inn.",
        )
    )
    # A selectbox cuts the long questions off with «…», so the full texts sit in a
    # closed panel as a wrapping radio list instead.
    with st.expander(tr(lang, "Or pick an open question", "Eller velg et åpent spørsmål")):
        st.radio(
            tr(lang, "Open questions", "Åpne spørsmål"),
            options=list(range(1, len(FAULTS[lang]) + 1)),  # A0-A8 in order
            index=None,
            format_func=_open_q_label,
            key=_open_q_key(lang),
            on_change=_fill_from_open_question,
            args=(lang,),
            label_visibility="collapsed",
        )
    col1, col2 = st.columns([1, 4])
    with col1:
        run = st.button(
            tr(lang, "Ask the sources", "Spør kildene"),
            type="primary",
            width="stretch",
        )
    with col2:
        n_active = len(selected_doc_ids) if selected_doc_ids else 0
        st.caption(
            tr(
                lang,
                f"The answer draws on the {min(top_k, n_active)} most relevant of {n_active} documents.",
                f"Svaret bygger på de {min(top_k, n_active)} mest relevante av {n_active} dokumenter.",
            )
        )

AREAL_MODEL = "gpt-6-luna"
ANSWER_TEXT_KEY = "areal_answer_text"  # CSS hook in ui.py; created once per run
MAX_UNCACHED_PER_SESSION = 8

if "areal_session_id" not in st.session_state:
    st.session_state["areal_session_id"] = uuid.uuid4().hex


def _warn_failure(exc: Exception | None) -> None:
    """Plain bilingual warning. Never show a traceback to users."""
    if isinstance(exc, (openai.RateLimitError, openai.APITimeoutError, openai.APIConnectionError)):
        st.warning(
            tr(
                lang,
                "The service is busy right now. Please try again in half a minute.",
                "Tjenesten er travel akkurat nå. Prøv igjen om et halvt minutt.",
            )
        )
    else:
        st.warning(
            tr(
                lang,
                "Something went wrong while answering. Please try again in a moment.",
                "Noe gikk galt under svaret. Prøv igjen om litt.",
            )
        )


def _log_answer(answer_id: str, q: str, results: list[dict], answer: str, started: float, cached: bool, error: str = "", routed_pq: list[str] | None = None) -> None:
    feedback.log_answer(
        session_id=st.session_state["areal_session_id"],
        answer_id=answer_id,
        question=q,
        mode=mode,
        language=lang,
        model=AREAL_MODEL,
        top_k=top_k,
        n_active_docs=len(selected_doc_ids or []),
        retrieved=[r.get("doc_id", "") for r in results],
        answer=answer,
        latency_s=time.perf_counter() - started,
        cached=cached,
        error=error,
        routed_pq=",".join(routed_pq or []),
    )


def _routing_caption(codes: list[str]) -> str:
    if not codes:
        return tr(
            lang,
            "Not linked to an open question; the answer uses plain search.",
            "Ikke koblet til et åpent spørsmål; svaret bygger på vanlig søk.",
        )
    titles = PQ_TITLES_NO if lang == "no" else PQ_TITLES
    linked = tr(lang, " and ", " og ").join(f"{c} · {titles[c]}" for c in codes)
    return tr(lang, "Linked to open question: ", "Koblet til åpent spørsmål: ") + linked


def _answer_header(codes: list[str]) -> None:
    st.divider()
    st.subheader(tr(lang, "Synthesis", "Syntese"))
    st.caption(_routing_caption(codes))


def _render_feedback(answer_id: str) -> None:
    """Rating form under the answer. One submission per answer_id."""
    rated = st.session_state.setdefault("areal_rated", set())
    thanks = tr(lang, "Thank you for your feedback.", "Takk for tilbakemeldingen.")
    if answer_id in rated:
        st.success(thanks)
        return
    choices = ["ja", "delvis", "nei"]
    choice_label = {
        "ja": tr(lang, "Yes", "Ja"),
        "delvis": tr(lang, "Partly", "Delvis"),
        "nei": tr(lang, "No", "Nei"),
    }
    # Sent as for_kort|passe|for_lang so the sheet columns stay language-neutral.
    length_choices = ["for_kort", "passe", "for_lang"]
    length_label = {
        "for_kort": tr(lang, "Too short", "For kort"),
        "passe": tr(lang, "About right", "Passe"),
        "for_lang": tr(lang, "Too long", "For lang"),
    }
    slot = st.empty()
    with slot.container():
        with st.form(f"areal_feedback_{answer_id}"):
            st.markdown(f"**{tr(lang, 'Help us: how was this answer?', 'Hjelp oss: hvordan var svaret?')}**")
            thumbs = st.feedback("thumbs", key=f"areal_thumbs_{answer_id}")
            answered = st.radio(
                tr(lang, "Did it answer the question?", "Svarte det på spørsmålet?"),
                options=choices,
                format_func=choice_label.get,
                index=None,
                horizontal=True,
                key=f"areal_answered_{answer_id}",
            )
            fair = st.radio(
                tr(
                    lang,
                    "Did the answer show the disagreement fairly?",
                    "Viste svaret uenigheten på en rettferdig måte?",
                ),
                options=choices,
                format_func=choice_label.get,
                index=None,
                horizontal=True,
                key=f"areal_fair_{answer_id}",
            )
            length = st.radio(
                tr(lang, "Was the length right?", "Var lengden passe?"),
                options=length_choices,
                format_func=length_label.get,
                index=None,
                horizontal=True,
                key=f"areal_length_{answer_id}",
            )
            readable = st.radio(
                tr(lang, "Was the answer easy to read?", "Var svaret lett å lese?"),
                options=choices,
                format_func=choice_label.get,
                index=None,
                horizontal=True,
                key=f"areal_readable_{answer_id}",
            )
            comment = st.text_area(
                tr(lang, "Is anything wrong or missing? (optional)", "Er noe feil eller mangler? (valgfritt)"),
                key=f"areal_comment_{answer_id}",
            )
            sent = st.form_submit_button(tr(lang, "Send feedback", "Send tilbakemelding"), type="primary")
    if sent:
        feedback.log_rating(
            session_id=st.session_state["areal_session_id"],
            answer_id=answer_id,
            thumbs={1: "up", 0: "down"}.get(thumbs, ""),
            answered_question=answered or "",
            fair_disagreement=fair or "",
            comment=comment.strip(),
            length=length or "",
            readability=readable or "",
        )
        rated.add(answer_id)
        slot.empty()
        st.success(thanks)


def _render_sources(results: list[dict]) -> None:
    st.divider()
    st.subheader(tr(lang, f"Retrieved sources ({len(results)})", f"Hentede kilder ({len(results)})"))
    for r in results:
        title = r.get("title") or r.get("doc_id")
        cite = _source_label(lang, r.get("authors", ""), r.get("year", ""), title)
        with st.expander(f"**{cite}** · {title[:90]}"):
            st.markdown(f"**{title}**")
            if r.get("via_pq"):
                st.caption(tr(lang, "Selected via ", "Valgt via ") + ", ".join(r["via_pq"]))
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
            if mode == "researcher":  # internal codes are only useful to experts
                qs = r.get("priority_questions") or []
                if qs:
                    st.caption(" · ".join(str(q) for q in qs))
                st.caption(f"doc_id: `{r.get('doc_id', '')}`")


def _render_answer(text: str, answer_mode: str) -> None:
    """The whole answer, open, in every mode. Nothing is folded away. The keyed
    container lets the CSS in ui.py set in-text headings at body size."""
    with st.container(key=ANSWER_TEXT_KEY):
        st.markdown(text)


def _render_last(last: dict) -> None:
    """Render a stored answer: synthesis, feedback form, sources. Older session state
    may still carry a `card_n` key from the removed question box; it is ignored."""
    _answer_header(last.get("routed_pq") or [])
    _render_answer(last["answer"], last.get("mode", mode))
    _render_feedback(last["answer_id"])
    _render_sources(last["results"])


def _stream_answer(client: OpenAI, q: str, results: list[dict], holder, codes: list[str]) -> str:
    """Stream the synthesis into `holder`. Returns the full text (stripped)."""
    status = st.empty()
    status.caption(tr(lang, "Writing the synthesis...", "Skriver syntese..."))

    def deltas():
        pieces = synthesise_stream(
            client,
            q,
            results,
            mode=mode,
            answer_format=answer_format,
            output_language=output_language,
            model=AREAL_MODEL,
            room="areal",
        )
        for piece in pieces:
            status.empty()  # first token arrived
            yield piece

    try:
        with holder.container():
            _answer_header(codes)
            with st.container(key=ANSWER_TEXT_KEY):
                text = st.write_stream(deltas())
    finally:
        status.empty()
    return str(text or "").strip()


def _ask(q: str) -> None:
    """One question: cache lookup, retrieval, streamed synthesis, logging.
    On success the answer is stored in session state and shown."""
    started = time.perf_counter()
    answer_id = uuid.uuid4().hex
    st.session_state.pop("areal_last", None)  # a new question replaces the old answer

    if not corpus_ready:
        st.error(tr(lang, "Corpus not ready.", "Korpuset er ikke klart."))
        return
    if not selected_doc_ids:
        st.error(
            tr(
                lang,
                "Select at least one document under Documents in the corpus before asking.",
                "Velg minst ett dokument under Dokumenter i korpuset før du spør.",
            )
        )
        return

    key = feedback.answer_cache_key(q, mode, lang, top_k, selected_doc_ids, AREAL_MODEL)
    last = {
        "answer_id": answer_id,
        "query": q,
        "mode": mode,
        "lang": lang,
        "results": [],
        "answer": "",
        "latency_s": 0.0,
        "cached": False,
        "routed_pq": [],
    }

    hit = feedback.cache_get(key)
    if hit is not None:
        results, answer, *rest = hit
        codes = list(rest[0]) if rest else []
        last.update(results=results, answer=answer, routed_pq=codes, latency_s=time.perf_counter() - started, cached=True)
        st.session_state["areal_last"] = last
        _log_answer(answer_id, q, results, answer, started, cached=True, routed_pq=codes)
        _render_last(last)
        return

    if st.session_state.get("areal_n_asked", 0) >= MAX_UNCACHED_PER_SESSION:
        st.info(
            tr(
                lang,
                f"You have reached the limit of {MAX_UNCACHED_PER_SESSION} new questions in this session. "
                "Questions that have already been answered stay available. Thank you for testing.",
                f"Du har nådd grensen på {MAX_UNCACHED_PER_SESSION} nye spørsmål i denne økten. "
                "Spørsmål som allerede er besvart, er fortsatt tilgjengelige. Takk for at du tester.",
            )
        )
        return

    client = get_client()
    if not client:
        return

    codes: list[str] = []
    try:
        with st.spinner(tr(lang, "Retrieving relevant documents...", "Henter relevante dokumenter...")):
            # A question repeated verbatim from the nine (either language) needs no classifier.
            code = pq_code_for_text(q, [f[2] for f in FAULTS[lang]]) or pq_code_for_text(
                q, [f[2] for f in FAULTS["en" if lang == "no" else "no"]]
            )
            if code:
                codes = [code]
            else:
                codes = classify_pq(client, q, [f[2] for f in FAULTS[lang]])
            results = retrieve_funnel(
                client,
                q,
                codes,
                top_k=top_k,
                selected_doc_ids=selected_doc_ids,
                data_file=AREAL_DATA_FILE,
            )
    except Exception as exc:
        _warn_failure(exc)
        _log_answer(answer_id, q, [], "", started, cached=False, error=type(exc).__name__)
        return
    if not results or (not codes and is_out_of_scope(results)):
        st.warning(
            tr(
                lang,
                "This question appears to fall outside this corpus. "
                "Try a question about sea area, locality or coastal-zone planning, or pick an open question in section C.",
                "Spørsmålet ser ut til å ligge utenfor dette korpuset. "
                "Prøv et spørsmål om sjøareal, lokalitet eller kystsoneplan, eller velg et av de åpne spørsmålene i seksjon C.",
            )
        )
        _log_answer(answer_id, q, results, "", started, cached=False, error="out_of_scope", routed_pq=codes)
        return

    st.session_state["areal_n_asked"] = st.session_state.get("areal_n_asked", 0) + 1
    holder = st.empty()
    try:
        answer = _stream_answer(client, q, results, holder, codes)
    except Exception as exc:
        holder.empty()
        _warn_failure(exc)
        _log_answer(answer_id, q, results, "", started, cached=False, error=type(exc).__name__, routed_pq=codes)
        return
    if not answer:
        holder.empty()
        _warn_failure(None)
        _log_answer(answer_id, q, results, "", started, cached=False, error="EmptyAnswer", routed_pq=codes)
        return

    last.update(results=results, answer=answer, routed_pq=codes, latency_s=time.perf_counter() - started)
    st.session_state["areal_last"] = last
    feedback.cache_put(key, (results, answer, codes))
    _log_answer(answer_id, q, results, answer, started, cached=False, routed_pq=codes)
    # The answer is already on screen from the stream; add what goes below it.
    _render_feedback(answer_id)
    _render_sources(results)


# The finished answer lives in session state, so it survives reruns triggered by
# other widgets. The run that produces it streams it (and renders nothing twice);
# later reruns re-render it from session state.
if run and query.strip():
    _ask(query.strip())
elif st.session_state.get("areal_last"):
    _render_last(st.session_state["areal_last"])

st.caption(
    tr(
        lang,
        "Editorial orientation · last reviewed 2026-10-19 · the answers search the active documents.",
        "Redaksjonell orientering · sist gjennomgått 2026-10-19 · svarene søker i de aktive dokumentene.",
    )
)

st.markdown(
    tr(
        lang,
        '<div class="hl-footer">Havbruksløftets Evidensrom. Prototype room on area and aquaculture. '
        "Honest Broker: we show the open questions, competing diagnoses, and where the file is empty.</div>",
        '<div class="hl-footer">Havbruksløftets Evidensrom. Prototype-rom om areal og havbruk. '
        "Honest Broker: vi viser de åpne spørsmålene, konkurrerende diagnoser, og der saksfilen er tom.</div>",
    ),
    unsafe_allow_html=True,
)
