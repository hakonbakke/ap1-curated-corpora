# Summary: Kristoffersen et al. (2018)

**Full title:** Quantitative risk assessment of salmon louse-induced mortality of seaward-migrating post-smolt Atlantic salmon
**Journal:** Epidemics, 23: 19-33
**DOI:** 10.1016/j.epidem.2017.11.001
**Document type:** Risk assessment / modelling study
**Priority questions:** Q2, Q3, Q4, Q5, Q7, Q8, Q10

---

## What this paper does

Kristoffersen et al. (2018) present the Norwegian Veterinary Institute (NVI) quantitative risk assessment model for salmon louse-induced mortality of seaward-migrating post-smolt Atlantic salmon. The model was developed to provide a scientific basis for Norway's Traffic Light System (TLS), which regulates production volumes in 13 salmon farming production zones based on estimated lice effects on wild salmonids. The paper covers all 401 Norwegian salmon rivers and all 13 production zones, using data from 2014 to 2016.

The model is structured as a causal chain of four linked processes: (1) **Farm louse egg production** — estimated from mandatory weekly farm reporting of reproductive female lice per fish, multiplied by farm census and temperature-dependent egg extrusion rate. (2) **Spatial infestation pressure** — farm-specific internal infestation pressure (IIP) is computed by accounting for temperature-dependent larval development time and larval mortality, then interpolated spatially using an empirical kernel-density function calibrated against sentinel cage data from multiple fjords; this gives a continuous field of infestation pressure along each river's migration route. (3) **Post-smolt exposure and infestation** — seaward-migrating post-smolts from each of 401 rivers are assumed to follow the shortest path from river outlet to open sea at a constant progression rate, accumulating lice according to the infestation pressure field encountered during migration. (4) **Lice-induced mortality** — accumulated infestation is converted to mortality using weight-dependent thresholds from Taranger et al. (2015), with post-smolts assumed to weigh 20 g.

The model includes comprehensive sensitivity analyses covering migration speed, smolt body weight, the lice mortality threshold, and the choice of sentinel cage calibration parameters. Best-case and worst-case scenarios are presented to bracket uncertainty.

---

## Main findings

### Geographic risk pattern

West Coast Norwegian production zones (zones roughly corresponding to Hordaland, Sogn og Fjordane, and neighbouring areas) consistently showed the highest estimated lice mortality risk across 2014-2016. Northerly production zones and the southernmost production zone showed lower risk. This geographic pattern was robust across the three years studied.

### Density-dependent effect

After adjusting louse-egg output for standing stock biomass, estimates varied by up to a factor of 8 between production zones. The correlation between biomass-adjusted louse-egg output and density of farmed salmon within production zones was identified as strong evidence for a **large-scale density-dependent host-parasite effect**: zones with higher farmed salmon density produce disproportionately more lice per wild fish, making biomass density a key driver of wild salmon mortality risk — not just total production volume.

### Uncertainty and sensitivity

The authors report large uncertainties throughout the causal chain. Key sensitivity findings include that mortality estimates are substantially influenced by: (a) the choice of lice tolerance threshold, (b) assumed post-smolt body weight, and (c) the calibration of the sentinel cage infestation model. Despite these uncertainties, the model structure and outputs are described as transparent and reproducible, suited for assessing **relative** spatial and temporal risks rather than absolute mortality.

---

## Relevance to this corpus

| Question | Contribution |
|----------|----------------|
| **Q2** | Explicitly models farm louse egg production from reported adult female lice counts, temperature, and standing stock biomass — directly addresses how aquaculture density drives lice production |
| **Q3** | Uses an empirical kernel-density function to model spatial spread of lice from farms; calibrated against sentinel cages rather than hydrodynamic modelling |
| **Q4** | Models post-smolt exposure along shortest-path migration routes; cumulative infestation calculated for full migration from each of 401 rivers |
| **Q5** | Provides modelled infestation estimates (and resulting mortality) for all 401 rivers across 2014-2016 under best-case, expected, and worst-case scenarios |
| **Q7** | Applies Taranger et al. (2015) weight-dependent mortality thresholds to translate infestation to mortality; same step that is central to the Jansen and Gjerde (2021) critique |
| **Q8** | Estimates fraction of smolts dying from lice at the river and production zone level; identifies West Coast zones as highest risk |
| **Q10** | One of the core models underlying the Norwegian TLS; the density-dependence finding has direct relevance to TLS zone design and threshold calibration |

---

## Limitations

- **Shortest-path routing**: The model assumes post-smolts take the shortest path from river to open sea at a constant speed. This ignores how actual ocean currents, fjord topography, and post-smolt behaviour may affect migration trajectories and lice exposure — a key methodological difference from the Johnsen et al. (2021) hydrodynamic VPS approach.
- **Constant progression rate**: A uniform migration speed is assumed regardless of current direction, water temperature, or individual variation. The sensitivity of results to this assumption is partially examined but not resolved.
- **Sentinel cage calibration basis**: The spatial infestation model is calibrated against sentinel cage data from a limited number of fjords. Sentinel cages are stationary and may not represent the exposure of freely moving post-smolts in different habitats or fjord types.
- **Lice tolerance thresholds**: As in all TLS models, the mortality conversion step depends on Taranger et al. (2015) thresholds derived from limited experimental challenge trials. The authors acknowledge this as a major uncertainty.
- **Error propagation**: The model chains at least four uncertain steps; cumulative uncertainty is acknowledged to be large but not formally propagated through the full chain.
- **Correlational density-dependence**: The density-dependent host-parasite finding is based on correlation between zone-level variables; mechanistic drivers are not explicitly modelled.

---

## Place in the literature

Kristoffersen et al. (2018) predates the Johnsen et al. (2021) IMR VPS paper and was one of the first comprehensive national-scale models for the Norwegian TLS. At the time of publication, it represented a substantial advance: it covered all 401 rivers and all 13 production zones, incorporated farm-level reporting data, and was calibrated against empirical infestation data from sentinel cages. The density-dependence finding — that zones with more farmed salmon per unit area show disproportionately higher infestation rates on wild fish — is an important scientific contribution that has implications beyond Norway.

Within this corpus, the paper occupies an interesting position because Peder Andreas Jansen (corresponding author here) is also the author of the 2021 critique of the IMR VPS model (`2021_icesjms_jansen-comment-vps-mortality`). The NVI model and the IMR VPS model were developed by different institutions for the same regulatory purpose and differ in several key assumptions. The NVI model uses simpler migration routing (shortest path vs. hydrodynamic) but in some respects a more detailed farm-origin infestation model (explicit egg production vs. archived larval concentrations). Neither model has been fully validated against direct observations of wild smolt survival, because no dataset for that exists at national scale.

When read alongside Johnsen et al. (2021) and Jansen and Gjerde (2021), this paper is essential for understanding what the Norwegian TLS is based on, where the two institutional models agree and diverge, and where the key scientific uncertainties lie in the chain from farm lice counts to estimated wild salmon mortality.
