<!-- page 1 -->
AQUACULTURE ENVIRONMENT INTERACTIONS 
Aquacult Environ Interact
Vol. 16: 59–69, 2024 
https://doi.org/10.3354/aei00473
Published February 15
1.  INTRODUCTION 
Host density is a key driver in parasite population 
dynamics, with studies showing a positive correlation 
between host population density and individual host 
parasite load (Arneberg et al. 1998). This relationship 
is especially pertinent in farming, where high host 
densities can elevate the risks of parasite infestations, 
impacting both plant and animal yields (Bondad-
Reantaso et al. 2005, Mennerat et al. 2010). Specifi-
cally, farmed salmonid (Salmonidae spp.) densities 
in fluence the population growth of salmon lice 
Lepeo phtheirus salmonis in marine farming systems 
in Norway (Grimnes & Jakobsen 1996, Jansen et al. 
2012, Kristoffersen et al. 2014, Aldrin et al. 2019, Dean 
et al. 2021). Beyond mere density, the spatial distribu-
tion of hosts in dense farms adds complexities, affect-
ing both between-farm dispersal and local infestation 
© The authors 2024. Open Access under Creative Commons by 
Attribution Licence. Use, distribution and reproduction are un -
restricted. Authors and original publication must be credited. 
Publisher: Inter-Research · www.int-res.com
*Corresponding author: lars.qviller@vetinst.no
Geographic redistribution of farmed salmonids 
reduces salmon lice infestations and treatment 
frequency in a simulation study 
Lars Qviller1,*, Katharine Rose Dean1, Mats Huserbråten2, Ingrid Askeland Johnsen2, 
Britt Bang Jensen1,3 
1Norwegian Veterinary Institute, 1433 Ås, Norway 
2Institute of Marine Research, 5817 Bergen, Norway 
3Technical University of Denmark, 2800 Kongens Lyngby, Denmark
ABSTRACT: Host density is a key driver in parasite population dynamics, and often the number of 
parasites increases rapidly with host density. In the context of Norwegian salmonid farming, this 
mechanism has led to a disparity between the desire to increase cultured salmonid production, and 
to reduce the negative effects of parasite infestations. Salmon lice infestations are detrimental to 
animal welfare due to salmon lice treatments and spillover from farms to wild salmonids. Here, we 
examine how a redistribution of the salmonid farm biomass may hamper exchanges of lice larvae 
between farms, and consequently reduce the salmon lice burdens and treatment frequencies. More 
specifically, we use a stochastic simulation model, fitted to empirical data from Norwegian aqua-
culture, to examine how lice abundances and treatments responded when the biomass in the sys-
tem was distributed onto fewer, larger farms situated farther apart. To maintain realistic fish 
growth, seasonality and cohort development, lice population dynamics were simulated on top of 
historic production data from Norway. We simulated several scenarios, where an increasing 
number of farms were closed, and their biomass was redistributed to other farms with matching co -
horts. The results indicate that fewer and larger farms reduce lice numbers and treatment fre -
quency, and that a strategic removal of farms, based on their importance for connectivity in an 
oceanographic lice dispersal network, improves this effect. Some core mechanisms are highlighted 
that should be considered in regional production planning, and in the allocation of production 
concessions in salmonid farming. 
 
KEY WORDS:  Salmon lice · Atlantic salmon · Aquaculture management · Simulation study · 
Spatial planning 
OPEN
PEN
 ACCESS
CCESS


