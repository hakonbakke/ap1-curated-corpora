<!-- page 1 -->
Preventive Veterinary Medicine 121 (2015) 132–141
Contents lists available at ScienceDirect
Preventive Veterinary Medicine
journal homepage: www.elsevier.com/locate/prevetmed
Space–time modelling of the spread of pancreas disease (PD) within
and between Norwegian marine salmonid farms
M. Aldrin a,c,∗, R.B. Huseby a, P.A. Jansen b
a Norwegian Computing Center, P.O. Box 114, Blindern, N-0314 Oslo, Norway
b Norwegian Veterinary Institute, P.O. Box 750, Sentrum N-0106 Oslo, Norway
c Department of Mathematics, University of Oslo, P.O. Box 1053, Blindern, N-0317 Oslo, Norway
a r t i c l e
i n f o
Article history:
Received 5 January 2015
Received in revised form 28 May 2015
Accepted 2 June 2015
Keywords:
Bayesian methods
Disease dynamics
Infection pathway
Aquaculture
Epidemiology
a b s t r a c t
Infectious diseases are a constant threat to industrialised farming, which is characterised by high densities
of farms and farm animals. Several mathematical and statistical models on spatio-temporal dynamics of
infectious diseases in various farmed host populations have been developed during the last decades.
Here we present a spatio-temporal stochastic model for the spread of a disease between and within
aquaculture farms. The spread between farms is divided into several transmission pathways, including (i)
distance related spread and (ii) other types of contagious contacts. The within-farm infection dynamics
is modelled by a susceptible–infected–recovered (SIR) model. We apply this framework to model the
spread of pancreas disease (PD) in salmon farming, using data covering all farms producing salmonids
over 9 years in Norway. The motivation for the study was partly to unravel the spatio-temporal dynamics
of PD in salmon farming and partly to use the model for scenario simulation of PD control strategies. We
ﬁnd, for example, that within-farm infection dynamics vary with season and we provide estimates of the
timing from unobserved infection events to disease outbreaks on farms are detected. The simulations
suggest that if a strategy involving culling of infectious cohorts is implemented, the number of detected
disease outbreaks per year may be reduced by 57% after the full effect has been reached. We argue that
the high detail and coverage of data on salmonid production and disease occurrence should encourage
the use of simulation modelling as a means of testing effects of extensive control measures before they
are implemented in the salmon farming industry.
© 2015 Elsevier B.V. All rights reserved.
1. Introduction
Infectious diseases are a constant threat to industrialised farm-
ing, which is characterised by high densities of farms and high
densities of farm animals. Several mathematical and statistical
models on spatio-temporal dynamics of infectious diseases in
farmed host populations have recently been developed and applied
to different diseases in livestock, such as foot-and-mouth dis-
ease, swine fever, blue-tongue, infectious salmon anaemia and
bovine tuberculosis (Keeling et al., 2001; Diggle, 2006; Höhle,
2009; Szmaragd et al., 2009; Aldrin et al., 2011; Brooks-Pollock
et al., 2014). In these models, probabilities of infection between
farms typically relate to between-farm distance. The relationship
between distance and probability of infection is often referred to as
∗Corresponding author at: Norwegian Computing Center, P.O. Box 114, Blindern,
N-0314 Oslo, Norway. Tel.: +47 22 85 26 58; fax: +47 22 69 76 60.
E-mail address: magne.aldrin@nr.no (M. Aldrin).
transmission kernels (Keeling et al., 2001; Szmaragd et al., 2009),
and play an important role.
We have developed a spatio-temporal stochastic model for
the spread of pancreas disease (PD) in marine ﬁsh farms pro-
ducing salmonids, i.e. Atlantic salmon (Salmo salar) and rainbow
trout (Oncorhynchus mykiss), in Norway. The model is a mecha-
nistic model constructed to account for known, likely or potential
transmission pathways between farms and for factors that may
affect susceptibility or infectiousness (e.g. the number of farm
animals). The within-farm infection is modelled by an internal
SIR (susceptible–infected–recovered) model. The model is formu-
lated within a Bayesian framework and the model parameters are
estimated from available data using Markov Chain Monte Carlo
(MCMC) techniques.
The motivation for the study is twofold. First, by formulating a
framework of relatively detailed biological processes of importance
to the propagation and spread of PD, and then ﬁt this to a large
historical base of observational data, we aim to gain insight into
the spatio-temporal dynamics of the disease. Second, given that
http://dx.doi.org/10.1016/j.prevetmed.2015.06.005
0167-5877/© 2015 Elsevier B.V. All rights reserved.


<!-- page 2 -->
M. Aldrin et al. / Preventive Veterinary Medicine 121 (2015) 132–141
133
the model captures spatio-temporal trends in the propagation and
spread of PD, we believe that it can be used to investigate effects of
extensive disease control measures by scenario-simulations, before
they are implemented in practice. We also believe that our mod-
elling framework can be useful also for other types of infectious
diseases in both land-based farms and aquaculture farms (see Sec-
tion 7 in Supplementary material).
2. Materials and methods
2.1. Salmonid farming and PD
Farm production of salmonids comprises a freshwater juvenile
phase, followed by a marine grow out phase, which is the focus of
this study. The production of salmonids on a marine farm typically
initiates by stocking juvenile smolts to net-pens either in spring or
in autumn. Smolts are kept in the marine farms for about 1.5 years
after which they are slaughtered for food consumption. Only ﬁsh
of the same year class of age are kept on a given farm and we term
this a cohort throughout the present paper. After slaughtering, it is
mandatory to fallow the farm for a period of at least two months
before stocking a new cohort of salmonids. Occasionally ﬁsh may
be moved from one marine farm location to a new empty farm
location, in which case a new farm will initially report ﬁsh weights
larger than expected for juvenile smolts.
PD is currently one of the most important diseases in Norwe-
gian aquaculture with regard to economic impact and ﬁsh welfare.
The disease is caused by the salmonid alpha virus (SAV) and mani-
fests in increased, but variable, mortality and reduced appetite and
growth (Jansen et al., 2014). When a farm becomes infected with
PD, this may at some time be detected and then reported (which is
mandatory upon detection). We will call this a detected outbreak
or simply an outbreak. More details on salmonid farming and PD
are given in Section 1 in the Supplementary Material.
2.2. Data
Our data consist of information on all 1412 Norwegian marine
farms producing salmonids in any month from February 2003 to
February 2012. For each farm, we know its geographic location and
its seaway distances to all other farms (truncated from above at
100 km). Furthermore, we have farm-level monthly data during the
observation period. These include numbers of ﬁsh, mean weights
of ﬁsh, seawater temperatures, and whether there were detected
outbreaks of PD in given farms and months.
We transform the time-discrete seawater temperatures into
continuous-time temperatures by ﬁrst assigning the monthly tem-
perature to the 15th of each month and then calculating the
temperatures at intermediate time points by linear interpola-
tion. Likewise, we calculate continuous-time seawater temperature
changes over one month by ﬁrst calculating the temperature dif-
ferences from 15th in one month to the 15th in the next month,
and again using linear interpolation for time points in-between.
Within the data period, each salmon farm normally had several
consecutive periods of production of ﬁsh populations, interrupted
by periods of fallowing (no ﬁsh on the farm). The ﬁsh population
within a production period (from stocking to removal) is termed a
cohort and the present data consists of 4332 cohorts with a total
of 62 408 farm-months of cohort production. 645 of the cohorts
were active at the start of the data period and have thus unknown
stocking times, whereas 519 cohorts have unknown removal times
because they were active at the end of the data period. Each cohort is
classiﬁed according to Kristoffersen et al. (2009), into either smolts
(directly stocked from freshwater into marine farms, 73% of all
cohorts) or relocated ﬁsh (moved from other farms).
Fig. 1 shows the locations of all Norwegian salmonid farms that
actively produced salmonids any month during the study period.
An example with a closer look at the farms that were active in an
area on the South-West coast of Norway and their PD-infection
status in May 2010, is also shown. Of the latter, 111 farms were
actively producing salmonids in May 2010. Of these, 31 farms had
a PD diagnosis at that time, whereas 38 farms got a PD diagnosis
later in the same production period.
The monthly number of active farms varied between 471 and
706 (Fig. 2, panel a). The various farms had on average 6.3 other
farms within a seaway distance of 10 km, and 1.2 farms within a
distance of 3 km. Farms produced between one and nine consecu-
tive cohorts, and the mean production period for a cohort was 15
months. During a production period, the number of ﬁsh varies, but
is usually at the maximum at or near the start of the period. The
Fig. 1. Location of salmonid farms. The right panel shows marine farms that were active in the period February 2003–February 2012 in the whole of Norway. The left panel
shows marine farms in the enlarged South-West coastal area that were actively producing salmonids between February 2003 and February 2012. PD status for those active
in May 2010 indicates whether a salmonid farm during the current production period either (i) detected a PD outbreak in May 2010 or earlier (red dots); (ii) detected a PD
outbreak after May 2010 (yellow dots); or (iii) did not detect a PD outbreak (green dots).


