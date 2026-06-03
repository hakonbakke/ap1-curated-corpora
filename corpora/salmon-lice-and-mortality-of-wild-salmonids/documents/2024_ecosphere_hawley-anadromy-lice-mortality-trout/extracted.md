![image 1](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile1.png>)

Received: 4 March 2024 Revised: 25 September 2024 Accepted: 10 October 2024 DOI: 10.1002/ecs2.70098

###### A R T I C L E

C o a s t a l a n d M a r i n e E c o l o g y

## Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout

###### K. L. Hawley1,2 | H. A. Urke3 | T. Kristensen4 | T. O. Haugen2

1Norwegian Institute for Water Research, Oslo, Norway 2Faculty of Environmental Sciences and Natural Resource Management, The Norwegian University of Life Sciences, Ås, Norway 3AquaLife R&D, Trondheim, Norway 4Faculty of Biosciences and Aquaculture, Nord University, Bodø, Norway

Abstract

Facultative anadromous salmonids may alter migratory behavior to mitigate against detrimental infections of aquaculture-derived salmon lice (Lepeophtheirus salmonis); however, this likely incurs negative growth and fitness consequences. This flexibility in migratory behavior also creates analytical challenges in estimating lice infestation levels and the consequences of exposure. We utilized simulated individual migration trajectories of facultatively anadromous brown trout (Salmo trutta) (N = 8049), generated from spatialtemporal fjord-use models fitted to empirical tracking data (N = 517). These trajectories were superimposed with open-access spatial-temporal modeled lice densities. Individual accumulated lice exposure and infestation were simulated over a 6-month period for smolts and annually for veteran migrant life-stages. The degree of lice-induced mortality was estimated according to year (2013–2015), population (N = 5), and life-stage of brown trout, within a semi-enclosed fjord system (Sognefjorden, Norway). A gradient of lice was spatially distributed throughout the fjord. Highest densities were modeled in the outer-fjord at a closer vicinity to aquaculture facilities. Accordingly, estimates of accumulated lice infestation were higher for individuals that underwent long-distance migrations, residing for longer in the outer-fjord, with limited differences observed between years. As most brown trout remained in the inner-fjord, an area protected from aquaculture, individual accumulated levels of lice exposure and infestation were low, resulting in infestation estimates largely below critical-mortality thresholds. The fraction of total mortality attributed to lice during sea-sojourn was greater for long-distance migrants (smolts: 25.3%; veteran migrants: 14.8%) versus those remaining within the inner-fjord (smolts: 14.7%; veteran migrants: 1.7%). This resulted in an unequal contribution of lice to total mortality among populations (range: 3.3%–34.3%). Despite an equal distribution of lice exposure for all populations within the fjord, diverse mortality consequences among populations were estimated, largely resulting from individual selection of migration trajectory. Therefore, generic models of lice effects on facultative anadromous salmonids should be used with caution. Instead, the application of simulated migration trajectories

Correspondence K. L. Hawley Email: kate.hawley@niva.no

Funding information SalmonTracking 2030, Grant/Award Number: FHF 901890; Norwegian University for Life Sciences, Grant/Award Number: 1302051230; Sogn and Fjordane County Authority; E-Co Energi AS; Østfold Energi AS; Luster Municipality; Årdal Municipality; County Governor of Sogn and Fjordane; Mowi AS; Osland Havbruk AS; Sulefisk AS

Handling Editor: Sean P. Powers

This is an open access article under the terms of the Creative Commons Attribution License, which permits use, distribution and reproduction in any medium, provided the original work is properly cited. © 2024 The Author(s). Ecosphere published by Wiley Periodicals LLC on behalf of The Ecological Society of America.

Ecosphere. 2024;15:e70098. https://onlinelibrary.wiley.com/r/ecs2 1 of 21 https://doi.org/10.1002/ecs2.70098

to incorporate flexible behavior at the individual level is suggested. The findings indicate that Sognefjorden brown trout may have reduced their seaward migration extent to avoid direct mortality from salmon lice. This emphasizes the importance of monitoring and management actions to preserve selection for anadromy.

K E Y W O R D S acoustic telemetry, anthropogenic environmental change, aquaculture, fitness, Lepeophtheirus salmonis, marine feeding migration, Salmo trutta, survival

###### INTRODUCTION

The rapidly developing aquaculture industry produces approximately 50% of the global aquatic food production. Among the fishes cultivated, Atlantic salmon (Salmo salar) is of immense significance, with current worldwide production exceeding 2.8 million tons in 2022 (FAO, 2022). Atlantic salmon are intensively farmed predominantly in open cages situated within fjords and coastal areas. This practice has resulted in an increased abundance of the parasitic copepod Lepeophtheirus salmonis, or salmon louse, due to greater densities of available salmon lice hosts (Jansen et al., 2012; Krkosekˇ et al., 2013). While attached to a host, female salmon lice produce strings of eggs which develop into planktonic larval copepodids that are transported by water currents into the surrounding marine environment (Boxaspen, 2006; Heuch et al., 2005). This has altered parasite–host interactions, with spillover of salmon lice from farmed salmon, one of the major environmental concerns for wild salmonids in countries with intensive salmon farming (Bouwmeester et al., 2021; Forseth et al., 2017; Vollset et al., 2023). Salmon lice are obligate ectoparasites of salmonids in marine waters, where they feed upon the skin, mucus, and blood of their host, causing osmoregulatory and physiological challenges which may ultimately result in death (Boxaspen, 2006; Vollset et al., 2018). Sublethal salmon lice infestation may also affect behavior, growth, and age of maturity of their host (Birkeland & Jakobsen, 1997; Bjørn & Finstad, 1998; Eldøy et al., 2020; Finstad et al., 2000; Thorstad et al., 2015). Thus, accurate assessment of the transmission of salmon lice from farmed sources and the response of wild hosts is of considerable ecological, societal, and economic consequence, manifesting as a pertinent sustainability indicator for the aquaculture industry (Fiske et al., 2024; Stige

- et al., 2021). Separating the negative effects of salmon lice from


other factors is challenging in natural settings, with repercussions conditional on the size, migratory behavior, and habitat use of the wild host (Bøhn et al., 2020;

Halttunen, Gjelland, Glover, et al., 2018; Halttunen, Gjelland, Hamel, et al., 2018; Serra-Llinares et al., 2020; Simmons et al., 2019). In the obligate anadromous Atlantic salmon, which undertakes rapid migrations from natal rivers to the open ocean, the primary concern is reduced survival in small, first-time migrants (smolts) during periods of high salmon lice densities, with smaller fish most susceptible to lethal levels of salmon lice infection (Taranger et al., 2015). Methods to model mortality risk on out-migrating salmon smolts are established (e.g., Johnsen et al., 2021; Moriarty et al., 2023; Stige et al., 2021). These models are well-developed central reference tools, and in Norway, the world’s largest producer of Atlantic salmon, these models provide the foundation for a risk assessment–based adaptive management framework. This framework has been implemented to mitigate against salmon lice–induced mortality of wild Atlantic salmon smolts by regulating aquaculture production (Ministry of Trade, Industry and Fisheries, 2020).

In facultative anadromous salmonids, the consequences of salmon lice infection are often less absolute (Finstad et al., 2021; Thorstad et al., 2015). Evidence suggests that both the facultative anadromous brown trout (Salmo trutta) and Arctic charr (Salvelinus alpinus) can adapt their migratory behavior in response to high salmon lice concentrations. Affected individuals may reside closer to their natal river, interrupt, or even discontinue their sea-sojourn to return to fresh or brackish water that salmon lice cannot tolerate (Birkeland & Jakobsen, 1997; Halttunen, Gjelland, Hamel, et al., 2018; Serra-Llinares et al., 2020; Strøm et al., 2022). This behavior is thought to occur as both a salmon lice avoidance strategy and/or a method to actively delouse upon infection, where inner fjord areas and surface waters are less saline due to the river-fed inputs of freshwater. This behavior results in reduced access to marine habitats and reduced feeding time at sea, while simultaneously increasing energetic expenditures due to increased migration pathways (Finstad et al., 2021). Consequently, individual growth may be restricted, which in turn may delay maturity and/or reduce fecundity (Eldøy et al., 2020;

21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

Gargan et al., 2016; Strøm et al., 2022). Such trait changes have the potential to impact fitness and to impose selection pressures that may disfavor the expression and/or degree of anadromy (Adams et al., 2022; Bøhn, Nilsen, Gjelland, Biuw, Sandvik, Primicerio, Karlsen, Serra-Llinares, Sandvik, et al., 2022a; Spares et al., 2015; Thorstad et al., 2015).

Anadromous brown trout (sea trout hereafter) are especially vulnerable to salmon lice infestation as they utilize coastal environments in close vicinity to aquaculture facilities during their sea-sojourn, where planktonic and infectious salmon lice are distributed for extended periods (Thorstad et al., 2015). Typically, sea trout first migrate to sea as smolts after 1–3 years as juveniles in their natal stream, where they often remain in near-shore coastal and estuarine waters for a few weeks to months during spring/summer (Elliott, 1994; Jonsson & Jonsson, 2011; Klemetsen et al., 2003). This migration period often coincides with increasing water temperature and salmon lice production (Stien et al., 2005; Vollset et al., 2018). While at sea, sea trout swim actively and day-to-day variation in environmental conditions, threats, and opportunities can impact an individual’s choice of migration pathway and distance, even among those that have the same start and end points of migration (Birnie-Gauvin et al., 2019; del Villar-Guerra et al., 2014; Hawley et al., 2024a; Thorstad et al., 2016). The majority of sea trout return to freshwater to overwinter or spawn; however, residency at sea may in some cases last for a whole year or beyond among veteran migrants, that is, fish that have previously undertaken at least one sea-sojourn (Haraldstad et al., 2018; Jensen & Rikardsen, 2008, 2012). Many sea trout populations are considered greatly impacted by the effects of salmon lice (Fiske et al., 2024; Thorstad et al., 2015), yet sea trout are not currently included in Norway’s salmon lice management framework. While it is generally acknowledged that sea trout warrant inclusion, this has been hindered by analytical challenges in estimating salmon lice infestation levels on sea trout, as well as the direct and indirect consequences of salmon lice infection due to the behavioral plasticity of this facultatively anadromous species (Bøhn, Nilsen, Gjelland, Biuw, Sandvik, Primicerio, Karlsen, & Serra-Llinares, 2022; Finstad et al., 2021).

In this study, we aimed to estimate the expected degree of salmon lice-induced mortality according to year, population, and life-stage (smolt vs. veteran migrant) of sea trout, within a single fjord system, Sognefjorden. Located on the west coast of Norway, aquaculture facilities in the coastal and outer reaches of Sognefjorden (Figure 1) produced a total biomass of more than 67,000 tons of salmon, equating to approximately 3.6 million fish during 2015 (Appendix S1:

Table S1). In contrast, the inner fjord region has never been widely used for aquaculture, and formal protection against aquaculture development was granted in 2007 when Sognefjorden was designated a National Salmon Fjord. Sognefjorden is the longest fjord system in the world that supports populations of sea trout, with individuals migrating a distance of more than 200 km to reach the open coast (Figure 1) (Hawley et al., 2024a; Kristensen et al., 2011). However, the seaward extent of migration in Sognefjorden has diminished over a 60-year period and since the introduction of aquaculture in the region. During modern times, most sea trout migrate no further than the mid fjord region, with survival rates of long-distant migrants being lower than those remaining closer to their natal river (Hawley et al., 2024a).