<!-- page 2 -->
Aquacult Environ Interact 16: 59–69, 2024
dynamics. Consequently, Norway’s salmonid farm-
ing industry grapples with the challenge of increasing 
production while mitigating the adverse impacts of 
salmon lice infestations on farmed and wild fish. 
The monthly average standing stock in a Norwe-
gian salmonid farm during our study period between 
2014 and 2017 was 713 000 fish, but the numbers vary 
greatly (67 000–1 578 000, 5–95% percentile range). 
The entire Norwegian standing stock of Atlantic sal-
mon currently varies annually between 350 and 450 
million fish (Kristoffersen et al. 2018). Dempster et al. 
(2021) estimated that farmed salmonids in 2017 out-
numbered wild salmonids by somewhere between 
267:1 and 281:1, and that farmed salmonids produced 
about 98% of the mated (ovigerous) female salmon 
lice in Norwegian coastal waters. Therefore, when the 
salmon louse is established in farms situated in areas 
with intense salmonid farming, the contribution to 
infestation pressure from wild populations is re -
garded as insignificant (Heuch & Mo 2001, Heuch et 
al. 2005, Johansen et al. 2011, Samsing et al. 2019, 
Dempster et al. 2021). 
Salmonids are usually farmed in open net-pens that 
allow for exchange of oxygenated water, but also 
plank tonic organisms such as transmissible salmon 
lice larvae. Globally there is a trend of increasing size 
of salmon farms, where the size of the net-pens has 
grown over 200% in surface area from 2005 to 2020 in 
Norway (McIntosh et al. 2022). During the same 
period (2005–2020), the distance between sites in -
creased in Norway (McIntosh et al. 2022). The marine 
phase of the production cycle of salmonids usually 
has a duration of between 14 and 19 mo (Bang Jensen 
et al. 2020b), and only 1 generation is allowed at the 
farm per production cycle. After the production cycle 
is ended, the farm must be fallowed for approximately 
2 mo as a biosecurity measure (Ministry of Trade, 
Industry and Fisheries 2008). 
Salmon lice are harmful to their hosts (Costello 
2006), and have been a major problem in Norwegian 
fish farming since the beginning of industrial salmon 
aquaculture in the 1970s. Lice surveillance, preven-
tion and control measures are mandatory, and include 
weekly reports of lice counts in 3 groups: adult fe -
males (AF), adult males and preadult lice (other 
motile, OM), and chalimus larvae (sessile lice). The 
current legislation stipulates that the parasite load 
cannot exceed 0.2 AF lice per salmonid on average 
during the wild salmon smolt outmigration in the 
spring, and 0.5 for the remainder of the year (Ministry 
of Trade, Industry and Fisheries 2012). 
Salmon lice feed on host mucus, skin and blood 
(Pike & Wadsworth 1999, Costello 2006). The spill-
over of salmon lice from farmed to wild fish is re -
garded as one of the major threats to wild salmonids 
in Norway (Taranger et al. 2015, Forseth et al. 2017, 
Vollset et al. 2019, Sandvik et al. 2021). The lice level 
on farmed fish is therefore monitored and managed to 
a low level where the treatments rather than the lice 
infestations are harmful to the farmed salmonids per 
se. The indirect deleterious effects may still be con-
siderable. Treatments to control salmon lice are costly 
and harmful to the fish and cause losses and mortality 
(Overton et al. 2019, Oliveira et al. 2021, Sviland 
Walde et al. 2021), and increased salmon lice prolifer-
ation is therefore a major sustainability concern, 
which negatively impacts the profitability of the 
industry, animal welfare, biodiversity, as well as the 
availability of farmed salmonids to the global food 
market. Salmonid farming intensity is now regulated 
according to the industry’s environmental impact on 
wild salmonids in 13 discrete production areas that 
covers the entire Norwegian coastline (Ministry of 
Trade, Industry and Fisheries 2015, 2017, Kristof-
fersen et al. 2018, Myksvoll et al. 2018, Sandvik et al. 
2020, Johnsen et al. 2021). The impact is currently 
assessed based on the mortality of out-migrating wild 
salmon smolts, caused by salmon lice spillover from 
farmed fish (Ministry of Trade, Industry and Fisheries 
2015, 2017, Kristoffersen et al. 2018, Sandvik et al. 
2020, Johnsen et al. 2021). 
The salmon louse naturally inhabits an ocean with 
low host densities (Dempster et al. 2021). In areas 
with intensive salmonid farming, the ocean is scat-
tered with dense clusters of suitable hosts in the 
farms, with varying degrees of contact between the 
clusters/farm (Samsing et al. 2017, Huserbråten & 
Johnsen 2022). This structure, a population of pop-
ulations, is commonly referred to as a metapopula-
tion (Levins 1969), illustrating the uneven distribution 
of a host population across distinct, yet intercon-
nected subpopulations. Within this structure, a sub-
population can experience lice infestations through 
2 primary path ways: (1)  through ‘self-infestations’, 
where the lice population within a farm is sustained 
by local reproduction; and (2) via dispersal, where 
lice are introduced from neighboring farms and 
then proliferate within the new environment (Toor-
ians & Adams 2020). Subpopulations face local 
extinctions or recolonizations, but if these are bal-
anced, the metapopulation as a whole remains 
stable. In the case of salmon lice in salmonid farm-
ing, extinctions or significant drops in lice subpop-
ulations occur at the end of the production cycle or 
with lice treatments, and farms are recolonized 
through the inter-farm network of lice dispersal 
60


<!-- page 3 -->
Qviller et al.: Biomass redistribution reduces salmon lice infestations
(Samsing et al. 2019). It is the size of the lice meta -
population, which is accelerated by connectivity 
between subpopulations, however, that limits the 
sustainability in salmonid farming within the pro-
duction areas. 
One suggestion to manage the salmon lice popula-
tion has been to modify the structure of the farming 
system. For example, if the biomass is distributed on 
fewer farms, the distances between the subpopula-
tions will increase, leading to increased network frag-
mentation. Moreover, if certain farms that are espe-
cially important for connectivity are removed, it is 
possible to create ‘firebreaks’, or barriers between 
parts of the network (Samsing et al. 2019). 
Here, we use a simulation model (Aldrin et al. 2019) 
to analyze how sea lice abundances respond to a 
redistribution of the overall biomass in an area onto 
fewer and larger farms. We achieved this by closing 
some farms and redistributing the biomass onto other 
farms, with matching cohorts. We then compared the 
effects of removing a random selection of farms with a 
strategic selection, informed by a biophysical model 
(Huserbråten et al. 2020, Huserbråten & Johnsen 2022) 
that identified farms with the strongest influence on 
the other farm sites. 
2.  MATERIALS AND METHODS 
2.1.  Study area 
The simulation study was conducted with data from 
production area PA3 (PO3 in Norwegian) on the west-
ern coast of Norway (Fig. 1). The area covers 2 main 
fjords, Bjørnafjorden in the north, and Hardangerfjor-
den in the south. The fjords are divided into several 
smaller fjord arms with deep basins, numerous small 
and large islands, sills, sounds and several openings 
to the outer ocean (Sandvik et al. 2020). PA3 covers an 
area of 3646 km2, and includes 147 farms that were 
actively producing salmonids during the study period 
(January 2014–December 2017). The average stand-
ing stock in the farms in PA3 during the study period 
was 544 000 fish (64 000–1 084 000, 5–95% percentile 
range). 
2.2.  Data 
The simulations were performed using data from 2 
different datasets. Farm locations were collected from 
the Norwegian aquaculture register, hosted by the 
61
Fig. 1. (a) Study area in Norway. Black outline: production area PA3. (b) The sites in PA3, with the coloration of the farms illus-
trating an example of a scenario. Red dots: the farms being removed with a strategic removal of 30% of the most connected 
farms (Scenario 7 in Table 1); their biomass was distributed onto those of the remaining farms (blue dots) with cohorts that 
match in time. The connectivity network used for the strategic removal of farms is presented in Fig. 2 in Huserbråten &  
Johnsen (2022)


