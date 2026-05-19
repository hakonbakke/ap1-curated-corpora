# Priority Questions
## Corpus: Salmon Lice and Mortality of Wild Salmonids

This corpus follows the AP1 methodology proposed by Coffay et al., where
agreement on priority questions precedes corpus construction and AI-supported
synthesis.

The purpose of these questions is not to produce single answers, but to
structure how evidence is selected, compared, and interpreted.

**Guiding principle**: We do not ask "what does the literature say in general?"
We ask "what do we need to understand in order to inform decisions in a
contested and context-dependent domain?"

---

## The causal chain

The 10 questions follow the logical sequence of the impact pathway:

```
(1) Lice production in farms
    → (2) Larval production
    → (3) Dispersal from farms
    → (4) Smolt exposure
    → (5) Infestation
    → (6) Physiological effects
    → (7) Individual mortality
    → (8) Smolt mortality estimates
    → (9) Population-level impact
    → (10) Regulatory assessment
```

Each document in this corpus must contribute evidence to at least one of
these questions. The relevant question IDs are recorded in `metadata.yaml`
under `priority_questions` and `causal_chain_stage`.

---

## Q1: Attribution of lice to aquaculture sources

**Question**
What proportion of salmon lice infecting wild salmonids originate from
aquaculture cages, and how is this attribution established?

**Why this question matters**
Determining the relative contribution of farm-origin lice vs. natural
background sources is fundamental to establishing causality between
aquaculture and wild fish infestation. Without this, any regulatory
response to lice pressure lacks causal grounding.

**Expected disagreement**
Attribution is methodologically difficult. Genetic and hydrodynamic methods
give different estimates. Background lice pressure in the absence of farms
is poorly known for most production areas.

**Evidence types needed**
`empirical_observational`, `model`, `review`

**Key metadata filters**
`causal_chain_stage: farm_lice_abundance`, `outcome_domain: infestation_on_wild_fish`

---

## Q2: Estimating lice production in farms

**Question**
How accurately can lice production in farms be estimated, and what are
the main sources of uncertainty in larval output estimates?

**Why this question matters**
Models typically derive larval output from counts of adult female lice on
farmed fish. Uncertainty in egg production rates, larval mortality, and
environmental effects on larvae propagates directly into all downstream
estimates of infestation pressure on wild fish.

**Expected disagreement**
Estimates vary depending on how egg production, temperature effects, and
larval mortality are parameterised. Industry monitoring data and research
estimates do not always align.

**Evidence types needed**
`empirical_observational`, `empirical_experimental`, `model`

**Key metadata filters**
`causal_chain_stage: farm_lice_abundance, lice_reproduction, larval_production`

---

## Q3: Larval dispersal from farms

**Question**
How far and under what conditions can salmon lice larvae disperse from
farms, and how well do hydrodynamic models capture this dispersal?

**Why this question matters**
Lice larvae are planktonic and may drift tens to more than 100 km depending
on currents and temperature. The spatial reach of farm-origin lice is a
critical parameter for assessing which wild salmon rivers and migration
corridors are at risk.

**Expected disagreement**
Hydrodynamic models simulate dispersal but depend strongly on ocean
circulation parameterisation and biological assumptions about larval
behaviour (vertical migration, mortality). Model predictions can vary
substantially for the same farm under different environmental conditions.

**Evidence types needed**
`model`, `empirical_observational`

**Key metadata filters**
`causal_chain_stage: larval_dispersal, environmental_drivers`
`study_design: hydrodynamic_modelling, particle_tracking`

---

## Q4: Smolt exposure to lice

**Question**
What determines the exposure of migrating wild salmon smolts to lice, and
which assumptions about smolt migration are most influential in exposure
estimates?

**Why this question matters**
Wild smolts migrate through fjords and coastal waters where farms may be
located. Exposure depends on migration timing, speed, route, and spatial
overlap with lice plumes. Migration duration assumptions are particularly
influential in mortality estimates — and are among the most uncertain
parameters in the entire causal chain.

**Expected disagreement**
Migration timing and duration are rarely directly observed. Models use
assumed or proxy values that differ between research groups. Small changes
in these assumptions produce large differences in estimated lice loads.

**Evidence types needed**
`empirical_observational`, `empirical_experimental`, `model`

**Key metadata filters**
`causal_chain_stage: host_exposure`
`outcome_domain: migration_timing, migration_route, infestation_pressure`

---

## Q5: Model predictions of infestation on wild fish

**Question**
How well do operational models predict lice infestation levels on wild
fish, and what is the residual uncertainty after calibration?

**Why this question matters**
Operational monitoring systems combine hydrodynamic lice models with field
observations of lice on captured wild fish. Model–observation agreement
is the primary validation basis for regulatory use of these models. The
degree of residual uncertainty determines how much weight to place on
model outputs in regulatory decisions.

**Expected disagreement**
Model predictions correlate with observed lice levels but still contain
substantial uncertainty due to environmental variability and sampling
limitations. Different research groups have assessed model performance
differently, and monitoring protocols vary by region.

**Evidence types needed**
`model`, `empirical_observational`

**Key metadata filters**
`causal_chain_stage: model_calibration, model_validation`
`study_design: sentinel_cage, wild_fish_sampling`

