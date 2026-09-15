"""
AI-verify metadata/summary against extracted.md (maker-checker).

Writes documents/<doc_id>/qa_report.json and updates curator_review_status:
  - ai_verified  if checker passes (no critical failures)
  - ai_draft     if critical issues remain

Usage:
    python scripts/ai_verify_document.py --doc 2025_jae_jansen-lice-effects-returns
    python scripts/ai_verify_document.py --all
    python scripts/ai_verify_document.py --corpus area-and-aquaculture --all

Does NOT invent new claims — only audits existing curation against the extract.

Default corpus is villaks. Pass --corpus area-and-aquaculture for the Areal room.
The API path still caps extract length (AP1_VERIFY_EXTRACT_CHARS). Large Areal
reports need a Cursor page walk, not this truncated API check.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml
from dotenv import load_dotenv
from openai import OpenAI
from openai import RateLimitError

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_paths import (  # noqa: E402
    DEFAULT_SLUG,
    STATUS_AI_DRAFT,
    STATUS_AI_VERIFIED,
    CorpusPaths,
    get_corpus,
    strip_yaml_comments,
)

load_dotenv()

VERIFY_MODEL = os.getenv("AP1_VERIFY_MODEL", "gpt-4o")
# Keep well under org TPM limits (e.g. 30k TPM on gpt-4o): ~8–10k tokens extract.
EXTRACT_CHAR_CAP = int(os.getenv("AP1_VERIFY_EXTRACT_CHARS", "32000"))
REQUEST_PAUSE_S = float(os.getenv("AP1_VERIFY_PAUSE_S", "2.5"))

EVIDENCE_DIRECTIONS = {
    "supports_effect",
    "weak_support",
    "mixed_within_study",
    "no_effect_detected",
    "contradicts_effect",
    "critiques_methodology",
    "not_applicable",
}

SYSTEM = """\
You are a strict verification checker for a scientific evidence corpus (Honest Broker).

Given an extracted paper text and AI-produced summary + metadata, audit faithfulness.

Rules:
1. Never invent support. If a claim is not clearly grounded in the extract, mark unsupported.
2. Prefer quotes from the extract (short) when supported=true.
3. Critical failures ONLY:
   - fabricated numbers / key_claims that contradict the extract
   - clearly wrong evidence_direction relative to the paper's own conclusions
   - taxonomy errors (e.g. no_significant_effect instead of no_effect_detected)
4. COI / funding is SOFT unless metadata invents a false industry conflict:
   - coi_declared = whether a competing-interest / COI statement exists (yes|no|unclear)
   - Funding acknowledgements alone are NOT a critical failure
   - Put funding/COI mismatches in soft_issues, not critical_issues
5. Soft issues: Del D judgement fields, minor summary omissions, COI/funding nuance
6. If key_claims are mostly supported and evidence_direction is defensible → recommended_status=ai_verified
   even when soft_issues exist.
7. Output JSON only.
"""

USER_TEMPLATE = """\
## doc_id
{doc_id}

## metadata.yaml
```yaml
{metadata}
```

## summary.md (excerpt)
{summary}

## extracted.md
<<<EXTRACT
{extract}
EXTRACT>>>

## Return JSON
{{
  "pass": true/false,
  "critical_issues": ["..."],
  "soft_issues": ["..."],
  "claim_checks": [
    {{"claim": "...", "supported": true/false, "extract_quote": "..." or null, "note": "..."}}
  ],
  "evidence_direction_ok": true/false,
  "evidence_direction_note": "...",
  "priority_questions_ok": true/false,
  "priority_questions_note": "...",
  "coi_ok": true/false,
  "coi_note": "...",
  "recommended_status": "ai_verified" or "ai_draft",
  "summary_faithfulness": "high|medium|low"
}}

