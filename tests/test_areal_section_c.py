"""Section C of the Areal room: audience, documents expander, own question, open-question
dropdown and the «Spør kildene» button.

Nothing here calls OpenAI or the webhook: dotenv loading, page_link, the OpenAI client,
retrieval and the webhook sender are replaced (see _PageCase in test_areal_answer_view).

The nine open questions are a radio list (key `areal_open_q_<lang>`, nothing chosen at first)
inside a closed expander, so the full texts wrap instead of being cut off. Choosing one only
fills the text area and clears the old answer.
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
CARDS = {c["n"]: c for g in GROUPS for c in g["cards"]}
CARD_ORDER = [c["n"] for g in GROUPS for c in g["cards"]]  # 1, 2, 8, 3, 5, 7, 4, 6, 9
ASK_BUTTON = {"no": "Spør kildene", "en": "Ask the sources"}
OLD_BUTTON = {"no": "Syntetiser", "en": "Synthesise"}
YOUR_Q = {"no": "Spørsmålet ditt", "en": "Your question"}
RADIO = {"no": "Velg bakgrunn", "en": "Choose your background"}
OPEN_Q = {"no": "Eller velg et åpent spørsmål", "en": "Or pick an open question"}
DOCS_PREFIX = {"no": "Dokumenter i korpuset (", "en": "Documents in the corpus ("}
DOCS_LABEL = {
    "no": "Dokumenter i korpuset ({n} av {m} valgt)",
    "en": "Documents in the corpus ({n} of {m} selected)",
}
SYNTHESIS = {"no": "Syntese", "en": "Synthesis"}
TAG = {"no": "Ditt eget spørsmål, eller et åpent", "en": "Your own question, or an open one"}
DRAWS_ON = {"no": "Svaret bygger på de", "en": "The answer draws on the"}
EDITORIAL = {"no": "Redaksjonell orientering", "en": "Editorial orientation"}
N_DOCS = 50


def flat(node):
    """Every element below `node`, in page order."""
    for child in node.children.values():
        yield child
        if hasattr(child, "children"):
            yield from flat(child)


class _SectionCase(_PageCase):
    def setUp(self) -> None:
        super().setUp()
        self.queries: list[str] = []
        self.retrieve_kwargs: list[dict] = []
        outer = self

        def recording_retrieve(client, query, **kwargs):
            outer.queries.append(query)
            outer.retrieve_kwargs.append(kwargs)
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
    def dropdown(at, lang):
        return at.radio(key=f"areal_open_q_{lang}")

    def choose(self, at, lang, n):
        """Pick open question n (1-9, i.e. A0-A8) in the list."""
        self.dropdown(at, lang).set_value(n)
        at.run()
        self.assertFalse(at.exception, at.exception)

    def answer_rows(self):
        return [p for p in self.sent if p["type"] == "answer"]

    @staticmethod
    def own_button(at, lang):
        return next(b for b in at.main.button if b.label == ASK_BUTTON[lang])

    @staticmethod
    def docs_expander(at, lang):
        return next(e for e in at.main.expander if e.label.startswith(DOCS_PREFIX[lang]))

    def captions(self, at):
        return [c.value for c in at.caption]


class SectionLayoutTests(_SectionCase):
    def test_content_module_covers_questions_one_to_nine_once(self) -> None:
        self.assertEqual(list(range(1, 10)), sorted(CARD_ORDER))
        self.assertEqual(3, len(GROUPS))
        self.assertTrue(all(len(g["cards"]) == 3 for g in GROUPS))

    def test_section_order_in_both_languages(self) -> None:
        for lang in ("no", "en"):
            with self.subTest(lang):
                at = self.in_lang(lang)
                labels = [getattr(e, "label", None) for e in flat(at.main)]
                docs_label = self.docs_expander(at, lang).label
                order = [
                    labels.index(RADIO[lang]),
                    labels.index(docs_label),
                    labels.index(YOUR_Q[lang]),
                    labels.index(OPEN_Q[lang]),
                    labels.index(ASK_BUTTON[lang]),
                ]
                self.assertEqual(sorted(order), order)
                self.assertEqual(5, len(set(order)))
                # The editorial caption and the footer come after the section.
                self.assertTrue([c.value for c in at.main.caption][-1].startswith(EDITORIAL[lang]))
                self.assertTrue(any(f">{TAG[lang]}<" in m for m in self.md(at.main)))
                self.assertEqual("primary", self.own_button(at, lang).proto.type)
                self.assertEqual([], [b for b in at.main.button if b.label == OLD_BUTTON[lang]])
                self.assertIn(DRAWS_ON[lang], " ".join(self.captions(at)))
        # Same order in the page source.
        src = Path(PAGE).read_text(encoding="utf-8")
        positions = [
            src.index("mode = st.radio("),
            src.index('key="areal_docs_expander"'),
            src.index("query = st.text_area("),
            src.index('with st.expander(tr(lang, "Or pick an open question"'),
            src.index("run = st.button("),
            src.index("if run and query.strip():"),
            src.index('"Redaksjonell orientering'),
        ]
        self.assertEqual(sorted(positions), positions)

    def test_documents_expander_holds_picker_and_k_slider_and_sidebar_does_not(self) -> None:
        for lang in ("no", "en"):
            with self.subTest(lang):
                at = self.in_lang(lang)
                exp = self.docs_expander(at, lang)
                self.assertFalse(exp.proto.expanded)
                self.assertEqual(DOCS_LABEL[lang].format(n=N_DOCS, m=N_DOCS), exp.label)
                self.assertEqual(1, len(exp.multiselect))
                self.assertEqual(N_DOCS, len(exp.multiselect[0].value))  # all selected by default
                self.assertEqual("areal_selected", exp.multiselect[0].key)
                self.assertEqual(N_DOCS, len(at.session_state["areal_selected"]))
                self.assertEqual(1, len(exp.slider))
                self.assertEqual((10, 3, 12), (exp.slider[0].value, exp.slider[0].min, exp.slider[0].max))
                self.assertEqual(
                    {"Velg alle", "Tøm"} if lang == "no" else {"Select all", "Clear all"},
                    {b.label for b in exp.button},
                )
                # Readable labels: author, year and title, not a bare doc id.
                self.assertTrue(all(" · " in o for o in exp.multiselect[0].options))
                # Nothing of it is left in the sidebar.
                self.assertEqual([], list(at.sidebar.expander))
                self.assertEqual([], list(at.sidebar.multiselect))
                self.assertEqual([], list(at.sidebar.slider))
                self.assertEqual([], list(at.sidebar.button))
                sidebar_text = " ".join(c.value for c in at.sidebar.caption)
                self.assertIn("Honest Broker", sidebar_text)
                self.assertFalse([e for e in at.sidebar.expander if "ksed" in e.label or "dvanced" in e.label])
                # Only one slider and one multiselect on the page.
                self.assertEqual(1, len(at.slider))
                self.assertEqual(1, len(at.multiselect))

    def test_dropdown_lists_the_full_priority_questions_in_order(self) -> None:
        for lang in ("no", "en"):
            with self.subTest(lang):
                at = self.in_lang(lang)
                # A closed panel, so the long questions wrap instead of being cut off.
                panel = [e for e in at.expander if e.label == OPEN_Q[lang]]
                self.assertEqual(1, len(panel))
                dd = self.dropdown(at, lang)
                # The full A0-A8 texts, verbatim and in order; not the short card titles.
                self.assertEqual([f[2] for f in FAULTS[lang]], dd.options)
                self.assertIsNone(dd.value)  # nothing chosen before a click
                self.assertEqual(0, len(at.selectbox))

    def test_no_chips_and_no_question_box_remain(self) -> None:
        src = Path(PAGE).read_text(encoding="utf-8")
        for gone in (
            "st.pills", "_pick_question", "_clear_chips", "areal_ask_now", "areal_ask_card",
            "_render_question_box", "areal_chips_", "_card_sources", "hl-card-title", "hl-group-title",
            "Avanserte innstillinger", "Advanced settings", "Last inn korpus på nytt", "areal_card_",
        ):
            self.assertNotIn(gone, src)
        ui = (REPO / "app" / "ui.py").read_text(encoding="utf-8")
        self.assertNotIn("hl-card-title", ui)
        self.assertNotIn("hl-group-title", ui)
        for lang in ("no", "en"):
            with self.subTest(lang):
                at = self.in_lang(lang)
                self.assertEqual([], list(at.get("button_group")))
                text = " ".join(self.md(at.main) + self.captions(at))
                for old in ("hl-card-title", "hl-group-title", "Spørsmålet som stilles", "The question asked",
                            "Uavklart", "Unresolved", "Åpent:", "**Open:**"):
                    self.assertNotIn(old, text)
                # No «Les mer» with editorial paragraphs from the open questions.
                long_texts = [f[1] for f in FAULTS[lang]]
                self.assertFalse(any(t in text for t in long_texts))
                self.assertEqual([], [b for b in at.button if (b.key or "").startswith("areal_card_")])
                self.assertEqual(1, len([b for b in at.main.button if b.label == ASK_BUTTON[lang]]))


class OpenQuestionTests(_SectionCase):
    def test_choosing_fills_the_text_area_with_the_full_question_and_asks_nothing(self) -> None:
        for lang, n in (("no", 3), ("en", 7), ("no", 9), ("en", 1)):
            with self.subTest(lang=lang, n=n):
                self.queries.clear()
                self.sent.clear()
                at = self.in_lang(lang)
                self.choose(at, lang, n)
                question = FAULTS[lang][n - 1][2]
                self.assertEqual(question, at.text_area[0].value)
                self.assertEqual(question, at.session_state["areal_query"])
                self.assertEqual(n, self.dropdown(at, lang).value)
                self.assertEqual([], self.queries)  # no retrieval, so no ask call
                self.assertEqual([], self.answer_rows())
                self.assertNotIn("areal_last", at.session_state)
                self.assertEqual([], [s for s in at.subheader if s.value == SYNTHESIS[lang]])
                # No prepared content: no card text, points or «Les mer» for the choice.
                text = " ".join(self.md(at.main) + self.captions(at))
                self.assertNotIn(CARDS[n]["intro"][lang], text)
                self.assertNotIn(CARDS[n]["open_" + lang], text)
                self.assertNotIn(FAULTS[lang][n - 1][1], text)
                for point in CARDS[n]["points"]:
                    self.assertNotIn(point[lang], text)

    def test_choosing_clears_an_existing_answer(self) -> None:
        at = self.in_lang("no")
        self.ask(at, "Hva er en lokalitet?")
        self.assertIn("areal_last", at.session_state)
        self.assertEqual(1, sum(m == KORT for m in self.md(at.main)))
        self.assertEqual(["Hva er en lokalitet?"], self.queries)
        self.choose(at, "no", 4)
        self.assertNotIn("areal_last", at.session_state)
        self.assertEqual(0, sum(m == KORT for m in self.md(at.main)))
        self.assertEqual([], [s for s in at.subheader if s.value == "Syntese"])
        self.assertEqual(FAULTS["no"][3][2], at.text_area[0].value)
        self.assertEqual(["Hva er en lokalitet?"], self.queries)  # still only the first ask
        self.assertEqual(1, len(self.answer_rows()))
        # And it stays cleared on a plain rerun.
        at.run()
        self.assertNotIn("areal_last", at.session_state)
        self.assertEqual(0, sum(m == KORT for m in self.md(at.main)))

    def test_choosing_another_question_replaces_the_text(self) -> None:
        at = self.in_lang("no")
        self.choose(at, "no", 1)
        self.choose(at, "no", 5)
        self.assertEqual(FAULTS["no"][4][2], at.text_area[0].value)
        self.assertEqual([], self.queries)

    def test_nothing_is_chosen_or_asked_until_a_click(self) -> None:
        at = self.in_lang("no")
        self.assertIsNone(self.dropdown(at, "no").value)
        self.assertEqual("", at.text_area[0].value)
        self.assertEqual([], self.queries)
        self.assertNotIn("areal_last", at.session_state)
        # An own question answered first stays until an open question is picked.
        at.text_area[0].set_value("Hva er en lokalitet?")
        self.ask(at, "Hva er en lokalitet?")
        self.assertIn("areal_last", at.session_state)
        at.run()
        self.assertIn("areal_last", at.session_state)
        self.assertEqual(["Hva er en lokalitet?"], self.queries)

    def test_ask_button_then_asks_the_chosen_question_once(self) -> None:
        for lang, n in (("no", 2), ("en", 6)):
            with self.subTest(lang=lang, n=n):
                self.queries.clear()
                self.sent.clear()
                at = self.in_lang(lang)
                self.choose(at, lang, n)
                self.assertEqual([], self.queries)
                self.own_button(at, lang).click()
                at.run()
                self.assertFalse(at.exception, at.exception)
                question = FAULTS[lang][n - 1][2]
                self.assertEqual([question], self.queries)
                last = at.session_state["areal_last"]
                self.assertEqual((question, lang), (last["query"], last["lang"]))
                self.assertNotIn("card_n", last)
                self.assertEqual(1, sum(m == KORT for m in self.md(at.main)))
                self.assertTrue([s for s in at.subheader if s.value == SYNTHESIS[lang]])
                self.assertTrue([b for b in at.button if b.label in ("Send tilbakemelding", "Send feedback")])
                self.assertTrue([s for s in at.subheader if s.value.startswith(("Hentede kilder", "Retrieved sources"))])
                row = self.answer_rows()[-1]
                self.assertEqual((question, lang), (row["question"], row["language"]))
                # Later reruns show the stored answer and ask nothing more.
                at.run()
                at.run()
                self.assertEqual([question], self.queries)
                self.assertEqual(1, len(self.answer_rows()))
                self.assertEqual(1, sum(m == KORT for m in self.md(at.main)))

    def test_edited_text_is_just_the_users_own_question(self) -> None:
        at = self.in_lang("no")
        self.choose(at, "no", 4)
        edited = FAULTS["no"][3][2] + " I Trøndelag?"
        at.text_area[0].set_value(edited)
        self.own_button(at, "no").click()
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertEqual([edited], self.queries)
        self.assertEqual(edited, at.session_state["areal_last"]["query"])
        # The answer sits under the edited text; no prepared content appears.
        self.assertEqual(1, sum(m == KORT for m in self.md(at.main)))
        text = " ".join(self.md(at.main) + self.captions(at))
        self.assertNotIn(CARDS[4]["open_no"], text)

    def test_empty_text_asks_nothing(self) -> None:
        at = self.in_lang("no")
        self.own_button(at, "no").click()
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertEqual([], self.queries)
        self.assertNotIn("areal_last", at.session_state)

    def test_language_switch_resets_the_open_question_list(self) -> None:
        at = self.in_lang("no")
        self.choose(at, "no", 3)
        self.set_radio(at, "Språk / Language", "en")
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertEqual([], self.queries)  # switching language asks nothing
        self.assertIsNone(self.dropdown(at, "en").value)  # English list starts unchosen
        self.assertEqual(FAULTS["no"][2][2], at.text_area[0].value)  # the text stays
        self.assertEqual(9, len(self.dropdown(at, "en").options))
        self.choose(at, "en", 3)
        self.assertEqual(FAULTS["en"][2][2], at.text_area[0].value)
        # Back to Norwegian: Streamlit drops the state of a widget that was not drawn, so the
        # list starts unchosen again. Nothing is asked, the text stays.
        self.set_radio(at, "Språk / Language", "no")
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertIsNone(self.dropdown(at, "no").value)
        self.assertEqual(FAULTS["en"][2][2], at.text_area[0].value)
        self.assertEqual([], self.queries)

    def test_mode_stays_the_chosen_one_after_choosing_a_question(self) -> None:
        at = self.in_lang("no")
        self.set_radio(at, RADIO["no"], "non_researcher")
        at.run()
        self.choose(at, "no", 5)
        self.own_button(at, "no").click()
        at.run()
        self.assertEqual("non_researcher", at.session_state["areal_last"]["mode"])
        self.assertEqual("non_researcher", self.answer_rows()[-1]["mode"])
        self.assertEqual(1, len(self.full_answer_expanders(at)))

    def test_old_session_state_with_card_n_does_not_crash(self) -> None:
        at = self.in_lang("no")
        self.ask(at, "Hva er en lokalitet?")
        last = dict(at.session_state["areal_last"], card_n=3)
        at.session_state["areal_last"] = last
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertEqual(1, sum(m == KORT for m in self.md(at.main)))
        self.assertEqual(["Hva er en lokalitet?"], self.queries)
        self.assertEqual("", " ".join(m for m in self.md(at.main) if "hl-card-title" in m))


class DocumentsAndKTests(_SectionCase):
    QUESTION = "Hva begrenser vekst i havbruk?"

    def multiselect(self, at):
        return at.multiselect(key="areal_selected")

    def drawn(self, at):
        return next(c for c in self.captions(at) if c.startswith(("Svaret bygger på", "The answer draws on")))

    def test_deselecting_documents_changes_caption_label_and_cache_key(self) -> None:
        at = self.in_lang("no")
        self.assertIn("de 10 mest relevante av 50 dokumenter", self.drawn(at))
        all_ids = list(self.multiselect(at).value)
        self.assertEqual(N_DOCS, len(all_ids))
        self.ask(at, self.QUESTION)
        self.assertEqual([self.QUESTION], self.queries)
        self.assertEqual(N_DOCS, len(self.retrieve_kwargs[0]["selected_doc_ids"]))
        self.assertEqual(10, self.retrieve_kwargs[0]["top_k"])
        self.assertEqual([False], [r["cached"] for r in self.answer_rows()])

        keep = all_ids[:-5]
        self.multiselect(at).set_value(keep)
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertIn("de 10 mest relevante av 45 dokumenter", self.drawn(at))
        self.assertEqual(DOCS_LABEL["no"].format(n=45, m=N_DOCS), self.docs_expander(at, "no").label)
        self.assertEqual(keep, at.session_state["areal_selected"])
        # Same question, fewer documents: a different cache key, so a fresh retrieval.
        self.own_button(at, "no").click()
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertEqual([self.QUESTION, self.QUESTION], self.queries)
        self.assertEqual(keep, self.retrieve_kwargs[1]["selected_doc_ids"])
        self.assertEqual(45, self.answer_rows()[-1]["n_active_docs"])
        self.assertEqual([False, False], [r["cached"] for r in self.answer_rows()])
        # The same selection again is a cache hit.
        self.own_button(at, "no").click()
        at.run()
        self.assertEqual(2, len(self.queries))
        self.assertEqual([False, False, True], [r["cached"] for r in self.answer_rows()])

    def test_k_slider_changes_caption_and_cache_key(self) -> None:
        at = self.in_lang("en")
        self.ask(at, self.QUESTION)
        self.assertEqual(10, self.retrieve_kwargs[0]["top_k"])
        at.slider[0].set_value(4)
        at.run()
        self.assertIn("The answer draws on the 4 most relevant of 50 documents.", self.drawn(at))
        self.own_button(at, "en").click()
        at.run()
        self.assertEqual([10, 4], [k["top_k"] for k in self.retrieve_kwargs])
        self.assertEqual([10, 4], [r["top_k"] for r in self.answer_rows()])

    def test_clear_and_select_all_buttons_follow_in_label_and_widget(self) -> None:
        for lang in ("no", "en"):
            with self.subTest(lang):
                at = self.in_lang(lang)
                clear, select_all = ("Tøm", "Velg alle") if lang == "no" else ("Clear all", "Select all")
                next(b for b in at.button if b.label == clear).click()
                at.run()
                self.assertFalse(at.exception, at.exception)
                self.assertEqual([], self.multiselect(at).value)
                self.assertEqual(DOCS_LABEL[lang].format(n=0, m=N_DOCS), self.docs_expander(at, lang).label)
                self.assertTrue(at.warning)
                # Asking with nothing selected shows the pointer to the expander, no retrieval.
                at.text_area[0].set_value(self.QUESTION)
                self.own_button(at, lang).click()
                at.run()
                self.assertFalse(at.exception, at.exception)
                self.assertEqual([], self.queries)
                self.assertTrue([e for e in at.error if "Dokumenter i korpuset" in e.value or "Documents in the corpus" in e.value])
                next(b for b in at.button if b.label == select_all).click()
                at.run()
                self.assertEqual(N_DOCS, len(self.multiselect(at).value))
                self.assertEqual(DOCS_LABEL[lang].format(n=N_DOCS, m=N_DOCS), self.docs_expander(at, lang).label)

    def test_old_session_with_display_labels_falls_back_to_all_documents(self) -> None:
        at = self.app()
        at.session_state["areal_selected"] = ["Hersoug 2020 · gammel visningstekst"]
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertEqual(N_DOCS, len(self.multiselect(at).value))

    def test_selected_documents_survive_a_language_switch(self) -> None:
        at = self.in_lang("no")
        keep = list(self.multiselect(at).value)[:7]
        self.multiselect(at).set_value(keep)
        at.run()
        self.set_radio(at, "Språk / Language", "en")
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertEqual(keep, self.multiselect(at).value)
        self.assertEqual(DOCS_LABEL["en"].format(n=7, m=N_DOCS), self.docs_expander(at, "en").label)


if __name__ == "__main__":
    unittest.main()
