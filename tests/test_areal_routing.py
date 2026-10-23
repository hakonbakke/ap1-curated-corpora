"""Tests for the A0-A8 funnel: routing in `_ask`, the routing caption, «Valgt via» captions,
the new slider range, and unit tests of routing.pq_code_for_text / retrieve_funnel.

No network: dotenv loading, page_link, the OpenAI client, routing.classify_pq and
routing.retrieve_funnel (page tests), routing.load_corpus and routing.get_embedding (unit tests)
are all replaced.
"""

from __future__ import annotations

import json
import math
import sys
import unittest
from pathlib import Path
from unittest import mock

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "app"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import feedback  # noqa: E402
import routing  # noqa: E402
from test_areal_answer_view import KORT, RESULTS, _PageCase  # noqa: E402
from test_areal_section_c import FAULTS  # noqa: E402

PQ_NO = [f[2] for f in FAULTS["no"]]
PQ_EN = [f[2] for f in FAULTS["en"]]


class PqCodeForTextTests(unittest.TestCase):
    def test_verbatim_text_gives_its_code(self) -> None:
        for i, text in enumerate(PQ_NO):
            self.assertEqual(f"A{i}", routing.pq_code_for_text(text, PQ_NO))

    def test_surrounding_whitespace_is_ignored(self) -> None:
        self.assertEqual("A2", routing.pq_code_for_text("  " + PQ_NO[2] + "\n", PQ_NO))

    def test_edited_other_language_empty_and_none_give_none(self) -> None:
        self.assertIsNone(routing.pq_code_for_text(PQ_NO[2] + " Og mer.", PQ_NO))
        self.assertIsNone(routing.pq_code_for_text(PQ_EN[2], PQ_NO))
        self.assertIsNone(routing.pq_code_for_text("", PQ_NO))
        self.assertIsNone(routing.pq_code_for_text(None, PQ_NO))


def _vec(angle_deg: float) -> np.ndarray:
    a = math.radians(angle_deg)
    return np.array([math.cos(a), math.sin(a)], dtype=np.float32)


def _row(doc_id: str, angle: float, tags: list[str]) -> dict:
    return {
        "doc_id": doc_id,
        "title": doc_id,
        "year": 2020,
        "priority_questions": json.dumps(tags),
        "_embedding": _vec(angle),
    }


KV_A = "2017_kvalvik_intermunicipal-coastal-planning"
KV_B = "2017_kvalvik_ocean-coastal-management"


class RetrieveFunnelTests(unittest.TestCase):
    """Query vector is (1, 0); a smaller angle means a higher similarity."""

    CORPUS = pd.DataFrame(
        [
            _row("tag_far", 80, ["A2"]),
            _row("tag_near", 40, ["A2", "A5"]),
            _row(KV_A, 50, ["A2"]),  # same publication as KV_B
            _row(KV_B, 45, ["A2"]),
            _row("other_tag", 5, ["A5"]),  # tagged, but not with the wanted code
            _row("plain_near", 10, []),
            _row("plain_far", 70, []),
        ]
    )

    def run_funnel(self, codes, top_k, selected=None):
        with mock.patch.object(routing, "load_corpus", lambda f=None: self.CORPUS), mock.patch.object(
            routing, "get_embedding", lambda client, text: _vec(0)
        ):
            return routing.retrieve_funnel(None, "q", codes, top_k=top_k, selected_doc_ids=selected)

    @staticmethod
    def ids(results):
        return [r["doc_id"] for r in results]

    def test_tagged_first_by_similarity_then_untagged_fill_by_similarity(self) -> None:
        results = self.run_funnel(["A2"], top_k=5)
        # Tagged A2 by similarity (the Kvalvik pair counts once), then the fill by similarity.
        self.assertEqual(["tag_near", KV_B, "tag_far", "other_tag", "plain_near"], self.ids(results))
        self.assertEqual([["A2"], ["A2"], ["A2"], [], []], [r["via_pq"] for r in results])

    def test_publication_group_takes_one_place_only(self) -> None:
        ids = self.ids(self.run_funnel(["A2"], top_k=7))
        self.assertEqual([KV_B], [i for i in ids if i.startswith("2017_kvalvik")])  # the more similar file
        self.assertEqual(6, len(ids))

    def test_via_pq_lists_only_the_matching_codes(self) -> None:
        results = self.run_funnel(["A2", "A5"], top_k=4)
        by_id = {r["doc_id"]: r["via_pq"] for r in results}
        self.assertEqual(["A2", "A5"], by_id["tag_near"])
        self.assertEqual(["A5"], by_id["other_tag"])

    def test_without_codes_it_is_plain_semantic_search(self) -> None:
        results = self.run_funnel([], top_k=3)
        self.assertEqual(["other_tag", "plain_near", "tag_near"], self.ids(results))
        self.assertTrue(all(r["via_pq"] == [] for r in results))

    def test_semantic_score_is_the_cosine_and_selection_is_respected(self) -> None:
        results = self.run_funnel(["A2"], top_k=5, selected=["tag_far", "plain_near"])
        self.assertEqual(["tag_far", "plain_near"], self.ids(results))
        self.assertAlmostEqual(math.cos(math.radians(80)), results[0]["semantic_score"], places=4)
        self.assertEqual([], self.run_funnel(["A2"], top_k=5, selected=["missing"]))


