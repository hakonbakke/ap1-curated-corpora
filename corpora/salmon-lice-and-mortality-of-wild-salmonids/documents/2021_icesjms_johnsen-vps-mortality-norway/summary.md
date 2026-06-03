# Summary: Johnsen et al. (2021)

**Full title:** Salmon lice-induced mortality of Atlantic salmon during post-smolt migration in Norway
**Journal:** ICES Journal of Marine Science, 78(1): 142–154
**DOI:** 10.1093/icesjms/fsaa202
**Document type:** Modelling study (IMR Virtual Post-Smolt model)
**Priority questions:** Q3, Q4, Q5, Q7, Q8, Q10

---

## What this paper does

Presents the **Virtual Post-Smolt (VPS)** model: combines **hydrodynamic salmon lice dispersion** (Sandvik et al.; upper 2 m copepodid concentrations) with simulated post-smolt migration from **401** Norwegian salmon rivers to estimate **lice-induced mortality** for the **Traffic Light System (TLS)**.

**Calibration:** Wild post-smolts caught by **NALO trawl** (weeks 18–24, 2015–2019, MAs 2–5), **genetically assigned** to rivers (Harvey et al. 2019; assignment probability >0.80). GLMM links lice counts to **infestation pressure** IP (migration time × mean lice concentration). **60%** of attached lice assumed to reach harmful mobile stages.

**Migration model:** Fjord-index grid (800 m); **5×** higher probability to move toward ocean; median **0.14 m s⁻¹**; **40 d** release window per river; **1000** VPS per river per year.

---

## Mortality conversion — Table 1 (20 g post-smolt, “normal”)

| Harmful lice per fish | Assumed mortality |
|----------------------|-------------------|
| <2 | 0% |
| 2–3 | 20% |
| 4–6 | 50% |
| >6 | 100% |

Low and high tolerance variants in Table 1 shift **4 of 13** management areas between TLS colour bands in **2019** (median river-weighted mortality).

---

## Main results (2019)

### River counts (equal weight per river)

| TLS class | Rivers (n) |
|-----------|------------|
| **Green** (<10% mortality) | **179** |
| **Yellow** (10–30%) | **140** |
| **Red** (>30%) | **82** |

### Management areas (river-weighted mean, 2019)

- **High (>30%):** MA **3** and **4**
- **Moderate (10–30%):** MA **2, 5, 6, 7, 10**
- **Low (<10%):** MA **1, 8, 9, 11, 12, 13**

**Pattern:** Inner-fjord rivers >> outer-coast rivers within the same MA (longer exposure路径).

**Example migration distances:** Etne → ocean **6.7 d**; Opo **17.6 d** (May–June 2018 lice field illustration).

### Temporal trend (2012–2019)

- Proportion of **low-mortality** rivers in MA2–6 **decreased** since 2012–13
- **MA3** alone shows fewer **>30%** rivers after 2016 peak
- Interannual swings in MA4–5 linked to coordinated farm production cycles

### Calibration notes

- **2125** genetically assigned trawl fish used in calibration pipeline; **446** discarded (no matching VPS)
- Genetic baseline: **45** populations, **31** microsatellites, MAs 2–5

---

## TLS regulatory link

- **Green / yellow / red** = <10% / 10–30% / >30% lice-induced mortality → **+6% / 0% / −6%** aquaculture volume
- Model outputs published **NMDC** (Johnsen et al. 2020) for all rivers from 2012

**Authors' conclusion:** Estimated lice on VPS **coincide** with observed levels on genetically assigned trawled post-smolts — **disputed** by Jansen & Gjerde (2021) in same journal volume.

---

## Conflict of interest (from paper)

**IMR** (primary affiliation) and **NINA** authors; funded by **Norwegian Department of Trade, Industry and Fisheries** (IMR project **14650**). IMR supplies TLS science advice. **No explicit competing-interest declaration** in extracted text. Open access **CC BY 4.0**.

---

## Limitations

- Taranger thresholds largely from lab/hatchery studies
- Migration timing extrapolated for rivers without smolt-trap series
- No active avoidance or vertical behaviour
- Calibration geography focused on highest aquaculture MAs

---

## Corpus pairing

| Document | Relationship |
|----------|--------------|
| **2021_icesjms_jansen-comment-vps-mortality** | Formal comment: 26/27 area-years VPS > trawl |
| **2022_aei_stige-model-sensitivity-calibration** | Trawl vs cage calibration drives model split |
| **2021_rcn_traffic-light-evaluation** | Independent review of threshold weakness |
