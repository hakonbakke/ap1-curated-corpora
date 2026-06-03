AQUACULTURE ENVIRONMENT INTERACTIONS Aquacult Environ Interact

Vol. 14: 263–277, 2022

Published November 17

https://doi.org/10.3354/aei00443

### OPEN ACCESS

# Modelling salmon lice-induced mortality of wild salmon post-smolts is highly sensitive to calibration data

## Leif Christian Stige*, Kari O. Helgesen, Hildegunn Viljugrein, Lars Qviller

Norwegian Veterinary Institute, 1431 Ås, Norway

ABSTRACT: Salmon lice from fish farms in open net pens pose a threat to the survival of wild salmon post-smolts migrating through areas with high farm and lice densities. Reliable estimation of this mortality is fundamental for the sustainable management of aquaculture in such areas but is challenged by considerable uncertainty about several of the processes that link reported lice numbers in fish farms to post-smolt mortality. Utilising recent access to lice data from post-smolt trawling, we revised a virtual post-smolt model that estimates salmon lice-induced mortality of seaward-migrating wild salmon post-smolts. We also assessed the sensitivity of model results to model assumptions that differ among the virtual post-smolt models currently being used as management support in Norway. The spatiotemporal variation in infestation pressure along the entire Norwegian coast was calculated based on monitoring data for salmon lice, temperature and fish abundance in all Norwegian salmonid farm locations. The revised model integrates lice data from sentinel cage experiments and post-smolt trawling to quantify the spatiotemporal variation in infestation rate of wild post-smolts from the spatiotemporal infestation pressure, while also estimating the effect of calibration data type on infestation rate. Results show 10 times higher infestation rate in trawl-caught post-smolts than in post-smolts from sentinel cage experiments. Mortality estimates calibrated to trawl data are more sensitive to assumptions about possible density dependence in lice infestation rate than to assumptions about migration speed. These findings contribute to explaining why different virtual post-smolt models provide different estimates of salmon lice-induced mortality.

KEY WORDS: Virtual post-smolt modelling · Lepeophtheirus salmonis · Salmo salar · Mortality · Sensitivity analysis

##### 1. INTRODUCTION

The salmon louse Lepeophtheirus salmonis is an ectoparasite on salmonids that disperses between hosts during planktonic larval stages (Pike & Wadsworth 1999, Brooker et al. 2018). Control of salmon lice is currently one of the biggest challenges to the sustainable farming of salmonids in open net pens (Taranger et al. 2015). Salmon lice may de crease the welfare, growth and survival of the farmed fish, with corresponding impacts on wild salmonids likely

*Corresponding author: leif.christian.stige@vetinst.no

affecting observed return rates (Vollset et al. 2018). Controversies exist, however, about how large the effects of farm-origin salmon lice are on wild populations of salmonids. Quantification of these effects is difficult because the relevant observation data are typically noisy and incomplete, there is individual host heterogeneity in lice infestation and the natural variability in population dynamics of lice and fish is large. Accordingly, our knowledge and models of infestation dynamics are hampered by large variation and uncertainty.

© The authors 2022. Open Access under Creative Commons by Attribution Licence. Use, distribution and reproduction are unrestricted. Authors and original publication must be credited.

Publisher: Inter-Research · www.int-res.com

Accurate assessment of salmon lice-induced mortality of seaward-migrating post-smolts of wild Atlantic salmon Salmo salar in Norway is of considerable ecological, societal and economic consequence. Norway is the largest producer of Atlantic salmon and one of the largest producers of rainbow trout Oncorhynchus mykiss in the world (FAO 2019). The political ambition is to increase production further, conditional on such growth being environmentally sustainable (Ministry of Trade, Industry and Fisheries 2015). The environmental indicator used to regulate whether to increase, maintain or reduce production in different areas along the coast is the estimated detrimental effect that salmon lice from fish farms has on wild salmonids, with a main focus on the mortality of seaward-migrating wild salmon post-smolts. In this management system—the socalled traffic light system—the Norwegian coast is divided into 13 management areas (MAs). For each area, the salmon lice-induced mortality of seawardmigrating wild salmon post-smolts is assessed annually by an expert group (e.g. Vollset et al. 2021b). Every second year, the Ministry of Trade, Industry and Fisheries decides production limits for salmonid aquaculture, taking into account the impact of farmorigin salmon lice on seaward-migrating wild salmon. According to a control rule implemented in 2017, the impact is considered to be low if salmon lice-induced mortality is less than 10%, moderate if the salmon lice-induced mortality is between 10 and 30% and high if the salmon lice-induced mortality is above 30% (Ministry of Trade, Industry and Fisheries 2015). MAs with low, moderate and high impact are termed, respectively, ‘green’, ‘yellow’ and ‘red’. Green areas may be allowed to increase production by 6%, yellow areas to maintain production at an unchanged level and red areas may be required to reduce production by 6%.

The assessment of salmon lice-induced mortality by the expert group is based on a combination of observation data and models (Vollset et al. 2021b). Two of the observation data sets are trawl data and sentinel cage data. The most direct observation data on salmon lice abundance on seaward-migrating post-smolts are obtained by counting lice on salmon post-smolts caught by trawling in coastal areas (Johnsen et al. 2021b). A limitation of these data is that the exposure history is uncertain, as the migration route and time of entry to the sea are unknown. A complementary observation data set is obtained by counting lice on cultured salmon post-smolts placed in sentinel cages (Sandvik et al. 2020). An advantage of the sentinel cage data is that the time and location

of exposure are known. However, it is uncertain how well lice counts on fish in stationary cages represent lice infestations on actively swimming fish. These observation data sets are also used to calibrate ‘virtual post-smolt’ models, which extrapolate from the observations to the scale of whole MAs and the entire seaward migration period of salmon post-smolts.

In the virtual post-smolt models, salmon lice infestation on seaward-migrating post-smolts is simulated by calculating the spatiotemporal distribution of salmon lice larvae and the resulting infestations on virtual post-smolts that swim from the mouth of each salmon-producing river to the open sea, based on assumptions about migration time, route, speed etc. (Kristoffersen et al. 2018, Myksvoll et al. 2018, Johnsen et al. 2021b, Stige et al. 2021). Salmon liceinduced mortality is calculated as a function of the simulated lice concentrations and summed up for each river and MA. Key input data for calculating the spatiotemporal distribution of lice larvae are weekly resolved monitoring data on temperature and the number of adult female salmon lice per fish from all salmonid fish farms in Norway (Ministry of Trade, Industry and Fisheries 2012). Together with reported numbers of farmed fish and knowledge of lice biology, these data allow estimation of the production of salmon lice eggs and larvae from the farms and, subsequently, the development and dispersion of salmon lice larvae and the spatiotemporal variation in infestation pressure along the entire Norwegian coast. To estimate the relationship between infestation pressure and infestation rate on salmon post-smolts, the calculated infestation pressure is either calibrated to lice counts on salmon post-smolts from sentinel cages (Kristoffersen et al. 2018, Stige et al. 2021) or trawls (Johnsen et al. 2021b).

The results of 3 different virtual post-smolt models are considered by the expert group (e.g. Vollset et al. 2021b); one from the Institute of Marine Research (IMR) (Johnsen et al. 2021b), one from the Norwegian Veterinary Institute (NVI) (Kristoffersen et al. 2018, Stige et al. 2021) and one from the independent research organisation SINTEF (Ellingsen 2021). The different models use the same input data to calculate infestation pressure but different calibration data (IMR’s model: trawl data, NVI’s and SINTEF’s models: sentinel cage data) and make different assumptions about e.g. post-smolt migration speed (IMR: around 12 km d−1; NVI: 7 km d−1; SINTEF: not reported) and the relationship between infestation pressure and infestation rate (IMR and SINTEF: constant, NVI: per-lice infestation rate decreases with lice density). Furthermore, model structure differs,

