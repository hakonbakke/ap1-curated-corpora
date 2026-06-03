AQUACULTURE ENVIRONMENT INTERACTIONS Aquacult Environ Interact

Vol. 7: 267–280, 2015

Published online December 3

doi: 10.3354/aei00155

FEATURE ARTICLE

OPENPEN ACCESSCCESS

# Statistical and ecological challenges of monitoring parasitic salmon lice infestations in wild salmonid fish stocks

## Ingeborg Palm Helland1,*, Ingebrigt Uglem1, Peder A. Jansen2, Ola H. Diserud1, Pål Arne Bjørn3, Bengt Finstad1

1Norwegian Institute for Nature Research, PO Box 5685 Sluppen, 7485 Trondheim, Norway 2Norwegian Veterinary Institute, PO Box 750 Sentrum, 0106 Oslo, Norway 3Institute of Marine Research, PO Box 6404, 9294 Tromsø, Norway

ABSTRACT: Ecological monitoring programmes should provide precise data to inform management, but the data quality is often limited by methodological challenges and the need for cost-effective sampling. Parasite infestations are particularly challenging to monitor due to complex interactions among hosts, parasites and the environment. In Norway, salmon lice infestations on wild salmonid fish have been monitored since 1992 to survey the potential transmission between farmed and wild salmonids. Here, we compared spatiotemporal variation in salmon lice levels with variations in local fjord conditions, including salinity, temperature and infestation pressure from salmon farms (measured as mean abundance of mature female lice × number of farmed fish). We tested 3 different measures of infestation with different statistical properties. Our results confirm that, even after correcting for temperature and salinity effects, infestation pressure from salmon farms significantly increases the probability of lice infestation in wild salmonids. The probability of infestation increases with fish body length, salmon farm infestation pressure and temperature, and decreases with increasing freshwater influence. Furthermore, we found a significant interaction between temperature and infestation pressure from salmon farms. When the infestation pressure from farms is low, temperature has a strong increasing effect on the probability of infestation, but

- as the infestation pressure from farms increases, temperature gradually becomes less important. The exact results vary somewhat depending on the measure of lice infestations used, but the same trend can be seen in all models. We discuss the statistical and biological complexities that make monitoring of salmon lice in wild populations challenging.


*Corresponding author: ingeborg.helland@nina.no

![image 1](<Helland et al_2015_Statistical and ecological challenges of monitoring parasitic salmon lice infestations in wild salmonid fish stocks_images/imageFile1.png>)

Variation in salmon lice levels on wild salmonids have been monitored along the entire Norwegian coast.

Photo: Bengt Finstad. Map: Ingeborg P. Helland

KEY WORDS: Lepeophtheirus salmonis · Zeroinflation · Salmon farming · Temperature · Salinity · Salmo spp. · Caligus elongatus · Norway

### INTRODUCTION

In order to monitor species and define nature management priorities, decision makers want information that is easy to evaluate and cost effective to gather. At the same time, ecological communities are complex, and a large number of interacting variables often makes it difficult to sample all relevant para-

© The authors 2015. Open Access under Creative Commons by Attribution Licence. Use, distribution and reproduction are unrestricted. Authors and original publication must be credited.

Publisher: Inter-Research · www.int-res.com

meters and to interpret their influence on the species of interest. It is therefore important that collection of data in ecological monitoring programmes is aimed

- at providing precisely the information needed to make conservation decisions (Nichols & Williams 2006, Lindenmayer & Likens 2009). This means that the information gathered must be sufficiently accurate and precise to understand the underlying scientific questions, including variations in time and space (Sims et al. 2008, Reynolds et al. 2011). Monitoring parasite infestations is particularly challenging due to the complex interactions among hosts, parasites and the environment (Dobson & Hudson 1986, Hatcher et al. 2006, Tompkins et al. 2011) and due to the statistical challenges related to excessive numbers of 0-values (Zuur et al. 2009).


Through the national salmon lice monitoring programme, Norway has since 1992 collected an extensive dataset based on registrations of salmon lice on wild salmonid fish (Atlantic salmon Salmo salar L., brown trout S. trutta L. and Arctic char Salvelinus alpinus L.). The programme was initiated because the massive increase in biomass of farmed salmonids (of which >90% are Atlantic salmon; Directorate of Fisheries 2013) during the last decades has raised growing concerns regarding the transmission of lice between farmed and wild salmonids, with subsequent negative population effects for wild salmonids (Heuch & Mo 2001, Serra-Llinares et al. 2014, Jones et al. 2015, Taranger et al. 2015, Thorstad et al. 2015). Since farmed salmon are kept in floating net pens with free water exchange, there is potential for pathogen exchange with the environment. The spatial density of salmon farms varies substantially along the Norwegian coast (Jansen et al. 2012), yet farmed salmon outnumbered wild salmon by a factor of 250 to 700 in 2011 (Johansen et al. 2011). Hence, the number of potential hosts for salmon lice has increased dramatically compared to natural host abundance. Moreover, while wild salmonids usually reside in the fjords mainly during summer, large numbers of farmed salmon are present year round. This causes a larger potential for heavy salmon lice infestations that may occur at different seasonal times compared to the natural infestation pressure (Bjørn et al. 2011, Jansen et al. 2012, Torrissen et al. 2013, Vollset & Barlaup 2014).

The dominating species of salmon lice found on salmonids in Norway is Lepeophtheirus salmonis (Krøyer), while Caligus elongatus (von Nordmann) occurs at lower abundances (Bjørn & Finstad 2002). The lice are transmitted between hosts, as planktonic larvae are free-living in seawater, and older stages attach to fish where they feed on mucus, skin and

blood (Pike & Wadsworth 1999, Boxaspen 2006). High infestations may reduce the immune system and growth of the fish and cause increased mortality (Todd et al. 2000, Revie et al. 2009, Finstad & Bjørn 2011, Finstad et al. 2011). The development and reproductive rates of salmon lice are temperature dependent, and their survival is significantly reduced at salinities below 20‰ (Stien et al. 2005, Bricknell et al. 2006). It has been estimated that under certain conditions, the planktonic larvae can spread more than 100 km before they need to attach to a host (Asplin et al. 2011, 2014). Recent experiments at different current velocities have shown that attachment probability of salmon lice during an encounter with a potential host likely is dependent on the swimming speed of the host (Samsing et al. 2015)

