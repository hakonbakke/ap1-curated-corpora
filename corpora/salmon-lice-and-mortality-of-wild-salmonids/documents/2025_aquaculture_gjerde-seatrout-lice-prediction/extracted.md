Aquaculture 599 (2025) 742149

![image 1](<Gjerde and Aslam_2025_Prediction of the salmon lice density on wild sea trout from the mean predicted lice density in the sea - A cross-validation of the data in Myksvoll et al_images/imageFile1.png>)

Contents lists available at ScienceDirect

![image 2](<Gjerde and Aslam_2025_Prediction of the salmon lice density on wild sea trout from the mean predicted lice density in the sea - A cross-validation of the data in Myksvoll et al_images/imageFile2.png>)

# Aquaculture

journal homepage: www.elsevier.com/locate/aquaculture

Prediction of the salmon lice density on wild sea trout from the mean predicted lice density in the sea: A cross-validation of the data in Myksvoll et al. (2018)

Bjarne Gjerde a,b,*, Muhammad Luqman Aslamb

- a BGJERDE, Ekornveien 12, 1430 Ås, Norway
- b Department of Breeding and Genetics, Nofima AS, P.O. Box 210, N-1431 Ås, Norway


![image 3](<Gjerde and Aslam_2025_Prediction of the salmon lice density on wild sea trout from the mean predicted lice density in the sea - A cross-validation of the data in Myksvoll et al_images/imageFile3.png>)

##### A R T I C L E I N F O

A B S T R A C T

Keywords: Salmon lice Atlantic salmon Cross-validation Prediction model Traffic light system

The coast of Norway is divided into 13 production zones (PZ 1–13) for farmed Atlantic salmon and rainbow trout. In the “Traffic Light System” (TLS) the increased mortality risk due to lice infestation on wild migrating smolt determines whether the production at the grow-out farms in a PZ must be reduced (Red light), can remain at the current level (Yellow), or can be increased (Green). Myksvoll et al. (2018) analysed observed mean lice burden per gram body weight (OMLB) of wild sea trout caught using traps and nets at 102 locations each of grid size 15 × 15 grid; i.e., 12 km × 12 km =144 km2) along the coast and the predicted mean lice particle density in the sea (PMLD) at these locations.. They concluded, based on a Spearman rank correlation of 0.72 between log of the PMLD and OMLB values, that PMLD provide reliable information about the spatial distribution of salmon lice infestation pressure all along the coast and therefore of importance for the knowledge base of TLS. Crossvalidation of their data with linear regression models, bivariate logistic regression models, and a threshold model with three assumed mortality classes (Green, Yellow and Red), do not confirm their conclusions. Rather, the very low predictive power of all models shows that PMLD is such a poor predictor of OMLB that assigning a Green, Yellow or Red colour to a PZ with a sufficiently high statistical power is only possible with PMLD values from many sea areas in sum larger than the area of the majority of the 13 PZs.

## 1. Introduction

The coast of Norway is divided into 13 production areas (PZ 1–13) for farmed Atlantic salmon and rainbow trout (Norsk Lovtidende, 2017). The salmon lice infestation level on wild Atlantic salmon, and the increased mortality risk due to this, determines whether the production at the grow-out farms in a zone must be reduced, can remain at the current level, or can be increased (Norsk Lovtidende, 2017). The increased mortality risk is based on the assumption that small salmonid post-smolts (<150 g) with an observed relative lice intensity (sum number of copepodites and chalimus 1 and 2) of <0.1, 0.1–0.2, 0.2–0.3 and > 0.3 g per fish have an expected increase in mortality of 0, 20, 50 and 100 %, respectively (Taranger et al., 2015).

These lice intensity and mortality risk criteria are further used to classify the mortality risk into three classes according to the “Traffic Light System” (TLS) (Ministry of Trade, Industry and Fisheries, 2017; Vollset et al., 2017): low risk with <10 % estimated increase in mortality

(Green colour) and with an offer to each farm in the actual PZ to increase the production capacity by 6 %; moderate risk with between 10 and 30 % increase in mortality (Yellow colour) with a maintenance of the production capacity at each farm at its current level; and high risk if the increase in mortality is >30 % (Red colour) with a decrease in the production capacity at each farm by a given percentage decided by the Ministry of Trade Industry and Fisheries in each round of evaluation of TLS. Farms who can document that the effect on the surrounding wild migrating salmon is substantially less than indicated by the Yellow or the Red colour classification given to the PZ in which they are located, may be offered to increase their production.

Each year a risk assessment is performed by an expert group of scientists (Vollset et al., 2017) and a steering group (Næsje et al., 2019) based on the results from a similar salmon lice infestation pressure model (Sandvik et al., 2020) and two other models (Kristoffersen et al., 2018; Ellingsen and Knutsen, 2020), as well as data from the national surveillance program for salmon lice on wild salmonids (NALO) which

* Corresponding author. E-mail address: bjarne.gjerde@nofima.no (B. Gjerde).

https://doi.org/10.1016/j.aquaculture.2025.742149 Received 24 July 2023; Received in revised form 6 November 2024; Accepted 10 January 2025

Available online 13 January 2025 0044-8486/© 2025 The Authors. Published by Elsevier B.V. This is an open access article under the CC BY license (http://creativecommons.org/licenses/by/4.0/).

are used to verify the models (Vollset et al., 2021).

An accurate and reliable classification of each of the 13 PZ into one of the three TLS classes is of great importance for farmers to gain confidence in the system and for a proper management of the wild salmonid populations. E.g., an erroneously classification of a zone into Green (rather than Yellow or Red) may have a negative effect on the wild salmon, while an erroneously classification of a zone into Yellow and particularly Red (rather than Green) may have substantial negative effect for the farmers but without a negative effect on the wild salmon.

Monitoring of the salmon lice infestation pressure on wild salmon has mainly been performed through sampling using nets or traps or by trawling after post-smolts at some selected locations (Serra-Llinares et al., 2014). However, because the Norwegian mainland coastline is 29,750 km including the fjords, and 103,600 km including also islands and bays (www.kartverket.no), complementary methods to give a more complete overview of the infestation pressure are needed (Myksvoll et al., 2018). Myksvoll et al. (2018) describes the use of an operational salmon lice model that calculates the horizontal concentration and distribution of infectious salmon lice from aquaculture grow-out farms all along the coast in near real-time. The dispersal of lice in this model is driven by a hydrodynamic ocean model and a salmon lice particle tracking model that uses the reproductive output of adult female lice reported weekly from the aquaculture grow-out farms as one of the input variables.

In Myksvoll et al. (2018) the predict lice density in the sea from the operational salmon lice model on a total of 102 locations (each of 144 km2) along the coast of Norway were compared with the observed lice count data (copepodite and chalimus 1 and 2 stages) obtained from a total of 5211 mainly wild sea trout, including an unknown number of Arctic char, caught at the same locations.

Based on the magnitude of a Spearman rank correlation of 0.72 between the observed mean lice burden on the fish (OMLB) caught at the 102 locations, and the corresponding predicted mean lice density in the sea (PMLB) from a operational salmon lice model (including both a hydrodynamic ocean model and a salmon lice particle tracking model) the authors concluded that PMLD have proven to be reliable in providing salmon lice infestation pressures in near real-time all along the entire Norwegian coast and represent invaluable information for evaluating the carrying capacity of wild fish with respect to salmon lice, and hence an important measure in combination with other model systems (Kristoffersen et al., 2018) and field observations for the implementation of TLS (Vollset et al., 2017).

However, as the predictive power of PMLD for OMLB has not been assessed, the utility of this approach remains untested. In this paper we used the data in Myksvoll et al. (2018) to explore through a crossvalidation of their data whether the predicted mean lice burden (PMLB) on the fish is both precise (low variance) and accurate (unbiased) when compared to the observed mean lice burden (OMLB) on the fish, and thus useful as a supplementary tool for assigning a Green, Yellow or Red colour to each of the 13 PZ.

## 2. Material and methods

The analysed OMLB and PMLD data are available from a Correction of Myksvoll et al., 2018). See Appendix 1 for more details about the data. The descriptive statistics of the data from each of the three years and for all three years combined are shown in Table 1 while the distribution of the data is shown in Appendix 2 with both variables skewed to their low values. For OMLB, 4.9 % of the 102 records has a value of zero, 54.9 % a value ≤0.1 and 73.5 % a value ≤0.3. For PMLD 14.7 % of the 102 records has a value of zero, 56.9 % a value ≤0.1 and 79.6 % a value ≤0.3. The scatter plot of the data in Fig. 1 shows a weak relationship between OMLB on the wild caught fish and and the corresponding PMLD in the sea.

