# Summary: Gjerde & Aslam (2025)

**Full title:** Prediction of the salmon lice density on wild sea trout from the mean predicted lice density in the sea: A cross-validation of the data in Myksvoll et al. (2018)
**Journal:** Aquaculture, 599: 742149
**DOI:** 10.1016/j.aquaculture.2025.742149
**Document type:** Methods paper (statistical reanalysis)
**Priority questions:** Q5, Q7, Q10

---

## What this paper does

This paper performs a rigorous cross-validation of a core component of the Norwegian Traffic Light System (TLS): the hydrodynamic salmon lice particle model developed by Myksvoll et al. (2018). That model estimates *Predicted Mean Lice Density in the sea* (PMLD) from farm reports, using an ocean circulation model and particle tracking. The question here is: does PMLD actually predict *observed* lice burden on wild fish (OMLB) well enough to use as a regulatory classification tool?

## The dataset re-analysed

The analysis uses data from Myksvoll et al. (2018):
- 5,211 mainly wild sea trout (plus some Arctic char) caught at 102 locations along the Norwegian coast
- Three years of data: 2015, 2016, 2017
- Each location: OMLB (observed mean lice burden per gram body weight on fish) paired with PMLD (model output from same 15×15 km grid, same period)

## Statistical methods

Four linear regression models, a non-linear logistic regression model, and a threshold model classifying TLS colours (Green/Yellow/Red) were fitted. Leave-one-out cross-validation was applied to assess predictive power.

## Key results

**Very poor predictive power across all models:**
- Pearson correlation between observed and predicted values: r = 0.52–0.55 (r² ≈ 0.28–0.30)
- Relative Predictive Deviation (RPD): 1.18–1.19 — classified as "very poor" by standard criteria (RPD <2.0)
- 95% confidence interval of predicted lice burden spans ~1 full lice/g unit over the entire PMLD range — approximately 3× the full span of the Green/Yellow/Red mortality risk thresholds (0 to 0.3 lice/g)

**TLS colour classification fails:**
- Green: TPR = 0.67, FPR = 0.10 (modest)
- Yellow: TPR = 0.43, FPR = 0.16 (poor)
- Red: TPR = 0.57, FPR = 0.23 (poor)
- Overall accuracy: 0.63

**Sample size requirements:**
- To reliably distinguish Green vs. Yellow (0.1 lice/g difference), PMLD data from **≥200 grid cells** (28,800 km²) are needed
- This exceeds the sea area of *most* of the 13 production zones (largest = 15,784 km²)
- For Green vs. Red (0.2 lice/g), ≥50 grid cells (7,200 km²) are needed — still exceeding several zones

## What went wrong in Myksvoll et al. (2018)?

The original paper concluded PMLD was reliable based on a Spearman rank correlation of 0.72. Gjerde & Aslam show that:
1. The Spearman correlation was artificially inflated by tied zero-values; the Kendall correlation is only 0.52
2. No cross-validation was performed — the model was assessed on training data, not held-out data
3. The correlation metric does not assess the accuracy of zone-level classification, which is the actual regulatory use case

## Relevance to this corpus

**Q5 (model predictions of infestation):** Shows directly that the key lice particle model used in TLS has very poor predictive power at the spatial scale required for regulatory classification.

**Q7 (translating infestation to mortality):** If the infestation prediction tool is unreliable, the downstream mortality estimates based on it inherit this uncertainty and then amplify it.

**Q10 (TLS robustness):** This is the most statistically explicit challenge to TLS model validity in this corpus. If PMLD cannot reliably classify zones, the TLS framework is using a poorly validated tool for significant regulatory decisions.

## Context and conflict of interest

The first author (Bjarne Gjerde, retired Nofima genetics researcher) presented these findings as a witness for Norwegian salmon farmers in two court cases against the Norwegian state (2020, 2021). The farmers lost both cases. The declared conflict of interest is notable but does not affect the statistical validity of the cross-validation analysis, which uses publicly available data and standard methods.