with e.g. the dispersion of salmon lice larvae either being simulated using a hydrodynamic model component (IMR and SINTEF models) or by a diffusive process estimated from long-term observations (NVI model). Interpretation of model results is complicated by systematic differences between models in calculated mortality levels, with the virtual post-smolt model from IMR often predicting higher mortality than the virtual post-smolt models from NVI and SINTEF (e.g. Vollset et al. 2021b). The causes of these differences are not completely understood, as the sensitivity to model-specific assumptions is incompletely known. As pointed out in an international evaluation of the traffic light management system, it is critical to demonstrate the sensitivity of modelled outputs to shifts around assumptions made about uncertain parameters (Eliasen et al. 2021).

Here, we aimed to improve the NVI virtual postsmolt model (Kristoffersen et al. 2018, Stige et al. 2021) by integrating data from both sentinel cages and post-smolt trawling. Hence, we used both cage and trawl data to quantify how infestation rate varies with infestation pressure and among MAs and years. Furthermore, we aimed to investigate the sensitivity of calculated infestation levels and mortality to 3 model assumptions that differ among models. We did so by considering the implications of 2 alternative modelling choices for each of 3 assumptions in the NVI model (Table 1): (A1) use of trawl or sentinel cage data for calibration, (A2) migration speed of seaward-migrating salmon and (A3) the relationship between infestation pressure and infestation rate. Testing assumption A1 (trawl or cage) is now possible because of recent access to trawl data with genetically assigned river of origin. The knowledge base for assumption A2 (speed) is uncertain, as post-smolt migration speed has been found to vary considerably among sites, years and groups of fish (Thorstad et al. 2012). Recent studies from Norwegian coastal waters have found progression rates of around 9 km d−1 (Vollset et al. 2016) and 12 km d−1 (Halttunen et al.

2018), but as high as 24 km d−1 for one fjord (Jensen et al. 2022). As an alternative to the previously assumed migration speed of 7 km d−1 in the NVI model, we considered 10 km d−1. Assumption A3 (density) was tested by either statistically estimating the slope of the relationship between log-scale infestation pressure experienced by the fish and log-scale expected lice abundance (as in previous versions of the NVI model; Kristoffersen et al. 2018) or fixing this slope at 1 (as in the IMR and SINTEF models). Fixing the slope to 1 meant that a proportional change in infestation pressure (e.g. a doubling) was constrained to lead to the same proportional change in expected lice abundance. The slope can also be interpreted in terms of the relationship between infestation pressure and per-lice infestation rate, i.e. the proportion of infective larvae attaching to a host. A slope of 1 implies a constant infestation rate while a slope between 0 and 1 implies decreasing infestation rate with increasing infestation pressure.

##### 2. MATERIALS AND METHODS

##### 2.1. Farm data

Extensive monitoring data from the aquaculture industry provided information about the spatiotemporal variation in the production of newly hatched salmon lice of farm origin. Farmed salmonids contribute around 98% of mated (ovigerous) female salmon lice in Norwegian coastal waters (Dempster et al. 2021). All active marine salmonid farms in Norway are required to count and report salmon lice infestations and also to report farm numbers of fish, the geographic coordinates of the farm and water temperature at 3 m depth (as described by Jansen et al. 2012, Kristoffersen et al. 2014). We used data from January 2012 to December 2021, comprising on average 636 active salmonid (Atlantic salmon and rainbow trout) farms at any given time (Fig. 1). The lice

- Table 1. Alternative model assumptions. For each of the assumptions A1 to A3, salmon lice infestation level and salmon liceinduced mortality were calculated in accordance with either the modelling choice from the previous version of the Norwegian


Veterinary Institute (NVI) model or an alternative

|Assumption Description Previous NVI model Alternative<br><br>A1 (trawl or cage) Calibrate infestation rate to lice levels for fish from trawling Sentinel cage data Trawl dataa or sentinel cages<br>A2 (speed) Post-smolt migration speed 7 km d−1 10 km d−1a<br>A3 (density) Relationship between per-lice infestation rate and lice density Estimated from the dataa Constant aModel setting for ‘main model’ as defined in Sections 2.9 and 3.1<br>|
|---|


- 58°N
- 59°N
- 60°N
- 61°N
- 62°N
- 63°N
- 64°N
- 65°N
- 66°N
- 67°N
- 68°N
- 69°N
- 70°N
- 71°N


MA 12 MA 13

MA 11

MA 10

MA 9

MA 8

MA 7

|MA 6|
|---|


MA 5

- MA 1
- MA 2
- MA 3
- MA 4


5°E 10°E 15°E 20°E 25°E 30°E

Fig. 1. Study area on the Norwegian coast, divided into 13 management areas (MA 1 to MA 13). Black dots: active salmonid farms in the period 2012–2021; red crosses: locations of sentinel cage experiments; blue crosses: mid-points of post-smolt trawl hauls

and temperature data have weekly resolution and are publicly available at the ‘BarentsWatch’ portal (https://www.barentswatch.no/fiskehelse/). The salmonid production data have monthly resolution and are administered by the Directorate of Fisheries. The monthly and weekly data were matched and converted to a daily time scale as described by Kristoffersen et al. (2018).

##### 2.2. Sentinel cage data

Counts of salmon lice on salmon post-smolts placed in sentinel cages along the Norwegian coast (Fig. 1) provided information about the spatiotemporal variation in infestation rates. Each year from 2012−2021, between 49 and 206 (mean 105) sentinel cages were placed in the sea for periods of between 6 and 30 d (mean: 16 d) during May–August (see Bjørn et al. 2011, Sandvik et al. 2020 for information about experimental setup). The cages were 0.8 m in diame-

ter, 0.9 m high and deployed at 0.5 m depth. Each cage contained around 25 farm-reared salmon postsmolts that were louse-free at the start of the experiments. We used data on total salmon lice abundance (all parasitic stages) per fish at the end of the experiments, for a total of 26697 fish from 1048 sentinel cages. The data represented 37 combinations of year and aquaculture MA (among MAs 2–7 and 12). These data are publicly available through the Norwegian Marine Data Centre (see Table S1 in the Supplement at www.int-res.com/articles/suppl/q014 p263_supp.pdf for references; data for 2019−2021 provided by Ø. Karlsen, IMR, pers. comm.).

##### 2.3. Trawl data

Seaward-migrating wild salmon post-smolts were collected during dedicated post-smolt surveys by IMR from 2017−2021 as described by Johnsen et al. (2021b). Surveys were performed in the outer parts

of fjords in 4 aquaculture MAs (MAs 2–5) in calendar weeks 18–23. We included data on wild salmon postsmolts up to 50 g in size where the river of origin had been assigned with an assignment probability higher than 0.80 (Harvey et al. 2019). The analysed data included a total of 3502 fish from 555 trawl hauls assigned to 49 rivers of origin. The data represented 22 combinations of year and aquaculture MA, 14 of which were also covered by sentinel cage data. Trawl data with genetic assignment were provided by Ø. Karlsen, IMR (pers. comm.).

##### 2.4. Modelling outline

The purpose of the virtual post-smolt model is to assess how salmon lice from salmonid farms influence the survival of wild salmon post-smolts. The model calculates the spatiotemporal variation in salmon lice infestation pressure along the Norwegian coast (Kristoffersen et al. 2014) and simulates the resulting lice infestations and lice-induced mortality of seaward-migrating salmon post-smolts (Kristoffersen et al. 2018). A set of possible model updates based on new empirical studies of lice dynamics was tested by Stige et al. (2021). Here, we incorporated the model updates that Stige et al. (2021) found to improve predictions of salmon lice infestations in sentinel cage experiments. Specifically, we took into account temperature-dependent egg batch size, temperature-dependent egg viability and temperaturedependent infectivity and used updated functions for temperature-dependent larval development time and how infestation pressure decreases with distance from each farm releasing larvae. We further calculated infestation pressure as weekly mean concentrations of infective larvae instead of as weekly production of infective larvae (Stige et al. 2021). Sections 2.5−2.9 provide a more detailed description of the modelling.

##### 2.5. Calculating spatiotemporal variation in infestation pressure

This section describes how spatiotemporal variation in infestation pressure was calculated from farmreported fish abundance, lice abundance and temperature data. Infestation pressure represents the weekly mean concentration of infective larvae at 100 × 100 m resolution.

The daily concentration of infective salmon lice larvae at a geographic position i and time T, termed IPi,T, was calculated by summing the product of egg

production, successful development, survival, dispersal and infectivity across all potentially contributing farms j = 1,..., nj and daily time steps t = t0,...,T, with t0 = 1 January 2012:

nj

T

(N jE,t sj,t,T ri,j Ii,j)

IPi,T =

(1)

j=1

t=t0

Specifically, is the number of salmon lice eggs produced from fish at farm j and day t, sj,t,T is the fraction of these eggs that developed into the infective larval stage and survive to time T, ri,j is the probability of dispersal of larvae from farm j to location i and Ii,j is a factor that controls for temperature-dependent infectivity of the larvae. The calculation of each of these components of infestation pressure is described in Text S1.

N jE,t

##### 2.6. Calculating infestation pressure for fish in sentinel cages and trawl catches

This section describes how we calculated infestation pressure for the salmon post-smolts used to calibrate the model. For each sentinel cage experiment, we used the average infestation pressure for the geographic position and time period of the experiment. For each trawl haul, only start and end locations were recorded. We assumed that the trawl path followed the shortest possible sea route from the start to the end location of the trawl haul and that the fish were sampled at the mid-point of the trawl haul. We further assumed that the fish swam the shortest possible route from the river mouth to the mid-point of the trawl haul at a speed of either 7 or 10 km d−1 (depending on assumption A2). The infestation pressure along the route was sampled every 100 m from the weekly infestation pressure fields. For each fish, we calculated mean infestation pressure and days at sea. The shortest sea routes were found using the ‘shortestPath’ function in the ‘gdistance’ library version 1.3.6 (van Etten 2017) of R version 4.03 (R Core Team 2020) using a raster sea map with 100 m resolution. To sample point locations on spatial lines at regular intervals, we used the ‘spsample’ function in the ‘sp’ library version 1.4-5 (Bivand et al. 2013).

##### 2.7. Estimating the relationship between infestation pressure and lice load

This section describes the statistical model used to relate infestation pressure to lice load, termed the ‘infestation model’. Data from trawl catches and sen-

tinel cages were analysed in one statistical model. Specifically, a mixed-effects model with a negative binomial error structure analysed salmon lice counts on salmon post-smolts as a function of infestation pressure:

NkObs,i,T' ~ exp( 0+ 1ln(IPi, T )+ 2Cagedata + ln(Durationi,T')+bi,T'