Modelling from salmon farms in Norway has shown how salmon lice spread between farms and has revealed that the infestation pressure among farms increases with density of fish and temperature (Jansen et al. 2012). Other studies have evaluated effects of environmental variables on salmon lice dynamics in farmed salmonids (e.g. Krkošek et al. 2010, Kristoffersen et al. 2013, Rogers et al. 2013, Rees et al. 2015), but similar studies are lacking for wild populations. To the best of our knowledge, only a few studies have statistically modelled spatiotemporal variations in salmon lice counts on wild salmonids (Gargan et al.

- 2003, Middlemas et al. 2013, Serra-Llinares et al. 2014, Patanasatienkul et al. 2015), and although they all found that the lice infestations were influenced by lice production in nearby salmon farms, none of the studies tested for interactions with other environmental variables, such as temperature and salinity. Since temperature is a strong driver of development and reproduction rate of salmon lice (Stien et al. 2005), lice abundances follow strong seasonal cycles. Salmon lice have their lowest abundance in early spring and peak during autumn, a pattern seen from lice counts both on farmed salmon (Jansen et al. 2012) and wild salmonids (Bjørn & Finstad 2002, Rikardsen
- 2004, Serra-Llinares et al. 2014). Therefore, in order to model the potential infestation pressure from farms on wild salmonids, it is important to correct for potential temperature effects before the separate effect of temperature and infestation pressure from farms can be evaluated.


In this paper, we used data from the Norwegian monitoring programme collected along the entire Norwegian coast and compared the temporal and spatial variation in salmon lice levels with variations in local conditions, including salinity, temperature and infestation pressure from salmon farms. Through

this approach, we identified the main drivers of variations in infestation levels among wild salmonids along the Norwegian coast. Further, we discuss weaknesses of the collected data and explain the statistical and biological complexities that make monitoring of salmon lice in wild populations challenging.

analyses, since lice intensity is assumed to be similar for both species (Bjørn & Finstad 2002, Serra-Llinares et al. 2014) and because all individuals are needed to increase the size of the dataset and to cover all regions. Hence, we hereafter refer to all fish included in our analyses as sea trout, since brown trout constitutes 95% of our data.

Sampling was conducted at 41 sampling sites distributed in 15 fjords along the entire Norwegian coast (Fig. 1). Details about fishing procedures are given by Serra-Llinares et al. (2014). Within a fjord, the sampling sites were usually organised in a gradient from inner to outer fjord areas in order to cover environmental variations and because salmon farming is less intensive in the inner part of the fjords. Further, some inner fjord areas have been protected from salmon farming by their status as ‘National Salmon Fjords’ (Aasetre & Vik 2013). In this sense, many of the sampling sites in the inner parts were used as control sites that are expected to be less affected by farming than sites closer to the open

MATERIALS AND METHODS

Data collation

The salmon lice monitoring programme in Norway consists of a variety of sampling methods used in combination. Atlantic salmon, brown trout and Arctic char (hereafter simply salmon, trout and char) spawn in freshwater but are susceptible to salmon lice infestations when they migrate to marine habitats for feeding. Trout and char usually stay in the fjords during their marine phase, while salmon migrate quickly through the fjords on their way to the open sea. The salmon lice density is lower in the open sea compared to near-shore waters, due to the high density of farmed salmonids in the latter area. Therefore, salmon are expected to be most vulnerable to infestations during the short period when they migrate through the fjords and along the coast. However, trout and char are exposed to salmon lice infestations in the fjords throughout most of their marine phase (Bjørn et al. 2007). In the Norwegian salmon lice monitoring programme, salmon are sampled by pelagic trawling during the assumed migration period, but it has often been difficult to collect a sufficient number of individuals. Therefore, gill net sampling of trout and char at selected sampling sites has also been used to monitor the local salmon lice infestation pressure (Serra-Llinares et al. 2014). In addition, the infestation pressure has been monitored by placing hatchery-reared salmon smolts in sentinel cages to estimate the infestation levels over several weeks (Bjørn et al. 2011). In our analyses, we only included data from gill net sampling conducted during the period 2004 to 2010, which is the largest part of the dataset that was collected in a comparable manner. Most of these catches consist of trout (4610 trout and 280 char), but in the northernmost fjords, char is more abundant. We did not separate between char and trout in our

![image 2](<Helland et al_2015_Statistical and ecological challenges of monitoring parasitic salmon lice infestations in wild salmonid fish stocks_images/imageFile2.png>)

Fig. 1. Sampling sites (•, n = 41) situated in 15 Norwegian fjords. Grey lines indicate borders between the 19 Norwegian counties

sea (Serra-Llinares et al. 2014). Normally salinity increases towards the outer fjord area due to higher freshwater influence in the innermost areas; hence, salinity and pressure from farming are probably correlated along the fjord gradient. Each site was usually sampled 2 to 3 times during the summer season, in order to follow the seasonal dynamics of the salmon lice infestations. The number of sampling sites included in the monitoring has increased over the years, from 6 sites in 2004 to 27 in 2010. Therefore, not all 41 sites were sampled each year, but 7 sites were sampled >10 times, 11 sites 5 to 10 times, and 23 sites were sampled <5 times. In total, the dataset consists of 244 unique sample occasions and 4890 individual fish (mean number of individuals at each sampling: 20, range: 1−80). A more detailed description of the dataset is given by Helland et al. (2012). Each individual was registered with species, body length (mm), body weight (g) and number of lice attached. Salmon lice were classified according to life stage (stationary chalimus larvae [66%], mobile pre-adults [17%] and adults [16%]) and species (Lepeophtheirus salmonis [99%] and Caligus elongatus [1%]). However, since the number of lice in each stage was often low, we grouped all lice stages and used the total number of lice in our analyses.

Temperature and salinity are known to influence salmon lice infestations (Stien et al. 2005, Bricknell et al. 2006). In order to obtain comparable data for all periods and areas, we downloaded historical data on fjord surface temperatures from http://lusedata.no/, which is based on monthly measures reported from all salmon farms to the Norwegian Food Safety Authority. Temperatures are registered as mean values for each month and each county, except the 3 southernmost counties (Rogaland, Vest-Agder and Aust-Agder, of which only the latter is included in the monitoring programme, see Sandnes in Fig. 1), which are grouped together in the database. Hence, due to the coarse spatial resolution of the temperature data, all sampling sites within the same county were given the same value, but the temporal variation between each sampling was maintained. We used temperature values from the month before each sampling, since we expected a delayed effect of temperature on the development of salmon lice infestations.

Freshwater influence was used as a proxy for salinity level, since no salinity data covering all the necessary areas and periods were available. This proxy was estimated for each of the 41 sampling sites based on the water discharge (m3 s−1, mean over the period 1961 to 1990, Norwegian Water Resources and Energy Directorate) at each river outlet within 25 km, di-