<!-- page 4 -->
Aquacult Environ Interact 16: 59–69, 2024
Norwegian Directorate of Fisheries (https://www.
fiskeridir.no/Akvakultur/Registre-og-skjema/akva
kulturregisteret) (in Norwegian, downloaded May 1, 
2022), and data on number and weight of salmonids 
were retrieved from a national registry hosted by the 
Norwegian Directorate of Fisheries on a monthly 
basis. Seaway distances between farms were calcu-
lated as distances between farms in the water, around 
islands, peninsulas and hindrances in the water (see 
Dean et al. 2021 for a thorough description of the 
calculation of seaway distances).
 
2.3.  Simulation model 
The simulations performed in the present study are 
based on a previously published model for predicting 
sea lice abundances (Aldrin et al. 2019). The model 
describes the spatiotemporal development of salmon 
lice in the farms, and was fitted using production data 
from all Norwegian farms with a standing stock of 
either rainbow trout Oncorhynchus mykiss or Atlantic 
salmon Salmo salar in weekly time steps, from Week 1 
in 2012, to Week 44 in 2016. The model consists of 
2  sub-models, 1 for AF lice and 1 for OM lice. The 
number of AF in the current week depends on the 
number of AF the previous week and their survival, 
and the recruitment from the OM stages. The model 
calculates the number of OM in the current week 
based on the number of OM the previous week, their 
survival, recruitment from reproduction in the cur-
rent farm, and recruitment from farms in the neigh-
borhood. Development times, reproduction and mor-
tality of the lice depend on temperature. Local 
recruitment is a function of the number of AF in the 
current farm, while the external recruitment is a func-
tion of AF in the surrounding farms, and the seaway 
distances between farms. The model also includes 
treatments against salmon lice based on average 
number of lice counted on fish in the farms, as re -
quired by Norwegian legislation (Ministry of Trade, 
Industry and Fisheries 2012). Manual counting of AF 
and OM abundances per fish in the farms were there-
fore simulated in the model, performed by random 
draws from the underlying distributions in the simula-
tion model, and registered weekly from 40 fish. Treat-
ments were initiated when the average number of sal-
mon lice in the simulated counts was above 0.5, or 
below 0.2 during the period for wild smolt out-migra-
tions (Weeks 16–21), as required by the legislation 
(Ministry of Trade, Industry and Fisheries 2012). 
Treatment in the model was set to reduce the lice 
counts by 75% for both AF and OM. 
Here, we use the same model and parameters as 
described above for simulations, with the exception of 
treatment mortality, as discussed above, and we re -
moved a downward trend in lice abundance over time 
(denoted βk
susc in Aldrin et al. 2019). This parameter 
was included in the original model to account for a 
downward trend in the historical data, but it is not 
needed to compare between scenarios. This trend was 
therefore removed (βk
susc was set to zero) in this effort. 
The first 16 wk in the simulations were considered a 
spin-up period used to calibrate the model and to 
construct the lagged variables, as described in Aldrin 
et al. (2019). 
2.4.  Scenario simulations 
We simulated the AF and OM populations using 
historical data of fish abundances and farm locations 
from 2014 to 2017 to inform the simulations. We simu-
lated 9 different scenarios (Table 1): the baseline sce-
nario where we made no changes to farm structure 
(Scenario 1); 4 scenarios where we randomly removed 
62
Scenario             Name                                                Description                                            Simulations                  Max cohort size 
 
1                         Baseline                                   Current farm structure                                        1000                                2 066 561 
2                             R20                          Random removal of 20% of the farms                         10 000                    4 324 984–7 195 871 
3                             R30                          Random removal of 30% of the farms                         10 000                   6 038 964–10 014 704 
4                             R40                          Random removal of 40% of the farms                         10 000                   6 057 988–15 296 941 
5                             R50                          Random removal of 50% of the farms                         10 000                   7 953 479–18 185 020 
6                              S20                          Strategic removal of 20% of the farms                          1000                                6 286 232 
7                              S30                          Strategic removal of 30% of the farms                          1000                                9 797 388 
8                              S40                          Strategic removal of 40% of the farms                          1000                               12 001 915 
9                              S50                          Strategic removal of 50% of the farms                          1000                               14 586 857 
Table 1. The 9 scenarios, with description, total number of simulations and maximum cohort size. Cohort size defined as the 
maximum number of fish registered with that cohort in the dataset. Note that max cohort size for scenarios R20, R30, R40 and 
R50 gave 1 maximum cohort size for each randomization, and the values are given as an interval, from the lowest to highest  
recorded max cohort size in all 10 randomizations