<!-- page 3 -->
134
M. Aldrin et al. / Preventive Veterinary Medicine 121 (2015) 132–141
(a)
(b)
(c)
(d)
2003
2004
2005
2006
2007
2008
2009
2010
2011
400
500
600
700
800
Number of active farms
2003
2004
2005
2006
2007
2008
2009
2010
2011
5
10
15
Temperature (degrees C)
2003
2004
2005
2006
2007
2008
2009
2010
2011
0
5
10
15
20
25
Number of outbreaks
2003 2004 2005 2006 2007 2008 2009 2010 2011
0.0
0.2
0.4
0.6
Number of fish (millions)
Fig. 2. Time plots of monthly values of (a) the number of active farms, (b) the average seawater temperature, (c) the number of detected PD outbreaks, (d) the average
number of ﬁsh per farm.
average number of ﬁsh was 785 000 (maximum 6.5 millions, min-
imum 100). The mean monthly ﬁsh weight in cohorts varied from
20 g to 15 kg and average weight over all cohort months was 2.0 kg.
The mean seawater temperature was 8.9 ◦C, and the monthly aver-
age over farms varied from 3.7 ◦C to 15.5 ◦C (Fig. 2, panel b). The
variation between monthly temperatures on a farm level varied
between −0.5 ◦C and 19.9 ◦C.
Fish farms sharing a common concession identity in the aqua-
culture licence register were deﬁned to constitute a local contact
network (see Section 1, Supplementary Material).
The monthly number of detected PD outbreaks was on average
5.4 (588 outbreaks in total) and varied between 0 and 22 (Fig. 2,
panel c). 96% of these outbreaks occurred south of Hustadvika
(62◦57′ N) in Southern Norway. Only 46% of the ﬁsh cohorts were
farmed in this area.
2.3. Model framework
The model is a hierarchical model consisting of several sub-
models. It is deﬁned on a continuous time scale, although the data
are in discrete time. The reason for specifying the model in continu-
ous time is that the timing of infection and outbreak events become
unique so there are no problems with ties. We assume that a ﬁsh
cohort during its production period is either susceptible to infec-
tion, or it is infected and then also infectious to other ﬁsh cohorts.
Each ﬁsh cohort can either (i) already be infected when it is stocked,
(ii) become infected later in the production period, or (iii) remain
uninfected, until it is removed. This is described by a simple model
for being infected when stocked and by a more complex model for
becoming infected after stocking. Once a cohort becomes infected,
it may infect other cohorts. In addition, it may develop a detected
outbreak of disease some time after the infection time. The latter
is modelled as a separate outbreak process. Fig. 3 illustrates how
the infection status may change over time for four different ﬁsh
cohorts, whereas Fig. 4 gives an overview of the model. A ﬁsh cohort
is stocked at a ﬁxed time that is known and treated as a ﬁxed quan-
tity in our model, but with a probability  for already being infected
when stocked. A ﬁsh cohort that is uninfected at stocking is suscep-
tible and can be infected with a rate (t) which varies over time.
time
(a)
stocked
removed
susceptible
time
(b)
infected
when stocked
detected
outbreak
removed
infectious
time
(c)
stocked
removed
infected
detected
outbreak
susceptible
infectious
time
(d)
stocked
removed
infected
susceptible
infectious
Fig. 3. Illustration of susceptible and infectious ﬁsh cohorts, with times of stocking,
infection, detected outbreaks and removal (slaughtering).
An infected ﬁsh cohort may develop a detected outbreak with a
time varying rate (t). Finally, the ﬁsh cohort is removed (either
slaughtered or moved to another farm) at a ﬁxed, known time.
We regard infectiousness of a cohort, and the probability of
detecting a disease outbreak, to depend on the proportion of
ρ
ρ
λ
κ
Fig. 4. Overview of the model.