We utilized simulated migration trajectories and estimates of survival that were derived from empirical in situ tracking data of sea trout sea-sojourn, from natal river to the open coast over a 3-year period. These trajectories were superimposed with openly available spatial-temporal modeled salmon lice densities (Sandvik, Ådlandsvik, et al., 2020; Sandvik, Johnsen, et al., 2020; Stige et al., 2021) of the same period. We then converted these values of environmental salmon lice exposure to transmission of salmon lice onto sea trout and estimated the probability of mortality due to the salmon lice infestation levels individually accumulated during sea-sojourn. Estimated rates of survival attributed to salmon lice infection were then compared with the estimates of absolute survival generated by the simulated migration trajectories to identify the fraction of total mortality attributed to infective salmon lice during sea-sojourn. This was conducted for each studied population and life-stage of sea trout from Sognefjorden. We expected to observe variation among years in the density of salmon lice within the fjord, as well as a spatial gradient of salmon lice distribution, with higher densities closer to aquaculture facilities, and very low densities within the protected inner fjord. Explicitly, we hypothesized that a spatial gradient of salmon lice density would mirror sea trout migration, with those individuals/populations most exposed to salmon lice due to a greater migratory distance and duration, being infected with the greatest number of salmon lice (H1). However, as sea trout predominately utilize the area of the fjord protected from aquaculture, we anticipated individual salmon lice infestation levels to be largely below critical thresholds expected to induce mortality (H2). Despite this, we expected salmon lice infestation to contribute toward total mortality during sea-sojourn, especially for those individuals and populations undertaking lengthier migrations (H3).

21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

![image 2](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile2.png>)

- F I G U R E 1 Map illustrating the location of Sognefjorden on the west coast of Norway and the nationwide distribution of marine salmonid farms (yellow dots). The inset presents a detailed distribution of active salmonid aquaculture facilities located within the county of Sogn and Fjordane during 2013–2015, as well as the five river arms of Sognefjorden that were included in the study. Fjord regions are colored according to given zone; orange, inner fjord; pink, mid fjord; purple, outer fjord. Red dots show sampling locations of the national salmon lice monitoring program (NALO, data are presented in Appendix S1: Table S2).


###### MATERIALS AND METHODS Study system

The study encompassed five adjacent rivers draining into four distinct fjord arms of inner-Sognefjorden (Aurland, Lærdal, Årdal, Fortun, Mørkrid; Figure 1), comprising a large majority of total sea trout production in the region. To aid spatial analyses, the extent of Sognefjorden was split into three geographical zones, defined as the inner, mid, and outer fjord, with a unique inner fjord zone for each fjord arm, and a collective mid and outer fjord zone for all populations (Figure 1). Sea trout originating from Mørkrid and Fortun have the furthest to travel to reach the mid fjord (48.8 km, an area of 129.2 km2), with the minimum migration distance of the inner fjord being 21.4 (67.4 km2), 8.5 (35.0 km2), and 22.4 km (43.2 km2) for Årdal, Lærdal, and Aurland populations, respectively. The mid fjord zone is 376.1 km2 (75.2 km long), and the outer fjord is both largest (1041.1 km2) and longest (93.3 km). Sognefjorden is included in the Norwegian national salmon lice monitoring program (NALO; Heuch et al., 2005); collated data include salmon lice counts on post-smolt Atlantic salmon held in cages and caught in trawls, and free-swimming sea trout caught within the fjord and coastal waters, using trawls and trap nets (see Figure 1 for sampling locations,

Appendix S1: Table S2 for sea trout data collected during 2013–2015; Bjørn et al., 2013; Nilsen et al., 2014, 2016).

###### Data analysis

Data encompassed a 3-year time series (2013–2015) of modeled weekly salmon lice density and transmission, which was used to estimate the accumulated salmon lice exposure and infection on two life-stages of individual anadromous brown trout at sea (simulated smolts N = 4234, simulated veteran migrants N = 3815), from five populations located in Sognefjorden, Norway (Figure 1). This study incorporates several existing models and datasets to address the research aims. A graphic overview illustrating the workflow, models, and data sources is given as conceptual aid (Figure 2). All statistical analyses were conducted using the R software, version 4.2.0 (R Core Team, 2022).

###### Simulated trajectories of sea trout migration and survival

This study utilized spatial-temporal trajectories of sea trout migration, derived from acoustic telemetry data of smolts (N = 175) and veteran migrants (N = 342) (Table 1, Hawley et al. 2024b). In short, acoustic

21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

Salmo tru a, Sogne orden

(SL monitoring NALO: Bjørn et al., 2013; Nilsen et al., 2014, 2016, 2018–2021)

(Tracking sample: Hawley et al., 2024)

![image 3](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile3.png>)

![image 4](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile4.png>)

![image 5](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile5.png>)

![image 6](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile6.png>)

![image 7](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile7.png>)

![image 8](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile8.png>)

![image 9](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile9.png>)

![image 10](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile10.png>)

#### (ZSL)

SLiinfIMR

p

### ZSL

### SSL

IMR WoY: 14–35

SmoltsIMR

WoY: 14–35

SmoltsIMR

SmoltsIMR

(Taranger et al., 2015)

(Sandvik et al., 2020)

(Bøhn et al., 2021)

p

#### (ZSL)

SLiinfNVI

### SSL

### ZSL

SmoltsNVI

WoY: 13–40

SmoltsNVI

SmoltsNVI

(Taranger et al., 2015)

(S ge et al., 2022)

NVI WoY: 1–52

p

SLiinfNVI

#### (ZSL)

(S ge et al., 2021)

### ZSL

### SSL

VeteransNVI

WoY: 1–52

VeteransNVI

, VeteransNVI

(Taranger et al., 2015)

(S ge et al., 2022)

![image 11](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile11.png>)

![image 12](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile12.png>)

![image 13](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile13.png>)

![image 14](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile14.png>)

![image 15](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile15.png>)

![image 16](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile16.png>)

![image 17](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile17.png>)

![image 18](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile18.png>)

![image 19](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile19.png>)

![image 20](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile20.png>)

![image 21](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile21.png>)

![image 22](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile22.png>)

![image 23](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile23.png>)

![image 24](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile24.png>)

![image 25](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile25.png>)

![image 26](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile26.png>)

![image 27](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile27.png>)

##### In-situ tracking

![image 28](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile28.png>)

![image 29](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile29.png>)

###### Simulated migra on trajectories

Salmo tru a Sogne orden: 5 rivers

# S

Smolts and veteran migrants 2013–2015

![image 30](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile30.png>)

![image 31](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile31.png>)

![image 32](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile32.png>)

![image 33](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile33.png>)

![image 34](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile34.png>)

![image 35](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile35.png>)

![image 36](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile36.png>)

![image 37](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile37.png>)

![image 38](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile38.png>)

![image 39](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile39.png>)

![image 40](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile40.png>)

![image 41](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile41.png>)

(Hawley et al., 2024)

(Hawley et al., 2024)

(Hawley et al., 2024)

- F I G U R E 2 Illustration of study design, data and model sources, where arrows indicate direction of workflow, green boxes a source of


empirical data, and gray boxes modeled predictions. Initially, the density of salmon lice in the environment (SLenv) was extracted for Sognefjorden (blue shading) from two models, produced by (1) the Institute of Marine Research (IMR) and (2) the Norwegian Veterinary Institute (NVI). To estimate weekly exposure of smolts to salmon lice, the SLenvIMR model was applied for the period week of year (WoY): 14–35, and the SLenvNVI model for the period WoY: 13–40. For veteran migrants, weekly salmon lice exposure was estimated over an annual period using the SLenvNVI model. These values were then converted into transmission of salmon lice (SLinf ) onto individual Salmo trutta (orange shading) smolts (IMR and NVI models) and veteran migrants (NVI model). These values were accumulated according to simulated individual trajectories of sea trout anadromy in Sognefjorden, which were derived from empirical tracking data. Each simulated individual was assigned a sea specific growth rate (gSW) according to life-stage, migration distance, and natal population. Fish length (TLSW) and weight (WtSW) of the simulated sample were estimated from empirical length–weight relationships of sea trout captured in Sognefjorden during the national salmon lice monitoring program (NALO). Individual probability of mortality due to salmon lice infestation (pðZSLÞ) was predicted according to stipulated salmon lice tolerance levels (SLinf =WtSW) of each life-stage. Estimated survival rates attributed to individual levels of salmon lice infestation (SSL) were compared with absolute simulated survival rates (STotal) to estimate the fraction of total mortality attributable to infective salmon lice (ZSL) for simulated sea trout smolts and veteran migrants of Sognefjorden.

telemetry allows for tracking of individually marked or tagged individuals in situ, from which statistical models targeting behavioral patterns can be built (Lennox et al., 2017). Given that sufficient data are derived, telemetry data lend itself to mark–recapture analyses, where a spatial, multistate model structure (conditional Arnason-Schwarz [CAS]; Arnason, 1973; Schwarz et al., 1993) produces survival and movement probabilities of tagged individuals while accounting for imperfect rates of detection. This is a shortcoming commonly encountered when tracking fish in larger marine systems. By combining CAS mark–recapture models and statistical

models of migration onset probability, migration duration, and maximum seaward migration distance (distance from river mouth), simulations of individual fjord-use trajectories and fates were run using 2013–2015 conditions as environmental frames. Model selection and parameters are outlined in Hawley et al. (2024a), as well as further methodological reasoning and description. To summarize, trajectories were built from simulations that were run using a weekly time resolution following 1000 individuals per river as initial populations, with each simulation iterated 100 times. The smolt simulations were run for a 6-month period (week of year [WoY]: 13–40,

21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

- T A B L E 1 Description of the simulated sample of Salmo trutta smolts and veteran migrants, from each study population of Sognefjorden, Norway.


Population Aurland Lærdal Årdal Fortun Mørkrid No. smolts 943 905 878 761 747

- gSW1 0.65 0.70 0.69 0.61 0.61 TLSW (cm) (range) 23.2 (16.7–30.5) 23.8 (16.1–31.1) 27.2 (21.9–31.1) 24.2 (16.3–29.8) 24.3 (16.6–29.8) WtSW (g) (range) 114.9 (39.6–248.0) 126.7 (35.6–265.0) 179.2 (91.2–263.7) 130.2 (36.8–233.0) 132.4 (38.7–233.2) No. veterans 950 957 945 963 0
- gSW2 (range) 0.38 (0.37–0.39) 0.37 (0.35–0.39) 0.38 (0.37–0.39) 0.38 (0.37–0.39) NA TLSW (cm) (range) 69.7 (28.1–89.6) 58.5 (27.5–89.9) 68.7 (28.7–89.7) 55.1 (29.3–88.2) NA WtSW (kg) (range) 6.15 (0.24–10.68) 4.22 (0.22–10.79) 5.85 (0.26–10.73) 2.66 (0.28–10.17) NA


Note: Each simulated individual was assigned a sea specific growth rate (gSW) according to life-stage, migration distance, and natal population. Fish length (TLSW) and weight (WtSW) of the simulated sample were estimated from empirical length–weight relationships of sea trout captured in Sognefjorden. Veteran migrant sea trout have previously undertaken at least one sea-sojourn; smolts are first-time sea migrants.

24 March to 29 September) and the veteran simulations for the entire year. The initial 1000 individuals were assigned trait values for total length (TLi) randomly drawn from river-specific trait summary statistics (i.e., TLi ¼rnorm μRTL,σRTL , where μ= mean and σ= SD) (Table 1), with simulations following each individual from week to week. The same initial 1000 individuals (i.e., same individual length) per population were used in each iteration. From each simulated iteration, the maximum distance reached (as fjord zone: inner, mid, or outer) per individual, river, and year was extracted from the initial population of 1000 fish (NStart). The number of surviving individuals (NSurv) was then calculated from the number of survivors per population, per year at the end of each run. Absolute simulated survival rate (STotal) was estimated from the fraction surviving dependent upon the maximum marine migration distance, per year at the end of each run (STotal ¼NSurv=NStart).