<!-- page 5 -->
Qviller et al.: Biomass redistribution reduces salmon lice infestations
an increasing percentage of farms (random removal) 
(Scenarios 2–5); and 4 scenarios where we removed 
an increasing percentage of the farms based on farm 
connectivity (strategic removal) (Scenarios 6–9). 
We performed Scenarios 2–5 on 10 different ran-
dom selections of farms from the dataset, to avoid 
drawing conclusions based on especially beneficial 
or harmful constellations appearing by chance. We 
moved the biomass from all cohorts in the closed 
farms to other farms with matching cohorts in time, to 
ensure that the biomass in the area did not change. 
The consequence of this redistribution scheme was 
that the farms grew, and in some cases the farms grew 
to become unrealistically large, with a few farms in 
the most radical scenarios exceeding 5 million fish, 
and a maximum of 18.2 million fish (Table 1). 
In Scenarios 6–9, we removed the farms that were 
shown to contribute the most to the external infesta-
tion pressure on the other farm sites, based on results 
of a connectivity ana lysis performed by the Institute 
for Marine Research (Huser bråten et al. 2020, Huser-
bråten & Johnsen 2022). This connectivity analysis 
was based on a coupled biological–physical model 
that used realistic nauplii production on farms (based 
on industry-provided lice counts and temperature), 
and the pelagic lice stages were dispersed and tracked 
by a high-resolution hydrodynamic model until settle-
ment. Here, total export to other farms (i.e. all outgo-
ing connections) were quantified as the sum of salmon 
lice larvae produced/released at Farm A that was 
transmitted to Farm B, C, D; and from Farm B to Farm 
A, C, D, etc.; iterated over all farms in the model do-
main. Subsequently a ranked list of which farm ex-
ported the most to other farms was compiled, and in 
the strategic removal scenarios farms were removed 
sequentially according to this list. As with the random 
farms, we eliminated an increasing percentage of 
farms in each subsequent scenario, as presented in 
Table 1. 
Fig. 1b illustrates one specific scenario geographi-
cally, as an example (Scenario 7). We simulated each 
scenario 1000 times using the procedure in Aldrin et 
al. (2019). 
Each simulation returned the average number of AF 
salmon lice per fish and the average number of OM 
lice per fish. From the simulated treatments, we calcu-
lated the number of annual fish treatments by taking 
the sum of the number of fish in all treated farms 
every month. 
All simulations were performed using R statistical 
software (R Development Core Team 2017). The map 
in Fig. 1 was made using the R package ‘tmap’ (Ten-
nekes 2018). Seaway distances were calculated using 
the ‘gdistance’ library in R (van Etten 2017). The code 
for making Figs. 2–5 is available at GitHub (https://
github.com/NorwegianVeterinaryInstitute/PO3_
paper.git). The code includes a download of the re -
sults from the simulations (available at: https://
zenodo.org/record/7308221/files/boxplot_df.RDS?
download=1).
 
63
Fig. 2. Mean and variability of simulated yearly mean adult female sea lice per fish from all simulations. Box: interquartile range  
(IQR); line: median; whiskers: max./min. value ≤ 1.5 × IQR; dots: outliers 


<!-- page 6 -->
Aquacult Environ Interact 16: 59–69, 2024
3.  RESULTS 
The results are summarized from the 9 scenario sim-
ulations described in Section 2.4 (Table 1). The bio-
mass from the closed farms was redistributed to other 
farms with matching cohorts to ensure that changes 
in treatment intensity or salmon lice numbers were 
not an effect of host population size, but rather the 
spatial distribution of the biomass. 
The results from all 45 000 simulations are sum -
marized as yearly averages for each of the 9 scenarios 
in Table 1. By closing farms and relocating the bio-
64
Fig. 4. Percent reduction of (a) adult female lice, (b) other motile lice and (c) treatment intensity, when comparing strategic  
removal scenarios and random removal scenarios with the baseline
Fig. 3. Mean and variability of simulated yearly mean other motile lice per fish, from all simulations. Boxplot parameters as in Fig. 2


<!-- page 7 -->
Qviller et al.: Biomass redistribution reduces salmon lice infestations
mass to other farms, the average number of AF and 
OM sal mon lice was reduced by 4–15 and 6–23%, 
re spectively (Figs. 2–4). With the reduced number of 
lice, the annually averaged number of fish treatments 
per year was also reduced, by 6–25% (Figs. 4 & 5). 
Note that each fish may be exposed to several treat-
ments, and the treatment number therefore ex ceeded 
the number of fish in the production area. The model 
used the first 16 wk of 2014 to construct the lagged 
variables, and these weeks are not in cluded in the 
results. The treatments recorded for 2014 therefore 
included fewer weeks, which resulted in fewer treat-
ments in 2014 (Fig. 5). 
The model predicted considerable variation be -
tween scenarios, and some variation between years 
(Figs. 2, 3 & 5). There was a general tendency, how -
ever, that closing a greater number of farms led to a 
greater reduction in the number of lice and treat-
ments. Moreover, the strategic removal of farms 
seemed to reduce the number of treatments and lice 
numbers more than removing farms randomly. 
The percentage reduction of strategic removal and 
random removal compared with the baseline revealed 
that the most effective measure to mitigate the impact 
of salmon lice was Scenario 9, to remove 50% of the 
farms strategically. This measure led to a 15% median 
reduction of AF, as compared to the baseline value, 
23% median reduction in OM lice and 25% median 
reduction in the number of fish treatments over the 
entire simulation period (Fig. 4).  
4.  DISCUSSION 
Here, we demonstrate that distributing the biomass 
of salmonids (the hosts) onto fewer farms with greater 
distance between them may be an effective preven-
tative measure against salmon lice infestations. Larger 
distances between farms reduces between-farm dis-
persal, disrupts transmission networks, and con-
sequently reduces the average number of lice in the 
metapopulation. AF lice (Fig. 2) and OM lice (Fig. 3) 
are consequently less abundant in all redistribution 
scenarios with increasingly larger and fewer farms, 
despite increased farm sizes. The effect is least pro-
nounced for AF in all scenarios. The latter result may 
be an effect of the treatment regime. Fish are treated 
based on AF counts, and the treatment regime will 
reduce the simulated numbers of female lice when the 
maximum allowed AF lice burden is ex ceeded, as 
long as the treatment efficacy is able to counteract the 
lice population growth. A reduced development of 
female lice when the salmonids are redistributed will 
therefore be partly manifested as a reduced treatment 
65
Fig. 5. Mean and variability of simulated annual fish treatments divided by 1 million. Note that each fish may be exposed to sev-
eral treatments, and this number will therefore exceed the number of fish in the production area. The simulations use 16 wk to 
stabilize, and those weeks are left out of the data. This is the reason for the lower number of fish in treated farms in 2014. Boxplot  
parameters as in Fig. 2


