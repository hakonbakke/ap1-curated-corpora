"""One-shot Ask smoke for Areal A0-A6 (retrieve k=8 + non-specialist synthesis).

Run from repo root:
    python eval/areal_smoke_runs/smoke_2026-09-15.py
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "app"))
load_dotenv(REPO / ".env", override=True)

from retrieval import (  # noqa: E402
    AREAL_DATA_FILE,
    OUT_OF_SCOPE_SCORE_THRESHOLD,
    is_out_of_scope,
    retrieve,
)
from synthesis import synthesise  # noqa: E402

ADJACENT = (
    "2011_aldrin_isa-farm-spread",
    "2015_aldrin_pd-space-time",
    "2017_aldrin_lice-farm-model",
    "2024_qviller_geographic-redistribution",
    "2026_moldal_fiskehelserapporten",
    "2020_gismervik_welfare-regulatory-frameworks",
    "2022_ipbes_values-assessment",
    "2022_ipbes_spm-values",
)

VILLAKS_LEAK = re.compile(
    r"\b(smoltd[øo]delighet|utvandrende smolt|kausal kjede|"
    r"Q[1-9]|Q10|villaks-rommet|lakselus og villaks)\b",
    re.I,
)

VILLAKS_DEBATE_OPENER = re.compile(
    r"debatten om lakseoppdrett.{0,160}villfisk|"
    r"påvirkning(?:en)? på villfiskbestander",
    re.I | re.S,
)

CASES = [
    {
        "id": "A0",
        "query": (
            "Hva begrenser vekst i havbruk på norskekysten: mangel på ledig sjøflate, "
            "produksjons- og lokalitetstillatelser, kommunal utpeking av brukbar sjø, "
            "eller biologi (lus, sykdom, tetthet, velferd)?"
        ),
        "must": [
            "2020_hersoug_whats-the-clue",
            "2015_sandersen_access-to-sites",
            "2011_gullestad_arealbruk-havbruk",
            "2025_sand_havbrukets-arealbehov-trondelag",
            "2025_kulmambetova_spatial-density-productivity",
            "undated_baerekraftig-arealbruk-havbruk",
            "2025_osmundsen_fylkeskommune-akvakulturloven",
            "2005_jentoft_challenges-myths-czm",
        ],
    },
    {
        "id": "A1",
        "query": (
            "Når kommunen peker ut, eller nekter å peke ut, sjøareal til havbruk, "
            "hva avgjør dette: selve plankartet, senere dispensasjon, eller innsigelse "
            "og avslag fra sektormyndighet etter at kartet er vedtatt?"
        ),
        "must": [
            ["2017_kvalvik_intermunicipal-coastal-planning", "2017_kvalvik_ocean-coastal-management"],
            "2021_sandersen_kystsone-helgeland",
            "2019_mikkelsen_arealplanlegging-sjo",
            "salt_1065_ku-arealplanlegging",
            "2015_rettslig_rammeverk-havbruk",
            "2025_osmundsen_fylkeskommune-akvakulturloven",
            "2025_sand_havbrukets-arealbehov-trondelag",
            "2024_sordahl_when-all-you-have-is-a-hammer",
        ],
    },
    {
        "id": "A2",
        "query": (
            "Hvordan former produksjonstillatelse, lokalitetstillatelse og "
            "fylkesbehandling etter akvakulturloven hvem som får en lokalitet, "
            "og hvor i den stabelen saken dør?"
        ),
        "must": [
            "2022_hersoug_ten-licensing-systems",
            "2025_osmundsen_fylkeskommune-akvakulturloven",
            "salt_1110_lokalitetssoknader",
            "2015_rettslig_rammeverk-havbruk",
            "2020_hersoug_whats-the-clue",
            "2011_gullestad_arealbruk-havbruk",
            "2014_sandersen_administrative-reform",
            "2019_schutz_strategic-marine-planning",
        ],
    },
    {
        "id": "A3",
        "query": (
            "Når sjø går til havbruksanlegg, hva må vike (annen bruk, levende natur, "
            "eller anlegget), og hvordan tas samlet belastning inn når merden kommer "
            "i sjø som allerede brukes?"
        ),
        "must": [
            "2023_evenset_sameksistens",
            "2025_mikkelsen_samlet-pavirkning-nord",
            "2025_sand_havbrukets-arealbehov-trondelag",
            "2025_sand_arealbruk-bionaringer-trondelag",
            "2015_sandersen_access-to-sites",
            "salt_1075_arealbruk-havbruk",
            "2019_schutz_strategic-marine-planning",
            "2024_meldst35_baerekraftig-bruk-natur",
        ],
    },
    {
        "id": "A4",
        "query": (
            "Hvilken kunnskap brukes, mangler, utsettes eller brukes skjevt i plan, "
            "KU og lokalitetsbehandling av havbruk, og hvordan skal usikkerhet og "
            "føre var inn i vedtaket?"
        ),
        "must": [
            "salt_1065_ku-arealplanlegging",
            "salt_1110_lokalitetssoknader",
            "2023_evenset_sameksistens",
            "2025_mikkelsen_samlet-pavirkning-nord",
            "2023_metier_marine-grunnkart",
            "2021_sandersen_kystsone-helgeland",
            "2024_sordahl_when-all-you-have-is-a-hammer",
            "2026_sordahl_nar-alt-skal-med",
        ],
    },
    {
        "id": "A5",
        "query": (
            "Hva følger av hvor og hvor tett havbruksanleggene ligger for produktivitet, "
            "sykdom, lus og belastning, og er «mer areal» feil grep hvis avstand og "
            "biologi binder først?"
        ),
        "must": [
            "2025_kulmambetova_spatial-density-productivity",
            "2011_gullestad_arealbruk-havbruk",
            "2020_hersoug_whats-the-clue",
            "2025_sand_havbrukets-arealbehov-trondelag",
            "undated_baerekraftig-arealbruk-havbruk",
            "2026_hi_risikorapport",
            "salt_1075_arealbruk-havbruk",
        ],
    },
    {
        "id": "A6",
        "query": (
            "Hvordan påvirker skatt, fond og arealavgiftsdebatten kommunenes vilje til "
            "å huse havbruksanlegg, og kan kommunen ta pengene uten å åpne mer sjøareal?"
        ),
        "must": [
            "2015_sandersen_access-to-sites",
            "2020_hersoug_whats-the-clue",
            "2025_rosendal_municipal-environment-economy",
            "2015_rettslig_rammeverk-havbruk",
            "2025_osmundsen_fylkeskommune-akvakulturloven",
            "undated_baerekraftig-arealbruk-havbruk",
            "2019_mikkelsen_arealplanlegging-sjo",
        ],
    },
]


def group_hit(group, got: set[str]) -> bool:
    if isinstance(group, list):
        return any(g in got for g in group)
    return group in got


def group_label(group) -> str:
    if isinstance(group, list):
        return " or ".join(group)
    return group


def main() -> int:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        print("ERROR: OPENAI_API_KEY not set", file=sys.stderr)
        return 2

    n_docs = len(pd.read_parquet(AREAL_DATA_FILE))
    print(f"Areal parquet: {AREAL_DATA_FILE} ({n_docs} rows)")
    client = OpenAI(api_key=key)
    records = []
    top_k = 8

    for case in CASES:
        results = retrieve(
            client,
            case["query"],
            top_k=top_k,
            data_file=AREAL_DATA_FILE,
        )
        got = [r["doc_id"] for r in results]
        got_set = set(got)
        scores = {r["doc_id"]: r["score"] for r in results}
        best = max(scores.values()) if scores else 0.0
        oos = is_out_of_scope(results)
        hits = [group_label(g) for g in case["must"] if group_hit(g, got_set)]
        misses = [group_label(g) for g in case["must"] if not group_hit(g, got_set)]
        adjacent = [d for d in got if d in ADJACENT]
        coverage = len(hits) / len(case["must"]) if case["must"] else 1.0
        status = "FAIL" if oos or coverage == 0 else ("WARN" if coverage < 0.5 else "PASS")

        print(f"\n{status}  {case['id']}  coverage {len(hits)}/{len(case['must'])}  top1={best:.3f}  oos={oos}")
        print(f"       top-{top_k}: {got}")
        print(f"       hits: {hits or '(none)'}")
        if misses:
            print(f"       miss: {misses}")
        if adjacent:
            print(f"       adjacent in top-k: {adjacent}")

        synth = synthesise(
            client,
            case["query"],
            results,
            mode="non_researcher",
            answer_format="freeform",
            output_language="Norwegian",
            room="areal",
        )
        leak = bool(VILLAKS_LEAK.search(synth))
        opener_drift = bool(VILLAKS_DEBATE_OPENER.search(synth[:500]))
        if leak:
            print("       SYNTH LEAK: villaks-pattern in answer")
            status = "FAIL" if status == "PASS" else status
        if opener_drift:
            print("       SYNTH DRIFT: villaks-debate opener")
            status = "FAIL"
        print(f"       synth {len(synth)} chars, leak={leak}, opener_drift={opener_drift}")
        print("       --- synth excerpt ---")
        print(synth[:500].replace("\n", " "))
        print("       ---")

        records.append(
            {
                "id": case["id"],
                "query": case["query"],
                "status": status,
                "top_k": got,
                "scores": scores,
                "best_score": best,
                "out_of_scope": oos,
                "must_hits": hits,
                "must_misses": misses,
                "coverage": coverage,
                "adjacent_in_topk": adjacent,
                "synthesis": synth,
                "villaks_pattern_in_synth": leak,
                "villaks_debate_opener": opener_drift,
            }
        )

    out_dir = Path(__file__).resolve().parent
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    out = out_dir / f"{stamp}_areal_ask_smoke.json"
    payload = {
        "created_at": stamp,
        "parquet": str(AREAL_DATA_FILE),
        "n_docs": n_docs,
        "top_k": top_k,
        "oos_threshold": OUT_OF_SCOPE_SCORE_THRESHOLD,
        "mode": "non_researcher",
        "room": "areal",
        "cases": records,
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {out}")
    fails = sum(1 for r in records if r["status"] == "FAIL")
    warns = sum(1 for r in records if r["status"] == "WARN")
    print(f"FAIL {fails}  WARN {warns}  PASS {len(records) - fails - warns}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
