"""Tests for app/regelverk.py: the Regelverk data list and its Streamlit rendering."""

import os
import sys
import unittest

from streamlit.testing.v1 import AppTest

APP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app")
sys.path.insert(0, APP_DIR)

from regelverk import REGELVERK  # noqa: E402

REQUIRED_KEYS = {"name_no", "name_en", "kind", "ministry_no", "url", "about_no", "about_en"}


def _regelverk_app(app_dir: str, lang: str) -> None:
    import sys

    sys.path.insert(0, app_dir)
    from regelverk import render_regelverk

    render_regelverk(lang)


class RegelverkDataTests(unittest.TestCase):
    def test_every_item_has_all_keys_and_nonempty_strings(self):
        for item in REGELVERK:
            self.assertEqual(set(item), REQUIRED_KEYS, item.get("name_no"))
            for key in REQUIRED_KEYS - {"kind"}:
                self.assertIsInstance(item[key], str, key)
                self.assertTrue(item[key].strip(), key)

    def test_kind_is_lov_or_forskrift(self):
        for item in REGELVERK:
            self.assertIn(item["kind"], {"lov", "forskrift"}, item["name_no"])

    def test_urls_point_to_lovdata_without_query_or_section(self):
        for item in REGELVERK:
            url = item["url"]
            self.assertTrue(url.startswith("https://lovdata.no/"), url)
            self.assertNotIn("?", url, url)
            self.assertNotIn("§", url, url)

    def test_names_are_unique(self):
        names = [item["name_no"] for item in REGELVERK]
        self.assertEqual(len(names), len(set(names)))

    def test_descriptions_are_short(self):
        for item in REGELVERK:
            for key in ("about_no", "about_en"):
                self.assertLessEqual(len(item[key].split()), 25, f"{item['name_no']} {key}")


class RenderRegelverkTests(unittest.TestCase):
    def _run(self, lang: str) -> AppTest:
        at = AppTest.from_function(_regelverk_app, args=(APP_DIR, lang))
        at.run()
        return at

    def test_renders_norwegian_without_exception(self):
        at = self._run("no")
        self.assertFalse(at.exception)

    def test_renders_english_without_exception(self):
        at = self._run("en")
        self.assertFalse(at.exception)


if __name__ == "__main__":
    unittest.main()