class _RoutingPageCase(_PageCase):
    classify_returns: list[str] = []
    funnel_score = 0.9

    def setUp(self) -> None:
        super().setUp()
        self.classify_calls: list[dict] = []
        self.funnel_calls: list[dict] = []
        outer = self

        def fake_classify(client, query, pq_texts):
            outer.classify_calls.append({"query": query, "pq_texts": list(pq_texts)})
            return list(outer.classify_returns)

        def fake_funnel(client, query, codes, **kwargs):
            outer.funnel_calls.append({"query": query, "codes": list(codes), **kwargs})
            return [
                {
                    **r,
                    "semantic_score": outer.funnel_score,
                    "score": outer.funnel_score,
                    "via_pq": list(codes) if i == 0 else [],
                }
                for i, r in enumerate(RESULTS)
            ]

        for p in (
            mock.patch("routing.classify_pq", fake_classify),
            mock.patch("routing.retrieve_funnel", fake_funnel),
        ):
            p.start()
            self.addCleanup(p.stop)

    def english(self):
        at = self.app().run()
        self.set_radio(at, "Språk / Language", "en")
        at.run()
        return at

    @staticmethod
    def ask_again(at):
        next(b for b in at.button if b.label in ("Spør kildene", "Ask the sources")).click()
        at.run()

    @staticmethod
    def captions(at):
        return [c.value for c in at.caption]

    def answers(self):
        return [p for p in self.sent if p["type"] == "answer"]


class RoutingFlowTests(_RoutingPageCase):
    def test_open_question_skips_the_classifier_and_routes_to_its_code(self) -> None:
        at = self.app().run()
        self.ask(at, PQ_NO[3])
        self.assertFalse(at.exception, at.exception)
        self.assertEqual([], self.classify_calls)
        self.assertEqual(["A3"], self.funnel_calls[0]["codes"])
        self.assertEqual(["A3"], at.session_state["areal_last"]["routed_pq"])
        self.assertEqual("A3", self.answers()[0]["routed_pq"])

    def test_open_question_from_the_other_language_still_routes(self) -> None:
        at = self.app().run()  # Norwegian page, English text kept across a language switch
        self.ask(at, PQ_EN[7])
        self.assertEqual([], self.classify_calls)
        self.assertEqual(["A7"], self.funnel_calls[0]["codes"])

    def test_own_question_calls_the_classifier_once_with_current_language_texts(self) -> None:
        self.classify_returns = ["A2", "A6"]
        at = self.app().run()
        self.ask(at, "Hvor lang tid tar en søknad?")
        self.assertEqual(1, len(self.classify_calls))
        self.assertEqual(PQ_NO, self.classify_calls[0]["pq_texts"])
        self.assertEqual(["A2", "A6"], self.funnel_calls[0]["codes"])
        self.assertEqual(12, self.funnel_calls[0]["top_k"])
        self.assertEqual("A2,A6", self.answers()[0]["routed_pq"])
        en = self.english()
        self.ask(en, "How long does an application take?")
        self.assertEqual(PQ_EN, self.classify_calls[1]["pq_texts"])

    def test_cache_hit_calls_neither_classifier_nor_funnel_and_keeps_the_caption(self) -> None:
        self.classify_returns = ["A2"]
        at = self.app().run()
        self.ask(at, "Hvor lang tid tar en søknad?")
        self.ask_again(at)
        self.assertFalse(at.exception, at.exception)
        self.assertEqual((1, 1), (len(self.classify_calls), len(self.funnel_calls)))
        self.assertEqual([False, True], [r["cached"] for r in self.answers()])
        self.assertEqual(["A2", "A2"], [r["routed_pq"] for r in self.answers()])
        expected = "Koblet til åpent spørsmål: A2 · Søknadsprosessen for lokaliteter"
        self.assertIn(expected, self.captions(at))
        self.assertEqual(["A2"], at.session_state["areal_last"]["routed_pq"])
        at.run()  # a plain rerun reads areal_last
        self.assertIn(expected, self.captions(at))
        self.assertEqual(1, len(self.classify_calls))

    def test_classifier_failure_is_plain_search(self) -> None:
        self.classify_returns = []
        at = self.app().run()
        self.ask(at, "Noe helt annet om havbruk")
        self.assertEqual([], self.funnel_calls[0]["codes"])
        self.assertEqual("", self.answers()[0]["routed_pq"])