###### Sea trout growth

Sea growth of the simulated smolts was estimated from the first year sea age specific growth (gSW1) for each population (TLSW ¼TLeðgSW1PopÞ× 0:5), derived from reading individual fish scales (N =169; Hawley et al., 2024a; Table 1), where Mørkrid smolts were assigned equivalent gSW1Pop as Fortun smolts, due to the proximity of the two rivers (Figure 1), and a lack of samples from this population. For veteran migrants, individual sea growth was generated from the second sea age specific growth (gSW2). This was explicit to the maximum zone (maxZ) reached (TLSW ¼TLeðgmaxZÞ×0:5) and generated from empirical growth (scale readings) and acoustic telemetry data (N=86; Hawley et al., 2024a Table 1). Fish weight (WtSW) of the simulated sample was estimated from

empirical log-transformed length–weight relationships of sea trout captured in Sognefjorden during the NALO (years 2013–2015; Appendix S1: Table S2 and 2018–2021; Heuch et al., 2005; Nilsen, Serra-Llinares, Ambjørndalen, Berg, Lehmann, Astrid, Finstad, et al., 2021; Nilsen, Serra-Llinares, Ambjørndalen, Berg, Lehmann, Astrid, Uglem, et al., 2021; Nilsen, Serra-Llinares, Berg, Lehmann, Astrid, et al., 2021b; Nilsen, Serra-Llinares, Berg, Lehmann, Finstad, et al., 2021a), with separate regressions run for smolts (WtSW ¼ e3:05× lnTLSW−4:91, TLSW: 10.3–38.8, N= 1269) and veteran migrants (WtSW ¼e3:27 × lnTLSW−5:42, TLSW: 26.1–60.0, N=317). Simulated individuals with a maximum TLSW >90cm (N =89) were filtered from the dataset, as no reliable length–weight relationship could be determined for these fish. Veteran migrants with a tagging length of <22 cm (N =96), and smolts with a tagging length of >22 cm (N =1008), were excluded from further analysis as fish of these size ranges were not present in the empirical data (Hawley et al., 2024a, 2024b).

###### Modeled salmon lice exposure, infection rate, and survival

To estimate salmon lice density in the environment (SLenv, in number of salmon lice per square kilometer), we utilized two openly available models of salmon lice distribution. The first is produced by the Norwegian Institute of Marine Research (IMR; Myksvoll et al., 2018; Sandvik et al., 2016; Sandvik, Ådlandsvik, et al., 2020; Sandvik, Johnsen, et al., 2020) and models sea lice distribution over a 6-month period (WoY: 14–35); the second covers a full 12 months and is supplied by the Norwegian Veterinary Institute (NVI; Kristoffersen et al., 2014, 2017; Stige et al., 2021). Both models estimate the spatial

21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

(IMR: 800 × 800m grid, NVI: 100 ×100 m grid) and temporal (weekly) distributions of infective salmon lice larvae, with input data derived from weekly monitoring of temperature and salmon lice counts from all salmonid farms in Norway, as well as hydrodynamic modeling of Norwegian coastal waters. From these models, the weekly median value of predicted SLenv was extracted using the terra package (Hijmans, 2023) in R, within each fjord zone of Sognefjorden, with distinct values generated for each arm of the inner fjord. Individual accumulated salmon lice exposure was then estimated from the total weekly SLenv for each simulated migration pathway (ΣSLenvt) of sea trout. To estimate weekly exposure of smolts to salmon lice, the SLenvIMR model was applied for the period 31 March to 25 August (WoY: 14–35), and the SLenvNVI model for the period 24 March to 29 September (WoY: 13–40). For veteran migrants, weekly salmon lice exposure was estimated over an annual 12-month period using the SLenvNVI model.

Conversion of SLenv to infestation levels of salmon lice on Sognefjorden sea trout (SLinf , in number of salmon lice per week) was estimated according to published approaches utilizing the two different models of SLenv. The IMR method uses a zero-altered gamma model to relate observed salmon lice infestations on sea trout (NALO data) to SLenvIMR, water salinity, and current speed (Bøhn, Nilsen, Gjelland, Biuw, Sandvik, Primicerio, Karlsen, & Serra-Llinares, 2022). To apply this model to Sognefjorden, we extracted weekly median values of water salinity and current speed within each fjord zone in the upper 2m of the water column, from the open-source NorKyst800 model (Norwegian Meteorological Institute, Asplin et al., 2020), according to Bøhn, Nilsen, Gjelland, Biuw, Sandvik, Primicerio, Karlsen, and Serra-Llinares (2022). We then assigned a weekly presence/absence of SLinf in each fjord zone, according to the model input values extracted and by use of the rbinom function in R and the parameter values of the Bernoulli model stated in Bøhn, Nilsen, Gjelland, Biuw, Sandvik, Primicerio, Karlsen, and Serra-Llinares (2022). If the model assigned a presence of salmon lice, the Gamma model parameters (according to Bøhn, Nilsen, Gjelland, Biuw, Sandvik, Primicerio, Karlsen, & Serra-Llinares, 2022; Bøhn, Nilsen, Gjelland, Biuw, Sandvik, Primicerio, Karlsen, Serra-Llinares, Sandvik,

- et al., 2022) were used to predict weekly rates of SLinf within each fjord zone. The NVI approach utilizes a negative binomial regression model to estimate salmon lice counts on Atlantic salmon post-smolts caught at sea


(NALO data) as a function of SLenvNVI (Stige et al., 2022). We then applied this model to estimate annual weekly values of SLinf within each zone of Sognefjorden according to: SLinf ¼ð0:0041 ×ððeSLenvNVI −1Þ0:425Þ×

lnð7ÞÞ (Stige et al., 2022). Individual accumulated salmon lice infestation was estimated from the total weekly SLinf for each simulated migration pathway (ΣSLinft) of smolt and veteran migrant sea trout.

Individual probability of direct mortality due to critical levels of salmon lice infestation (pðZSLÞ) was modeled according to the salmon lice tolerance limits defined by Taranger et al. (2015), who classified the risk of mortality for two size groups of salmonids (<150 and ≥150 g) at different threshold levels of salmon lice infestation (three levels for <150 g fish, and four levels for fish ≥150 g), specified as the number of salmon lice per gram host body mass (Appendix S1: Figure S1). We subsequently applied these two threshold groupings to Sognefjorden smolts and veteran migrants, respectively, and individual pðZSLÞ was assigned according to the stipulated salmon lice tolerance of ΣSLinft/WtSW. We then predicted individual survival (SSL) by drawing a fate of either survival or death using the rbinom function in R (rbinomð1− pðZSLÞÞ). These values were subsequently compared to absolute simulated survival (STotal) to estimate the fraction of total mortality attributable to infective salmon lice accumulated during sea-sojourn ðZSL ¼ ð1−SSLÞ=ð1−STotalÞÞ, for simulated sea trout smolts (IMR and NVI models) and veteran migrants (NVI model) of Sognefjorden.

###### RESULTS

The highest levels of SLenv and SLinf were seen in the outer fjord region of Sognefjorden (Figure 3; Appendix S1: Table S3), corresponding to the region where most aquaculture facilities are located (Figure 1). Mean values of SLenv for the inner, mid, and outer fjord were estimated as 708, 18,402, and 290,834 and 195, 518, and 1128 salmon lice km−2 for IMR and NVI models, respectively (for the overlapping period WoY: 14–35). This translated to a mean SLinf of 0.02, 0.07, 1.50 and 0.02, 0.12, 1.70 salmon lice week−1 in the inner, mid, and outer fjord for IMR and NVI models, respectively (for the period WoY: 14–35) (Appendix S1: Table S3). Variation among years was modeled with mean values of SLenvIMR estimated as 48,855, 159,068 and 102,021 salmon lice km−2 during 2013, 2014, and 2015, resulting in a mean infection rate (SLinf IMR) of 0.30, 0.95, and 0.34 salmon lice week−1 during the respective years. The SLenvNVI model produced mean estimates of 483, 662, and 697 salmon lice km−2, which resulted in a mean infection rate (SLinf NVI) of 0.42, 0.87, and 0.55 salmon lice week−1 during 2013, 2014, and 2015, respectively (WoY: 14–35). Maximum IMR-derived values of SLenv and SLinf were estimated in

21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

![image 42](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile42.png>)

- F I G U R E 3 Median weekly salmon lice (SL) density (SLenv, in number of salmon lice per square kilometer) and infection rate (SLinf , in number of salmon lice per week) for each sampled year and fjord zone of Sognefjorden. Values were derived from two models of SLenv and SLinf provided by (a, b) the Institute of Marine Research (IMR) and (c, d) the Norwegian Veterinary Institute (NVI), where the latter provides annual estimates, while the former encompasses a 6-month period (gray shaded region on panels (c) and (d): week of year 14–35). Distinct values of salmon lice density and transmission were generated for each fjord arm of the inner-fjord (distinguished by orange line type).


the outer fjord in WoY 34 during 2013 (626, 572, 4.49) and 2014 (1065, 158, 12.74), and WoY 23 (646, 866, 2.86) in 2015. The NVI model predicted maximum values of

SLenv and SLinf in WoY 41 (1469, 4.13), 36 (1568, 6.29), and 45 (1384, 2.89) during 2013, 2014, and 2015, respectively.

21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

Individually accumulated salmon lice exposure (ΣSLenvt) and infection frequency (ΣSLinft) were greatest for veteran migrant sea trout that reached the outer fjord, with mean values of ΣSLenvt estimated as 9889, 14476, and 14264 and mean values of ΣSLinft estimated as 10.62, 20.72, and 14.45 during the years 2013, 2014, and 2015, respectively (Appendix S1: Table S4). However, these values translated to low numbers of salmon lice per gram host body mass (0.002, 0.003, 0.002), due to the larger WtSW of the veteran migrants (mean: 2108 g, range: 224–10792g; Table 1). For smolts reaching the outer fjord, mean values of salmon lice per gram host body mass were estimated as 0.01, 0.03, 0.02 and 0.01, 0.04, 0.03 during the years 2013, 2014, and 2015 for the IMR and NVI models, respectively (Appendix S1: Table S4). Variation among populations in the mean values of salmon lice exposure (ΣSLenvt) and infection frequency (ΣSLinft) was also estimated, with highest values estimated for Fortun veteran migrants (8785, 8.9) and lowest for Lærdal (5623, 4.6) (mean values across years) (Figure 4). In smolts, the two populations that reached the outer fjord were most exposed to salmon lice, with mean values of ΣSLinft for Lærdal smolts estimated as 570460 and 5128 and Årdal smolts estimated as 724869 and 6756 for IMR and NVI models, respectively. This corresponds to a mean ΣSLinft of 2.23 and 2.87 for Lærdal smolts and 2.87 and 3.81 for Årdal smolts (IMR and NVI models, respectively), with these values equating to 0.00–0.02 salmon lice g−1 (Figure 5).

Estimates of sea trout survival that correspond to individual mortality from critical levels of salmon lice infestation (SSL) revealed limited variation among years. Mean values of SSL ranged from 0.951 (2014) to 0.969 (2013) for veteran migrants and 0.927 (2014) to 0.936

- (2013) and 0.925 (2014) to 0.938 (2013) for smolts, me IMR and NVI models, respectively. Disparity was however observed among populations, with mean annual


