"""Tests for the full-text material in the Areal room: the checks and segmentation in
scripts/build_areal_enrichment.py, app/enrichment.py, the chapter lift in
routing.retrieve_funnel and the evidence block in synthesis.py. No network.
"""

from __future__ import annotations

import math
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "app"))
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_areal_enrichment as build  # noqa: E402
import enrichment  # noqa: E402
import routing  # noqa: E402
from synthesis import AREA_EVIDENCE_BUDGET, build_evidence_block  # noqa: E402
from test_areal_routing import _row, _vec  # noqa: E402

SOURCE = """<!-- page 86 -->
## 3.3.3 Contaminants

Of the 256 papers kept after the full-text screen, nearly
50 % concerned delousing agents (164 papers), and **most** of them
were field stud-
ies from Norway.
<!-- page 87 -->
Copper use was 1 539 tonnes in 2020.
"""


class QuoteCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.norm = build.squash(SOURCE)

    def test_quote_survives_line_breaks_markdown_and_hyphenation(self) -> None:
        self.assertTrue(build.quote_found("nearly 50 % concerned delousing agents (164 papers)", self.norm))
        self.assertTrue(build.quote_found("and most of them were field studies from Norway", self.norm))

    def test_invented_or_too_short_quote_is_rejected(self) -> None:
        self.assertFalse(build.quote_found("64 % concerned delousing agents (164 papers)", self.norm))
        self.assertFalse(build.quote_found("50 %", self.norm))

    def test_statement_may_not_compute_new_numbers(self) -> None:
        quote = "nearly 50 % concerned delousing agents (164 papers)"
        self.assertTrue(build.statement_numbers_ok("Nearly 50 % (164) of the papers were on delousing agents.", quote))
        self.assertFalse(build.statement_numbers_ok("64 % of the papers were on delousing agents.", quote))

    def test_numbers_with_spaces_and_commas_match(self) -> None:
        self.assertTrue(build.statement_numbers_ok("Copper use was 1539 tonnes.", "Copper use was 1 539 tonnes in 2020."))
        self.assertTrue(build.statement_numbers_ok("Turnover 3 030, factor 0,597.", "Ringvirkning 3 030 0,597|1 806"))

    def test_a_year_from_the_source_may_be_added_but_no_other_number(self) -> None:
        quote = "nearly 50 % concerned delousing agents"
        self.assertTrue(build.statement_numbers_ok("In 2020, nearly 50 % ...", quote, build.numbers(SOURCE)))
        self.assertFalse(build.statement_numbers_ok("In 2021, nearly 50 % ...", quote, build.numbers(SOURCE)))
        self.assertFalse(build.statement_numbers_ok("Nearly 50 % in area 12.", quote, build.numbers(SOURCE)))

    def test_words_split_by_spaces_or_soft_hyphens_still_match(self) -> None:
        source = build.squash("en kommunal område regulering etter energi loven. Sammenstilte­data­for­de")
        self.assertTrue(build.quote_found("en kommunal områderegulering etter energiloven", source))
        self.assertTrue(build.quote_found("Sammenstilte data for de", source))

    def test_sentences_with_unknown_numbers_are_dropped(self) -> None:
        note = "Delousing agents dominate the contaminant papers (164 of 256). That is 64 % of the total. Copper is local."
        kept, dropped = build.keep_sentences_with_known_numbers(note, build.numbers(SOURCE))
        self.assertEqual(1, dropped)
        self.assertNotIn("64 %", kept)
        self.assertIn("164 of 256", kept)
        self.assertIn("Copper is local.", kept)

    def test_pq_codes_and_single_digits_are_not_checked(self) -> None:
        self.assertEqual(set(), build.numbers("Relevant to A4; three cases and 2 farms."))

    def test_page_comes_from_the_markers(self) -> None:
        pages = build.page_index(SOURCE)
        self.assertEqual(86, build.page_for_quote("nearly 50 % concerned delousing agents", pages))
        self.assertEqual(87, build.page_for_quote("Copper use was 1 539 tonnes in 2020.", pages))