vided by the seaway distance between each sampling site and river (calculated from ArcGIS tools). Thereafter values from each river were summed up to 1 value for each sampling site. Hence, the spatial variation in salinity levels between each sampling site was maintained, but no temporal variation was included in our models.

For each of the 244 sampling occasions, we estimated the local infestation pressure resulting from salmon farms at the time of sampling. This was based on monthly count data of mature female salmon lice and reported numbers of fish on all active marine salmon farms along the coast of Norway (Jansen et al. 2012). The amount of salmon lice emanating from each farm in each month was calculated as the mean abundance of mature female lice multiplied by the reported number of fish at each farm. Lice infestation pressure for the whole coast in each month was calculated using the kernel density function in ArcGIS (Spatial Analyst) with a 40 km search radius and 1 km2 grid cells. The infestation pressure for a given sampling month and location was then extracted from the grid cell accounting for infestation pressure for the corresponding location and month. The standard score of the value, calculated by subtracting the mean and dividing by standard deviation, was used in the analyses in order to prevent the large span between minimum and maximum values from influencing the models. Further, to avoid negative numbers, 1 was added to the standard score.

### Statistical approaches

Data on salmon lice infestations can be presented in different ways and the unit of measure used determines what kind of biological information can be retrieved and which statistical methods are appropriate. We compared statistical analyses based on 3 different units of measure, since these 3 approaches together give a better understanding of the infestation levels than each measure alone. First, we used a binary response variable where each individual fish was noted either to have (2974 individuals) or not to have (1916 individuals) any lice. Although a binary response variable has limited biological information as it does not allow for testing why some individuals have many lice while others have few, the advantage of this measure is that the statistical methods are relatively simple and that the number of observations remain high (N = 4890 individual fish). However, it is of limited interest whether a fish has 1 or only a few lice, since the potential negative effects, such as

(Taranger et al. 2015, Thorstad et al. 2015). Below the threshold value of 0.1 lice g−1, no extra mortality is assumed, while mortality is assumed to increase by 20% among fish with 0.1 to 0.2 lice g−1, 50% among fish with 0.2 to 0.3 lice g−1, and for fish with more than 0.3 lice g−1, 100% extra mortality risk is anticipated (Taranger et al. 2015). Studies of effects on older and larger trout (i.e. maturing individuals or veteran migrants) are lacking, but because studies on char have indicated that the effect of salmon lice is expected to be more severe for larger fish (Tveiten et al. 2010), extra mortality is predicted to occur above 0.025 lice g−1 for this group (Taranger et al. 2015, Thorstad et al. 2015). Based on this, we compared 3 different lice levels in our models with proportional response variables: >0.1, >0.05 and >0.025 lice g−1. To include first-time migrants only, we selected individuals <200 g. Further, we used only sampling occasions with catches of at least 15 individuals to avoid single individuals with extreme values having too strong an influence on the results. This subset of data thus included 2250 individuals (46% of the total number of individuals, see Fig. S1 in the Supplement, available at www.intres.com/articles/suppl/q007p267_supp.pdf), but still captures a similar range of lice infestations as the full

immune responses, reduced growth and mortality, only occur after the infestation reaches a certain level (Thorstad et al. 2015).

Therefore, as a second unit, we used a proportional response variable, measured as the percentage of individuals from each sample with a given level of salmon lice infestation. Parasite data are often reported as abundance, intensity or prevalence (Rózsa et al. 2000). Due to the 0-inflated distribution of salmon lice data (Fig. 2), abundance (mean or median based on all individuals) is not a suitable way of describing the variation at the population level. Further, intensity and prevalence are not suitable measures for our modelling approach because they either exclude individuals without any lice (intensity, mean or median based on infected individuals only) or do not take into account the variation in extent of infestation (prevalence, the proportion of infected hosts). Therefore, the proportion of individuals above a threshold level may be a better measure, especially if this threshold represents a biologically meaningful lice infestation level. A threshold of 0.1 lice g−1 fish weight (lice g−1) has been suggested as a critical value for initial physiological disturbances caused by salmon lice on first-time migrating trout in Norwegian fjords

dataset (Fig. S2 in the Supplement). The advantage of using a proportional response variable is that it represents a more biologically meaningful variable than the binary response variable; however, a disadvantage is that the number of observations is reduced to the number of sampling occasions (N = 159).

![image 3](<Helland et al_2015_Statistical and ecological challenges of monitoring parasitic salmon lice infestations in wild salmonid fish stocks_images/imageFile3.png>)

Finally, as the third unit of measure, we used the actual number of lice counted on each individual fish as the response variable. This is clearly the most accurate measure that incorporates detailed biological information and keeps the number of observations as high as possible (N = 4890 individual fish). Yet, there are statistical limitations to what kind of methods that can cope with such an extremely 0-inflated distribution and very large variation between individuals, as seen in this variable (Fig. 2). Approximately 39% of the individuals in the dataset had no lice, while 9% had only 1 louse, and the highest number of lice recorded on 1 fish was 586.

We tested for the relationship between salmon lice infestations (SL) and temperature (T), freshwater influence (F), infestation pressure from salmon farms (IP) and their interaction terms, by comparing a set of linear models. In addition, fish length (L) was included since body size is expected to positively influence the probability for salmon lice infestations. This gave the following full model:

- Fig. 2. Frequencies of total number of salmon lice Lepeophtheirus salmonis counted on wild sea trout Salmo trutta. The lower panel shows the same data as presented in the upper


panel, but includes only lice counts of ≤50

SL = L + T + F + IP + T × F + T × IP + F × IP (1)

true 0s by the same full model as described in Eq. (1). To correct for potential overdispersion, we tested whether models based on ZINB performed better than models based on ZIP, since ZINB models correct for overdispersion both in the 0s and in number of salmon lice, while ZIP models only correct for 0inflation.

As the response (salmon lice infestation, SL), we used each of the 3 measures described above, viz. binary variable, proportional variable and the 0inflated variable. For the binary variable, we used a general linear mixed model. Due to the location of sampling sites in a gradient from inner to outer fjord area and the repeated sampling at each site, all 244 sampling occasions included cannot be considered statistically independent. To account for this non-independence, we grouped all sampling occasions performed in the same fjord in the same year (totalling 52 groups), and included this grouping variable as a random effect. In the models based on the proportional response variable, the number of data points was too low (N = 159) to include this random effect, and thus simpler general linear models (GLMs) were used. In the proportional models, we controlled for overdispersion (i.e. variance greater than expected from model) by correcting the standard errors using a quasi-GLM and adding a dispersion parameter (Zuur et al. 2009). Fish length was naturally not included in the model with the proportional response variable, since this was based on grouped individuals rather than single fish and we already selected individuals of comparable size.

