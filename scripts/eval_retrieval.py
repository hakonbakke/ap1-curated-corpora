"""
Eval retrieval recall for smoke queries (REQUIRES OpenAI embeddings API).

Usage (from repo root):
    python scripts/eval_retrieval.py
    python scripts/eval_retrieval.py --top-k 8

Checks that at least one doc_id from each case's must_include_any appears in
the top-k from retrieve_routed(). Routing-only checks stay in eval_routing.py
(API-free).

Cost: one embedding call per smoke query (~5 calls with the default file).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "app"))

from retrieval import retrieve_routed  # noqa: E402

load_dotenv()
SMOKE = REPO / "eval" / "smoke_queries.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Eval retrieve_routed recall on smoke queries")
    parser.add_argument("--top-k", type=int, default=8)
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

    total = len(cases)
    print()
    print(f"retrieval recall: {total - failed}/{total} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
