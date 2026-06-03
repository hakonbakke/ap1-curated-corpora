# Summary: Jansen et al. (2025/2026)

**Full title:** Effects of salmon lice on numbers and size distributions of Atlantic salmon returning to spawn in Norwegian rivers
**Journal:** Journal of Applied Ecology, 63, e70212 (2026 online; DOI 2025)
**DOI:** 10.1111/1365-2664.70212
**Document type:** Research article (open access)
**Priority questions:** Q4, Q6, Q9, Q10

---

## What this paper does

This study tests whether salmon-lice parasite-induced mortality (PIM) estimated by the Norwegian Traffic Light System (TLS) is reflected in real-world numbers of mature Atlantic salmon returning to spawn. It links two public data streams — national river counting (NINA/bestand.nina.no) and mandatory recreational catch statistics — with yearly NVI PIM values per river (Stige et al. 2023b, "Doede" column). Returns are analysed by size class proxy for sea-age: small <3 kg (1 sea winter, 1SW), medium 3–7 kg (2SW), large >7 kg (3SW), for 2019–2024.

---

## Methods

- **Raw data:** 143 rivers, 560 river-years; after five exclusion filters (Gyrodactylus salaris rivers, video counts, <70% anadromous stretch surveyed, poor count conditions, missing PIM) → **104 rivers, 396 river-years** (1,188 model observations).
- **Return estimate:** R = (count / survey proportion) + rod catch (June–August, caught not released).
- **Model:** Log-normal regression with mgcv smooth spatial term s(geo) on coastal river index; covariates: theoretical smolt production (TS), weighted prior-generation catch (CGW), year factors, separate (1−PIM) effects per size class. Adjusted R² = 0.70.
- **Data:** Dryad 10.5061/dryad.m0cfxpphh.

---

## Main findings

| Finding | Detail |
|---------|--------|
| **1SW (grilse) most affected** | β for (1−PIM) on 1SW = 2.883 (p<0.0005) — expected return loss exceeds PIM estimate |
| **2SW** | Positive but non-significant (p=0.10) |
| **3SW** | Significantly negative coefficient but small absolute numbers; net effect on total returns still negative |
| **Size structure** | Share of 1SW falls from ~60% (low PIM) to <20% (high PIM) |
| **Population thresholds** | ~10% fewer total returns at PIM ~5.5%; ~10% lower spawning weight at PIM ~10% |
| **Policy gap** | >70% of river-years exceed PIM where 10% return reduction is predicted — conflicts with government goal of <10% additional wild mortality from lice (Meld.St. 24, 2024–2025) |
| **2024 collapse** | Returns in 2024 ~36% below 2019 — attributed to marine conditions, not PIM in the model |
| **TLS debate** | Authors state results are "more in support of" TLS model outcomes than Van Nes et al. (2024) and Jansen & Gjerde (2021) |

---

## Uncertainty and limitations

- Correlational — cannot prove causation or rule out confounders.
- PIM is not the dominant predictor; TS and CGW explain more variance between rivers.
- Sea-age inferred from weight will misclassify some fish (especially large/multi-sea-winter fish).
- PIM in year t affects 1SW, 2SW and 3SW in overlapping years — partial violation of independence (addressed in supplements).

---

## Relevance to this corpus

Provides the population-level evidence the Eliasen et al. (2021) Evaluation Committee requested: observed adult returns vs modelled post-smolt PIM. Central to Q4 (population impacts), Q6 (life-history/size effects), Q9 (returns/abundance), and Q10 (TLS regulatory logic). Complements VPS modelling papers and contrasts with Van Nes TLS critique chain.

---

## Relation to other documents

- Uses PIM from Stige et al. (2022, 2023) / Johnsen et al. (2021a) TLS framework.
- Same first author as Jansen & Gjerde (2021) VPS critique — here finds population-level support for TLS mortality estimates.
- Contextualises debate with Van Nes et al. (2024), Larsen et al. (2024), Vollset et al. (2023).