The available OMLB and PMLD data were analysed with four linear regression models, a non-linear logistic regression model, and a

Table 1

Descriptive statistics of the observed mean lice burden per fish (OMLB) and predicted mean lice density per m2 sea area (PMLD) for each and all three years of data.

Year/Trait N Mean SD Min Max

- 2015 OMLB 21 0.221 0.342 0 1.146 PMLD 21 0.491 0.683 0 2.337
- 2016 OMLB 44 0.256 0.350 0 1.509 PMLD 44 0.243 0.406 0 1.995
- 2017 OMLB 37 0.291 0.641 0 3.545 PMLD 37 0.203 0.271 0 0.943


All three

OMLB 102 0.261 0.471 0 3.545 PMLD 102 0.279 0.448 0 2.337 ln(OMLB+1) 102 0.190 0.265 0 1.514 ln(PMLD+1) 102 0.202 0.279 0 1.205

threshold regression model.

2.1. The four linear models

The following four linear 2nd degree polynomial regression models were used:

- OMLB = Intercept1 +b1PMLD+b2PMLD2 +e1 (1)
- OMLB = Intercept2 +b3ln(PMLD+1)+b4(ln(PMLD + 1))2 +e2


(2)

- ln(OMLB+1) = Intercept3 +b5PMLD+b6PMLD2 +e3 (3)
- ln(OMLB+1) = Intercept4 +b7ln(PMLD +1)+b8(ln(PMLD + 1))2


+e4

(4)

where the b’s are the regression coefficients and the e’s are the random residual errors. In Model 2 the natural logarithm (ln) of the independent variables were used, in Model 3 ln of the dependent variable, and in Model 4 ln of both the dependent and the independent variables, thus allowing for a semi-log (Model 2 and Model 3) and a log-log (Model 4) linear relationship between the dependent (response) and the independent (predictor) variables within the ordinary linear regression framework.

The 2nd degree polynomial was used to allow for a curvilinear relationship between PMLD and OMLB. The purpose of the log transformation of OMLB and PMLD was to obtain normally distributed error variance and homoscedasticity of the error variance (constant variance at each level of the independent variables). The significance of the 2nd degree polynomial was tested with a maximum likelihood ratio test in Proc Mixed in (SAS/STAT Software, 2002-2012).

To avoid computing errors for observations with zero value for which logarithm is not defined, a positive constant value (Δ) was added to all the PMLD (Model 2 and 4) and OMLB (Model 3 and 4) observations, as often recommended (e.g. Bell´ego and Pape, 2019). Adding a smaller value than Δ = 1.0 to the observations (e.g. 0.001, 0.005, 0.01 or 0.1) did not improve the predictive power of the models. Rather a reduced relative predicted deviation (RPD, see below chapter 2.4.1) was observed. E.g., when adding Δ = 0.1 to all the PMLD and OMLB observations, the following evaluation parameters (see below) were obtained from Model 4: rp = 0.49, Bias = 0.04, |Bias | = 0.243, and RPD = 1.027 as compared to RPD = 1.192 when adding Δ = 1.0 as shown in Table 2. When adding a smaller value than Δ = 0.1, lower RPD were obtained; i.e. RPD = 1.003 when adding Δ = 0.001, RPD = 0.946 when adding Δ = 0.005, and RPD = 0.917 when adding Δ = 0.01. There may

![image 4](<Gjerde and Aslam_2025_Prediction of the salmon lice density on wild sea trout from the mean predicted lice density in the sea - A cross-validation of the data in Myksvoll et al_images/imageFile4.png>)

- Fig. 1. Plots of the observed mean lice burden (OMLB) of the fish on the predicted mean lice density (PMLD) in the sea, and the regression line (Model 1) through these plots with its parameters in the upper right corner where RMSEC = the Root Mean Squared Error of Calibration. The two dotted lines represent the 95 % confidence interval of the predicted mean lice burden (PMLB) values of the fish on the predicted PMLD values in the sea from Model 1.


- Table 2 Estimated cross validation parameters of the four liner models.


Model rp Bias |Bias| RMSECV RPD RMSECV-b RPD-b

- 1 0.55 0.035 0.205 0.396 1.189 0.394 1.195
- 2 0.54 0.027 0.208 0.396 1.189 0.395 1.192
- 3 0.52 0.071 0.212 0.400 1.178 0.393 1.198
- 4 0.55 0.066 0.201 0.400 1.178 0.395 1.192


rP = the Pearson correlation coefficient. Bias and |Bias| is the mean bias and the mean absolute bias, respectively. RMSECV = the Root Mean Squared Error of Cross Validation. RMSECV-b = the Root Mean Squared Error of Cross Validation accounted for the mean bias. RPD = SD/RMSECV, the Relative Predicted Deviation. RPD-b = SD/RMSECV-b, the Relative Predicted Deviation accounted for the mean bias.

exist an optimal Δ but that is not necessarily the smallest possible value for Δ, contrary to common believe (Croux and Behon, 2010). Therefore, a constant of Δ = 1.0 was added to all the PMLD (Model 2 and 4) and OMLB (Model 3 and 4) observations thus obtaining a ln-value of zero for those observations with a zero value.

The models were run by using both centred (zero mean) and scaled (unit variance) OMLB and PMLD, as well as non-centred and non-scaled OMLB and PMLD values, by using the Scale and Center, or NoScale and NoCenter, options in Proc PLS in SAS/STAT Software, 2002-2012). As the two options produced very similar results, only the results from the NoScale and NoCenter options are shown. With the NoCenter option, an estimate of the bias of the predicted OMLB are obtained.

2.2. The logistic model

A non-linear logistic regression model (Proc Logistic in SAS/STAT Software, 2002-2012) was used to test to what degree the predicted mean lice densities in the sea (PMLD) was able to correctly classify the observed mean lice burden on the fish (OMLB) into binary classes with different OMLB thresholds. Due to the close to unity Pearson correlations coefficient between the predicted lice burden (PMLB) of the four regression models, the logistic regression model was only applied for the same two independent variables as for the linear regression Model 1.

For this purpose, the following three binary trait hypotheses were defined with different OMLB thresholds and assumed increased mortality risk in TLS (Taranger et al., 2015):

- • H0: OMLB ≤0.1, BIN = 0; H1: OMLB>0.1, BIN = 1, 45.1 % of the 102 observations; or
- • H0: OMLB ≤0.2, BIN = 0; H1: OMLB>0.2, BIN = 1, 31.4 % of the 102 observations; or
- • H0: OMLB ≤0.3, BIN = 0; H1: OMLB>0.3, BIN = 1, 25.5 % of the 102 observations.


The non-linear relationship between PMLD and the probability of BIN = 1 (pi) for a given observation (location in the present study) can be written as:

eλ 1 + eλ

1 1 + e λ

pi =

= Seλ,

=

where Se is the sigmoid function with base e, and λ = b0 + b1PMLDi + b2PMLD2i .

This non-linear S-shape relationship can be transformed to a linear relationship through the logistic function (often referred to as taking the logit, and linear in the logit), and can be written as:

)

