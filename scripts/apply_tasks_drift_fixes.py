"""
Surgical applicator for TASKS.md Task 2 (preserves YAML comments where possible).
No API. No full YAML rewrite of untouched fields.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_paths import doc_dir, list_doc_ids, strip_yaml_comments  # noqa: E402


def set_scalar(raw: str, key: str, value: str) -> str:
    pat = re.compile(rf"^({re.escape(key)}:\s*).*$", re.M)
    if pat.search(raw):
        return pat.sub(rf"\g<1>{value}", raw, count=1)
    # insert before curator_review_status if missing
    if "curator_review_status:" in raw:
        return raw.replace(
            "curator_review_status:",
            f"{key}: {value}\n\ncurator_review_status:",
            1,
        )
    return raw.rstrip() + f"\n{key}: {value}\n"


def replace_list_item(raw: str, old: str, new: str | list[str]) -> str:
    """Replace a YAML list item line '- old' with one or more '- new' lines."""
    esc = re.escape(old)
    pat = re.compile(rf"^(\s*)-\s*[\"']?{esc}[\"']?\s*$", re.M)
    m = pat.search(raw)
    if not m:
        # try without anchor (inline)
        return raw
    indent = m.group(1)
    news = new if isinstance(new, list) else [new]
    block = "\n".join(f"{indent}- \"{n}\"" if " " in n or "/" in n else f"{indent}- {n}" for n in news)
    return pat.sub(block, raw, count=1)


def append_retrieval_tag(raw: str, tag: str) -> str:
    if f"- \"{tag}\"" in raw or f"- {tag}" in raw:
        return raw
    # Find retrieval_tags block
    m = re.search(r"^retrieval_tags:\s*\n((?:[ \t]*-.*\n)*)", raw, re.M)
    line = f'  - "{tag}"\n' if any(c in tag for c in " ,()/") else f"  - {tag}\n"
    if not m:
        # insert before curator_note or curator_review_status
        anchor = "curator_note:" if "curator_note:" in raw else "curator_review_status:"
        return raw.replace(anchor, f"retrieval_tags:\n{line}\n{anchor}", 1)
    block = m.group(0)
    # skip empty placeholder
    if re.search(r'-\s*""\s*$', block, re.M) and block.count("-") == 1:
        new_block = f"retrieval_tags:\n{line}"
        return raw[: m.start()] + new_block + raw[m.end() :]
    return raw[: m.end()] + line + raw[m.end() :]


def ensure_key_list(raw: str, key: str, values: list[str]) -> str:
    if re.search(rf"^{re.escape(key)}:", raw, re.M):
        return raw
    lines = "\n".join(
        f'  - "{v}"' if any(c in v for c in " ,()") else f"  - {v}" for v in values
    )
    block = f"{key}:\n{lines}\n\n"
    if "primary_endpoint:" in raw:
        return raw.replace("primary_endpoint:", block + "primary_endpoint:", 1)
    return raw.rstrip() + "\n" + block


def ensure_key_scalar(raw: str, key: str, value: str) -> str:
    if re.search(rf"^{re.escape(key)}:", raw, re.M):
        return raw
    return set_scalar(raw, key, value)


def main() -> int:
    # 2a quality
    for doc, val in {
        "2015_aei_helland-monitoring-lice-challenges": "medium",
        "2018_epidemics_kristoffersen-risk-assessment": "medium",
        "2022_fishes_lamberg-pre-fishery-abundance": "medium",
        "2025_dao_jones-broughton-lice-unchanged": "medium",
        "2025_jfd_jones-pacific-lice-cessation-bc": "medium",
    }.items():
        p = doc_dir(doc) / "metadata.yaml"
        p.write_text(set_scalar(p.read_text(encoding="utf-8"), "quality_signal", val), encoding="utf-8")
        print(f"2a {doc}")

    # 2b consensus
    for doc, val in {
        "1998_cjfas_mccormick-smolting-migration": "high_agreement",
        "2016_jfb_jonsson-environmental-change-salmon": "high_agreement",
        "2022_fishes_lamberg-pre-fishery-abundance": "insufficient_evidence",
    }.items():
        p = doc_dir(doc) / "metadata.yaml"
        p.write_text(set_scalar(p.read_text(encoding="utf-8"), "consensus_signal", val), encoding="utf-8")
        print(f"2b {doc}")

    # 2c controversy
    for doc, val in {
        "1998_cjfas_mccormick-smolting-migration": "foundational",
        "2015_aei_helland-monitoring-lice-challenges": "critical",
        "2016_jfb_jonsson-environmental-change-salmon": "peripheral",
        "2018_epidemics_kristoffersen-risk-assessment": "foundational",
        "2022_fishes_lamberg-pre-fishery-abundance": "peripheral",
        "2024_ecosphere_hawley-anadromy-lice-mortality-trout": "supportive",
        "2024_ijpara_stige-regional-lice-coordination": "supportive",
        "2025_dao_jones-broughton-lice-unchanged": "critical",
        "2025_jfd_jones-pacific-lice-cessation-bc": "critical",
    }.items():
        p = doc_dir(doc) / "metadata.yaml"
        p.write_text(set_scalar(p.read_text(encoding="utf-8"), "controversy_role", val), encoding="utf-8")
        print(f"2c {doc}")

    # 2d life_stage hyphenation + known prose
    life_repl = [
        ("post-smolt", "post_smolt"),
        ("postsmolt", "post_smolt"),
        ("adult (returning spawners)", "returning_adult"),
        ("smolt (smolt age used for standardization)", "smolt"),
        ("sea trout (resident fjord phase)", "adult"),
        ("veteran migrant (repeat sea-sojourner)", "adult"),
    ]
    for doc in list_doc_ids():
        p = doc_dir(doc) / "metadata.yaml"
        raw = p.read_text(encoding="utf-8")
        orig = raw
        for old, new in life_repl:
            if old in raw:
                raw = replace_list_item(raw, old, new)
                if old != new and ("(" in old or " " in old):
                    raw = append_retrieval_tag(raw, old)
        if raw != orig:
            p.write_text(raw, encoding="utf-8")
            print(f"2d {doc}")

    # 2f causal_chain_stage
    stage_repl = [
        ("infestation_pressure", ["infestation"]),
        ("smolt exposure to lice", ["host_exposure"]),
        (
            "smolt exposure to lice (migration timing, behavior, physiology)",
            ["host_exposure"],
        ),
        ("fraction dying from lice", ["individual_mortality"]),
        (
            "translating infestation to mortality",
            ["individual_mortality", "model_calibration"],
        ),
        ("population-level impact", ["population_impacts"]),
        ("population-level impact of lice-induced mortality", ["population_impacts"]),
        ("management_intervention", ["regulatory_assessment"]),
        (
            "monitoring and validation of management effectiveness",
            ["monitoring_methods", "model_validation"],
        ),
    ]
    for doc in list_doc_ids():
        p = doc_dir(doc) / "metadata.yaml"
        raw = p.read_text(encoding="utf-8")
        orig = raw
        for old, new in stage_repl:
            if old in raw:
                raw = replace_list_item(raw, old, new)
                raw = append_retrieval_tag(raw, old)
        if raw != orig:
            p.write_text(raw, encoding="utf-8")
            print(f"2f {doc}")

    # 2e geography + regulatory — parse and rewrite those list blocks carefully via yaml load of those keys only
    geo_map = {
        "Norway (nationwide, 13 production zones, 401 rivers)": ["Norway"],
        "Norway (8 river regions from 58.6N to 69.0N)": ["Norway"],
        "Norwegian coast (15 fjords)": ["Norway"],
        "Hardangerfjord, Norway": ["Hardangerfjord"],
        "Hardanger area (Region 3)": ["Hardangerfjord"],
        "Sognefjorden, Norway": ["Sognefjorden"],
        "Nordfjord area (Region 6)": ["Nordfjord"],
        "Nordfjord": ["Nordfjord"],
        "Broughton Archipelago, British Columbia, Canada": ["Broughton_Archipelago"],
        "Discovery Islands, British Columbia, Canada": ["Discovery_Islands"],
        "North Atlantic Ocean": ["North_Atlantic"],
        "North Atlantic": ["North_Atlantic"],
        "Production_area_4": ["Norway_PO4"],
        "River Imsa, Norway (Boknafjorden, south-western Norway)": ["Norway"],
        "River Etne, Hordaland": ["Norway", "Hardangerfjord"],
        "Bjerkreimselva (Region 1)": ["Norway"],
        "Frafjord area (Region 2)": ["Norway"],
        "Sunnfjord (Region 4)": ["Norway"],
        "Orkla/Trondheimsfjord (Region 5)": ["Norway"],
        "Salten (Region 7)": ["Norway"],
        "Malselva/Troms (Region 8)": ["Norway"],
        "Eastern Norwegian Sea": ["Eastern_Norwegian_Sea"],
        "review_mixed (North America and Europe)": ["not_applicable"],
        "National Salmon Fjord": ["Norway"],
        "Oppedal": ["Norway", "Austevoll"],
        "Austevoll": ["Austevoll"],
        "Rogaland": ["Rogaland"],
        "Romsdalsfjord": ["Romsdalsfjord"],
        "Clayoquot_Sound": ["Clayoquot_Sound"],
        "Fife Sound": ["Fife_Sound"],
        "Knight Inlet": ["Knight_Inlet"],
        "Tribune Channel": ["Tribune_Channel"],
        "Canada": ["Canada"],
        "Greenland": ["Greenland"],
        "Scotland": ["Scotland"],
        "Ireland": ["Ireland"],
        "Norway": ["Norway"],
        "Hardangerfjord": ["Hardangerfjord"],
        "British_Columbia": ["British_Columbia"],
        "Discovery_Islands": ["Discovery_Islands"],
        "Broughton_Archipelago": ["Broughton_Archipelago"],
        "Norway_PO3": ["Norway_PO3"],
        "Norway_PO5": ["Norway_PO5"],
        "Sognefjorden": ["Sognefjorden"],
    }
    reg_map = {
        "Norwegian Traffic Light System (TLS)": ["Norway_TLS"],
        "Norwegian Traffic Light System": ["Norway_TLS"],
        "Norwegian national salmon lice monitoring programme": ["none"],
        "Norwegian Scientific Committee for Salmon Management (VRL)": ["Norway_expert_group"],
        "Norwegian National Salmon Fjord designation": ["none"],
        "Spawning target (ST) management model": ["none"],
        "Norway_TLS": ["Norway_TLS"],
        "Norway_expert_group": ["Norway_expert_group"],
        "Canada_management": ["Canada_management"],
        "none": ["none"],
    }

    for doc in list_doc_ids():
        p = doc_dir(doc) / "metadata.yaml"
        raw = p.read_text(encoding="utf-8")
        meta = yaml.safe_load(strip_yaml_comments(raw)) or {}
        prose_tags: list[str] = []

        geos = [str(x) for x in (meta.get("geography") or []) if x]
        new_geo: list[str] = []
        for g in geos:
            if g in geo_map:
                for m in geo_map[g]:
                    if m not in new_geo:
                        new_geo.append(m)
                if geo_map[g] != [g]:
                    prose_tags.append(g)
            else:
                print(f"ASK geography unmapped: {doc} :: {g}")
                if g not in new_geo:
                    new_geo.append(g)

        regs = [str(x) for x in (meta.get("regulatory_context") or []) if x]
        new_reg: list[str] = []
        for r in regs:
            if r in reg_map:
                for m in reg_map[r]:
                    if m not in new_reg:
                        new_reg.append(m)
                if reg_map[r] != [r]:
                    prose_tags.append(r)
            else:
                print(f"ASK regulatory unmapped: {doc} :: {r}")
                if r not in new_reg:
                    new_reg.append(r)

        # model_type cleanup
        mt = meta.get("model_type")
        new_mt = None
        if mt is None:
            defaults = {
                "1998_cjfas_mccormick-smolting-migration": ["none"],
                "2016_jfb_jonsson-environmental-change-salmon": ["none"],
                "2022_fishes_lamberg-pre-fishery-abundance": ["statistical_regression_model"],
                "2024_ecosphere_hawley-anadromy-lice-mortality-trout": ["population_model"],
                "2025_dao_jones-broughton-lice-unchanged": ["none"],
                "2025_jfd_jones-pacific-lice-cessation-bc": ["none"],
            }
            if doc in defaults:
                new_mt = defaults[doc]
                print(f"2g fill {doc} -> {new_mt}")
        else:
            items = mt if isinstance(mt, list) else [mt]
            norm = {
                "generalized linear mixed model": "statistical_regression_model",
                "zero-inflated count model": "statistical_regression_model",
                "binomial logistic regression": "statistical_regression_model",
                "generalized_linear_mixed_model": "statistical_regression_model",
                "cox_proportional_hazards": "statistical_regression_model",
                "stage_structured_lice_model": "infestation_model",
                "scenario_simulation": "population_model",
            }
            if doc == "2018_epidemics_kristoffersen-risk-assessment" and any(
                len(str(x)) > 80 for x in items
            ):
                new_mt = [
                    "risk_assessment_model",
                    "infestation_model",
                    "statistical_regression_model",
                ]
                prose_tags.append(str(items[0])[:180])
            else:
                built = []
                for x in items:
                    s = str(x)
                    if s in norm:
                        if norm[s] not in built:
                            built.append(norm[s])
                        prose_tags.append(s)
                    else:
                        if s not in built:
                            built.append(s)
                if built != items:
                    new_mt = built

        # Rewrite list sections by regex block replace
        def rewrite_list_block(text: str, key: str, values: list[str]) -> str:
            lines = "\n".join(
                f'  - "{v}"' if re.search(r"[ ,()/]", v) else f"  - {v}" for v in values
            )
            pat = re.compile(
                rf"^{re.escape(key)}:\s*\n(?:[ \t]*-.*\n)*",
                re.M,
            )
            if pat.search(text):
                return pat.sub(f"{key}:\n{lines}\n", text, count=1)
            return text

        orig = raw
        if new_geo != geos:
            raw = rewrite_list_block(raw, "geography", new_geo)
        if new_reg != regs:
            raw = rewrite_list_block(raw, "regulatory_context", new_reg)
        if new_mt is not None:
            raw = rewrite_list_block(raw, "model_type", new_mt)
            if "model_type:" not in orig:
                # insert after data_source block
                raw = ensure_key_list(raw, "model_type", new_mt)

        for t in prose_tags:
            raw = append_retrieval_tag(raw, t)

        # 2h Jansen missing keys
        if doc == "2025_jae_jansen-lice-effects-returns":
            if "comparison_type:" not in raw:
                raw = ensure_key_list(
                    raw,
                    "comparison_type",
                    ["observed_vs_modelled", "among_regions", "among_years"],
                )
            if "outcome_domain:" not in raw:
                raw = ensure_key_list(
                    raw,
                    "outcome_domain",
                    [
                        "adult_returns",
                        "mortality",
                        "population_abundance",
                        "model_performance",
                    ],
                )
            if re.search(r"^primary_endpoint:\s*$", raw, re.M) or "primary_endpoint:" not in raw:
                raw = set_scalar(
                    raw,
                    "primary_endpoint",
                    '"Association between TLS/PIM estimates and observed adult salmon returns"',
                )
            if re.search(r"^secondary_endpoints:\s*\n\s*-\s*\"\"\s*$", raw, re.M) or (
                "secondary_endpoints:" in raw
                and re.search(r"secondary_endpoints:\s*\n\s*-\s*\"\"\s*\n", raw)
            ):
                raw = rewrite_list_block(
                    raw,
                    "secondary_endpoints",
                    [
                        "Effect by sea-age class (1SW, 2SW, 3SW)",
                        "Predicted reduction in total returns at given PIM levels",
                    ],
                )
            elif "secondary_endpoints:" not in raw:
                raw = ensure_key_list(
                    raw,
                    "secondary_endpoints",
                    [
                        "Effect by sea-age class (1SW, 2SW, 3SW)",
                        "Predicted reduction in total returns at given PIM levels",
                    ],
                )

        # Ensure Task-4 keys exist (empty)
        for key in ("inclusion_decided_by", "added_by", "added_date"):
            if not re.search(rf"^{key}:", raw, re.M):
                raw = raw.rstrip() + f"\n{key}: \"\"\n"

        if raw != orig:
            p.write_text(raw, encoding="utf-8")
            print(f"2e/g/h {doc}")

    print(
        "NOTE (Task 2g hard stop): Lamberg→statistical_regression_model; "
        "Hawley→population_model. Confirm with Thord."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
