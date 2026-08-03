"""Map remaining free-text controlled-field values to vocabulary.json tokens."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_paths import doc_dir, list_doc_ids, strip_yaml_comments  # noqa: E402

HOST = {
    "Salmo salar": "atlantic_salmon",
    "Salmo salar (Atlantic salmon)": "atlantic_salmon",
    "Salmo trutta": "sea_trout",
    "Salmo trutta (anadromous brown trout / sea trout)": "sea_trout",
    "Salmo trutta (brown trout / sea trout)": "sea_trout",
    "Salvelinus alpinus": "arctic_char",
    "sockeye_salmon": "pacific_salmon",
    "pacific_herring": "not_species_specific",
    "threespine_stickleback": "not_species_specific",
}
PARASITE = {
    "Lepeophtheirus salmonis": "lepeophtheirus_salmonis",
    "Caligus clemensi": "caligus_clemensi",
    "Caligus elongatus": "caligus_elongatus",
}
ENV = {
    "river": "freshwater",
    "coastal marine": "coastal",
    "coastal_marine": "coastal",
    "coastal fjord": "fjord",
    "fjord (marine and brackish)": "fjord",
    "inner fjord (protected from aquaculture)": "fjord",
    "outer fjord (near aquaculture facilities)": "fjord",
    "marine": "coastal",
    "North Atlantic": "open_ocean",
    "Norwegian Sea": "shelf_sea",
}
EFFECT = {"individual": "individual_level", "review_mixed": "not_applicable"}
SEASON = {
    "annual": "full_year",
    "early summer": "summer",
    "not_specified": "not_applicable",
}
STUDY = {
    "longitudinal_time_series": "field_sampling",
    "natural_experiment": "field_sampling",
    "before_after_aquaculture_removal": "field_sampling",
    "before_after_3_phases": "field_sampling",
    "narrative synthesis review": "literature_review",
    "synthesis of experimental and observational studies": "literature_review",
    "observational longitudinal monitoring": "field_sampling",
    "statistical modelling": "statistical_analysis",
    "mixed-effects regression": "statistical_analysis",
    "regression_analysis": "statistical_analysis",
    "mark_recapture": "field_sampling",
    "controlled_experiment": "laboratory_challenge",
    "randomized_controlled_trial": "laboratory_challenge",
    "individual-based simulation model": "population_modelling",
    "farm_lice_dynamics_model": "virtual_post_smolt_modelling",
    "hindcast_scenario": "virtual_post_smolt_modelling",
    "spatial-temporal superimposition of trajectories and lice densities": "statistical_analysis",
    "empirically-fitted fjord-use models": "statistical_analysis",
    "comparative cross-regional methods study": "statistical_analysis",
    "multi-river population monitoring": "field_sampling",
    "long_term_time_series": "field_sampling",
    "data_harmonisation": "statistical_analysis",
    "backcalculation_from_scales": "statistical_analysis",
    "wild_and_hatchery_comparison": "field_sampling",
    "wild_fish_sampling": "field_sampling",
}
DATA = {
    "review of published literature": "published_literature",
    "beach_seine_sampling": "wild_fish_sampling",
    "microscopic_lice_enumeration": "wild_fish_sampling",
    "catch statistics": "wild_fish_sampling",
    "coded_wire_tag_mark_recapture": "wild_fish_sampling",
    "farm_production_data": "farm_lice_counts",
    "fish_trap_monitoring_River_Imsa": "trap_net_data",
    "government_monitoring": "wild_fish_sampling",
    "hatchery_release_and_recapture": "wild_fish_sampling",
    "industry_MERP": "farm_lice_counts",
    "industry_biomass_records": "farm_lice_counts",
    "laboratory_challenge": "wild_fish_sampling",
    "ocean_model_salinity": "hydrodynamic_model_output",
    "scale_backcalculation": "wild_fish_sampling",
    "NGO_programmes": "wild_fish_sampling",
    "Norwegian_Sea_surface_temperature_records": "published_literature",
    "snorkelling surveys of spawning populations": "wild_fish_sampling",
    "underwater video surveillance systems (fish ladders)": "wild_fish_sampling",
    "acoustic telemetry tracking data (N=517 individual sea trout)": "telemetry_tracking",
    "simulated individual trajectories (N=8049)": "particle_tracking_output",
    "open-access spatial-temporal modelled lice density data (Sandvik et al. 2020; Stige et al. 2021)": "particle_tracking_output",
    "Norwegian national salmon lice monitoring programme gill-net sampling (2004-2010)": "wild_fish_sampling",
    "Salmon farm infestation pressure data (lusedata.no)": "farm_lice_counts",
    "Fjord surface temperature data (monthly county means)": "published_literature",
    "River discharge as freshwater proxy": "published_literature",
    "hydrogeographic data (river length, area, mean discharge, precipitation field)": "published_literature",
}
OBS = {
    "individual fish": "individual_fish",
    "individual fish (simulated trajectory)": "individual_fish",
    "individual post-smolt; river-level mortality estimate aggregated to production zone": "mixed",
    "individual river (N=27 rivers)": "river",
    "population": "mixed",
    "population (N=5 populations)": "mixed",
    "river region (N=8 regions)": "production_area",
    "sampling occasion": "site",
    "sampling_event": "site",
    "site_year": "site",
    "cohort": "fish_group",
    "farm_network": "farm",
    "fish_health_zone": "production_area",
    "individual_parasite": "individual_fish",
}
COMP = {
    "pre_post_aquaculture_removal": "farm_present_vs_removed",
    "temporal_trend": "among_years",
    "temporal_trend_regression": "among_years",
    "review_mixed": "mixed",
    "scenario_vs_baseline": "mixed",
    "coordinated_vs_uncoordinated": "mixed",
    "environmental_correlation": "mixed",
    "three_phase_comparison": "before_after",
    "wild_vs_hatchery": "mixed",
    "lethal_vs_non_lethal_protocol": "mixed",
    "across populations (N=5)": "among_regions",
    "across years (2013, 2014, 2015)": "among_years",
    "comparison across 8 Norwegian river regions": "among_regions",
    "high vs. low infestation pressure years": "high_vs_low_infestation",
    "inner fjord vs. outer fjord (farm density gradient)": "among_regions",
    "inner-fjord vs outer-fjord migrants": "among_regions",
    "merged PFA (salmon + trout) vs single-species PFA (salmon only)": "mixed",
    "smolts vs veteran migrants": "mixed",
    "standardized vs raw PFA values": "mixed",
    "temperature x farm pressure interaction": "mixed",
}
OUT = {
    "infestation": "infestation_on_wild_fish",
    "sea_lice_prevalence": "infestation_on_wild_fish",
    "sea_lice_abundance": "infestation_on_wild_fish",
    "sea_lice_intensity": "infestation_on_wild_fish",
    "lice abundance": "infestation_on_wild_fish",
    "lice infestation level": "infestation_on_wild_fish",
    "lice infestation prevalence": "infestation_on_wild_fish",
    "lice intensity": "infestation_on_wild_fish",
    "lice-induced mortality probability": "mortality",
    "fraction of total mortality attributed to lice": "mortality",
    "farm_lice_abundance": "lice_abundance_on_farms",
    "lice_load_by_zone": "infestation_pressure",
    "management_effectiveness": "regulatory_classification",
    "treatment_frequency": "lice_abundance_on_farms",
    "pre-fishery abundance (PFA)": "population_abundance",
    "population status assessment": "population_abundance",
    "regional variation in salmonid populations": "population_abundance",
    "smolt migration timing": "migration_timing",
    "physiological readiness for seawater": "physiological_stress",
    "survival during migration": "survival",
    "behavioral changes during smoltification": "behaviour_change",
    "age_at_maturity": "population_abundance",
    "body_size_at_maturity": "population_abundance",
    "condition_factor": "physiological_stress",
    "fecundity": "population_abundance",
    "post-smolt_growth": "physiological_stress",
    "Lice-induced mortality fraction of seaward-migrating post-smolts; production-zone biomass-adjusted louse egg output": "mortality",
}

UNCERT_KEYWORDS = [
    ("calibration", "calibration_data"),
    ("migration timing", "migration_timing"),
    ("migration", "migration_timing"),
    ("hydrodynamic", "hydrodynamics"),
    ("threshold", "infestation_to_mortality_thresholds"),
    ("taranger", "infestation_to_mortality_thresholds"),
    ("sampling", "sampling_representativeness"),
    ("sample size", "sampling_representativeness"),
    ("model", "model_structure"),
    ("parameter", "parameter_uncertainty"),
    ("transfer", "transferability"),
    ("bias", "observational_bias"),
    ("larval", "larval_production"),
    ("duration", "migration_duration"),
]


def map_uncertainty(s: str) -> str:
    low = s.lower()
    for kw, token in UNCERT_KEYWORDS:
        if kw in low:
            return token
    # already controlled?
    controlled = {
        "migration_timing",
        "migration_duration",
        "larval_production",
        "hydrodynamics",
        "calibration_data",
        "infestation_to_mortality_thresholds",
        "observational_bias",
        "sampling_representativeness",
        "model_structure",
        "parameter_uncertainty",
        "transferability",
        "none_highlighted",
    }
    if s in controlled:
        return s
    return "none_highlighted"


def rewrite_list(raw: str, key: str, values: list[str]) -> str:
    lines = "\n".join(
        f'  - "{v}"' if re.search(r"[ ,()/]", v) else f"  - {v}" for v in values
    )
    pat = re.compile(rf"^{re.escape(key)}:\s*\n(?:[ \t]*-.*\n)*", re.M)
    if not pat.search(raw):
        return raw
    return pat.sub(f"{key}:\n{lines}\n", raw, count=1)


def append_tag(raw: str, tag: str) -> str:
    if tag in raw and f"- \"{tag}\"" in raw:
        return raw
    line = f'  - "{tag[:180]}"\n'
    m = re.search(r"^retrieval_tags:\s*\n((?:[ \t]*-.*\n)*)", raw, re.M)
    if not m:
        return raw.replace("curator_review_status:", f"retrieval_tags:\n{line}\ncurator_review_status:", 1)
    return raw[: m.end()] + line + raw[m.end() :]


def norm_list(values, mapper: dict, tag_prose=True):
    out, prose = [], []
    for v in values or []:
        s = str(v)
        if s in mapper:
            t = mapper[s]
            if t not in out:
                out.append(t)
            if tag_prose and mapper[s] != s:
                prose.append(s)
        else:
            # leave; caller may handle
            if s not in out:
                out.append(s)
    return out, prose


def main() -> int:
    for doc in list_doc_ids():
        p = doc_dir(doc) / "metadata.yaml"
        raw = p.read_text(encoding="utf-8")
        meta = yaml.safe_load(strip_yaml_comments(raw)) or {}
        orig = raw
        prose: list[str] = []

        def apply(key, mapper, transform=None):
            nonlocal raw, prose
            vals = meta.get(key) or []
            if not isinstance(vals, list):
                vals = [vals]
            if transform:
                new, pr = [], []
                for v in vals:
                    s = str(v)
                    t = transform(s)
                    if t not in new:
                        new.append(t)
                    if t != s:
                        pr.append(s)
            else:
                new, pr = norm_list(vals, mapper)
            # drop unknowns that are still invalid by forcing transform-only paths
            if new != list(map(str, vals)):
                raw = rewrite_list(raw, key, new)
                prose.extend(pr)
                meta[key] = new

        apply("host_species", HOST)
        apply("parasite_species", PARASITE)
        apply("environment", ENV)
        apply("seasonality_focus", SEASON)
        apply("study_design", STUDY)
        apply("data_source", DATA)
        apply("observation_unit", OBS)
        apply("comparison_type", COMP)
        apply("outcome_domain", OUT)

        # effect_scale scalar
        es = meta.get("effect_scale")
        if es in EFFECT:
            raw = re.sub(
                r"^effect_scale:\s*.*$",
                f"effect_scale: {EFFECT[es]}",
                raw,
                count=1,
                flags=re.M,
            )
            prose.append(str(es))

        # comparison_type long Kristoffersen blob
        comps = [str(x) for x in (meta.get("comparison_type") or [])]
        new_c = []
        for c in comps:
            if c.startswith("River-level and production-zone"):
                new_c.extend(["among_regions", "among_years"])
                prose.append(c[:120])
            elif c in COMP:
                if COMP[c] not in new_c:
                    new_c.append(COMP[c])
                if COMP[c] != c:
                    prose.append(c)
            elif c in {
                "exposed_vs_unexposed",
                "treated_vs_untreated",
                "farm_present_vs_removed",
                "high_vs_low_infestation",
                "observed_vs_modelled",
                "trawl_vs_sentinel",
                "before_after",
                "among_regions",
                "among_years",
                "none",
                "mixed",
            }:
                if c not in new_c:
                    new_c.append(c)
            else:
                if "mixed" not in new_c:
                    new_c.append("mixed")
                prose.append(c)
        if new_c and new_c != comps:
            raw = rewrite_list(raw, "comparison_type", new_c)

        # uncertainty sources
        unc = [str(x) for x in (meta.get("main_uncertainty_sources") or []) if x]
        new_u = []
        for u in unc:
            t = map_uncertainty(u)
            if t not in new_u:
                new_u.append(t)
            if t != u:
                prose.append(u[:160])
        if new_u != unc:
            raw = rewrite_list(raw, "main_uncertainty_sources", new_u)

        # outcome leftovers → map or mortality/infestation
        outs = [str(x) for x in (meta.get("outcome_domain") or [])]
        new_o = []
        for o in outs:
            if o in OUT:
                if OUT[o] not in new_o:
                    new_o.append(OUT[o])
                if OUT[o] != o:
                    prose.append(o)
            elif o in {
                "lice_abundance_on_farms",
                "larval_density_in_water",
                "infestation_on_wild_fish",
                "infestation_pressure",
                "migration_timing",
                "migration_route",
                "physiological_stress",
                "skin_damage",
                "osmoregulatory_effects",
                "behaviour_change",
                "survival",
                "mortality",
                "marine_survival",
                "adult_returns",
                "population_abundance",
                "regulatory_classification",
                "model_performance",
                "uncertainty_estimation",
            }:
                if o not in new_o:
                    new_o.append(o)
            else:
                if "mortality" not in new_o:
                    new_o.append("mortality")
                prose.append(o)
        if new_o != outs:
            raw = rewrite_list(raw, "outcome_domain", new_o)

        # study_design leftovers
        sds = [str(x) for x in (meta.get("study_design") or [])]
        new_s = []
        for s in sds:
            if s in STUDY:
                if STUDY[s] not in new_s:
                    new_s.append(STUDY[s])
                prose.append(s)
            elif s in {
                "laboratory_challenge",
                "field_sampling",
                "trawl_sampling",
                "sentinel_cage",
                "telemetry",
                "genetic_assignment",
                "farm_monitoring",
                "statistical_analysis",
                "hydrodynamic_modelling",
                "particle_tracking",
                "virtual_post_smolt_modelling",
                "population_modelling",
                "literature_review",
                "expert_assessment",
                "mixed",
            }:
                if s not in new_s:
                    new_s.append(s)
            else:
                if "statistical_analysis" not in new_s:
                    new_s.append("statistical_analysis")
                prose.append(s)
        if new_s != sds:
            raw = rewrite_list(raw, "study_design", new_s)

        # data_source leftovers
        dss = [str(x) for x in (meta.get("data_source") or [])]
        new_d = []
        for d in dss:
            if d in DATA:
                if DATA[d] not in new_d:
                    new_d.append(DATA[d])
                prose.append(d[:160])
            elif d in {
                "wild_fish_sampling",
                "farm_lice_counts",
                "sentinel_cages",
                "trawl_data",
                "trap_net_data",
                "telemetry_tracking",
                "genetic_assignment",
                "hydrodynamic_model_output",
                "particle_tracking_output",
                "expert_group_reports",
                "published_literature",
                "mixed",
            }:
                if d not in new_d:
                    new_d.append(d)
            else:
                if "published_literature" not in new_d:
                    new_d.append("published_literature")
                prose.append(d[:160])
        if new_d != dss:
            raw = rewrite_list(raw, "data_source", new_d)

        for t in prose:
            raw = append_tag(raw, t)

        if raw != orig:
            p.write_text(raw, encoding="utf-8")
            print(f"normalized {doc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