(

pi 1 pi

= bo +b1PMLDi +b2PMLD2i

logit(pi) = ln

The new set of values of the dependent variable is the logit of the probability of the outcome of interest (BIN = 1), and thus the linear relationship between the independent variable PMLD and logit of pi on the log scale.

- 2.3. The threshold-model

The observed mean lice burden on the fish (OMLB) was classified into the following three classes separated by the two OMLB thresholds 0.1 and 0.3 and thus approximately in line with the assumed increased mortality risk in TLS (Taranger et al., 2015):

- • For OMLB ≤0.1 light class Green = 1 (54.9 % of the 102 observations);
- • For 0.1 < OMLB ≤0.3 light class Yellow = 2 (19.6 % of the 102 observations);
- • For OMLB >0.3 light class Red = 3 (25.5 % of the 102 observations).


The following threshold model in the ASReml software (Gilmore et al., 2021) was used to test to what degree the predicted mean lice density in the sea (PMLD) was able to simultaneously classify correctly the 102 OMLB observations into the three above defined classes:

Pr(y = 1,2 or 3) = ∅ bo +b1PMLDi +b2PMLD2i

)

where y is an assumed underlying non-observable liability of the dependent variable and ∅( • ) is the cumulative standard normal distribution, and the other parameters are as described in chapter 2.1.

- 2.4. Evaluation parameters


2.4.1. Linear models

The predictive power of each of the four linear models was investigated using the leave-one-out cross validation procedure in Proc PLS in (SAS/STAT Software, 2002-2012This implies that each model was trained on all observations except one (N = 102–1) after which a predicted OMLB value (PMLB) for Model 1 and 2, and the predicted ln (OMLB+1) values for Model 3 and 4, was obtained for that observation; a procedure that was repeated for each of the 102 observations. In Model 3 and Model 4 the predicted values were transformed back to their values on the observed scale (PMLB) by the inverse transformation epred. ln(OMLB+1) -1.

The following evaluation parameters were used, and in the following exemplified using the variables in Model 1: (a) the Pearson correlation coefficient between the predicted (PMLB) and the observed (OMLB) values; (b) the Root Means Squared Error of Cross Validation,

̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅

√

∑N i=1 (OMLBi PMLBi)2

1 N

RMSECV =

; (c) RMSECV b = ̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅

√

∑N i=1 (Biasi Bias)2

1 N 1

and thus the RMSECV accounted for the bias (Davies and Fearn, 2006) where N is the number of locations, Biasi = OMLBi PMLBi and Bias = N1

∑N

i=1 (OMLBi PMLBi) is the mean bias; (d) the mean absolute bias |Bias |= N1

∑N

i=1 ∣(OMLBi PMLBi)|, (e) the relative predicted deviation RPD = SD/RMSECV, where SD is the standard deviation of OMLB; and (f) RPD-b = SD/RMSECV-b and thus the RPD accounted for the bias.

According to Williams (2014) a prediction model is considered very poor, poor, fair, good, very good or excellent for RPD values varying from 0 to 2, 2–2.4, 2.4–2.9, 2.9–3.4, 3.4–4, and > 4.

2.4.2. Non-linear logistic model

The predictive power of the non-linear model for each of the three binary traits was calculated using the leave-one-out cross validation procedure in the package Caret (Kuhn et al., 2018), while the ROCcurves and their 95 % confidence intervals, one for each of the three binary traits, were obtained by the package cvAUC (LeDell et al., 2012), both in (R Core Team, 2020).

For each of the three binary trait classes, RMSECV = ̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅

√

∑N i=1 (BINi pi)2

1 N

where BINi is the observed value of the binary trait for observation i and pi the predicted probability for BINi=1

; and RPD is as for the linear regression model where SD is the standard deviation of the observed binary trait.

From the cross validation of the non-linear regression model for each of the three binary OMLB traits a 2 × 2 confusion matrix was calculated that displays the number of observations of the four combinations of the observed and the predicted binary traits OMLB ≤0.1, ≤0.2 or ≤ 0.3 (Sharma et al., 2009; Monaghan et al., 2021) where NTN = number of true negative, NFP = number of false positive, NFN = number of false negative and NTP = number of true positive:

PMLB < set threshold Accepted, BIN = 0 Rejected, BIN = 1

H0 OMLB < set threshold

True, BIN = 0 NTN NFP False, BIN = 1 NFN NTP

OMLB = observed mean lice burden; PMLB = predicted mean lice burden.

- • True negative rate TNR = NTN/(NTN + NFP) = Specificity; i.e., in this study the proportion of the locations correctly classified ac-

cording to H0. A test with a higher specificity has a lower Type-I error rate.

- • False positive rate FPR = NFP/(NFP + NTN) = 1 - Specificity; i.e., the

proportion of the locations incorrectly classified according to H0. A test with a higher FPR has a higher Type-I error rate.

- • False negative rate, FNR = NFN/(NFN + NTP); i.e., the proportion of the locations incorrectly classified (Type-II error). A test with a higher FNR has a higher Type-II error rate.
- • True positive rate TPR = NTP/(NTP + NFN) = Sensitivity or Recall rate; i.e., the proportion of the locations correctly classified ac-

cording to H1. A test with a higher sensitivity has a lower Type-II error rate and thus a higher power = 1-Type-II error.

- • Accuracy of prediction = (NTP + NTN)/(NTN + NTP + NFP + NFN); i.e., the proportion of all the locations correctly classified.


As the main goal of TLS is to classify migrating Atlantic salmon postsmolt with an above given OMLB (and thus with an expected increased mortality risk), NTP should be high and consequently FN low, resulting in a high TPR or sensitivity. This is especially important as failing to classify fish with an above given OMLB may have a negative effect on the wild salmon in the actual PZ. At the same time FPR should be low; i.e., low NFP and high NTN, as a high FPR may cause that a PZ may be wrongly classified as Yellow instead of Green, or Red instead of Yellow or Green, both with a large negative economic consequence for the grow-out farmers in the actual PZ.

The Receiver Operating Characteristic (ROC) is a plot of TPR on FPR (Figs. 3 and 4). It is a graphical representation of the trade-off between sensitivity (TPR) and specificity (1-FPR) obtained by assigning several different threshold values (depending on the number of observations in the data) from zero to one to the estimated probability of the dependent variable in the logistic regression model; and in this study for each of the three binary OMLB traits. This approach was used by Sandvik et al. (2020) for the analyses of lice data recorded on hatchery-reared Atlantic salmon reared in 18 small (diameter 0.8 m, height 0.9 m) sentinel net cages, but not through the application of a non-linear logistic model or a

threshold model as in this study.

The area under the curve is a measure of the usefulness of the test in general, where a greater area means a more useful test. A point on the curve at the top-left corner (TPR = 1, FPR = 0) represents a case where all observations (in this study locations) are correctly classified as either above (NFN = 0) or below (NFP = 0) the set binary threshold, A point at the top-right corner (TPR = FPR = 1) represents a case where all locations are correctly classified above the set binary threshold (NFN = 0), but incorrectly classify all locations below the threshold (NTN = 0). A point to the bottom-left (TPR = FPR = 0) represents a case where we correctly classify all locations below the threshold (NFP = 0), but incorrectly classify all locations above the threshold (NTP = 0). A point on the 45-degree diagonal (NTP=NFN, NFP=NTN, and thus TPR = FPR

- = 0.5) indicates an inaccurate test with no predictive power. Of two points on the curve with the same TPR, the one with the lowest FPR represent a more useful and better threshold.


The trade-off between sensitivity (TPR) and specificity (1-FPR) can be expressed in the Youden index J (Youden, 1950) with a max value of unity:

J = max (Sensitivityc+Specificityc 1) = TPR FPR.

The Youden index is a useful measure to choose the most appropriate pair of Sensitivity and pecificity values, where c ranges over all possible criteria values or points on the curve. Graphically, J is the maximum vertical distance between the ROC curve and the diagonal line. However, the point on the ROC curve corresponding with J is the optimal criterion value only at 50 % of the binary trait (equal number of locations above and below the set threshold), at which equal weight is given to sensitivity and specificity, and for which the benefit and costs of various decisions are ignored. In this study benefit and cost relates to those for the grow-out farmers in a PZ that were assigned a Green, Yellow or Red light, and those for the society if e.g. a Green or Yellow light was incorrectly assigned instead of a Red light which is assumed to be associated with a higher migratory smolt mortality than a Yellow or Green light (Taranger et al., 2015).

NTPGreen + NTNGreen=Yellow+Red NFPGreen + NTNGreen + NFPGreen + NTNGreen=Yellow+Red Similarly for the colour class Yellow and Red.

AccuracyGreen =

- 2.5. Average PMLB of several 15 × 15 grid sizes

The predictive power obtained from the cross validation of the studied models relates to PMLD from a single 15 × 15 grid size (144 km2) at each location. However, as a single grid size is much smaller than the entire area of each of the 13 PZs within the Baseline of the territorial sea of Norway (Grunnlinja, geodetic straight lines between outer points of the Norwegian coast not being flooded at low tide) (Appendix 3), the predictive power of the models may be improved by using PMLD values from several 15 × 15 grid sizes and thus the use of a more dense sampling grid. This was investigated by taking the average PMLD of different number of 15 × 15 grid sizes.

How many such grid sizes (N) are needed to detect a true difference (δ) in PMLB between two equally sized seawater areas, corresponding to a Type I error with significance level α and Type II error with significance level β, is:

δ = tα tβ

)

̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅ 2

(

RMSECV2 N

√ )

where tα and tβ are the value of the t-distribution statistic, in this case for a one-tailed t-test (>0.1, >0, or > 0.3 lice g/fish), and which for large N values can be replaced with the normal deviates Zα and Zβ, and RMSECV squared is the estimated prediction error variance of PMLB (linear regression model) and pi (non-linear logistic regression model) (see 4.13 in Snedecor and Cochran, 1967).

- 3. Results


3.1. Linear model

- 2.4.3. Threshold model The predictive power of the threshold model was also calculated


using the leave-one-out cross-validation procedure with the predicted values for each observation obtained from the ASReml software (Gilmore et al., 2021). For this model

̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅

√ √ √ √

(

∑N

1 N

BINi (1pi1 + 2pi2 + 3pi3)2

RMSECV =

i=1

where BINi is the observed class value (1, 2 or 3) for observation i, and pi1, pi2 and pi3 are the simultaneously predicted probability for each the three classes of the threshold trait. RPD is as for the linear and the nonlinear logistic model where SD is the standard deviation of the observed class values for the threshold trait.For each of the 102 observations, the most likely predicted class (Green = 1, Yellow = 2 or Red = 3) was defined based on the PMLB values on the underlying probit scale relative to the two set threshold values for OMLB, from which we obtained a 3 × 3 confusion matrix with the number of the observations in each of the nine combinations of these observed and the predicted colour classes (Table 5).

From this 3 × 3 confusion matrix (Table 5) a 2 × 2 confusion matrix for each colour class was calculated (Appendix 5) from which the TPR and FPR and Accuracy were calculated as follows (Evidently, 2024):

For colour class Green the following parameters were calculated as:

NTPGreen NTPGreen + NFNYellow+Red

TPRGreen =

NFPGreen NFPGreen + NTNGreen

FPRGreen =

The 2nd degree polynomial for each model was significant for Model 1 (P = 0.002), Model 2 (P = 0.070), Model 3 (P = 0.001) and Model 4 (P = 0.030). For each model the regression coefficient for the 2nd degree polynomial (b2, b4, b6, b8) was negative, showing that one unit increase in PMLD resulted in a larger increase in OMLB at lower than at medium and higher PMLD, as shown in Fig. 1 for Model 1.

Appendix 4 shows, for each of the four linear models, the plot of the standardized residuals on their predicted OMLB (Model 1 and 2) and predicted ln(OMLB+1) (Model 3 and 4). All OMLB except one were located within 2 and + 3 standardized residuals. For Model 1 and 2 there was a tendency for the standardized residuals to decrease with increasing predicted values, a tendency that was less pronounced for Model 3 and 4. For all models there was a tendency for variability of the standardized residuals to increase with increasing predicted values. The same pattern was seen when plotting the standardized residual on PMLD (Model 1 and 2) and ln(PMLD+1) (not shown). Therefore, some departure from the ideal situation of normality and constancy of the residual errors for the application of linear regression was seen for all models. The observed difference in the pattern of the standardized residuals between the models were small and thus with no clear indication that one model was expected to be better than the others with respect to predicting OMLB.

The estimated evaluation parameters for each of the four linear models (Table 2) show low and very similar RPD values (1.178 to 1.189) and thus very poor predictive power (Williams, 2014). The very similar RPD and the RPD-b values show that the poor predictive power of the models are not caused by the bias but by their poor predictive power per se.

The Pearson correlation coefficients between the observed and the predicted values for the four models were also very similar, and only

marginally higher for Model 1 (0.55) and Model 4 (0.55) than for Model 2 (0.54) and Model 3 (0.52). The correlation coefficients of Model 1 and Model 4 implies that the PMLB values explain only rp2=30.3 % of the variation in the OMLB values. The similarity of the models is also evident by the close to unity Pearson correlation coefficients (≥0.985) between the predicted values of the different models.

Fig. 1 shows that the 95 % confidence interval of PMLB (from Model 1) span about one PMLB unit along the entire range of PMLD, which is close to three times the entire span of the mean lice burden criteria (0 to

- 0.3 lice/g fish) used to classify the expected increased mortality risk of the wild fish and to assign a Green, Yellow or Red colour to each PZ. This poor predictive power of Model 1 (and for the other models, see Table 2) is illustrated in Fig. 2 by the wide and irregular scatter plots of OMLB vs. PMLB. One of the OMLB values (3.54) and three of the PMLD values (1.92, 1.99 and 2.34) may be considered as outliers (see Fig. 1). However, omitting these four observations from the data of Model 1 resulted


in a poorer predictive power than with all observations (rp = 0.53, RPD

- = 1.162) thus confirming that the predictive power of this and the three other models are very poor (Williams, 2014).


- 3.2. Non-linear logistic model


### Table 3

Confusion matrix from the crossvalidated non-linear logistic model showing the number of the 102 observations assigned to the four different combinations of the observed and the predicted mean lice burden per fish for each of the three investigated threshold values.

Hypothesis Threshold for OMLB

PMLB True False

- H0 ≤ 0.1 NTN = 46 NFP = 10
- H1 > 0.1 NFN = 11 NTP = 35


- H0 ≤ 0.2 56 14
- H1 > 0.2 7 25


- H0 ≤ 0.3 62 14
- H1 > 0.3 7 19


OMLB = observed mean lice burden per fish; PMLB = predicted mean lice burden per fish; NTN = no. og true negative; NTP = no. of true positive; NFN = no. of false negative; NFP = no. of false positive.

index (Table 7). This is also evident from the similar ROC curves of the binary traits and the very large confidence interval of TPR, particularly at FPR values (<0.1) considered as acceptable Type I errors (Fig. 3 A, B and C).

The confusion matrix for each of the three binary traits are given in

- Table 3 and the evaluation parameters in Table 4. The low predictive power of this model for each of the three binary


traits was evident both from their low RPD values, as well as the modest TPR (power) and high FPR (Type I error) values of the max Youden

3.3. Threshold model

The 3 × 3 confusion matrix is given in Table 5 and the overall resulting evaluation parameters in Table 6 and Table 7. Both the overall RPD (1.24) and accuracy (0.63) was low.

![image 5](<Gjerde and Aslam_2025_Prediction of the salmon lice density on wild sea trout from the mean predicted lice density in the sea - A cross-validation of the data in Myksvoll et al_images/imageFile5.png>)

- Fig. 2. Plots of the observed mean lice burden (OMLB) values of the fish on their predicted values (PMLB) from Model 1, and the regression line through these plots with its parameters in the upper right corner, where RMSECV is the Root Mean Squared Error of Cross Validation and RPD is the Relative Predicted Deviation, and r is the Pearson correlation coefficient between the OMLB and PMLB values. One observation, OMLB = 3.54 and PMLB = 0.59, not shown.


B. Gjerde and M.L. Aslam

Aquaculture 599 (2025) 742149

- Table 4 Estimated cross validation parameters for each of the three binary traits of the non-linear logistic model.

OMLB threshold Observed proportion, % SD RMSECV RPD TPR FPR Accuracy AUC

- H0 ≤ 0.1 54.9 / 45.1 0.4976 0.3913 1.27 0.76 0.18 0.79 0.80
- H0 ≤ 0.2 68.3 / 31.7 0.4640 0.3920 1.18 0.78 0.20 0.79 0.80
- H0 ≤ 0.3 74.5 / 25.5 0.3702 0.3888 0.95 0.73 0.18 0.80 0.79


SD = standard deviations of the observed binary trait values; RMSECV = Root Means Squared Error of Cross Validation; RPD = Relative predicted deviation; TPR = true positive rate; FPR = false positive rate; AUC = area under the ROC curve.

![image 6](<Gjerde and Aslam_2025_Prediction of the salmon lice density on wild sea trout from the mean predicted lice density in the sea - A cross-validation of the data in Myksvoll et al_images/imageFile6.png>)

Fig. 3. Receiver Operating Characteristic (ROC) curves with 95 % confidence interval for the three different binary traits of the non-linear logistic model (A, B and C) and for the threshold model (D).

- Table 5 Confusion matrix from the cross-validated threshold model showing the number of the 102 observations assigned to the nine different combinations of the observed and the predicted colour classes.


Table 6 shows also the evaluation parameters calculated from the 2 × 2 confusion matrix for each colour class (Appendix 5). A high proportion of the 56 locations observed as Green was predicted as Green with modest TPR = 0.67 and relatively low FPR = 0.10. Of the 20 locations observed as Yellow 12 was predicted as Yellow with modest TPR = 0.57 and relatively high FPR = 0.23. Of the 26 locations observed as Red 16 were predicted as Red with low TPR = 0.43 and relatively high FPR = 0.16. Accuracy of prediction for each colour class was similar (0.72 to 0.78), while the TPR and AUC for the Yellow class was lower than for the Green and the Red classes.

Observed light colour

Predicted light colour

Total Green = 1 Yellow = 2 Red = 3

Green = 1 54 1 1 56 Yellow = 2 12 6 2 20 Red = 3 15 7 4 26 Total 81 14 7 102

The lower predicting ability of the Yellow class as compared to the Green and the Red class is evident from the ROC curves in Fig. 3 C. At acceptable FPR values (<0.1) the predictability of the Red class is higher than for the Green class, but at low (<0.5) and thus unacceptable TPR

- Table 6 The simultaneously estimated cross validation parameters for the threshold model for the three colour classes and for each colour class.

OMLB class Obs. prop., % SD RMSECV RPD TPR FPR Accuracy AUC Green/Yellow/Red 54.9/19.6/25.5 0.8470 0.6809 1.24 – – 0.63 – Green 54.9 – – – 0.67 0.10 0.72 0.80 Yellow 19.6 – – – 0.43 0.16 0.78 0.51 Red 25.5 – – – 0.57 0.23 0.75 0.80

SD = standard deviations of the observed trait values; RMSECV = Root Means Squared Error of Cross Validation; RPD = Relative predicted deviation; TPR = true possitive rate; FPR = false positive rate; nd = not defined as both NFP = 0 and NFN = 0; ACU = area under the ROC curve.

- Table 7 The Youden index with corresponding FPR and TPR values of the three nonlinear logistic regression models and the three different colour classes of the threshold model.


- 3.4. Use of PMLD values from several grid sizes

Fig. 4 shows that for a Type I error of α = 0.05 and Type II error of β = 0.20 (power 0.80) of the linear regression Model 1, PMLD values from at least 200 different 15 × 15 grid sizes (corresponding to a sea area of 28,800 km2 = 200 × 144 km2) are required to detect a true difference of 0.1 PMLB unit between PMLB of two such equally sized sea areas (Green vs. Yellow, or Yellow vs. Red; one sided Student’s t-test). To detect a true difference equal to 0.2 PMLB unit (Green vs. Red.), PMLD from at least 50 15 × 15 grid sizes (7200 km2 = 50 × 144 km2) are required. For more stringent Type I (α = 0.01) and Type II (β = 0.10) errors the number of 15 × 15 grid sizes must be increased substantially to detect similar sized PMLB differences; i.e. in order to reduce the probability of rejecting the null hypothesis (no difference in OMLB between two zones) when it is true (Type I error), and not rejecting it when it is false (Type II error). Very similar results were obtained from the non-linear logistic model (not shown).

- 4. Discussion


Model Youden index TPR FPR Logistic regression

- H0 ≤ 0.1 0.60 0.76 0.16
- H0 ≤ 0.2 0.58 0.75 0.18
- H0 ≤ 0.3 0.60 0.88 0.29


Threshold model

Green 0.60 0.95 0.35 Yellow 0.22 0.60 0.22 Red 0.60 0.88 0.29

Youden index = TPR-FPR; TPR = true positive rate; FPR = false positive rate.

values.

When the second-degree polynomial of PMLD was excluded from the threshold model, its predictive power become slightly reduced; RPD =

- 1.22 and accuracy 0.65. These changes in the estimates were due to the following changes in the confusion matrix: cell 2,1 from 10 to 11, cell 2,3


Observed means of lice count data (OMLB) on total 5211 mainly wild sea trout caught from 102 localities along the coast of Norway and the corresponding predicted lice density data (PMLD) in the sea from the

from 10 to 9, cell 3,1 from 10 to 14 and cell 3,3 from 16 to 12.

![image 7](<Gjerde and Aslam_2025_Prediction of the salmon lice density on wild sea trout from the mean predicted lice density in the sea - A cross-validation of the data in Myksvoll et al_images/imageFile7.png>)

- Fig. 4. Number of 15 × 15 grid sizes (each of 144 km2) required to detect a given true difference in PMLB of fish from two equally sized sea areas by use of the linear regression Model 1 for combinations of two different Type I (α) and Type II (β) errors. Power of the test =1- β.


same localities in Myksvoll et al. (2018) were cross-evaluated with three different statistical models with OMLB as the dependent variable and PMLD as the explanatory variable. The results show that the predictive power of the three modelsare all very poor and that PMLD therefore is a poor predictor of OMLB (PMLB). Consequently, the low predictive power of the models is not caused by the type of statistical model used, but by the low information content of PMLD for PMLB.The low predictive power of the models are shown by the (a) very large 95 % confidence interval of about one PMLB unit from the linear model over the range of PLMD values, as compared to the much smaller lice burden threshold values (<0.1, 0.1–0.2, 0.2–0.3 and > 0.3 no. of lice/g fish) used to classify the mortality risk of the wild migrating salmon, (b) very low RPD values of all three models, and (c) very low TPR values at acceptable FPR values (<0.10) of both the logistic model and the threshold model. The benefit of the threshold model, with a simultaneous prediction of the three defined OMLB classes in line with the assumed mortality risk in TLS, can be seen of its higher predictability of the Green and the Red class as compared to the Yellow class. The similar predictability of the four linear regression models as compared to the two other models show the powerful of a simple linear regression model as compared to the more advanced non-linear logistic and threshold models.

A likely reason for the low predictability of the models is the large proportion of the locations with zero or close to zero OMLB and PMLD values, and the very large variation in the lice count among the individual fish (Vollset et al., 2017; Gjerde et al., 2011) that may require that a higher number of fish are caught and counted for lice at each location than in the present study. However, this is a challenging task as the wild sea trout at each location must be caught over a relative short period of time for OMLB to be of any relevance for the corresponding PMLD obtained from the same 15 × 15 grid size (144 km2) seawater area. This may also be the reason why the collected lice data were obtained on mainly sea trout and not wild migratory Atlantic salmon that is the target species in TLS. However, catching small migrating salmon (most <50 g) in nets is not possible, and probably also not possible to catch high numbers in trawls both within a sufficient small geographic area and period.

Another reason could be low reliability of the PMLD values for which no estimate is available, most likely because detection of particularly non-infective nauplii (0.5 to 0.6 mm in length) and infective copepodites (0.7 to 0.8 mm in length) from seawater samples is very challenging (Schram, 1993 and references therein). In future this may become possible through a recently published easy-to-use and cost-effective machine learning approach (Zhang et al., 2024).

The predictive power of the logistic model was very similar for the three defined binary traits, indicating that choice of OMLB threshold value was of little importance probably due to the low information content of the present data as mentioned above. Furthermore, the predictability of the two binary traits 0.1 ≥ OMLB>0.1 and 0.3 ≥ OMLB>0.3 of the logistic model was very similar but not identical to the predictability of the Green and Red class, respectively of the threshold model. This is as expected as the underlying non-observable normally distributed laten variable of the threshold model is very similar to the underlying latent variable of the logistic distribution. Formula for logistic regression like logit(p) can explicitly be written out (see 2.2) whereas probit(p) of the threshold model cannot and its use depending on the availability of an appropriate software.

Calculation of the optimal pair of TPR and FPR values in this study requires a reliable association between the lice burden and the mortality of the migrating post-smolts. However, a reliable estimate of this

association is not available as the present assumed estimates are based on data from laboratory experiments with Atlantic salmon (Taranger et al., 2015), while the OMLB data in this study were obtained from mainly wild sea trout. Additional requirements for such a calculation are the benefit and cost related to both the false and the true positive and negative decisions (Zweig and Campbell, 1993; Greiner et al., 2000). Those for the farmers should be relatively easy to calculate as they are related to increased (Green light), lost increased (Yellow) and reduced (Red light) production at the farms in the actual PZ. Reliable benefit and cost estimates for the society are more difficult to obtain as the association between lice burden and migratory post-smolt mortality is poorly established and still debated as increased post-smolt mortality may as well be caused by many other factors (Vollset et al., 2017; Lie and Vormedal, 2021).A well-funded decision on what is the proper Type I error and power (1-Type II error) is very important as an incorrectly classification (Type I error) means that the farmers are not allowed to increase (Yellow) or may have to reduce (Red) their production, while a failure of not rejecting the null-hypothesis (Type II error) is expected to have a negative effect through increased parasite burdens and mortality for wild migrating post-smolts and thus a cost for the society.

Myksvoll et al. (2018) stated that the PMLD in the sea should be used together with other complementary sources of information (Serra-Llinares et al., 2014; Kristoffersen et al., 2018) in the decision on whether a Green, Yellow or Red colour should be given to a PZ. However, the very low predictive power of the studied statistical models in this paper show that that a single PMLD value from a location provide very little added information about OMLB at the same location. By using the average PMLD of different number of 15 × 15 grid sizes it was found that a sea area of 28,800 km2 which is larger than the largest PZ within the Baseline of the territorial sea (PZ 9 = 15,784 km2) is required to detect a true difference in PMLB between two such equally sized sea areas of 0.1 PMLB unit (Green vs. Yellow, or Yellow vs. Red) with a reasonable high statistical power (0.80 at a Type I error of 0.05). Similarly, that a sea area of 7200 km2 is required to detect a true difference in the average PMLB of 0.2 PMLB unit (Green vs. Red). The two PZs that both in year 2022 and 2024 were assigned a Red colour have a sea area within the Baseline of 3563 km2 (PZ 3) and 5600 km2 (PZ 4).

As most of the grow-out farms are located well inside the Baseline of the territorial sea, the actual farm area of a PZ is smaller than the above given area within the Baseline. Included in the above PZ areas are also areas that have special status as protected areas, e.g. national salmon fjords. Therefore, it is not likely that PMLD can be used to detect a true PMLB difference of 0.1 lice/g fish (i.e. Yellow > Green, or Red > Yellow) between two PZs with a sufficiently high statistical power (0.80 at a Type I error of 0.05). Moreover, most of the 13 PZs are too small to detect a true PMLB difference of 0.2 lice/g fish (i.e. Red > Green) with a sufficiently high statistical power.s.

An alternative to the use of OMLB in the statistical analyses could be to model the observed lice burden of the individual fish (OLB) and assign these to their corresponding PMLD values from a smaller grid size at which each fish was caught. However, use of OLB rather than OMLB values may result in more inaccurate PMLD value as a smaller than 15 × 15 grid size will increase the probability that the sampled fish might have been infected with lice outside the sea area in which they were caught. Furthermore, a possible significant effect of different species on OLB could be tested for model inclusion as well as effect of PZ as these have quite different environmental conditions with effect on both OLB and PMLD. However, the latter would require OMLB and PMLD data from a good number of localities from each PZ and therefore demanding to obtain.

Based on the rigorous analysis of the data in Myksvoll et al. (2018) it has been demonstrated unequivocally that PMLD is a poor predictor of OMLB (PMLB) on sea trout caught in nets and that assigning a reliable Green vs. Yellow, or Yellow vs. Red, colour to a PZ is not possible without use of PMLD values from so many 15 × 15 grid sizes that it will exceed the seawater area of the actual PZ in which the farms are located. This conclusion is very different from Myksvoll et al. (2018) who concluded, based on an estimated Spearman rank correlation coefficient of 0.72 between log of the OMLB and PMLD values, that there is good comparison between PMLD and OMLB, and that PMLD is a reliable measure in providing salmon lice infestation pressure in near real-time all along the entire Norwegian coast. Particularly, given that no crossvalidation of the data was performed, and that the targeted species in TLS is Atlantic salmon of a smaller body size (about 20 g) than the sea trout (<150 g) in Myksvoll et al. (2018).

The prediction of salmon lice infestation pressure by the hydrodynamic ocean and salmon lice particle tracking models in Myksvoll et al. (2018) are described in more details in Sandvik et al., 2020) and used in the development of the virtual post-smolt (VPS) model that estimates lice infestation and lice-induced mortality of salmon post-smolts during migration from their respective rivers of origin to the ocean (Kristoffersen et al., 2018; Johnsen et al., 2021; Stige et al., 2021). In a recent comment paper by Jansen and Gjerde (2021) on Johnsen et al. (2021) it was found that the lice-induced mortality estimates from VPS were systematically overestimated compared to estimates from observed lice counts on post-smolts caught by trawls in the corresponding outer fjord areas; on average 27.1 vs. 16.0 % for the 27 pairwise comparisons (see Table 1 in Jansen and Gjerde, 2021). A further analysis of the VPS and trawl data in Table 1 in Jansen and Gjerde (2021) revealed a very low RPD=SD/RMSECV = 0.98 (where SD is the standard deviation of the calculated lice induced mortality values of the trawled post-smolt and RMSECV is that obtained from the differences between the calculated and the predicted lice induced mortality values of the trawled postsmolts and the VPS, respectively), a strong indication that the predictive