class RoutingCaptionTests(_RoutingPageCase):
    def test_caption_text_in_both_languages_with_codes_and_without(self) -> None:
        cases = [
            ("no", ["A2"], "Koblet til åpent spørsmål: A2 · Søknadsprosessen for lokaliteter"),
            (
                "no",
                ["A2", "A8"],
                "Koblet til åpent spørsmål: A2 · Søknadsprosessen for lokaliteter og A8 · Biosikkerhet, smitte og vannkontakt",
            ),
            ("en", ["A2"], "Linked to open question: A2 · The site application process"),
            (
                "en",
                ["A4", "A1"],
                "Linked to open question: A4 · Economic instruments and area use and A1 · Bottlenecks and development",
            ),
            ("no", [], "Ikke koblet til et åpent spørsmål; svaret bygger på vanlig søk."),
            ("en", [], "Not linked to an open question; the answer uses plain search."),
        ]
        for lang, codes, expected in cases:
            with self.subTest(lang=lang, codes=codes):
                self.classify_returns = codes
                at = self.english() if lang == "en" else self.app().run()
                self.ask(at, f"Et eget spørsmål om areal {lang} {codes}")
                self.assertFalse(at.exception, at.exception)
                self.assertIn(expected, self.captions(at))  # the streaming run
                at.run()
                self.assertIn(expected, self.captions(at))  # a rerun from areal_last

    def test_caption_sits_directly_under_the_heading(self) -> None:
        self.classify_returns = ["A2"]
        at = self.app().run()
        self.ask(at, "Et eget spørsmål om areal")
        flat = [getattr(e, "value", "") for e in at.main]
        heads = [i for i, v in enumerate(flat) if v == "Syntese"]
        self.assertTrue(heads)
        self.assertTrue(flat[heads[0] + 1].startswith("Koblet til åpent spørsmål"))


class OutOfScopeTests(_RoutingPageCase):
    funnel_score = 0.05

    def test_low_score_without_codes_is_out_of_scope(self) -> None:
        at = self.app().run()
        self.ask(at, "Hva er hovedstaden i Frankrike?")
        self.assertTrue(any("utenfor dette korpuset" in w.value for w in at.warning))
        self.assertEqual("out_of_scope", self.answers()[0]["error"])
        self.assertNotIn("areal_last", at.session_state)

    def test_low_score_with_codes_is_still_answered(self) -> None:
        self.classify_returns = ["A2"]
        at = self.app().run()
        self.ask(at, "Hvor lang tid tar en søknad?")
        self.assertFalse(at.warning)
        self.assertEqual("", self.answers()[0]["error"])
        self.assertIn(KORT, [m.value for m in at.markdown])

    def test_open_question_with_low_score_is_answered(self) -> None:
        at = self.app().run()
        self.ask(at, PQ_NO[0])
        self.assertFalse(at.warning)
        self.assertEqual("A0", self.answers()[0]["routed_pq"])


class SourceCaptionTests(_RoutingPageCase):
    def test_tagged_sources_show_valgt_via_in_both_modes_and_languages(self) -> None:
        for lang, expected in (("no", "Valgt via A4"), ("en", "Selected via A4")):
            for mode in ("researcher", "non_researcher"):
                with self.subTest(lang=lang, mode=mode):
                    at = self.english() if lang == "en" else self.app().run()
                    self.set_radio(at, "Choose your background" if lang == "en" else "Velg bakgrunn", mode)
                    at.run()
                    self.ask(at, PQ_NO[4] if lang == "no" else PQ_EN[4])
                    self.assertFalse(at.exception, at.exception)
                    for _ in range(2):  # the streaming run, then a rerun
                        self.assertEqual(1, self.captions(at).count(expected))  # only the tagged first source
                        at.run()

    def test_untagged_sources_have_no_caption(self) -> None:
        at = self.app().run()
        self.ask(at, "Et eget spørsmål om areal")  # no codes: via_pq stays empty
        self.assertFalse([c for c in self.captions(at) if c.startswith("Valgt via")])


class SliderTests(_RoutingPageCase):
    def test_default_12_and_max_15(self) -> None:
        for at in (self.app().run(), self.english()):
            s = at.slider[0]
            self.assertEqual((3, 15, 12), (s.min, s.max, s.value))


class PayloadOrderTests(unittest.TestCase):
    BASE = dict(
        session_id="s", answer_id="a", question="q", mode="researcher", language="no", model="m",
        top_k=12, n_active_docs=5, retrieved=["d1"], answer="x", latency_s=1.0, cached=False,
    )

    def test_routed_pq_comes_last_after_answer_shape(self) -> None:
        p = feedback.build_answer_payload(**self.BASE, routed_pq="A2,A6")
        self.assertEqual(["answer_words", "answer_shape", "routed_pq"], list(p)[-3:])
        self.assertEqual("A2,A6", p["routed_pq"])
        self.assertEqual("", feedback.build_answer_payload(**self.BASE)["routed_pq"])


if __name__ == "__main__":
    unittest.main()
