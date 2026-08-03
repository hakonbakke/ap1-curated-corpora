"""
Add-paper pipeline: human selects PDF + doc_id; AI does the rest.

Stages:
  1. Place PDF / extract → extracted.md
  2. AI curate → summary.md + metadata.yaml (ai_draft)
  3. AI verify → qa_report.json + status ai_verified|ai_draft
  4. Ingest → data/corpus.parquet (optional)

Usage (from repo root):
    # New paper from a local PDF
    python scripts/add_paper.py --doc 2025_journal_keyword --pdf path\\to\\paper.pdf

    # PDF already in documents/PDFs/ (uses convert_pdfs_odl mapping)
    python scripts/add_paper.py --doc 2025_journal_keyword --extract-only
    python scripts/add_paper.py --doc 2025_journal_keyword   # full pipeline if extract exists or PDF mapped

    # Skip stages
    python scripts/add_paper.py --doc ID --skip-extract --skip-ingest
    python scripts/add_paper.py --doc ID --verify-only

Trust model: human = inclusion decision only. AI curates and checks against extract.
Expert approval is optional (expert_approved), not required for corpus use.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_paths import PDF_DIR, REPO_ROOT, doc_dir  # noqa: E402

load_dotenv()


def _run(cmd: list[str]) -> None:
    print(">", " ".join(cmd))
    r = subprocess.run(cmd, cwd=str(REPO_ROOT))
    if r.returncode != 0:
        raise RuntimeError(f"Command failed ({r.returncode}): {' '.join(cmd)}")


def stage_extract(doc_id: str, pdf: Path | None) -> None:
    d = doc_dir(doc_id)
    d.mkdir(parents=True, exist_ok=True)
    out = d / "extracted.md"

    if pdf is not None:
        if not pdf.exists():
            raise FileNotFoundError(pdf)
        PDF_DIR.mkdir(parents=True, exist_ok=True)
        dest = PDF_DIR / pdf.name
        if pdf.resolve() != dest.resolve():
            shutil.copy2(pdf, dest)
            print(f"Copied PDF → {dest}")
        # Convert this PDF directly into the doc folder
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from convert_pdfs_odl import convert_one  # noqa: E402

        print(f"Extracting {pdf.name} → {out}")
        convert_one(dest if dest.exists() else pdf, out)
        print(f"  wrote {out} ({out.stat().st_size} bytes)")
        return

    if out.exists():
        print(f"Extract exists: {out}")
        return

    # Fall back to ODL batch mapper
    _run([sys.executable, "scripts/convert_pdfs_odl.py", "--doc", doc_id])
    if not out.exists():
        raise FileNotFoundError(
            f"No extracted.md for {doc_id}. Pass --pdf PATH or place PDF in documents/PDFs/"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Human selects paper; AI extracts, curates, verifies, ingests"
    )
    parser.add_argument("--doc", required=True, help="Document id YYYY_journal_keyword")
    parser.add_argument("--pdf", type=Path, help="Path to source PDF")
    parser.add_argument("--force-curate", action="store_true", help="Overwrite summary/metadata")
    parser.add_argument("--skip-extract", action="store_true")
    parser.add_argument("--skip-curate", action="store_true")
    parser.add_argument("--skip-verify", action="store_true")
    parser.add_argument("--skip-ingest", action="store_true")
    parser.add_argument("--extract-only", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()

    doc_id = args.doc.strip()
    if "/" in doc_id or "\\" in doc_id:
        print("ERROR: --doc must be a folder id, not a path", file=sys.stderr)
        return 1

    try:
        if args.verify_only:
            _run([sys.executable, "scripts/ai_verify_document.py", "--doc", doc_id])
            return 0

        if not args.skip_extract:
            stage_extract(doc_id, args.pdf)

        if args.extract_only:
            return 0

        if not args.skip_curate:
            cmd = [sys.executable, "scripts/ai_curate_document.py", "--doc", doc_id]
            if args.force_curate:
                cmd.append("--force")
            # If files exist and no --force, curate will error — allow verify+ingest on existing
            meta = doc_dir(doc_id) / "metadata.yaml"
            summary = doc_dir(doc_id) / "summary.md"
            if meta.exists() and summary.exists() and not args.force_curate:
                print("summary.md + metadata.yaml exist; skipping curate (use --force-curate to redo)")
            else:
                _run(cmd)

        if not args.skip_verify:
            _run([sys.executable, "scripts/ai_verify_document.py", "--doc", doc_id])

        if not args.skip_ingest:
            _run([sys.executable, "scripts/ingest.py", "--doc", doc_id])

        print()
        print("Pipeline complete.")
        print(f"  folder: {doc_dir(doc_id)}")
        print("  Next: spot-check qa_report.json; restart Streamlit / reboot Cloud if deployed.")
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
