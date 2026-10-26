"""
keep_awake.py — Open the deployed app in a real browser so Streamlit Community
Cloud counts a visit, and press the wake button if the app has gone to sleep.

Run by .github/workflows/keep-awake.yml every few hours. Exits non-zero when the
app does not come up, so the failed run shows in GitHub Actions.

Usage:
  python scripts/keep_awake.py [url]
"""

from __future__ import annotations

import re
import sys

from playwright.sync_api import sync_playwright

URL = "https://ap1-curated-corpora-test.streamlit.app/Areal_og_havbruk"
WAKE_BUTTON = re.compile(r"get this app back up", re.I)
READY_TEXT = "Areal og havbruk"


def app_ready(page) -> bool:
    return any(READY_TEXT in (frame.content() or "") for frame in page.frames)


def main() -> int:
    url = sys.argv[1] if len(sys.argv) > 1 else URL
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=120_000)
        page.wait_for_timeout(15_000)
        button = page.get_by_role("button", name=WAKE_BUTTON)
        if button.count():
            print("app was asleep; pressing the wake button")
            button.first.click()
        for _ in range(20):  # up to about 5 minutes for a cold start
            if app_ready(page):
                print("app is up")
                browser.close()
                return 0
            page.wait_for_timeout(15_000)
        print("app did not come up", file=sys.stderr)
        browser.close()
        return 1


if __name__ == "__main__":
    sys.exit(main())
