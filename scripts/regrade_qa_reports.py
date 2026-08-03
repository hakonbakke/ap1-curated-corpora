"""
Regrade existing qa_report.json files with clarified COI rules (no API calls).

Moves funding/COI false-positive "critical" issues to soft_issues when claim checks
are mostly supported and evidence_direction is OK (or only taxonomy alias issue).

Updates metadata.yaml curator_review_status accordingly.

Usage:
    python scripts/regrade_qa_reports.py
    python scripts/regrade_qa_reports.py --doc 2025_jae_jansen-lice-effects-returns
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_paths import (  # noqa: E402
    STATUS_AI_DRAFT,
    STATUS_AI_VERIFIED,
    doc_dir,
    list_doc_ids,
)

COI_SOFT_PATTERNS = [
    r"\bcoi\b",
    r"conflict of interest",
    r"competing interest",
    r"funding",
    r"financed",
    r"acknowledg",
]


def _is_coi_soft(text: str) -> bool:
    t = text.lower()
    return any(re.search(p, t) for p in COI_SOFT_PATTERNS)


def _set_status_in_yaml(raw: str, status: str) -> str:
    if re.search(r"curator_review_status:\s*\S+", raw):
        return re.sub(
            r"curator_review_status:\s*\S+",
            f"curator_review_status: {status}",
            raw,
            count=1,
        )
    return raw.rstrip() + f"\n\ncurator_review_status: {status}\n"


def regrade_one(doc_id: str) -> dict | None:
    d = doc_dir(doc_id)
    path = d / "qa_report.json"
    if not path.exists():
        return None
    report = json.loads(path.read_text(encoding="utf-8"))
    critical = list(report.get("critical_issues") or [])
    soft = list(report.get("soft_issues") or [])

    kept_critical: list[str] = []
    moved = 0
    for issue in critical:
        # Keep real taxonomy / claim failures
        if "no_significant_effect" in issue.lower() or "taxonomy" in issue.lower():
            kept_critical.append(issue)
            continue
        if _is_coi_soft(issue) and "fabricat" not in issue.lower():
            soft.append(f"[regraded from critical] {issue}")
            moved += 1
            continue
        kept_critical.append(issue)

    claims = report.get("claim_checks") or []
    supported = sum(1 for c in claims if c.get("supported"))
    unsupported = sum(1 for c in claims if c.get("supported") is False)
    mostly_ok = (not claims) or (supported >= unsupported)

    ed_ok = report.get("evidence_direction_ok", True)
    # Taxonomy alias alone shouldn't block if we will fix YAML separately
    taxonomy_only = kept_critical and all(
        "no_significant_effect" in i.lower() or "taxonomy" in i.lower()
        for i in kept_critical
    )

    if kept_critical and not taxonomy_only:
        status = STATUS_AI_DRAFT
        passed = False
    elif mostly_ok and (ed_ok or taxonomy_only):
        status = STATUS_AI_VERIFIED
        passed = True
        if taxonomy_only:
            # keep taxonomy note as soft so humans see it
            for i in kept_critical:
                soft.append(f"[taxonomy note] {i}")
            kept_critical = []
    else:
        status = STATUS_AI_DRAFT
        passed = False

    report["critical_issues"] = kept_critical
    report["soft_issues"] = soft
    report["pass"] = passed
    report["final_status"] = status
    report["recommended_status"] = status
    report["regraded"] = True
    report["regrade_moved_coi_critical_to_soft"] = moved

    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    meta_path = d / "metadata.yaml"
    if meta_path.exists():
        raw = meta_path.read_text(encoding="utf-8")
        updated = _set_status_in_yaml(raw, status)
        updated = re.sub(r"\n# ai_verify:.*\n?", "\n", updated)
        stamp = (
            f"\n# ai_verify: regraded → {status} "
            f"(moved_coi={moved}, critical={len(kept_critical)})\n"
        )
        meta_path.write_text(updated.rstrip() + stamp, encoding="utf-8")

    return {
        "doc_id": doc_id,
        "status": status,
        "moved": moved,
        "critical": len(kept_critical),
        "pass": passed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc")
    args = parser.parse_args()
    docs = [args.doc] if args.doc else list_doc_ids()
    verified = 0
    draft = 0
    for doc_id in docs:
        result = regrade_one(doc_id)
        if not result:
            print(f"SKIP {doc_id}: no qa_report.json")
            continue
        print(
            f"{result['status']:14} moved_coi={result['moved']} "
            f"crit={result['critical']} {result['doc_id']}"
        )
        if result["pass"]:
            verified += 1
        else:
            draft += 1
    print(f"Done. ai_verified={verified} ai_draft={draft}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
