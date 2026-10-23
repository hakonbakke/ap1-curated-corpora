"""UI layout checks for the Areal room: where the main choices sit, readable source names.

Nothing here calls OpenAI: dotenv loading, page_link and the OpenAI client are replaced,
and no button that triggers synthesis is pressed.
"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "app"))

PAGE = str(REPO / "app" / "pages" / "2_Areal_og_havbruk.py")


class _NoOpenAI:
    def __init__(self, *a, **k):
        raise AssertionError("The UI tests must never construct an OpenAI client.")


class ArealUiTests(unittest.TestCase):
    def setUp(self) -> None:
        from streamlit.testing.v1 import AppTest

        self.AppTest = AppTest
        patches = [
            mock.patch("dotenv.load_dotenv", lambda *a, **k: False),
            mock.patch("streamlit.page_link", lambda *a, **k: None),
            mock.patch("openai.OpenAI", _NoOpenAI),
            mock.patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-not-real"}),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)

    def app(self):
        return self.AppTest.from_file(PAGE, default_timeout=120)

    @staticmethod
    def _labels(widgets):
        return [w.label for w in widgets]

    def test_language_and_audience_are_in_main_area_not_sidebar(self) -> None:
        at = self.app().run()
        self.assertFalse(at.exception, at.exception)
        main_radios = {r.label: r for r in at.main.radio}
        sidebar_radios = list(at.sidebar.radio)
        self.assertEqual([], sidebar_radios)
        self.assertIn("Språk / Language", main_radios)
        self.assertEqual("no", main_radios["Språk / Language"].value)
        self.assertEqual("researcher", main_radios["Velg bakgrunn"].value)
        # The expert controls live in a collapsed expander in section C, not in the sidebar.
        self.assertEqual([], list(at.sidebar.expander))
        self.assertEqual([], list(at.sidebar.slider))
        self.assertEqual([], list(at.sidebar.multiselect))
        docs = [e for e in at.main.expander if e.label.startswith("Dokumenter i korpuset")]
        self.assertEqual(1, len(docs))
        self.assertFalse(docs[0].proto.expanded)
        self.assertEqual((12, 3, 15), (at.slider[0].value, at.slider[0].min, at.slider[0].max))

    def test_loads_in_both_languages_and_both_modes(self) -> None:
        at = self.app().run()
        self.assertFalse(at.exception, at.exception)
        at.main.radio[0].set_value("en").run()
        self.assertFalse(at.exception, at.exception)
        self.assertIn("Choose your background", self._labels(at.main.radio))
        self.assertEqual([], list(at.sidebar.expander))
        self.assertTrue([e for e in at.main.expander if e.label.startswith("Documents in the corpus (")])
        for r in at.main.radio:
            if r.label == "Choose your background":
                r.set_value("non_researcher")
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertTrue(any("plain language" in i.value for i in at.info))
        self.assertEqual("non_researcher", [r for r in at.main.radio if r.label == "Choose your background"][0].value)

    def test_jargon_is_gone_from_visible_text(self) -> None:
        at = self.app().run()
        text = " ".join([m.value for m in at.markdown] + [c.value for c in at.caption])
        for needle in ("PRIORITY_QUESTIONS", "A0 til A8", "A0-A8", "k = "):
            self.assertNotIn(needle, text)


class SourceLabelTests(unittest.TestCase):
    """_source_label lives in the page script, so exercise it through its source text."""

    @classmethod
    def setUpClass(cls) -> None:
        src = Path(PAGE).read_text(encoding="utf-8")
        start = src.index("def _surname")
        end = src.index("# ── Open questions (C)")
        ns = {"tr": lambda lang, en, no: no if lang == "no" else en}
        exec(src[start:end], ns)
        cls.label = staticmethod(ns["_source_label"])

    def test_author_counts(self) -> None:
        L = self.label
        self.assertEqual("Myklebust 2018", L("no", "Ingunn Elise Myklebust", 2018, "x"))
        self.assertEqual("Sand og Misund 2025", L("no", "Roald Sand; Andreas Ugelvik Misund", 2025, "x"))
        self.assertEqual("Sand and Misund 2025", L("en", "Roald Sand; Andreas Ugelvik Misund", 2025, "x"))
        self.assertEqual("Hersoug mfl. 2020", L("no", "Bjørn Hersoug; Eirik Mikkelsen; Tonje C. Osmundsen", 2020, "x"))
        self.assertEqual("Hersoug et al. 2020", L("en", "Bjørn Hersoug; Eirik Mikkelsen; Tonje C. Osmundsen", 2020, "x"))

    def test_organisation_and_missing_authors(self) -> None:
        L = self.label
        self.assertEqual("Metier AS 2023", L("no", "Metier AS", 2023, "x"))
        short = L("no", "", 2024, "Barekraftig bruk og bevaring av natur. Norsk handlingsplan for naturmangfold")
        self.assertTrue(short.endswith("… (2024)"), short)
        self.assertLessEqual(len(short), 40 + len("… (2024)"))
        self.assertEqual("Kort tittel (2024)", L("no", None, 2024, "Kort tittel"))


if __name__ == "__main__":
    unittest.main()
