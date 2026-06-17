# Summary: Gjerde & Aslam 2025 Prediction of the salmon lice density on wild sea trout from the mean predicted lice density in the sea: A cross-validation of the data in Myksvoll et al. (2018)

**Full title:** Prediction of the salmon lice density on wild sea trout from the mean predicted lice density in the sea: A cross-validation of the data in Myksvoll et al. (2018)  
**Journal:** Aquaculture, 599: 742149  
**DOI / URL:** 10.1016/j.aquaculture.2025.742149  
**Document type:** Methods paper (statistical reanalysis)  
**Priority questions:** Q5, Q7, Q10  
**Funding / COI:** The first author presented findings as a witness for Norwegian salmon farmers in court cases against the Norwegian state; the farmers lost both cases. No funding was received for this work.

---

## What this paper does

Gjerde and Aslam (2025) critically evaluate a key component of the Norwegian Traffic Light System (TLS) for managing salmon lice infestations, specifically the hydrodynamic salmon lice particle model developed by Myksvoll et al. (2018). This model predicts the mean predicted lice density (PMLD) in the sea based on farm reports and ocean circulation data. The authors investigate whether PMLD can reliably predict the observed mean lice burden (OMLB) on wild sea trout, which is crucial for regulatory classifications that impact aquaculture practices.

The study is geographically focused on the Norwegian coast, utilizing data collected over three years (2015-2017) from 102 coastal locations. The dataset includes 5,211 wild sea trout, making it a substantial sample for assessing the model's predictive capabilities. The findings are significant for the TLS framework, as they challenge the reliability of a model that underpins regulatory decisions affecting both wild fish populations and aquaculture operations.

## Methods and data

The authors reanalyze the dataset from Myksvoll et al. (2018), which includes:
- 5,211 wild sea trout and some Arctic char caught at 102 locations along the Norwegian coast.
- Data spans three years: 2015 (21 locations), 2016 (44 locations), and 2017 (37 locations).
- Each location's OMLB is paired with PMLD from the same 15×15 km grid area.

The analysis employs four linear regression models, a non-linear logistic regression model, and a threshold model to classify TLS colors (Green, Yellow, Red). Leave-one-out cross-validation is utilized to assess the predictive power of these models.

## Key findings

**Predictive Power:**
- The Pearson correlation between OMLB and PMLD is low (r = 0.52–0.55), indicating that PMLD explains only ~30% of the variation in OMLB (R² ≈ 0.28–0.30).
- Relative Predictive Deviation (RPD) values range from 1.18 to 1.19, classified as "very poor" predictive power (RPD < 2.0).

**Confidence Intervals:**
- The 95% confidence interval for predicted lice burden spans nearly one full lice/g unit, approximately three times the range of the mortality risk thresholds used in TLS classification (0 to 0.3 lice/g).

**TLS Classification Accuracy:**
- Green classification: True Positive Rate (TPR) = 0.67, False Positive Rate (FPR) = 0.10.
- Yellow classification: TPR = 0.43, FPR = 0.16.
- Red classification: TPR = 0.57, FPR = 0.23.
- Overall accuracy of classification is 0.63.

**Sample Size Requirements:**
- To reliably distinguish between Green and Yellow classifications (0.1 lice/g difference), PMLD data from at least 200 grid cells (28,800 km²) are needed, exceeding the area of most production zones.
- For distinguishing Green from Red (0.2 lice/g), at least 50 grid cells (7,200 km²) are required.

## Limitations and caveats

The authors highlight several limitations in the original Myksvoll et al. (2018) study:
1. The Spearman correlation was inflated due to tied zero-values; the Kendall correlation is lower (0.52).
2. No cross-validation was performed in the original study, which assessed the model on training data rather than held-out data.
3. The correlation metric used does not adequately assess the accuracy of zone-level classification, which is critical for regulatory applications.

## What this paper does not claim

Gjerde and Aslam do not claim that the PMLD model is entirely without merit; rather, they assert that its predictive power is insufficient for regulatory classification at the required spatial scale. They do not provide alternative models or solutions to improve PMLD predictions but emphasize the need for more extensive data collection and analysis.

## Relevance to this corpus

This paper directly addresses key questions in the corpus:
- **Q5 (model predictions of infestation):** It demonstrates that the PMLD model has very poor predictive power for regulatory classification.
- **Q7 (translating infestation to mortality):** The unreliability of the infestation prediction tool implies that downstream mortality estimates are similarly uncertain.
- **Q10 (TLS robustness):** This study presents a significant statistical challenge to the validity of the TLS model, suggesting that regulatory decisions may be based on poorly validated tools.

## Related evidence in corpus

The findings of Gjerde and Aslam (2025) are relevant to ongoing debates regarding the efficacy of the TLS and the management of salmon lice in aquaculture. Their critique aligns with previous studies that have questioned the reliability of models used to predict lice-induced mortality in wild salmonids, including those by Myksvoll et al. (2018) and subsequent analyses of the VPS model.

*Expanded from extracted.md 2023-10-01 for synthesis context.*