<!-- page 4 -->
M. Aldrin et al. / Preventive Veterinary Medicine 121 (2015) 132–141
135
ﬁsh infected. Therefore, the progress of infection within cohorts
is modelled as a separate sub-process that is included in both
the infection and the outbreak processes. Put together for all
ﬁsh cohorts, these sub-models constitute the full model for the
spatio-temporal spread of the disease. The model is estimated by
a Bayesian approach using latent variables to represent the unob-
served data.
At the start of the data period, many ﬁsh cohorts have already
started their production periods. Some adjustments of the mod-
els and the data have been made to handle this in an initialisation
period before the start of the data period (see Section 5, Supple-
mentary Material).
In the following, we ﬁrst deﬁne notation for observed and
unobserved data, and then we describe the various sub-models.
Information on estimation, probability distributions of the data,
prior distribution and the MCMC algorithm used is given in Sections
4 and 6 in the Supplementary Material.
2.3.1. Notation for observed and unobserved data
Let tstart (1 February 2003) and tend (28 February 2012) denote
the start and the end of the data period, respectively. For a given
cohort i we know the time the cohort was stocked, termed tsto
i
,
and the time the cohort was removed, termed trem
i
. These are in
reality given only on a monthly time scale, but we attribute stocking
and removal times to the middle of the month in question. Some
of the cohorts were stocked prior to tstart, and for these cohorts
the stocking times are actually unknown. However, their stocking
times are estimated (see Section 5, Supplementary Material) and
considered known in our model. For a given cohort, we also know
its location, its size and whether it is a relocated cohort or not. All
these quantities are regarded as external, ﬁxed variables.
We also know ıout
i
, an indicator variable, which is 1 if an out-
break of the disease has been detected for cohort i and 0 otherwise.
The corresponding outbreak time, termed tout
i
, is interval censored
since it is only known with a monthly time resolution. These two
variables are stochastic and depend on the outbreak process.
In addition, we include the following unobserved data in our
model: (i) an indicator variable ısto
i
, which is 1 if the cohort is
already infected at the time of stocking and 0 otherwise; and (ii)
an indicator variable ıinf
i
, which is 1 if the cohort is infected after
stocking and 0 otherwise, with a corresponding time of infection
termed tinf
i
.
We let ısto, ıinf, tinf, ıout and tout denote the vectors of unob-
served and observed stochastic data. Both ısto
i
, ıinf
i
and ıout have 4
332 elements (the number of ﬁsh cohorts) and tout has 588 ele-
ments (the number of detected outbreaks). tinf has an unknown
number of elements equal to the sum of infection episodes. In addi-
tion, our model consists of a set of unknown parameters, which will
be described in the subsequent sections. The vector of unknown
parameters is denoted ω and consists of 23 parameters in the ﬁnal
model.
2.3.2. Model for cohorts infected at stocking
We assume that there is a probability  for a cohort already
being infected when it is stocked, i.e. ısto
i
∼Bin(1, ). This probability
may be higher for relocated cohorts compared to smolt cohorts. The
probability distribution for the ısto
i
is then given by
p(ısto
i
|ω) = p(ısto
i
|) = ısto
i
· (1 −)1−ısto
i ,
(1)
where p() here and elsewhere denotes a probability distribution,
and where  = r for a relocated cohort and  = o for an ordinary
cohort.
2.3.3. The infection process model
A key concept in the infection process model is the infection
rate i(t) for a given susceptible ﬁsh cohort i at a given time
t. i(t)dt is then approximately the probability that the cohort
will be infected in the small time interval from t to t + dt. We
break down i(t) into the contribution from four possible trans-
mission pathways. We assume that conditioned on the history up
to time t, transmission through each pathway may occur inde-
pendently of the other pathways. Since the infection rates are
small probabilities, the contributions from the four pathways may
then be added to a total infection rate. In addition, the infec-
tion rate for a ﬁsh cohort i depends on factors inﬂuencing the
cohort susceptibility, and these factors are included as multiplica-
tive terms in the infection rate. The total infection rate for ﬁsh
cohort i at time t has the following additive-multiplicative struc-
ture
i(t) = ısusc
i
(t) · b(t) · ix(t) · [d
i (t) + c
i (t) + p
i (t) + o
i (t)].
(2)
The three multiplicative factors in Eq. (2) are: (i) ısusc
i
(t), an
at-risk indicator being 1 when ﬁsh cohort i is susceptible and 0
otherwise (ısusc
i
(t) = 1 if ısto
i
= ıinf
i
= 0 or if ısto
i
= 0, ıinf
i
= 1 and
t < tinf
i
); (ii) b(t), a time-varying proportionality factor common
for all ﬁsh cohorts, called the baseline hazard (more details are
given in Section 2.3.3.5); and (iii) ix(t), a factor proportional to the
susceptibility of ﬁsh cohort i and functionally related to explanatory
variables x (more details are given in Section 2.3.3.5).
The four additive terms in Eq. (2) represent alternative trans-
mission pathways: (i) d
i (t), the relative rate of infection from
infectious ﬁsh cohorts in the neighbourhood, depending on dis-
tance to infected ﬁsh cohorts; (ii) c
i (t), the relative rate of infection
from infectious ﬁsh cohorts in the same local contact network; and
(iii) p
i (t), the relative rate of infection from previous infected ﬁsh
cohorts at the same ﬁsh farm i; (iv) o
i (t), the relative rate of infec-
tion via other, non-speciﬁed, pathways.
The transmission pathways and expressions for the baseline
hazard, cohort susceptibility and cohort infectiousness are pre-
sented in more detail in the following sections. The full expression
for the infection process model is given in Section 2 in the Supple-
mentary Material.
2.3.3.1. Transmission pathways; distance. This component repre-
sents transmission from neighbourhood cohorts such that the risk
of infection is related to the seaway distances to the surrounding
infectious cohorts. This component has been associated with the
spread of infection via water currents (Viljugrein et al., 2009; Stene
et al., 2014), but could in principle represent any infection pathway
whose risk decreases with distance. The neighbourhood compo-
nent can be broken down into the sum of contributions from each
cohort j, denoted d
ij(t), such that d
i (t) = 
j /= id
ij(t). The contribu-
tion from cohort j is modelled as
d
ij(t) =  · exp
− · d˛
ij˛
· jz(t) · Ij(t),
(3)
where (i) dij is the seaway distance between ﬁsh cohorts i and j;
(ii)  and ˛ are parameters that express the effect of the seaway
distance for the risk of infection; (iii) jz(t) is a factor proportional
to the infectiousness of ﬁsh cohort j, and functionally related to
explanatory variables z (more details are given in Section 2.3.3.5);
and (iv) Ij(t) represents the relative infectiousness of a neighbour-
hood cohort j at time t. This can be interpreted as the proportion of
ﬁsh infected. Ij(t) is exactly zero when cohort j is non-infectious and
maximum when cohort j is infectious. It is modelled by an internal
SIR model described in Section 2.3.3.6. Note that the parameter 
is entered twice in Eq. (3), which provides the beneﬁcial property
that d
ij(t) = 0 if  is exactly 0.


<!-- page 5 -->
136
M. Aldrin et al. / Preventive Veterinary Medicine 121 (2015) 132–141
2.3.3.2. Contact network. Transmission from ﬁsh cohorts in the
same local contact network is included as an additional transmis-
sion pathway because such cohorts are likely to share personnel or
equipment. Also this component can be broken down into the sum
of contributions from each ﬁsh cohort j, denoted by c
ij(t), such that
c
i (t) = 
j /= ic
ij(t). The contribution from one single farm is mod-
elled similar to Eq. (3), but the term  · exp(− · d˛
ij/˛) in Eq. (3) is
replaced with a term  · Cij, giving
c
ij(t) =  · Cij · jz(t) · Ij(t).
(4)
Here, Cij is 1 if the ﬁsh cohorts i and j are in the same contact
network, and 0 otherwise. The parameter  is non-negative and
expresses the effect of being in the same contact network.
2.3.3.3. Previous infected cohorts. Transmission from a previous
infected ﬁsh cohort at the same ﬁsh farm may occur if the dis-
ease agent resides in the local farm environment after the infected
cohort has been removed. This transmission pathway is modelled
as
p
i (t) = p
i =  · ıprev
i
,
(5)
where ıprev
i
is an indicator variable being 1 if a previous ﬁsh cohort
at the same farm i was infectious at most six months prior to stock-
ing of the current ﬁsh cohort and 0 otherwise. This means that
ıprev
i
= 1 if there is a cohort j at the same farm with 0 < tsto
i
−trem
j
<
6 months and with either ısto
j
= 1 or ıinf
j
= 1. The parameter 
expresses the effect of previous infected cohorts. This term is anal-
ogous to an autoregressive term in time series models.
2.3.3.4. Other transmission pathways. Finally, transmission via
other pathways accounts for all other potential sources of infec-
tion. Such unspeciﬁed transmission is assumed to be constant in
time and space in the present application i.e.
o
i (t) = 0,
(6)
where 0 is a non-negative parameter. However, remember that
o
i (t) is multiplied by ısusc
i
(t) · b(t) · ix(t), so the product of these
terms varies both in time and between farms.
2.3.3.5. Baseline hazard, susceptibility, and infectiousness. The base-
line hazard b(t) is currently modelled as
b(t) = exp( 0 + 1 · l(t)).
(7)
where l is a linear function increasing from −1 to 1 during the data
period, and the k-s are parameters. This term can be generalised
by allowing for non-linear time dependency or seasonal variation.
The susceptibility factor ix(t) has the general form
ix(t) = exp

