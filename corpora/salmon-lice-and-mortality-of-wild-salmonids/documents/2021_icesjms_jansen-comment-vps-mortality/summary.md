# Summary: Jansen & Gjerde (2021)

**Full title:** Comment on "Salmon lice-induced mortality of Atlantic salmon post-smolt during migration in Norway" by Johnsen et al. (2021)
**Journal:** ICES Journal of Marine Science, 78(10): 3847–3851
**DOI:** 10.1093/icesjms/fsab206
**Document type:** Comment (peer-reviewed)
**Priority questions:** Q5, Q7, Q8, Q10

---

## What this paper does

Validates the **IMR Virtual Post-Smolt (VPS)** model (Johnsen et al. 2021) by comparing **the same mortality algorithm** applied to:
1. **Observed** lice on **NALO trawl** post-smolts (outer fjords, 2017–2020)
2. **Mean predicted VPS mortality** from rivers draining into those fjords

**Dataset:** **N = 7,929** Atlantic salmon post-smolts (5–50 g, wild); excluded **339** tagged and **326** with scale-loss comments (lower mean lice: 1.9 vs 3.05).

**Mortality steps (identical to Johnsen et al.):**
- Mean lice × **0.6** → harmful lice count
- Negative binomial, dispersion **= 0.3695**
- Assume **20 g** fish
- Thresholds: **>6** lice → 100% mortality; **4–6** → 50%; **2–3** → 20%; **0–1** → 0%

---

## Main findings

### Headline comparison

- VPS mortality **higher than trawl** in **26 of 27** area-year pairs (Figure 1)
- Gap largest when trawl mortality is **low** (low mean lice abundance)

### Mortality class distribution (Table 2)

| Class | Trawl area-years | VPS area-years |
|-------|------------------|----------------|
| **M > 30%** | 4 | **13** |
| 10% < M < 30% | 5 | 8 |
| M < 10% | 18 | 6 |

**χ²(2, N=54) = 11.46, p = 0.003**

### Example area-years (Table 1 excerpt)

| Area | Year | Trawl N | Trawl M (%) | VPS mean M (%) | VPS range |
|------|------|---------|-------------|----------------|-----------|
| MA4-1 | 2017 | 187 | 52.8 | 59.5 | 49–64 |
| MA5 | 2017 | 413 | 6.0 | 24.7 | 7–36 |
| MA6-2 | 2017 | 228 | 0.3 | 8.2 | 3–26 |
| MA4-1 | 2020 | 241 | 10.1 | 39.2 | 30–43 |

### Supplementary: remaining migration pathway

Critics argued trawled fish accumulate more lice **after** the trawl station. Authors regressed lice vs relative distance toward open ocean (**RD**): significant positive RD in **11/27** area-years. Adjusted trawl mortalities rise, but VPS still higher in **22/27** comparisons (**χ² p = 0.023**).

### Policy link

Johnsen et al. **2019** VPS results (**>30%** mortality for **82 rivers**) contributed to **mandatory production reductions** in **MAs 4 and 5**. This comment argues the model **overstates** mortality vs trawl-consistent estimates.

---

## Conflict of interest (from paper)

- **Peder A. Jansen** — **INAQ AS** (consultancy)
- **Bjarne Gjerde** — **Nofima**
- No specific grant declared
- Jansen is co-author of the **NVI** VPS framework that competes with IMR's model in TLS assessments

Open access CC BY 4.0.

---

## Relevance to this corpus

| Question | Contribution |
|----------|----------------|
| **Q5** | Tests whether modelled infestation/mortality matches observed trawl lice loads |
| **Q7–Q8** | Same Taranger thresholds — shows conversion step yields higher VPS than trawl |
| **Q10** | Direct evidence of systematic bias in TLS input model |

**Always read with** `2021_icesjms_johnsen-vps-mortality-norway` and **Stige et al. 2022** (trawl vs cage calibration).

---

## Limitations

- Mean VPS across rivers ≠ trawl catch mix
- Cannot attribute overestimation to specific sub-model
- Origin-of-trawl-fish assumption debated but defended via genetics and VPS routing rules