For all 3 approaches, the model selection was performed by stepwise removal of terms from the full model (Eq. 1) to minimize Akaike’s information criterion (AIC), and models with ΔAIC < 2 were considered to have equal support (Burnham & Anderson 2002). Based on the parsimony principle, the simplest model with fewest terms was selected when 2 models were equally supported (ΔAIC < 2). All modelling was performed with the statistical software R 2.14.0 (R Development Core Team 2012) with the packages lme4 (Bates et al. 2014) and pscl (Jackman 2014).

### RESULTS

According to the final model with the binary response variable, all explanatory variables had a statistical influence on the probability of presence of lice on wild sea trout (Table 1). The probability that an individual fish had lice increases with body length, increasing infestation pressure from salmon farms and increasing temperature, and decreases with increasing freshwater influence (Fig. 3). Further, there was a significant interaction between temperature and infestation pressure from salmon farms. When the infestation pressure from farms is low, temperature has a strong increasing effect on the probability of a fish having lice; however, as the infestation pressure from farms increases, temperature gradually becomes less important (Fig. 4).

The last response variable, with 0-inflation, required use of models that can deal with excessive numbers of 0s, such as 0-inflated Poisson (ZIP) or 0-inflated negative binomial (ZINB) models (Zuur et al. 2009). When modelling parasite data, it is important to treat the 0s in an appropriate way and separate between ‘true’ and ‘false’ 0-values. While the true 0s are what we want to measure, namely the individuals that have been exposed to salmon lice, but still have no infestations due to their immune response, behaviour, environmental conditions or other factors that protect them, the false 0s are individuals that do not have any lice because they have not been exposed to salmon lice. It is not possible to separate between these 0s in reality, as we do not know where the fish have been prior to sampling, but it is important that the method used can handle this combination of true and false 0s statistically. The ZIP and ZINB models consist of 2 parts: first the probability for false 0s in the data is estimated and thereafter the number of salmon lice is estimated when corrected for the probability for false 0s (Zuur et al. 2009). For the 0-inflated models, we corrected for non-independent sampling points by letting the grouping variable of fjord and year (explained above) describe the probability for false 0s. Thereafter we modelled the probability of

Also, when using the proportion of individuals with a given level of lice infestations, we found a positive

Table 1. Summary of the best model explaining the probability of a sea trout Salmo trutta having salmon lice Lepeophtheirus salmonis measured as a binary response variable of either lice or no lice

|Estimate SE p<br><br>Intercept −3.445 0.547 <0.001 Fish length 0.003 <0.001 <0.001 Infestation pressure from farms 1.245 0.278 <0.001 Temperature 0.314 0.039 <0.001 Freshwater influence −134.100 8.671 <0.001 Temperature × infestation −0.075 0.021 <0.001<br><br>pressure from farms|
|---|


![image 4](<Helland et al_2015_Statistical and ecological challenges of monitoring parasitic salmon lice infestations in wild salmonid fish stocks_images/imageFile4.png>)

- Fig. 3. Predicted probability of a wild sea trout Salmo trutta having salmon lice Lepeophtheirus salmonis as a function of each of the 4 explanatory variables, viz. infestation pressure from farms (estimated from reported counts, see Jansen et al. 2012), temperature, freshwater influence and fish length. Solid black lines represent predicted regression values (parameter values in Table 1), and grey lines show 95% confidence interval. The upper (lower) boxplots in each panel illustrate fish with (without) salmon lice. In each boxplot, the black vertical line shows the median, the box marks 25th−75th percentiles, and the


stippled lines indicate the spread between the minimum and maximum values

influence of temperature and a negative influence of salinity (Fig. 5, Table 2). While temperature and salinity were strongly significant independent of which threshold level that was used, the increasing effect of infestation pressure was statistically significant only when using the proportion of individuals with >0.025 lice g−1 and not at threshold levels of 0.05 or 0.1 lice g−1 (Fig. 6). Further, there were no interac-

tion effects in any of the final models. One reason why the results vary among the 3 levels may be the statistical distribution of different variables. When the threshold level is set to 0.1 lice g−1, 47% percent of the data points are 0, meaning that in almost half of the samples, none of the individuals have lice infestations above the threshold (see Fig. S3 in the Supplement). Such a high number of 0s likely restricts the

model’s ability to explain the variation, which causes the results to be less reliable. When the level is reduced to 0.025 lice g−1, more variation is seen in the variable, since the number of 0s is reduced to 26%.

![image 5](<Helland et al_2015_Statistical and ecological challenges of monitoring parasitic salmon lice infestations in wild salmonid fish stocks_images/imageFile5.png>)

We were unable to use the final lice intensity response variable, i.e. the total number of lice counted on each individual fish. We attempted both ZINB and ZIP models but were not able to perform a model selection because many of the models would not converge when variables were removed from the full model. Hence, the models were considered to be unreliable due to low explanatory power and are not presented.

### DISCUSSION

Our study shows that infestation pressure from salmon farms, temperature and salinity strongly influenced lice infestations on wild sea trout in Norway in the period between 2004 and 2010. The significant influence of these variables was expected, as salmon lice infestations are naturally governed by variations in ambient temperature and salinity (Stien et al. 2005, Bricknell et al. 2006), and a previous Norwegian study also pointed out the importance of nearby salmon farms (Serra-Llinares et al. 2014). Although the exact results vary somewhat depending on which measure

- Fig. 4. Predicted probability of a wild sea trout Salmo trutta having salmon lice Lepeophtheirus salmonis as a function of the interaction between infestation pressure from farms and temperature (parameter values from the regression are presented in Table 1). Solid line, long dashed line and short dashed line represent infestation pressure with levels 3, 2 and 1, respectively. Higher levels of infestation pressures are not plotted, since the majority of the data (94%) were below this level (see

Fig. 3)

![image 6](<Helland et al_2015_Statistical and ecological challenges of monitoring parasitic salmon lice infestations in wild salmonid fish stocks_images/imageFile6.png>)

- Fig. 5. Proportion of wild sea trout Salmo trutta with salmon lice Lepeophtheirus salmonis levels above 0.025 lice per gram fish weight (lice g−1) as a function of (a) temperature and (b) freshwater influence. Solid black lines represent predicted regression


values (parameter values in Table 2), and grey lines show 95% confidence intervals

Table 2. Summary of best models explaining the proportion of sea trout Salmo trutta in a sample with salmon lice Lepeophtheirus salmonis levels above either 0.1, 0.05 or 0.025 lice per gram fish weight

