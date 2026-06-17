# Summary: Stige et al. 2022 Modelling salmon lice-induced mortality of wild salmon post-smolts is highly sensitive to calibration data

**Full title:** Modelling salmon lice-induced mortality of wild salmon post-smolts is highly sensitive to calibration data  
**Journal:** Aquaculture Environment Interactions, 14: 263–277  
**DOI / URL:** https://doi.org/10.3354/aei00443  
**Document type:** Modelling / sensitivity study (Norwegian Veterinary Institute)  
**Priority questions:** Q5, Q7, Q8, Q10  
**Funding / COI:** All authors are affiliated with the Norwegian Veterinary Institute (NVI), which operates one of the three TLS expert-group models.

---

## What this paper does

Stige et al. (2022) revise the Norwegian Veterinary Institute's (NVI) virtual post-smolt model to assess the impact of calibration data on the predicted mortality of wild *Salmo salar* post-smolts due to salmon lice (*Lepeophtheirus salmonis*). The study integrates data from both sentinel cage experiments and genetically assigned trawl surveys conducted between 2012 and 2021 across all 13 management areas (MAs) in Norway. The primary motivation for this research stems from discrepancies observed in mortality estimates produced by different models (IMR, NVI, and SINTEF), which utilize the same farm lice inputs but yield systematically different results. This study addresses a call for sensitivity analysis made by Eliasen et al. (2021) to clarify these discrepancies.

The research is significant for understanding the ecological and economic implications of salmon lice on wild salmon populations, particularly as Norway is a leading producer of Atlantic salmon. Accurate mortality estimates are essential for sustainable aquaculture management, especially given the regulatory framework that categorizes management areas based on the estimated impact of salmon lice on wild salmonids.

---

## Methods and data

The study employs a mixed negative-binomial model to analyze data from various sources, including:

- **Salmonid farms:** Monitoring data from an average of 636 active sites per year, reporting weekly lice counts and monthly biomass from 2012 to 2021.
- **Sentinel cages:** Data from 26,697 fish across 1,048 cage deployments, with exposure periods averaging 16 days during May to August.
- **Post-smolt trawls:** Data from 3,502 fish collected through 555 hauls across 49 rivers, with genetic assignment probabilities exceeding 0.80, conducted in weeks 18 to 23.

The model tests three key assumptions that vary among existing models:

1. **Calibration data type (A1):** Comparison between sentinel cage and trawl data.
2. **Migration speed (A2):** Assumed speeds of 7 km/d (NVI) versus 10 km/d (alternative).
3. **Density dependence (A3):** Estimated slope from data versus a fixed slope of 1.

The model evaluates how these assumptions affect predicted lice infestation rates and subsequent mortality estimates for wild salmon post-smolts migrating from 401 rivers.

---

## Key findings

1. **Infestation Rates:** Trawl-caught post-smolts exhibited an infestation rate approximately 10 times higher than that of sentinel cage post-smolts under equivalent infestation pressure, indicating a significant biological signal.
   
2. **Sensitivity to Calibration Type:** Mortality estimates were found to be more sensitive to the choice of calibration data (A1) than to migration speed (A2). Specifically, calibration to trawl data resulted in higher mortality estimates.

3. **Density Dependence Impact:** When calibrated to trawl data, mortality estimates were particularly sensitive to assumptions regarding density dependence (A3), with a decreasing infestation rate observed at higher lice densities.

4. **Model Discrepancies Explained:** The paper elucidates the reasons behind the differing mortality estimates among models:
   - IMR uses trawl calibration with a higher migration speed (~12 km/d) and constant infestation efficiency.
   - NVI historically relied on cage calibration with a lower speed (7 km/d) and density-dependent infestation.
   - SINTEF employs cage-like assumptions.

5. **No Definitive Calibration Claim:** The authors clarify that while they provide insights into the discrepancies, they do not assert which calibration method is definitively “true.”

---

## Limitations and caveats

- The study assumes a shortest-path migration model to the trawl mid-point, which may not accurately reflect actual migration routes.
- As an NVI-led study, it may carry inherent biases favoring the NVI model.
- The model did not test the sensitivity of the 60% mobile-lice survival factor.
- The analysis is limited to data from 2012 to 2021, which may not capture longer-term trends.

---

## What this paper does not claim

The authors do not claim to have established a definitive calibration method for estimating salmon lice-induced mortality. They acknowledge the complexity and uncertainty surrounding the biological processes linking lice infestations to mortality, and they do not assert that their findings resolve all discrepancies among existing models.

---

## Relevance to this corpus

This study contributes to understanding how different calibration methods impact mortality estimates of wild salmon due to salmon lice, addressing key questions in the corpus, particularly Q5 (infestation differences by sampling method), Q7 and Q8 (mortality translation and calibration choices), and Q10 (stability of TLS outputs across models).

---

## Related evidence in corpus

The findings of Stige et al. (2022) should be read in conjunction with related studies such as Johnsen et al. (2021) on IMR trawl VPS, Jansen & Gjerde (2021) comparing trawl versus VPS mortality, and Eliasen et al. (2021) regarding threshold and sensitivity governance.

*Expanded from extracted.md 2023-10-01 for synthesis context.*