<!-- page 8 -->
Aquacult Environ Interact 16: 59–69, 2024
frequency. The results also indicate that each fish will 
experience fewer treatments when there are fewer 
and larger farms, as expected with a slower develop-
ment of AF lice populations (Figs. 4 & 5). 
Salmon lice dispersal has usually been modeled in 2 
different paradigms. The simulation model (Aldrin et 
al. 2019) belongs to a group of lice models where the 
transmission contact between farms is an effect of 
seaway distances (Aldrin et al. 2013, Kristoffersen et 
al. 2014, 2018), effectively assuming that the large-
scale distribution of water movement evens out over 
time, as well as geographically over several farm loca-
tions. By contrast, the model used to target important 
farms in the system models lice larvae transmission in 
a hydrodynamic model (Asplin et al. 2014, Sandvik et 
al. 2016, 2020, Myksvoll et al. 2018, Johnsen et al. 
2021). Networks built with the 2 different approaches 
are not equal, and the farms that are removed based 
on the hydrodynamic model are not necessarily the 
best choice for a distance-based model. A model suit-
able to simulate the population dynamics of salmon 
lice that includes the hydrodynamic properties is not 
currently available. The hydrodynamic properties, 
however, are important for the dispersal of planktonic 
organisms like salmon lice larvae, and a model that 
includes the movement of the water is probably better 
suited to identify important nodes in the real-world 
network. Here, we demonstrate that simulated sce-
narios with a strategic removal of farms based on a 
hydrodynamic network model is a better mitigation 
measure than the random removal of farms. There-
fore, the illustrated potential in removing farms stra -
tegically is valid across model specifications, which 
implies a robustness to this finding. 
The system of salmonid farms in Norway can be 
thought of as a network composed of nodes. Although 
it is shown that this network has great temporal vari-
ability, spatial networks that are highly structured can 
be identified where there are farms that support high 
densities of salmon lice in subpopulations (Huser-
bråten & Johnsen 2022). These salmon lice subpop-
ulations are connected through water exchange be -
tween the farms, the intensity of which is determined 
by distance, geographical features, water currents and 
temperature-controlled development of the salmon 
lice (Samsing et al. 2019). The distribution of the con-
nections between nodes/farms is important for the 
resilience of the network. Real-world networks often 
display an extremely inhomogeneous connectivity be -
tween nodes, and some nodes may connect otherwise 
distinct or significantly less connected populations 
(Albert et al. 2000). The removal of a random farm in 
this case could be redundant, and is consequently not 
likely to alter the path structure of lice larvae ex -
change, or the overall network topology (Albert et al. 
2000). The random removal of several farms may 
reduce connectivity, but the intervention be comes 
stronger than necessary, because the re moved farms 
contribute to the desired effect to a varying degree. 
An informed management strategy, on the other 
hand, can target key farms in the system for removal, 
thus exploiting the properties of the network for dis-
ease control (Albert et al. 2000, Chami et al. 2017), ef -
fectively producing ‘firebreaks’ that disconnect parts 
of the network, as suggested by Samsing et al. (2019). 
Recent research, however, argues that natural net-
works are more resilient than previously believed 
(Broido & Clauset 2019). It is also important to note 
that the salmon lice in the present simulation study 
are not restricted to farms, but are also naturally oc -
curring in the absence of salmonid aquaculture. 
While the infestation pressure from wild sources is 
regarded as insignificant in calculations of infestation 
pressure in most cases (Heuch & Mo 2001, Heuch et 
al. 2005, Johansen et al. 2011, Samsing et al. 2019, 
Dempster et al. 2021), it makes a total isolation from 
salmon lice impossible in aquaculture with open 
cages that are exposed to the environment. Both the 
simulation model and the real world includes a back-
ground infestation rate from natural sources, which 
may reduce the effect of network fragmentation be -
tween farms to some degree. In addition, the wild host 
populations interact with the salmon lice densities 
produced in farms. A complete transformation into 
disconnected subnetworks may therefore not be fea-
sible. Nevertheless, our results indicate that the bene-
fits of removing farms becomes bigger when we re -
move them strategically, based on the connection 
network developed in Huserbråten & Johnsen (2022). 
For instance, the average fish experience between 6 
and 17% less treatments in the random removal sce-
narios, and between 14 and 25% less treatments in 
the strategic removal scenarios. 
Treatments in the model were set to reduce lice 
counts by 75% for both AF and OM lice. The effec-
tiveness chosen in the present study was therefore 
somewhat higher than the estimated 44 to 47% in the 
development of the simulation model (Aldrin et al. 
2019). The authors do, however, argue that this value 
was unexpectedly low, and it is unclear whether treat-
ments cover the entire farm or some selected cages. A 
more detailed model with similar outlines that were 
fitted to cage-level data describes treatment effec-
tiveness between 0 and 99% (Aldrin et al. 2017). We 
assumed that there is knowledge in the industry 
about treatment effectiveness, and chose an effective-
66