values of SSL ranging from 0.934 (Fortun) to 0.974 (Lærdal) in veteran migrants (Figure 6, Table 2). For smolts, mean values ranged from 0.881 and 0.873 (Årdal) to 0.979 and 0.984 (Mørkrid) according to IMR and NVI estimates, respectively (Figure 6, Table 3). Greatest variation in SSL was dependent upon individual maximum seaward migration distance, with those individuals reaching the outer fjord having lower estimates of SSL than those individuals migrating no further than the inner and mid fjord regions. In veteran migrants, mean annual values of SSL were 0.975, 0.964, and 0.952 for sea trout reaching the inner, mid, and outer fjord, respectively (Figure 6, Table 2). For smolts, SSL was estimated

- as 0.944 and 0.945 for individuals remaining in the inner fjord, 0.932 and 0.934 for smolts reaching the mid fjord, and reduced to 0.907 and 0.895 for smolts reaching the


outer fjord (IMR and NVI models, respectively, Figure 6, Table 3).

When these estimates were compared with simulated absolute survival estimates (STotal), the fraction of total mortality attributable to salmon lice during sea-sojourn (ZSL) was estimated as 10.4% for veteran migrant sea trout and 15.7% (NVI model) and 17.3% (IMR model) for smolts (mean values across years and populations). Considerable variation in ZSL was estimated for both smolts (Table 3) and veteran migrants (Table 2), resulting from the sizeable variation in both STotal and SSL at the population level, but also due to individual migratory extent (Figure 6, Tables 2 and 3). A difference of 40.2 percentage points in the fraction of residual mortality attributed to salmon lice was estimated among populations of Sognefjorden smolts. In Aurland smolts, mean ZSL was estimated as 23.0% and 20.0%, Lærdal smolts 8.4% and 8.8%, Årdal smolts 43.8% and 34.6%, Fortun smolts 22.3% and 19.2%, and Mørkrid smolts 3.6% and 3.0% (mean values IMR models and NVI models, respectively). For individual smolts remaining in the inner fjord, mean ZSL was estimated as 15.8% and 13.7%, with little difference for smolts reaching the mid fjord, 15.5% and 13.7%. These values increased by 10 percentage points for smolts reaching the outer fjord, 24.9% and 23.8% (IMR and NVI models, respectively). Among veteran migrants, difference in annual ZSL was estimated between migrants reaching the mid fjord (8.9%) and outer fjord (14.8%) (mean values across populations and years). However, a difference of 56.2 percentage points in annual ZSL was estimated among the veteran migrant populations. Estimates of mean annual ZSL were 7.0%, 3.0%, 15.3%, and 59.2% for veteran migrants from Aurland, Lærdal, Årdal, and Fortun, respectively.

###### DISCUSSION

The use of simulated trajectories of anadromy and survival combined with modeled salmon lice abundance and infection rates provides a unique contribution to our knowledge of sea trout behavior and the impacts of salmon lice in a natural setting. Our findings reveal that individual traits of anadromous behavior influence potential exposure to salmon lice within the fjord, with salmon lice infestation highest for those individuals and populations utilizing the outer fjord region, in closest proximity to aquaculture facilities. Despite limited probability of individual mortality from critical levels of salmon lice infestation, salmon lice contributed toward reduced survival for both smolts and veteran migrants, with individual salmon

21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

lice exposure a greater contributor toward mortality risk than annual variation in salmon lice distribution within the fjord. Thus, individual timing, duration and

seaward extent of migratory behavior largely accounts for the consequences of salmon lice on sea trout in Sognefjorden.

![image 43](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile43.png>)

- F I G U R E 4 Legend on next page.


21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

###### Spatial-temporal distribution of salmon lice

Our investigation makes use of two openly available models to estimate the spatial-temporal distribution of salmon lice within Sognefjorden. Both models described a spatial gradient of salmon lice, with highest salmon lice concentrations (SLenv) in the outer fjord that decreased toward the inner fjord (Figure 3; Appendix S1: Table S3). This was reflected in the salmon lice infection rates (SLinf ) with high levels occurring in the outer fjord and limited transmission of salmon lice occurring in the mid and inner fjord (Figure 3;

- Appendix S1: Table S3). This gradient was anticipated, with the protection provided by the designation as a National Salmon Fjord; the inner and mid fjord regions are subjected to lower numbers of salmon lice spillover from farmed sources that are restricted to the outer fjord and coastline (Figure 1). In their evaluation of the Norwegian National Salmon Fjords, Serra-Llinares et al.


- (2014) state that larger protected areas (e.g., Sognefjorden) are granted protection from salmon lice dispersed from aquaculture when farms are located at a minimum distance of 30km. Due to the sheer extent and semi-enclosed nature of Sognefjorden, this “buffer zone” corresponds to a distance reaching ca. halfway into the mid fjord zone, with the inner fjord being completely protected from the nearest located aquaculture facility. Salmon lice-distribution models have demonstrated that salmon lice may be transported up to 200km over a 10-day period, but that most transportation is restricted to a 20- to 30-km radius from a source (Asplin et al., 2020; Serra-Llinares et al., 2014). Estimated salmon lice density did fluctuate week to week within the inner fjord region (i.e., at a radius of >30km); however, these densities translated to very low levels of salmon lice infestation (Figure 3; Appendix S1: Table S3). Considerable annual variation in the density and infestation rate of salmon lice was also generated by the models, with highest levels estimated during 2014. This reflects reported salmon lice numbers by local aquaculture facilities, with mean values of total salmon lice per farmed fish 60% higher during 2014 than during 2013 (Appendix S1: Table S1), a


consequence of higher biomass densities and warmer water temperatures (reported by the Directorate of Fisheries).

Both models of salmon lice distribution (i.e., produced by IMR and NVI) are central reference tools for the Norwegian regulatory framework for aquaculture. Although we did not aim to evaluate and compare the two models directly within the scope of this study, we chose to apply and present the findings from both models, thus providing a form of control or sensitivity in our estimates. When comparing the overlapping period addressed by both models (WoY 14–35), similar weekly values of salmon lice infestation were estimated, despite estimated values of salmon lice density in the outer fjord zone being considerably higher in the IMR model. This highlights that although these state-of-the-art models provide valuable tools for monitoring and risk assessment, model products are reliant on calibration data, which include high levels of variability (e.g., NALO monitoring data), thus considerable uncertainty in the estimates of salmon lice distribution and density remains.

Two different approaches to transform salmon lice density into the rate of salmon lice transmission onto free-swimming fish were implemented, where both are calibrated using NALO monitoring data. The method outlined by Bøhn, Nilsen, Gjelland, Biuw, Sandvik, Primicerio, Karlsen, and Serra-Llinares (2022a) is developed specifically for sea trout smolts, whereas the method generated by Stige et al. (2022) was designed to estimate salmon lice infestation onto out-migrating salmon smolts. The observational data required to calibrate these models are labor-intensive, coarse (both spatially and temporally), and typically noisy. Natural variability in the population dynamics of salmon lice and fish-hosts generates patchy distributions of salmon lice and individual heterogeneity in lice infestation. Thus, observed salmon lice infestations are often typically over-dispersed and exhibit an excess of zeros (as illustrated in the NALO data; Appendix S1: Table S2), this therefore imposes statistical limitations to methods that can cope with such distributions (Helland et al., 2015). Accordingly, the development of methods and models to predict transmission of salmon lice in the

- F I G U R E 4 Individual accumulated salmon lice (SL) (a) exposure (ΣSLenvt), (b) infection (ΣSLinft), and (c) degree of infestation (ΣSLinft/ WtSW) resulting from the simulated annual migration trajectories of 3815 simulated individuals from four populations of veteran migrant sea trout from Sognefjorden. Mean individual values are grouped by maximum seaward extent of migration (inner, mid, and outer fjord),


population, and colored by year. To estimate weekly exposure and infection of veteran migrants to salmon lice, the SLenvNVI model was applied over an annual period. Box plots present mean individual values across 100 simulated iterations of migration trajectories, where midlines represent the median value, box limits represent the interquartile range (IQR). The upper and lower whisker extends from the box limits to the largest and lowest value no further than 1.5 * IQR from the respective box limits. Outliers, if present, are plotted as individual points, representing values beyond whisker values.

21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

environment onto wild hosts remains extremely challenging and both models applied in this study include variation and uncertainty in their estimates (Bøhn, Nilsen,

Gjelland, Biuw, Sandvik, Primicerio, Karlsen, & Serra-Llinares, 2022a; Stige et al., 2022). Nevertheless, in Sognefjorden, limited difference in the overall rates of

![image 44](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile44.png>)

- F I G U R E 5 Legend on next page.


21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

infestation was produced by the two approaches (Appendix S1: Table S3). We acknowledge that a transmission model developed for salmon smolts is far from ideal in its application to veteran migrant sea trout. However, to our knowledge, current predictors of salmon lice transmission solely apply to the smolt (predominantly salmon) stage of anadromous individuals, presumably as these smaller fish are considered more susceptible to critical levels of salmon lice infestation. Hence, the veteran migrant infestation estimates generated in this study should be cautiously considered as an initial point of reference. However, given that veteran migrant sea trout are considered especially vulnerable to salmon lice infestation as they may remain in close vicinity to aquaculture facilities for extended periods, we argue that although unrefined, this study provides an important first step of enquiry into this knowledge gap.

It is unfortunate that annual estimates were not openly accessible for both models, preventing the use of both models for veteran migrant trout. We also note that the period of overlap in the two models likely excludes the peak in salmon lice numbers with values increasing over late summer/autumn and maximum values reported by the NVI model in the weeks shortly after the IMR model terminated (Figure 3). This may lead to an underestimated effect of salmon lice on later migrating smolts and veteran migrants that have not yet returned to freshwater to overwinter/spawn, with late migrants shown to be most susceptible to detrimental consequences from salmon lice, as they exploit marine areas during this peak period of salmon lice density (Bøhn et al., 2020; Finstad et al., 2021). The sea trout migration trajectories describe a return to freshwater that was initiated in the autumn, with smolts returning earlier than veteran migrants. Peak numbers of returning smolts occurred between WoY 30–32 and between WoY 36–42 for veteran migrants, with 34% of veteran migrants returning to the fjord to overwinter (Hawley et al., 2024a). Both models therefore encompass the majority of fjord use by smolts, but the difference in estimates generated by the two models is also attributed to the additional 5-week period of simulated migration data and overall survival included in the NVI estimates for smolts.

###### Migration trajectories of sea trout

Individual accumulated salmon lice exposure (ΣSLenvt) and infection (ΣSLinft) reflected the distribution of salmon lice within Sognefjorden. As hypothesized (H1), those individuals undertaking long-distance migrations into the more densely infested outer fjord accumulated the greatest number of salmon lice during sea-sojourn (Figures 4 and 5; Appendix S1: Table S4). NALO monitoring of salmon lice counts on sampled sea trout corroborate this pattern, with free swimming sea trout sampled in the outer fjord infested with higher numbers of salmon lice (mean, range:12, 0–334) than fish caught in the mid fjord (5, 0–107; Appendix S1: Table S2). The salmon lice count data correspond to the estimated values of accumulated salmon lice infestation for veteran migrant individuals reaching the outer fjord, but are higher for both life-stages of sea trout reaching the mid fjord. Mean accumulated infestation was simulated as 15 (4–30) and 1 (0–1) salmon lice for veteran migrants and 5 (1–10) and 1 (0–1) salmon lice for smolts reaching the outer and mid fjord, respectively. Given mean rates of salmon lice infestation (IMR: 1.5, NVI: 1.7 salmon lice week−1), sea trout would have to reside in the outer fjord for 7–8 weeks to become infested with 12 salmon lice and 42–71 weeks in the mid fjord to become infested with five salmon lice (IMR: 0.07, NVI: 0.12 salmon lice week−1). We observe that the monitoring data collected from the mid fjord during 2013 reflect our simulated values (0, 0–1 salmon lice), with these samples collected closer to the inner fjord and 35 km from the nearest aquaculture facility (Figure 1; Appendix S1: Table S2). In contrast, 2014 sampling was conducted closer to the outer fjord, 24 km from the nearest farmed source, and therefore, a higher salmon lice infection rate is expected at this location. Annual variation in count data is also anticipated, with both NALO counts and modeled densities of salmon lice highest during 2014, and no comparative NALO monitoring data collected from the mid fjord during 2015. However, rather than annual variation in widespread salmon lice levels, the spatial distribution of salmon lice largely dictated individual levels of accumulated infestation. Therefore, a comparison with 2013 NALO count