Set pass=false and recommended_status=ai_draft if any critical_issues.
Set pass=true and recommended_status=ai_verified only if key_claims are mostly supported
and evidence_direction is defensible from the extract.
"""


def _load(path: Path, cap: int | None = None) -> str:
    text = path.read_text(encoding="utf-8")
    if cap and len(text) > cap:
        # Head (abstract/methods) + tail (discussion/COI) beats a pure prefix cut
        head = int(cap * 0.65)
        tail = cap - head
        return (
            text[:head]
            + f"\n\n[... TRUNCATED middle; kept head {head} + tail {tail} chars ...]\n\n"
            + text[-tail:]
        )
    return text


def _chat_with_retry(client: OpenAI, **kwargs) -> object:
    """Retry on TPM/rate limits; reduce extract pressure via pauses."""
    delays = [5, 15, 35, 60]
    last_err: Exception | None = None
    for i, delay in enumerate([0] + delays):
        if delay:
            print(f"  rate-limit pause {delay}s (attempt {i + 1})...")
            time.sleep(delay)
        try:
            return client.chat.completions.create(**kwargs)
        except RateLimitError as e:
            last_err = e
            msg = str(e)
            if "Request too large" in msg or "tokens per min" in msg:
                # Hard size issue — caller should use smaller cap; still retry once after pause
                continue
            continue
    assert last_err is not None
    raise last_err


def _parse_meta(raw: str) -> dict:
    clean = strip_yaml_comments(raw)
    return yaml.safe_load(clean) or {}


def _rule_precheck(meta: dict) -> list[str]:
    issues: list[str] = []
    ed = str(meta.get("evidence_direction") or "")
    if ed == "no_significant_effect":
        issues.append(
            "TAXONOMY: evidence_direction is no_significant_effect; use no_effect_detected"
        )
    elif ed and ed not in EVIDENCE_DIRECTIONS:
        issues.append(f"TAXONOMY: unknown evidence_direction '{ed}'")
    pq = meta.get("priority_questions") or []
    if not pq:
        issues.append("MISSING: priority_questions empty")
    claims = [c for c in (meta.get("key_claims") or []) if c and str(c).strip()]
    if len(claims) < 1:
        issues.append("MISSING: key_claims empty")
    if not (meta.get("rag_summary") or "").strip():
        issues.append("MISSING: rag_summary empty")
    return issues


def _extract_json(content: str) -> dict:
    content = (content or "").strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)
    return json.loads(content)


def _set_status_in_yaml(raw: str, status: str) -> str:
    if re.search(r"curator_review_status:\s*\S+", raw):
        return re.sub(
            r"curator_review_status:\s*\S+",
            f"curator_review_status: {status}",
            raw,
            count=1,
        )
    return raw.rstrip() + f"\n\ncurator_review_status: {status}\n"


def verify_document(
    client: OpenAI,
    doc_id: str,
    write_status: bool = True,
    paths: CorpusPaths | None = None,
) -> dict:
    if paths is None:
        paths = get_corpus()
    d = paths.doc_dir(doc_id)
    extract_path = d / "extracted.md"
    meta_path = d / "metadata.yaml"
    summary_path = d / "summary.md"

    for p in (extract_path, meta_path, summary_path):
        if not p.exists():
            raise FileNotFoundError(f"Missing {p}")

    meta_raw = _load(meta_path)
    meta = _parse_meta(meta_raw)
    summary = _load(summary_path)[:8000]
    extract = _load(extract_path, EXTRACT_CHAR_CAP)

    pre = _rule_precheck(meta)

    print(f"Verifying {doc_id} with {VERIFY_MODEL}...")
    # Cap metadata too — long YAML + extract blows low TPM tiers
    resp = _chat_with_retry(
        client,
        model=VERIFY_MODEL,
        temperature=0.0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": USER_TEMPLATE.format(
                    doc_id=doc_id,
                    metadata=meta_raw[:12000],
                    summary=summary[:5000],
                    extract=extract,
                ),
            },
        ],
    )
    report = _extract_json(resp.choices[0].message.content)
    report["doc_id"] = doc_id
    report["verified_at"] = datetime.now(timezone.utc).isoformat()
    report["verify_model"] = VERIFY_MODEL
    report["rule_precheck_issues"] = pre

    critical = list(report.get("critical_issues") or [])
    soft = list(report.get("soft_issues") or [])
    # Funding/COI mismatches are soft under clarified trust rules
    kept: list[str] = []
    for issue in critical:
        low = issue.lower()
        if any(k in low for k in ("coi", "funding", "conflict of interest", "competing interest")):
            if "fabricat" not in low and "taxonomy" not in low:
                soft.append(issue)
                continue
        kept.append(issue)
    kept.extend(pre)
    report["critical_issues"] = kept
    report["soft_issues"] = soft

    if kept:
        status = STATUS_AI_DRAFT
        report["pass"] = False
    else:
        status = STATUS_AI_VERIFIED
        report["pass"] = True
        report["recommended_status"] = STATUS_AI_VERIFIED
    report["final_status"] = status

    report_path = d / "qa_report.json"
    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"  wrote {report_path}")
    print(f"  pass={report['pass']} status={status} critical={len(critical)}")

    if write_status:
        updated = _set_status_in_yaml(meta_raw, status)
        note = (
            f"AI verify {report['verified_at'][:10]}: "
            f"{'PASS' if report['pass'] else 'FAIL'} "
            f"({len(critical)} critical, {len(report.get('soft_issues') or [])} soft). "
            f"See qa_report.json."
        )
        if re.search(r"curator_note:\s*>", updated):
            # leave existing block; append a short line after status if needed
            pass
        meta_path.write_text(updated if updated.endswith("\n") else updated + "\n", encoding="utf-8")
        # Append verification stamp as YAML comment at end for audit trail
        stamp = f"\n# ai_verify: {note}\n"
        text = meta_path.read_text(encoding="utf-8")
        text = re.sub(r"\n# ai_verify:.*\n?", "\n", text)
        meta_path.write_text(text.rstrip() + stamp, encoding="utf-8")

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="AI-verify curation against extract")
    parser.add_argument("--doc", help="Single document id")
    parser.add_argument("--all", action="store_true", help="Verify all documents with extract+meta+summary")
    parser.add_argument(
        "--missing-only",
        action="store_true",
        help="With --all: skip docs that already have qa_report.json",
    )
    parser.add_argument("--no-write-status", action="store_true")
    parser.add_argument(
        "--corpus",
        default=DEFAULT_SLUG,
        help="Corpus slug (default: villaks). Use area-and-aquaculture for Areal.",
    )
    args = parser.parse_args()

    if not args.doc and not args.all:
        print("ERROR: pass --doc or --all", file=sys.stderr)
        return 1
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not set", file=sys.stderr)
        return 1

    paths = get_corpus(args.corpus)
    client = OpenAI()
    docs = [args.doc] if args.doc else paths.list_doc_ids()
    failed = 0
    ok = 0
    for i, doc_id in enumerate(docs):
        d = paths.doc_dir(doc_id)
        if not (d / "extracted.md").exists() or not (d / "metadata.yaml").exists():
            if args.all:
                print(f"SKIP {doc_id}: missing extract or metadata")
                continue
        if args.all and args.missing_only and (d / "qa_report.json").exists():
            print(f"SKIP {doc_id}: qa_report.json exists")
            continue
        try:
            report = verify_document(
                client,
                doc_id,
                write_status=not args.no_write_status,
                paths=paths,
            )
            if not report.get("pass"):
                failed += 1
            else:
                ok += 1
        except Exception as e:
            print(f"ERROR {doc_id}: {e}", file=sys.stderr)
            failed += 1
        if args.all and i < len(docs) - 1 and REQUEST_PAUSE_S > 0:
            time.sleep(REQUEST_PAUSE_S)

    print(f"Done. ai_verified_ok={ok} failures_or_draft={failed}")
    return 1 if failed and args.doc else 0


if __name__ == "__main__":
    raise SystemExit(main())