power of the VPS model is very poor.

Recently, Stige et al. (2022) revised a VPS where lice data from postsmolt trawling were integrated with lice data from sentinel cage experiments to quantify the spatiotemporal variation in infestation rate of wild Atlantic salmon post-smolts along the entire Norwegian coast. Their Pearson’s correlation coefficient between predicted and observed lice counts per fish on the log10(x + 1) scale was for the trawl data 0.41 at the sample level and 0.56 at the area-year level, and for the cage data 0.56 at the sample level and 0.58 at the area-year level. These correlations are very similar to the Pearson correlation coefficients between the PMLB and PMLD (0.52 to 0.55) of the linear regression models in this study. Stige et al. (2022) do not report any RPD values but from their Fig. 3 it is evident that the value is probably very low given the very large variation in the observed number of lice per fish for a given predicted number of lice per fish; e.g., for the trawl data from zero to about 32 observed number of lice per fish for a predicted number of about two lice per fish.

## CRediT authorship contribution statement

Bjarne Gjerde: Conceptualization, Formal analysis, Investigation, Methodology, Project administration, Validation, Visualization, Writing – original draft, Writing – review & editing. Muhammad Luqman Aslam: Formal analysis, Writing – review & editing.

## Declaration of competing interest

The first author of the paper, retired pensioner from Nofima, presented the main results of this paper when acting as a witness for some Norwegian salmon farmers in two court cases against the Norwegian state related to the TLS; in Sogn og Fjordane tingrett, Førde (the district court) in January 2020 and in Gulating lagmansrett, Bergen (the court of appeal) in February 2021. The farmers lost the case in both courts. None of the two authors has received any funding for this work.