(2)

Here, refers to observed counts of salmon lice on fish k in a sentinel cage experiment or trawl haul at position i and time T'. The coefficient β0 is the intercept and represents the daily infestation rate for trawl data at low infestation pressure (at IP = 1). The coefficient β1 quantifies the relationship between log-scale expected lice abundance on post-smolts and log-scale infestation pressure. Dependent on assumption A3, we either estimated β1 from the data or used a fixed slope of β1 = 1. The fixed slope was modelled by setting the term ln(IPi,T') as an offset variable. The exponent of the coefficient β2 is the proportional change in infestation rate between trawl and sentinel cage data, with ‘Cagedata’ being an indicator variable with a value of 0 for trawl samples and 1 for cage samples. The offset variable ‘Duration’ (days) is exposure duration, measured as the duration of the sentinel cage experiment or the calculated number of days from the river mouth to the trawl location for trawl data. The random effect bi,T is a random effect of the combination of MA and year. The area−year effect captures variation in lice abundance between MAs and years through factors other than the calculated infestation pressure. We assumed that the random effect of area−year was normally distributed with a mean zero and standard deviation σ. The shape of the negative binomial distribution depends on the estimated dispersion parameter θ, and the variance is μ + μ2/θ, where μ is the mean.

NkObs,i,T'

##### 2.8. Simulating lice load and mortality of wild salmon post-smolts from all rivers

Following Kristoffersen et al. (2018), we simulated salmon lice-induced mortality for each of 401 salmonproducing rivers in Norway. For each river, we assumed that salmon post-smolts followed the shortest sea route from the river mouth to the open sea, 12 nautical miles from the base line (Kristoffersen et al. 2018). The infestation pressure along the route was sampled from the weekly raster maps at a fixed interval of 100 m. This approach facilitated more accurate simulation of swimming speed than if we had

sampled all pixels crossed by the route (as done by Kristoffersen et al. 2018).

For each river, we simulated the seaward migration of virtual post-smolts for 3 alternative starting dates and calculated mean infestation pressure and days to open sea (with a swimming speed of 7 or 10 km d−1 dependent on assumption A2). The 3 alternative starting dates represented the start, median and end dates of the period when post-smolts from the given river reach the sea. The migration time for each river followed Vollset et al. (2021a), who estimated the date of 25% migration as a function of latitude, longitude, temperature and river discharge. Here, we used river-specific average dates for 2014–2018, the last 5 yr predicted by Vollset et al. (2021a). The start and end dates were assumed to be, respectively, 10 d before and 30 d after the date of 25% migration. The median day of year (D50) was based on the statistical relationship between D50 and the day of year of 25% migration (D25): D50 = 10.836 + 0.967 D25 (K. Vollset pers. comm.).

The distribution of salmon lice between fish was assumed to follow a negative binomial distribution with parameters from Eq. (2) and with mean infestation pressure and duration of exposure dependent on river, migration date and swimming speed. For each river, we simulated salmon lice numbers on 105 fish at start, median and end dates of migration by randomly drawing from the negative binomial model (following Kristoffersen et al. 2018). The parameter values of this model (i.e. the values of β0, β1, β2, σ, θ) depended on assumptions A2 (speed) and A3 (density). Depending on model assumption A1 (trawl or cage), we either set the ‘Cagedata’ variable to 0, meaning that the simulated infestation level was calibrated to trawl data, or 1, meaning that the simulated infestation level was calibrated to cage data.

Only around 20% of the salmon lice in the sentinel cage data and 3% in the trawl data had reached the mobile pre-adult and adult stages that are most detrimental to the host fish. Based on findings from experimental studies that around 30–50% of the lice die or fall off between chalimus and pre-adult molts (Stien et al. 2005, Wagner et al. 2008), we adjusted the simulated lice numbers by multiplying the expected value of the negative binomial distribution by 0.6 before calculating salmon lice-induced mortality. This adjustment is equivalent to applying a random draw where each louse has a probability of 0.4 that it will die before harming the host. Although there is uncertainty associated with this correction, we did not conduct a sensitivity analysis because of the direct relationship with lice abundance.

Stige et al.: Modelling salmon lice-induced mortality 269

Mean mortality for fish at start, median and end dates of migration was calculated by assuming zero mortality for fish with 0–1 lice, 20% mortality for fish with 2–3 lice, 50% mortality for fish with 4–6 lice and 100% mortality for fish with more than 6 lice (Kristoffersen et al. 2018, Johnsen et al. 2021b). This mortality scheme was based on an assumption that small (here, 20 g) salmon post-smolts will suffer 100% licerelated marine mortality in the wild if they are infected with more than 0.3 lice per gram fish weight (Taranger et al. 2015). Mean mortality for all fish was calculated from the mortality at start, median and end dates by assuming that the migration dates for each river followed a beta-PERT distribution with lambda parameter 4 (hence distributing the fish between start and end dates with a peak at the median date) and assuming that mortality changed linearly between start and median dates and between median and end dates of migration (see Kristoffersen et al. 2018 for details). Mortality was aggregated to the MA level by calculating the average of the river-specific mortality estimates for each MA and year (with the same weight given to all salmonproducing rivers in the MA).