salmonids, as seen both from our results from the binary model as well as other studies (MacKenzie et al. 1998, Gargan et al. 2003, Middlemas et al. 2013, SerraLlinares et al. 2014, Thorstad et al. 2015). In salmon farms, a clear pattern of increased lice levels with increasing temperature can be seen (Jansen et al. 2012), and although we lack true baseline data of the natural lice level on wild salmonids before salmon farms were present, it is likely that the effect of seasonal temperature also influences the natural salmon lice dynamics. Thus, correlating lice levels among wild fish with lice levels in farms, without considering ambient temperature of the wild fish, may partly confound the influence of infestation pressure from salmon farms, if both levels are

|Lice level Estimate SE p (lice g−1)<br><br>0.1 Intercept −3.084 0.817 <0.001 Infestation pressure from farms 0.178 0.109 0.104 Temperature 0.176 0.064 0.006 Freshwater influence −87.383 26.839 0.001<br><br>0.05 Intercept −2.589 0.749 <0.001 Infestation pressure from farms 0.195 0.113 0.087 Temperature 0.172 0.059 0.004 Freshwater influence −68.171 23.236 0.003<br><br>0.025 Intercept −2.190 0.720 0.002 Infestation pressure from farms 0.312 0.128 0.016 Temperature 0.158 0.057 0.006 Freshwater influence −58.019 21.968 0.009|
|---|


of lice infestations we used, the same trend was evident in all models, which indicates that our results are relatively robust. The binary model, comparing individuals with and without lice, showed a significant increase in the probability of lice infestations with increased infestation pressure from farms. Similarly, previous studies from Ireland (Gargan et al. 2003), Scotland (Middlemas et al. 2013) and Norway (SerraLlinares et al. 2014) found an increase in salmon lice levels on wild sea trout with high density of salmon farms. However, these studies did not take potential interactions with other environmental variables, such as temperature and salinity, into account. In our study, we found an interaction between temperature and infestation pressure from salmon farms. At low infestation pressure from farms, temperature is a strong driver of the presence of lice on wild sea trout; however, when the infestation pressure from farms is high, temperature becomes less important. This may be because most of the fish already have salmon lice when infestation pressure is higher. Alternatively, it may be because the infestation pressure from farms is lower when temperatures are low, and as temperature increases, so does the infestation pressure.

strongly driven by the same seasonal temperature development. It is therefore noteworthy that even after correcting for the temperature effect, our results show that infestation pressure from salmon farms significantly increases the probability of wild sea trout having salmon lice. To our knowledge, this has never been demonstrated before.

The measure of the total number of lice displayed extreme 0-inflation, and we were therefore not able to test which drivers determine the total number of lice on wild sea trout. In addition to the 0-inflation, a relatively low number of fish were collected at each site and there are large temporal and spatial variations in environmental conditions between sampling occasions. This combination causes statistical challenges even for methods that are created to cope with 0-inflation, and the measure of total number of lice on each fish could not be used as the response variable in spatiotemporal statistical comparisons. One reason for 0-inflated distribution is that individuals that have recently been living in freshwater may not be infested even if they are collected in a fjord area with high lice density. Hence, this can lead to unexpected results, such as higher infection pressure being associated with reduced probability of infestation, even if the intensity rises.

When using proportion of fish with a given level of lice infestation in our models, the results were partly dependent on the threshold level used. The effect of temperature and salinity remained similar independent of lice level, while the effect of infestation pressure from salmon farms was statistically significant only when we used the lowest level of 0.025 lice g−1 and not at levels of 0.05 or 0.1 lice g−1. Nevertheless, it is clear that infestation pressure from salmon farms causes increased level of lice infestations of wild

One of the reasons why so few studies have modelled effects of environmental variables on the temporal and spatial variation in salmon lice infestations on wild salmonids likely is the methodological challenge with collecting and analysing parasite data in a representative manner. We recognize 4 main challenges: (1) to find the most relevant biological and statistical measure of salmon lice levels, (2) to get

![image 7](<Helland et al_2015_Statistical and ecological challenges of monitoring parasitic salmon lice infestations in wild salmonid fish stocks_images/imageFile7.png>)

Fig. 6. Proportion of wild sea trout Salmo trutta with salmon lice Lepeophtheirus salmonis levels above (a) 0.025, (b) 0.05 and (c) 0.1 lice per gram fish weight (lice g−1) as a function of infestation pressure from farms. Solid black lines represent predicted regression values (parameter values in Table 2), and grey lines show 95% confidence intervals. Predicted values are only drawn for statistically significant results

access to sufficiently detailed environmental variables in space and time, (3) that the large natural variation on parasite data requires very large datasets and advanced statistical methods, and (4) to collect sufficient and representative individuals of fish without negatively influencing the fish population. In the following, we will discuss these 4 challenges.

It is not straightforward to determine what measure of lice infestations to use in order to keep as much biological information as possible and simultaneously fulfil statistical requirements for relevant comparisons. The comparison of fish with and without lice (i.e. the binary model) was the most statistically robust of our models, since it has a high number of

observations (i.e. all collected fish in the monitoring programme) and includes a random effect in order to correct for spatiotemporal autocorrelation. The output of this model was clear, and all explanatory variables followed the expected pattern. In spite of this, it is of limited interest, both scientifically and for conservation purposes, to group all infected fish together irrespective of the number of lice. The main task is to understand under what circumstances salmon lice infestations have a considerable negative effect on individuals or populations. A binary comparison of fish with and without lice cannot answer this question since the presence of lice does not necessarily cause negative effects if the number of lice is low.

The frequency of parasites on hosts is often presented as aggregated group values, such as prevalence, abundance and intensity, in order to create a measure that summarizes the variation among individuals in a way that facilitates comparisons between groups or populations (Rózsa et al. 2000). Although useful for many comparisons, the interpretation of such aggregated measures is less intuitive than total parasite counts or categorical variables (e.g. lice vs. no lice). Further, all aggregated measures are sensitive to the number of individuals included in each group, and it is not always clear whether all individuals should be grouped or whether grouping should be based on size classes, sex, species etc. For statistical comparisons, there is also a challenge with using group aggregations instead of individual values because of the reduction in number of observations. When we used the aggregated proportional measure based on suggested threshold values for salmon liceinduced mortality (Taranger et al. 2015), our results were partly sensitive to the threshold value of lice infestations used. The reason this approach was less robust than the binary comparison is likely that the number of observations is strongly reduced when using aggregated group values rather than individual information. However, although there are statistical challenges with analysing such group values with our approach, the threshold values used by Taranger et al. (2015) may still be useful measures for risk assessment purposes. An alternative measure of infestation that would be interesting to explore in future statistical analyses is to combine the threshold value approach with a binary approach. Hence, rather than comparing lice vs. no lice, infested vs. not infested may be measured as above and below a threshold value of number of lice per gram fish. This would keep all individuals in the dataset, but at the same time incorporate a biologically meaningful measure of infestation level. However, it is not fully clear what threshold values would be meaningful to use on an individual level. The values suggested by Taranger et al. (2015) are intended for populationlevel effects (i.e. % mortality), while individual tolerance levels may be highly variable (Finstad & Bjørn 2011). This should be a future topic of research.

