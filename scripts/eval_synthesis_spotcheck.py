"""
Spot-check non-expert freeform synthesis for silent-failure risk.

Runs a small subset of contested golden queries through retrieve → synthesise
(non_researcher, freeform) and saves answers for human/agent review.

Usage (from repo root):
    python scripts/eval_synthesis_spotcheck.py

Cost: ~1 embedding + 1 GPT-4o call per case (default 4 cases).
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "app"))
load_dotenv(REPO / ".env", override=True)

from retrieval import retrieve_routed  # noqa: E402
from synthesis import synthesise  # noqa: E402

SMOKE = REPO / "eval" / "smoke_queries.json"
OUT_DIR = REPO / "eval" / "synthesis_runs"

# Contested fault-line / trap cases — highest silent-failure risk
SPOT_IDS = [
    "fault2_calibration_no",
    "fault4_returns_no",
    "trap_other_drivers_no",
    "q10_tls_no",
]


def main() -> int:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set", file=sys.stderr)
        return 2

    cases = {c["id"]: c for c in json.loads(SMOKE.read_text(encoding="utf-8"))}
    client = OpenAI(api_key=api_key)
    records = []

    for cid in SPOT_IDS:
        case = cases[cid]
        query = case["query"]
        print(f"RUNNING {cid}")
        results, routes = retrieve_routed(client, query, top_k=8)
        text = synthesise(
            client,
            query=query,
            results=results,
            mode="non_researcher",
            answer_format="freeform",
            output_language="Norwegian Bokmål",
        )
        records.append(
            {
                "id": cid,
                "query": query,
                "routes": routes,
                "retrieved": [r["doc_id"] for r in results],
                "must_include_any": case.get("must_include_any") or [],
                "mode": "non_researcher",
                "answer_format": "freeform",
                "output_language": "Norwegian Bokmål",
                "answer": text,
            }
        )
        print(f"   retrieved {len(results)} · answer chars {len(text)}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    out = OUT_DIR / f"{stamp}_nonexpert_freeform.json"
    out.write_text(
        json.dumps(
            {
                "run_utc": stamp,
                "purpose": "silent-failure spotcheck: non-expert freeform keeps disagreement",
                "n_cases": len(records),
                "results": records,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"wrote {out.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