k
ˇkxik(t)

,
(8)
where the xik-s are explanatory variables that affect the suscep-
tibility of cohort i equally for all four transmission pathways and
the ˇ-s are parameters. In the current version of the model, ix(t)
depends on the number of ﬁsh and the mean weight of ﬁsh in the
cohort in month t. To be speciﬁc, it is modelled as
ix(t) = exp(ˇnxn
i (t) + ˇwxw
i (t)).
(9)
Here, xn
i (t) = log(ni(t) −
¯
log(n)), where ni(t) is the number of ﬁsh
in cohort i in month t, and
¯
log(n) is the mean of log(ni(t)) taken
over all cohorts and months. Likewise, xw
i (t) = log(wi(t) −
¯
log(w)),
where wi(t) is the mean weight of ﬁsh in cohort i in month t, and
¯
log(w) is the mean of log(wi(t)).
Table 1
Various models for the transmission rate 	.
Model
Eq. in Suppl.
Mat.
No. parameters
Constant
(2)
1
Seasonal, 1 pair of sine and cosine functions
(3)
3
Seasonal, 2 pairs of sine and cosine functions
(4)
5
Linear in sea temperature
(5)
2
Quadratic in sea temperature
(6)
3
Linear in sea temperature difference
(7)
2
The infectiousness factor jz(t) has the general form
jz(t) = exp

k

kzjk(t)

,
(10)
where the zjk-s are explanatory variables that affect the infectious-
ness of cohort j and the 
-s are parameters. Currently, only ﬁsh
numbers and mean weights of ﬁsh in the cohorts are included as
explanatory variables, i.e.
jz(t) = exp(
nzn
j (t) + 
wzw
j (t)),
(11)
where zn
j (t) = xn
j (t) and zw
j (t) = xw
j (t), i.e. the same variables that
were included in the susceptibility factor.
2.3.3.6. Modelling Ij(t) by an SIR model. To mimic the propagation of
infection within cohorts consisting of large numbers of individual
ﬁsh, we assume that the cohort-internal epidemic follows an SIR
model (e.g. Anderson and May, 1991). Thus, at time t a ﬁsh can be
either susceptible, infected, or recovered. We let Sj(t), Ij(t) and Rj(t)
denote the proportions of susceptible, infected and recovered ﬁsh
in cohort j at time t, where Ij(t) is included in Eqs. (3) and (4). Then
Sj(t) + Ij(t) + Rj(t) = 1.
(12)
At the time cohort j becomes infected, Ij(t) = I0 and Sj(t) = 1 −I0,
where I0 is a constant parameter. An SIR model is usually deﬁned
by a set of differential equations in continuous time, but this is
computationally demanding since it involves integration. Instead,
we evaluate the process states at discrete, monthly time steps, and
interpolate Ij(t) at intermediate time points to derive a continuous
process. Thus, starting at time t = tinf
j
with Ij(tinf
j
) = I0, future pro-
portions of susceptible and infected ﬁsh are ﬁrst calculated at a set
of discrete time points by
Sj(t + 1) = −	j(t′) · Ij(t) · Sj(t),
(13)
Ij(t + 1) = 	j(t′) · Ij(t) · Sj(t) − · Ij(t),
(14)
where the time unit is month. The proportions of infected
ﬁsh
at
intermediate
times
t < t′ < t + 1
are
further
given
by
Ij(t′) = [1 −(t′ −t)]Ij(t) + (t′ −t)Ij(t + 1). In an ordinary SIR model, both
the transmission rate 	 and the recovery rate  are assumed to be
constant, but here we use a more ﬂexible version and let 	 vary
both in time and between cohorts, and evaluate it at the midpoint
t′ between t and t + 1, i.e. t′ = t + 1/2. We ﬁt six different models for
	, one model where 	 is constant, two seasonal models and three
models where 	 depends on the sea temperatures. These models
are summarised in Table 1 and more details are given in Section 3
in the Supplementary Material.
2.3.4. The outbreak process model
Similar to the transmission model, the key concept in the mod-
elling of detected outbreaks is the outbreak rate for a given infected
ﬁsh cohort at time t. PD manifests in increased mortality and
reduced appetite and growth, and the probability of an outbreak
being detected increases with the proportion of ﬁsh infected. We


<!-- page 6 -->
M. Aldrin et al. / Preventive Veterinary Medicine 121 (2015) 132–141
137
therefore assume that the outbreak rate is proportional to the pro-
portion of infected ﬁsh Ii(t) modelled by Eq. (14), which was termed
the relative infectiousness in Eqs. (3) and (4). Let i(t) denote the
outbreak rate for a ﬁsh cohort i at time t, which is given by
i(t) = exp(0) · Ii(t),
(15)
where 0 is a parameter common for all cohorts.
2.3.5. The relative importance of a source of infection
The importance of each source of infection cannot be directly
read from Table 3, but can be derived from the model parameters
and the latent variables. We use the term relative importance of
a source of infection for the proportion of all infections that can
be attributed to that speciﬁc source. The relative importance of
infection prior to stocking is

1ninf 
i∈AllInf
ısto
i
,
(16)
where AllInf denotes all the ninf = 
i(ısto
i
+ ıinf
i
) infection episodes.
Furthermore, the relative importance of infection from neighbour-
ing farms related to seaway distance is given by