Total number of lice recorded on each individual fish is an intuitive measure containing more of the biological information. However, summing up lice counts on each individual is also a simplification that does not fully capture the biological complexity of the infestations. Different development stages of salmon lice have different impacts on salmonids, and although chalimus larvae may cause severe damage

on skin and fins when they occur in high numbers, it is the pre-adult and adult stages that account for the most severe damage (Thorstad et al. 2015). Additionally, the number of lice in different stages gives information about the population cycle of lice and indicates the potential for lice exposure in the near future. Hence, some important biological information is lost by grouping all stages of salmon lice together. Another reason why salmon lice infestations, like many parasite infestations, are notoriously difficult to study is that the likelihood of a fish to be collected in the monitoring programme is dependent on its infestation level, since salmon lice influence the survival and behaviour of the fish (Finstad & Bjørn 2011). However, studies that include acoustic telemetry may shed light on fish movements in the fjords as well as behavioural differences between individuals with and without lice, as recently illustrated by Gjelland et al. (2014).

It may be that our 0-inflated model approach would have been more successful if the explanatory variables (i.e. temperature, salinity and infestation pressure from salmon farms) had been more accurate. The temperature data we had access to have limited spatial resolution and resulted in the same value for all sites within a county. Even more problematic is the proxy we used for salinity, which lacks any temporal variation. In fact, it is rather surprising that the binary and proportional models were able to incorporate such a poor variable successfully. Our measure of infestation pressure from farms has a good spatiotemporal resolution, and Kristoffersen et al. (2014) recently evaluated this measure and confirmed that it can be used to predict infestation levels of farmed fish over spatial scales. However, it is based on the assumption that salmon lice larvae are spread evenly in all directions away from the fish farm, without taking into account currents or variations in temperature and salinity. Stochastic factors influence infection pressure with local accumulations of larval lice (Penston et al. 2008). Conditions to create such accumulations may or may not be present depending on local hydrodynamics, which have been seen to strongly influence local infection pressure associated with salmon farms (e.g. Murray & Hall 2014). Hence, the detailed variations in local environments in the large Norwegian fjords are not captured by our data and are therefore not accounted for by the measures of temperature, salinity and infestation pressure we have included. Yet, in spite of this, all environmental variables showed significant results in our models, and we can therefore assume that they did capture sufficient variation among the sampling occasions.

Further, even if detailed information on environmental variations in time and space had been available, it is impossible to know exactly what environmental conditions wild fish have been exposed to. Salmonids may swim large distances in a short time period (Finstad et al. 2005) and thereby move between different salinity and temperature zones, as well as between areas with high or low infestation risk of salmon lice. Such variations that cannot be fully predicted are common in many ecological studies and although not all relevant details may ever be available, it would likely have been possible to reduce the noise and improve the models by having a more thorough sampling design and higher number of data points. Further, recent approaches of spatiotemporal models of salinity, temperature and currents in the fjords may improve the availability of relevant environmental data (Asplin et al. 2011, Salama & Rabe 2013, Johnsen et al. 2014). Although statistical models based on rather coarse-scale proxy data can be used to identify factors influencing the infection pressure on wild salmonids, as we have tried here, this approach may not be that useful for determining whether individual areas have a lice problem owing to finer-scale environmental variation.

As expected, our result showed that both temperature and salinity influenced salmon lice levels in addition to infestation pressure from farms. However, all 3 of these variables are correlated along gradients from inner to outer fjord areas. Salinity is often lowest in the innermost areas due to higher freshwater influence from rivers, which also influences the temperature and causes colder water in inner fjord areas. Simultaneously, the infestation pressure is lower in innermost areas, because the density of salmon farms is higher in outer parts of many of the sampled fjords. The sampling in the monitoring programme was therefore designed with several sampling sites along each fjord, in order to capture the variation in these gradients. However, this also creates a challenge since the 3 variables are correlated and we cannot separate between the effects of each of the 3 within 1 fjord. Yet, by having sampling sites distributed in different geographic areas that vary in climate and hydrology and ensure that both areas with and without salmon farms in the outer fjord are included, it is possible to separate statistically between the effects of temperature, salinity and infestation pressure if the sample sizes are sufficiently large.

Due to the complexity discussed above, it is clear that statistical analyses of salmon lice infestations on wild salmonids require advanced statistical methods and a large dataset in order to handle the natural

variation in lice levels, fish behaviour and environmental conditions. Hence, the number of individuals in each sample is crucial. If resources are limited, a monitoring programme may benefit from having fewer sampling sites with larger effort at each location, instead of high numbers of sampling sites spread over large areas with large environmental variations that cannot be accounted for. For the Norwegian salmon lice monitoring programme, this would imply selection of certain fjords to study in more detail, both temporally and spatially, rather than having a low number of samples from each area and a high number of included fjords. Some Norwegian fjords are very large and therefore have large environmental variations, including large variation in intensity of salmon farming. Hence, it has to be expected that there will be large differences in salmon lice infestation levels on wild sea trout collected in different areas in the same fjord. Since the dataset analysed in this study was primarily collected to provide an up-to-date snapshot of the infestations on wild fish in different regions, the sample sizes are in many cases too small for advanced statistical analyses. One of the reasons for the low sample sizes is the use of gill nets as sampling gear. As gill nets unavoidably involve mortality, sample sizes were kept at a minimum to avoid negatively influencing the already weak populations of sea trout and Arctic char. However, after the methodological challenges of analysing the monitoring data were reported to the management authorities (Helland et al. 2012), the sampling design of the Norwegian monitoring programme changed in 2013. Today, sampling is performed with fyke nets, which secure a live catch of fish and opens up the possibility of catching a larger number of individuals at each sampling site and releasing the fish unharmed after measurements and counting of salmon lice (Taranger et al. 2015). Further, the number of sampling sites has been reduced and effort has been concentrated in 4 model fjords with detailed sampling of a higher number of environmental parameters. We welcome this approach and recommend increasing the number of such modelling fjords in order to capture the large environmental variation along the Norwegian coast. Clearly, a detailed monitoring programme cannot cover the full coastline; however, considering the length of the Norwegian coast and the continuous expansion of the fish farming activity, there should be room for more than 4 model fjords. Future statistical analyses of these data may improve our understanding of under what circumstances salmon lice levels negatively affect wild salmonid stocks.