---

## Q6: Physiological effects of infestation on wild fish

**Question**
At what infestation levels do lice cause physiological stress or mortality
in wild salmonids, and how do these thresholds vary with fish size,
condition, and life stage?

**Why this question matters**
Experimental studies provide the biological mechanism linking lice load
to host damage. Severe infestations can cause mortality in post-smolts,
which are particularly vulnerable due to their small size. These
thresholds underpin dose–response models used to estimate mortality.

**Expected disagreement**
Most experimental evidence comes from controlled challenge studies, which
may not reflect conditions in the wild. Thresholds vary with temperature,
fish condition, and lice species. Extrapolation from experimental to field
conditions is contested.

**Evidence types needed**
`empirical_experimental`, `review`

**Key metadata filters**
`causal_chain_stage: physiological_effects, behaviour`
`wild_or_farmed_focus: wild`
`life_stage: smolt, post_smolt`

---

## Q7: Translating infestation to mortality estimates

**Question**
How can infestation levels observed on wild fish be translated into
mortality estimates, and how robust are the dose–response relationships
used for this?

**Why this question matters**
This translation step is one of the largest sources of uncertainty in
the entire causal chain. Mortality is estimated using dose–response
relationships derived from limited experiments. These may vary with fish
size, temperature, and condition — and are applied in contexts that
differ substantially from the experimental conditions.

**Expected disagreement**
The dose–response relationship used in Norwegian regulatory models has
been contested on the grounds of limited experimental basis, lack of
validation in field conditions, and sensitivity to parameter choices.
This is a central point of scientific disagreement in the field.

**Evidence types needed**
`empirical_experimental`, `model`, `review`

**Key metadata filters**
`causal_chain_stage: individual_mortality`
`outcome_domain: survival, mortality`
`study_design: laboratory_challenge, virtual_post_smolt_modelling`

---

## Q8: Fraction of smolts dying due to lice

**Question**
What fraction of migrating smolts actually die due to lice infestation,
and how sensitive are model-based estimates to input assumptions?

**Why this question matters**
This is the headline number in regulatory risk assessments. Model-based
estimates suggest large spatial variation — from <10% mortality in some
rivers to >30% in high-exposure regions. However, these values depend
strongly on model assumptions and calibration data. Understanding the
sensitivity of these estimates is critical for their regulatory use.

**Expected disagreement**
Different modelling groups have produced different estimates for the same
areas and periods. The sensitivity of results to migration duration, lice
load thresholds, and dispersal parameters is a major source of disagreement.
Field-based estimates of smolt mortality are rare and difficult to obtain.

**Evidence types needed**
`model`, `empirical_observational`, `review`

**Key metadata filters**
`causal_chain_stage: individual_mortality`
`outcome_domain: mortality, marine_survival`
`study_design: virtual_post_smolt_modelling`

---

## Q9: Population-level impact of lice-induced mortality

**Question**
Even where lice increase individual smolt mortality, does this translate
to reduced adult returns and impaired population viability — and how does
lice-induced mortality compare to other sources of marine mortality?

**Why this question matters**
Individual-level mortality estimates do not automatically imply
population-level harm. The key question is whether lice-induced mortality
is additive (on top of other mortality) or compensatory (replacing other
mortality that would have occurred anyway). Marine survival is also
affected by climate, predation, fisheries, and food availability at sea.

**Expected disagreement**
Some studies argue that marine survival changes are dominated by broader
oceanic factors, making lice impacts difficult to detect at population
level. Others argue the mortality is additive and population-significant
in high-exposure rivers. This is one of the most contested questions in
the field.

**Evidence types needed**
`empirical_observational`, `model`, `review`

**Key metadata filters**
`causal_chain_stage: population_impacts`
`outcome_domain: marine_survival, adult_returns, population_abundance`
`effect_scale: population_level`

---

## Q10: Robustness of the Norwegian Traffic Light System

**Question**
How robust is the Norwegian Traffic Light System as a regulatory
assessment framework, and how sensitive are its classifications to
model assumptions, calibration data, and monitoring design?

**Why this question matters**
The Traffic Light System determines whether Norwegian production areas
may grow, maintain, or reduce capacity. Its classifications are based on
models estimating lice-induced mortality. The robustness of these
classifications — and whether they correctly reflect the state of evidence
— determines the legitimacy of the regulatory framework.

**Expected disagreement**
The industry has challenged both the underlying models and the threshold
values. Researchers have raised questions about sensitivity to migration
assumptions, calibration data limitations, uncertainty propagation, and
monitoring representativeness. HI and the expert group have defended the
system. This is the central regulatory controversy of this corpus.

**Evidence types needed**
`model`, `regulatory`, `review`, `commentary`

**Key metadata filters**
`causal_chain_stage: regulatory_assessment`
`regulatory_context: Norway_TLS, Norway_expert_group`
`outcome_domain: regulatory_classification, model_performance, uncertainty_estimation`

---

## Relationship to the corpus

Each document included in this corpus must:
- contribute evidence to at least one priority question (Q1–Q10)
- have its relevance justified explicitly in `included_because`
- be interpretable within the context defined by these questions
- record the relevant question IDs in `priority_questions`
  and the relevant causal chain stage(s) in `causal_chain_stage`