## Appendix A. Appendix 1

The data and the main results in Myksvoll et al. (2018). The data in Myksvoll et al. (2018) were the observed lice counts (copepodites and chalimus 1 and 2) per fish (OLC) of a total of 5211 mainly wild sea trout including an unknown number of Arctic char caught at 102 locations along the coast of Norway over three years; 1088 fish at 21 locations in 2015, 1733 fish at 44 locations in 2016, and 2390 fish at 37 locations in 2017, and thus with an on average 51.8 (2015), 39.4 (2016) and 64.6 (2017) wild fish recorded per location. For each fish, the observed lice burden was calculated as OLB=OLC/body weight (g) from which the observed mean lice burden (OMLB) was calculated for all infected and non-infected fish caught at each location. In addition, the predicted mean lice (nauplius 1 and 2 stages and copepodite 1 stage) densities per m2 sea area (PMLD) was obtained from an operational salmon lice model, including both the hydrodynamic ocean model and the salmon lice particle tracking model, from a three-week observation period, including two weeks of fish sampling and one week prior to the fish sampling.

For PMLD obtained from a 15 × 15 grid size (i.e., 12 km × 12 km =144 km2) sea area, a Spearman rank correlation coefficient of 0.72 was found between the rank of the log10 of the centred (c) and standardized (s) OMLB and PMLD after adding a value of one to each of the centred and standardized values; i.e. log10(csOMLB+1) and log10(csPMLD+1). They concluded based on the magnitude of this rank correlation that PMLD is a reliable measure in providing salmon lice infestation pressure in near real-time all along the entire Norwegian coast, but without a cross- validation of the data. Moreover, (a) a rank correlation coefficient is not an appropriate measure as the decision criteria in TLS is the mortality risk of wild migrating

