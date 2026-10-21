"""Regelverk: lover og forskrifter som rammer inn havbrukets arealbruk (kontekst, ikke søkbart)."""

from __future__ import annotations

import streamlit as st

REGELVERK: list[dict] = [
    {
        "name_no": "Akvakulturloven",
        "name_en": "Aquaculture Act",
        "kind": "lov",
        "ministry_no": "Nærings- og fiskeridepartementet",
        "url": "https://lovdata.no/dokument/NL/lov/2005-06-17-79",
        "about_no": "Hovedloven for havbruk: krever tillatelse for å drive akvakultur og setter vilkår for tildeling og plassering av lokaliteter.",
        "about_en": "The main aquaculture law: requires a permit to farm and sets conditions for allocating permits and siting localities.",
    },
    {
        "name_no": "Laksetildelingsforskriften",
        "name_en": "Salmon Allocation Regulation",
        "kind": "forskrift",
        "ministry_no": "Nærings- og fiskeridepartementet",
        "url": "https://lovdata.no/forskrift/2022-11-07-1929",
        "about_no": "Regulerer tildeling av tillatelser til oppdrett av laks, ørret og regnbueørret, og dermed produksjonskapasiteten.",
        "about_en": "Regulates the allocation of permits to farm salmon, trout and rainbow trout, and thereby production capacity.",
    },
    {
        "name_no": "Produksjonsområdeforskriften",
        "name_en": "Production Area Regulation",
        "kind": "forskrift",
        "ministry_no": "Nærings- og fiskeridepartementet",
        "url": "https://lovdata.no/forskrift/2017-01-16-61",
        "about_no": "Deler kysten inn i 13 produksjonsområder og kobler produksjonskapasiteten til et trafikklyssystem.",
        "about_en": "Divides the coast into 13 production areas and links production capacity to a traffic-light system.",
    },
    {
        "name_no": "Andre arter-forskriften",
        "name_en": "Regulation on Aquaculture of Other Species",
        "kind": "forskrift",
        "ministry_no": "Nærings- og fiskeridepartementet",
        "url": "https://lovdata.no/forskrift/2004-12-22-1799",
        "about_no": "Regulerer tillatelser til akvakultur av andre arter enn laks, ørret og regnbueørret.",
        "about_en": "Regulates permits for aquaculture of species other than salmon, trout and rainbow trout.",
    },
    {
        "name_no": "Samordningsforskriften",
        "name_en": "Coordination and Deadlines Regulation",
        "kind": "forskrift",
        "ministry_no": "Nærings- og fiskeridepartementet",
        "url": "https://lovdata.no/forskrift/2010-05-18-708",
        "about_no": "Fastsetter samordning og tidsfrister i behandlingen av søknader om akvakultur.",
        "about_en": "Sets coordination rules and deadlines for processing aquaculture applications.",
    },
    {
        "name_no": "Laksevassdragsforskriften",
        "name_en": "Regulation on National Salmon Rivers and Fjords",
        "kind": "forskrift",
        "ministry_no": "Nærings- og fiskeridepartementet",
        "url": "https://lovdata.no/forskrift/2009-06-22-961",
        "about_no": "Setter særskilte krav til akvakultur i eller ved nasjonale laksevassdrag og nasjonale laksefjorder.",
        "about_en": "Sets special requirements for aquaculture in or near national salmon rivers and national salmon fjords.",
    },
    {
        "name_no": "Kvalitetsnorm for villaks",
        "name_en": "Quality Standard for Wild Atlantic Salmon",
        "kind": "forskrift",
        "ministry_no": "Klima- og miljødepartementet",
        "url": "https://lovdata.no/dokument/SF/forskrift/2013-09-20-1109",
        "about_no": "Setter mål for tilstanden i ville laksebestander, blant annet for genetisk innblanding fra rømt oppdrettslaks.",
        "about_en": "Sets targets for the state of wild salmon stocks, including genetic introgression from escaped farmed salmon.",
    },
    {
        "name_no": "Plan- og bygningsloven",
        "name_en": "Planning and Building Act",
        "kind": "lov",
        "ministry_no": "Kommunal- og distriktsdepartementet",
        "url": "https://lovdata.no/dokument/NL/lov/2008-06-27-71",
        "about_no": "Kommunene fastsetter i arealplaner hvilke sjøområder som kan brukes til akvakultur.",
        "about_en": "Municipalities designate in their area plans which sea areas can be used for aquaculture.",
    },
    {
        "name_no": "Konsekvensutredningsforskriften",
        "name_en": "Impact Assessment Regulation",
        "kind": "forskrift",
        "ministry_no": "Klima- og miljødepartementet, Kommunal- og distriktsdepartementet",
        "url": "https://lovdata.no/forskrift/2017-06-21-854",
        "about_no": "Stiller krav til miljøkonsekvensutredning av planer, som kan omfatte arealplanlegging i sjø.",
        "about_en": "Sets requirements for environmental impact assessment of plans, which can include planning of sea areas.",
    },
    {
        "name_no": "Dyrevelferdsloven",
        "name_en": "Animal Welfare Act",
        "kind": "lov",
        "ministry_no": "Landbruks- og matdepartementet",
        "url": "https://lovdata.no/dokument/NL/lov/2009-06-19-97",
        "about_no": "Stiller krav til dyrs velferd, også fisk i oppdrett.",
        "about_en": "Sets welfare requirements for animals, including farmed fish.",
    },
    {
        "name_no": "Matloven",
        "name_en": "Food Act",
        "kind": "lov",
        "ministry_no": "Helse- og omsorgsdepartementet",
        "url": "https://lovdata.no/dokument/NL/lov/2003-12-19-124",
        "about_no": "Stiller krav til mattrygghet og fiskehelse; Mattilsynet fører tilsyn.",
        "about_en": "Sets food-safety and fish-health requirements; the Norwegian Food Safety Authority (Mattilsynet) supervises.",
    },
    {
        "name_no": "Havne- og farvannsloven",
        "name_en": "Harbour and Fairway Act",
        "kind": "lov",
        "ministry_no": "Nærings- og fiskeridepartementet",
        "url": "https://lovdata.no/dokument/NL/lov/2019-06-21-70",
        "about_no": "Sikrer trygg ferdsel i farvannet; Kystverket må gi tillatelse når et anlegg kan påvirke sikkerhet eller ferdsel.",
        "about_en": "Protects safe navigation; the Coastal Administration (Kystverket) must give permission when a farm may affect safety or traffic.",
    },
    {
        "name_no": "Forurensningsloven",
        "name_en": "Pollution Control Act",
        "kind": "lov",
        "ministry_no": "Klima- og miljødepartementet",
        "url": "https://lovdata.no/dokument/NL/lov/1981-03-13-6",
        "about_no": "Regulerer utslipp og forurensning; Statsforvalteren gir utslippstillatelse til oppdrettsanlegg.",
        "about_en": "Regulates pollution and discharges; the County Governor (Statsforvalteren) grants discharge permits to fish farms.",
    },
    {
        "name_no": "Naturmangfoldloven",
        "name_en": "Nature Diversity Act",
        "kind": "lov",
        "ministry_no": "Klima- og miljødepartementet",
        "url": "https://lovdata.no/dokument/NL/lov/2009-06-19-100",
        "about_no": "Skal ta vare på naturens mangfold; forsiktighetsprinsippet gjelder når kunnskapen er usikker.",
        "about_en": "Aims to conserve nature's diversity; the precautionary principle applies where knowledge is uncertain.",
    },
    {
        "name_no": "Friluftsloven",
        "name_en": "Outdoor Recreation Act",
        "kind": "lov",
        "ministry_no": "Klima- og miljødepartementet",
        "url": "https://lovdata.no/dokument/NL/lov/1957-06-28-16",
        "about_no": "Gir allmennheten rett til ferdsel og opphold i utmark, blant annet langs kysten.",
        "about_en": "Gives the public a right of access and outdoor recreation, including along the coast.",
    },
    {
        "name_no": "Vannressursloven",
        "name_en": "Water Resources Act",
        "kind": "lov",
        "ministry_no": "Energidepartementet",
        "url": "https://lovdata.no/dokument/NL/lov/2000-11-24-82",
        "about_no": "Regulerer bruk og vern av vassdrag og grunnvann; mest relevant for land- og ferskvannsbaserte anlegg.",
        "about_en": "Regulates use and protection of water resources; mainly relevant for land-based and freshwater facilities.",
    },
    {
        "name_no": "Sameloven kapittel 4",
        "name_en": "Sámi Act, chapter 4",
        "kind": "lov",
        "ministry_no": "Kommunal- og distriktsdepartementet",
        "url": "https://lovdata.no/dokument/NL/lov/1987-06-12-56/KAPITTEL_4",
        "about_no": "Pålegger myndighetene å konsultere samiske interesser før vedtak som kan påvirke dem direkte, også om arealbruk.",
        "about_en": "Requires authorities to consult Sámi interests before decisions that may affect them directly, including on area use.",
    },
]

_KIND_LABEL = {
    "no": {"lov": "Lov", "forskrift": "Forskrift"},
    "en": {"lov": "Act", "forskrift": "Regulation"},
}


def render_regelverk(lang: str) -> None:
    """Render the Regelverk section. `lang` is "no" or "en"; anything else falls back to English."""
    no = lang == "no"
    labels = _KIND_LABEL["no" if no else "en"]

    if no:
        st.caption(
            "Lover og forskrifter som styrer hvor og hvordan havbruk kan etableres. "
            "De er kontekst for lesingen. Verktøyet søker ikke i lovtekstene."
        )
    else:
        st.caption(
            "Laws and regulations that govern where and how aquaculture can be established. "
            "They are context for reading. The tool does not search the legal texts."
        )

    for item in REGELVERK:
        name = item["name_no"] if no else item["name_en"]
        about = item["about_no"] if no else item["about_en"]
        st.markdown(f"[**{name}**]({item['url']})")
        st.caption(f"{labels[item['kind']]} · {item['ministry_no']}")
        st.markdown(about)
