"""Short-answer split, answer-shape logging, the background panel, the new map, the
folded «Les hele svaret» view and the two extra rating questions.

Nothing here calls OpenAI or the webhook: dotenv loading, page_link, the OpenAI client,
retrieval and the webhook sender are replaced.
"""

from __future__ import annotations

import os
import sys
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "app"))

import feedback  # noqa: E402

PAGE = str(REPO / "app" / "pages" / "2_Areal_og_havbruk.py")

RESULTS = [
    {"doc_id": "2020_hersoug_a", "authors": "Hersoug, B.", "year": 2020, "title": "A study of licences",
     "semantic_score": 0.9, "score": 0.9, "rag_summary": "Licences limit growth.",
     "evidence_direction": "not_applicable", "quality_signal": "medium"},
]

LONG_REST = " ".join(f"ord{i}" for i in range(120))  # 120 words
KORT = f"**Kort svar**\n- Lisensene setter grensen.\n- Kommunene peker ut sjøen.\n\n{LONG_REST}"
SHORT_EN = "**Short answer**\n- Licences set the limit.\n\nMore text here."


class SplitShortAnswerTests(unittest.TestCase):
    def test_norwegian_label_with_bullets(self) -> None:
        short, rest = feedback.split_short_answer(KORT)
        self.assertEqual("**Kort svar**\n- Lisensene setter grensen.\n- Kommunene peker ut sjøen.", short)
        self.assertEqual(LONG_REST, rest)

    def test_english_label(self) -> None:
        short, rest = feedback.split_short_answer(SHORT_EN)
        self.assertEqual("**Short answer**\n- Licences set the limit.", short)
        self.assertEqual("More text here.", rest)

    def test_no_label_returns_text_unchanged(self) -> None:
        text = "Det er 13 produksjonsområder.\n\n- ikke en kort blokk"
        self.assertEqual(("", text), feedback.split_short_answer(text))
        self.assertEqual(("", ""), feedback.split_short_answer(""))

    def test_leading_whitespace_is_ignored(self) -> None:
        short, rest = feedback.split_short_answer("\n  **Kort svar**\n* a\n* b\nResten")
        self.assertEqual("**Kort svar**\n* a\n* b", short)
        self.assertEqual("Resten", rest)

    def test_blank_line_between_label_and_bullets(self) -> None:
        short, rest = feedback.split_short_answer("**Kort svar**\n\n- a\n- b\n\nResten her.")
        self.assertEqual("**Kort svar**\n- a\n- b", short)
        self.assertEqual("Resten her.", rest)

    def test_numbered_bullets(self) -> None:
        short, rest = feedback.split_short_answer("**Kort svar**\n1. første\n2. andre\n\nResten.")
        self.assertEqual("**Kort svar**\n1. første\n2. andre", short)
        self.assertEqual("Resten.", rest)

    def test_ends_at_first_non_bullet_line(self) -> None:
        short, rest = feedback.split_short_answer("**Kort svar**\n- a\nVidere tekst uten blank linje.\n\nMer.")
        self.assertEqual("**Kort svar**\n- a", short)
        self.assertEqual("Videre tekst uten blank linje.\n\nMer.", rest)

    def test_label_without_bullets_is_not_a_short_block(self) -> None:
        text = "**Kort svar**\nBare tekst."
        self.assertEqual(("", text), feedback.split_short_answer(text))

    def test_label_and_bullets_only(self) -> None:
        self.assertEqual(("**Kort svar**\n- a", ""), feedback.split_short_answer("**Kort svar**\n- a"))


