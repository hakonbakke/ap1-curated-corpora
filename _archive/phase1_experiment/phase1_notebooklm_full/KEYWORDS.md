# Keyword Ontology
## Corpus: Salmon Lice and Mortality of Wild Salmonids

Keywords are grouped by causal chain stage, corresponding to the 10
priority questions in `PRIORITY_QUESTIONS.md`.

Use these keywords to:
- guide literature searches (Scopus, Google Scholar, Web of Science)
- populate `retrieval_tags` in document metadata
- structure RAG retrieval queries
- identify gaps in corpus coverage

---

## Core set (36 keywords)

A concise, structured keyword set covering the full causal chain.

### 1. Lice production in aquaculture farms (→ Q1, Q2)
- Salmon aquaculture
- Salmon lice (*Lepeophtheirus salmonis*)
- Farm lice abundance
- Adult female lice
- Egg production rate
- Lice reproductive output

### 2. Larval production and infective stages (→ Q2)
- Nauplius larvae
- Copepodid stage
- Larval survival
- Temperature-dependent development
- Degree-days

### 3. Dispersal from farms (→ Q3)
- Lice larval dispersal
- Hydrodynamic circulation
- Ocean current transport
- Particle tracking models
- Larval drift distance

### 4. Environmental drivers of lice distribution (→ Q3, Q4)
- Temperature gradients
- Salinity gradients
- Wind-driven circulation
- Fjord hydrodynamics

### 5. Smolt exposure to lice (→ Q4, Q5)
- Smolt migration timing
- Smolt migration routes
- Coastal migration corridors
- Spatial overlap with farms

### 6. Infestation processes (→ Q5, Q6)
- Infestation pressure
- Lice attachment success
- Host–parasite interaction

### 7. Physiological effects on wild fish (→ Q6)
- Skin damage
- Osmoregulation impairment
- Stress response

### 8. Individual fish mortality (→ Q7, Q8)
- Lice load thresholds
- Dose–response relationship
- Post-smolt mortality

### 9. Population-level consequences (→ Q9)
- Marine survival
- Smolt-to-adult return rate (SAR)
- Population recruitment

### 10. Monitoring, modelling, and management (→ Q5, Q8, Q10)
- Lice monitoring programs
- Lice dispersion models
- Virtual smolt models
- Traffic Light System (TLS)

---

## Extended ontology (~75 keywords)

A more detailed keyword set for systematic searches and fine-grained
RAG retrieval, with additional biological, oceanographic, modelling,
statistical, and regulatory terms.

### 1. Aquaculture sources of lice (→ Q1, Q2)
- Salmon aquaculture
- Marine cage farming
- Farmed salmon biomass
- Stocking density
- Salmon lice (*Lepeophtheirus salmonis*)
- Farm lice abundance
- Adult female lice
- Egg string production
- Lice reproductive output
- Chemotherapeutant resistance

### 2. Lice life cycle and larval production (→ Q2)
- Nauplius I
- Nauplius II
- Copepodid stage
- Infective stage
- Larval survival
- Degree-day development
- Temperature-dependent development
- Larval mortality
- Host-seeking behaviour

### 3. Larval dispersal and oceanography (→ Q3)
- Larval dispersal
- Hydrodynamic circulation
- Ocean current transport
- Particle tracking models
- Lagrangian dispersal models
- Larval drift distance
- Fjord circulation
- Coastal currents
- Vertical migration behaviour
- Wind-driven transport

### 4. Environmental drivers of lice dynamics (→ Q3, Q4)
- Temperature gradients
- Salinity gradients
- Freshwater runoff
- Stratification
- Turbulence
- Seasonal variability
- Climate variability

### 5. Exposure of migrating smolts (→ Q4)
- Smolt migration timing
- Smolt migration routes
- Migration speed
- Migration duration
- Coastal migration corridors
- Fjord residence time
- Spatial overlap with farms

### 6. Infestation processes (→ Q5, Q6)
- Infestation pressure
- Infection pressure
- Host encounter rate
- Attachment success
- Host–parasite interaction
- Lice load
- Parasite burden

### 7. Physiological and behavioural effects (→ Q6)
- Skin lesions
- Osmoregulation impairment
- Stress response
- Cortisol levels
- Secondary infections
- Reduced swimming performance
- Behavioural avoidance

### 8. Individual mortality processes (→ Q7, Q8)
- Lice load thresholds
- Dose–response relationship
- Condition-dependent mortality
- Post-smolt mortality
- Size-dependent susceptibility
- Acute mortality

### 9. Population-level impacts (→ Q9)
- Marine survival
- Smolt-to-adult return rate (SAR)
- Recruitment dynamics
- Population productivity
- Density dependence
- Compensatory mortality
- Stock–recruitment relationship

### 10. Monitoring, modelling, and regulation (→ Q5, Q8, Q10)
- Lice monitoring programs
- Sentinel cages
- Wild fish sampling
- Hydrodynamic lice models
- Virtual smolt models
- Model calibration
- Parameter uncertainty
- Sensitivity analysis
- Traffic Light System (TLS)
- Risk-based aquaculture regulation

---

## Notes on literature search use

When running systematic searches, combine terms across causal chain stages
to find documents that bridge multiple steps. Key high-yield combinations:

- `salmon lice` + `wild salmon` + `mortality`
- `lice dispersal` + `hydrodynamic` + `smolt`
- `dose-response` + `Lepeophtheirus` + `post-smolt`
- `traffic light system` + `salmon lice` + `model`
- `smolt migration` + `infestation` + `fjord`
- `marine survival` + `sea lice` + `Atlantic salmon`

Record all search strings and databases in `inclusion_log.md`.
