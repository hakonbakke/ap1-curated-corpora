"""
Åpne spørsmål i Areal og havbruk, som kort gruppert etter tema.

Hvert kort er en fortetning av den redaksjonelle teksten i FAULTS på siden
(spørsmål n = FAULTS[lang][n - 1]); punktene skal ikke si mer enn den teksten.
«Kildene peker på ulike svar» brukes bare der teksten selv sier at kildene
er uenige. Utkast 2026-10-22, ikke godkjent av utvelgerne.
"""

from __future__ import annotations

DIVERGE = {"no": "Kildene peker på ulike svar:", "en": "The sources point to different answers:"}
SHOW = {"no": "Det kildene viser:", "en": "What the sources show:"}

GROUPS: list[dict] = [
    {
        "title_no": "Vekst og grenser",
        "title_en": "Growth and its limits",
        "cards": [
            {
                "n": 1,
                "title_no": "Hva setter grensen for vekst?",
                "title_en": "What sets the limit on growth?",
                "intro": DIVERGE,
                "points": [
                    {
                        "no": "Produksjonstillatelser og trafikklys, selv om noen regioner er fulle.",
                        "en": "Production licences and the traffic-light system, though some regions are full.",
                        "docs": ["2020_hersoug_whats-the-clue"],
                    },
                    {
                        "no": "For få gode lokaliteter, og kommunens vilje til å peke ut sjø.",
                        "en": "Too few good sites, and the municipality's willingness to designate sea.",
                        "docs": ["2015_sandersen_access-to-sites", "2011_gullestad_arealbruk-havbruk"],
                    },
                    {
                        "no": "Miljø, fiskevelferd og økonomi: stor vekst går ikke med dagens teknologi og drift.",
                        "en": "Environment, fish welfare and economics: large growth is not possible with today's technology and operations.",
                        "docs": ["undated_baerekraftig-arealbruk-havbruk"],
                    },
                    {
                        "no": "Én miljønektelse kan stoppe en lokalitet, selv om en samlet avveining ville pekt en annen vei.",
                        "en": "A single environmental refusal can stop a site, even where an overall weighing would point the other way.",
                        "docs": ["2015_rettslig_rammeverk-havbruk"],
                    },
                ],
                "open_no": "Ingen tekst prøver diagnosene mot samme kyst og samme år.",
                "open_en": "No text tests the diagnoses against the same coast and the same year.",
            },
            {
                "n": 2,
                "title_no": "Hvilken faktor binder først?",
                "title_en": "Which factor binds first?",
                "intro": SHOW,
                "points": [
                    {
                        "no": "Produksjonstillatelsen styres av trafikklyset; lokalitetstillatelsen må ligge i kommunens plan.",
                        "en": "The production licence is governed by the traffic light; the site licence must fit the municipal plan.",
                        "docs": ["2022_hersoug_ten-licensing-systems"],
                    },
                    {
                        "no": "Lus, rømming, tap og avstand mellom anlegg former arealstrukturen.",
                        "en": "Lice, escapes, losses and distance between farms shape the spatial structure.",
                        "docs": ["2011_gullestad_arealbruk-havbruk", "2020_hersoug_whats-the-clue"],
                    },
                    {
                        "no": "Brakklegging og flytterestriksjoner krever flere lokaliteter enn tillatelsene dekker (Trøndelag).",
                        "en": "Fallowing and movement restrictions require more sites than the licences cover (Trøndelag).",
                        "docs": ["2025_sand_havbrukets-arealbehov-trondelag"],
                    },
                    {
                        "no": "Kommunens plan er porten, men større planområder gir få sikre nye arealer.",
                        "en": "The municipal plan is the gate, but larger plan areas yield few secure new sites.",
                        "docs": ["2017_kvalvik_intermunicipal-coastal-planning", "2019_mikkelsen_arealplanlegging-sjo"],
                    },
                ],
                "open_no": "Hvilken faktor som binder først, og hvor de trekker i hver sin retning.",
                "open_en": "Which factor binds first, and where they pull in different directions.",
            },
            {
                "n": 8,
                "title_no": "Hva kan næringen gjøre selv?",
                "title_en": "What can the industry do itself?",
                "intro": SHOW,
                "points": [
                    {
                        "no": "Samarbeid om brakklegging, utsett og beredskap er i stor grad frivillig.",
                        "en": "Cooperation on fallowing, stocking and preparedness is largely voluntary.",
                        "docs": ["2019_karlsen_omradesamarbeid"],
                    },
                    {
                        "no": "Selskapene deler biologisk risiko og regulatorisk press i uformelle nettverk.",
                        "en": "Companies share biological risk and regulatory pressure in informal networks.",
                        "docs": ["2026_bjorna_adaptive-co-management", "2021_osmundsen_shared-waters"],
                    },
                    {
                        "no": "Drift i en åpen allmenning krever koordinert bruk av lokaliteter.",
                        "en": "Farming in an open commons requires coordinated use of sites.",
                        "docs": ["undated_baerekraftig-arealbruk-havbruk"],
                    },
                ],
                "open_no": "Om frivillig sonesamarbeid gir mer effektiv arealbruk, er omstridt. Effekten av felles brakklegging på lus er usikker.",
                "open_en": "Whether voluntary zone cooperation makes area use more efficient is disputed. The effect of joint fallowing on lice is uncertain.",
            },
        ],
    },
    {
        "title_no": "Plan, søknad og styring",
        "title_en": "Plans, applications and governance",
        "cards": [
            {
                "n": 3,
                "title_no": "Hvor stopper søknaden om lokalitet?",
                "title_en": "Where do site applications stall?",
                "intro": SHOW,
                "points": [
                    {
                        "no": "Fylkeskommunen vedtar, men Mattilsynet, Statsforvalteren og Kystverket kan hver for seg si nei.",
                        "en": "The county decides, but the Food Safety Authority, the County Governor and the Coastal Administration can each say no.",
                        "docs": ["2023_evenset_sameksistens"],
                    },
                    {
                        "no": "Fristene ryker oftere hos Mattilsynet og Statsforvalteren enn hos fylket.",
                        "en": "Deadlines are missed more often at the Food Safety Authority and the County Governor than at the county.",
                        "docs": ["2025_osmundsen_fylkeskommune-akvakulturloven"],
                    },
                    {
                        "no": "Smitterisiko dominerer Mattilsynets avslag (251 avslag, 2020–2025).",
                        "en": "Disease risk dominates the Food Safety Authority's refusals (251 refusals, 2020–2025).",
                        "docs": ["salt_1110_lokalitetssoknader"],
                    },
                ],
                "open_no": "Hvor mye av forsinkelsen skyldes kunnskapsmangel, og hvor mye at etatene verner hvert sitt hensyn.",
                "open_en": "How much of the delay comes from missing knowledge, and how much from each agency guarding its own concern.",
            },
            {
                "n": 5,
                "title_no": "Får penger kommunene til å si ja?",
                "title_en": "Does money make municipalities say yes?",
                "intro": SHOW,
                "points": [
                    {
                        "no": "Verstefall: kommunen får pengene og peker likevel ikke ut mer sjø.",
                        "en": "Worst case: the municipality gets the money and still designates no more sea.",
                        "docs": ["2015_sandersen_access-to-sites"],
                    },
                    {
                        "no": "Overføringene fra Havbruksfondet veier ofte ikke opp for husholdningenes ønske om å unngå mer havbruk.",
                        "en": "Transfers from the Aquaculture Fund often do not outweigh households' wish to avoid more aquaculture.",
                        "docs": ["2020_aanesen_arctic-aquaculture-cba"],
                    },
                    {
                        "no": "Folk i havbrukskommuner er mer positive til næringen, men ikke mer fornøyde med fordelingen.",
                        "en": "People in aquaculture municipalities are more positive to the industry, but not more satisfied with the distribution.",
                        "docs": ["2023_misund_political-economy-salmon"],
                    },
                ],
                "open_no": "Om pengene faktisk åpner mer sjø, er ikke testet i settet.",
                "open_en": "Whether the money actually opens more sea is not tested in the set.",
            },
            {
                "n": 7,
                "title_no": "Konflikt om sjøen: hva gir legitimitet?",
                "title_en": "Conflict over the sea: what builds legitimacy?",
                "intro": SHOW,
                "points": [
                    {
                        "no": "Når interessene spriker, faller utpekingen ofte tilbake til den enkelte kommunen.",
                        "en": "When interests diverge, designation often falls back to the individual municipality.",
                        "docs": ["2017_kvalvik_intermunicipal-coastal-planning", "2021_sandersen_kystsone-helgeland"],
                    },
                    {
                        "no": "Det er et legitimitetsgap mot fiskere, mens innbyggerne er mer positive.",
                        "en": "There is a legitimacy gap with fishers, while residents are more positive.",
                        "docs": ["2020_bjorkan_local-perceptions"],
                    },
                    {
                        "no": "Legitimitet henger på om konsekvensvurderingene er gjennomsiktige og like fra sak til sak.",
                        "en": "Legitimacy depends on impact assessments being transparent and consistent from case to case.",
                        "docs": ["2022_mikkelsen_ocean-coastal-management"],
                    },
                    {
                        "no": "Mer helhet i plandokumentet avgjør ikke i seg selv utfallet.",
                        "en": "A more holistic plan document does not in itself settle the outcome.",
                        "docs": ["2026_sordahl_nar-alt-skal-med"],
                    },
                ],
                "open_no": "Hvordan forutsigbare tillatelser kan forenes med å endre vilkår når miljøvirkningene endrer seg.",
                "open_en": "How predictable licences can be reconciled with changing conditions when environmental effects change.",
            },
        ],
    },
    {
        "title_no": "Kunnskap, miljø og smitte",
        "title_en": "Knowledge, environment and disease",
        "cards": [
            {
                "n": 4,
                "title_no": "Hvem vurderer samlet belastning?",
                "title_en": "Who assesses cumulative impact?",
                "intro": DIVERGE,
                "points": [
                    {
                        "no": "KU-forskriften krever vurdering av samlede påvirkninger, men sier ikke hvordan.",
                        "en": "The impact-assessment regulation requires cumulative effects to be assessed, but not how.",
                        "docs": ["2025_mikkelsen_samlet-pavirkning-nord"],
                    },
                    {
                        "no": "Det mangler metoder og data for kumulative miljøvirkninger.",
                        "en": "Methods and data for cumulative environmental effects are lacking.",
                        "docs": ["2023_evenset_sameksistens"],
                    },
                    {
                        "no": "Smitte og lus bør i stor grad vurderes av andre enn kommuneplanens konsekvensutredning.",
                        "en": "Disease and lice should largely be assessed by others than the municipal plan's impact assessment.",
                        "docs": ["salt_1065_ku-arealplanlegging"],
                    },
                    {
                        "no": "Omvendt planmetodikk flyttet konfliktavklaringen ut av planen.",
                        "en": "Reverse planning moved conflict resolution out of the plan.",
                        "docs": ["2021_sandersen_kystsone-helgeland"],
                    },
                ],
                "open_no": "Lovene krever en samlet vurdering, men hvem som skal gjøre den, og med hvilket grunnlag, er uavklart.",
                "open_en": "The law requires a cumulative assessment, but who should make it, and on what basis, is unsettled.",
            },
            {
                "n": 6,
                "title_no": "Hva bygger arealvedtakene på?",
                "title_en": "What do area decisions rest on?",
                "intro": SHOW,
                "points": [
                    {
                        "no": "Temadata er dårlig tilrettelagt, og vurderingene varierer mellom planene.",
                        "en": "Thematic data are poorly prepared, and assessments vary between plans.",
                        "docs": ["2014_robertsen_interkommunal-planlegging", "salt_1065_ku-arealplanlegging"],
                    },
                    {
                        "no": "Svak konsistens i hva som vektes, på tvers av 143 foreslåtte havbruksområder.",
                        "en": "Weak consistency in what is weighted, across 143 proposed aquaculture areas.",
                        "docs": ["2022_mikkelsen_ocean-coastal-management"],
                    },
                    {
                        "no": "Marine grunnkart anslås å kunne redusere risikoen ved nye lokaliteter.",
                        "en": "Marine base maps are estimated to reduce the risk of new sites.",
                        "docs": ["2023_metier_marine-grunnkart"],
                    },
                    {
                        "no": "Behovet for skjermet kystareal avhenger av om ny teknologi blir lønnsom.",
                        "en": "The need for sheltered coastal area depends on whether new technology becomes profitable.",
                        "docs": ["2020_hersoug_whats-the-clue", "undated_baerekraftig-arealbruk-havbruk"],
                    },
                ],
                "open_no": "Hvor mye ny teknologi faktisk flytter lokaliteter, er bare beskrevet kvalitativt.",
                "open_en": "How much new technology actually moves sites is described only qualitatively.",
            },
            {
                "n": 9,
                "title_no": "Smitte mellom anlegg: hvor mye betyr avstand?",
                "title_en": "Disease between farms: how much does distance matter?",
                "intro": SHOW,
                "points": [
                    {
                        "no": "En stor del av PD-smitten kommer fra naboanlegg.",
                        "en": "A large share of PD infection comes from neighbouring farms.",
                        "docs": ["2015_aldrin_pd-space-time"],
                    },
                    {
                        "no": "Færre og større anlegg lenger fra hverandre kan senke lusenivået (simulering).",
                        "en": "Fewer, larger farms further apart can lower lice levels (simulation).",
                        "docs": ["2024_qviller_geographic-redistribution"],
                    },
                    {
                        "no": "Tettere naboer henger sammen med høyere produksjonskostnad.",
                        "en": "Denser neighbours go with higher production costs.",
                        "docs": ["2025_kulmambetova_spatial-density-productivity"],
                    },
                ],
                "open_no": "Hvor stor avstand som faktisk bryter smittekontakten, og om felles brakklegging virker.",
                "open_en": "How much distance actually breaks disease contact, and whether joint fallowing works.",
            },
        ],
    },
]
