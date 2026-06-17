"""
expand_summaries_from_extract.py — Expand documents/*/summary.md from extracted.md.

Uses OpenAI to produce structured evidence briefs (methods, numbers, limitations, COI).
Skips documents that already meet --min-chars unless --force.

Usage (from repo root):
    python scripts/expand_summaries_from_extract.py --dry-run
    python scripts/expand_summaries_from_extract.py --doc 1997_icesjms_dawson-seatrout-salmon-susceptibility
    python scripts/expand_summaries_from_extract.py --min-chars 4500

Then re-run: python scripts/ingest.py
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import yaml
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "corpora" / "salmon-lice-and-mortality-of-wild-salmonids" / "documents"
EXTRACT_MAX_CHARS = 95_000
MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You write evidence briefs for a curated salmon-lice research corpus.
Output ONLY valid markdown for summary.md — no preamble, no code fences.

Rules:
- Use ONLY facts, numbers, and claims supported by the supplied extract and metadata.
- Do not invent studies, results, or citations.
- Preserve nuance: limitations, what authors did NOT claim, and uncertainty.
- Include quantitative detail (sample sizes, effect sizes, thresholds, dates, geography).
- Structured sections with ## headings (see template).
- Target roughly 1,800–2,800 words for full papers; 900–1,400 for short communications or comments.
- English prose; keep species names italicized where appropriate (*Salmo salar*).
- End with a single line: *Expanded from extracted.md YYYY-MM-DD for synthesis context.*"""

USER_TEMPLATE = """Document ID: {doc_id}

## Current metadata (for alignment — do not contradict)
Title: {title}
Year: {year}
Authors: {authors}
rag_summary (keep consistent with this): {rag_summary}

## Current summary.md (may be short — expand and enrich)
{current_summary}

## Paper extract (OpenDataLoader — primary source)
{extract}

---

Write an expanded **summary.md** using this structure:

# Summary: [Short author et al. year title]

**Full title:** ...
**Journal:** ...
**DOI / URL:** ...
**Document type:** ...
**Priority questions:** ...
**Funding / COI:** ...

---

## What this paper does
(2–4 paragraphs: question, design, geography, period, why it matters in corpus)

## Methods and data
(design, samples, models, thresholds, key definitions)

## Key findings
(subsections or bullets with numbers; tables summarised in markdown where useful)

## Limitations and caveats
(author-stated and methodological)

## What this paper does not claim
(explicit boundaries — important for synthesis)

## Relevance to this corpus
(link to Q IDs, debate chains, related doc_ids if known from text)

## Related evidence in corpus
(only if clearly inferable from extract/metadata; else omit section)
"""


def load_meta(meta_path: Path) -> dict:
    raw = meta_path.read_text(encoding="utf-8")
    clean = "\n".join(
        line for line in raw.splitlines()
        if not line.lstrip().startswith("#") or line.strip() == "#"
    )
    return yaml.safe_load(clean) or {}


def doc_ids() -> list[str]:
    return sorted(
        d.name
        for d in DOCS_DIR.iterdir()
        if d.is_dir() and d.name != "PDFs" and (d / "metadata.yaml").exists()
    )


def expand_one(
    client: OpenAI | None,
    doc_id: str,
    *,
    force: bool,
    min_chars: int,
    dry_run: bool,
) -> str:
    doc_dir = DOCS_DIR / doc_id
    meta = load_meta(doc_dir / "metadata.yaml")
    extract_path = doc_dir / "extracted.md"
    summary_path = doc_dir / "summary.md"

    if not extract_path.exists():
        return f"SKIP {doc_id}: no extracted.md"

    current = summary_path.read_text(encoding="utf-8") if summary_path.exists() else ""
    if not force and len(current) >= min_chars:
        return f"SKIP {doc_id}: summary already {len(current)} chars (>= {min_chars})"

    extract = extract_path.read_text(encoding="utf-8")
    if len(extract) > EXTRACT_MAX_CHARS:
        extract = (
            extract[: EXTRACT_MAX_CHARS // 2]
            + "\n\n[… middle of extract omitted for length …]\n\n"
            + extract[-EXTRACT_MAX_CHARS // 2 :]
        )

    authors = meta.get("authors", []) or []
    authors_str = "; ".join(str(a) for a in authors)
    rag = (meta.get("rag_summary") or "").strip().replace("\n", " ")

    user_msg = USER_TEMPLATE.format(
        doc_id=doc_id,
        title=meta.get("title", ""),
        year=meta.get("year", ""),
        authors=authors_str,
        rag_summary=rag[:2000],
        current_summary=current[:6000] if current else "(none)",
        extract=extract,
    )

    if dry_run:
        return f"DRY-RUN {doc_id}: would expand ({len(current)} -> target >= {min_chars} chars)"

    if client is None:
        raise RuntimeError("OpenAI client required when not dry-run")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.2,
        max_tokens=4500,
    )
    out = response.choices[0].message.content.strip()
    if out.startswith("```"):
        lines = out.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        out = "\n".join(lines).strip()

    summary_path.write_text(out + "\n", encoding="utf-8")
    return f"OK {doc_id}: wrote {len(out)} chars"


def main() -> int:
    parser = argparse.ArgumentParser(description="Expand summary.md from extracted.md")
    parser.add_argument("--doc", metavar="DOC_ID", help="Process one document folder")
    parser.add_argument("--force", action="store_true", help="Rewrite even if summary is long enough")
    parser.add_argument("--min-chars", type=int, default=4500, help="Skip if summary already this long")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ids = [args.doc] if args.doc else doc_ids()
    if args.doc and args.doc not in doc_ids():
        print(f"Unknown doc_id: {args.doc}")
        return 1

    client = OpenAI() if not args.dry_run else None

    for i, doc_id in enumerate(ids, 1):
        print(f"[{i}/{len(ids)}] ", end="", flush=True)
        msg = expand_one(
            client,
            doc_id,
            force=args.force,
            min_chars=args.min_chars,
            dry_run=args.dry_run,
        )
        if client is not None:
            time.sleep(0.5)
        print(msg)

    return 0


if __name__ == "__main__":
    sys.exit(main())
