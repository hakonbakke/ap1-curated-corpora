"""
Eval question→priority routing WITHOUT OpenAI API calls.

Usage (from repo root):
    python scripts/eval_routing.py

Checks infer_priority_questions() against eval/smoke_queries.json expect_route.
Retrieval recall (must_include_any) requires the live app / embeddings API —
run that separately when testing the deployed RAG.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "app"))

from retrieval import infer_priority_questions  # noqa: E402

SMOKE = REPO / "eval" / "smoke_queries.json"


def main() -> int:
    cases = json.loads(SMOKE.read_text(encoding="utf-8"))
    failed = 0
    for case in cases:
        got = infer_priority_questions(case["query"])
        expect = case.get("expect_route") or []
        # Pass if every expected Q is present (extra routes OK)
        missing = [q for q in expect if q not in got]
        ok = not missing
        status = "PASS" if ok else "FAIL"
        if not ok:
            failed += 1
        print(f"{status}  {case['id']}")
        print(f"       query: {case['query'][:80]}")
        print(f"       expect subset of got: {expect}")
        print(f"       got: {got}")
        if missing:
            print(f"       missing: {missing}")
    print()
    print(f"routing: {len(cases) - failed}/{len(cases)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
