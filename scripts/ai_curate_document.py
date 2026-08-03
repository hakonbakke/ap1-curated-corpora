"""
AI-curate one document from extracted.md → summary.md + metadata.yaml.

Human role stops at paper selection. This script fills Del A–E as an AI draft
and sets curator_review_status: ai_draft.

Usage (from repo root):
    python scripts/ai_curate_document.py --doc 2025_jae_jansen-lice-effects-returns
    python scripts/ai_curate_document.py --doc NEW_DOC_ID --force

Requires OPENAI_API_KEY. Requires documents/<doc_id>/extracted.md.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_paths import (  # noqa: E402
    PRIORITY_QUESTIONS_PATH,
    STATUS_AI_DRAFT,
    TEMPLATE_PATH,
    doc_dir,
    list_doc_ids,
)

load_dotenv()

CURATE_MODEL = os.getenv("AP1_CURATE_MODEL", "gpt-4o")
# Keep under low org TPM tiers (~30k TPM on gpt-4o).
EXTRACT_CHAR_CAP = int(os.getenv("AP1_CURATE_EXTRACT_CHARS", "40000"))

SYSTEM = """\
You are the AI curator for AP1 (Havbruksløftet): a curated evidence corpus on
salmon lice and mortality of wild salmonids (Honest Broker approach).

Rules (MUST follow):
1. Use ONLY the provided extracted.md text. Never invent studies, numbers, or findings.
2. If a value is not in the extract, use null, "unclear", empty list, or omit — do not guess.
3. Mark uncertain judgments with the prefix [UNVERIFIED] in free-text fields.
4. Preserve disagreement; do not advocate for a policy outcome.
5. evidence_direction must use taxonomy values exactly:
   supports_effect | weak_support | mixed_within_study | no_effect_detected |
   contradicts_effect | critiques_methodology | not_applicable
   (use no_effect_detected, never no_significant_effect)
5b. controversy_role is a DIFFERENT axis from evidence_direction — never copy
   evidence_direction values into it. controversy_role is the paper's position
   in a scientific debate, not its substantive finding on lice effects.
   Allowed: foundational | supportive | critical | rebuttal |
   bridge_between_positions | peripheral | not_applicable
   Do NOT invent values such as challenges_effect, supports_effect, or
   mixed_within_study for controversy_role.
6. priority_questions must be a subset of Q1–Q10 justified by the paper's content.
7. related_documents_* must use existing corpus doc_ids from the provided list when possible;
   otherwise leave empty rather than inventing links.
8. Write summary.md and rag_summary in English.
9. Set curator_review_status to ai_draft.
10. Output valid JSON only (schema below). metadata_yaml must be valid YAML matching the template fields.
"""

USER_TEMPLATE = """\
## Document id
{doc_id}

## Existing corpus doc_ids (for related_* links)
{doc_id_list}

## Priority questions (abbreviated)
{priority_questions}

## Metadata template (field guide — fill all Del A–E fields you can)
{template}

## Extracted source text (from PDF)
<<<EXTRACT
{extract}
EXTRACT>>>

## Output JSON schema
{{
  "summary_md": "full markdown for summary.md — sections: Background, Methods, Main findings (with numbers), Uncertainty and limitations, Relevance to this corpus, Relation to other documents. Mark as AI-generated.",
  "metadata_yaml": "complete YAML document for metadata.yaml (no comment-only instruction lines required; include real values). Must include curator_review_status: ai_draft, added_by: ai_curate_pipeline, added_date: {today}"
}}
"""


def _load_text(path: Path, cap: int | None = None) -> str:
    text = path.read_text(encoding="utf-8")
    if cap and len(text) > cap:
        head = int(cap * 0.65)
        tail = cap - head
        return (
            text[:head]
            + f"\n\n[... TRUNCATED middle; kept head {head} + tail {tail} chars ...]\n\n"
            + text[-tail:]
        )
    return text


def _priority_abbrev(raw: str, max_chars: int = 6000) -> str:
    """Keep question headers + first paragraph to save tokens."""
    chunks: list[str] = []
    for block in re.split(r"\n(?=## Q\d+)", raw):
        if block.startswith("# Priority") or block.startswith("## The causal"):
            chunks.append(block[:800])
            continue
        if block.startswith("## Q"):
            lines = block.strip().splitlines()
            head = "\n".join(lines[:12])
            chunks.append(head)
    out = "\n\n".join(chunks)
    return out[:max_chars]


def _extract_json(content: str) -> dict:
    content = content.strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)
    return json.loads(content)


def curate_document(client: OpenAI, doc_id: str, force: bool = False) -> Path:
    d = doc_dir(doc_id)
    extract_path = d / "extracted.md"
    if not extract_path.exists():
        raise FileNotFoundError(
            f"Missing {extract_path}. Run convert_pdfs_odl.py or add_paper.py with --pdf first."
        )

    summary_path = d / "summary.md"
    meta_path = d / "metadata.yaml"
    if not force and meta_path.exists() and summary_path.exists():
        raise FileExistsError(
            f"{doc_id} already has summary.md and metadata.yaml. Pass --force to overwrite."
        )

    d.mkdir(parents=True, exist_ok=True)
    extract = _load_text(extract_path, EXTRACT_CHAR_CAP)
    template = _load_text(TEMPLATE_PATH)
    pq = _priority_abbrev(_load_text(PRIORITY_QUESTIONS_PATH))
    others = [x for x in list_doc_ids() if x != doc_id]

    user = USER_TEMPLATE.format(
        doc_id=doc_id,
        doc_id_list="\n".join(f"- {x}" for x in others) or "(empty corpus)",
        priority_questions=pq,
        template=template,
        extract=extract,
        today=date.today().isoformat(),
    )

    print(f"Curating {doc_id} with {CURATE_MODEL}...")
    resp = client.chat.completions.create(
        model=CURATE_MODEL,
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user},
        ],
    )
    data = _extract_json(resp.choices[0].message.content or "{}")
    summary_md = (data.get("summary_md") or "").strip()
    metadata_yaml = (data.get("metadata_yaml") or "").strip()
    if not summary_md or not metadata_yaml:
        raise ValueError("Model returned empty summary_md or metadata_yaml")

    # Enforce trust status
    if "curator_review_status:" not in metadata_yaml:
        metadata_yaml += f"\n\ncurator_review_status: {STATUS_AI_DRAFT}\n"
    else:
        metadata_yaml = re.sub(
            r"curator_review_status:\s*\S+",
            f"curator_review_status: {STATUS_AI_DRAFT}",
            metadata_yaml,
            count=1,
        )

    summary_path.write_text(summary_md + "\n", encoding="utf-8")
    meta_path.write_text(metadata_yaml + "\n", encoding="utf-8")
    print(f"  wrote {summary_path}")
    print(f"  wrote {meta_path}")
    print(f"  status: {STATUS_AI_DRAFT}")
    return d


def main() -> int:
    parser = argparse.ArgumentParser(description="AI-curate summary + metadata from extract")
    parser.add_argument("--doc", required=True, help="Document folder id")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not set", file=sys.stderr)
        return 1

    client = OpenAI()
    try:
        curate_document(client, args.doc, force=args.force)
    except (FileNotFoundError, FileExistsError, ValueError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
