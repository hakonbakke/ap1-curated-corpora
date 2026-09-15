"""Shared paths and helpers for AP1 corpus pipelines."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

VILLAKS_SLUG = "salmon-lice-and-mortality-of-wild-salmonids"
AREAL_SLUG = "area-and-aquaculture"
DEFAULT_SLUG = VILLAKS_SLUG


@dataclass(frozen=True)
class CorpusPaths:
    slug: str
    root: Path
    docs_dir: Path
    pdf_dir: Path
    parquet: Path
    template_path: Path
    priority_questions_path: Path

    def doc_dir(self, doc_id: str) -> Path:
        return self.docs_dir / doc_id

    def list_doc_ids(self) -> list[str]:
        if not self.docs_dir.exists():
            return []
        return sorted(
            d.name
            for d in self.docs_dir.iterdir()
            if d.is_dir() and d.name != "PDFs" and not d.name.startswith("_")
        )


def get_corpus(slug: str | None = None) -> CorpusPaths:
    slug = slug or DEFAULT_SLUG
    root = REPO_ROOT / "corpora" / slug
    parquet_name = "corpus.parquet" if slug == VILLAKS_SLUG else f"{slug}.parquet"
    return CorpusPaths(
        slug=slug,
        root=root,
        docs_dir=root / "documents",
        pdf_dir=root / "documents" / "PDFs",
        parquet=REPO_ROOT / "data" / parquet_name,
        template_path=root / "metadata_template.yaml",
        priority_questions_path=root / "PRIORITY_QUESTIONS.md",
    )


# Backward-compatible aliases (villaks / default)
CORPUS = get_corpus(VILLAKS_SLUG).root
DOCS_DIR = get_corpus(VILLAKS_SLUG).docs_dir
PDF_DIR = get_corpus(VILLAKS_SLUG).pdf_dir
TEMPLATE_PATH = get_corpus(VILLAKS_SLUG).template_path
PRIORITY_QUESTIONS_PATH = get_corpus(VILLAKS_SLUG).priority_questions_path
DATA_FILE = get_corpus(VILLAKS_SLUG).parquet

# Trust model (human selects papers; AI curates + verifies against extract)
STATUS_AI_DRAFT = "ai_draft"
STATUS_AI_VERIFIED = "ai_verified"
STATUS_EXPERT_APPROVED = "expert_approved"
STATUS_PENDING = "pending"

VALID_STATUSES = {
    STATUS_AI_DRAFT,
    STATUS_AI_VERIFIED,
    STATUS_EXPERT_APPROVED,
    STATUS_PENDING,
    "reviewed",
    "approved",
}


def doc_dir(doc_id: str) -> Path:
    return get_corpus().doc_dir(doc_id)


def list_doc_ids() -> list[str]:
    return get_corpus().list_doc_ids()


def strip_yaml_comments(raw: str) -> str:
    return "\n".join(
        line
        for line in raw.splitlines()
        if not line.lstrip().startswith("#") or line.strip() == "#"
    )
