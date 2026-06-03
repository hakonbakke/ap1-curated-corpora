# Summary: Stige et al. (2022)

**Full title:** Modelling salmon lice-induced mortality of wild salmon post-smolts is highly sensitive to calibration data
**Journal:** Aquaculture Environment Interactions, 14: 263–277
**DOI:** 10.3354/aei00443
**Document type:** Modelling / sensitivity study (Norwegian Veterinary Institute)
**Priority questions:** Q5, Q7, Q8, Q10

---

## What this paper does

Revises the **NVI virtual post-smolt model** to use **both** calibration streams used separately by other TLS models, then tests how three assumptions change predicted **lice infestation** and **mortality** for wild Atlantic salmon leaving **401** rivers (**2012–2021**, all **13** management areas).

**Motivation:** IMR, NVI, and SINTEF models share farm lice inputs but produce **systematically different** TLS mortality — causes previously unclear. Study responds to **Eliasen et al. (2021)** EvalComm call for sensitivity analysis.

---

## Data scale

| Source | Scale |
|--------|-------|
| **Salmonid farms** | Mean **636** active sites/year; weekly lice + temperature; monthly biomass |
| **Sentinel cages** | **26,697** fish, **1,048** cage deployments (49–206 cages/year), May–Aug, **~16 d** exposure |
| **Post-smolt trawls** | **3,502** fish, **555** hauls, **49** rivers (genetic assignment **P > 0.80**), weeks 18–23, MAs 2–5 |
| **Overlap** | **14** MA×year combinations have **both** cage and trawl data |

Farmed salmon estimated **~98%** of ovigerous female lice in Norwegian coastal waters (Dempster et al. 2021).

---

## Sensitivity design (Table 1)

| Assumption | NVI default | Alternative |
|------------|-------------|-------------|
| **A1 Calibration** | Sentinel **cage** | **Trawl** data |
| **A2 Speed** | **7 km d⁻¹** | **10 km d⁻¹** |
| **A3 Density slope β₁** | Estimated from data | Fixed **β₁ = 1** (IMR/SINTEF style) |

Mixed negative-binomial model includes **Cagedata** indicator: exponent of **β₂** = proportional trawl vs cage infestation rate at equal pressure.

---

## Key findings

1. **~10× higher infestation rate** on **trawl-caught** vs **cage** post-smolts at the same modelled infestation pressure — largest biological signal in the paper.

2. **Mortality estimates more sensitive to A1 (calibration type) than A2 (migration speed).**

3. When calibrated to **trawl**, results especially sensitive to **A3 (density dependence)**.

4. **Mechanistic explanation for official model split:**
   - **IMR** — trawl calibration, ~**12 km d⁻¹**, constant infestation efficiency
   - **NVI** — historically cage calibration, **7 km d⁻¹**, density-dependent infestation
   - **SINTEF** — cage-like assumptions (per expert-group practice)

5. Paper **explains** disagreement; does **not** declare which calibration is “true.”

---

## Conflict of interest (from paper / context)

All authors at **Norwegian Veterinary Institute (NVI)** — operates one of three **TLS expert-group models** (typically **lower** mortality than IMR). **No formal COI statement** in extract; **institutional stake** in NVI methodology vs IMR is relevant when interpreting conclusions. Open access CC BY.

---

## Relevance to this corpus

| Question | Contribution |
|----------|----------------|
| **Q5** | Shows observed infestation differs 10× by sampling method at equal pressure |
| **Q7–Q8** | Mortality translation inherits calibration choice |
| **Q10** | Core evidence that TLS outputs are not stable across official models |

**Read with:** Johnsen et al. 2021 (IMR trawl VPS), Jansen & Gjerde 2021 (trawl vs VPS mortality), Eliasen 2021 (threshold/sensitivity governance).

---

## Limitations

- Shortest-path migration to trawl mid-point
- NVI-led study of NVI model
- 60% mobile-lice survival factor not sensitivity-tested
- 2012–2021 period only