class SegmentTests(unittest.TestCase):
    def test_chapters_start_segments_and_references_are_left_out(self) -> None:
        body = "word " * 4000  # 20,000 characters
        text = (
            f"<!-- page 1 -->\n## 1 Introduction\n{body}\n## References\nSmith 2001. Jones 2002.\n"
            f"<!-- page 9 -->\n## 2 Results\n{body}\n## 2.1 Detail\nshort\n"
        )
        segments = build.segment(text)
        self.assertEqual([["1 Introduction"], ["2 Results", "2.1 Detail"]], [s["headings"] for s in segments])
        self.assertNotIn("Smith 2001", "".join(s["text"] for s in segments))
        self.assertEqual([1, 9], [s["page_from"] for s in segments])

    def test_long_block_is_split_under_the_maximum(self) -> None:
        text = "## 1 One\n" + ("para " * 300 + "\n\n") * 100  # about 150,000 characters
        segments = build.segment(text)
        self.assertGreater(len(segments), 2)
        self.assertTrue(all(len(s["text"]) <= build.SEGMENT_MAX for s in segments))


def _write_enrichment(path: Path) -> None:
    rows = [
        {"kind": "chapter", "doc_id": "big", "pq": "", "title": "5 Planning", "text": "planning chapter",
         "quote": "", "page_from": 40, "page_to": 52, "embedding": _vec(5).tolist()},
        {"kind": "chapter", "doc_id": "big", "pq": "", "title": "2 Method", "text": "method chapter",
         "quote": "", "page_from": 3, "page_to": 9, "embedding": _vec(60).tolist()},
        {"kind": "figure", "doc_id": "near", "pq": "", "title": "", "text": "f-near", "quote": "q near 12",
         "page_from": 4, "page_to": None, "embedding": _vec(1).tolist()},
        {"kind": "figure", "doc_id": "near", "pq": "", "title": "", "text": "f-far", "quote": "q far 13",
         "page_from": None, "page_to": None, "embedding": _vec(80).tolist()},
        {"kind": "pq_note", "doc_id": "near", "pq": "A2", "title": "", "text": "note A2", "quote": "",
         "page_from": None, "page_to": None, "embedding": _vec(0).tolist()},
        {"kind": "pq_note", "doc_id": "near", "pq": "A5", "title": "", "text": "note A5", "quote": "",
         "page_from": None, "page_to": None, "embedding": _vec(0).tolist()},
    ]
    frame = pd.DataFrame(rows)
    frame["page_from"] = frame["page_from"].astype("Int64")
    frame["page_to"] = frame["page_to"].astype("Int64")
    frame.to_parquet(path, index=False)


class EnrichmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "enrichment.parquet"
        _write_enrichment(self.path)

    def tearDown(self) -> None:
        enrichment._load_cached.clear()
        self.tmp.cleanup()

    def test_attach_adds_best_chapters_figures_and_notes_for_via_pq(self) -> None:
        results = [{"doc_id": "big", "via_pq": []}, {"doc_id": "near", "via_pq": ["A2"]}]
        enrichment.attach(results, _vec(0), self.path)
        big, near = results
        self.assertEqual(["5 Planning", "2 Method"], [c["title"] for c in big["chapter_hits"]])
        self.assertEqual((40, 52), (big["chapter_hits"][0]["page_from"], big["chapter_hits"][0]["page_to"]))
        self.assertEqual([], big["key_figures"])
        self.assertEqual(["f-near", "f-far"], [f["statement"] for f in near["key_figures"]])
        self.assertEqual([4, None], [f["page"] for f in near["key_figures"]])
        self.assertEqual({"A2": "note A2"}, near["pq_notes"])  # A5 not routed

    def test_best_chapter_scores(self) -> None:
        scores = enrichment.best_chapter_scores(_vec(0), self.path)
        self.assertAlmostEqual(math.cos(math.radians(5)), scores["big"], places=4)

    def test_other_embedding_size_or_missing_file_attaches_nothing(self) -> None:
        results = [{"doc_id": "near", "via_pq": []}]
        enrichment.attach(results, np.ones(3, dtype=np.float32), self.path)
        self.assertEqual(([], []), (results[0]["chapter_hits"], results[0]["key_figures"]))
        untouched = [{"doc_id": "near"}]
        enrichment.attach(untouched, _vec(0), Path(self.tmp.name) / "missing.parquet")
        self.assertEqual([{"doc_id": "near"}], untouched)


