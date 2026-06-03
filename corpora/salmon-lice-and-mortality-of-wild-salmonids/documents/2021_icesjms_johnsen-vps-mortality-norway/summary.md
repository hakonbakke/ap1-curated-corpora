# Summary: Johnsen et al. (2021)

**Full title:** Salmon lice-induced mortality of Atlantic salmon during post-smolt migration in Norway
**Journal:** ICES Journal of Marine Science, 78(1): 142-154
**DOI:** 10.1093/icesjms/fsaa202
**Document type:** Modelling study
**Priority questions:** Q3, Q4, Q5, Q7, Q8, Q10

---

## What this paper does

Johnsen et al. (2021) present the Virtual Post-Smolt (VPS) model developed by the Institute of Marine Research (IMR) in Norway. The model was designed to estimate salmon lice-induced mortality of wild Atlantic salmon post-smolts as they migrate from their natal rivers to oceanic feeding grounds — for all 401 Norwegian salmon rivers simultaneously. This is the primary model used by Norway's Traffic Light System (TLS) for aquaculture regulation: TLS classification determines whether production in each of 13 management areas may expand (green, <10% estimated mortality), stay constant (yellow, 10-30%), or must be reduced (red, >30%).

The VPS model works by combining two main components. First, a spatiotemporal archive of salmon lice larval concentrations in Norwegian coastal waters, built using state-of-the-art hydrodynamic ocean models and lice biology models (Sandvik et al. 2020), captures how farm-produced lice larvae disperse through fjords and coastal waters — potentially >100 km from source farms. Second, virtual post-smolts are released from each river according to empirically derived migration timing and speed parameters (based on smolt trapping data from 25 rivers, extrapolated to all 401), and their accumulated lice infestation is tracked as they travel through the larval concentration field toward open ocean.

Critically, the model was calibrated and validated against observed lice loads on wild post-smolts captured during the national NALO trawl surveys in 2015-2019. These trawled fish were genetically assigned to their rivers of origin using baseline genetic profiles from Norwegian salmon populations (Harvey et al. 2019). This genetic assignment step enabled river-specific calibration — a major methodological advance over earlier approaches that treated all post-smolts within a management area as equivalent. Mortality was then estimated by applying the lice tolerance thresholds from Taranger et al. (2015): post-smolts acquiring more than a threshold number of lice (weight-dependent) are assumed to die.

---

## Main findings

### River-level mortality estimates for 2019

The model estimated salmon lice-induced mortality for 401 Norwegian rivers in 2019:
- **<10% mortality**: 179 rivers (green TLS category)
- **10-30% mortality**: 140 rivers (yellow TLS category)
- **>30% mortality**: 82 rivers (red TLS category)

### Geographic pattern

Rivers located deep within fjord systems, particularly in western Norway, faced the highest estimated lice exposure and mortality. Post-smolts from inner fjord rivers must transit through aquaculture-dense zones for longer periods, accumulating more lice. Outer-coast rivers had lower estimated mortality.

### Migration timing and lice exposure window

Post-smolt migration typically commences from late April in southern Norway and late June in northern Norway, lasting 3-7 weeks per river, with most fish migrating within a 1-2 week window. The model used a 40-day migration window for all rivers. The timing of migration relative to peak lice larval concentrations is a key determinant of infestation.

### Sensitivity analyses

Sensitivity tests showed that mortality estimates are meaningfully sensitive to the lice tolerance thresholds applied. Using stricter or more lenient thresholds can shift the classification of individual rivers between TLS categories, illustrating that the mortality conversion step — not the dispersal or infestation modelling — is a key source of uncertainty.

---

## Relevance to this corpus

| Question | Contribution |
|----------|----------------|
| **Q3** | Model describes how farm-produced lice larvae disperse via hydrodynamic transport and quantifies larval concentration fields throughout Norwegian coastal waters |
| **Q4** | Quantifies smolt exposure to lice as virtual post-smolts transit through the larval concentration field from each of 401 rivers |
| **Q5** | Provides model-predicted infestation levels on virtual post-smolts from all Norwegian rivers, calibrated against genetically assigned trawl data |
| **Q7** | Applies Taranger et al. (2015) weight-dependent thresholds to convert infestation to mortality; directly addresses the infestation-to-mortality translation step |
| **Q8** | The primary paper estimating the fraction of post-smolts dying from lice: <10% for 179, 10-30% for 140, >30% for 82 rivers in 2019 |
| **Q10** | Foundational model for the Norwegian TLS; all discussions of TLS robustness refer to this model and its assumptions |

---

## Limitations

- **Lice tolerance thresholds**: Mortality conversion depends entirely on thresholds from Taranger et al. (2015), which are based on limited experimental challenge data from hatchery fish; this is the most contested parameter in the model.
- **Migration timing extrapolation**: Empirical migration timing data exist for only 25 rivers; parameters for the remaining 376 rivers are estimated by analogy, introducing uncertainty that is difficult to quantify.
- **Passive migration assumption**: Virtual post-smolts follow hydrodynamically modelled currents; the model does not incorporate active directional migration, avoidance of high-lice areas, or surface-layer behaviour.
- **Genetic resolution**: Not all trawled post-smolts can be assigned to a specific river of origin; calibration coverage varies by region.
- **Single focal year for detailed results**: The 2019 results are presented as the primary output; inter-annual variability across 2015-2019 is used for calibration but not fully reported for all rivers.
- **One-way coupling**: The model estimates lice effects on wild fish but does not feed back into farm management dynamics.

---

## Place in the literature

Johnsen et al. (2021) is the definitive publication of the IMR VPS model, which represents one of the most sophisticated national-scale attempts to quantify lice-induced mortality of wild salmon post-smolts. It builds on a lineage of IMR hydrodynamic and lice dispersal modelling (Johnsen et al. 2014, 2016; Sandvik et al. 2016, 2020) and incorporates the genetic assignment methodology of Harvey et al. (2019) as a novel calibration tool. In the context of this corpus, it is the paper that most directly answers Q8 (fraction of smolts dying) and Q10 (TLS robustness) at the national scale.

Jansen and Gjerde (2021) published a formal comment on this paper in the same issue of ICES Journal of Marine Science (`2021_icesjms_jansen-comment-vps-mortality`), arguing that the VPS model's use of Taranger et al. (2015) thresholds overestimates lice-induced mortality and questioning whether the model's output reliably supports the binary TLS classification system. This critique goes to the core of Q10. The Johnsen et al. paper and the Jansen and Gjerde comment must be read as a pair.

The Kristoffersen et al. (2018) NVI model (`2018_epidemics_kristoffersen-risk-assessment`) was developed in parallel for the same regulatory purpose. Its key differences are: it uses a shortest-path routing assumption for migration (rather than hydrodynamic routing), it calibrates against sentinel cage data (rather than genetically assigned trawl fish), and it uses a kernel-density empirical infestation model (rather than a mechanistic dispersal model). The two models can yield different river-level classifications, which has been a source of scientific and policy debate within the Norwegian TLS process. Notably, Peder Andreas Jansen — who later critiqued the IMR model — is a co-author of the NVI model, a context relevant to interpreting the critique.
