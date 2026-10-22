"""Section C of the Areal room: your own question, the open-question chips and the question box.

Nothing here calls OpenAI or the webhook: dotenv loading, page_link, the OpenAI client,
retrieval and the webhook sender are replaced (see _PageCase in test_areal_answer_view).

The nine open questions are `st.pills` chips, one group per theme. AppTest exposes pills as
`button_group` elements: `select(n)` picks the card with number n; see `unpick` for deselecting.
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
from streamlit.testing.v1.element_tree import ButtonGroup  # noqa: E402
from test_areal_answer_view import KORT, RESULTS, PAGE, _PageCase  # noqa: E402


def _faults() -> dict:
    """FAULTS lives in the page script, so read the literal from its source."""
    tree = ast.parse(Path(PAGE).read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "FAULTS":
            return ast.literal_eval(node.value)
    raise AssertionError("FAULTS not found in the page")


FAULTS = _faults()
CARDS = {c["n"]: c for g in GROUPS for c in g["cards"]}
CARD_ORDER = [c["n"] for g in GROUPS for c in g["cards"]]  # 1, 2, 8, 3, 5, 7, 4, 6, 9
GROUP_OF = {c["n"]: gi for gi, g in enumerate(GROUPS) for c in g["cards"]}
ASK_BUTTON = {"no": "Spør kildene", "en": "Ask the sources"}
OLD_BUTTON = {"no": "Syntetiser", "en": "Synthesise"}
YOUR_Q = {"no": "Spørsmålet ditt", "en": "Your question"}
RADIO = {"no": "Velg bakgrunn", "en": "Choose your background"}
OR_PICK = {"no": "Eller velg et åpent spørsmål:", "en": "Or pick an open question:"}
ASKED = {"no": "Spørsmålet som stilles:", "en": "The question asked:"}
UNRESOLVED = {"no": "Uavklart:", "en": "Unresolved:"}
SYNTHESIS = {"no": "Syntese", "en": "Synthesis"}
READ_MORE = {"no": "Les mer", "en": "Read more"}
TAG = {"no": "Ditt eget spørsmål, eller et åpent", "en": "Your own question, or an open one"}
DRAWS_ON = {"no": "Svaret bygger på de", "en": "The answer draws on the"}
TITLE_OPEN = '<div class="hl-card-title">'
BOX_AFTER_CHIPS = ["chips"] * 3 + ["box_title", "box_question", "unresolved", "synthesis", "answer"]


def flat(node):
    """Every element below `node`, in page order."""
    for child in node.children.values():
        yield child
        if hasattr(child, "children"):
            yield from flat(child)


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
    def chip_groups(at):
        return sorted(
            (g for g in at.get("button_group") if (g.key or "").startswith("areal_chips_")),
            key=lambda g: g.key,
        )

    def pick(self, at, n):
        """Click the chip of card n."""
        next(g for g in self.chip_groups(at) if g.key == f"areal_chips_{GROUP_OF[n]}").select(n)
        at.run()
        self.assertFalse(at.exception, at.exception)

    def unpick(self, at, n):
        """Click the selected chip of card n again (deselect).

        AppTest's ButtonGroup.set_value(None) is a no-op (value falls back to the stored
        state when _value is None), so send the empty selection the browser would send."""
        group = next(g for g in self.chip_groups(at) if g.key == f"areal_chips_{GROUP_OF[n]}")
        self.assertEqual(n, group.value)
        original = ButtonGroup.formatted_values.fget
        group._deselect = True
        with mock.patch.object(
            ButtonGroup,
            "formatted_values",
            property(lambda g: [] if getattr(g, "_deselect", False) else original(g)),
        ):
            at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertIsNone(next(g for g in self.chip_groups(at) if g.key == group.key).value)

    def selected(self, at):
        return [g.value for g in self.chip_groups(at)]

    def answer_rows(self):
        return [p for p in self.sent if p["type"] == "answer"]

    @staticmethod
    def own_button(at, lang):
        return next(b for b in at.main.button if b.label == ASK_BUTTON[lang])

    @staticmethod
    def box_titles(at):
        return [m.value for m in at.main.markdown if m.value.startswith(TITLE_OPEN)]

    def box_read_more(self, at, lang):
        """The «Les mer» expanders of a question box (the A and B panels have their own)."""
        long_texts = [f[1] for f in FAULTS[lang]]
        return [
            e for e in at.main.expander
            if e.label == READ_MORE[lang] and any(t in " ".join(self.md(e)) for t in long_texts)
        ]

    @staticmethod
    def page_order(at):
        """Names of the interesting elements, in page order."""
        out = []
        for el in flat(at.main):
            kind = type(el).__name__
            value = getattr(el, "value", "")
            if kind == "Markdown" and isinstance(value, str) and value.startswith(TITLE_OPEN):
                out.append("box_title")
            elif kind == "Caption" and value.startswith(("**Spørsmålet som stilles:**", "**The question asked:**")):
                out.append("box_question")
            elif kind == "Markdown" and value.startswith(("**Uavklart:**", "**Unresolved:**")):
                out.append("unresolved")
            elif kind == "Subheader" and value in ("Syntese", "Synthesis"):
                out.append("synthesis")
            elif kind == "Markdown" and value == KORT:
                out.append("answer")
            elif kind == "ButtonGroup":
                out.append("chips")
        return out


class SectionLayoutTests(_CardCase):
    def test_content_module_covers_questions_one_to_nine_once(self) -> None:
        self.assertEqual(list(range(1, 10)), sorted(CARD_ORDER))
        self.assertEqual(3, len(GROUPS))
        self.assertTrue(all(len(g["cards"]) == 3 for g in GROUPS))

    def test_three_chip_groups_with_nine_titles_in_both_languages(self) -> None:
        for lang in ("no", "en"):
            with self.subTest(lang):
                at = self.in_lang(lang)
                groups = self.chip_groups(at)
                self.assertEqual(["areal_chips_0", "areal_chips_1", "areal_chips_2"], [g.key for g in groups])
                for g, spec in zip(groups, GROUPS):
                    self.assertEqual([c["title_" + lang] for c in spec["cards"]], g.options)
                    self.assertIsNone(g.value)  # nothing selected before a click
                self.assertEqual(9, sum(len(g.options) for g in groups))
                self.assertEqual([CARDS[n]["title_" + lang] for n in CARD_ORDER], [o for g in groups for o in g.options])
                # One small label per theme group, and the lead-in line.
                md = self.md(at.main)
                for g in GROUPS:
                    self.assertEqual(1, md.count(f'<div class="hl-group-title">{g["title_" + lang]}</div>'))
                self.assertEqual(1, md.count(f"**{OR_PICK[lang]}**"))
                self.assertTrue(any(f">{TAG[lang]}<" in m for m in md))

    def test_the_card_grid_and_its_buttons_are_gone(self) -> None:
        src = Path(PAGE).read_text(encoding="utf-8")
        for gone in ("areal_card_", "_render_card", "zip(st.columns(3)", "SCROLL_TO_ANSWER", "areal-answer", "components.v1"):
            self.assertNotIn(gone, src)
        for lang in ("no", "en"):
            with self.subTest(lang):
                at = self.in_lang(lang)
                self.assertEqual([], [b for b in at.button if (b.key or "").startswith("areal_card_")])
                self.assertEqual([], [b for b in at.button if b.label in ("Spør kildene om dette", "Ask the sources about this")])
                self.assertEqual(1, len([b for b in at.main.button if b.label == ASK_BUTTON[lang]]))
                # No card text at load: no card title, no «Les mer», no old «Åpent:» line.
                self.assertEqual([], self.box_titles(at))
                self.assertEqual([], self.box_read_more(at, lang))
                text = " ".join(self.md(at.main) + [c.value for c in at.caption])
                self.assertNotIn("Åpent:", text)
                self.assertNotIn("**Open:**", text)
                self.assertEqual([], [c for c in at.columns if any((b.key or "").startswith("areal_card_") for b in c.button)])

    def test_old_c_and_d_structure_and_example_selectbox_are_gone(self) -> None:
        for lang in ("no", "en"):
            with self.subTest(lang):
                at = self.in_lang(lang)
                self.assertEqual([], list(at.selectbox))
                for key in at.session_state.filtered_state:
                    self.assertNotIn("areal_example", key)
                    self.assertNotIn("areal_fault", key)
                self.assertNotIn("_areal_example", at.session_state)
                text = " ".join(self.md(at.main) + [c.value for c in at.caption])
                for old in (
                    "C · Åpne spørsmål", "C · Open questions", "D · Spør kildene", "D · Ask the sources",
                    "Eksempelspørsmål", "Velg et åpent spørsmål, eller skriv ditt eget nederst.",
                ):
                    self.assertNotIn(old, text)

    def test_section_order_audience_own_question_chips_answer_caption(self) -> None:
        src = Path(PAGE).read_text(encoding="utf-8")
        order = [
            src.index("mode = st.radio("),
            src.index("query = st.text_area("),
            src.index("run = st.button("),
            src.index("st.pills("),
            src.index('pending = st.session_state.pop("areal_ask_now"'),
            src.index('"Redaksjonell orientering'),
        ]
        self.assertEqual(sorted(order), order)
        for lang in ("no", "en"):
            with self.subTest(lang):
                at = self.in_lang(lang)
                self.assertEqual(1, len(at.text_area))
                self.assertEqual(YOUR_Q[lang], at.text_area[0].label)
                self.assertNotEqual("COLLAPSED", at.text_area[0].proto.label_visibility.value)
                self.assertTrue(at.text_area[0].placeholder)
                self.assertEqual("primary", self.own_button(at, lang).proto.type)
                self.assertEqual([], [b for b in at.main.button if b.label == OLD_BUTTON[lang]])
                self.assertIn(DRAWS_ON[lang], " ".join(c.value for c in at.caption))
                # Element order: audience radio, text area, button, chips.
                labels = [getattr(e, "label", None) for e in flat(at.main)]
                kinds = [type(e).__name__ for e in flat(at.main)]
                self.assertLess(labels.index(RADIO[lang]), labels.index(YOUR_Q[lang]))
                self.assertLess(labels.index(YOUR_Q[lang]), labels.index(ASK_BUTTON[lang]))
                self.assertLess(labels.index(ASK_BUTTON[lang]), kinds.index("ButtonGroup"))
        at = self.in_lang("no")
        self.assertEqual([RADIO["no"]], [r.label for r in at.main.radio if r.label == RADIO["no"]])


class ChipClickTests(_CardCase):
    def test_click_asks_exactly_the_full_question_once_in_both_languages(self) -> None:
        for lang, n in (("no", 3), ("en", 7)):
            with self.subTest(lang=lang, n=n):
                self.queries.clear()
                at = self.in_lang(lang)
                self.pick(at, n)
                question = FAULTS[lang][n - 1][2]
                self.assertEqual([question], self.queries)
                self.assertEqual(question, at.text_area[0].value)
                self.assertEqual(question, at.session_state["areal_query"])
                last = at.session_state["areal_last"]
                self.assertEqual((question, lang, n), (last["query"], last["lang"], last["card_n"]))
                # Only the clicked chip is selected.
                self.assertEqual([n if GROUP_OF[n] == i else None for i in range(3)], self.selected(at))
                # Answer, feedback form and sources follow, as for the own-question button.
                self.assertEqual(1, sum(m == KORT for m in self.md(at.main)))
                self.assertTrue([s for s in at.subheader if s.value == SYNTHESIS[lang]])
                self.assertTrue([b for b in at.button if b.label in ("Send tilbakemelding", "Send feedback")])
                self.assertTrue([s for s in at.subheader if s.value.startswith(("Hentede kilder", "Retrieved sources"))])
                # The flags are consumed. There is no scroll script or anchor any more.
                self.assertNotIn("areal_ask_now", at.session_state)
                self.assertNotIn("areal_ask_card", at.session_state)
                self.assertEqual([], at.get("iframe"))
                self.assertFalse([m for m in at.markdown if 'id="areal-answer"' in m.value])
                row = self.answer_rows()[-1]
                self.assertEqual((question, lang), (row["question"], row["language"]))

    def test_question_box_sits_between_the_chips_and_the_synthesis(self) -> None:
        for lang, n in (("no", 4), ("en", 9)):
            with self.subTest(lang=lang, n=n):
                at = self.in_lang(lang)
                self.pick(at, n)
                card = CARDS[n]
                self.assertEqual(BOX_AFTER_CHIPS, self.page_order(at))
                md = " ".join(self.md(at.main))
                self.assertIn(f'{TITLE_OPEN}{card["title_" + lang]}</div>', md)
                captions = [c.value for c in at.caption]
                self.assertIn(f"**{ASKED[lang]}** {FAULTS[lang][n - 1][2]}", captions)
                self.assertIn(card["intro"][lang], captions)
                self.assertIn(f"**{UNRESOLVED[lang]}** {card['open_' + lang]}", self.md(at.main))
                self.assertNotIn("Åpent:", md)
                self.assertNotIn("**Open:**", md)
                read_more = self.box_read_more(at, lang)
                self.assertEqual(1, len(read_more))
                self.assertFalse(read_more[0].proto.expanded)
                self.assertIn(FAULTS[lang][n - 1][1], " ".join(self.md(read_more[0])))

    def test_question_box_shows_points_with_readable_source_names(self) -> None:
        at = self.in_lang("no")
        self.assertFalse([m for m in self.md(at.main) if "Hersoug mfl. 2020" in m])  # nothing before a click
        self.pick(at, 1)
        md = " ".join(self.md(at.main))
        card = CARDS[1]
        self.assertIn(f"- {card['points'][0]['no']} · :gray[*Hersoug mfl. 2020*]", md)
        self.assertIn("Sandersen og Kvalvik 2015", md)
        self.assertIn("Tveterås 2023", md)
        self.assertNotIn("2020_hersoug_whats-the-clue", md)
        for p in card["points"]:
            self.assertIn(f"- {p['no']} · :gray[*", md)
        at = self.in_lang("en")
        self.pick(at, 1)
        md = " ".join(self.md(at.main))
        self.assertIn(f"- {CARDS[1]['points'][0]['en']} · :gray[*Hersoug et al. 2020*]", md)
        self.assertIn("Sandersen and Kvalvik 2015", md)

    def test_question_box_is_there_before_any_retrieval_result(self) -> None:
        """The box is static text rendered before retrieval and streaming, so it shows
        even when retrieval fails and no answer ever arrives."""
        at = self.in_lang("no")

        def failing(client, query, **kw):
            raise RuntimeError("down")

        with mock.patch("retrieval.retrieve", failing):
            self.pick(at, 5)
        self.assertEqual([f"{TITLE_OPEN}{CARDS[5]['title_no']}</div>"], self.box_titles(at))
        self.assertEqual(1, len([m for m in self.md(at.main) if m.startswith("**Uavklart:**")]))
        self.assertEqual([], [s for s in at.subheader if s.value == "Syntese"])
        self.assertTrue(at.warning)
        self.assertNotIn("areal_last", at.session_state)

    def test_a_later_rerun_keeps_the_box_and_does_not_ask_again(self) -> None:
        for lang in ("no", "en"):
            with self.subTest(lang):
                self.queries.clear()
                self.sent.clear()
                at = self.in_lang(lang)
                self.pick(at, 1)
                at.run()
                at.run()
                self.assertFalse(at.exception, at.exception)
                self.assertEqual([FAULTS[lang][0][2]], self.queries)
                self.assertEqual(1, len(self.answer_rows()))
                self.assertEqual(1, sum(m == KORT for m in self.md(at.main)))
                self.assertEqual(1, len(self.box_titles(at)))
                self.assertEqual(BOX_AFTER_CHIPS, self.page_order(at))
                self.assertEqual([], at.get("iframe"))

    def test_the_box_uses_the_language_at_render_time(self) -> None:
        at = self.in_lang("no")
        self.pick(at, 3)
        self.set_radio(at, "Språk / Language", "en")
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertEqual([FAULTS["no"][2][2]], self.queries)  # switching language asks nothing
        self.assertEqual([f"{TITLE_OPEN}{CARDS[3]['title_en']}</div>"], self.box_titles(at))
        self.assertIn(f"**{ASKED['en']}** {FAULTS['en'][2][2]}", [c.value for c in at.caption])
        self.assertIn(f"**{UNRESOLVED['en']}** {CARDS[3]['open_en']}", self.md(at.main))

    def test_deselecting_a_chip_asks_nothing(self) -> None:
        at = self.in_lang("no")
        self.pick(at, 2)
        self.assertEqual([FAULTS["no"][1][2]], self.queries)
        first = at.session_state["areal_last"]["answer_id"]
        self.unpick(at, 2)
        self.assertEqual([FAULTS["no"][1][2]], self.queries)  # still one retrieval
        self.assertEqual(1, len(self.answer_rows()))
        self.assertEqual([None, None, None], self.selected(at))
        self.assertNotIn("areal_ask_now", at.session_state)
        # The earlier answer and its box stay.
        self.assertEqual(first, at.session_state["areal_last"]["answer_id"])
        self.assertEqual(1, len(self.box_titles(at)))

    def test_only_one_chip_looks_selected_across_groups(self) -> None:
        at = self.in_lang("no")
        self.pick(at, 1)
        self.pick(at, 5)  # a different theme group
        self.assertEqual([None, 5, None], self.selected(at))
        self.pick(at, 9)
        self.assertEqual([None, None, 9], self.selected(at))
        self.pick(at, 8)  # back in the first group
        self.assertEqual([8, None, None], self.selected(at))
        self.assertEqual([FAULTS["no"][n - 1][2] for n in (1, 5, 9, 8)], self.queries)
        self.assertEqual(8, at.session_state["areal_last"]["card_n"])
        self.assertEqual(1, len(self.box_titles(at)))
        self.assertEqual(1, sum(m == KORT for m in self.md(at.main)))

    def test_a_cache_hit_after_a_chip_click_still_shows_the_box(self) -> None:
        at = self.in_lang("no")
        self.pick(at, 2)
        self.pick(at, 1)
        self.pick(at, 2)  # asked before: served from the cache
        self.assertEqual([FAULTS["no"][1][2], FAULTS["no"][0][2]], self.queries)  # no third retrieval
        self.assertEqual([False, False, True], [r["cached"] for r in self.answer_rows()])
        last = at.session_state["areal_last"]
        self.assertTrue(last["cached"])
        self.assertEqual(2, last["card_n"])
        self.assertEqual(BOX_AFTER_CHIPS, self.page_order(at))
        self.assertEqual([f"{TITLE_OPEN}{CARDS[2]['title_no']}</div>"], self.box_titles(at))
        # And on the rerun after the cache hit.
        at.run()
        self.assertEqual(BOX_AFTER_CHIPS, self.page_order(at))
        self.assertEqual(3, len(self.answer_rows()))

    def test_the_chosen_mode_is_used_by_a_chip_click(self) -> None:
        at = self.in_lang("no")
        self.set_radio(at, RADIO["no"], "non_researcher")
        at.run()
        self.pick(at, 5)
        self.assertEqual("non_researcher", at.session_state["areal_last"]["mode"])
        self.assertEqual("non_researcher", self.answer_rows()[-1]["mode"])
        self.assertEqual("non_researcher", next(r for r in at.main.radio if r.label == RADIO["no"]).value)
        self.assertEqual(1, len(self.full_answer_expanders(at)))  # non-specialist view of the answer
        self.assertEqual(1, len(self.box_titles(at)))
        # Back to researcher: the same chip (deselect, select) asks again in that mode.
        self.set_radio(at, RADIO["no"], "researcher")
        at.run()
        self.unpick(at, 5)
        self.pick(at, 5)
        self.assertEqual("researcher", self.answer_rows()[-1]["mode"])
        self.assertEqual([False, False], [r["cached"] for r in self.answer_rows()])
        self.assertEqual([], self.full_answer_expanders(at))

    def test_chip_click_replaces_an_earlier_answer(self) -> None:
        at = self.in_lang("no")
        self.pick(at, 1)
        first = at.session_state["areal_last"]["answer_id"]
        self.pick(at, 9)
        self.assertNotEqual(first, at.session_state["areal_last"]["answer_id"])
        self.assertEqual([FAULTS["no"][0][2], FAULTS["no"][8][2]], self.queries)
        self.assertEqual(1, sum(m == KORT for m in self.md(at.main)))
        self.assertEqual([f"{TITLE_OPEN}{CARDS[9]['title_no']}</div>"], self.box_titles(at))


class OwnQuestionTests(_CardCase):
    def test_text_area_and_ask_button_work_without_a_question_box(self) -> None:
        for lang in ("no", "en"):
            with self.subTest(lang):
                self.queries.clear()
                at = self.in_lang(lang)
                self.assertEqual("", at.text_area[0].value)
                at.text_area[0].set_value("Hva betyr trafikklyset for areal?")
                self.own_button(at, lang).click()
                at.run()
                self.assertFalse(at.exception, at.exception)
                self.assertEqual(["Hva betyr trafikklyset for areal?"], self.queries)
                self.assertEqual("Hva betyr trafikklyset for areal?", at.session_state["areal_query"])
                self.assertEqual(1, sum(m == KORT for m in self.md(at.main)))
                self.assertIsNone(at.session_state["areal_last"]["card_n"])
                self.assertEqual([], at.get("iframe"))
                # No question box: no card title, no «Spørsmålet som stilles», no «Uavklart», no «Les mer».
                self.assertEqual([], self.box_titles(at))
                text = " ".join(self.md(at.main) + [c.value for c in at.caption])
                self.assertNotIn(ASKED[lang], text)
                self.assertNotIn(UNRESOLVED[lang], text)
                self.assertEqual([], self.box_read_more(at, lang))
                self.assertEqual(["chips"] * 3 + ["synthesis", "answer"], self.page_order(at))
                self.assertIn(DRAWS_ON[lang], " ".join(c.value for c in at.caption))

    def test_a_chip_question_can_be_edited_and_asked_with_the_button(self) -> None:
        at = self.in_lang("no")
        self.pick(at, 4)
        self.assertEqual(FAULTS["no"][3][2], at.text_area[0].value)
        self.assertEqual(1, len(self.box_titles(at)))
        at.text_area[0].set_value(FAULTS["no"][3][2] + " I Trøndelag?")
        self.own_button(at, "no").click()
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertEqual([FAULTS["no"][3][2], FAULTS["no"][3][2] + " I Trøndelag?"], self.queries)
        self.assertNotIn("areal_ask_now", at.session_state)
        # An edited question is an own question: no box, and no chip stays marked.
        self.assertIsNone(at.session_state["areal_last"]["card_n"])
        self.assertEqual([], self.box_titles(at))
        self.assertEqual([None, None, None], self.selected(at))
        # The chip can be clicked again to ask its question afresh (a cache hit, with its box).
        self.pick(at, 4)
        self.assertEqual(4, at.session_state["areal_last"]["card_n"])
        self.assertEqual(1, len(self.box_titles(at)))
        self.assertTrue(at.session_state["areal_last"]["cached"])

    def test_mode_stays_the_chosen_one_for_the_own_question(self) -> None:
        at = self.in_lang("no")
        self.set_radio(at, RADIO["no"], "non_researcher")
        at.run()
        self.ask(at, "Hva er en lokalitet?")
        self.assertEqual("non_researcher", at.session_state["areal_last"]["mode"])
        self.assertEqual("non_researcher", self.answer_rows()[-1]["mode"])


if __name__ == "__main__":
    unittest.main()