1ninf 
i∈AllInf
(ıinf
i
· d
i (tinf
i
))
(d
i (tinf
i
)
+ c
i (tinf
i
) + p
i (tinf
i
) + o
i (tinf
i
)),
(17)
and the relative importance of each of the other three sources in
Eq. (2) are deﬁned similarly.
2.4. Model selection and validation
We investigated the six models given by the variants of the SIR
model speciﬁed in Section 1 and chose the best model based on
the following cross validation experiment: ﬁrst, the ﬁsh cohorts
were randomly divided into ten groups (denoted by g ; g = 1, . . . 10)
with approximately equal numbers of cohorts in each group.
Then, the outbreak information for the cohorts in the ﬁrst group
(g = 1) was regarded as missing. Each of the candidate models
were re-estimated based on all data except the missing outbreak
information, so these “excluded” cohorts were still a part of the
transmission network. We then introduced a new indicator vari-
able (ıout
im ) which was 1 if farm i detects an outbreak in month m
and 0 otherwise, where m denotes a given month in the data period.
For each model, we computed the posterior probabilities for each
of these “excluded” cohorts in detecting an outbreak in a given
month m, i.e. pim = P(ıout
im = 1|Dobs
−g ) for cohort i in group g, where
Dobs
−g denotes all available data except the missing outbreak infor-
mation for the cohorts in the “excluded” group g. This procedure
was repeated for each group (g = 1, . . . 10).
For each cohort, the outbreak indicator ıout
im follows a multino-
mial distribution with ni + 1 categories, where ni is the number
of months that cohort i is active. Either cohort i had a detected
outbreak in one of these months (the ﬁrst ni categories, or it
never developed an outbreak that was detected (category ni + 1
with probability (1 −
mpim)). Ignoring potential dependencies
between cohorts, the cross validated log-likelihood for each model
M is then given by
CVLL(M)
=

i

m
ıout
im log(pim) + (1 −

m
ıout
im ) log(1 −

m
pim)

. (18)
Note that both ıout
im and pim are zero if cohort i is in-active in month
m. We chose the model with the highest value of CVLL. This criterion
takes into account both the occurrence and the timing of detected
outbreaks and is referred to as the logarithmic score in the literature
on proper scoring rules (Gneiting and Raftery, 2007).
The six model variants were validated in various ways. First,
based on the cross validation experiment, we calculated the pos-
terior probability for cohort i detecting an outbreak in any month
as pi =
mpim, and furthermore the average outbreak probabili-
ties p1 and p0 over all cohorts that detected an outbreak and over
those who didn’t, respectively. A model has predictive power if p1
is much higher than p0, so we used the ratio p1/p0 as a criterion
for model validation. This criterion ignores what month the out-
breaks are detected. Therefore, we additionally computed a similar
monthly based criterion p1m/p0m, where the averages p1m and p0m
were taken over given farm-months with and without outbreaks,
respectively.
We also validated the selected model by a simulation experi-
ment to check whether the estimated model was able to reproduce
(not only ﬁt) certain aspects of the data. First, the model was
estimated on all data, giving the posterior distributions for the
parameters ω and the latent variables Dlat. Then, starting at a time
t* > tstart, we simulated future infection episodes and detected out-
breaks until tend, conditioned on a random sample from the joint
posteriors for the parameters ω and all ısto
i
, ıinf
i
and tinf
i
until time
t* and furthermore on the full production history (i.e. stocking and
slaughtering times, and ﬁsh cohort sizes in the whole data period).
We took t* as 1 March 2004 and performed 200 simulations, each
conditioned on a new sample from the joint posteriors.
From the same simulation experiment, we computed a measure,
K(ds, dt), which takes into account the space–time relationships
between detected outbreaks. Given a detected outbreak, K(ds, dt)
is the average proportion of farm-months with other simultaneous
or previous detected outbreaks within a seawater distance ds and
time distance dt. This measure is inspired by Ripley’s K function for
spatial point processes (Ripley, 1988), and is given by
K(ds, dt) =

i∈Out
mi
m=mi−dt

j /= iI((dij ≤ds) ∩(ıout
jm = 1))

i∈Out
mi
m=mi−dt

j /= iI((dij ≤ds) ∩(ıact
jm = 1))
,
(19)
where (i) I(u) is an indicator function being 1 if u is true and 0 oth-
erwise; (ii) Out denotes all cohorts with detected outbreaks; (iii)
mi is the outbreak month for cohort i, and (iv) ıact
jm is an indicator
variable being 1 if farm j is active at month m and 0 otherwise. We
considered previous, but not future, outbreaks, because K is then
not inﬂuenced by end effects as long as dt ≤(t* −tstart). The simu-
lated times of outbreak detections were rounded to whole calendar
months, such that the K functions for simulated and real data could
be compared.
3. Results
3.1. Results for model selection and validation
The results of the cross validation experiment described in Sec-
tion 2.4 are summarised in Table 2. As a reference, the table also
includes the results for a naive model with a common constant out-
break rate for all cohorts from their stocking times to their removal
times.
The model with seasonal SIR transmission rate described by
two pairs of sine and cosine functions, and including both numbers
and weights of ﬁsh in the susceptibility and infectiousness factors,
has the highest predictive log likelihood and is thus our preferred
model. As expected, the ratio p1/p0 is near 1 for the naive predic-
tion (it differs from 1 only because of the randomness in the cross
validation experiment), but is between 7.6 and 7.7 for all variants of
our model, indicating that all models clearly have predictive power.
The corresponding monthly ratios p1m/p0m are between 4.8 and 6.2


<!-- page 7 -->
138
M. Aldrin et al. / Preventive Veterinary Medicine 121 (2015) 132–141
Table 2
Cross validated predictive measures for various models for the SIR transmission rate and for a model free reference prediction. The cross validated log likelihood CVLL is
reported as the difference from the model with highest CVLL.
Model
CVLL −max(CVLL)
p1
p0
p1/p0
p1m
p0m
p1m/p0m
Naive prediction – no model
−910.6
0.141
0.117
1.2
0.0078
0.0076
1.0
Constant
−79.0
0.537
0.070
7.7
0.0390
0.0081
4.8
Seasonal, 1 pair of sin/cos
−16.8
0.532
0.069
7.7
0.0450
0.0080
5.6
Seasonal, 2 pairs of sin/cos
0.0
0.533
0.070
7.6
0.0490
0.0080
6.2
Linear in temperature
−65.8
0.543
0.070
7.7
0.0410
0.0082
5.0
Quadratic in temperature
−73.0
0.542
0.070
7.7
0.0410
0.0082
5.0
Linear in temperature diff.
−48.4
0.535
0.071
7.6
0.0450
0.0081
5.5
(a)
2003 2004 2005 2006 2007 2008 2009 2010 2011
0
5
10
15
20
25
Number of outbreaks
(b)
Jan
Feb Mar
Apr May Jun
Jul
Aug Sep Oct Nov Dec
0
5
10
15
20
25
Number of outbreaks
Fig. 5. Simulated numbers of detected outbreaks from 10 simulations (thin lines) and the average of all 200 simulations (red, thick line), together with the observed numbers
(black, thick line). Panel a shows time plots of the monthly numbers of outbreaks and panel b shows the seasonal distribution of the outbreaks. (For interpretation of the
references to colour in this ﬁgure legend, the reader is referred to the web version of the article.)
for the various models. These are lower since it is easier to predict
whether a cohort detects an outbreak (p1 = 0.53 for the selected
model) than to predict exactly in which month the outbreak is
detected (p1m = 0.049 for the selected model).
The validation results from the simulation experiment are
shown in Figs. 5 and 6. Panel a in Fig. 5 shows the monthly number
of detected outbreaks in each of 10 simulations and the average
of all 200 simulations together with the observed numbers. The
overall pattern of the simulations is reasonably consistent with the
data. The average correlation between the observed and simulated
data series is similar to the average correlation between the sim-
ulated series (0.59 vs. 0.57). However, the seasonal pattern is less
pronounced in the simulations than in the observations (panel b)
in Fig. 5).
Panel a in Fig. 6 shows the K functions for the observed data,
for seaway distances from 2 to 50 km and for temporal distances
dt =0, 1, 2, 3, 6, 9 and 12 months. In addition, the limit values
K(∞, 0) = 0.016 and K(∞, 12) = 0.011, i.e. including all farms regard-
less of distance, are also shown. The curves indicate a pronounced
spatio-temporal clustering. Panel b in Fig. 6 shows the K function as
an average over 20 independent simulations of times of outbreak
detections, whereas panels c and d show the K functions for two
speciﬁc simulated samples. The curves from the simulated sam-
ples are lower than the corresponding curves for the observations,
Fig. 6. K functions for (a) observed outbreak history; (b) average of 20 simulated outbreak histories; (c) and (d) two separate simulated outbreak histories.


