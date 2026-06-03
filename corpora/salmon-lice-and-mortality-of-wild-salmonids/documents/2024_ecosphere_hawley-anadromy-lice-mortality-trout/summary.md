# Summary: Hawley et al. (2024)

**Full title:** Individual patterns of anadromy determine the cost of salmon lice exposure in brown trout
**Journal:** Ecosphere, 15: e70098
**DOI:** 10.1002/ecs2.70098
**Document type:** Modelling study (individual-based simulation with empirical calibration)
**Priority questions:** Q4, Q5, Q7, Q8, Q9

---

## What this paper does

This study estimates lice-induced mortality for facultatively anadromous brown trout (sea trout) in Sognefjorden, Norway, across years 2013-2015. The central methodological innovation is the use of individual-level simulated migration trajectories — not population-average models — to capture the behavioral heterogeneity that characterizes sea trout. The authors generated **N = 8,049** simulated trajectories (**4,234** smolts, **3,815** veteran migrants) from fjord-use models fitted to **N = 517** tagged fish (**175** smolts, **342** veterans) across **5** rivers (Aurland, Lærdal, Årdal, Fortun, Mørkrid), 2013–2015. These trajectories were overlaid with openly available spatial-temporal modelled salmon lice (*Lepeophtheirus salmonis*) densities for the same period.

For each simulated individual, accumulated lice exposure was converted to estimated infestation intensity using a transmission model. Infestation intensity was then translated into a probability of mortality using dose-response functions adapted from Atlantic salmon literature. This produced, for each simulated fish, an estimated probability of lice-induced death during sea-sojourn. The fraction of total mortality attributable to lice was then calculated by comparing lice-survival curves against absolute survival estimates from the simulation.

The study explicitly compares results across life-stages (first-time smolts vs. veteran migrants), populations (N=5, ranging from inner- to outer-fjord origin), and years (2013-2015). Sognefjorden was designated a National Salmon Fjord in 2007, meaning its inner reaches are protected from aquaculture development; farms are concentrated in the outer fjord and coastal zone.

---

## Main findings

- **Spatial gradient of lice:** Modelled lice densities followed a strong spatial gradient, with highest densities in the outer fjord near aquaculture facilities and very low densities in the protected inner fjord. Year-to-year variation was limited across 2013-2015.

- **Individual heterogeneity is the key driver:** Despite equal opportunity for all populations to encounter the same lice field, actual accumulated infestation depended almost entirely on how far each individual migrated. Most sea trout from all populations remained in the inner fjord and accumulated lice levels below critical mortality thresholds.

- **Lice-attributed mortality by group:**
  - Long-distance migrants (smolts): **25.3%** of total sea-sojourn mortality attributed to lice
  - Long-distance migrants (veteran migrants): **14.8%** attributed to lice
  - Inner-fjord fish (smolts): **14.7%** attributed to lice
  - Inner-fjord fish (veteran migrants): **1.7%** attributed to lice

- **Population-level range:** Across the 5 study populations, lice-attributed mortality ranged from **3.3% to 34.3%**, depending on the typical migration distance of each population.

- **Declining migration extent:** The seaward extent of migration in Sognefjorden has declined over 60 years, coinciding with aquaculture expansion in the outer fjord — consistent with lice-driven behavioral avoidance of outer-fjord areas.

- **Generic models are inadequate:** Because individual trajectory selection determines exposure so decisively, applying population-average lice exposure models to facultatively anadromous salmonids is likely to produce systematically biased estimates.

---

## Relevance to this corpus

| Question | Contribution |
|----------|----------------|
| **Q4** | Quantifies how individual migration trajectory (distance and duration in outer fjord) determines smolt and adult sea trout exposure to lice; shows most fish avoid the high-lice outer-fjord zone |
| **Q5** | Provides individual-level lice infestation estimates from a model combining simulated trajectories with modelled lice density fields |
| **Q7** | Applies dose-response functions to translate accumulated infestation levels to probability of mortality |
| **Q8** | Estimates fraction of total mortality attributable to lice: 3.3–34.3% by population; 25.3% for outer-fjord smolts |
| **Q9** | Demonstrates population-level heterogeneity: outer-fjord populations face substantially higher lice-attributed mortality than inner-fjord populations, with implications for how TLS metrics are applied to sea trout |

---

## Limitations

- Trajectories are simulated from empirical data, not direct observations during 2013-2015; model outputs depend on how well the trajectory simulation captures real behavior.
- Lice density fields are modelled (not measured in situ on wild fish) — systematic errors in the lice model propagate to mortality estimates.
- Dose-response functions (converting infestation to mortality probability) are borrowed from Atlantic salmon literature; their validity for brown trout is uncertain.
- No direct empirical mortality data are used to validate predicted mortality fractions.
- Study is restricted to a single, unusually long fjord with a formally protected inner region; results may not transfer to more exposed fjord systems with different geometries and farm distributions.

---

## Place in the literature

This paper represents a significant methodological advance over earlier population-average lice models applied to sea trout. It directly addresses the analytical gap that has historically prevented brown trout from being incorporated into Norway's Traffic Light System: the difficulty of assigning a single "typical exposure" to a species with highly variable individual migration behavior. By showing that lice-attributed mortality ranges from <2% (inner-fjord veterans) to 25% (outer-fjord smolts) within the same fjord, the paper makes a compelling case that sea trout cannot be managed under the same blanket metrics used for obligate-anadromous Atlantic salmon.

The paper builds on work on salmon lice and sea trout behavior (e.g., Thorstad et al. 2015, Bøhn et al. 2020) and uses the lice density model framework from Sandvik et al. (2020) and Stige et al. (2021) — the same modelling infrastructure underlying the TLS for Atlantic salmon. The finding of declining migration extent over 60 years echoes concerns in the broader sea trout literature that aquaculture-derived lice may be reshaping the migratory behavior of the species, with long-term fitness and demographic consequences that are not captured in current monitoring frameworks.
