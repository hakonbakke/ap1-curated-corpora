"""
Eval retrieval recall for smoke queries (REQUIRES OpenAI embeddings API).

Usage (from repo root):
    python scripts/eval_retrieval.py
    python scripts/eval_retrieval.py --top-k 8

Checks that at least one doc_id from each case's must_include_any appears in
the top-k from retrieve_routed(). Routing-only checks stay in eval_routing.py
(API-free).

Every run writes a timestamped JSON result to eval/recall_runs/ so a reported
recall figure always has an artifact behind it. A recall claim with no saved run
is not evidence — this gates the hybrid-BM25 decision, so it needs to be
checkable.

Cost: one embedding call per smoke query (~5 calls with the default file).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "app"))

from retrieval import retrieve_routed  # noqa: E402

load_dotenv(REPO / ".env", override=True)
SMOKE = REPO / "eval" / "smoke_queries.json"
RUNS_DIR = REPO / "eval" / "recall_runs"


def main() -> int:
    parser = argparse.ArgumentParser(description="Eval retrieve_routed recall on smoke queries")
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Skip writing the run artifact (not recommended; the artifact is the evidence)",
    )
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        print(
            "ERROR: OPENAI_API_KEY not set. This script embeds each query "
            "(~5 small embedding calls). Use eval_routing.py for the API-free check.",
            file=sys.stderr,
        )
        return 2

    cases = json.loads(SMOKE.read_text(encoding="utf-8"))
    client = OpenAI(api_key=api_key)
    failed = 0
    case_records = []

    for case in cases:
        must = case.get("must_include_any") or []
        results, routes = retrieve_routed(client, case["query"], top_k=args.top_k)
        got_ids = [r["doc_id"] for r in results]
        hit = [d for d in must if d in got_ids]
        ok = bool(hit) if must else True
        status = "PASS" if ok else "FAIL"
        if not ok:
            failed += 1
        print(f"{status}  {case['id']}")
        print(f"       query: {case['query'][:80]}")
        print(f"       routes: {routes}")
        print(f"       top-{args.top_k}: {got_ids}")
        print(f"       must_include_any hits: {hit or '(none)'}")

        case_records.append(
            {
                "id": case["id"],
                "query": case["query"],
                "routes": routes,
                "retrieved": got_ids,
                "must_include_any": must,
                "hits": hit,
                "passed": ok,
                # No must_include_any means nothing was asserted, so a PASS here
                # is vacuous. Recorded so the summary cannot be read as stronger
                # evidence than it is.
                "asserted": bool(must),
            }
        )

    total = len(cases)
    asserted = sum(1 for r in case_records if r["asserted"])
    print()
    print(f"retrieval recall: {total - failed}/{total} passed ({asserted}/{total} assert recall)")

    if not args.no_save:
        RUNS_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
        out = RUNS_DIR / f"{stamp}_recall.json"
        out.write_text(
            json.dumps(
                {
                    "run_utc": stamp,
                    "top_k": args.top_k,
                    "cases_total": total,
                    "cases_asserting_recall": asserted,
                    "passed": total - failed,
                    "failed": failed,
                    "results": case_records,
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        print(f"wrote {out.relative_to(REPO)}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