<!-- page 8 -->
M. Aldrin et al. / Preventive Veterinary Medicine 121 (2015) 132–141
139
Table 3
Overview of parameters with posterior means and 95% credible intervals for the model with a seasonal SIR transmission rate described by Eq. (4) in the Supplementary
Material.
Parameter description
Parameter symbol
Section
Posterior mean
95% C.I. lower
95% C.I. upper
P(infected at stocking)
o
2.3.2
0.0029
0.0002
0.0082
P(infected at stocking), relocated
r
2.3.2
0.0054
0.0002
0.0140
Distance effect

2.3.3.1
0.6251
0.3914
0.8297
Distance transformation
˛
2.3.3.1
0.4951
0.3528
0.7171
Effect of contact network

2.3.3.2
0.0011
0.0001
0.0030
Effect of previous infected cohorts

2.3.3.3
0.0008
0.0001
0.0026
Effect of other sources
0
2.3.3.4
37.1 × 10−6
6.4 × 10−6
107.1 × 10−6
Log baseline hazard intercept
 0
2.3.3.5
2.1149
1.2301
2.9748
Log baseline hazard coef., time
 1
2.3.3.5
−0.2791
−0.4912
−0.0527
Log susceptibility coef., log number of ﬁsh
ˇn
2.3.3.5
0.7712
0.5973
0.9734
Log susceptibility coef., log weight of ﬁsh
ˇw
2.3.3.5
0.0396
−0.0995
0.1526
Log infectiousness coef., log number of ﬁsh

n
2.3.3.5
0.4502
0.1067
0.7678
Log infectiousness coef., log weight of ﬁsh

w
2.3.3.5
0.7051
0.1960
1.2411
Initial proportion of infection in SIR
I0
2.3.3.6
0.1168
0.0710
0.1697
Recovery rate in SIR

2.3.3.6
0.5026
0.3801
0.6245
Logit transmission rate in SIR, intercept
	S2
0
Suppl. Mat.
−2.7222
−3.1702
−2.2671
Logit transmission rate in SIR, seasonal coef.
	S2
s1
Suppl. Mat.
0.9506
0.5719
1.4292
Logit transmission rate in SIR, seasonal coef.
	S2
c1
Suppl. Mat.
−0.0727
−0.3424
0.1898
Logit transmission rate in SIR, seasonal coef.
	S2
s2
Suppl. Mat.
−0.8138
−1.2328
−0.4757
Logit transmission rate in SIR, seasonal coef.
	S2
c2
Suppl. Mat.
0.8673
0.4150
1.3677
Log outbreak rate intercept
0
2.3.4
0.1798
−0.2506
0.7625
Used in initialisation
1
Suppl. Mat.
0.2367
0.0054
0.8580
Used in initialisation

Suppl. Mat.
13.8 × 10−6
0.3 × 10−6
54.7 × 10−6
implying that the simulated outbreaks are less clustered than the
real data.
3.2. The estimated model
The rightmost columns of Table 3 show the posterior means and
95% credible intervals for the parameters in the model selected in
Section 3.1. We will comment on some of these results.
There is a small (0.3% for smolts and 0.5% for relocated cohorts),
but (statistically) signiﬁcant (at the 5% level) probability for cohorts
alreadybeinginfectedwhenstocked.The riskof being infected from
infected neighbourhood farms decreases abruptly with increasing
seaway distance, as shown in Fig. 7, panel a. There the baseline
hazard parameter 1 is negative, implying that the baseline hazard
b(t) decreases over time. Cohort size, represented by the number
and weight of ﬁsh, has a pronounced effect on both susceptibility
and infectiousness.
Panel b in Fig. 7 shows how the transmission rate in the SIR
model varies by time of the year. Panels c and d in the same ﬁgure
show how the proportion of infected ﬁsh varies over time after the
infection episode, and illustrates that the time proﬁle depends on
the seasonal timing of the infection events in cohorts.
The relative importance was computed for each of the various
sources of infection (Section 2.3.5). Infection from infected neigh-
bouring farms is by far the most important source of infection,
accounting for 87.8% (95% C.I. 81.1–94.2%) of the infection events.
Infection from infected farms in the same contact network accounts
for 5.6% (C.I. 0.9–10.6%); infection related to previous infected
cohorts accounts for 2.8% (C.I. 0.3–6.2%); and infection from other,
non-speciﬁed sources accounts for 2.3% (C.I. 1.0–3.9%). In addition,
0
10
20
30
40
50
0.0
0.4
0.8
(a)
seaway distance (km)
relative effect
Posterior mean
95 % pointwise credible band
(b)
transmission rate
Jan Feb Mar Apr May Jun
Jul Aug Sep Oct Nov Dec
month in year
0
1
2
3
4
0
5
10
15
20
0.0
0.2
0.4
0.6
0.8
(c)
months after infection
proportion infected
0
5
10
15
20
0.0
0.2
0.4
0.6
0.8
(d)
months after infection
proportion infected
Fig. 7. Selected results from the estimated model. (a) Relative effect of the seaway distance. (b) Transmission rate as a function of time of year. (c) Time development of the
proportion of infected ﬁsh in a cohort infected 1 January. (d) Time development of the proportion of infected ﬁsh in a cohort infected 1 April.