class AnswerShapeTests(unittest.TestCase):
    def test_features_and_order(self) -> None:
        self.assertEqual("", feedback.answer_shape(""))
        self.assertEqual("", feedback.answer_shape("  \n "))
        self.assertEqual("plain", feedback.answer_shape("Bare tekst."))
        self.assertEqual("kort_svar", feedback.answer_shape(KORT))
        self.assertEqual("steps", feedback.answer_shape("Slik gjør du:\n1. Søk\n2. Vent"))
        self.assertEqual("table", feedback.answer_shape("Oversikt:\n| a | b |\n|---|---|\n| 1 | 2 |"))
        full = "**Kort svar**\n- a\n\nIntro\n1. Søk\n2. Vent\n\n| a | b |\n|---|---|"
        self.assertEqual("kort_svar,steps,table", feedback.answer_shape(full))
        self.assertEqual("steps,table", feedback.answer_shape("1. a\n\n| a | b |"))

    def test_numbered_short_block_is_not_steps(self) -> None:
        self.assertEqual("kort_svar", feedback.answer_shape("**Kort svar**\n1. a\n2. b\n\nProsa."))


class PayloadTests(unittest.TestCase):
    ANSWER = dict(session_id="s", answer_id="a", question="q", mode="researcher", language="no", model="m",
                  top_k=10, n_active_docs=5, retrieved=["d1"], latency_s=1.0, cached=False)

    def test_answer_payload_appends_words_and_shape(self) -> None:
        p = feedback.build_answer_payload(**self.ANSWER, answer=KORT)
        self.assertEqual(
            ["type", "ts", "session_id", "answer_id", "room", "question", "mode", "language", "model", "top_k",
             "n_active_docs", "retrieved", "answer", "latency_s", "cached", "error", "answer_words", "answer_shape"],
            list(p),
        )
        self.assertEqual(len(KORT.split()), p["answer_words"])
        self.assertIsInstance(p["answer_words"], int)
        self.assertEqual("kort_svar", p["answer_shape"])
        empty = feedback.build_answer_payload(**self.ANSWER, answer="", error="x")
        self.assertEqual((0, ""), (empty["answer_words"], empty["answer_shape"]))

    def test_rating_payload_appends_length_and_readability(self) -> None:
        p = feedback.build_rating_payload(session_id="s", answer_id="a")
        self.assertEqual(
            ["type", "ts", "session_id", "answer_id", "thumbs", "answered_question", "fair_disagreement",
             "comment", "length", "readability"],
            list(p),
        )
        self.assertEqual(("", ""), (p["length"], p["readability"]))
        p = feedback.build_rating_payload(session_id="s", answer_id="a", length="passe", readability="delvis")
        self.assertEqual(("passe", "delvis"), (p["length"], p["readability"]))


