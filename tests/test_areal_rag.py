from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "app"))

from retrieval import (  # noqa: E402
    AREAL_DATA_FILE,
    areal_route_match_score,
    best_retrieval_score,
    evidence_family,
    infer_areal_priority_questions,
    is_areal_out_of_scope,
    json_list_contains,
    lexical_scores,
    publication_group,
    retrieve_areal_hybrid,
)
from synthesis import build_evidence_block, citation_label  # noqa: E402


class ArealBenchmarkTests(unittest.TestCase):
    def test_fixture_is_complete_and_references_existing_documents(self) -> None:
        fixture_path = REPO / "eval" / "areal_retrieval_benchmark.json"
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        cases = fixture["cases"]
        self.assertEqual({f"A{i}" for i in range(7)}, {c["route"] for c in cases if not c["expected_oos"]})
        self.assertGreaterEqual(sum(c["expected_oos"] for c in cases), 3)

        corpus_ids = set(pd.read_parquet(AREAL_DATA_FILE, columns=["doc_id"])["doc_id"])
        referenced = {
            doc_id
            for case in cases
            for group in case["essential_groups"]
            for doc_id in group
        } | {doc_id for case in cases for doc_id in case["acceptable"]}
        self.assertEqual(set(), referenced - corpus_ids)


class ArealRetrievalUnitTests(unittest.TestCase):
    def test_areal_scope_guard_rejects_non_room_questions(self) -> None:
        self.assertTrue(is_areal_out_of_scope("Hvilken antibiotikadose bør brukes for å behandle laks?", [{"semantic_score": 0.9}]))
        self.assertFalse(is_areal_out_of_scope("Hvordan påvirker smoltdødelighet lokalitetstillatelser og arealplanlegging for havbruk?", [{"semantic_score": 0.9}]))
        self.assertFalse(is_areal_out_of_scope("Hva begrenser havbrukets arealbruk?", [{"semantic_score": 0.9}]))

    def test_json_list_filter_matches_populated_metadata(self) -> None:
        self.assertTrue(json_list_contains('["A1", "A4"]', ["A4"]))
        self.assertFalse(json_list_contains('["A1"]', ["A4"]))

    def test_routes_cover_areal_question_types(self) -> None:
        self.assertEqual(["A0", "A5"], infer_areal_priority_questions("Hva begrenser vekst og er mer areal nok når tetthet binder?"))
        self.assertIn("A2", infer_areal_priority_questions("Hvor dør en lokalitetstillatelse etter akvakulturloven?"))
        self.assertIn("A6", infer_areal_priority_questions("Åpner Havbruksfondet mer sjø?"))

    def test_route_boost_does_not_require_every_inferred_code(self) -> None:
        query = (
            "Når kommunen peker ut sjøareal, avgjør plankartet, dispensasjon "
            "eller innsigelse og avslag saken?"
        )
        routes = {q for q in infer_areal_priority_questions(query) if q != "A0"}
        self.assertIn("A1", routes)
        self.assertIn("A2", routes)
        self.assertEqual(1.0, areal_route_match_score(["A1", "A3"], routes))
        self.assertEqual(1.0, areal_route_match_score(["A1", "A2", "A3", "A4", "A5", "A6"], routes))
        self.assertEqual(0.0, areal_route_match_score(["A5"], routes))

    def test_lexical_scoring_rewards_rare_exact_terms(self) -> None:
        scores = lexical_scores(
            "korall føre var lokalitetssøknad",
            ["korall og føre var i lokalitetssøknad", "kommunal plan og skatt", "fiskehelse"],
        )
        self.assertGreater(scores[0], scores[1])
        self.assertGreater(scores[0], scores[2])

    def test_semantic_score_remains_basis_for_scope_check(self) -> None:
        results = [{"score": 0.9, "semantic_score": 0.12}, {"score": 0.5, "semantic_score": 0.31}]
        self.assertEqual(0.31, best_retrieval_score(results))

    def test_duplicate_publications_and_evidence_families_are_explicit(self) -> None:
        self.assertEqual(
            publication_group("2017_kvalvik_intermunicipal-coastal-planning"),
            publication_group("2017_kvalvik_ocean-coastal-management"),
        )
        self.assertEqual(
            evidence_family("2024_sordahl_when-all-you-have-is-a-hammer"),
            evidence_family("2026_sordahl_nar-alt-skal-med"),
        )

    def test_hybrid_retrieval_deduplicates_same_publication_without_api(self) -> None:
        df = pd.read_parquet(AREAL_DATA_FILE)
        target = df.loc[df["doc_id"] == "2017_kvalvik_intermunicipal-coastal-planning"].iloc[0]
        query_vec = np.array(json.loads(target["embedding"]), dtype=np.float32)
        results, routes = retrieve_areal_hybrid(
            client=None,
            query="intermunicipal coastal planning and dispensation",
            top_k=39,
            query_embedding=query_vec,
            data_file=AREAL_DATA_FILE,
        )
        groups = [r["publication_group"] for r in results]
        self.assertEqual(len(groups), len(set(groups)))
        self.assertIn("A1", routes)


class EvidenceContextTests(unittest.TestCase):
    def test_context_contains_query_relevant_claims_and_caveats(self) -> None:
        result = {
            "doc_id": "doc",
            "authors": "Example Author",
            "year": "2025",
            "title": "Example",
            "evidence_direction": "not_applicable",
            "quality_signal": "medium",
            "effect_scale": "municipal_level",
            "document_type": "research_article",
            "source_type": "peer_reviewed",
            "study_design": ["case_study"],
            "geography": ["Norway"],
            "controversy_role": "supportive",
            "key_claims": ["Tax revenue was discussed.", "Coral thresholds varied between locality cases."],
            "claims_about_uncertainty": ["The coral evidence was incomplete."],
            "claims_about_policy_or_management": ["Authorities should document precaution."],
            "methodological_limitations": ["The sample covered one county."],
            "rag_summary": "A study of locality decisions.",
            "summary_text": "General background.\n\nThe analysis found inconsistent coral thresholds in locality applications.\n\nUnrelated history.",
            "curator_review_status": "ai_verified",
            "evidence_family": "family:doc",
        }
        block = build_evidence_block([result], compact=True, query="coral threshold locality")
        self.assertIn("Coral thresholds varied", block)
        self.assertIn("Methodological limitations", block)
        self.assertIn("The coral evidence was incomplete", block)
        self.assertIn("inconsistent coral thresholds", block)
        self.assertIn("Verification status: ai_verified", block)

    def test_citation_label_counts_authors(self) -> None:
        self.assertEqual(citation_label("Ingunn Elise Myklebust", "2018"), "Myklebust 2018")
        self.assertEqual(
            citation_label("Tonje C. Osmundsen; Marit Schei Olsen", "2025"), "Osmundsen & Olsen 2025"
        )
        self.assertEqual(
            citation_label("Roy Robertsen; Ingrid Kvalvik; Otto Andreassen", "2014"), "Robertsen et al. 2014"
        )
        self.assertEqual(citation_label("", "2024", "Meld. St. 35"), "Meld. St. 35 2024")


if __name__ == "__main__":
    unittest.main()