<!-- page 9 -->
Qviller et al.: Biomass redistribution reduces salmon lice infestations
ness closely resembling the estimated effect of aza -
methiphos in Aldrin et al. (2017). Moreover, synchro-
nization of generations and salmon lice treatments 
were mandatory in the study area during the study 
period (Ministry of Trade, Industry and Fisheries 
2010, Guarracino et al. 2018), and synchronized treat-
ments are known to be an effective measure (Arria-
gada et al. 2017). 
The modeling paper by Aldrin et al. (2019) did 
include an analysis where the authors looked at how 
the infestation pressure increased by doubling the 
farm sizes, and by doubling the number of farms. The 
results from this analysis indicated that larger and 
fewer farms reduce lice burdens, thus concurring with 
the results from the present study. The authors simul-
taneously suggest that causal ef fects should be inter-
preted with care, due to confounding factors related 
to regions where the farms are located and how farms 
are managed. Here, in the present study, we add real-
ism to the simulations by redistributing the biomass 
between existing farms with matching cohorts, and 
we show that the location of the farms does matter in 
the strategic removal scenarios. 
Time-series simulations have been effectively ap -
plied to study disease transmission of other agents, 
such as those that cause pancreas disease (PD) and 
infectious salmon anemia (ISA). These outbreak sim-
ulations typically factor in distances between farms, 
with their sizes and overlapping production history 
revealing that both farm size and increasing inter-
farm distances are significant predictors of disease 
transmission in Norwegian salmonid aquaculture (Al -
drin et al. 2019, 2021, Bang Jensen et al. 2020a, 2021, 
Stige et al. 2021). There is a prevailing trend showing 
a rapid decline in transmission probability as distance 
between farms increases. On the other hand, bigger 
farms constitute a larger transmitter and re ceiver of 
infectious agents, which may contradict the effect of 
increasing distances between farms. Modeling of 
viral and bacterial diseases does suggest, however, 
that distributing the biomass over larger farms situ-
ated farther apart may also reduce transmission of 
viruses and bacteria (Salama & Murray 2012). 
It is important to note that the results of the present 
study are the product of a modeling and simulation 
exercise, and there are several caveats to generalizing 
the results to the real world. First, we did not consider 
whether the location of removed farms is suitable for 
the increased biomasses and fish abundances that 
were created in the scenarios. Second, we did not con-
sider whether the increased fish abundance was 
within the numbers that can be managed in a salmo-
nid farm, and some of the farms did become unrealis-
tically large, especially in the 50% removal scenarios 
(Table 1). Large farms will cover more cages and a 
larger area, the handling of fish may become more dif-
ficult, and ordering wellboats for treatment etc. may 
be delayed in big farms. Third, the treatments in the 
model were carried out the week after the farm ex -
ceeded the threshold for mandatory treatments. This 
is probably not realistic in many cases, because lice 
treatments are big operations that include wellboats 
with proper equipment. The availability of wellboats 
and equipment may be limited, especially in periods 
with high lice burdens in many farms. Fourth, the 
farm sizes in the redistribution scenarios exceed the 
data used to fit the simulation model to a large degree 
(Table 1). Extrapolations outside the range of the data 
used to fit the model will introduce unknown uncer-
tainty in the simulations. 
The methods behind the present paper are therefore 
not a straightforward procedure to optimize farm 
structure in the study area. The qualitative re sults, ho-
wever, point to some core mechanisms that could be 
considered in the planning of farm structure in salmo-
nid aquaculture to ease the burden of salmon lice. 
 
 
Acknowledgements. This study was partly funded by the 
Research Council of Norway, project 254830/E40 ‘Host den-
sity and pathogen transmission in salmon aquaculture: ef fects 
of increased production and pathogen control policies’, and 
partly by the Norwegian Veterinary Institute and the Institute 
of Marine Research. We thank Magne Aldrin and Ragnar 
Bang Huseby for a copy of the simulation software developed 
in Aldrin et al. (2019), and instructions on how to use it. 
 
 
LITERATURE CITED 
 
Albert R, Jeong H, Barabási AL (2000) Error and attack toler-
ance of complex networks. Nature 406: 378– 382  
Aldrin M, Storvik B, Kristoffersen AB, Jansen PA (2013) 
Space-time modelling of the spread of salmon lice be -
tween and within Norwegian marine salmon farms. PLOS 
ONE 8: e64039  
Aldrin M, Huseby RB, Stien A, Grøntvedt RN, Viljugrein H, 
Jansen PA (2017) A stage-structured Bayesian hierarchi-
cal model for salmon lice populations at individual sal-
mon farms — estimated from multiple farm data sets. Ecol 
Modell 359: 333– 348  
Aldrin M, Jansen PA, Stryhn H (2019) A partly stage-struc-
tured model for the abundance of salmon lice in salmonid 
farms. Epidemics 26: 9– 22  
Aldrin M, Huseby RB, Bang Jensen B, Jansen MD (2021) 
Evaluating effects of different control strategies for Infec-
tious Salmon Anaemia (ISA) in marine salmonid farming 
by scenario simulation using a disease transmission 
model. Prev Vet Med 191: 105360  
Arneberg P, Skorping A, Grenfell B, Read AF (1998) Host 
densities as determinants of abundance in parasite com-
munities. Proc R Soc B 265: 1283– 1289  
Arriagada G, Stryhn H, Sanchez J, Vanderstichel R and 
67


