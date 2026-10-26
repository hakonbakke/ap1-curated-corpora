"""Short-answer split, answer-shape logging, the background panel, the new map, the
folded «Les hele svaret» view and the two extra rating questions.

Nothing here calls OpenAI or the webhook: dotenv loading, page_link, the OpenAI client,
retrieval and the webhook sender are replaced.
"""

from __future__ import annotations

import os
import sys
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
        self.assertEqual("sections", feedback.answer_shape("Svar.\n\n### Hva bestemmer\nTekst.\n\n### Hvordan avveies\nTekst."))

    def test_numbered_short_block_is_not_steps(self) -> None:
        self.assertEqual("kort_svar", feedback.answer_shape("**Kort svar**\n1. a\n2. b\n\nProsa."))


class PayloadTests(unittest.TestCase):
    ANSWER = dict(session_id="s", answer_id="a", question="q", mode="researcher", language="no", model="m",
                  top_k=10, n_active_docs=5, retrieved=["d1"], latency_s=1.0, cached=False)

    def test_answer_payload_appends_words_and_shape(self) -> None:
        p = feedback.build_answer_payload(**self.ANSWER, answer=KORT)
        self.assertEqual(
            ["type", "ts", "session_id", "answer_id", "room", "question", "mode", "language", "model", "top_k",
             "n_active_docs", "retrieved", "answer", "latency_s", "cached", "error", "answer_words", "answer_shape", "routed_pq"],
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
        self.api_calls = 0
        outer = self

        class Completions:
            def create(self, **kwargs):
                outer.api_calls += 1
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
            mock.patch("routing.retrieve_funnel", lambda client, query, codes, **kw: list(RESULTS)),
            mock.patch("routing.classify_pq", lambda client, query, pq_texts: []),
            mock.patch.object(feedback, "send_async", lambda payload, url=None: self.sent.append(payload)),
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
    def test_whole_answer_is_shown_open_in_both_modes_streaming_and_rerun(self) -> None:
        for mode_session in ("non_specialist", "researcher"):
            with self.subTest(mode_session):
                at = self.non_specialist_session() if mode_session == "non_specialist" else self.app().run()
                self.ask(at, f"spørsmål {mode_session}")
                self.assertFalse(at.exception, at.exception)
                for _ in range(2):  # the streaming run, then a rerun from session state
                    self.assertEqual([], self.full_answer_expanders(at))
                    self.assertEqual(1, sum(m == KORT for m in self.md(at.main)))
                    at.run()
                    self.assertFalse(at.exception, at.exception)

    def test_english_answer_is_not_folded(self) -> None:
        self.pieces = ("**Short answer**\n- a\n\n" + " ".join(["w"] * 84),)
        at = self.non_specialist_session("en")
        self.ask(at)
        self.assertFalse(at.exception, at.exception)
        self.assertEqual([], self.full_answer_expanders(at))
        self.assertEqual(1, sum(m == self.pieces[0] for m in self.md(at.main)))

    def test_cache_hit_shows_the_whole_answer_too(self) -> None:
        # The cache is per session: the same participant asking again gets the hit.
        at = self.non_specialist_session()
        self.ask(at)
        self.assertEqual(1, self.api_calls)
        self.ask(at)
        self.assertFalse(at.exception, at.exception)
        self.assertEqual(1, self.api_calls)
        self.assertTrue(at.session_state["areal_last"]["cached"])
        self.assertEqual([], self.full_answer_expanders(at))
        self.assertEqual(1, sum(m == KORT for m in self.md(at.main)))

    def test_other_session_gets_a_fresh_answer_not_the_cached_one(self) -> None:
        first = self.non_specialist_session()
        self.ask(first)
        other = self.non_specialist_session()
        self.ask(other)
        self.assertFalse(other.exception, other.exception)
        self.assertEqual(2, self.api_calls)
        self.assertFalse(other.session_state["areal_last"]["cached"])
        self.assertEqual(1, sum(m == KORT for m in self.md(other.main)))

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


class SessionHistoryTests(_PageCase):
    def history_expanders(self, at):
        return [e for e in at.main.expander if e.label.startswith("Første") or e.label.startswith("Andre")]

    def test_a_new_question_keeps_the_old_answer_folded_below(self) -> None:
        at = self.app().run()
        self.ask(at, "Første spørsmål?")
        first_id = at.session_state["areal_last"]["answer_id"]
        self.assertNotIn("areal_history", at.session_state)
        self.ask(at, "Andre spørsmål?")
        self.assertFalse(at.exception, at.exception)
        self.assertEqual(2, self.api_calls)
        history = at.session_state["areal_history"]
        self.assertEqual(["Første spørsmål?"], [h["query"] for h in history])
        self.assertEqual("Andre spørsmål?", at.session_state["areal_last"]["query"])
        self.assertIn("Tidligere svar i denne økten (1)", [s.value for s in at.subheader])
        folded = self.history_expanders(at)
        self.assertEqual(["Første spørsmål?"], [e.label for e in folded])
        self.assertFalse(folded[0].proto.expanded)
        self.assertIn(KORT, self.md(folded[0]))
        # The old answer keeps its own rating form.
        self.assertEqual("Var lengden passe?", at.radio(key=f"areal_length_{first_id}").label)
        at.run()  # a plain rerun keeps both
        self.assertEqual(2, sum(m == KORT for m in self.md(at.main)))

    def test_newest_earlier_answer_comes_first(self) -> None:
        at = self.app().run()
        for q in ("Første a?", "Første b?", "Første c?"):
            self.ask(at, q)
        self.assertEqual(["Første b?", "Første a?"], [h["query"] for h in at.session_state["areal_history"]])
        self.assertEqual(["Første b?", "Første a?"], [e.label for e in self.history_expanders(at)])

    def test_same_question_again_does_not_duplicate(self) -> None:
        at = self.app().run()
        self.ask(at, "Første spørsmål?")
        self.ask(at, "Første spørsmål?")
        self.assertFalse(at.exception, at.exception)
        self.assertEqual([], at.session_state["areal_history"] if "areal_history" in at.session_state else [])
        self.assertEqual(1, sum(m == KORT for m in self.md(at.main)))

    def test_rating_an_earlier_answer_logs_its_own_id(self) -> None:
        at = self.app().run()
        self.ask(at, "Første spørsmål?")
        first_id = at.session_state["areal_last"]["answer_id"]
        self.ask(at, "Andre spørsmål?")
        at.radio(key=f"areal_readable_{first_id}").set_value("ja")
        form_buttons = [b for b in at.button if b.label == "Send tilbakemelding"]
        self.assertEqual(2, len(form_buttons))
        form_buttons[-1].click()  # the history form sits below the current answer
        at.run()
        self.assertFalse(at.exception, at.exception)
        rating = [p for p in self.sent if p["type"] == "rating"][0]
        self.assertEqual((first_id, "ja"), (rating["answer_id"], rating["readability"]))

    def test_history_heading_in_english(self) -> None:
        at = self.app().run()
        self.set_radio(at, "Språk / Language", "en")
        at.run()
        self.ask(at, "Første q?")
        self.ask(at, "Andre q?")
        self.assertIn("Earlier answers in this session (1)", [s.value for s in at.subheader])

    def test_css_covers_history_answers(self) -> None:
        import ui

        self.assertIn('[class*="st-key-areal_hist_answer_"] h3', ui._BASE_CSS)


HEADED = (
    "Innledning om saken.\n\n### Første overskrift\n\nTekst under første.\n\n"
    "### Andre overskrift\n\nTekst under andre."
)


def _source(doc_id, authors, year, title):
    return {"doc_id": doc_id, "authors": authors, "year": year, "title": title, "semantic_score": 0.8,
            "score": 0.8, "rag_summary": "x", "evidence_direction": "not_applicable", "quality_signal": "medium"}


TWO_AUTHORS = _source("2025_osmundsen", "Tonje C. Osmundsen; Marit Schei Olsen", 2025, "Søknadsprosessen")
THREE_AUTHORS = _source("2014_robertsen", "Rolf Robertsen; Anne Hansen; Per Berg", 2014, "Kystsoneplaner")
ONE_AUTHOR = _source("2018_myklebust", "Vibeke Myklebust", 2018, "Kommunale vilkår")


def _texts(*roots):
    """All visible text (markdown, captions, headings, labels) below the given roots."""
    out = []

    def walk(node):
        for child in node.children.values():
            for attr in ("value", "label"):
                v = getattr(child, attr, None)
                if isinstance(v, str):
                    out.append(v)
            if hasattr(child, "children"):
                walk(child)

    for root in roots:
        walk(root)
    return out


def _answer_blocks(at):
    """The keyed `areal_answer_text` containers on the page."""
    found = []

    def walk(node):
        for child in node.children.values():
            if str(getattr(getattr(child, "proto", None), "id", "")).endswith("-areal_answer_text"):
                found.append(child)
            if hasattr(child, "children"):
                walk(child)

    walk(at.main)
    return found


class AnswerPresentationTests(_PageCase):
    pieces = (HEADED,)

    def english(self):
        at = self.app().run()
        self.set_radio(at, "Språk / Language", "en")
        at.run()
        return at

    def test_answer_text_sits_in_the_keyed_container_streaming_rerun_and_cache_hit(self) -> None:
        at = self.app().run()
        self.ask(at)  # the streaming run
        for step in ("stream", "rerun", "cache hit"):
            with self.subTest(step):
                if step == "rerun":
                    at.run()
                elif step == "cache hit":
                    self.ask(at)
                    self.assertTrue(at.session_state["areal_last"]["cached"])
                self.assertFalse(at.exception, at.exception)
                blocks = _answer_blocks(at)
                self.assertEqual(1, len(blocks), "exactly one keyed answer container")
                self.assertEqual([HEADED], [m.value for m in blocks[0].markdown])
                # The answer is not also rendered outside the container.
                self.assertEqual(1, sum(m == HEADED for m in self.md(at.main)))
        self.assertEqual(1, self.api_calls)

    def test_answer_heading_is_syntese_and_synthesis(self) -> None:
        at = self.app().run()
        self.ask(at)
        self.assertEqual(["Syntese"], [s.value for s in at.subheader if s.value in ("Svar", "Syntese")])
        en = self.english()
        self.ask(en)
        self.assertEqual(["Synthesis"], [s.value for s in en.subheader if s.value in ("Answer", "Synthesis")])

    def test_css_sets_in_text_headings_to_body_size(self) -> None:
        import ui

        css = ui._BASE_CSS
        for tag in ("h1", "h2", "h3", "h4"):
            self.assertIn(f".st-key-areal_answer_text {tag}", css)
        self.assertIn("font-size:1rem; font-weight:700;", css)
        self.assertIn("margin:1rem 0 .25rem", css)
        self.assertIn('.st-key-areal_answer_text [data-testid="stHeaderActionElements"]', css)

    def test_feedback_heading_and_primary_submit_in_both_languages(self) -> None:
        for lang, heading, button in (
            ("no", "**Hjelp oss: hvordan var svaret?**", "Send tilbakemelding"),
            ("en", "**Help us: how was this answer?**", "Send feedback"),
        ):
            with self.subTest(lang):
                at = self.app().run() if lang == "no" else self.english()
                self.ask(at)
                self.assertFalse(at.exception, at.exception)
                self.assertIn(heading, self.md(at.main))
                self.assertNotIn("Din tilbakemelding på dette svaret", " ".join(self.md(at.main)))
                submit = next(b for b in at.button if b.label == button)
                self.assertEqual("primary", submit.proto.type)

    def test_source_labels_use_the_readable_label(self) -> None:
        cases = (
            ("no", ["**Osmundsen og Olsen 2025** · Søknadsprosessen", "**Robertsen mfl. 2014** · Kystsoneplaner",
                    "**Myklebust 2018** · Kommunale vilkår"]),
            ("en", ["**Osmundsen and Olsen 2025** · Søknadsprosessen", "**Robertsen et al. 2014** · Kystsoneplaner",
                    "**Myklebust 2018** · Kommunale vilkår"]),
        )
        results = [TWO_AUTHORS, THREE_AUTHORS, ONE_AUTHOR]
        with mock.patch("routing.retrieve_funnel", lambda client, query, codes, **kw: list(results)):
            for lang, expected in cases:
                with self.subTest(lang):
                    at = self.app().run() if lang == "no" else self.english()
                    self.ask(at)
                    self.assertFalse(at.exception, at.exception)
                    for _ in range(2):  # the streaming run, then a rerun from session state
                        labels = [e.label for e in at.main.expander]
                        for label in expected:
                            self.assertIn(label, labels)
                        at.run()


class PrototypeWordingTests(_PageCase):
    def test_no_utkast_or_draft_in_visible_areal_text(self) -> None:
        for lang in ("no", "en"):
            with self.subTest(lang):
                at = self.app().run()
                if lang == "en":
                    self.set_radio(at, "Språk / Language", "en")
                    at.run()
                self.ask(at)
                self.assertFalse(at.exception, at.exception)
                text = " ".join(_texts(at.main, at.sidebar)).lower()
                self.assertNotIn("utkast", text)
                self.assertNotIn("draft", text)
        at = self.app().run()
        self.assertIn("prototype-rom", " ".join(c.value for c in at.sidebar.caption))
        self.assertIn("Prototype-rom om areal og havbruk", " ".join(self.md(at.main)))

    def test_stats_box_shows_the_full_review_date_and_hero_caption_is_gone(self) -> None:
        for lang, label in (("no", "sist gjennomgått"), ("en", "last reviewed")):
            with self.subTest(lang):
                at = self.app().run()
                if lang == "en":
                    self.set_radio(at, "Språk / Language", "en")
                    at.run()
                stats = next(m for m in self.md(at.main) if '<div class="hl-stats">' in m)
                self.assertIn(f"<strong>19.10.2026</strong><span>{label}</span>", stats)
                self.assertNotIn("<strong>19.10</strong>", stats)
                captions = " ".join(c.value for c in at.main.caption)
                self.assertNotIn("A og B ligger", captions)
                self.assertNotIn("A and B sit", captions)

    def test_sidebar_starts_collapsed(self) -> None:
        self.assertIn('initial_sidebar_state="collapsed"', Path(PAGE).read_text(encoding="utf-8"))

    def test_home_page_calls_the_areal_card_prototype(self) -> None:
        at = self.AppTest.from_file(str(REPO / "app" / "app.py"), default_timeout=120).run()
        self.assertFalse(at.exception, at.exception)
        html = " ".join(self.md(at.main))
        self.assertIn('<span class="hl-status hl-status-on">Prototype</span>', html)
        self.assertIn('<div class="hl-room-meta">50 dokumenter · prototype</div>', html)
        self.assertNotIn("tkast", html)


if __name__ == "__main__":
    unittest.main()
