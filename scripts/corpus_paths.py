"""Shared paths and helpers for the salmon-lice corpus pipeline."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CORPUS = REPO_ROOT / "corpora" / "salmon-lice-and-mortality-of-wild-salmonids"
DOCS_DIR = CORPUS / "documents"
PDF_DIR = DOCS_DIR / "PDFs"
TEMPLATE_PATH = CORPUS / "metadata_template.yaml"
PRIORITY_QUESTIONS_PATH = CORPUS / "PRIORITY_QUESTIONS.md"
DATA_FILE = REPO_ROOT / "data" / "corpus.parquet"

# Trust model (human selects papers; AI curates + verifies against extract)
STATUS_AI_DRAFT = "ai_draft"
STATUS_AI_VERIFIED = "ai_verified"
STATUS_EXPERT_APPROVED = "expert_approved"
# Legacy synonym treated as ai_draft
STATUS_PENDING = "pending"

VALID_STATUSES = {
    STATUS_AI_DRAFT,
    STATUS_AI_VERIFIED,
    STATUS_EXPERT_APPROVED,
    STATUS_PENDING,  # legacy
    "reviewed",  # legacy
    "approved",  # legacy → prefer expert_approved
}


def doc_dir(doc_id: str) -> Path:
    return DOCS_DIR / doc_id


def list_doc_ids() -> list[str]:
    return sorted(
        d.name
        for d in DOCS_DIR.iterdir()
        if d.is_dir() and d.name != "PDFs" and not d.name.startswith("_")
    )


def strip_yaml_comments(raw: str) -> str:
    return "\n".join(
        line
        for line in raw.splitlines()
        if not line.lstrip().startswith("#") or line.strip() == "#"
    )