class ChapterLiftTests(unittest.TestCase):
    CORPUS = pd.DataFrame([_row("small", 35, []), _row("big", 40, [])])  # cos 0.819 and 0.766

    def run_funnel(self, chapter_scores):
        with mock.patch.object(routing, "load_corpus", lambda f=None: self.CORPUS), mock.patch.object(
            routing, "get_embedding", lambda client, text: _vec(0)
        ), mock.patch.object(enrichment, "best_chapter_scores", lambda q: chapter_scores), mock.patch.object(
            enrichment, "attach", lambda results, q: results
        ):
            return routing.retrieve_funnel(None, "q", [], top_k=2)

    def test_a_standout_chapter_lifts_its_report_but_keeps_the_document_cosine(self) -> None:
        results = self.run_funnel({"big": 0.99})
        self.assertEqual(["big", "small"], [r["doc_id"] for r in results])
        self.assertAlmostEqual(0.99 - routing.CHAPTER_LIFT_MARGIN, results[0]["score"], places=4)
        self.assertAlmostEqual(math.cos(math.radians(40)), results[0]["semantic_score"], places=4)

    def test_a_chapter_within_the_margin_changes_nothing(self) -> None:
        # 0.95 beats "small" (0.819), but less the margin it does not.
        self.assertEqual(["small", "big"], [r["doc_id"] for r in self.run_funnel({"big": 0.95})])
        self.assertEqual(["small", "big"], [r["doc_id"] for r in self.run_funnel({"big": 0.1})])


class EvidenceBlockTests(unittest.TestCase):
    RESULT = {
        "doc_id": "d", "title": "T", "authors": "Ann Evenset; Bo Refseth; Cy Dale", "year": "2023",
        "rag_summary": "s", "evidence_direction": "x", "quality_signal": "y", "key_claims": [],
        "pq_notes": {"A3": "What the report says on A3."},
        "chapter_hits": [{"title": "5 Planning", "text": "Chapter text.", "page_from": 40, "page_to": 52},
                         {"title": "2 Method", "text": "Method text.", "page_from": None, "page_to": None}],
        "key_figures": [{"quote": f"quote {n}", "statement": f"stmt {n}", "page": 7 if n == 0 else None}
                        for n in range(8)],
    }

    def test_top_documents_get_the_full_material(self) -> None:
        block = build_evidence_block([dict(self.RESULT)], compact=True, query="q", budget=AREA_EVIDENCE_BUDGET)
        self.assertIn("Note on A3, written from the full text:\nWhat the report says on A3.", block)
        self.assertIn('Matching chapter "5 Planning" (pp. 40-52)', block)
        self.assertIn('Matching chapter "2 Method", summary', block)
        self.assertIn('  - "quote 0" (p. 7) [stmt 0]', block)
        self.assertIn("quote 5", block)
        self.assertNotIn("quote 6", block)

    def test_lower_documents_get_less_and_the_default_budget_none(self) -> None:
        results = [dict(self.RESULT, doc_id=f"d{i}") for i in range(6)]
        last = build_evidence_block(results, compact=True, query="q", budget=AREA_EVIDENCE_BUDGET).split("---")[-1]
        self.assertIn("quote 2", last)
        self.assertNotIn("quote 3", last)
        self.assertNotIn("2 Method", last)
        plain = build_evidence_block([dict(self.RESULT)], compact=True, query="q")
        self.assertNotIn("Key figures", plain)
        self.assertNotIn("Matching chapter", plain)
        self.assertIn("Note on A3", plain)


if __name__ == "__main__":
    unittest.main()
