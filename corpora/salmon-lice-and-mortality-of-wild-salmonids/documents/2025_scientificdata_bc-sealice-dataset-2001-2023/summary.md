# Summary: Crawford et al. (2025)

**Full title:** Sea lice infestation dataset for wild and farmed salmon populations on the Pacific coast of Canada (2001–2023)
**Journal:** Scientific Data (Nature Portfolio)
**DOI:** 10.1038/s41597-025-05653-x
**Document type:** Dataset description (Data Descriptor)
**Priority questions:** Q1, Q5

---

## What this paper does

Harmonises two decades of British Columbia sea lice monitoring into five linked CSV files on figshare, integrating government, industry, First Nations, NGO and research programmes that previously used incompatible formats. Goal: enable coast-wide spatial and temporal analysis and reduce reliance on small or anecdotal datasets in BC aquaculture policy debates.

---

## The dataset (key numbers)

| Component | Scale |
|-----------|-------|
| **Wild events** | 16,920 sampling events (`all_wild_sample_events`) |
| **Wild fish assessed** | 376,764 individual records (`all_wild_fish_lice`) — ~1M fish caught, ~25% assessed due to protocol caps |
| **Farms** | 96 facilities (`industry_farm_details`) |
| **Farm monthly records** | 10,159 abundance rows (`industry_farm_abundance`) |
| **Zone load medians** | 1,527 rows (`industry_zone_loads_median`) |
| **Geography** | Seven active DFO fish health sub-zones (2.3, 2.4, 3.1–3.5) |

**Wild hosts:** Chum and pink salmon ≈93% of fish; stickleback ~3%; sampling mainly April–June (>90% of events). **28%** of assessed wild fish had any sea louse; **~1%** had >10 lice.

**Farm data:** Weekly pen sampling (40–60 fish) aggregated to monthly mean abundances by species/stage; weighted zonal means for March–June (DFO sensitive period for out-migrating juveniles).

---

## Monitoring programmes and protocols

Ten wild sampling sources (SCS, MK, Hak, Kit, DFO, BAMP, MERP, MBC, Pacif, etc.) with **lethal** (lab species/stage ID), **non-lethal** (field, limited chalimus ID), or **mixed** protocols. Longest runs: Salmon Coastal Station (3.3 Broughton) and Krkošek programme (2003–2009, also 3.3). Spatial coverage uneven — e.g. Cedar Coast (2.3) only 2018–2021.

---

## Notable patterns documented

- **2015:** Coast-wide elevated farm *L. salmonis* motile abundances in most zones (warm blob), except southern zones 2.3 and 3.1.
- **2021/2022 onward:** Fewer farm sampling events in **Discovery Islands (3.2)** and **Broughton (3.3)** after government farm reductions.
- **Data quality:** Early years weak species resolution for early stages; DFO reporting shifted from monthly to weekly (2013) and farm-level to pen-level over time.

---

## Relevance to this corpus

Foundational **Q1** (farm–wild lice linkage) and **Q5** (characterising infestation pressure / validating models) resource for Pacific Canada. Complements Jones et al. (2025 JFD/DAO) natural-experiment papers and provides the empirical base those short communications draw on. Methodological reference for harmonising multi-source lice monitoring — analogous challenges to Norwegian TLS multi-index assessments.

---

## Limitations

- No mortality or population outcomes; no causal transmission modelling in this paper.
- Wild sampling not standardised across zones/years.
- Farm inventories not disclosed at site level (zone load medians only).
- BC species and regulatory context differ from Norwegian TLS.

**Repository:** https://doi.org/10.6084/m9.figshare.28078100 — code: https://github.com/modailmara/BCSalmonData