<!-- page 9 -->
140
M. Aldrin et al. / Preventive Veterinary Medicine 121 (2015) 132–141
2003 2004 2005 2006 2007 2008 2009 2010 2011
0
5
10
15
20
25
Number of outbreaks
Observed
Average of simulations, unchanged strategy
Average of simulations, new strategy
Fig. 8. Monthly averages of detected outbreaks in scenario simulations representing
(i) the unchanged strategy and (ii) the new strategy with slaughtering of infected
cohorts.
about 1.5% (C.I. 0.2–3.4%) of the infected cohorts are estimated to
already be infected when stocked.
Other interesting quantities can also be derived. We estimate
that 20.3% of all cohorts were infected (C.I. 18.9–21.7%), even
though an outbreak was only detected in 13.6% of the cohorts in
the data set. This means that about 1/3 (posterior mean 33.4%, C.I.
28.8–37.9%) of all infected cohorts did not result in a detected out-
break. The average time from infection to detection of an outbreak
is estimated to be 3.6 months (C.I. 3.1–4.2 months) for infected
cohorts in which an outbreak was detected.
3.3. Scenario simulations
The estimated model can be used to evaluate and compare the
overall effect of various management strategies by scenario simula-
tions. Alternative strategies may for instance involve re-location of
farms, vaccination or slaughtering strategies. Here, we demonstrate
how to compare two management strategies that differ with regard
to depopulating cohorts with detected PD outbreaks. The ﬁrst strat-
egy resembles the regulations enforced north of the endemic PD
area delimited by Hustadvika (62◦57′ N) from 2008 and onwards,
where farmers were required to remove (slaughter) ﬁsh cohorts
after detection of PD. In the second strategy, no restrictions are
imposed on removal of infected cohorts, agreeing with the practice
south of Hustadvika. Here we explore the outcome of a scenario
where the ﬁrst restrictive culling strategy is implemented for all
Norwegian farms, and compare this with a scenario based on the
second strategy where no restrictions are imposed on infected
cohorts.
We investigate this by using the model for scenario simulations.
To ensure realistic production conditions, we base the simulations
on the observed production history. First, we simulate detected
outbreaks in the period t*= 1 March 2004 to tend= 28 February 2012.
We performed 200 simulations, each conditioned on a new sample
from the joint posterior. In these simulations, cohorts north of
Hustadvika were removed at most one month after a simulated
detected outbreak occurred. In reality this was only enforced from
2008 and onwards, but there were very few outbreaks in this area
before 2008. Then, using the same 200 parameter sets as for the
ﬁrst simulations, we simulated detected outbreaks in the same
period on the condition that infected cohorts were removed within
a month after a simulated detected outbreak occurred, regardless
of farm location. Fig. 8 shows the monthly number of detected
outbreaks for each strategy, averaged over the simulations. The
number of detected outbreaks decreases the ﬁrst three years with
the new strategy, before it stabilises. On average over the last ﬁve
years, the new strategy reduces the number of detected outbreaks
by 42 per year (C.I. 18–69). Compared to the strategy followed
in reality, this was a reduction of 57% (C.I. 24–90%). The price for
this improvement is that the ﬁsh must be slaughtered before it is
economically optimal, and there is a loss of 174 (C.I. from 4 to 331)
farm months of production per year due to early removal of cohorts.
4. Discussion
In this paper, we have presented a structured stochastic model
for the spread of an infectious disease between farms. The model is
an extended and improved version of a model we have used previ-
ously to model both PD and other salmonid diseases (Aldrin et al.,
2010, 2011). The most important improvements in the present
model are that (i) it is now a fully speciﬁed stochastic model that
can be used for scenario simulations; (ii) the infection and outbreak
processes are modelled separately, which allows for ﬁsh cohorts
being infected without an outbreak being detected; (iii) the infec-
tion intensity, and thus infectiousness, within infected ﬁsh cohorts
is allowed to vary over time according to a seasonal SIR model; and
(iv) the effect of seaway distance is modelled by a two-parametric
curve, as opposed to a one-parametric exponential curve that was
used previously. In addition, the data period used for estimation
has been extended with ﬁve years.
Extending the study period and expanding parts of the model
to incorporate more of the disease dynamics, generally reproduced
many of the ﬁndings from previous studies, e.g. emphasising the
importance of distance related spread of PD between farms (Aldrin
et al., 2010). However, the expansion also produced novel outputs
of potential importance to controlling the spread of this disease.
For example, new insight into the timing of infection events and
subsequent outbreak events, and how the SIR dynamics depend
on season, may improve disease surveillance and the prospects of
interventions. In addition, new testable hypotheses on PD dynamics
and spread in salmon farming have been generated.
We show here how the model can be used to investigate effects
of control interventions aimed at reducing farm infectiousness
and further spread of PD. Speciﬁcally, we show that a strategy
with mandatory culling of infected cohorts reduces the number
of detected PD outbreaks by approximately 60%, compared to the
practice followed up until 2012. Models for scenario simulations
have previously been used to investigate effects of various mea-
sures to control foot-and-mouth disease (Tildesley et al., 2009,
2012) or bovine tuberculosis (Brooks-Pollock et al., 2014) in cattle.
We do not, however, know of similar applications in the aqua-
culture industry. The preventive effects of the culling strategy in
the present simulations, which would come at a cost of reduced
production and yield for those affected, represents information of
central importance to cost-beneﬁt evaluation of disease manage-
ment strategies on an industry level. Furthermore, we believe that
the high detail and coverage of the data on salmonid production and
disease occurrence should encourage the use of simulation mod-
elling as a means of testing effects of extensive control measures
before they are implemented.
However, the beneﬁt of using a mechanistic model like the
present for scenario modelling depends on (i) that the model is
reasonably capable of reproducing important aspects of the true
infection process and (ii) that the production system that the model
is ﬁtted to does not change to the degree that the model has lit-
tle future relevance. The primary transmission component in the
present model is “infection from infected neighbourhood farms”,
a pathway which we interpret as a distance related probability of
contagious contacts between farms. Hence, the model is suitable
for scenario modelling in endemic situations where this compo-
nent dominates, as in the present study. On the other hand, results
for geographical areas that are free from disease should be inter-
preted with care. Infection from other, non-speciﬁed sources will
then be the dominating transmission component, and represent
the probability of introduction of the disease into a disease-free