- F I G U R E 5 Individual accumulated salmon lice (SL) (a) exposure (ΣSLenvt), (b) infection (ΣSLinft), and (c) degree of infestation (ΣSLinft/ WtSW) resulting from the simulated migration trajectories of 4234 simulated individuals from five populations of Sognefjorden sea trout smolts. Mean individual values are grouped by maximum seaward extent of migration (inner, mid, and outer fjord), natal population, and colored by year. Values of modeled salmon lice exposure and transmission are provided by the Institute of Marine Research (IMR) and the Norwegian Veterinary Institute (NVI). To estimate weekly exposure and infection of smolts to salmon lice, the SLenvIMR model was applied for the period week of year (WoY): 14–35 and the SLenvNVI model for the period WoY: 13–40. Box plots present mean individual values across 100 simulated iterations of migration trajectories, where midlines represent the median value, box limits represent the interquartile range (IQR). The upper and lower whisker extends from the box limits to the largest and lowest value no further than 1.5 * IQR from the respective box limits. Outliers, if present, are plotted as individual points, representing values beyond whisker values.


21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

![image 45](<Hawley et al_2024_Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout_images/imageFile45.png>)

- F I G U R E 6 Estimated survival dependent upon individual maximum seaward migration extent (inner, mid, and outer fjord) and river of origin for Sognefjorden sea trout (a) smolts and (b) veteran migrants. Green boxplots denote mean total simulated survival STotal; purple boxplots denote mean survival rate when mortality is exclusively attributed to salmon lice infection SSL. To estimate weekly exposure of smolts to salmon lice, the SLenvIMR model was applied for the period week of year (WoY): 14–35 and the SLenvNVI model for the period WoY: 13–40. For veteran migrants, weekly salmon lice exposure was estimated over an annual 12-month period using the SLenvNVI model. Box plots present mean individual values across 100 simulated iterations of migration trajectories, where midlines represent the median value, box limits represent the interquartile range (IQR). The upper and lower whisker extends from the box limits to the largest and lowest value no further than 1.5 * IQR from the respective box limits. Outliers, if present, are plotted as individual points, representing values beyond whisker values. IMR, Institute of Marine Research; NVI, Norwegian Veterinary Institute.


21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

data is a reasonable validation of our methodology, with the monitoring data reflecting the spatial gradient of salmon lice distribution throughout the fjord.

data from which movement and survival probabilities were modeled (Hawley et al., 2024a). Thus, the values of accumulated salmon lice infestation are limited due to the coarse horizontal resolution of the simulated data. Despite the comprehensive study design, the empirical fish-tracking data generated by Hawley et al. (2024a) were weakened by low N values, particularly within the outer fjord region. Although typical for this type of data collection, this generated uncertainty in the migration behavior models and mark–recapture models on which the simulated trajectories were built. Notwithstanding these limitations, we outline a novel and applicable method for generating individual estimates of salmon lice infestation, for a species typified by its plasticity in migratory behavior and threatened by increasing exposure to anthropogenic-induced alterations and pressure (Fiske et al., 2024; Thorstad et al., 2016). Although the results presented here comprise a single fjord system, this methodology could be applied to any system where sufficient empirical tracking data are available. We also reiterate the importance of monitoring data, and their necessity for the development and calibration of risk assessment tools.

Ideally, sea trout migration trajectories would match the spatial resolution of the salmon lice models; however, the simulations are constrained by the empirical tracking

- T A B L E 2 Mean rates of individual survival due to salmon lice

infestation (SSL) and absolute simulated survival (STotal) of veteran migrant sea trout during sea-sojourn in Sognefjorden, given maximum seaward migration distance (as fjord zone: inner/mid/ outer) and river of origin.

Fjord zone Population STotal SSL (NVI) ZSL (%) (NVI)

Inner Lærdal 0.56 0.99 1.7 Mid Aurland 0.79 0.99 6.9

Lærdal 0.73 0.99 3.7 Årdal 0.89 0.98 15.0 Fortun 0.94 0.98 29.8

Outer Aurland 0.71 0.98 7.0 Lærdal 0.54 0.98 3.8 Årdal 0.83 0.97 15.5 Fortun 0.88 0.91 73.0

Note: The fraction of total mortality (ZSL) attributable to SSL is given as a percentage. Under the current traffic light system (Taranger et al., 2015), estimates of SSL would be placed in the “green zone.” Estimates were generated from the NVI model of salmon lice density and infestation over an annual period. The table presents mean values for data encompassing the years 2013–2015. Estimates of ZSL are calculated according to ð1−SSLÞ=ð1−STotalÞ× 100. Abbreviation: NVI, Norwegian Veterinary Institute.

- T A B L E 3 Mean rates of individual survival due to salmon lice infestation (SSL) and absolute simulated survival (STotal) of sea trout smolts during sea-sojourn in Sognefjorden, given maximum seaward migration distance (as fjord zone: inner/mid/outer) and river of origin, for two models of salmon lice density and infestation (provided by the Institute of Marine Research [IMR] and the Norwegian Veterinary Institute [NVI]).


###### Critical mortality from salmon lice infestation

Our simulations estimated accumulated salmon lice infestation to be largely below critical mortality thresholds (ΣSLinft/WtSW) for both smolts and veteran migrants, even among those individuals reaching the outer fjord

Fjord zone Population STotal (IMR) STotal (NVI) SSL (IMR) SSL (NVI) ZSL (%) (IMR) ZSL (%) (NVI)

Inner Aurland 0.48 0.41 0.89 0.89 20.8 18.2 Fortun 0.82 0.80 0.95 0.95 28.1 22.6 Mørkrid 0.63 0.60 0.99 0.99 2.8 2.5

Mid Aurland 0.54 0.46 0.88 0.88 25.4 21.9 Lærdal 0.54 0.52 0.97 0.97 6.8 6.5 Årdal 0.73 0.64 0.90 0.90 38.3 28.3 Fortun 0.70 0.68 0.94 0.95 18.8 17.0 Mørkrid 0.34 0.30 0.97 0.98 4.1 3.3

Outer Lærdal 0.55 0.51 0.95 0.95 10.1 11.1 Årdal 0.72 0.64 0.86 0.85 49.2 40.8

Note: The fraction of total mortality (ZSL) attributable to SSL is given as a percentage. Under the current traffic light system (Taranger et al., 2015), estimates of SSL (both IMR and NVI) would be placed in the “yellow zone” for the populations of Aurland and Årdal and the “green zone” for the remaining populations. The simulated period for IMR estimates =week of year (WoY) 14–35, NVI: WoY 13–40. The table presents mean values for data encompassing the years 2013–2015. Estimates of ZSL are calculated according to ð1−SSLÞ=ð1−STotalÞ×100.

21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

(Figures 4 and 5; Appendix S1: Table S4). Therefore, simulated salmon lice infestation levels were largely below those expected to induce individual mortality (H2). An index of critical limits based on the impact of salmon lice on salmonid smolts, according to the number of salmon lice per weight of host body mass, was developed by Taranger et al. (2015). These mortality thresholds, although widely applied, are generated according to lab-based observations that are unlikely to represent the variable mortality rates occurring among wild fish in natural settings, with this index highly sensitive to the weight of an individual fish. Given the importance of fish weight in determining individual mortality thresholds from salmon lice infestation, we propose that future simulations investigate the role of among-individual variation to overall mortality rates for a given fish weight. This would generate a form of sensitivity analysis in this widely applied mortality index.

According to this index, smaller lightweight fish, as sampled during NALO monitoring (mean: 185 g), are more likely to reach the critical levels of infestation resulting in mortality, with this reflected in our simulations. We observed that when sea trout survival was attributed to critical thresholds of salmon lice exposure (SSL), mean survival rates were estimated as 0.93 and 0.96 for smolts and veteran migrants, respectively, despite limited use of densely salmon lice infested fjord areas by lighter weighted smolts (mean sea weight: 138g). The Norwegian regulatory framework for aquaculture production, the so-called “traffic light system,” determines whether production within a geographical zone can be increased, maintained at current levels or reduced, where the expected degree of salmon lice-induced mortality of salmon smolts corresponds to <10% (green), 10%–30% (yellow), and >30% (red), respectively (Taranger et al., 2015). Expanding this framework to sea trout, the fraction of individual mortality resulting from salmon lice infestation (i.e., 1−SSL) is in the “yellow” zone for the smolt populations of Aurland and Årdal (12% mean mortality) and the “green” zone for the remaining smolt populations and all veteran migrant populations sampled (Tables 2 and 3). In Sognefjorden, the mean sea weight of a tagged veteran migrant was

- 2.1 kg, which would need to be infested with 21 salmon lice for us to estimate a 20% probability of individual mortality using the current index. Although this degree of salmon lice infestation (and higher) was simulated

(maximum ΣSLinft=62 lice, 0.007lice g−1) and recorded during NALO monitoring (maximum values= 332 lice,

- 3.1 liceg−1; Appendix S1: Table S2), the simulated mean value of accumulated salmon lice infestation on veteran migrants was considerably lower (2 lice, 0.001lice g−1;


- Appendix S1: Table S4). We suggest that a more sensitive stress-response threshold could be an informative


indicator (Fjelldal et al., 2020), particularly for larger veteran migrant sea trout that are largely ignored when addressing the impacts of salmon lice, with most research focused solely on smolts.

###### Contribution of salmon lice to total mortality during sea-sojourn

Despite salmon lice infestation estimates largely below the critical probability levels expected to induce individual mortality, we observed that salmon lice contributed toward reduced total survival for sea trout populations in Sognefjorden (H3) (Figure 6, Tables 2 and 3). In both smolts and veteran migrants, the fraction of total mortality attributable to salmon lice (ZSL) was greater for long-distance migrants (smolts: 25.3, veteran migrants: 14.8%) than for those remaining within the inner fjord (smolts: 14.7, veteran migrants: 1.7%). Among populations, the contribution of salmon lice to total mortality during sea-sojourn ranged from 3.3% to 38.5% for smolts and between 3.0% and 59.2% for veteran migrants (Tables 2 and 3). Thus, our simulations revealed that the consequences of salmon lice reflect individual migratory behavior and survival at different life-stages. This generates an unequal mortality cost due to salmon lice among populations, despite widespread salmon lice densities within the fjord being equal (or close to) for all populations.

In sea trout, the degree of anadromy varies among populations and individuals, with veteran migrants undertaking more extensive migrations, in both distance and duration, than smolts (Eldøy et al., 2021; Hawley et al., 2024a, Thorstad et al., 2016). Veteran migrants are more mobile, and presumably able to actively avoid or seek out refuge from salmon lice more easily than smolts, due to their larger body size and superior swimming ability (Kennedy et al., 2022). Among individuals, larger sea trout are often observed to migrate further than smaller individuals (Eldøy et al., 2021; Flaten et al., 2016; Jensen et al., 2022), and larger smolts often migrate to sea before smaller smolts, with size of smolts decreasing throughout the spring/summer (Bohlin et al., 1993; Jensen et al., 2012, 2022). In addition to size, migratory behavior may also be condition-dependent, with individuals in low body condition tending to migrate further than sea trout in better body condition (Bordeleau et al., 2018; Davidsen et al., 2014; Eldøy et al., 2015, 2021). It has also been observed that sea survival differs between sexes, suggesting that the two sexes have differential behavior and (or) habitat use at sea (Bordeleau et al., 2018; Haraldstad et al., 2018). Accordingly, multiple physiological factors not only contribute toward migratory behavior and the resulting potential for infestation by salmon lice

