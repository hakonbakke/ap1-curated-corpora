# Archive

This folder contains earlier experimental work that is no longer part of the active pipeline.
Files are kept for reference and reproducibility documentation.

## `phase1_experiment/`

NotebookLM phase 1 testing (March 2026). Compared PDF-only vs curated metadata+summaries
vs generic ChatGPT on Q1–Q3-style questions. Raw outputs documented in
`Test_phase1_ap1_extracted.txt` and `Test_phase1_ap1.docx`.

The `phase1_notebooklm_full/` and `phase1_notebooklm_md/` folders were the input bundles
uploaded to NotebookLM for that experiment.

## `ragie/`

Ragie.ai integration (March 2026). Ragie was used as a managed RAG service.
The partition `ap1-curated-summaries` was populated via the upload script.
Superseded by the local Streamlit app (`app/`) which gives full control
over retrieval, metadata filtering, and synthesis prompts.
