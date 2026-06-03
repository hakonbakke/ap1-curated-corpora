"""
Batch-convert corpus PDFs to Markdown using OpenDataLoader PDF.
Saves one extracted.md per document folder (matched by author/year heuristics).

Usage (from repo root):
    python scripts/convert_pdfs_odl.py
    python scripts/convert_pdfs_odl.py --doc 2025_jfd_jones-pacific-lice-cessation-bc
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CORPUS = REPO_ROOT / "corpora" / "salmon-lice-and-mortality-of-wild-salmonids"
PDF_DIR = CORPUS / "documents" / "PDFs"
DOCS_DIR = CORPUS / "documents"

# Manual overrides where filename heuristics fail
MANUAL_MAP: dict[str, str] = {
    "dawson": "1997_icesjms_dawson-seatrout-salmon-susceptibility",
    "mccormick": "1998_cjfas_mccormick-smolting-migration",
    "helland": "2015_aei_helland-monitoring-lice-challenges",
    "forseth": "2017_icesjms_forseth-major-threats-norway",
    "kristoffersen": "2018_epidemics_kristoffersen-risk-assessment",
    "fjelldal": "2020_conphys_fjelldal-lice-osmoregulation-salmon",
    "bøhn": "2020_jae_bohn-timing-survival-postsmolts",
    "bohn": "2020_jae_bohn-timing-survival-postsmolts",
    "finstad": "2021_aei_seatrout-risk-assessment",
    "jansen and gjerde": "2021_icesjms_jansen-comment-vps-mortality",
    "jansen et al_2021_comment": "2021_icesjms_jansen-comment-vps-mortality",
    "johnsen": "2021_icesjms_johnsen-vps-mortality-norway",
    "eliasen": "2021_rcn_traffic-light-evaluation",
    "dadswell": "2021_rfsa_dadswell-atlantic-salmon-collapse",
    "stige et al_2022": "2022_aei_stige-model-sensitivity-calibration",
    "stige et al_2022_modelling": "2022_aei_stige-model-sensitivity-calibration",
    "gillson": "2022_rfbf_gillson-marine-stressors-salmon",
    "lamberg": "2022_fishes_lamberg-pre-fishery-abundance",
    "stige et al_2024": "2024_ijpara_stige-regional-lice-coordination",
    "stige et al_2024_effects": "2024_ijpara_stige-regional-lice-coordination",
    "nes, imsland, jones_2024_salmon lice biology": "2024_raq_vannes-critical-review-tls",
    "hawley": "2024_ecosphere_hawley-anadromy-lice-mortality-trout",
    "gjerde": "2025_aquaculture_gjerde-seatrout-lice-prediction",
    "jansen et al_2025_effects": "2025_jae_jansen-lice-effects-returns",
    "crawford et al_2025_sea lice infestation dataset": "2025_scientificdata_bc-sealice-dataset-2001-2023",
    "sea lice infestation dataset for wild": "2025_scientificdata_bc-sealice-dataset-2001-2023",
    "s41597-025": "2025_scientificdata_bc-sealice-dataset-2001-2023",
    "stige et al_2025_comment": "2025_raq_stige-comment-vannes",
    "comment on salmon lice biology": "2025_raq_stige-comment-vannes",
    "stige et al 2025 comment on salmon": "2025_raq_stige-comment-vannes",
    "nes et al 2025 response to stige": "2025_raq_vannes-response-to-stige",
    "response to stige lc": "2025_raq_vannes-response-to-stige",
    "folk": "2026_prslb_folk-parasites-high-host-density",
    "jonsson": "2016_jfb_jonsson-environmental-change-salmon",
    "trends in sea lice infestations on chum": "2025_dao_jones-broughton-lice-unchanged",
    "trends in abundance of sea lice": "2025_jfd_jones-pacific-lice-cessation-bc",
}


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def match_pdf_to_doc(pdf_name: str, doc_ids: list[str]) -> str | None:
    stem = _norm(Path(pdf_name).stem)
    for key, doc_id in MANUAL_MAP.items():
        if _norm(key) in stem:
            return doc_id
    for doc_id in doc_ids:
        parts = doc_id.split("_")
        if len(parts) >= 3:
            hint = _norm(parts[2])
            if hint and hint in stem:
                return doc_id
        year = parts[0] if parts else ""
        if year and year in stem:
            for p in parts[2:]:
                if len(p) >= 5 and _norm(p) in stem:
                    return doc_id
    return None


# doc_id -> unique substring that must appear in PDF filename (lowercase)
DOC_PDF_HINTS: dict[str, str] = {
    "2025_raq_stige-comment-vannes": "stige et al_2025_comment on salmon",
    "2025_raq_vannes-response-to-stige": "nes et al_2025_response to stige",
    "2025_scientificdata_bc-sealice-dataset-2001-2023": "crawford et al_2025_sea lice infestation dataset",
    "2024_raq_vannes-critical-review-tls": "nes, imsland, jones_2024_salmon lice biology",
}


def build_mapping() -> dict[str, Path]:
    doc_ids = sorted(
        d.name for d in DOCS_DIR.iterdir() if d.is_dir() and d.name != "PDFs"
    )
    mapping: dict[str, Path] = {}
    unmatched: list[str] = []
    for pdf in sorted(PDF_DIR.glob("*.pdf")):
        doc_id = match_pdf_to_doc(pdf.name, doc_ids)
        if doc_id:
            if doc_id in mapping:
                print(f"WARNING: duplicate map for {doc_id}: {pdf.name}", file=sys.stderr)
            mapping[doc_id] = pdf
        else:
            unmatched.append(pdf.name)
    for doc_id, hint in DOC_PDF_HINTS.items():
        if doc_id not in mapping:
            hint_l = hint.lower()
            for pdf in PDF_DIR.glob("*.pdf"):
                if hint_l in pdf.name.lower():
                    mapping[doc_id] = pdf
                    break
    if unmatched:
        still = [u for u in unmatched if not any(u == p.name for p in mapping.values())]
        if still:
            print("WARNING: unmatched PDFs:", file=sys.stderr)
            for u in still:
                print(f"  - {u}", file=sys.stderr)
    return mapping


def convert_one(pdf: Path, out_md: Path) -> None:
    import opendataloader_pdf

    out_md.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_md.parent / "_odl_tmp"
    tmp.mkdir(exist_ok=True)
    opendataloader_pdf.convert(
        input_path=[str(pdf)],
        output_dir=str(tmp),
        format="markdown",
        quiet=True,
    )
    md_files = list(tmp.glob("*.md"))
    if not md_files:
        raise RuntimeError(f"No markdown output for {pdf}")
    out_md.write_text(md_files[0].read_text(encoding="utf-8"), encoding="utf-8")
    for f in tmp.iterdir():
        if f.is_file():
            f.unlink()
        elif f.is_dir():
            import shutil
            shutil.rmtree(f, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc", help="Convert only this document id")
    args = parser.parse_args()

    mapping = build_mapping()
    if args.doc:
        if args.doc not in mapping:
            print(f"ERROR: no PDF mapped for {args.doc}", file=sys.stderr)
            return 1
        mapping = {args.doc: mapping[args.doc]}

    print(f"Converting {len(mapping)} PDF(s)...")
    for doc_id, pdf in mapping.items():
        out = DOCS_DIR / doc_id / "extracted.md"
        print(f"  {doc_id} <- {pdf.name[:50]}...")
        try:
            convert_one(pdf, out)
            print(f"    -> {out} ({out.stat().st_size} bytes)")
        except Exception as e:
            print(f"    FAILED: {e}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