21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

but also affect the consequences, both absolute as mortality and/or inconclusively as sublethal effects and altered behavior. It has therefore been suggested that the currently applied sized-based mortality index (Taranger et al., 2015) is not wholly applicable to facultative anadromous salmonids, where the consequences of salmon lice are often less absolute than mortality (Bøhn, Nilsen, Gjelland, Biuw, Sandvik, Primicerio, Karlsen, & Serra-Llinares, 2022; Finstad et al., 2021; Strøm et al., 2022). An alternative indicator has therefore been proposed, that instead quantifies change in “marine living area” and “marine feeding time” for sea trout, according to modeled densities of salmon lice encountered during anadromy (Finstad et al., 2021). This method shows promise, particularly in its application for the inclusion of sea trout into the Norwegian regulatory framework for aquaculture production (Bøhn, Nilsen, Gjelland, Biuw, Sandvik, Primicerio, Karlsen, & Serra-Llinares, 2022). These indicators were however unapplicable to Sognefjorden, where the minimum threshold (SLinf = 6 salmon lice week−1) for quantifying change in “marine living area” and “marine feeding time” was only exceeded during 4 weeks in 2014 (WoY: 31, 34–36) in the outer fjord zone. The use of simulated sea trout migration trajectories is an alternative approach, both as a method for estimating individual levels of salmon lice infestation and as a means for estimating the contribution of salmon lice to absolute mortality rates. When relying solely on empirical tracking data, the behavioral observations are inherently derived from the surviving individuals that return to freshwater; thus, the full duration and extent of marine use for lost individuals remain unknown. Simulated trajectories, generated from spatial-temporal fjord-use models that are fitted to empirical tracking data, consist of both those individuals that return to freshwater (or remain in the fjord) and also those that die while at sea. The combination of empirical and simulated approaches can generate data at an individual level yet produce sufficient data to make generalized assumptions

- at a population level. It is therefore a superior tool to approaches based on solely empirical or modeled data, in this context. If we had limited our investigation to modeled estimates of critical salmon lice infection that predict the probability of individual mortality, the total contribution of salmon lice-induced mortality for Sognefjorden sea trout populations would have been overlooked.


###### Salmon lice and altered expression of anadromy

In salmonids, growth is an important contributor to reproductive success, particularly in females, with the number

of eggs increasing with body size (L’Abée-Lund & Hindar, 1990). Previous studies have observed a reduction in sea trout growth when comparing the periods before and after introduction of intensive salmon-farming activity in nearby areas (Eldøy et al., 2020; Fjørtoft et al., 2014). In Sognefjorden, a trend for superior growth rate in sea trout reaching the mid and outer fjord regions has been observed (Hawley et al., 2024a), presumably reflecting a gradient in the quantity and quality of feeding opportunities (Eldøy et al., 2015; Rikardsen & Amundsen, 2005). Sognefjorden, the world’s longest fjord system that supports populations of sea trout, presents a unique opportunity to study the expression of anadromy, where during a 60-year period, the seaward extent of migration distance has decreased, with sea trout now predominately remaining in the inner and mid fjord areas (Hawley et al., 2024a). Findings from this study suggest that this reduction in migratory extent may result from salmon lice avoidance, with sea trout actively selecting for areas of low salmon lice density, and in turn avoiding direct mortality from salmon lice. Similar observations of salmon lice avoidance in facultatively anadromous salmonids have been recorded in field-based experimental settings, with the potential for reduction or loss of anadromy implied (Halttunen, Gjelland, Hamel, et al., 2018; Serra-Llinares et al., 2020; Strøm et al., 2022). An informative experiment would be to observe whether historical patterns of anadromy returned upon removal of salmon lice and if so, over what timeframe. However, we emphasize that aquaculture is just one of numerous recent anthropogenic alterations in the river-to-fjord environment of Sognefjorden (Fiske et al., 2024); thus, we are unable to isolate the effects of salmon lice during this 60-year period. This is reiterated in the simulated estimates of absolute survival, with salmon lice a relatively minor contribution to overall mortality of sea trout in this system. However, reduced growth and increased mortality likely result in negative demographic consequences for the total sea trout population, given that fecundity, offspring growth, and viability are improved with larger and older parents (Gauthey, 2017; Kamler, 2005; L’Abée-Lund & Hindar, 1990).

###### CONCLUSION

We present a novel method for assessing the impact of salmon lice on the facultatively anadromous brown trout. Results show that Sognefjorden sea trout predominately avoid areas of high salmon lice densities, resulting in levels of salmon lice infestation largely below critical thresholds likely to induce individual mortality. However, the consequences of salmon lice are not equally distributed among populations and life-stages, despite the distribution of lice

21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

exposure within the fjord being equal for all populations. Instead, salmon lice infestation largely resulted from the migration extent of individual sea trout, and therefore, generalized models of salmon lice risk assessment for facultative anadromous salmonids should be used with caution. However, we reiterate the need for inclusion of sea trout into management strategies, with the estimated contribution of salmon lice to the total mortality of sea trout being considerable in this fjord system, despite designated protection from aquaculture. Although we stress that aquaculture is just one of multiple anthropogenic-induced stressors, our findings suggest that Sognefjorden sea trout have altered their anadromous behavior to avoid critical levels of salmon lice infestation and predominantly remain in the mid and inner fjord regions, where salmon lice infestation rates were lowest. Ultimately, this may result in negative demographic consequences for the brown trout populations of Sognefjorden and highlights the importance of decisive management actions for the preservation of anadromy.

AUTHOR CONTRIBUTIONS

K. L. Hawley, H. A. Urke, T. Kristensen, and T. O. Haugen designed the sampling and the idea for the manuscript. K. L. Hawley and T. O. Haugen analyzed and interpreted the data. K. L. Hawley led the writing of the manuscript with contribution from H. A. Urke, T. Kristensen, and T. O. Haugen. All authors approved the final version of the manuscript.

ACKNOWLEDGMENTS

The work was funded by an internal grant from the Norwegian University for Life Sciences (project number: 1302051230) and the project SalmonTracking 2030 (project number: FHF 901890). Funding was also provided by the Sogn and Fjordane County Authority, E-Co Energi AS (now named Hafslund Eco Vannkraft AS), Østfold Energi AS, Luster Municipality, Årdal Municipality, County Governor of Sogn and Fjordane, Mowi AS, Osland Havbruk AS, and Sulefisk AS, as part of the KUSTUS project. We thank Ørjan Karlsen (IMR) for providing access to NALO trawl and trap data (years 2013–2015) and Leif Christian Stige and Lars Qviller (NVI) for supplying the modeled salmon lice data. The manuscript has been much improved from comments provided by reviewers. The authors are grateful for the field assistance given by V. Moen, T. Grimelid, J. I. Øygard, R. A. Golf, R. M. Bjørum, R. Lunde, M. A. Bergan, M. Brooks, J. B. Ulvund, O. Pettersen, and O. Wendelboe among others, as well as the river owners for their contribution.

CONFLICT OF INTEREST STATEMENT The authors declare no conflicts of interest.

DATA AVAILABILITY STATEMENT Data underlying this article are available at DataverseNO (Hawley et al., 2024c): https://doi.org/10.18710/XCISVI. Additional datasets utilized for this research are as follows: Salmon lice infection rate (IMR) (Bøhn, Nilsen, Gjelland, Biuw, Sandvik, Primicerio, Karlsen, Serra-Llinares, Sandvik, et al., 2022b): https://doi.org/ 10.5061/dryad.9ghx3ffjj; Sea trout trajectories (Hawley et al., 2024b): https://doi.org/10.18710/LIYHRV; NALO monitoring 2018–2021 (The Norwegian Marine Data Centre) (Nilsen, Serra-Llinares, Ambjørndalen, Berg, Lehmann, Tonstad, Finstad, & Karlsen, 2021; Nilsen, Serra-Llinares, Ambjørndalen, Berg, Lehmann, Tonstad, Finstad, & Karlsen, 2021, Nilsen, Serra-Llinares, Berg, Lehmann, Finstad, & Karlsen, 2021; Nilsen, Serra-Llinares, Berg, Lehmann, Finstad, & Karlsen, 2021a): https://doi.org/10.21335/NMDC-616838292; https://doi.org/10.21335/NMDC-163762784; https://doi. org/10.21335/NMDC-477241498; https://ftp.nmdc.no/ nmdc/IMR/lakselus/Havforskningsinstituttet_RuseOgG arnNALO-2021.xlsx; NorKyst800 model (Norwegian Meteorological Institute): https://thredds.met.no/thredds/ catalog/sea/norkyst800mv0_24h/catalog.html; Salmon lice density IMR (The Norwegian Marine Data Centre) (Sandvik, Ådlandsvik, et al., 2020): https://doi.org/10. 21335/NMDC-410516615; Salmon lice density (NVI) (Stige et al., 2021): https://doi.org/10.3354/aei00410.

ORCID K. L. Hawley https://orcid.org/0000-0002-2981-5452

REFERENCES

Adams, C. E., L. Chavarie, J. R. Rodger, H. M. Honkanen, D. Thambithurai, and M. P. Newton. 2022. “An Opinion Piece: The Evolutionary and Ecological Consequences of Changing Selection Pressures on Marine Migration in Atlantic Salmon.” Journal of Fish Biology 100: 860–67.

Arnason, N. A. 1973. “The Estimation of Population Size, Migration Rates and Survival in a Stratified Population.” Researches on Population Ecology 15: 1–8.

Asplin, L., J. Albretsen, I. A. Johnsen, and A. D. Sandvik. 2020. “The Hydrodynamic Foundation for Salmon Lice Dispersion Modelling Along the Norwegian Coast.” Ocean Dynamics 70: 1151–67.

Birkeland, K., and P. J. Jakobsen. 1997. “Salmon Lice, Lepeophtheirus salmonis, Infestation as a Causal Agent of Premature Return to Rivers and Estuaries by Sea Trout, Salmo trutta, Juveniles.” Environmental Biology of Fishes 49: 129–137.

Birnie-Gauvin, K., E. B. Thorstad, and K. Aarestrup. 2019. “Overlooked Aspects of the Salmo salar and Salmo trutta Lifecycles.” Reviews in Fish Biology and Fisheries 29: 749–766.

Bjørn, P. A., and B. Finstad. 1998. “The Development of Salmon Lice (Lepeophtheirus salmonis) on Artificially Infected Post Smolts of Sea Trout (Salmo trutta).” Canadian Journal of Zoology 76: 970–77.

21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

Bjørn, P. A., R. Nilsen, R. M. Serra-Llinares, L. Asplin, I. A. Johnsen, Ø. Karlsen, B. Finstad, et al. 2013. “Lakselusinfeksjonen på vill laksefisk langs norskekysten i 2013. Sluttrapport til Mattilsynet.” Report from the Norwegian Institute of Marine Research: Nr 32-2013 (in Norwegian). Bohlin, T., C. Dellefors, and U. Faremo. 1993. “Timing of Sea-Run Brown Trout (Salmo trutta) Smolt Migration: Effects of Climatic Variation.” Canadian Journal of Fisheries and Aquatic Sciences 50, 1132–36.

Bøhn, T., K. Ø. Gjelland, R. M. Serra-Llinares, B. Finstad, R. Primicerio, R. Nilsen, Ø. Karlsen, et al. 2020. “Timing Is Everything: Survival of Atlantic Salmon Salmo salar Postsmolts during Events of High Salmon Lice Densities.” Journal of Applied Ecology 57: 1149–60.