<!-- page 10 -->
M. Aldrin et al. / Preventive Veterinary Medicine 121 (2015) 132–141
141
area. However, this component is estimated from endemic data in
the present model and the estimated value may therefore not be
relevant for the probability of introduction. With regard to future
relevance, there were changes implemented in the salmon farm-
ing production system during the study. The use of PD vaccination
increased (Bang Jensen et al., 2012). This may have reduced the
baseline hazard over time which is reﬂected in the negative param-
eter 1 in our model. This could have been addressed explicitly
in the model, but we did not have detailed information on which
cohorts that were vaccinated. Also, there was an increasing trend in
cohort numbers of ﬁsh (Fig. 2, panel d). This increasing trend may
explain the increases in both observed and simulated detected out-
breaks (Fig. 5, panel a). Such changes must be taken into account
when using scenario modelling as a basis for deciding disease con-
trol strategies.
We selected our ﬁnal model among a set of alternative mod-
els by cross validation and demonstrated that the ﬁnal model, as
well as the alternatives, had clear predictive capacity. However, we
also demonstrated that the model was unable to fully reproduce
the spatio-temporal pattern of detected disease outbreaks, quanti-
ﬁed by Ripley’s K-function. Apparently, there are some other, still
unknown, factors that contribute to clustering beyond the present
model estimations. In discussions with professional ﬁsh health staff
with experience with PD we have been led to one possible expla-
nation, i.e. following a PD diagnosis on a given farm, the probability
of PD diagnoses in proximate farms may increase simply because
of increased awareness of the disease. In future work, we wish to
introduce a random spatio-temporal term in the outbreak model or
in the susceptibility factor in the infection model and investigate if
that improves the reproducibility of the observed spatio-temporal
pattern of detected disease outbreaks.
Some of the seasonal aspects of introducing the SIR sub-model
for within cohort infection are worth a ﬁnal comment. For exam-
ple, it is obvious that the rate of transition from the susceptible to
infected compartment depends on the seasonal timing of infection
in a cohort, i.e. the force of infection is higher for cohorts infected
in April than in January (Fig. 7, panels c and d; Anderson and May,
1991). Furthermore, the transmission rate showed a pronounced
reduction in the period August–September, for reasons that we
cannot explain. Such dynamic patterns may, however, derive from
host–pathogen interactions that depend non-trivially on season
or temperature. For example, it is well established that immune
competence in ﬁsh may vary according to seasons, a phenomenon
that possibly is linked to the physiological cost of maintaining
such a system in periods of low pathogen loads in the environ-
ment (Morgan et al., 2008). Seasonality in within-farm infection
processes could, however, also be linked to the seasonal biology
and characteristics of the salmonid production (e.g. Fig. 2, panel a).
Nevertheless, the governing factors for the seasonal dynamics in
the present infection processes, whether they are driven by biolog-
ical interactions of the system or more trivial observational biases,
need more in depth studies to disentangle.
Acknowledgements
This work was funded by the Research Council of Norway
through the following projects: 190484/S40 “Transmission and
infection dynamics of salmonid alphavirus (SAV)”, 194067/F40
“Grunnbevilgning” and 218985/E40 “MOLTRAQ, Molecular tracing
of viral pathogens in aquaculture (EMIDA)”.
We thank professors Geir Storvik and Sylvia Richardson for very
helpful discussions about model selection and model validation and
Gianpaolo Scalia Tomba for suggesting the use of an SIR model for
within-farm transmission.
Appendix A. Supplementary data
Supplementary data associated with this article can be found, in
the online version, at http://dx.doi.org/10.1016/j.prevetmed.2015.
06.005
References
Aldrin, M., Lyngstad, T., Kristoffersen, A., Storvik, B., Borgan Ø, Jansen, P., 2011. Mod-
elling the spread of infectious salmon anaemia (ISA) among salmon farms based
on seaway distances between farms and genetic relationships between ISA virus
isolates. J. R. Soc. Interface 8, 1346–1356.
Aldrin, M., Storvik, B., Frigessi, A., Viljugrein, H., Jansen, P., 2010. A stochastic model
for the assessment of the transmission pathways of heart and skeleton mus-
cle inﬂammation, pancreas disease and infectious salmon anaemia in marine
ﬁsh farms in Norway. Prev. Vet. Med. 93, 51–61, http://dx.doi.org/10.1016/j.
prevetmed.2009.09.010
Anderson, R., May, R., 1991. Infectious Diseases of Humans: Dynamics and Control.
Oxford University Press, Oxford.
Bang Jensen, B., Kristoersen, A., Myr, C., Brun, E., 2012. Cohort study of effect of
vaccination on pancreas disease in Norwegian salmon aquaculture. Dis. Aquat.
Organ. 102, 23–31, http://dx.doi.org/10.3354/dao02529
Brooks-Pollock, E., Roberts, G., Keeling, M., 2014. A dynamic model of bovine tuber-
culosis spread and control in Great Britain. Nature, http://dx.doi.org/10.1038/
nature13529, Published online 2 July 2014.
Diggle, P., 2006. Spatio-temporal point processes, partial likelihood, foot and
mouth disease. Stat. Methods Med. Res. 15, 325–336, http://dx.doi.org/10.1191/
0962280206sm454oa
Gneiting, T., Raftery, A., 2007. Strictly proper scoring rules, prediction, and
estimation.
J.
Am.
Stat.
Assoc.
102,
359–378,
http://dx.doi.org/10.1198/
016214506000001437
Höhle, M., 2009. Additive-multiplicative regression models for spatio-temporal epi-
demics. Biometr. J. 51, 961–978, http://dx.doi.org/10.1002/bimj.200900050
Jansen, M., Bang Jensen, B., Brun, E., 2014. Clinical manifestations of pancreas disease
outbreaks in Norwegian marine salmon farming – variations due to salmonid
alphavirus subtype. J. Fish Dis., http://dx.doi.org/10.1111/jfd.12238, Article ﬁrst
published online 24 March 2014.
Keeling, M., Woolhouse, M., Shaw, D., Matthews, L., Chase-Topping, M., Haydon, D.,
Cornell, S., Kappey, J., Wilesmith, J., Grenfell, B., 2001. Dynamics of the 2001 UK
foot and mouth epidemic: stochastic dispersal in a heterogeneous landscape.
Science 294, 813–817.
Kristoffersen, A., Viljugrein, H., Kongtorp, R., Brun, E., Jansen, P., 2009. Risk factors for
pancreas disease (PD) outbreaks in farmed Atlantic salmon and rainbow trout
in Norway during 2003–2007. Prev. Vet. Med. 90, 127–136.
Morgan, A., Thompson, K., Auchinachie, N., Migaud, H., 2008. The effect of seasonal-
ity on normal haematological and innate immune parameters of rainbow trout
Oncorhynchus mykiss L. Fish Shellﬁsh Immun. 25, 791–799, http://dx.doi.org/10.
1016/j.fsi.2008.05.011
Ripley, B., 1988. Statistical Inference for Spatial Processes. Cambridge University
Press, Cambridge.
Stene, A., Viljugrein, H., Yndestad, H., Tavornpanich, S., Skjerve, E., 2014. Transmis-
sion dynamics of pancreas disease (PD) in a Norwegian fjord: aspects of water
transport, contact networks and infection pressure among salmon farms. J. Fish
Dis. 37, 123–134, http://dx.doi.org/10.1111/jfd.12090
Szmaragd, C., Wilson, A., Carpenter, S., Wood, J., Mellor, P., Gubbins, S., 2009. A mod-
eling framework to describe the transmission of bluetongue virus within and
between farms in Great Britain. PLoS ONE 4, e7741, http://dx.doi.org/10.1371/
journal.pone.0007741
Tildesley, M., P.R.B., M.J.K., M.E.W., 2009. The role of pre-emptive culling in the con-
trol of foot-and-mouth disease. Proc. R. Soc. B 276, 3239–3248, http://dx.doi.
org/10.1098/rspb.2009.0427
Tildesley, M., Smith, G., Keeling, M., 2012. Modeling the spread and control of
foot-and-mouth disease in Pennsylvania following its discovery and options for
control. Prev. Vet. Med. 104, 224–239, http://dx.doi.org/10.1016/j.prevetmed.
2011.11.007
Viljugrein, H., Staalstrøm, A., Molvær, J., Urke, H., Jansen, P., 2009. Integration of
hydrodynamics into a statistical model on the spread of pancreas disease (PD)
in salmon farming. Dis. Aquat. Organ. 88, 35–44, http://dx.doi.org/10.3354/
dao02151.
