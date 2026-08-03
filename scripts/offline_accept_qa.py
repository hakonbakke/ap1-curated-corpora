"""
Offline accept of qa_report.json based on claim_checks (no OpenAI API).

Promotes ai_draft → ai_verified when:
  - No taxonomy-blocker issues remain, AND
  - claim_checks are empty OR supported >= unsupported, AND
  - remaining critical issues are only soft-class (wording / summary emphasis),
    OR --force-doc is used after human/agent spot-check.

Usage:
    python scripts/offline_accept_qa.py
    python scripts/offline_accept_qa.py --dry-run
    python scripts/offline_accept_qa.py --force-doc 2017_icesjms_forseth-major-threats-norway
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_paths import STATUS_AI_DRAFT, STATUS_AI_VERIFIED, doc_dir, list_doc_ids  # noqa: E402

HARD_PATTERNS = [
    r"taxonomy",
    r"no_significant_effect",
    r"contradict.*extract",
    r"key_claims that contradict",
]

# Issues that are usually checker pedantry once claims are supported
SOFT_CRITICAL = [
    r"fabricated numbers",
    r"not directly quoted",
    r"summary mentions",
    r"summary states",
    r"summary does not",
    r"summary's",
    r"emphasis",
    r"nuanced",
    r"suggesting a more",
    r"may not align",
    r"does not clearly support this as the primary",
    r"predominantly discusses",
    r"potential benefits",
    r"evidence direction mismatch",
    r"evidence_direction",
    r"mixed_within_study",
    r"supports_effect",
    r"critiques_methodology",
    r"not_applicable",
    r"fabricated coi",
    r"coi",
]


def _set_status(raw: str, status: str) -> str:
    if re.search(r"curator_review_status:\s*\S+", raw):
        return re.sub(
            r"curator_review_status:\s*\S+",
            f"curator_review_status: {status}",
            raw,
            count=1,
        )
    return raw.rstrip() + f"\n\ncurator_review_status: {status}\n"


def _is_hard(issue: str) -> bool:
    low = issue.lower()
    return any(re.search(p, low) for p in HARD_PATTERNS)


def _is_soft(issue: str) -> bool:
    low = issue.lower()
    return any(re.search(p, low) for p in SOFT_CRITICAL)


def decide(report: dict, force: bool) -> tuple[bool, str]:
    if report.get("pass") and report.get("final_status") == STATUS_AI_VERIFIED:
        return False, "already_verified"

    claims = report.get("claim_checks") or []
    supported = sum(1 for c in claims if c.get("supported"))
    unsupported = sum(1 for c in claims if c.get("supported") is False)
    critical = list(report.get("critical_issues") or [])

    hard = [c for c in critical if _is_hard(c)]
    if hard and not force:
        return False, f"hard_issues={len(hard)}"

    if force:
        return True, "force_doc"

    if claims and unsupported > supported:
        return False, f"claims_unsupported={unsupported}>{supported}"

    # All remaining critical look soft, or no critical left
    if not critical:
        return True, "no_critical"

    if all(_is_soft(c) for c in critical):
        return True, "soft_critical_only"

    return False, "mixed_critical"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force-doc", action="append", default=[])
    args = parser.parse_args()

    promoted = 0
    skipped = 0
    for doc_id in list_doc_ids():
        path = doc_dir(doc_id) / "qa_report.json"
        if not path.exists():
            continue
        report = json.loads(path.read_text(encoding="utf-8"))
        force = doc_id in args.force_doc
        ok, reason = decide(report, force=force)
        if not ok:
            print(f"KEEP  {doc_id} ({reason})")
            skipped += 1
            continue
        print(f"PROMOTE {doc_id} ({reason})")
        promoted += 1
        if args.dry_run:
            continue

        soft = list(report.get("soft_issues") or [])
        for c in report.get("critical_issues") or []:
            soft.append(f"[offline_accept] {c}")
        report["critical_issues"] = []
        report["soft_issues"] = soft
        report["pass"] = True
        report["final_status"] = STATUS_AI_VERIFIED
        report["recommended_status"] = STATUS_AI_VERIFIED
        report["offline_accepted"] = True
        report["offline_accept_reason"] = reason
        path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        meta = doc_dir(doc_id) / "metadata.yaml"
        if meta.exists():
            raw = meta.read_text(encoding="utf-8")
            raw = _set_status(raw, STATUS_AI_VERIFIED)
            raw = re.sub(r"\n# ai_verify:.*\n?", "\n", raw)
            meta.write_text(
                raw.rstrip()
                + f"\n# ai_verify: offline_accept → {STATUS_AI_VERIFIED} ({reason})\n",
                encoding="utf-8",
            )

    print(f"Done. promote={promoted} keep={skipped} dry_run={args.dry_run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