Acknowledgements. Sampling of the data was financed by the Norwegian Environment Agency, the Norwegian Food Safety Authority, the Norwegian Research Council and own funding from the Norwegian Institute for Nature Research (NINA) and the Institute of Marine Research (IMR). Many persons within science, management and other institutions were involved in sampling the data and are hereby acknowledged for their contribution. Statistical analyses were funded by the Norwegian Environment Agency to NINA and the Ministry of Trade, Industry and Fisheries to IMR. The study was also partially funded by the NINA Strategic Institute Initiative ‘Interactions between aquaculture and wild salmonids’. In addition, both IMR and the Norwegian Veterinary Institute added significant funding.

LITERATURE CITED

Aasetre J, Vik J (2013) Framing the environment—disputes and developments in the management of Norwegian salmon fjords. Ocean Coast Manag 71:203−212

Asplin L, Boxaspen KK, Sandvik AD (2011) Modeling the distribution and abundance of planktonic larval stages of Lepeophtheirus salmonis in Norway. In: Jones S, Beamish R (eds) Salmon lice: an integrated approach to understanding parasite abundance and distribution. Wiley-Blackwell, Oxford, p 31–50

Asplin L, Johnsen IA, Sandvik AD, Albretsen J, Sundfjord V, Aure J, Boxaspen KK (2014) Dispersion of salmon lice in the Hardangerfjord. Mar Biol Res 10:216−225

Bates D, Maechler M, Bolker B, Walker S (2014) lme4: Linear mixed-effects models using Eigen and S4. R package version 1.1-7. Available at http://CRAN.R-project.org/ package=lme4

Bjørn PA, Finstad B (2002) Salmon lice, Lepeophtheirus salmonis (Krøyer), infestation in sympatric populations of Arctic char, Salvelinus alpinus (L.), and sea trout, Salmo trutta (L.), in areas near and distant from salmon farms. ICES J Mar Sci 59:131−139

Bjørn PA, Finstad B, Kristoffersen R, McKinley RS, Rikardsen AH (2007) Differences in risks and consequences of salmon louse, Lepeophtheirus salmonis (Krøyer), infestation on sympatric populations of Atlantic salmon, brown trout, and Arctic charr within northern fjords. ICES J Mar Sci 64:386−393

Bjørn PA, Sivertsgård R, Finstad B, Nilsen R, Serra-Llinares RM, Kristoffersen R (2011) Area protection may reduce salmon louse infection risk to wild salmonids. Aquacult Environ Interact 1:233−244

Boxaspen K (2006) A review of the biology and genetics of sea lice. ICES J Mar Sci 63:1304−1316

Bricknell IR, Dalesman SJ, O’Shea B, Pert CC, Mordue Luntz AJ (2006) Effect of environmental salinity on sea lice Lepeophtheirus salmonis settlement success. Dis Aquat Org 71:201−212

Burnham KP, Anderson DR (2002) Model selection and multimodel inference: a practical information-theoretic approach, Springer, New York, NY

Directorate of Fisheries (2013) Key figures from aquaculture industry. Available at www.fiskeridir.no

Dobson AP, Hudson PJ (1986) Parasites, disease and the structure of ecological communities. Trends Ecol Evol 1: 11−15

Finstad B, Bjørn PA (2011) Present status and implications of salmon lice on wild salmonids in Norwegian coastal

zones. In: Jones S, Beamish R (eds) Salmon lice: an integrated approach to understanding parasite abundance and distribution. Wiley-Blackwell, Oxford, p 281–305 Finstad B, Økland F, Thorstad EB, Bjørn PA, McKinley RS (2005) Migration of hatchery-reared Atlantic salmon and wild anadromous brown trout post-smolts in a Norwegian fjord system. J Fish Biol 66:86−96

Finstad B, Bjørn PA, Todd CD, Whoriskey F, Gargan PG, Forde G, Revie C (2011) The effect of sea lice on Atlantic salmon and other salmonid species. In: Aaas Ø, Einum S, Klemetsen A, Skurdal J (eds) Atlantic salmon ecology. Wiley-Blackwell, Oxford, p 253–276

Gargan PG, Tully O, Poole WR (2003) Relationship between sea lice infestation, sea lice production and sea trout survival in Ireland, 1992-2001. In: Mills D (ed) Salmon at the edge. Blackwell Science Ltd., Oxford, p 119–135

Gjelland KØ, Serra-Llinares RM, Hedger RD, ArechavalaLopez P and others (2014) Effects of salmon lice infection on the behaviour of sea trout in the marine phase. Aquacult Environ Interact 5:221−233

Hatcher MJ, Dick JTA, Dunn AM (2006) How parasites affect interactions between competitors and predators. Ecol Lett 9:1253−1271

Helland IP, Finstad B, Uglem I, Diserud OH and others (2012) What governs sea lice infections of wild salmonids? Statistical analyses of data from the Norwegian national sea lice monitoring, 2004-2010. NINA Report 891. Norwegian Institute for Nature Research, Trondheim (in Norwegian)

Heuch PA, Mo TA (2001) A model of salmon louse production in Norway: effects of increasing salmon production and public management measures. Dis Aquat Org 45: 145−152

Jackman S (2014) pscl: Classes and methods for R developed in the Political Science Computational Laboratory, Stanford University. Department of Political Science, Stanford University, Stanford, CA. R package version 1.4.6. Available at http://pscl.stanford.edu/

Jansen PA, Kristoffersen AB, Viljugrein H, Jimenez D, Aldrin M, Stien A (2012) Sea lice as a density-dependent constraint to salmonid farming. Proc R Soc Lond B Biol Sci 279:2330−2338

Johansen LH, Jensen I, Mikkelsen H, Bjørn PA, Jansen PA, Bergh O (2011) Disease interaction and pathogens exchange between wild and farmed fish populations with special reference to Norway. Aquaculture 315: 167−186

Johnsen IA, Fiksen Ø, Sandvik AD, Asplin L (2014) Vertical salmon lice behaviour as a response to environmental conditions and its influence on regional dispersion in a fjord system. Aquacult Environ Interact 5:127−141

Jones SRM, Bruno DW, Madsen L, Peeler EJ (2015) Disease management mitigates risk of pathogen transmission from maricultured salmonids. Aquacult Environ Interact 6:119−134

Kristoffersen AB, Rees EE, Stryhn H, Ibarra R, Campisto JL, Revie CW, St-Hilaire S (2013) Understanding sources of sea lice for salmon farms in Chile. Prev Vet Med 111: 165−175