- A. salmon post-smolts determined from by the their predicted lice counts, and supplemented with other sources of information; (b) the reported Spearman correlation (0.72) is biased upwards due to five (OMLB) and 13 (PMLD) tied rank observations (i.e. observations with the same value, in this case zero), while the more appropriate Kendall correlation was much smaller (0.52), and also a more robust (smaller gross error sensitivity) and efficient (smaller asymptotic variance) correlation coefficient (Croux and Behon, 2010); (c) centring, standardisation and log transformation of the observations is not necessary for ranks of observations as these transformations do not change the rank.


Worth a notice is that the Person correlation coefficient between the PLMB and PMLD values was 0.48, and that between the log transformed and standardized PLMB and PMLD values 0.65.

![image 8](<Gjerde and Aslam_2025_Prediction of the salmon lice density on wild sea trout from the mean predicted lice density in the sea - A cross-validation of the data in Myksvoll et al_images/imageFile8.png>)

#### Appendix 2. Distribution of the 103 OMLB and PMLD records in Myksvoll et al. (2018).

## Appendix B. The sea area within Baseline of the territorial sea of Norway (Grunnlinja) for each of the 13 PZs (The Norwegian Directorate of Fisheries, 2017)

![image 9](<Gjerde and Aslam_2025_Prediction of the salmon lice density on wild sea trout from the mean predicted lice density in the sea - A cross-validation of the data in Myksvoll et al_images/imageFile9.png>)

- B. Gjerde and M.L. Aslam


Aquaculture 599 (2025) 742149

![image 10](<Gjerde and Aslam_2025_Prediction of the salmon lice density on wild sea trout from the mean predicted lice density in the sea - A cross-validation of the data in Myksvoll et al_images/imageFile10.png>)

Appendix 4. Plots of the standardized residuals on the predicted OMLB values (Model 1 and 2) or on the predicted ln(OMLB+1) values (Model 3 and 4).

Appendix 5 Confusion matrix from the cross validated threshold model showing the number of the 102 observations assigned to the four different combinations of the observed and the predicted mean lice burden per fish for each colour class.

Hypothesis Colour class PMLB OMLB threshold True False

- H0: OMLB ≤0.1 Green NTN = 19 NFP = 2
- H1: OMLB >0.1 Yellow or Red NFN = 27 NTP = 54


- H0: 0.1 < OMLB ≤0.3 Yellow 74 14
- H1: OMLB≤0.1 or OMLB>0.3 Green or Red 8 6


- H0: OMLB >0.3 Red 73 22
- H1: OMLB ≤0.3 Green or Yellow 3 4


## Data availability

The data are avaialble in a published Correction of Myksvoll et al

(2018)

## References

Bell´ego, C., Pape, L.-D., 2019. Dealing with logs and zeros in regression models. S´erie des documents de travail n◦ 2019-13. https://doi.org/10.2139/ssrn.3444996.

Croux, C., Behon, C., 2010. Influence functions of the spearman and Kendall correlation measures. Stat Methods Appl 19, 497–515. https://doi.org/10.1007/s10260-0100142-z.

Davies, A.M.C., Fearn, T., 2006. Back to basics: calibration statistics. Spectrosc. Eur. 18

(2), 31–32. Ellingsen, E., Knutsen, Ø., 2020. Simulert lusedødelighet på virtuell smolt i produksjonsområde 2 til 7 ved bruk av SINMOD. In: Appendix VIII, Rapport nr.

01072. https://www.regjeringen.no/contentassets/3d127a90edbc4d34a1ded5125 e41f31e/appendix-viii-sintef_sinmod_resultat_po2-7_2020.pdf.

Evidently, A.I., 2024. Accuracy, precision, and recall in multi-class classification. https ://www.evidentlyai.com/classification-metrics/multi-class-metrics.

Gilmore, A.R., Gogel, B.J., Cullis, B.R., Welham, S.J., Thompson, R., 2021. ASReml User Guide Release 4.2 Functional Specification. VSN International Ltd, Hemel Hempstead. HP2 4TP, UK. www.vsni.co.uk.

Gjerde, B., Ødegård, J., Thorland, I., 2011. Estimates of genetic variation in the susceptibility of Atlantic salmon (Salmo salar) to the salmon louse Lepeophtheirus salmonis. Aquaculture 314, 66–72.

Greiner, M., Pfeiffer, D., Smith, R.D., 2000. Principles and practical application of the receiver-operating characteristic analysis for diagnostic tests. Prev. Vet. Med. 45, 23–41.

Jansen, P.A., Gjerde, B., 2021. Comment on “Salmon lice-induced mortality of Atlantic salmon post-smolt during migration in Norway” by Johnsen et al. (2021). ICES J. Mar. Sci. 78, 3847–3851. https://doi.org/10.1093/icesjms/fsab206.