We also calculated worst- and best-case scenarios representing 90% intervals around the expected mortality. To do so, we subtracted or added 1.64 standard deviations of the estimated random area−year variation (σ of b, Eq. 2) when simulating the dynamics, giving the 5th and 95th percentiles of the empirical variation in lice abundance for a given infestation pressure (Kristoffersen et al. 2018). For MAs and years represented in the calibration data set, we also calculated salmon lice-induced mortality by including the random effect for the given MA and year (bi,T', Eq. 2) when simulating the dynamics.

##### 2.9. Model evaluation

We fitted alternative versions of the infestation model (Eq. 2) dependent on assumptions A2 (speed) and A3 (density). These alternative models were compared based on Akaike’s information criterion (AIC). AIC is a measure of model quality that seeks the optimal trade-off between goodness-of-fit and model parsimony, where a model with a lower AIC value is considered better than a model with a higher AIC value (Akaike 1974). This model comparison assessed which of assumptions A2 and A3 was best supported by the trawl and cage data. Furthermore, by analysing the trawl and cage data in one statistical model, we quantified the effect of assumption A1 (trawl or cage)

on the calculated infestation rate (given by the model parameter β2). To assess how sensitive the mortality calculation was to the assumptions, we calculated salmon lice-induced mortality for each MA and year with alternative model assumptions A1 to A3. As a baseline for these comparisons, we considered the infestation model with the lowest AIC (termed the ‘main model’) calibrated to trawl data and then changed one assumption at a time.

To quantify how well the model explained the observed variation in salmon lice infestations, we compared mean lice abundance in each sentinel cage experiment or trawl haul with mean lice abundance predicted from the model. We also compared mean observed and predicted salmon lice abundance at the MA−year level. The predictions were made for the time and locations of the observations in each data set (sentinel cage or trawl) and without including the random area−year effect. We also compared mean mortality per MA and year calculated directly from the sentinel cage or trawl data with mean mortality calculated from the predicted abundances. The same scheme for calculating salmon lice-induced mortality from lice numbers was used for observation data as for simulated data.

##### 3. RESULTS

##### 3.1. Infestation model

The infestation model estimated the infestation rate, that is, the ratio between the expected lice abundance on salmon post-smolts and the calculated infestation pressure in the sea. The model formulation with the lowest AIC value assumed a migration speed of 10 km d−1 (assumption A2) and estimated the slope of the relationship between log-scale infestation pressure and log-scale expected lice abundance from the data (assumption A3; Table 2). We hereafter term this model formulation the ‘main model’.

Assuming a migration speed of 7 km d−1 increased the AIC by 2.8, meaning that this model is about 25% as likely as the main model (as represented by the ratio of Akaike weights; Wagenmakers & Farrell 2004). Such an assumption hence provided somewhat worse predictions of lice infestations on trawl-caught fish. Note that this assumption was only relevant for predicting lice infestations on trawl-caught fish. For these fish, only the river of origin and the date of capture were known, and the exposure history depended on migration speed. In contrast, for the fish in sentinel cages, the exposure history was known. As-

Table 2. Regression models of lice abundance as a function of infestation pressure. The table gives coefficients (±SE) for the model parameters (Eq. 2). σ: the standard deviation of the random-effect combination of management area and year included in the models; ΔAIC: difference in Akaike’s information criterion from the baseline model. Akaike weights can be interpreted as conditional probabilities for each model (Wagenmakers & Farrell 2004). The alternative models differ from the main model by assuming a post-smolt migration speed of 7 instead of 10 km d−1 (assumption A2) or fixing the slope (β1) to 1 by assuming a constant infestation rate (assumption A3)

|Main model Alternative models 7 km d−1 Fixed slope<br><br>β0: model intercept −5.49 ± 0.17 −5.80 ± 0.17 −11.6 ± 0.22<br>β1: infestation pressure effect 0.425 ± 0.006 0.426 ± 0.006 1<br>β2: cage data effect −2.28 ± 0.03 −1.99 ± 0.03 −3.13 ± 0.04 σ: standard deviation of random effects 0.98 0.98 1.43 θ: negative binomial parameter 0.921 0.921 0.659 ΔAIC: difference in AIC − 2.8 6507 Akaike weight 0.80 0.20 <0.001<br><br><br>|
|---|


suming a migration speed of 7 km d−1 when fitting the infestation model implies a lower infestation rate for a given infestation pressure and exposure duration than assuming a migration speed of 10 km d−1 (compare dashed and unbroken lines in Fig. 2a).

Fixing the slope to 1 increased the AIC by more than 6000, implying that the model fitted the data poorly. Fixing the slope to 1 implies a linear relationship between infestation pressure and lice infestations, while a slope lower than 1, as estimated by the main model, implies a concave relationship (compare dotted and unbroken lines in Fig. 2). The concave relationship found by the main model means that the infestation rate is highest at low infestation pressure, and that a doubling in the calculated infestation pressure leads to less than a doubling in the number of salmon lice on the post-smolts.

The infestation rate on salmon post-smolts in sentinel cages was estimated to be only 10.2% of that on wild-caught post-smolts (exp[β2] of the main model;

- Table 2). That is, for a given infestation pressure, we expect to find 9.8 times as many salmon lice on trawlcaught post-smolts than on post-smolts in sentinel cages. This estimate depends on the migration speed assumed; when we assumed that the trawl-caught fish migrated at 7 km d−1, the estimated infestation rate on trawl-caught fish was 7.3 times higher than for fish in sentinel cages.


##### 3.2. Relationship between fitted and observed lice abundance

Comparing fitted and observed numbers of lice per fish, we found that there was considerable unexplained variation, especially at the level of individual

trawl hauls (grey points in Fig. 3a). The model explained 34% of the variation between MAs and years in lice abundance in both trawl data (crosses in Fig. 3a) and cage data (crosses in Fig. 3b).

##### 3.3. Model-predicted and calculated mortality in sampled fish

Comparing mortality calculated based on lice abundances in the sampled fish with mortality calculated based on the model-predicted lice abundances for the same fish showed considerable unexplained varia-

a. Trawl data

b. Cage data

- 0.8
- 1


14

Meanliceperfish

12

Frequency

10

0.6

8

6

0.4

4

0.2

2

0

0

0 0.5 1 1.5 2

0 0.5 1 1.5 2

Infestation pressure (million larvae)

Fig. 2. Model predictions of mean number of lice per fish and calculated infestation pressure for fish in the (a) trawl and (b) cage data set. Lines (left y-axis scale) show expected number of lice per fish as a function of infestation pressure for an exposure duration of 7 d. Unbroken lines: predictions assuming 10 km d–1 post-smolt migration speed and estimated infestation pressure effect (main model). Dashed line in (a) assumes 7 km d−1 post-smolt migration speed (only relevant for trawl data). Dotted lines: assuming a fixed slope of 1 for the infestation pressure effect. Grey histograms (right y-axis scale) show the frequency distribution of infestation pressure among the fish in each data set

a. Trawl data

b. Cage data

r = 0.41 (0.58)

r = 0.55 (0.58)

Observedliceperfish

128

32

| | |
|---|---|
| | |
| | |


8

| | |
|---|---|
| | |
| | |


2

| | | |
|---|---|---|
| | | |


0

0 2 8 32 128

0 2 8 32 128

Fitted lice per fish

Fig. 3. Fitted and observed number of salmon lice per fish in the (a) trawl and (b) sentinel cage data. Fitted values refer to the main model. Grey circles: mean lice per fish in one sample (trawl haul or sentinel cage experiment); crosses: mean for one management area and year. Pearson’s correlation coefficient (r) between predictions and observations is calculated at the scale log10(x + 1) at the sample level and at the area−year level (numbers in parentheses). Dashed lines show the 1:1 relationship

a. Trawl data

b. Cage data

r = 0.51

r = 0.51

Calculatedmortality

0.8

0.4

0.0

0.0 0.4 0.8

0.0 0.4 0.8

Model−predicted mortality

Fig. 4. Model-predicted and calculated salmon lice-induced mortality in sampled fish in the (a) trawl and (b) sentinel cage data. Mortality is calculated from lice abundances predicted from the main model (x-axes) or from observed lice abundances (y-axes). Crosses: mean for one management area and year; grey areas: 90% intervals for empirical variation around the expected mortality. Pearson’s correlation coefficient (r) between predictions and observations is given; N = 22 in (a), N = 37 in (b). Dashed lines: 1:1 relationship

tion (Fig. 4). This variation was reflected in broad 90% intervals for the empirical variation around the expected mortality (grey areas in Fig. 4). The model explained 25–26% of the variation between MAs and years in mortality calculated from lice abundances in trawl data (Fig. 4a) and cage data (Fig. 4b).

##### 3.4. Mortality of simulated seaward-migrating salmon post-smolts

The lowest salmon lice-induced mortality was estimated for MAs 1 and 13. Here, both the expected mortality estimated by the main model calibrated to trawl data (blue circles in Fig. 5) and the 90% intervals for the empirical variation around the expected mortality (grey-shaded polygons in Fig. 5) were well within the 0–10% mortality range for all years. The expected mortality in MAs 10–12 was also in the 0–10% range, but the 90% intervals went into the 10–30% range for MAs 11 and 12 and above 30% for recent years in MA 10. The expected mortality in each of MAs 5–9 in recent years has varied between being in the 0–10% range and the 10–30% range, with the 90% intervals often extending above 30% mortality. The expected mortality in MAs 2 and 4 has consistently been in the 10–30% range in recent years, with the 90% intervals spanning from below 10% to above 30% mortality. The expected mortality in MA 3 has been above 30% for all years since 2014, with the lower limit of the 90% interval being around 10% mortality.

For MAs and years with trawl and/or sentinel cage data, we also have mortality estimates that include the random effect of MA and year on infestation rate (crosses in Fig. 5). In contrast to the expected mortality, these estimates adjust to the salmon lice data in the particular MA and year, assuming that the infestation rate for the sampled fish is representative of the entire MA and post-smolt migration period. For MA 4, these estimates tend to be higher than the expected mortality, suggesting that the model tends to underestimate mortality in this area. For other MAs, we see no indications of systematic over- or underestimation.

##### 3.5. Mortality estimated with alternative model assumptions

The mortality estimates calibrated to sentinel cage data were an order of magnitude lower than the mortality estimates calibrated to trawl data (Fig. 6a). Assuming a migration speed of 7 instead of 10 km d−1 had only a minor effect on the mortality estimates (Fig. 6b). Note that this comparison was based on mortality estimates calibrated to trawl data, which assumed the same migration speed when calibrating the infestation model as when simulating the seaward migration from each river. Fixing the slope β1 of the relationship between ln-scale infestation pressure and ln-scale expected lice abundance to 1 led to higher mortality estimates for mortalities higher than around 10% (Fig. 6c).

Salmonlice−inducedmortality(%)

#### 100 MA 1

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |
| | |


80

60

40

20

0

2012 2016 2020

#### 100 MA 6

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |
| | |


80

60

40

20

0

2012 2016 2020

#### 100 MA 11

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |
| | |


80

60

40

20

0

2012 2016 2020

#### 100 MA 2

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |
| | |


80

60

40

20

0

2012 2016 2020

#### 100 MA 7

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |


80

60

40

20

0

2012 2016 2020

#### 100 MA 12

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |


80

60

40

20

0

2012 2016 2020

#### 100 MA 3

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |
| | |


80

60

40

20

0

2012 2016 2020

#### 100 MA 8

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |
| | |


80

60

40

20

0

2012 2016 2020

#### 100 MA 13

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |
| | |


80

60

40

20

0

2012 2016 2020

Year

#### 100 MA 4

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |


80

60

40

20

0

2012 2016 2020

#### 100 MA 9

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |
| | |


80

60

40

20

0

2012 2016 2020

#### 100 MA 5

| | |
|---|---|
| | |
| | |
| | |
| | |


80

60

40

20

0

2012 2016 2020

#### 100 MA 10

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |
| | |


80

60

40

20

0

2012 2016 2020

Fig. 5. Model-predicted salmon liceinduced mortality for seaward-migrating salmon post-smolts for each management area (MA) and year using the main model calibrated to trawl data. Blue circles: expected mortality; grey shading: 90% intervals around the expected values; crosses: mortality, including the random effect of MA and year on infestation rate (when data exist). The right axis and horizontal dashed lines show the mortality thresholds used in the traffic light system

##### 4. DISCUSSION

##### 4.1. Model predictions of salmon lice-induced mortality

The virtual post-smolt model provided yearly estimates of expected salmon lice-induced mortality for all 13 MAs with salmonid production in Norway, with 90% intervals for empirical variation around the expected mortality. For areas and years with observations of lice infestations on salmon post-smolts, the model also provided mortality estimates that included the random area−year effect.

Expected mortality can be interpreted as the longterm mean mortality anticipated for a given infestation pressure, which in turn depends on the reported number and geographic distribution of farmed salmonids, the number of lice per farmed fish and sea temperatures. In most MAs, the random year effects fall on both sides of the expected values, with no indication of systematic over- or underestimation. However, in MA 4, the observed numbers of salmon lice on sampled post-smolts are typically higher than

expected from the model, suggesting that lice infestations may be systematically underestimated by the model. The reason for this possible underestimation in MA 4 is unknown and could be related to e.g. topographic factors or data issues.

The 90% intervals for empirical variation around the expected mortality provide information about how much the salmon lice-induced mortality of salmon post-smolts in a MA varies between years for a given calculated infestation pressure. Several factors contribute to such variation, including spatial and temporal variation in the natural mortality of the planktonic salmon lice larvae (Wootten et al. 1982), inaccuracies in reported lice numbers and environmental data as well as processes that were simplified or not included in the model. Such processes include variable sea currents (Skarðhamar et al. 2018, Huserbråten & Johnsen 2022) and salinity effects on lice dynamics (Tucker et al. 2000, Bricknell et al. 2006, Crosbie et al. 2019). More realistic representation of spatial connectivity by incorporating results from hydrodynamic models could potentially explain some of the temporal and spatial variability in lice infesta-

a. Cage data

b. Migration 7 km d–1

c. Fixed slope

100

alternativeassumptions

80

Mortality(%)with

60

40

20

0

0 20 40 60 80 100

0 20 40 60 80 100

0 20 40 60 80 100

Mortality (%) calculated from main model calibrated to trawl data

Fig. 6. Sensitivity of salmon lice-induced mortality predictions to alternative model assumptions. The x-axis in each panel shows the salmon lice-induced mortality for each management area (MA) and year calculated by the main model calibrated to trawl data (as in Fig. 5). This model assumes a migration speed of the seaward-migrating post-smolts of 10 km d−1 and estimates the slope (β1) of the relationship between ln-scale infestation pressure and ln-scale expected lice abundance from the data. The y-axis in each panel shows mortality calculated using alternative assumptions: (a) calibrating the model to cage data, (b) assuming a migration speed of 7 km d−1 or (c) fixing β1 to 1. Diagonal lines show the 1:1 relationship

tions, especially at small spatiotemporal scales. Including more processes in the model will, however, not necessarily result in more accurate model predictions, as illustrated by similar correspondence between model and data for our model and a more complex virtual post-smolt model (compare, for example, our Fig. 3a with Fig. 3 in Johnsen et al. 2021a). Furthermore, accounting for salinity effects on salmon lice survival and infectivity failed to improve the predictive power of the model (Stige et al. 2021). Although future model improvements may potentially increase the explanatory power of the model, a large part of the unexplained variation is likely to reflect natural variability. Natural variability can be difficult to predict and is outside of human control, in contrast to the expected mortality, which can be directly impacted by management interventions.

The model results nonetheless show large-scale geographic patterns in salmon lice-induced mortality. In areas with low mortality, the 90% intervals for the empirical variation around the expected mortality are relatively narrow, meaning that mortality is predictably low with little variation between years. In areas with high mortality, the variability between years is higher, with mortality in some cases varying from below 10% (i.e. the lowest category in the traffic light system) to above 30% (the highest category). This asymmetry is not surprising; areas with the lowest salmon lice-induced mortality have low farming intensity and low production of salmon lice larvae, which excludes the possibility of high infestation levels. In contrast, a number of biological and physical

factors can potentially cause low infestation levels despite high production of salmon lice larvae.

The mortality estimates that include the random area−year effects (crosses in Fig. 5) integrate the empirical information for each MA and year, including information from trawl hauls and sentinel cage experiments. While the expected mortality can be interpreted as the long-term mean, these values adjust the expected mortality based on the observed lice levels on post-smolts sampled in the MA for a particular year. Specifically, the infestation rate for the simulated seaward-migrating post-smolts is adjusted to the infestation rate for the sampled post-smolts for the area and year. This adjustment can be interpreted in terms of anomalies in lice larval survival and infestation rates. These values need to be interpreted in light of how representative the sampling is for the entire MA and migration period. For MAs and years with low sampling coverage, sampling variability may be large and the adjustments to the sampling data uncertain.

##### 4.2. Sensitivity to type of calibration data

The results suggested 10 times higher infestation rate on trawl-caught wild salmon post-smolts than on post-smolts in sentinel cages and an order of magnitude higher mortality estimates when the model was calibrated to trawl data rather than sentinel cage data. The trawl catches sample the seaward-migrating post-smolts we want mortality estimates for and are therefore the most direct data source. Therefore,

it seems more parsimonious to assume that cage data underestimate than that trawl data overestimate infestation rates on wild post-smolts. It is, however, conceivable that the trawl data overestimate lice infestations if lice-infested fish are overrepresented in the catches because of lower swimming speeds (Wagner et al. 2003, 2008, Bui et al. 2016) and hypothetically aberrant migration routes and schooling behaviour. Furthermore, migration speed typically varies considerably among individuals (Thorstad et al. 2012, Vollset et al. 2016, Halttunen et al. 2018). This variation may lead to an overestimation of population-level infestation rate, also if the lice are not the cause of the slow progression of some individuals. This is because post-smolts that stay in coastal waters for a long time are likely to be overrepresented in trawl catches and also to accumulate high lice loads. On the other hand, loss of salmon lice in the trawl may lead to underestimation. Lice levels are comparable, however, between post-smolts protected in a fish lift attached to the cod end of the trawl and post-smolts outside of the fish lift (Vollset et al. 2021b), suggesting that this is not a large problem.

Sentinel cage data may underestimate lice infestations on seaward-migrating salmon post-smolts for several reasons. Firstly, the cages are stationary and exposure to lice depends on currents, while seawardmigrating post-smolts swim actively and are therefore probably exposed to more lice. The cage walls may restrict the swimming of the post-smolts and the transport of water (and hence lice larvae) through the sentinel cages. The relationship between the swimming speed of the post-smolts and infestation rate is nonlinear, with the highest infestation rate at moderate speed and reduced infestation at low speed because of reduced contact rate with lice larvae (Samsing et al. 2015, Murray & Moriarty 2021). In addition, the fixed depth of the cages may reduce contact between fish and lice. In comparison, by making irregular dives down to 6.5 m depth (Thorstad et al. 2012), wild post-smolts may be exposed to salmon lice if the lice aggregate at a sub-surface halocline (Crosbie et al. 2019). Secondly, it is possible that the high density of fish in the cages reduces the infestation risk of each individual fish compared to post-smolts outside of the cages. The per-individual infestation risk of farmed salmon does appear to be reduced with increasing density of fish (Samsing et al. 2014, van Walraven et al. 2021). However, it is unclear to which degree schooling also dilutes the infestation of wild seaward-migrating post-smolts. Thirdly, the cages may hypothetically obstruct the salmon behaviour used by lice for host detection and

attachment, leading to lower infestation success than on free-swimming hosts. Fourthly, the fish in the cages may lose lice through contact with the cage walls during the experiment or as a result of the handling of the lice at the end of the experiment. Finally, the post-smolts in the sentinel cage experiments, which are of cultured origin, may for some reason be less susceptible to lice infestations than wild post-smolts.

Our results imply that mortality estimates of virtual post-smolt models are highly sensitive to the choice of calibration data type. Based on current knowledge, calibration to trawl data appears most parsimonious as a measure of infestations on seaward-migrating salmon post-smolts, but more information is needed about the representativeness of these data.

##### 4.3. Sensitivity to post-smolt migration speed

Mortality estimates calibrated to trawl data were not very sensitive to assumptions about swimming speed. The reason is that possible over- or underassessment of swimming speed has opposite effects on the calculation of daily infestation rate as on simulated migration duration. Hence, the slightly higher mortality estimated by assuming a migration speed of 7 km d−1 instead of 10 km d−1 was caused by seasonal variation in infestation pressure. Mortality estimates calibrated to sentinel cage data are, on the other hand, highly sensitive to assumptions about swimming speed (results not shown). In that case, assumptions about swimming speed do not influence the calculation of daily infestation rate, whereas migration duration (and hence lice exposure) is inversely proportional to the assumed swimming speed (with, e.g. 43% longer migration duration with a swimming speed of 7 compared to 10 km d−1).

##### 4.4. Sensitivity to assumptions about density dependence

Mortality estimates were somewhat sensitive to assumptions about possible density dependence in infestation rate. In the main model, the infestation rate decreased with increasing infestation pressure, whereas in an alternative model formulation, infestation rate was constant. Decreasing infestation rate with increasing infestation pressure could be caused by compensatory density dependence in lice dynamics through competition among salmon lice for the

best sites on the host fish or by induced immune responses of the fish. Reduced infestation success and survival of salmon lice on salmon at high lice densities has been found at the adult stage of the lice but not at the preadult and chalimus stages that dominate in our data (Ugelvik & Dalvin 2022). Another explanation could be that salmon lice larvae originating from wild salmonids weakened the relationship between spatiotemporal variation in farm-origin infestation pressure and infestation rate in the sea. However, this source of lice larvae appears to be quantitatively unimportant (Dempster et al. 2021). Finally, inaccurate calculation of farm-origin infestation pressure would lead to underestimation of the true effect of farm-origin lice on lice infestations on post-smolts. It is well known that observation noise in a predictor variable in a linear regression model leads to biased estimation of the true relationship between this variable and the response. Such noise could be caused, e.g. by undetected salmon lice due to lice falling off fish when handled, lice not being spotted, or sea-current effects on larval transport. If inaccurate calculation of farm-origin infestation pressure is the main cause of the slope parameter being lower than 1, a model formulation with a fixed slope of 1 would provide more realistic estimates of mortality from farm-origin salmon lice. However, without knowledge about the magnitude of the observation noise, we cannot determine the magnitude of this bias.

##### 4.5. Sensitivity to other factors

The calculation of salmon lice-induced mortality is also sensitive to model assumptions not investigated in the present study. In particular, the lice-induced mortality scheme has a large influence on results (Kristoffersen et al. 2018) and was highlighted as a key uncertainty in a recent evaluation of the scientific basis of the traffic light management system (Eliasen et al. 2021). The mortality scheme is uncertain due to limited data from natural conditions and complications in the use of laboratory-based estimates (Wagner et al. 2008, Taranger et al. 2015). Also, the timing of migration has a large influence on the results, as infestation pressure typically increases during the seaward-migration period, and later migration usually means higher infestation pressure (Kristoffersen et al. 2018). The migration route can also have a large influence, but this influence is reduced by the infestation patterns calculated based on sea distance being relatively smooth and by the

fact that results for each MA are averages across several rivers (Kristoffersen et al. 2018).

##### 4.6. Implications of findings for the traffic light system

The salmon lice-induced mortality predicted by our revised NVI model match quite well with the conclusions from the expert group for the traffic light system (see Text S2 in the Supplement). This correspondence is not surprising given that key data sources and assumptions about mortality thresholds are the same, but suggests that the revised model provides a useful synthesis of central data evaluated by the expert group.

Furthermore, the results contribute towards answering a question that has been raised since the beginning of the work with the traffic light system: Why do the results from different virtual post-smolt models differ? The versions of the NVI model used in the traffic light work before 2022, as well as a virtual post-smolt model from SINTEF, tended to provide lower estimates of salmon lice-induced mortality than a post-smolt model from IMR (Vollset et al. 2021b). Mortality levels calculated by our revised NVI model (i.e. ‘main model’, Table 1) are, however, more similar to the mortality levels calculated by the IMR model. It seems likely that calibration data, which our results show give an order of magnitude difference in mortality estimates, was the main factor behind this systematic difference between models (as also proposed by Johnsen et al. 2021b). The NVI and SINTEF models were calibrated to sentinel cage data and the IMR model to trawl data. The reason for not using trawl data to calibrate the NVI model previously was not that sentinel cage data were considered better than trawl data for this purpose, but that trawl data with river of origin were not available to us. Some of the other factors that differed between models and model versions had opposing effects on mortality estimates. For example, the previous versions of the NVI model assumed slower migration speed than the revised 'main' model (Table 1) and the IMR model. The previous NVI model versions also did not correct for post-attachment mortality of salmon lice. These factors contributed to increased mortality estimates and reduced the difference between the models and model versions. On the other hand, the IMR model assumed a constant infestation rate, which contributed to increased mortality estimates in that model. The different virtual postsmolt models also differ in several other aspects, such

as assumptions about migration routes, temporal distribution of migration and lice larval drift. These factors cause differences between model predictions for particular areas and years but are unlikely to cause substantial systematic differences between the models in the calculated mortality levels.

By systematically investigating the implications of key model assumptions, our results identify high sensitivity to calibration data, lower sensitivity to assumptions about density dependence in infestation rates and low sensitivity to migration speed when using trawl data to calibrate. Results are, however, more sensitive to migration speed when using sentinel cage data for calibration, as in the previous versions of the NVI and SINTEF virtual post-smolt models. To reduce modelling uncertainty, attention should therefore be paid to the representativeness of trawl and sentinel cage data for lice infestations on seawardmigrating post-smolts. Modelling uncertainty can also be reduced by linking the results to independent data sets, in particular by assessing to which degree mortality calculated using different model assumptions is consistent with spatiotemporal variation in salmon return rates. Analyses of salmon return rates would also allow for assessing uncertainty associated with assumptions not investigated in the present study, e.g. regarding the relationship between lice load and lice-induced mortality, but are complicated by the large variability in ocean survival and interaction effects between salmon lice effects and ocean conditions (Vollset et al. 2018, 2019, Vollset 2019).

The results presented here document the sensitivity of post-smolt mortality calculations to model assumptions and data sources, which improve the scientific basis and transparency of the management system. Improving the scientific foundation for the expert group’s future work will indirectly affect decisions on changes in salmonid production made by the government. These decisions are of great financial value for the fish farming companies and great biological value for Atlantic salmon, now red-listed as ‘nearly threatened’ in Norway (Hesthagen et al. 2021).

Acknowledgements. We thank Ørjan Karlsen for providing access to sentinel cage and trawl data on post-smolts.

LITERATURE CITED Akaike H (1974) A new look at the statistical model identifi-

![image 1](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile1.png>)

cation. IEEE Trans Automat Contr 19:716−723 Bivand RS, Pebesma E, Gomez-Rubio V (2013) Applied spatial data analysis with R. Springer, New York, NY Bjørn PA, Sivertsgård R, Finstad B, Nilsen R, Serra-Llinares

![image 2](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile2.png>)

RM, Kristoffersen R (2011) Area protection may reduce salmon louse infection risk to wild salmonids. Aquacult Environ Interact 1:233−244

![image 3](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile3.png>)

Bricknell IR, Dalesman SJ, O’Shea B, Pert CC, Luntz AJM (2006) Effect of environmental salinity on sea lice Lepeophtheirus salmonis settlement success. Dis Aquat Org 71:201−212

![image 4](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile4.png>)

Brooker AJ, Skern-Mauritzen R, Bron JE (2018) Production, mortality, and infectivity of planktonic larval sea lice, Lepeophtheirus salmonis (Kroyer, 1837): current knowledge and implications for epidemiological modelling. ICES J Mar Sci 75:1214−1234

![image 5](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile5.png>)

Bui S, Dempster T, Remen M, Oppedal F (2016) Effect of ectoparasite infestation density and life-history stages on the swimming performance of Atlantic salmon Salmo salar. Aquacult Environ Interact 8:387−395

![image 6](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile6.png>)

Crosbie T, Wright DW, Oppedal F, Johnsen IA, Samsing F, Dempster T (2019) Effects of step salinity gradients on salmon lice larvae behaviour and dispersal. Aquacult Environ Interact 11:181−190

![image 7](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile7.png>)

Dempster T, Overton K, Bui S, Stien LH and others (2021) Farmed salmonids drive the abundance, ecology and evolution of parasitic salmon lice in Norway. Aquacult Environ Interact 13:237−248

Eliasen K, Jackson D, Koed A, Revie C and others (2021) An evaluation of the scientific basis of the traffic light system for Norwegian salmonid aquaculture. Evaluation Committee, The Research Council of Norway, Lysaker

Ellingsen I (2021) Simulert luseindusert dødelighet på virtuell smolt i produksjonsområde 2 til 7 ved bruk av SINMOD (Simulated lice induced mortality of virtual smolt in production area 2 to 7 by use of SINMOD). SINTEF Report No. 2021:01223. SINTEF, Trondheim

FAO (2019) FAO yearbook. Fishery and aquaculture statistics 2017. FAO, Rome

![image 8](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile8.png>)

Halttunen E, Gjelland KØ, Glover KA, Johnsen IA and others (2018) Migration of Atlantic salmon post-smolts in a fjord with high infestation pressure of salmon lice. Mar Ecol Prog Ser 592:243−256

![image 9](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile9.png>)

Harvey AC, Quintela M, Glover KA, Karlsen Ø and others (2019) Inferring Atlantic salmon post-smolt migration patterns using genetic assignment. R Soc Open Sci 6:190426

![image 10](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile10.png>)

Hesthagen T, Wienerroither R, Bjelland O, Byrkjedal I and others (2021) Fisker: Vurdering av laks Salmo salar for Norge. Rødlista for arter 2021 (Fishes: assessment of salmon Salmo salar for Norway. Redlist for species 2021). Artsdatabanken. https://www.artsdatabanken.no/lister/ rodlisteforarter/2021/8149 (accessed on 24 November 2021)

Huserbråten MBO, Johnsen IA (2022) Seasonal temperature regulates network connectivity of salmon louse. ICES J Mar Sci 79:1075−1082

![image 11](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile11.png>)

Jansen PA, Kristoffersen AB, Viljugrein H, Jimenez D, Aldrin M, Stien A (2012) Sea lice as a density-dependent constraint to salmonid farming. Proc R Soc B 279: 2330−2338

![image 12](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile12.png>)

Jensen JLA, Strøm JF, Nikolopoulos A, Primicerio R and others (2022) Micro- and macro-habitat selection of Atlantic salmon, Salmo salar, post-smolts in relation to marine environmental cues. ICES J Mar Sci 79:1394−1407

![image 13](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile13.png>)

Johnsen IA, Harvey A, Næverlid Sævik P, Sandvik AD and others (2021a) Reply to Jansen and Gjerde’s (2021) critique of the salmon louse infection model reported in Johnsen et al. (2021). ICES J Mar Sci 78:3852-3857

![image 14](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile14.png>)

Johnsen IA, Harvey A, Sævik PN, Sandvik AD and others

(2021b) Salmon lice-induced mortality of Atlantic salmon during post-smolt migration in Norway. ICES J Mar Sci 78:142−154

![image 15](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile15.png>)

Kristoffersen AB, Jimenez D, Viljugrein H, Grøntvedt R, Stien A, Jansen PA (2014) Large scale modelling of salmon lice (Lepeophtheirus salmonis) infection pressure based on lice monitoring data from Norwegian salmonid farms. Epidemics 9:31−39

![image 16](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile16.png>)

Kristoffersen AB, Qviller L, Helgesen KO, Vollset KW, Viljugrein H, Jansen PA (2018) Quantitative risk assessment of salmon louse-induced mortality of seaward-migrating post-smolt Atlantic salmon. Epidemics 23:19−33

![image 17](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile17.png>)

Ministry of Trade, Industry and Fisheries (2012) Forskrift om bekjempelse av lakselus i akvakulturanlegg (Regulation on control of salmon lice in aquaculture). Nærings- og fiskeridepartementet. https://lovdata.no/dokument/SF/ forskrift/2012-12-05-1140?q=lakselus (accessed on 24 February 2020)

Ministry of Trade, Industry and Fisheries (2015) Forutsigbar og miljømessig bærekraftig vekst i norsk lakse- og ørretoppdrett (Predictable and environmentally sustainable growth in Norwegian salmon and trout production). Nærings- og fiskeridepartementet, Oslo

![image 18](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile18.png>)

Murray AG, Moriarty M (2021) A simple modelling tool for assessing interaction with host and local infestation of sea lice from salmonid farms on wild salmonids based on processes operating at multiple scales in space and time. Ecol Modell 443:109459

![image 19](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile19.png>)

Myksvoll MS, Sandvik AD, Albretsen J, Asplin L and others (2018) Evaluation of a national operational salmon lice monitoring system—from physics to fish. PLOS ONE 13: e0201338

![image 20](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile20.png>)

Pike AW, Wadsworth SL (1999) Sealice on salmonids: their biology and control. Adv Parasitol 44:233−337

R Core Team (2020) R: a language and environment for statistical computing. R Foundation for Statistical Computing, Vienna

![image 21](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile21.png>)

Samsing F, Oppedal F, Johansson D, Bui S, Dempster T (2014) High host densities dilute sea lice Lepeophtheirus salmonis loads on individual Atlantic salmon, but do not reduce lice infection success. Aquacult Environ Interact 6:81−89

![image 22](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile22.png>)

Samsing F, Solstorm D, Oppedal F, Solstorm F, Dempster T (2015) Gone with the flow: current velocities mediate parasitic infestation of an aquatic host. Int J Parasitol 45: 559−565

![image 23](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile23.png>)

Sandvik AD, Johnsen IA, Myksvoll MS, Sævik PN, Skogen MD (2020) Prediction of the salmon lice infestation pressure in a Norwegian fjord. ICES J Mar Sci 77:746−756

![image 24](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile24.png>)

Skarðhamar J, Albretsen J, Sandvik AD, Lien VS and others (2018) Modelled salmon lice dispersion and infestation patterns in a sub-arctic fjord. ICES J Mar Sci 75: 1733−1747

![image 25](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile25.png>)

Stien A, Bjørn PA, Heuch PA, Elston DA (2005) Population dynamics of salmon lice Lepeophtheirus salmonis on Atlantic salmon and sea trout. Mar Ecol Prog Ser 290: 263−275

![image 26](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile26.png>)

Stige LC, Helgesen KO, Viljugrein H, Qviller L (2021) A statistical mechanistic approach including temperature and salinity effects to improve salmon lice modelling of infestation pressure. Aquacult Environ Interact 13:339−361

![image 27](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile27.png>)

Taranger GL, Karlsen Ø, Bannister RJ, Glover KA and others (2015) Risk assessment of the environmental impact of Norwegian Atlantic salmon farming. ICES J Mar Sci 72: 997−1021

![image 28](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile28.png>)

Thorstad EB, Whoriskey F, Uglem I, Moore A, Rikardsen AH, Finstad B (2012) A critical life stage of the Atlantic salmon Salmo salar: behaviour and survival during the smolt and initial post-smolt migration. J Fish Biol 81: 500−542

![image 29](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile29.png>)

Tucker CS, Sommerville C, Wootten R (2000) The effect of temperature and salinity on the settlement and survival of copepodids of Lepeophtheirus salmonis (Krøyer, 1837) on Atlantic salmon, Salmo salar L. J Fish Dis 23: 309−320

![image 30](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile30.png>)

Ugelvik MS, Dalvin S (2022) The effect of different intensities of the ectoparasitic salmon lice (Lepeophtheirus salmonis) on Atlantic salmon (Salmo salar). J Fish Dis 45: 1133−1147

![image 31](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile31.png>)

van Etten J (2017) R package gdistance: distances and routes on geographical grids. J Stat Softw 76:1−21

![image 32](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile32.png>)

van Walraven N, Fjørtoft HB, Stene A (2021) Less is more: negative relationship between biomass density and sea lice infestation in marine salmon farming. Aquaculture 539:736602

![image 33](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile33.png>)

Vollset KW (2019) Parasite induced mortality is context dependent in Atlantic salmon: insights from an individualbased model. Sci Rep 9:17377

![image 34](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile34.png>)

Vollset KW, Barlaup BT, Mahlum S, Bjørn PA, Skilbrei OT (2016) Estimating the temporal overlap between postsmolt migration of Atlantic salmon and salmon lice infestation pressure from fish farms. Aquacult Environ Interact 8:511−525

![image 35](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile35.png>)

Vollset KW, Dohoo I, Karlsen Ø, Halttunen E and others

(2018) Disentangling the role of sea lice on the marine survival of Atlantic salmon. ICES J Mar Sci 75:50−60 Vollset KW, Barlaup BT, Friedland KD (2019) Contextdependent impact of an ectoparasite on early marine growth in Atlantic salmon. Aquaculture 507:266−274 Vollset KW, Lennox RJ, Lamberg A, Skaala Ø and others (2021a) Predicting the nationwide outmigration timing of Atlantic salmon (Salmo salar) smolts along 12 degrees of latitude in Norway. Divers Distrib 27:1383−1392

![image 36](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile36.png>)

![image 37](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile37.png>)

Vollset KW, Nilsen F, Ellingsen I, Finstad B and others (2021b) Vurdering av lakselusindusert villfiskdødelighet per produksjonsområde i 2021 (Evaluation of salmon lice induced mortality of wild fish per production area in 2021). Ekspertgruppe for vurdering av lusepåvirkning, Bergen

![image 38](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile38.png>)

Wagenmakers EJ, Farrell S (2004) AIC model selection using Akaike weights. Psychon Bull Rev 11:192−196

![image 39](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile39.png>)

Wagner GN, McKinley RS, Bjørn PA, Finstad B (2003) Physiological impact of sea lice on swimming performance of Atlantic salmon. J Fish Biol 62:1000−1009

![image 40](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile40.png>)

Wagner GN, Fast MD, Johnson SC (2008) Physiology and immunology of Lepeophtheirus salmonis infections of salmonids. Trends Parasitol 24:176−183

![image 41](<Stige et al_2022_Modelling salmon lice-induced mortality wild salmon post-smolts of is highly sensitive to calibrated data_images/imageFile41.png>)

Wootten R, Smith JW, Needham EA (1982) Aspects of the biology of the parasitic copepods Lepeophtheirus salmonis and Caligus elongatus on farmed salmonids, and their treatment. Proc R Soc Edinb Biol Sci 81:185−197

Editorial responsibility: Tim Dempster, Melbourne, Victoria, Australia Reviewed by: S. Murray, I. A. Johnsen and 1 anonymous referee

Submitted: May 3, 2022 Accepted: October 6, 2022 Proofs received from author(s): November 10, 2022

