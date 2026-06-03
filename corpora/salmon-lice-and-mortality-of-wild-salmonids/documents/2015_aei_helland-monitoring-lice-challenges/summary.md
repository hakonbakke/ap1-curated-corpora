# Summary: Helland et al. (2015)

**Full title:** Statistical and ecological challenges of monitoring parasitic salmon lice infestations in wild salmonid fish stocks  
**Journal:** Aquaculture Environment Interactions, 7: 267–280  
**DOI:** 10.3354/aei00155 (Open Access, CC BY)  
**Document type:** Feature article / methods  
**Priority questions:** Q5, Q10  
**Funding:** Norwegian Environment Agency, Food Safety Authority, Research Council, NINA, IMR

---

## What this paper does

Models **2004–2010** Norwegian national gill-net monitoring (4890 fish, 244 occasions, 41 sites, 15 fjords; 95% sea trout) and critiques statistical design for management use.

## Dataset composition

- **4610** trout + **280** char; **99%** *L. salmonis*; stage mix ~66% chalimus, 17% pre-adults, 16% adults.
- **39%** zero lice; **9%** one louse; maximum **586** lice on one fish.
- Farm IP: mature female lice × farm fish count, kernel-smoothed (Jansen et al. 2012); temperature = prior-month county means; salinity = river-discharge proxy.

## Main statistical results

**Binary GLMM (lice present/absent):**

| Predictor | Estimate | p |
|-----------|----------|---|
| Intercept | −3.445 | <0.001 |
| Fish length | +0.003 mm⁻¹ | <0.001 |
| Farm IP (standardized) | +1.245 | <0.001 |
| Temperature | +0.314 | <0.001 |
| Freshwater influence | −134.1 | <0.001 |
| Temperature × farm IP | −0.075 | <0.001 |

Farm pressure remains significant **after** temperature adjustment—first Norwegian analysis with T×farm interaction (temperature matters most when farm pressure is low).

**Proportional thresholds** (trout <200 g, N=2250): farm IP significant only at **>0.025 lice g⁻¹**, not at 0.05 or 0.1 (47% zero samples at 0.1 threshold).

**Count models:** ZIP/ZINB on per-fish counts **failed to converge**.

## Management implications

- Recommend fewer fjords, more fish per site; biologically meaningful thresholds.
- Programme adapted **from 2013**: fyke nets, four model fjords (Taranger et al. 2015).

## Relevance

| Q | Role |
|---|------|
| **Q5** | Coast-wide drivers of wild infestation |
| **Q10** | Documents monitoring limits underpinning TLS evidence |

*ODL refresh 2026-06-03 from extracted.md*