Bøhn, T., R. Nilsen, K. Ø. Gjelland, M. Biuw, A. D. Sandvik, R. Primicerio, Ø. Karlsen, and R. M. Serra-Llinares. 2022a. “Salmon Louse Infestation Levels on Sea Trout Can be Predicted from a Hydrodynamic Lice Dispersal Model.” Journal of Applied Ecology 59: 704–714.

Bøhn, T., R. Nilsen, K. Ø. Gjelland, M. Biuw, A. Sandvik, R. Primicerio, Ø. Karlsen, R. Serra-Llinares, A. D. Sandvik, and R. M. Serra-Llinares. 2022b. “Salmon Louse Infestation Levels on Sea Trout Can be Predicted from a Hydrodynamic Lice Dispersal Model.” Dataset. Dryad. https://doi.org/10. 5061/dryad.9ghx3ffjj.

Bordeleau, X., J. G. Davidsen, S. H. Eldøy, A. D. Sjursen, F. G. Whoriskey, and G. T. Crossin. 2018. “Nutritional Correlates of Spatiotemporal Variations in the Marine Habitat Use of Brown Trout (Salmo trutta) Veteran Migrants.” Canadian Journal of Fisheries and Aquatic Sciences 75: 1744–54.

Bouwmeester, M. M., M. A. Goedknegt, R. Poulin, and D. W. Thieltges. 2021. “Collateral Diseases: Aquaculture Impacts on Wildlife Infections.” Journal of Applied Ecology 58: 453–464.

Boxaspen, K. 2006. “A Review of the Biology and Genetics of Sea Lice.” ICES Journal of Marine Science 63: 1304–16.

Davidsen, J. G., M. Daverdin, A. D. Sjursen, L. Rønning, J. V. Arnekleiv, and J. I. Koksvik. 2014. “Does Reduced Feeding Prior to Release Improve the Marine Migration of Hatchery Brown Trout Salmo trutta Smolts?” Journal of Fish Biology 85: 1992–2002.

del Villar-Guerra, D., K. Aarestrup, C. Skov, and A. Koed. 2014. “Marine Migrations in Anadromous Brown Trout (Salmo trutta). Fjord Residency as a Possible Alternative in the Continuum of Migration to the Open Sea.” Ecology of Freshwater Fish 23: 594–603.

Eldøy, S. H., X. Bordeleau, M. Lawrence, E. Thorstad, A. Finstad, F. Whoriskey, G. Crossin, et al. 2021. “The Effects of Nutritional State, Sex and Body Size on the Marine Migration Behaviour of Sea Trout.” Marine Ecology Progress Series 665: 185–200.

Eldøy, S. H., J. G. Davidsen, E. B. Thorstad, F. Whoriskey, K. Aarestrup, T. F. Næsje, L. Rønning, A. D. Sjursen, A. H. Rikardsen, and J. V. Arnekleiv. 2015. “Marine Migration and Habitat Use of Anadromous Brown Trout (Salmo trutta).” Canadian Journal of Fisheries and Aquatic Sciences 72: 1366–78.

Eldøy, S. H., D. Ryan, W. K. Roche, E. B. Thorstad, T. F. Næsje, A. D. Sjursen, P. G. Gargan, and J. G. Davidsen. 2020. “Changes in Growth and Migration Patterns of Sea Trout

before and after the Introduction of Atlantic Salmon Farming.” ICES Journal of Marine Science 77: 2623–34.

Elliott, J. M. 1994. Quantitative Ecology and the Brown Trout. Oxford University Press. Oxford, New York and Tokyo. 286 pp.

FAO. 2022. The State of World Fisheries and Aquaculture 2022. Towards Blue Transformation. Rome: FAO. https://doi.org/10. 4060/cc0461en.

Finstad, B., P. A. Bjørn, A. Grimnes, and N. A. Hvidsten. 2000. “Laboratory and Field Investigations of Salmon Lice [Lepeophtheirus salmonis (Krøyer)] Infestation on Atlantic Salmon (Salmo salar L.) Post-Smolts.” Aquaculture Research 31: 795–803.

Finstad, B., A. Sandvik, O. Ugedal, K. Vollset, Ø. Karlsen, J. Davidsen, H. Sægrov, and R. Lennox. 2021. “Development of a Risk Assessment for Sea Trout in Coastal Areas Exploited for Aquaculture.” Aquaculture Environment Interactions 13: 133–144.

Fiske, P., T. Forseth, E. B. Thorstad, V. Bakkestuen, S. Einum, M. Falkegård, Ø. A. Garmo, et al. 2024. “Novel Large-Scale Mapping Highlights Poor State of Sea Trout Populations.” Aquatic Conservation: Marine and Freshwater Ecosystems 2024: 1–20.

Fjelldal, P. G., T. J. Hansen, and Ø. Karlsen. 2020. “Effects of Laboratory Salmon Louse Infection on Osmoregulation, Growth and Survival in Atlantic Salmon. Conservation.” Physiology 8: coaa023.

Fjørtoft, H. B., R. Borgstrøm, and Ø. Skaala. 2014. “Differential Changes in Growth Patterns of Anadromous Brown Trout and Atlantic Salmon from the River Etneelva over a 25-Year Period.” Marine Biology Research 10: 301–7.

Flaten, A. C., J. G. Davidsen, E. B. Thorstad, F. Whoriskey, L. Rønning, A. D. Sjursen, A. H. Rikardsen, and J. V. Arnekleiv. 2016. “The First Months at Sea: Marine Migration and Habitat Use of Sea Trout Salmo trutta Post-Smolts.” Journal of Fish Biology 89: 1624–40.

Forseth, T., B. T. Barlaup, B. Finstad, P. Fiske, H. Gjøsæter, M. Falkegård, A. Hindar, T. A. Mo, A. H. Rikardsen, and E. B. Thorstad. 2017. “The Major Threats to Atlantic Salmon in Norway.” ICES Journal of Marine Science 74: 1496–1513.

Gargan, P., F. Kelly, S. Shephard, and K. Whelan. 2016. “Temporal Variation in Sea Trout Salmo trutta Life History Traits in the Erriff River, Western Ireland.” Aquaculture Environment Interactions 8: 675–689.

Gauthey, Z. 2017. “Brown Trout Spawning Habitat Selection and Its Effects on Egg Survival.” Ecology of Freshwater Fish 26: 133–140.

Halttunen, E., K.-Ø. Gjelland, K. Glover, I. Johnsen, R. M. Serra-Llinares, O. Skaala, R. Nilsen, et al. 2018. “Migration of Atlantic Salmon Post-Smolts in a Fjord with High Infestation Pressure of Salmon Lice.” Marine Ecology Progress Series 592: 243–256.

Halttunen, E., K.-Ø. Gjelland, S. Hamel, R.-M. Serra-Llinares, R. Nilsen, P. Arechavala-Lopez, J. Skarðhamar, et al. 2018. “Sea Trout Adapt their Migratory Behaviour in Response to High Salmon Lice Concentrations.” Journal of Fish Diseases 41: 953–967.

Haraldstad, T., E. Höglund, F. Kroglund, A. Lamberg, E. Olsen, and T. Haugen. 2018. “Condition-Dependent Skipped Spawning in Anadromous Brown Trout (Salmo trutta).” Canadian Journal of Fisheries and Aquatic Sciences 75: 2313–19.

21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

- Hawley, K. L., H. A. Urke, T. Kristensen, and T. O. Haugen. 2024a. “Balancing Risks and Rewards of Alternate Strategies in the Seaward Extent, Duration and Timing of Fjord Use in Contemporary Anadromy of Brown Trout (Salmo trutta).” BMC Ecology and Evolution 24: 27.
- Hawley, K. L., H. A. Urke, T. Kristensen, and T. O. Haugen. 2024b. “Replication Data for: Balancing Risks and Rewards of Alternate Strategies in the Seaward Extent, Duration and Timing of Fjord Use in Contemporary Anadromy of Brown Trout (Salmo trutta).” DataverseNO. https://doi.org/10.18710/ LIYHRV.
- Hawley, K. L., H. A. Urke, T. Kristensen, and T. O. Haugen. 2024c. “Replication Data for: Individual Patterns of Anadromy Determine the Cost of Salmon Lice Exposure in Brown Trout.” Dataset. DataverseNO. https://doi.org/10.18710/XCISVI.


Helland, I. P., I. Uglem, P. A. Jansen, O. H. Diserud, P. A. Bjørn, and B. Finstad. 2015. “Statistical and Ecological Challenges of Monitoring Parasitic Salmon Lice Infestations in Wild Salmonid Fish Stocks.” Aquaculture Environment Interactions 7: 267–280.

Heuch, P. A., P. A. Bjørn, B. Finstad, J. C. Holst, L. Asplin, and F. Nilsen. 2005. “A Review of the Norwegian ‘National Action Plan against Salmon Lice on Salmonids’: The Effect on Wild Salmonids.” Aquaculture 246: 79–92.

Hijmans, R. 2023. “terra: Spatial Data Analysis.” R Package Version 1.7-39. https://CRAN.R-project.org/package=terra.

Jansen, P. A., A. B. Kristoffersen, H. Viljugrein, D. Jimenez, M. Aldrin, and A. Stien. 2012. “Sea Lice as a Density-Dependent Constraint to Salmonid Farming.” Proceedings of the Royal Society B: Biological Sciences 279: 2330–38.

Jensen, A. J., O. H. Diserud, B. Finstad, P. Fiske, and E. B. Thorstad. 2022. “Early-Season Brown Trout (Salmo trutta) Migrants Grow and Survive Better at Sea.” Journal of Fish Biology 100: 1419–31.

Jensen, A. J., B. Finstad, P. Fiske, N. A. Hvidsten, A. H. Rikardsen, and L. Saksgård. 2012. “Timing of Smolt Migration in Sympatric Populations of Atlantic Salmon (Salmo salar), Brown Trout (Salmo trutta), and Arctic Char (Salvelinus alpinus).” Canadian Journal of Fisheries and Aquatic Sciences 69: 711–723.

Jensen, J. L. A., and A. H. Rikardsen. 2008. “Do Northern Riverine Anadromous Arctic Charr Salvelinus alpinus and Sea Trout Salmo trutta Overwinter in Estuarine and Marine Waters?” Journal of Fish Biology 73: 1810–18.

Jensen, J. L. A., and A. H. Rikardsen. 2012. “Archival Tags Reveal that Arctic Charr Salvelinus alpinus and Brown Trout Salmo trutta Can Use Estuarine and Marine Waters during Winter.” Journal of Fish Biology 81: 735–749.

Johnsen, I. A., A. Harvey, P. N. Sævik, A. D. Sandvik, O. Ugedal, B. Ådlandsvik, V. Wennevik, K. A. Glover, and Ø. Karlsen. 2021. “Salmon Lice-Induced Mortality of Atlantic Salmon during Post-Smolt Migration in Norway.” ICES Journal of Marine Science 78: 142–154.

Jonsson, B., and N. Jonsson. 2011. Ecology of Atlantic Salmon and Brown Trout. Dordrecht: Springer.

Kamler, E. 2005. “Parent–Egg–Progeny Relationships in Teleost Fishes: An Energetics Perspective.” Reviews in Fish Biology and Fisheries 15: 399–421.

Kennedy, R. J., J. Barry, W. Roche, R. Rosell, and M. Allen. 2022. “In-River Behaviour and Freshwater Return Rates of Sea Trout, Salmo trutta L., from Two Coastal River Populations.” Journal of Fish Biology 101: 1008–20.