Johnsen, I.A., Harvey, A., Sævik, P.N., Sandvik, A.D., Ugedal, O., Adlandsvik, B., Wennevik, V., Glover, K.A., Karlsen, Ø., 2021. Salmon lice-induced mortality of

Atlantic salmon during post-smolt migration in Norway. ICES J. Mar. Sci. 78, 142–154. https://doi.org/10.1093/icesjms/fsaa202.

Kristoffersen, A.B., Qviller, L., Helgesen, K.O., Vollset, K.W., Viljugrein, H., Jansen, P.A.,

2018. Quantitative risk assessment of salmon louse-induced mortality of seawardmigrating post-smolt Atlantic salmon. Epidemics 23, 19–33. https://doi.org/ 10.1016/j.epidem.2017.11.001 (PMID: 29233546).

Kuhn, M., Wing, J., Weston, S., Williams, A., Keefer, C., Engelhardt, A., Cooper, T., Mayer, Z., Benesty, M., Lescarbeau, R., Ziem, A., Scrucca, L., Tang, Y., Candan, C., Hunt, T., 2018. Package “Caret” Classification and Regression Training.

LeDell, E., Petersen, M.L., van der Laan, M.J., 2012. Computationally Efficient Confidence Intervals for Cross-validated Area Under the ROC Curve Estimates. In: U. C. Berkeley Division of Biostatistics Working Paper Series. Working Paper 304. htt p://biostats.bepress.com/ucbbiostat/paper304.

Lie, M.L., Vormedal, I., 2021. The environmental effectiveness of sea lice regulation: compliance and consequences for farmed and wild salmon. Aquaculture 532 (6). https://doi.org/10.1016/j.aquaculture.2020.736000.

Ministry of Trade, Industry and Fisheries, 2017. Regjeringen skrur på trafikklyset. [The Government turns on the Traffick light]. Press release. 30.10.2017. https://www.re gjeringen.no/no/aktuelt/regjeringen-skrur-pa-trafikklyset/id2577032/.

Monaghan, T.F., Rahman, S.N., Agudelo, C.W., Wein, A.J., Lazar, J.M., Everaert, K., Dmochowski, R.R., 2021. Foundational statistical principles in medical research: sensitivity, specificity, positive predictive value, and negative predictive value. Medicina 57, 503. https://doi.org/10.3390/medicina57050503.

Myksvoll, M.S., Sandvik, A.D., Albretsen, J., Asplin, L., Johnsen, I.A., Karlsen, Ø.,

Kristensen, N.M., Melsom, A., Skardhamar, J., Ådlandsvik, B., 2018. Evaluation of a national operational salmon lice monitoring system - from physics to fish. PLoS One 13 (7), e0201338. https://doi.org/10.1371/journal.pone.0201338. Correction:13

(12): e0209949. doi: 10.1371/journal.pone.0209949.

Næsje, T.F., Boxaspen, K.K., Hjeltnes, B., 2019. Råd fra styringsgruppen for vurdering av lusepåvirkning 2018–2019 [advice from the steering group for evaluation of lice impact 2018–2019]. https://www.hi.no/resources/rad-fra-styringsgruppen-til-nf d2019.pdf.

Norsk Lovtidende, 2017. Ministry of Trade, Industry and Fisheries. Forskrift om produksjonsområder for akvakultur av matfisk i sjø av laks, ørret og regnbueørret (produksjonsområde-forskriften) [Regulation on production areas for salmon, sea trout and rainbow trout]. https://lovdata.no/dokument/LTI/forskrift/2017

-01-16-61. R Core Team, 2020. R: A Language and Environment for Statistical Computing. R Foundation for Statistical Computing, Vienna, Austria. https://www.R-project.org.

Sandvik, A.D., Johnsen, I.A., Myksvoll, M.S., Sævik, P.N., Skogen, M.D., 2020. Prediction of the salmon lice infestation pressure in a Norwegian fjord. ICES J. Mar. Sci. 77, 746–756. https://doi.org/10.1093/icesjms/fsz256.

SAS/STAT Software, 2002-2012. Version 13.2 of the SAS System for Windows. Copyright © by SAS Institute Inc., Cary, NC, USA.

Schram, T.A., 1993. Supplementary descriptions of the developmental stages of Lepeophtheirus salmonis (krøyer, 1837)(copepoda: Caligidae). Pathogens of Wild and Farmed Fish: Sea Lice 1, 30–47.

Serra-Llinares, R.M., Bjørn, P.A., Finstad, B., Nilsen, R., Harbitz, A., Berg, M., Asplin, L.,

2014. Salmon lice infection on wild salmonids in marine protected areas: an evaluation of the Norwegian “National Salmon Fjords”. Aquac. Environ. Interact. 5, 1–16. https://doi.org/10.3354/aei00090.

Sharma, D., Yadav, U.B., Sharma, P., 2009. The concept of sensitivity and specificity in relation to two types of errors and its application in medical research. J. Reliabili. Statist. Stud. 2 (2), 53–58 (ISSN: 0974-8024).

Snedecor, G.W., Cochran, W.G., 1967. Statistical Methods, 6th edition. The Iowa State University Press, Ames.

- Stige, L.C., Helgesen, K.O., Viljugrein, H., Qviller, L., 2021. A statistical mechanistic approach including temperature and salinity effects to improve salmon lice modelling of infestation pressure. Aquacult. Environ. Interact. 13, 339–361.
- Stige, L.C., Helgesen, K.O., Viljugrein, H., Qviller, L., 2022. Modelling salmon liceinduced mortality of wild salmon post-smolts is highly sensitive to calibration data. Aquacult. Environ. Interac.t 14, 263–277. https://doi.org/10.3354/aei00443.


Taranger, G.L., Karlsen, Ø., Bannister, R.J., Glover, K.A., Husa, V., Karlsbakk, E., et al.,

2015. Risk assessment of the environmental impact of Norwegian Atlantic salmon farming. CES J. Mar. Sci. 72 (997–1021), 1. https://doi.org/10.1093/icesjms/ fsu132.

The Norwegian Directorate of Fisheries, 2017. På vei inn i produksjonsområdene. https://www.fiskeridir.no/Akvakultur/Nyheter/2017/1017/Samsvar-i-ny-vurder ing.

Vollset, K.W., Dohoo, I., Karlsen, Ø., Halttunen, E., Kvamme, B.O., Finstad, B., et al.,

2017. Disentangling the role of sea lice on the marine survival of Atlantic salmon. ICES J. Mar. Sci. https://doi.org/10.1093/icesjms/fsx104.

Vollset, K.W., Nilsen, F., Ellingsen, I., Finstad, B., Karlsen, Ø., Myksvoll, M., Stige, L.C., Sægrov, H., Ugedal, O., Qviller, L., Dalvin, S., 2021. Vurdering av lakselusindusert villfiskdødelighet per produksjonsområde i 2021 (Evaluation of salmon lice induced mortality of wild fish per production area in 2021). Rapport fra ekspertgruppe for vurdering av lusepåvirkning (Expert group report on evaluation of lice induced wild fish mortality per production area in 2021). https://www.regjeringen.no/content assets/e2ce5edb567341eb8ac15fd46714417f/ekspertgrupperapport-2021.pdf. Williams, P.C., 2014. Tutorial: the RPD statistic: a tutorial note. NIR News 25, 22–26.

https://doi.org/10.1255/nirn.1419. Youden, W.J., 1950. An index for rating diagnostic tests. Cancer 3, 32–35. Zhang, C., Bracke, M., da Silva Torres, R., Gansel, L.C., 2024. Rapid Detection of Salmon

Louse Larvae in Seawater Based on Machine Learning. https://doi.org/10.1016/j. aquaculture.2024.741252.

Zweig, M.H., Campbell, G., 1993. Receiver-operating characteristic (ROC) plots: a fundamental evaluation tool in clinical medicine. Clin. Chem. 39, 561–577.