class _PageCase(unittest.TestCase):
    pieces = (KORT,)

    def setUp(self) -> None:
        from streamlit.testing.v1 import AppTest

        self.AppTest = AppTest
        self.sent: list[dict] = []
        self.store = ({}, threading.Lock())
        outer = self

        class Completions:
            def create(self, **kwargs):
                return iter(
                    [SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=piece))])
                     for piece in outer.pieces]
                )

        class FakeOpenAI:
            def __init__(self, **kwargs):
                self.chat = SimpleNamespace(completions=Completions())

        patches = [
            mock.patch("dotenv.load_dotenv", lambda *a, **k: False),
            mock.patch("streamlit.page_link", lambda *a, **k: None),
            mock.patch("openai.OpenAI", FakeOpenAI),
            mock.patch("retrieval.retrieve", lambda client, query, **kw: list(RESULTS)),
            mock.patch.object(feedback, "send_async", lambda payload, url=None: self.sent.append(payload)),
            mock.patch.object(feedback, "_answer_cache", lambda: self.store),
            mock.patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-not-real"}),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        os.environ.pop("FEEDBACK_WEBHOOK_URL", None)

    def app(self):
        return self.AppTest.from_file(PAGE, default_timeout=120)

    @staticmethod
    def set_radio(at, label, value):
        next(r for r in at.main.radio if r.label == label).set_value(value)

    def ask(self, at, question="Hva begrenser vekst i havbruk?"):
        at.text_area[0].set_value(question)
        next(b for b in at.button if b.label in ("Spør kildene", "Ask the sources")).click()
        at.run()

    def non_specialist_session(self, lang="no"):
        at = self.app().run()
        if lang == "en":
            self.set_radio(at, "Språk / Language", "en")
            at.run()
        self.set_radio(at, "Choose your background" if lang == "en" else "Velg bakgrunn", "non_researcher")
        at.run()
        return at

    @staticmethod
    def full_answer_expanders(at):
        return [e for e in at.main.expander if e.label.startswith(("Les hele svaret", "Read the full answer"))]

    @staticmethod
    def md(container):
        return [m.value for m in container.markdown]


class BackgroundPanelAndMapTests(_PageCase):
    def test_a_and_b_are_two_separate_collapsed_expanders_in_both_languages(self) -> None:
        at = self.app().run()
        self.assertFalse(at.exception, at.exception)
        labels = [e.label for e in at.main.expander]
        self.assertFalse([x for x in labels if x.startswith("Bakgrunn")], "the shared background panel is gone")
        panel_a = next(e for e in at.main.expander if e.label == "A · Introduksjon")
        panel_b = next(e for e in at.main.expander if e.label == "B · Norsk rammeverk")
        self.assertFalse(panel_a.proto.expanded)
        self.assertFalse(panel_b.proto.expanded)
        inside_a, inside_b = " ".join(self.md(panel_a)), " ".join(self.md(panel_b))
        self.assertIn("Merdareal", inside_a)
        self.assertNotIn("lovdata.no", inside_a)
        self.assertIn("lovdata.no", inside_b)
        self.assertNotIn("Merdareal", inside_b)
        inside_values = set(self.md(panel_a)) | set(self.md(panel_b))
        outside = " ".join(m.value for m in at.main.markdown if m.value not in inside_values)
        self.assertIn("C · Spør kildene", outside)
        self.assertNotIn("C · Åpne spørsmål", outside)
        self.assertNotIn("D · Spør kildene", outside)
        # The inner «Les mer» expanders still exist (nested).
        self.assertTrue([e for e in at.main.expander if e.label == "Les mer"])

        self.set_radio(at, "Språk / Language", "en")
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertEqual("A · Introduction", next(e for e in at.main.expander if e.label.startswith("A ·")).label)
        self.assertEqual(
            "B · The Norwegian framework", next(e for e in at.main.expander if e.label.startswith("B ·")).label
        )
        self.assertFalse([e for e in at.main.expander if e.label.startswith("Background")])

    def test_new_map_is_shown_with_caption(self) -> None:
        at = self.app().run()
        images = at.get("imgs")
        self.assertEqual(1, len(images))
        self.assertTrue(images[0].proto.imgs[0].url)
        self.assertEqual(
            "Havbruk og andre interesser langs kysten. Kilder står i kartet.", images[0].proto.imgs[0].caption
        )
        self.assertTrue((REPO / "mockup" / "figur-havbruk-og-areal.jpg").exists())
        self.assertNotIn("arealbruk-snl", Path(PAGE).read_text(encoding="utf-8"))


class FullAnswerViewTests(_PageCase):
    def test_non_specialist_gets_short_block_and_folded_rest_streaming_and_rerun(self) -> None:
        at = self.non_specialist_session()
        self.ask(at)
        self.assertFalse(at.exception, at.exception)
        for run_label in ("streaming run", "rerun"):
            with self.subTest(run_label):
                self.assertEqual("non_researcher", at.session_state["areal_last"]["mode"])
                exps = self.full_answer_expanders(at)
                self.assertEqual(1, len(exps))
                self.assertEqual("Les hele svaret (ca. 120 ord)", exps[0].label)
                self.assertFalse(exps[0].proto.expanded)
                self.assertIn(LONG_REST, self.md(exps[0]))
                main_md = self.md(at.main)
                self.assertEqual(1, sum("Kommunene peker ut sjøen" in m for m in main_md))
                self.assertEqual(1, sum(LONG_REST in m for m in main_md), "long text rendered twice")
                self.assertFalse([m for m in main_md if m == KORT], "whole text must not be shown")
            at.run()
            self.assertFalse(at.exception, at.exception)

    def test_english_label_and_rounding(self) -> None:
        self.pieces = ("**Short answer**\n- a\n\n" + " ".join(["w"] * 84),)
        at = self.non_specialist_session("en")
        self.ask(at)
        self.assertFalse(at.exception, at.exception)
        self.assertEqual(["Read the full answer (about 80 words)"], [e.label for e in self.full_answer_expanders(at)])

    def test_researcher_mode_shows_whole_text_without_expander(self) -> None:
        at = self.app().run()
        self.ask(at)
        self.assertFalse(at.exception, at.exception)
        self.assertEqual([], self.full_answer_expanders(at))
        self.assertEqual(1, sum(m == KORT for m in self.md(at.main)))
        at.run()
        self.assertEqual([], self.full_answer_expanders(at))
        self.assertEqual(1, sum(m == KORT for m in self.md(at.main)))

    def test_non_specialist_without_label_or_with_short_rest_shows_whole_text(self) -> None:
        for answer in ("Det er 13 produksjonsområder.", "**Kort svar**\n- a\n\nBare noen få ord."):
            with self.subTest(answer=answer):
                self.pieces = (answer,)
                at = self.non_specialist_session()
                self.ask(at, f"spørsmål {answer[:10]}")
                self.assertFalse(at.exception, at.exception)
                self.assertEqual([], self.full_answer_expanders(at))
                self.assertEqual(1, sum(m == answer for m in self.md(at.main)))

    def test_cache_hit_folds_too(self) -> None:
        first = self.non_specialist_session()
        self.ask(first)
        other = self.non_specialist_session()
        self.ask(other)
        self.assertFalse(other.exception, other.exception)
        self.assertTrue(other.session_state["areal_last"]["cached"])
        self.assertEqual(1, len(self.full_answer_expanders(other)))

    def test_mode_switch_after_answer_keeps_the_generated_mode(self) -> None:
        at = self.non_specialist_session()
        self.ask(at)
        self.set_radio(at, "Velg bakgrunn", "researcher")
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertEqual(1, len(self.full_answer_expanders(at)))

    def test_answer_row_logs_words_and_shape(self) -> None:
        at = self.app().run()
        self.ask(at)
        row = [p for p in self.sent if p["type"] == "answer"][0]
        self.assertEqual(len(KORT.split()), row["answer_words"])
        self.assertEqual("kort_svar", row["answer_shape"])


class RatingFormTests(_PageCase):
    def test_form_has_length_and_readability_radios_and_logs_them(self) -> None:
        at = self.app().run()
        self.ask(at)
        answer_id = at.session_state["areal_last"]["answer_id"]
        length = at.radio(key=f"areal_length_{answer_id}")
        readable = at.radio(key=f"areal_readable_{answer_id}")
        self.assertEqual("Var lengden passe?", length.label)
        self.assertEqual(["For kort", "Passe", "For lang"], list(length.options))
        self.assertEqual("Var svaret lett å lese?", readable.label)
        self.assertEqual(["Ja", "Delvis", "Nei"], list(readable.options))
        self.assertIsNone(length.value)
        self.assertIsNone(readable.value)
        length.set_value("for_lang")
        readable.set_value("delvis")
        next(b for b in at.button if b.label == "Send tilbakemelding").click()
        at.run()
        self.assertFalse(at.exception, at.exception)
        rating = [p for p in self.sent if p["type"] == "rating"][0]
        self.assertEqual(("for_lang", "delvis"), (rating["length"], rating["readability"]))
        self.assertEqual("", rating["answered_question"])

    def test_unanswered_new_questions_log_empty_strings_in_english(self) -> None:
        at = self.app().run()
        self.set_radio(at, "Språk / Language", "en")
        at.run()
        self.ask(at)
        answer_id = at.session_state["areal_last"]["answer_id"]
        self.assertEqual(
            ["Too short", "About right", "Too long"], list(at.radio(key=f"areal_length_{answer_id}").options)
        )
        self.assertEqual("Was the answer easy to read?", at.radio(key=f"areal_readable_{answer_id}").label)
        next(b for b in at.button if b.label == "Send feedback").click()
        at.run()
        rating = [p for p in self.sent if p["type"] == "rating"][0]
        self.assertEqual(("", ""), (rating["length"], rating["readability"]))


if __name__ == "__main__":
    unittest.main()