Kristoffersen AB, Jimenez D, Viljugrein H, Grøntvedt RN, Stien A, Jansen PA (2014) Large scale modelling of salmon lice (Lepeophtheirus salmonis) infection pressure based on lice monitoring data from Norwegian salmonid farms. Epidemics 9:31−39

Krkošek M, Bateman A, Proboszcz S, Orr C (2010) Dynamics

of outbreak and control of salmon lice on two salmon farms in the Broughton Archipelago, British Columbia. Aquacult Environ Interact 1:137−146

| |
|---|


Lindenmayer DB, Likens GE (2009) Adaptive monitoring: a new paradigm for long-term research and monitoring. Trends Ecol Evol 24:482−486

| |
|---|


MacKenzie K, Longshaw M, Begg GS, McVicar AH (1998) Sea lice (Copepoda: Caligidae) on wild sea trout (Salmo trutta L.) in Scotland. ICES J Mar Sci 55:151−162

| |
|---|


Middlemas SJ, Fryer RJ, Tulett D, Armstrong JD (2013) Relationship between sea lice levels on sea trout and fish farm activity in western Scotland. Fish Manag Ecol 20: 68−74

| |
|---|


Murray AG, Hall M (2014) Treatment rates for sea lice of Scottish inshore marine salmon farms depend on local (sea loch) farmed salmon biomass and oceanography. Aquacult Environ Interact 5:117−125

| |
|---|


Nichols JD, Williams BK (2006) Monitoring for conservation. Trends Ecol Evol 21:668−673

| |
|---|


Patanasatienkul T, Sanchez J, Rees EE, Pfeiffer D, Revie CW (2015) Space-time cluster analysis of sea lice infestation (Caligus clemensi and Lepeophtheirus salmonis) on wild juvenile Pacific salmon in the Broughton Archipelago of Canada. Prev Vet Med 120:219−231

| |
|---|


Penston MJ, Millar CP, Zuur A, Davies IM (2008) Spatial and temporal distribution of Lepeophtheirus salmonis (Kroyer) larvae in a sea loch containing Atlantic salmon, Salmo salar L., farms on the north-west coast of Scotland. J Fish Dis 31:361−371

Pike AW, Wadsworth SL (1999) Sea lice on salmonids: their biology and control. Adv Parasitol 44:233–337

R Development Core Team (2012) R: a language and environment for statistical computing. R Foundation for Statistical Computing, Vienna

| |
|---|


Rees EE, St-Hilaire S, Jones SR, Krkošek M and others (2015) Spatial patterns of parasite infection among wild and captive salmon in western Canada. Landsc Ecol 30: 989−1004

Revie C, Dill L, Finstad B, Todd CD (2009) Sea Lice Working Group Report. NINA Special Report 39. NINA, Trondheim

| |
|---|


Reynolds JH, Thompson WL, Russell B (2011) Planning for success: identifying effective and efficient survey designs for monitoring. Biol Conserv 144:1278−1284

| |
|---|


Rikardsen AH (2004) Seasonal occurrence of sea lice Lepeophtheirus salmonis on sea trout in two north Norwegian fjords. J Fish Biol 65:711−722

| |
|---|


Rogers LA, Peacock SJ, McKenzie P, DeDominicis S and others (2013) Modeling parasite dynamics on farmed salmon for precautionary conservation management of wild salmon. PLoS ONE 8:e60096

| |
|---|


Rózsa L, Reiczigel J, Majoros G (2000) Quantifying parasites

Editorial responsibility: Kenneth Black, Oban, UK

in samples of hosts. J Parasitol 86:228−232

| |
|---|


Salama NKG, Rabe B (2013) Developing models for investigating the environmental transmission of diseasecausing agents within open-cage salmon aquaculture. Aquacult Environ Interact 4:91−115

| |
|---|


Samsing F, Solstorm D, Oppedal F, Solstorm F, Dempster T (2015) Gone with the flow: current velocities mediate parasitic infestation of an aquatic host. Int J Parasitol 45: 559−565

| |
|---|


Serra-Llinares RM, Bjørn PA, Finstad B, Nilsen R, Harbitz A, Berg M, Asplin L (2014) Salmon lice infection on wild salmonids in marine protected areas: an evaluation of the Norwegian ‘National Salmon Fjords’. Aquacult Environ Interact 5:1−16

| |
|---|


Sims M, Bjorkland R, Mason P, Crowder LB (2008) Statistical power and sea turtle nesting beach surveys: How long and when? Biol Conserv 141:2921−2931

| |
|---|


Stien A, Bjørn PA, Heuch PA, Elston DA (2005) Population dynamics of salmon lice Lepeophtheirus salmonis on Atlantic salmon and sea trout. Mar Ecol Prog Ser 290: 263−275

| |
|---|


Taranger G, Karlsen Ø, Bannister R, Glover K and others (2015) Risk assessment of the environmental impact of Norwegian Atlantic salmon farming. ICES J Mar Sci 72: 997−1021

| |
|---|


Thorstad EB, Todd CD, Uglem I, Bjørn PA and others (2015) Effects of salmon lice Lepeophtheirus salmonis on wild sea trout Salmo trutta—a literature review. Aquacult Environ Interact 7:91−113

Todd CD, Walker AM, Hoyle JE, Northcott SJ, Walker AF, Ritchie MG (2000) Infestations of wild adult Atlantic salmon (Salmo salar L.) by the ectoparasitic copepod sea louse Lepeophtheirus salmonis Krøyer: prevalence, intensity and the spatial distribution of males and females on the host fish. Hydrobiologia 429:181−196

Tompkins DM, Dunn AM, Smith MJ, Telfer S (2011) Wildlife diseases: from individuals to ecosystems. J Anim Ecol 80: 19−38

| |
|---|


Torrissen O, Jones S, Asche F, Guttormsen A and others

(2013) Salmon lice—impact on wild salmonids and salmon aquaculture. J Fish Dis 36:171−194

| |
|---|


Tveiten H, Bjørn PA, Johnsen HK, Finstad B, McKinley RS (2010) Effects of the sea louse Lepeophtheirus salmonis on temporal changes in cortisol, sex steroids, growth and reproductive investment in Arctic charr Salvelinus alpinus. J Fish Biol 76:2318−2341

| |
|---|


Vollset KW, Barlaup BT (2014) First report of winter epizootic of salmon lice on sea trout in Norway. Aquacult Environ Interact 5:249−253

Zuur AF, Ieno EN, Walker NJ, Saveliev AA, Smith GM

(2009) Mixed effects models and extensions in ecology with R. Springer, New York, NY

Submitted: June 10, 2015; Accepted: October 19, 2015 Proofs received from author(s): November 25, 2015