<!-- page 10 -->
Aquacult Environ Interact 16: 59–69, 2024
others (2017) Evaluating the effect of synchronized sea 
lice treatments in Chile. Prev Vet Med 136: 1– 10  
Asplin L, Johnsen IA, Sandvik AD, Albretsen J, Sundfjord V, 
Aure J, Boxaspen KK (2014) Dispersion of salmon lice in 
the Hardangerfjord. Mar Biol Res 10: 216– 225  
Bang Jensen B, Mårtensson A, Kristoffersen AB (2020a) Esti-
mating risk factors for the daily risk of developing clinical 
cardiomyopathy syndrome (CMS) on a fishgroup level. 
Prev Vet Med 175: 104852  
Bang Jensen B, Qviller L, Toft N (2020b) Spatio-temporal 
variations in mortality during the seawater production 
phase of Atlantic salmon (Salmo salar) in Norway. J Fish 
Dis 43: 445– 457  
Bang Jensen B, Dean KR, Huseby RB, Aldrin M, Qviller L 
(2021) Realtime case study simulations of transmission of 
Pancreas Disease (PD) in Norwegian salmonid farming 
for disease control purposes. Epidemics 37: 100502  
Bondad-Reantaso MG, Subasinghe RP, Arthur JR, Ogawa K 
and others (2005) Disease and health management in 
Asian aquaculture. Vet Parasitol 132: 249– 272  
Broido AD, Clauset A (2019) Scale-free networks are rare. 
Nat Commun 10: 1017  
Chami GF, Ahnert SE, Kabatereine NB, Tukahebwa EM 
(2017) Social network fragmentation and community 
health. Proc Natl Acad Sci USA 114: E7425– E7431  
Costello MJ (2006) Ecology of sea lice parasitic on farmed 
and wild fish. Trends Parasitol 22: 475– 483  
Dean KR, Aldrin M, Qviller L, Helgesen KO, Jansen PA, 
Jensen BB (2021) Simulated effects of increasing salmo-
nid production on sea lice populations in Norway. Epi-
demics 37: 100508  
Dempster T, Overton K, Bui S, Stien LH and others (2021) 
Farmed salmonids drive the abundance, ecology and evo-
lution of parasitic salmon lice in Norway. Aquacult Envi-
ron Interact 13: 237– 248  
Forseth T, Barlaup BT, Finstad B, Fiske P and others (2017) 
The major threats to Atlantic salmon in Norway. ICES J 
Mar Sci 74: 1496– 1513  
Grimnes A, Jakobsen PJ (1996) The physiological effects of 
salmon lice infection on post-smolt of Atlantic salmon. 
J Fish Biol 48: 1179– 1194 
Guarracino M, Qviller L, Lillehaug A (2018) Evaluation of 
aquaculture management zones as a control measure for 
salmon lice in Norway. Dis Aquat Org 130: 1– 9  
Heuch PA, Mo TA (2001) A model of salmon louse production 
in Norway: effects of increasing salmon production and 
public management measures. Dis Aquat Org 45: 145– 152  
Heuch PA, Bjørn PA, Finstad B, Holst JC, Asplin L, Nilsen F 
(2005) A review of the Norwegian ‘National Action Plan 
Against Salmon Lice on Salmonids’: the effect on wild 
salmo nids. Aquaculture 246: 79– 92  
Huserbråten M, Ådlandsvik B, Bergh Ø, Grove S and others 
(2020) Endret lokalitetsstruktur i produksjonsområde 3. 
Rapport fra havforskningen 2020-12. Institute of Marine 
Research, Bergen  
Huserbråten MBO, Johnsen IA (2022) Seasonal temperature 
regulates network connectivity of salmon louse. ICES J 
Mar Sci 79: 1075– 1082  
Jansen PA, Kristoffersen AB, Viljugrein H, Jimenez D, Aldrin 
M, Stien A (2012) Sea lice as a density-dependent con-
straint to salmonid farming. Proc R Soc B 279: 2330– 2338 
Johansen LH, Jensen I, Mikkelsen H, Bjørn PA, Jansen PA, 
Bergh O (2011) Disease interaction and pathogens ex -
change between wild and farmed fish populations with 
special reference to Norway. Aquaculture 315: 167– 186  
Johnsen IA, Harvey A, Sævik PN, Sandvik AD and others 
(2021) Salmon lice-induced mortality of Atlantic salmon 
during post-smolt migration in Norway. ICES J Mar Sci 
78: 142– 154  
Kristoffersen AB, Jimenez D, Viljugrein H, Grøntvedt R, 
Stien A, Jansen PA (2014) Large scale modelling of sal-
mon lice (Lepeophtheirus salmonis) infection pressure 
based on lice monitoring data from Norwegian salmonid 
farms. Epidemics 9: 31– 39  
Kristoffersen AB, Qviller L, Helgesen KO, Vollset KW, Vil-
jugrein H, Jansen PA (2018) Quantitative risk assessment 
of salmon louse-induced mortality of seaward-migrating 
post-smolt Atlantic salmon. Epidemics 23: 19– 33  
Levins R (1969) Some demographic and genetic consequences 
of environmental heterogeneity for biological control. Bull 
Entomol Soc Am 15: 237– 240 
McIntosh P, Barrett LT, Warren-Myers F, Coates A and 
others (2022) Supersizing salmon farms in the coastal 
zone: a global analysis of changes in farm technology and 
location from 2005 to 2020. Aquaculture 553: 738046  
Mennerat A, Nilsen F, Ebert D, Skorping A (2010) Intensive 
farming: evolutionary implications for parasites and patho-
gens. Evol Biol 37: 59– 67  
Ministry of Trade, Industry and Fisheries (2008) Forskrift om 
drift av akvakulturanlegg (akvakulturdriftsforskriften) 
(in Norwegian). Norway; Regulation no. FOR-2017-03-
06-275  
Ministry of Trade, Industry and Fisheries (2010) Forskrift om 
sone for å forebygge og bekjempe lus i akvakulturanlegg 
i kommunene Os, Samnanger, Fusa, Tysnes, Austevoll, 
Kvinnherad, Jondal, Kvam, Fitjar, Stord, Bømlo, Sveio, 
Vindafjord og Etne kommuner, Hordaland og Rogaland 
(in Norwegian). Norway; decommissioned in 2014, Regu-
lation no. FOR-2010-07-14-1123 
Ministry of Trade, Industry and Fisheries (2012) Forskrift om 
bekjempelse av lakselus i akvakulturanlegg (=Regula-
tion on the control of salmon lice in aquaculture) (in Nor-
wegian). Norway; Regulation no. FOR-2017-03-06-275 
Ministry of Trade, Industry and Fisheries (2015) Forutsigbar 
og miljømessig bærekraftig vekst i norsk lakse- og ørre-
toppdrett (in Norwegian). Norway; Meld. St. 16 
Ministry of Trade, Industry and Fisheries (2017) Forskrift om 
produksjonsområder for akvakultur av matfisk i sjø av laks, 
ørret og regnbueørret (produksjonsområdeforskriften)(in 
Norwegian). Norway; Regulation no. FOR-2017-01-16-61  
Myksvoll MS, Sandvik AD, Albretsen J, Asplin L and others 
(2018) Evaluation of a national operational salmon lice 
monitoring system — from physics to fish. PLOS ONE 13: 
e0201338  
Oliveira VHS, Dean KR, Qviller L, Kirkeby C, Bang Jensen B 
(2021) Factors associated with baseline mortality in Nor-
wegian Atlantic salmon farming. Sci Rep 11: 14702 
Overton K, Dempster T, Oppedal F, Kristiansen TS, Gismer-
vik K, Stien LH (2019) Salmon lice treatments and salmon 
mortality in Norwegian aquaculture: a review. Rev Aqua-
cult 11: 1398– 1417  
Pike AW, Wadsworth SL (1999) Sealice on salmonids: their 
biology and control. Adv Parasitol 44: 233– 337  
R Development Core Team (2017) R: a language and envi-
ronment for statistical computing. R Foundation for Sta-
tistical Computing, Vienna 
Salama NKG, Murray A (2012) Fish farm size and surround-
ing water current speed dictate the separation required 
to avoid transmission of disease agents between produc-
tion sites. Proc SVEPM Meeting, Glasgow, 28–30 March 
68


