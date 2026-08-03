# Architecture — hybrid stack and positioning

**Status:** Reference / ideas · **Updated:** 2026-07-03

---

## Three products, three jobs

| System | Job | AP1 relationship |
|--------|-----|------------------|
| **FHF KI-formidler** | Formidle FHF-prosjekter og sluttrapporter ([fhf.no](https://www.fhf.no/prosjekter/ki-formidler/)) | Complementary — broad formidling, not contested-evidence layer |
| **AP1 Streamlit RAG** | Honest Broker synthesis on curated peer-reviewed corpus | **Primary deliverable** for Havbruksløftet / demo |
| **Obsidian LLM wiki** | Personal compile layer: cross-domain, grey + academic (`Obsidian/` vault) | Optional L1; do not re-curate AP1 papers separately |

---

## Hybrid model (L1 + L2)

Industry consensus (2026): not wiki *or* RAG — **both at different layers**.

```
L1  Compiled wiki     →  stable synthesis, debate maps, concept navigation
L2  Governed RAG      →  traceable DOI answers, metadata filters, demo UI
L3  External formidling → FHF KI-formidler (not owned by AP1)
```

**Karpathy “LLM wiki”** = compile at ingest, query compiled markdown.  
**AP1 RAG** = retrieve at query from governed `metadata.yaml` + embeddings.  
**Infographic overclaim:** RAG does not “accumulate zero”; AP1 corpus grows at ingest. Wiki is not zero-maintenance — requires COMPILE, lint, human curation of `raw/`.

---

## What benchmark showed (2026-07-03)

Same question: *evidence that farm lice cause wild salmon population decline.*

| | FHF KI-formidler | AP1 API |
|--|------------------|---------|
| Sources | 20 FHF projects (many peripheral) | 12 peer-reviewed (relevant) |
| Debate (Van Nes ↔ Stige) | Absent | Present |
| Population level (Q9) | Attempted (FHF reports) | Jansen 2025 retrieved but underused in prose |
| Counter-evidence (Jones BC, Dadswell) | Absent | Not retrieved |
| Risk | Over-coherent “pro-causal” narrative | “High confidence” after showing debate |

**Positioning sentence:** KI-formidler answers “what has FHF-funded research found?” AP1 answers “what does the evidence say — including disagreement — on contested questions like TLS?”

---

## HAVREG / UiS collaboration (from email thread)

- **No course change** on HAVREG as structured registry (system of record).
- AP1 + optional wiki = **knowledge layer on top**, not replacement for registration databases.
- **Sequence:** land AP1 demo → optional wiki link → broader data platform later.

---

## Obsidian vault (existing, external to this repo)

Path: `C:\Users\ThordHåkonBakke\OneDrive - Blue Planet AS\Obsidian`

| Layer | Scale (Jul 2026) |
|-------|------------------|
| `raw/` | 223 extracts |
| `wiki/` | 68 concept articles |
| Workflows | `prompts/COMPILE.md`, lint, `log.md` |

**Integration ideas (all optional):**

1. Auto-generate `wiki/Q9-population-impact.md` from AP1 `PRIORITY_QUESTIONS.md` + metadata.
2. Sync AP1 `summary.md` exports into `raw/Selected/` (single source for curated papers).
3. Cursor workflow: read wiki for map → AP1 RAG for citable answer.

**Do not:** maintain parallel corpus in `Koding/LLM_wiki/` (planned P2, superseded by Obsidian).

---

## GraphRAG and enterprise patterns

- **GraphRAG:** Useful at large scale; AP1 already has `related_documents_contrasting`, debate map, `priority_questions` — lightweight graph in YAML.
- **ACL 2026 finding:** retrieval–generation gap — more retrieval does not always improve answers; measure on generation quality, not retrieval metrics alone.
- **AquaVision stack** (see `AI_R&D/01_Knowledge_Base/Concepts/2026-aquavision-ai-dataarkitektur-havbruk.md`): data → ontology → logic → agents — relevant for long-term HAVREG, not AP1 MVP scope.
