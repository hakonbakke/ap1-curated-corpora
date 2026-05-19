# Summary: Modelling salmon lice-induced mortality of wild salmon post-smolts is highly sensitive to calibration data

**Citation**: Stige, L.C., Helgesen, K.O., Viljugrein, H. & Qviller, L. (2022). Modelling salmon lice-induced mortality of wild salmon post-smolts is highly sensitive to calibration data. *Aquaculture Environment Interactions*, 14, 263–277. https://doi.org/10.3354/aei00443

**AI-generated summary** — pending expert review
**Added**: 2026-03-03

---

## Background

The Norwegian Traffic Light System (TLS) for regulating salmon aquaculture production capacity uses estimated lice-induced mortality of seaward-migrating wild Atlantic salmon post-smolts as its central environmental indicator. This mortality is not directly observed but estimated using **virtual post-smolt models** — simulation models that integrate farm lice monitoring data, hydrodynamics, and fish biology to calculate how many post-smolts die from lice during their seaward migration.

Three such models are used by the Norwegian expert group: one from the Institute of Marine Research (IMR), one from the Norwegian Veterinary Institute (NVI, the authors' institution), and one from SINTEF. Despite using the same input data, the three models have systematically produced different mortality estimates. The causes of these differences were not well understood prior to this study.

---

## Methods

The authors revised the NVI virtual post-smolt model by integrating two types of calibration data previously used separately:
- **Sentinel cage data**: lice counts on cultured post-smolts placed in stationary cages at known locations and times
- **Post-smolt trawl data**: lice counts on wild post-smolts caught by trawling in coastal areas, with genetic assignment of river of origin

They then conducted a systematic **sensitivity analysis** across three key model assumptions that differ between the three official models:
- **A1**: Calibration data type (trawl vs. sentinel cage)
- **A2**: Post-smolt migration speed (7 vs. 10 km/day)
- **A3**: Density-dependence in infestation rate (estimated slope vs. fixed slope of 1)

Data covered all Norwegian salmonid farms (average 636 active farms/year), all 13 management areas, and 401 salmon-producing rivers, for the period 2012–2021.

---

## Key Findings

**Trawl vs. cage: 10× difference in infestation rate**
Post-smolts caught by trawling show approximately **10 times higher infestation rates** than post-smolts from sentinel cage experiments, even after controlling for infestation pressure. This is the study's most consequential finding: the choice of calibration data type propagates directly into large differences in estimated mortality.

**Calibration data matters more than migration speed**
Mortality estimates are **more sensitive to calibration data type** (A1) than to assumptions about post-smolt migration speed (A2). This helps explain why IMR's model (calibrated to trawl data) consistently predicts higher mortality than NVI's and SINTEF's models (calibrated to cage data).

**Density-dependence amplifies the calibration effect**
When the model is calibrated to trawl data, estimates become especially sensitive to assumptions about density-dependence in infestation rate (A3). This three-way interaction between calibration data, density-dependence, and mortality estimates is a key source of the systematic divergence among the three official models.

**Explains, but does not resolve, the model disagreement**
The paper provides a mechanistic explanation for why the three TLS models give different results. It does not conclude which model is more accurate — the "true" infestation rate of wild post-smolts remains uncertain.

---

## Uncertainty and Limitations

- The paper is written from the NVI perspective: the model being improved is NVI's own. While there is no commercial COI, NVI has an institutional position in the debate between the three models.
- Migration routes are assumed to follow the shortest sea path from river mouth to open sea; actual migration behaviour is unknown and variable.
- The trawl data used here were genetically assigned to river of origin — a methodological advance, but one that introduces its own assumptions about migration history.
- The paper covers 2012–2021; lice dynamics and farm distributions may have shifted since then.

---

## Relevance to this Corpus

This is one of the most important methodological papers for **Q10** (robustness of the TLS) in the entire corpus. It directly quantifies the sensitivity of the models that underpin Norwegian regulatory decisions to choices that remain unresolved. Key contributions:

- Explains why the three official models give different mortality estimates — a question previously without a clear answer
- Demonstrates that mortality estimates used in regulatory decisions depend critically on calibration choices, not just on biological parameters
- Makes a direct case for why the TLS expert group should communicate model uncertainty explicitly

**Priority questions addressed**: Q5, Q7, Q8, Q10

---

## Relation to Other Documents in this Corpus

| Document | Relationship |
|---|---|
| Torrissen et al. (2013) | Provides the biological baseline and widely-cited smolt survival odds ratio; Stige 2022 shows that the model basis behind such estimates is more uncertain than previously understood |
| Crawford et al. (2025) | Illustrates, from BC data, why calibration data quality matters; the trawl vs. cage issue has parallels in other monitoring systems |