<!-- page 11 -->
Qviller et al.: Biomass redistribution reduces salmon lice infestations
2012. Society for Veterinary Epidemiology and Preven-
tive Medicine (SVEPM), Glasgow, p 28– 30 
Samsing F, Johnsen I, Dempster T, Oppedal F, Treml EA 
(2017) Network analysis reveals strong seasonality in the 
dispersal of a marine parasite and identifies areas for 
coordinated management. Landsc Ecol 32: 1953– 1967  
Samsing F, Johnsen I, Treml EA, Dempster T (2019) Identify-
ing ‘firebreaks’ to fragment dispersal networks of a mar-
ine parasite. Int J Parasitol 49: 277– 286  
Sandvik AD, Bjørn PA, Ådlandsvik B, Asplin L and others 
(2016) Toward a model-based prediction system for sal-
mon lice infestation pressure. Aquacult Environ Interact 
8: 527– 542  
Sandvik AD, Johnsen IA, Myksvoll MS, Sævik PN, Skogen 
MD (2020) Prediction of the salmon lice infestation pres-
sure in a Norwegian fjord. ICES J Mar Sci 77: 746– 756  
Sandvik AD, Bui S, Huserbråten M, Karlsen Ø, Myksvoll MS, 
Ådlandsvik B, Johnsen IA (2021) The development of a 
sustainability assessment indicator and its response to 
management changes as derived from salmon lice dis-
persal modelling. ICES J Mar Sci 78: 1781– 1792 
Stige LC, Helgesen KO, Viljugrein H, Qviller L (2021) A 
statistical mechanistic approach including temperature 
and salinity effects to improve salmon lice modelling of 
infestation pressure. Aquacult Environ Interact 13: 
339– 361  
Sviland Walde C, Bang Jensen B, Pettersen JM, Stormoen M 
(2021) Estimating cage-level mortality distributions fol-
lowing different delousing treatments of Atlantic salmon 
(Salmo salar) in Norway. J Fish Dis 44: 899– 912 
Taranger GL, Karlsen Ø, Bannister RJ, Glover KA and others 
(2015) Risk assessment of the environmental impact of 
Norwegian Atlantic salmon farming. ICES J Mar Sci 72: 
997– 1021  
Tennekes M (2018) tmap: thematic maps in R. J Stat Softw 
84: 1– 39 
Toorians MEM, Adams TP (2020) Critical connectivity thres-
holds and the role of temperature in parasite metapopula-
tions. Ecol Modell 435: 109258 
van Etten J (2017) R package gdistance: distances and routes 
on geographical grids. J Stat Softw 76: 22  
Vollset KW, Barlaup BT, Friedland KD (2019) Context-
dependent impact of an ectoparasite on early marine 
growth in Atlantic salmon. Aquaculture 507: 266– 274
69
Editorial responsibility: Kate S. Hutson,  
Nelson, New Zealand 
Reviewed by: T. Ben-Horin and 2 anonymous referees
Submitted: April 28, 2023 
Accepted: November 7, 2023 
Proofs received from author(s): February 12, 2024
