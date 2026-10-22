"""The open-question cards in section C of the Areal room, and the own-question box.

Nothing here calls OpenAI or the webhook: dotenv loading, page_link, the OpenAI client,
retrieval and the webhook sender are replaced (see _PageCase in test_areal_answer_view).
"""

from __future__ import annotations

import ast
import sys
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "app"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from areal_questions import GROUPS  # noqa: E402
from test_areal_answer_view import KORT, RESULTS, PAGE, _PageCase  # noqa: E402


def _faults() -> dict:
    """FAULTS lives in the page script, so read the literal from its source."""
    tree = ast.parse(Path(PAGE).read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "FAULTS":
            return ast.literal_eval(node.value)
    raise AssertionError("FAULTS not found in the page")


FAULTS = _faults()
CARD_ORDER = [c["n"] for g in GROUPS for c in g["cards"]]  # 1, 2, 8, 3, 5, 7, 4, 6, 9
ASK = {"no": "Spør kildene om dette", "en": "Ask the sources about this"}
GROUP_TITLE = {"no": "title_no", "en": "title_en"}


class _CardCase(_PageCase):
    def setUp(self) -> None:
        super().setUp()
        self.queries: list[str] = []
        outer = self

        def recording_retrieve(client, query, **kwargs):
            outer.queries.append(query)
            return list(RESULTS)

        p = mock.patch("retrieval.retrieve", recording_retrieve)
        p.start()
        self.addCleanup(p.stop)

    def in_lang(self, lang):
        at = self.app().run()
        if lang == "en":
            self.set_radio(at, "Språk / Language", "en")
            at.run()
        self.assertFalse(at.exception, at.exception)
        return at

    @staticmethod
    def card_buttons(at):
        return [b for b in at.main.button if b.key and b.key.startswith("areal_card_")]

    def answer_rows(self):
        return [p for p in self.sent if p["type"] == "answer"]


class CardLayoutTests(_CardCase):
    def test_content_module_covers_questions_one_to_nine_once(self) -> None:
        self.assertEqual(list(range(1, 10)), sorted(CARD_ORDER))
        self.assertEqual(3, len(GROUPS))
        self.assertTrue(all(len(g["cards"]) == 3 for g in GROUPS))

    def test_nine_card_buttons_in_three_groups_in_both_languages(self) -> None:
        for lang in ("no", "en"):
            with self.subTest(lang):
                at = self.in_lang(lang)
                buttons = self.card_buttons(at)
                self.assertEqual(9, len(buttons))
                self.assertEqual([f"areal_card_{lang}_{n}" for n in CARD_ORDER], [b.key for b in buttons])
                self.assertEqual({ASK[lang]}, {b.label for b in buttons})
                # Three groups: one heading each, and the three cards of a group share one st.columns row.
                md = self.md(at.main)
                for g in GROUPS:
                    self.assertEqual(
                        1, sum(f'<div class="hl-group-title">{g[GROUP_TITLE[lang]]}</div>' == m for m in md)
                    )
                rows = [c for c in at.columns if len(c.button) == 1 and (c.button[0].key or "").startswith("areal_card_")]
                self.assertEqual(9, len(rows))
                self.assertEqual(
                    [[f"areal_card_{lang}_{n}" for n in (g["cards"][i]["n"] for i in range(3))] for g in GROUPS],
                    [[c.button[0].key for c in rows[i : i + 3]] for i in (0, 3, 6)],
                )

    def test_card_shows_title_intro_points_with_readable_sources_open_line_and_read_more(self) -> None:
        at = self.in_lang("no")
        md = " ".join(self.md(at.main))
        card = GROUPS[0]["cards"][0]
        self.assertIn(f'<div class="hl-card-title">{card["title_no"]}</div>', md)
        self.assertIn(card["intro"]["no"], [c.value for c in at.caption])
        self.assertIn(
            f"- {card['points'][0]['no']} · :gray[*Hersoug mfl. 2020*]", md
        )
        self.assertIn(f"**Åpent:** {card['open_no']}", md)
        self.assertNotIn("2020_hersoug_whats-the-clue", md)
        # Every point carries at least one readable source name.
        for g in GROUPS:
            for c in g["cards"]:
                for p in c["points"]:
                    self.assertIn(f"- {p['no']} · :gray[*", md)
        read_more = [e for e in at.main.expander if e.label == "Les mer" and FAULTS["no"][0][1] in " ".join(self.md(e))]
        self.assertEqual(1, len(read_more))
        self.assertFalse(read_more[0].proto.expanded)

    def test_english_card_text(self) -> None:
        at = self.in_lang("en")
        md = " ".join(self.md(at.main))
        card = GROUPS[0]["cards"][0]
        self.assertIn(f"- {card['points'][0]['en']} · :gray[*Hersoug et al. 2020*]", md)
        self.assertIn(f"**Open:** {card['open_en']}", md)
        self.assertTrue([e for e in at.main.expander if e.label == "Read more" and FAULTS["en"][8][1] in " ".join(self.md(e))])

    def test_old_c_and_d_structure_and_example_selectbox_are_gone(self) -> None:
        for lang in ("no", "en"):
            with self.subTest(lang):
                at = self.in_lang(lang)
                self.assertEqual([], list(at.selectbox))
                self.assertEqual([], [b for b in at.button if b.label in ("Spør kildene om dette ↓", "Ask the sources about this ↓")])
                for key in at.session_state.filtered_state:
                    self.assertNotIn("areal_example", key)
                    self.assertNotIn("areal_fault", key)
                self.assertNotIn("_areal_example", at.session_state)
                text = " ".join(self.md(at.main) + [c.value for c in at.caption])
                for old in ("C · Åpne spørsmål", "C · Open questions", "D · Spør kildene", "D · Ask the sources", "Eksempelspørsmål"):
                    self.assertNotIn(old, text)
        at = self.in_lang("no")
        self.assertIn("Velg et åpent spørsmål, eller skriv ditt eget nederst.", self.md(at.main))

    def test_audience_radio_sits_before_the_cards_and_own_question_after(self) -> None:
        at = self.in_lang("no")
        src = Path(PAGE).read_text(encoding="utf-8")
        self.assertLess(src.index("mode = st.radio("), src.index("for group in GROUPS:"))
        self.assertLess(src.index("for group in GROUPS:"), src.index("query = st.text_area("))
        self.assertEqual(["Velg bakgrunn"], [r.label for r in at.main.radio if r.label == "Velg bakgrunn"])
        self.assertEqual(1, len(at.text_area))
        self.assertTrue(any("Ditt eget spørsmål" in m for m in self.md(at.main)))


class CardClickTests(_CardCase):
    def test_click_asks_exactly_the_full_question_once_and_answers_below_in_both_languages(self) -> None:
        for lang, n in (("no", 3), ("en", 7)):
            with self.subTest(lang=lang, n=n):
                self.queries.clear()
                at = self.in_lang(lang)
                self.assertEqual([], at.get("iframe"))
                at.button(key=f"areal_card_{lang}_{n}").click()
                at.run()
                self.assertFalse(at.exception, at.exception)
                question = FAULTS[lang][n - 1][2]
                self.assertEqual([question], self.queries)
                self.assertEqual(question, at.text_area[0].value)
                self.assertEqual(question, at.session_state["areal_query"])
                last = at.session_state["areal_last"]
                self.assertEqual((question, lang), (last["query"], last["lang"]))
                # The answer sits in the answer area, not in any card column.
                self.assertEqual(1, sum(m == KORT for m in self.md(at.main)))
                self.assertFalse([c for c in at.columns if KORT in self.md(c)])
                self.assertTrue([s for s in at.subheader if s.value in ("Syntese", "Synthesis")])
                # Feedback form and sources follow the answer, as for the Synthesise button.
                self.assertTrue([b for b in at.button if b.label in ("Send tilbakemelding", "Send feedback")])
                self.assertTrue([s for s in at.subheader if s.value.startswith(("Hentede kilder", "Retrieved sources"))])
                # The flag is consumed and the scroll anchor plus script were rendered for this run.
                self.assertNotIn("areal_ask_now", at.session_state)
                self.assertEqual(1, len(at.get("iframe")))
                self.assertTrue([m for m in at.markdown if 'id="areal-answer"' in m.value])
                row = self.answer_rows()[-1]
                self.assertEqual((question, lang), (row["question"], row["language"]))

    def test_a_later_rerun_does_not_ask_again(self) -> None:
        at = self.in_lang("no")
        at.button(key="areal_card_no_1").click()
        at.run()
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertEqual([FAULTS["no"][0][2]], self.queries)
        self.assertEqual(1, len(self.answer_rows()))
        self.assertEqual(1, sum(m == KORT for m in self.md(at.main)))
        self.assertEqual([], at.get("iframe"))  # no scroll on later reruns

    def test_repeat_click_is_served_from_the_cache(self) -> None:
        at = self.in_lang("no")
        at.button(key="areal_card_no_2").click()
        at.run()
        at.button(key="areal_card_no_2").click()
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertEqual([FAULTS["no"][1][2]], self.queries)  # one retrieval, second answer cached
        self.assertEqual([False, True], [r["cached"] for r in self.answer_rows()])

    def test_the_chosen_mode_is_used_by_a_card_click(self) -> None:
        at = self.in_lang("no")
        self.set_radio(at, "Velg bakgrunn", "non_researcher")
        at.run()
        at.button(key="areal_card_no_5").click()
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertEqual("non_researcher", at.session_state["areal_last"]["mode"])
        self.assertEqual("non_researcher", self.answer_rows()[-1]["mode"])
        self.assertEqual("non_researcher", next(r for r in at.main.radio if r.label == "Velg bakgrunn").value)
        self.assertEqual(1, len(self.full_answer_expanders(at)))  # non-specialist view of the answer
        # Back to researcher: the same card now asks in that mode (a new cache entry).
        self.set_radio(at, "Velg bakgrunn", "researcher")
        at.run()
        at.button(key="areal_card_no_5").click()
        at.run()
        self.assertEqual("researcher", self.answer_rows()[-1]["mode"])
        self.assertEqual([False, False], [r["cached"] for r in self.answer_rows()])
        self.assertEqual([], self.full_answer_expanders(at))

    def test_card_click_replaces_an_earlier_answer(self) -> None:
        at = self.in_lang("no")
        at.button(key="areal_card_no_1").click()
        at.run()
        first = at.session_state["areal_last"]["answer_id"]
        at.button(key="areal_card_no_9").click()
        at.run()
        self.assertNotEqual(first, at.session_state["areal_last"]["answer_id"])
        self.assertEqual([FAULTS["no"][0][2], FAULTS["no"][8][2]], self.queries)
        self.assertEqual(1, sum(m == KORT for m in self.md(at.main)))


class OwnQuestionTests(_CardCase):
    def test_text_area_and_synthesise_still_work(self) -> None:
        at = self.in_lang("no")
        self.assertEqual("", at.text_area[0].value)
        self.ask(at, "Hva betyr trafikklyset for areal?")
        self.assertFalse(at.exception, at.exception)
        self.assertEqual(["Hva betyr trafikklyset for areal?"], self.queries)
        self.assertEqual("Hva betyr trafikklyset for areal?", at.session_state["areal_query"])
        self.assertEqual(1, sum(m == KORT for m in self.md(at.main)))
        self.assertEqual([], at.get("iframe"))  # the scroll is only for card clicks
        self.assertIn("Svaret bygger på de", " ".join(c.value for c in at.caption))

    def test_a_card_question_can_be_edited_and_asked_with_synthesise(self) -> None:
        at = self.in_lang("no")
        at.button(key="areal_card_no_4").click()
        at.run()
        self.assertEqual(FAULTS["no"][3][2], at.text_area[0].value)
        at.text_area[0].set_value(FAULTS["no"][3][2] + " I Trøndelag?")
        self.button_by_label(at, "Syntetiser").click()
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertEqual([FAULTS["no"][3][2], FAULTS["no"][3][2] + " I Trøndelag?"], self.queries)
        self.assertNotIn("areal_ask_now", at.session_state)

    @staticmethod
    def button_by_label(at, label):
        return next(b for b in at.button if b.label == label)

    def test_mode_stays_the_chosen_one_for_the_own_question(self) -> None:
        at = self.in_lang("no")
        self.set_radio(at, "Velg bakgrunn", "non_researcher")
        at.run()
        self.ask(at, "Hva er en lokalitet?")
        self.assertEqual("non_researcher", at.session_state["areal_last"]["mode"])
        self.assertEqual("non_researcher", self.answer_rows()[-1]["mode"])


if __name__ == "__main__":
    unittest.main()