Klemetsen, A., P. A. Amundsen, J. B. Dempson, B. Jonsson, N. Jonsson, M. F. O’Connell, and E. Mortensen. 2003. “Atlantic Salmon Salmo salar L., Brown Trout Salmo trutta L. and Arctic Charr Salvelinus alpinus (L.): A Review of Aspects of their Life Histories.” Ecology of Freshwater Fish 12: 1–59.

Kristensen, T., H. Urke, T. Haugen, A. Rustadbakken, J. A. Alfredsen, K. Alfredsen, and B. O. Rosseland. 2011. “Sea Trout (Salmo trutta) from River Lærdalselva, W Norway: A Comparison of Growth and Migratory Patterns in Older and Recent Studies.” NIVA Report: Nr. 6122 (in Norwegian).

Kristoffersen, A. B., D. Jimenez, H. Viljugrein, R. Grøntvedt, A. Stien, and P. A. Jansen. 2014. “Large Scale Modelling of Salmon Lice (Lepeophtheirus salmonis) Infection Pressure Based on Lice Monitoring Data from Norwegian Salmonid Farms.” Epidemics 9: 31–39.

Kristoffersen, A. B., L. Qviller, K. O. Helgesen, K. W. Vollset, H. Viljugrein, and P. A. Jansen. 2017. “Quantitative Risk Assessment of Salmon Louse-Induced Mortality of Seaward-Migrating Post-Smolt Atlantic Salmon.” Epidemics 23: 19–33.

Krkosek,ˇ M., C. W. Revie, P. G. Gargan, O. T. Skilbrei, B. Finstad, and C. D. Todd. 2013. “Impact of Parasites on Salmon Recruitment in the Northeast Atlantic Ocean.” Proceedings of the Royal Society B: Biological Sciences 280: 20122359.

L’Abée-Lund, J. H., and K. Hindar. 1990. “Interpopulation Variation in Reproductive Traits of Anadromous Female Brown Trout, Salmo trutta L.” Journal of Fish Biology 37: 755–763.

Lennox, R. J., K. Aarestrup, S. J. Cooke, P. D. Cowley, Z. D. Deng, A. T. Fisk, R. G. Harcourt, M. Heupel, S. G. Hinch, and K. N. Holland. 2017. “Envisioning the Future of Aquatic Animal Tracking: Technology, Science, and Application.” BioScience 67: 884–896.

Ministry of Trade, Industry and Fisheries. 2020. “Regjeringen skrur på trafikklyset [The Government turns on the traffic light], press release.” Ministry of Trade, Industry and Fisheries [WWW Document]. https://www.regjeringen.no/no/aktuelt/ regjeringen-skrur-pa-trafikklyset/id2577032/.

Moriarty, M., S. C. Ives, J. M. Murphy, and A. G. Murray. 2023. “Modelling Parasite Impacts of Aquaculture on Wild Fish: The Case of the Salmon Louse (Lepeophtheirus salmonis) on Out-Migrating Wild Atlantic Salmon (Salmo salar) Smolt.” Preventive Veterinary Medicine 214: 105888.

Myksvoll, M. S., A. D. Sandvik, J. Albretsen, L. Asplin, I. A. Johnsen, Ø. Karlsen, N. M. Kristensen, A. Melsom, J. Skardhamar, and B. Ådlandsvik. 2018. “Evaluation of a National Operational Salmon Lice Monitoring System—From Physics to Fish.” PLoS One 13: e0201338.

Nilsen, R., P. A. Bjørn, R. M. Serra-Llinares, L. Asplin, I. A. Johnsen, O. F. Skulstad, Ø. Karlsen, et al. 2014. “Lakselusinfeksjonen på vill laksefisk langs norskekysten i 2014. Sluttrapport til Mattilsynet.” Report from the Norwegian Institute of Marine Research: Nr 12-2014 (in Norwegian).

21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

Nilsen, R., P. A. Bjørn, R. M. Serra-Llinares, L. Asplin, A. D. Sandvik, I. A. Johnsen, Ø. Karlsen, et al. 2016. “Lakselusinfeksjonen på vill laksefisk langs norskekysten i 2015. En fullskala test av modellbasert varsling og tilstandsbekreftelse. Sluttrapport til Mattilsynet.” Report from the Norwegian Institute of Marine Research: Nr 2-2016 (in Norwegian).

Nilsen, R., R. M. Serra-Llinares, V. Ambjørndalen, M. Berg, G. B. Lehmann, T.A. Tonstad, B. Finstad, and Ø. Karlsen. 2021. “Havforskningsinstituttet Ruse og Garn NALO 2020.” Dataset. https://doi.org/10.21335/NMDC-477241498.

Nilsen, R., R. M. Serra-Llinares, V. Ambjørndalen, M. Berg, G. B. Lehmann, A.Tonstad, I. Uglem, and Ø. Karlsen. 2021. “Havforskningsinstituttet Ruse og Garn NALO 2021.” Dataset. https://ftp.nmdc.no/nmdc/IMR/lakselus/ Havforskningsinstituttet_RuseOgGarnNALO-2021.xlsx.

Nilsen, R., R. M. Serra-Llinares, M. Berg, G. B. Lehmann, B. Finstad, and Ø. Karlsen. 2021b. “Havforskningsinstituttet Ruse og Garn NALO 2019.” Dataset. https://doi.org/10.21335/ NMDC-163762784.

Nilsen, R., R. M. Serra-Llinares, M. Berg, G. B. Lehmann, B. Finstad, and Ø. Karlsen. 2021a. “Havforskningsinstituttet Ruse og Garn NALO 2018.” Dataset. https://doi.org/10.21335/ NMDC-616838292.

R Core Team. 2022. R: A Language and Environment for Statistical Computing. Vienna: R Foundation for Statistical Computing.

Rikardsen, A. H., and P.-A. Amundsen. 2005. “Pelagic Marine Feeding of Arctic Charr and Sea Trout.” Journal of Fish Biology 66: 1163–66.

Sandvik, A. D., B. Ådlandsvik, L. Asplin, I. A. Johnsen, M. Myksvoll, and J. Albretsen. 2020. “Salmon Lice LADIM V2.” Dataset. https://doi.org/10.21335/NMDC-410516615. Sandvik, A. D., P. Bjørn, B. Ådlandsvik, L. Asplin, J. Skardhamar, I. Johnsen, M. Myksvoll, and M. Skogen. 2016. “Toward a Model-Based Prediction System for Salmon Lice Infestation Pressure. Aquaculture Environment.” Interactions 8: 527–542.

Sandvik, A. D., I. A. Johnsen, M. S. Myksvoll, P. N. Sævik, and M. D. Skogen. 2020. “Prediction of the Salmon Lice Infestation Pressure in a Norwegian Fjord.” ICES Journal of Marine Science 77: 746–756.

Schwarz, C. J., J. F. Schweigert, and N. A. Arnason. 1993. “Estimating Migration Rates Using Tag-Recovery Data.” Biometrics 49: 177–193.

Serra-Llinares, R. M., P. A. Bjørn, B. Finstad, R. Nilsen, A. Harbitz, M. Berg, and L. Asplin. 2014. “Salmon Lice Infection on Wild Salmonids in Marine Protected Areas: Aquaculture Environment.” Interactions 5: 1–16.

Serra-Llinares, R. M., T. Bøhn, Ø. Karlsen, R. Nilsen, C. Freitas, J. Albretsen, T. Haraldstad, E. Thorstad, K. Elvik, and P. Bjørn. 2020. “Impacts of Salmon Lice on Mortality, Marine Migration Distance and Premature Return in Sea Trout.” Marine Ecology Progress Series 635: 151–168.

Simmons, O., M. Thorsteinsson, and G. A.´ Ólafsd ottir. 2019. “Trophic Dynamics of Anadromous Brown Trout and Arctic Charr in NW Iceland and their Correlation to Salmon Lice Infection.” Polar Biology 42: 2119–30.

Spares, A. D., M. J. Dadswell, M. P. Dickinson, and M. J. W. Stokesbury. 2015. “A Critical Review of Marine Adaptability

within the Anadromous Salmoninae.” Reviews in Fish Biology and Fisheries 25: 503–519.

Stien, A., P. Bjørn, P. Heuch, and D. Elston. 2005. “Population Dynamics of Salmon Lice Lepeophtheirus salmonis on Atlantic Salmon and Sea Trout.” Marine Ecology Progress Series 290: 263–275.

- Stige, L. C., K. O. Helgesen, H. Viljugrein, and L. Qviller. 2021. “A Statistical Mechanistic Approach Including Temperature and Salinity Effects to Improve Salmon Lice Modelling of Infestation Pressure.” Aquaculture Environment Interactions 13: 339–361. https://doi.org/10.3354/aei00410.
- Stige, L. C., K. O. Helgesen, H. Viljugrein, and L. Qviller. 2022. “Modelling Salmon Lice-Induced Mortality of Wild Salmon Post-Smolts Is Highly Sensitive to Calibration Data.” Aquaculture Environment Interactions 14: 263–277.


Strøm, J. F., P. A. Bjørn, E. E. Bygdnes, L. Kristiansen, B. Skjold, and T. Bøhn. 2022. “Behavioural Responses of Wild Anadromous Arctic Char Experimentally Infested In Situ with Salmon Lice.” ICES Journal of Marine Science 79: 1853–63.

Taranger, G. L., Ø. Karlsen, R. J. Bannister, K. A. Glover, V. Husa, E. Karlsbakk, B. O. Kvamme, et al. 2015. “Risk Assessment of the Environmental Impact of Norwegian Atlantic Salmon Farming.” ICES Journal of Marine Science 72: 997–1021.

Thorstad, E. B., C. D. Todd, I. Uglem, P. A. Bjørn, P. G. Gargan, K. W. Vollset, E. Halttunen, S. Kålås, M. Berg, and B. Finstad. 2015. “Effects of Salmon Lice Lepeophtheirus salmonis on Wild Sea Trout Salmo trutta a Literature Review.” Aquaculture Environment Interactions 7: 91–113.

Thorstad, E. B., C. D. Todd, I. Uglem, P. A. Bjørn, P. G. Gargan, K. W. Vollset, E. Halttunen, S. Kålås, M. Berg, and B. Finstad.

2016. “Marine Life of the Sea Trout.” Marine Biology 163: 47.

Vollset, K. W., I. Dohoo, Ø. Karlsen, E. Halttunen, B. O. Kvamme, B. Finstad, V. Wennevik, et al. 2018. “Disentangling the Role of Sea Lice on the Marine Survival of Atlantic Salmon.” ICES Journal of Marine Science 75: 50–60.

Vollset, K. W., R. J. Lennox, H. Skoglund, Ø. Karlsen, E. S. Normann, T. Wiers, E. Stöger, and B. T. Barlaup. 2023. “Direct Evidence of Increased Natural Mortality of a Wild Fish Caused by Parasite Spillback from Domestic Conspecifics.” Proceedings of the Royal Society B: Biological Sciences 290: 20221752.

SUPPORTING INFORMATION

Additional supporting information can be found online in the Supporting Information section at the end of this article.

|How to cite this article: Hawley, K. L., H. A. Urke, T. Kristensen, and T. O. Haugen. 2024. “Individual Patterns of Anadromy Determine the Cost of Salmon Lice Exposure in Brown Trout.” Ecosphere 15(12): e70098. https://doi.org/10.1002/ ecs2.70098<br><br>|
|---|


21508925,2024,12,Downloadedfromhttps://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.70098byNorwegianInstituteOfPublicHealtInvoiceReceiptDFO,WileyOnlineLibraryon[27/01/2025].SeetheTermsandConditions(https://onlinelibrary.wiley.com/terms-and-conditions)onWileyOnlineLibraryforrulesofuse;OAarticlesaregovernedbytheapplicableCreativeCommonsLicense

