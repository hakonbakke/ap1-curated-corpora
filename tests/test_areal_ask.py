"""Tests for the Areal ask flow: streaming, cache, logging, rate limit, rerun persistence.

Nothing here calls OpenAI or the feedback webhook. The OpenAI client, retrieval,
synthesis stream and webhook sender are all replaced.
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
import synthesis  # noqa: E402
from synthesis import _build_request, synthesise, synthesise_stream  # noqa: E402

PAGE = str(REPO / "app" / "pages" / "2_Areal_og_havbruk.py")

RESULTS = [
    {
        "doc_id": "2020_hersoug_a",
        "authors": "Hersoug, B.",
        "year": 2020,
        "title": "A study of licences",
        "semantic_score": 0.9,
        "score": 0.9,
        "rag_summary": "Licences limit growth.",
        "evidence_direction": "not_applicable",
        "quality_signal": "medium",
    },
    {
        "doc_id": "2022_hersoug_b",
        "authors": "Hersoug, B.",
        "year": 2022,
        "title": "Another study",
        "semantic_score": 0.8,
        "score": 0.8,
        "rag_summary": "Plans limit growth.",
        "evidence_direction": "not_applicable",
        "quality_signal": "medium",
    },
]


def _chunk(text):
    delta = SimpleNamespace(content=text)
    return SimpleNamespace(choices=[SimpleNamespace(delta=delta)])


class FakeCompletions:
    def __init__(self, pieces=("Hello", " ", "world")):
        self.calls = []
        self.pieces = pieces

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if kwargs.get("stream"):
            # An empty-choices chunk (as Azure-style keep-alives send) and a None delta.
            return iter([SimpleNamespace(choices=[])] + [_chunk(p) for p in self.pieces] + [_chunk(None)])
        message = SimpleNamespace(content="  " + "".join(self.pieces) + "  ")
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def fake_client(pieces=("Hello", " ", "world")):
    completions = FakeCompletions(pieces)
    return SimpleNamespace(chat=SimpleNamespace(completions=completions)), completions


class SynthesisStreamTests(unittest.TestCase):
    ARGS = dict(mode="non_researcher", answer_format="freeform", output_language="Norwegian Bokmål", model="gpt-6-luna", room="areal")

    def test_request_keeps_gpt6_parameters(self) -> None:
        kwargs = _build_request("Hva begrenser vekst?", RESULTS, **self.ARGS)
        self.assertEqual("gpt-6-luna", kwargs["model"])
        self.assertIn("max_completion_tokens", kwargs)
        self.assertNotIn("max_tokens", kwargs)
        self.assertEqual("none", kwargs["reasoning_effort"])
        self.assertEqual(0.35, kwargs["temperature"])
        self.assertEqual("user", kwargs["messages"][0]["role"])
        self.assertIn("Hva begrenser vekst?", kwargs["messages"][0]["content"])

    def test_request_keeps_gpt4_parameters(self) -> None:
        kwargs = _build_request("q", RESULTS, model="gpt-4o", room="villaks")
        self.assertIn("max_tokens", kwargs)
        self.assertNotIn("max_completion_tokens", kwargs)
        self.assertNotIn("reasoning_effort", kwargs)

    def test_synthesise_uses_build_request_and_strips(self) -> None:
        client, completions = fake_client()
        text = synthesise(client, "q", RESULTS, **self.ARGS)
        self.assertEqual("Hello world", text)
        self.assertEqual([_build_request("q", RESULTS, **self.ARGS)], completions.calls)

    def test_stream_yields_deltas_and_skips_empty_chunks(self) -> None:
        client, completions = fake_client()
        pieces = list(synthesise_stream(client, "q", RESULTS, **self.ARGS))
        self.assertEqual(["Hello", " ", "world"], pieces)
        self.assertEqual({**_build_request("q", RESULTS, **self.ARGS), "stream": True}, completions.calls[0])

    def test_empty_results_behave_like_before(self) -> None:
        client, completions = fake_client()
        self.assertEqual("No relevant documents found in the corpus for this query.", synthesise(client, "q", []))
        self.assertEqual(["No relevant documents found in the corpus for this query."], list(synthesise_stream(client, "q", [])))
        self.assertEqual([], completions.calls)


class FeedbackModuleTests(unittest.TestCase):
    ANSWER = dict(
        session_id="s", answer_id="a", question="q", mode="researcher", language="no", model="gpt-6-luna",
        top_k=10, n_active_docs=50, retrieved=["d1", "d2"], answer="x", latency_s=12.34, cached=False,
    )

    def test_answer_payload_keys_and_values(self) -> None:
        p = feedback.build_answer_payload(**self.ANSWER)
        self.assertEqual(
            ["type", "ts", "session_id", "answer_id", "room", "question", "mode", "language", "model",
             "top_k", "n_active_docs", "retrieved", "answer", "latency_s", "cached", "error",
             "answer_words", "answer_shape"],
            list(p),
        )
        self.assertEqual("answer", p["type"])
        self.assertEqual("areal", p["room"])
        self.assertEqual("d1, d2", p["retrieved"])
        self.assertEqual(12.3, p["latency_s"])
        self.assertIs(False, p["cached"])
        self.assertEqual("", p["error"])
        self.assertTrue(p["ts"].endswith("+00:00"))

    def test_rating_payload_keys_and_defaults(self) -> None:
        p = feedback.build_rating_payload(session_id="s", answer_id="a", thumbs="up", comment="hm")
        self.assertEqual(
            ["type", "ts", "session_id", "answer_id", "thumbs", "answered_question", "fair_disagreement", "comment",
             "length", "readability"],
            list(p),
        )
        self.assertEqual("rating", p["type"])
        self.assertEqual("", p["answered_question"])
        self.assertEqual("", p["fair_disagreement"])

    def test_cache_key_is_stable_and_order_independent(self) -> None:
        a = feedback.answer_cache_key("  Hva?  ", "researcher", "no", 10, ["b", "a", "c"], "gpt-6-luna")
        b = feedback.answer_cache_key("Hva?", "researcher", "no", 10, ("c", "a", "b"), "gpt-6-luna")
        self.assertEqual(a, b)
        self.assertEqual(("Hva?", "researcher", "no", 10, ("a", "b", "c"), "gpt-6-luna"), a)
        self.assertNotEqual(a, feedback.answer_cache_key("Hva?", "non_researcher", "no", 10, ["a", "b", "c"], "gpt-6-luna"))
        self.assertNotEqual(a, feedback.answer_cache_key("Hva?", "researcher", "en", 10, ["a", "b", "c"], "gpt-6-luna"))
        self.assertNotEqual(a, feedback.answer_cache_key("Hva?", "researcher", "no", 9, ["a", "b", "c"], "gpt-6-luna"))

    def test_cache_put_get_and_eviction(self) -> None:
        store = ({}, threading.Lock())
        self.assertIsNone(feedback.cache_get(("k",), store))
        feedback.cache_put(("k",), ([1], "answer"), store)
        self.assertEqual(([1], "answer"), feedback.cache_get(("k",), store))
        with mock.patch.object(feedback, "CACHE_MAX_ENTRIES", 2):
            feedback.cache_put(("k2",), ([], "b"), store)
            feedback.cache_put(("k3",), ([], "c"), store)
        self.assertIsNone(feedback.cache_get(("k",), store))
        self.assertEqual(2, len(store[0]))

    def test_send_is_noop_without_url(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=False), mock.patch("urllib.request.urlopen") as urlopen:
            os.environ.pop("FEEDBACK_WEBHOOK_URL", None)
            with mock.patch.object(feedback, "_webhook_url", return_value=""):
                self.assertIsNone(feedback.send_async({"type": "answer"}))
                feedback.log_answer(**self.ANSWER)
                feedback.log_rating(session_id="s", answer_id="a")
            urlopen.assert_not_called()

    def test_send_posts_json_in_daemon_thread_and_swallows_errors(self) -> None:
        with mock.patch("urllib.request.urlopen", side_effect=OSError("boom")) as urlopen:
            thread = feedback.send_async({"type": "answer"}, url="https://example.invalid/exec")
            self.assertTrue(thread.daemon)
            thread.join(5)
            self.assertFalse(thread.is_alive())
            request = urlopen.call_args.args[0]
            self.assertEqual(b'{"type": "answer"}', request.data)
            self.assertEqual(feedback.WEBHOOK_TIMEOUT_S, urlopen.call_args.kwargs["timeout"])
        # Bad payload and bad URL must not raise either.
        feedback._post("not a url", {"x": object()})

    def test_webhook_url_reads_env_first(self) -> None:
        with mock.patch.dict(os.environ, {"FEEDBACK_WEBHOOK_URL": " https://example.invalid/exec "}):
            self.assertEqual("https://example.invalid/exec", feedback._webhook_url())


class ArealPageTests(unittest.TestCase):
    """Drive the real page with streamlit.testing.v1.AppTest and everything external mocked."""

    def setUp(self) -> None:
        from streamlit.testing.v1 import AppTest

        self.AppTest = AppTest
        self.sent: list[dict] = []
        self.store = ({}, threading.Lock())
        self.completions = FakeCompletions(("Svar ", "fra ", "kildene."))
        self.retrieve_calls = 0
        outer = self

        def fake_retrieve(client, query, **kwargs):
            outer.retrieve_calls += 1
            return list(RESULTS)

        class FakeOpenAI:
            def __init__(self, **kwargs):
                outer.client_kwargs = kwargs
                self.chat = SimpleNamespace(completions=outer.completions)
                self.embeddings = SimpleNamespace(create=mock.Mock(side_effect=AssertionError("embeddings called")))

        self.fake_retrieve = fake_retrieve
        patches = [
            mock.patch("dotenv.load_dotenv", lambda *a, **k: False),
            # AppTest has no multipage navigation context, so st.page_link raises KeyError.
            mock.patch("streamlit.page_link", lambda *a, **k: None),
            mock.patch("openai.OpenAI", FakeOpenAI),
            mock.patch("retrieval.retrieve", fake_retrieve),
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
    def button(at, label):
        return next(b for b in at.button if b.label == label)

    def ask(self, at, question="Hva begrenser vekst i havbruk?"):
        at.text_area[0].set_value(question)
        self.button(at, "Syntetiser").click()
        at.run()

    @staticmethod
    def texts(at):
        return [m.value for m in at.markdown]

    def test_loads_without_key_or_webhook(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("OPENAI_API_KEY", None)
            at = self.app().run()
            self.assertFalse(at.exception, at.exception)
            self.ask(at)
            self.assertFalse(at.exception, at.exception)
            self.assertTrue(any("OPENAI_API_KEY" in e.value for e in at.error))
        self.assertEqual([], self.sent)

    def test_answer_survives_reruns_and_is_logged(self) -> None:
        at = self.app().run()
        self.assertFalse(at.exception, at.exception)
        self.ask(at)
        self.assertFalse(at.exception, at.exception)
        self.assertEqual({"max_retries": 3, "timeout": 120.0}, {k: v for k, v in self.client_kwargs.items() if k != "api_key"})
        self.assertIn("Svar fra kildene.", self.texts(at))
        self.assertEqual(1, sum("Svar fra kildene." == t for t in self.texts(at)), "answer rendered twice in one run")
        self.assertEqual(1, len(self.completions.calls))
        self.assertTrue(self.completions.calls[0]["stream"])
        last = at.session_state["areal_last"]
        self.assertEqual(["answer_id", "query", "mode", "lang", "results", "answer", "latency_s", "cached"], list(last))
        self.assertEqual("Svar fra kildene.", last["answer"])
        self.assertFalse(last["cached"])

        # Rerun with no button pressed: the answer must still be on screen, no API call.
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertEqual(1, sum("Svar fra kildene." == t for t in self.texts(at)))
        self.assertEqual(1, len(self.completions.calls))
        self.assertEqual(1, self.retrieve_calls)

        answer_rows = [p for p in self.sent if p["type"] == "answer"]
        self.assertEqual(1, len(answer_rows))
        row = answer_rows[0]
        self.assertEqual("2020_hersoug_a, 2022_hersoug_b", row["retrieved"])
        self.assertEqual("Svar fra kildene.", row["answer"])
        self.assertEqual(("no", "researcher", "gpt-6-luna", 10), (row["language"], row["mode"], row["model"], row["top_k"]))
        self.assertIs(False, row["cached"])
        self.assertEqual("", row["error"])
        self.assertEqual(row["answer_id"], last["answer_id"])
        self.assertEqual(at.session_state["areal_session_id"], row["session_id"])

    def test_identical_question_is_a_cache_hit_without_api_calls(self) -> None:
        at = self.app().run()
        self.ask(at)
        calls_before = len(self.completions.calls)
        other = self.app().run()  # a different session
        self.ask(other)
        self.assertFalse(other.exception, other.exception)
        self.assertEqual(calls_before, len(self.completions.calls))
        self.assertEqual(1, self.retrieve_calls)
        self.assertIn("Svar fra kildene.", self.texts(other))
        rows = [p for p in self.sent if p["type"] == "answer"]
        self.assertEqual([False, True], [r["cached"] for r in rows])
        self.assertNotEqual(rows[0]["session_id"], rows[1]["session_id"])
        self.assertNotEqual(rows[0]["answer_id"], rows[1]["answer_id"])
        self.assertNotIn("areal_n_asked", other.session_state)  # cache hits do not count

    def test_session_limit_blocks_new_questions_but_not_cached_ones(self) -> None:
        at = self.app().run()
        for i in range(8):
            self.ask(at, f"Spørsmål nummer {i}")
        self.assertEqual(8, len(self.completions.calls))
        self.ask(at, "Spørsmål nummer 8")
        self.assertFalse(at.exception, at.exception)
        self.assertEqual(8, len(self.completions.calls))
        self.assertTrue(any("grensen" in i.value for i in at.info))
        self.assertNotIn("areal_last", at.session_state)
        self.ask(at, "Spørsmål nummer 3")  # cached
        self.assertEqual(8, len(self.completions.calls))
        self.assertIn("Svar fra kildene.", self.texts(at))

    def test_api_failure_shows_friendly_warning_and_logs_error(self) -> None:
        import httpx
        import openai

        def boom(**kwargs):
            raise openai.APIConnectionError(request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"))

        self.completions.create = boom
        at = self.app().run()
        self.ask(at)
        self.assertFalse(at.exception, at.exception)
        self.assertTrue(any("Tjenesten er travel" in w.value for w in at.warning))
        self.assertNotIn("areal_last", at.session_state)
        row = [p for p in self.sent if p["type"] == "answer"][0]
        self.assertEqual("APIConnectionError", row["error"])
        self.assertEqual("", row["answer"])
        self.assertEqual(0, len(self.store[0]))  # failures are not cached

    def test_retrieval_failure_shows_friendly_warning(self) -> None:
        import httpx
        import openai

        def boom(client, query, **kwargs):
            raise openai.RateLimitError(
                "rate limited",
                response=httpx.Response(429, request=httpx.Request("POST", "https://api.openai.com/v1/embeddings")),
                body=None,
            )

        with mock.patch("retrieval.retrieve", boom):
            at = self.app().run()
            self.ask(at)
        self.assertFalse(at.exception, at.exception)
        self.assertTrue(any("Tjenesten er travel" in w.value for w in at.warning))
        self.assertEqual("RateLimitError", [p for p in self.sent if p["type"] == "answer"][0]["error"])
        self.assertEqual(0, len(self.completions.calls))

    def test_rating_form_logs_once_and_is_replaced_by_thanks(self) -> None:
        at = self.app().run()
        self.ask(at)
        answer_id = at.session_state["areal_last"]["answer_id"]
        at.radio(key=f"areal_answered_{answer_id}").set_value("delvis")
        at.radio(key=f"areal_fair_{answer_id}").set_value("ja")
        at.text_area(key=f"areal_comment_{answer_id}").set_value("Mangler tall")
        self.button(at, "Send tilbakemelding").click()
        at.run()
        self.assertFalse(at.exception, at.exception)
        ratings = [p for p in self.sent if p["type"] == "rating"]
        self.assertEqual(1, len(ratings))
        self.assertEqual(
            (answer_id, "delvis", "ja", "Mangler tall"),
            (ratings[0]["answer_id"], ratings[0]["answered_question"], ratings[0]["fair_disagreement"], ratings[0]["comment"]),
        )
        self.assertTrue(any("Takk for tilbakemeldingen" in s.value for s in at.success))
        # Later rerun: answer still there, form gone, nothing resent.
        at.run()
        self.assertIn("Svar fra kildene.", self.texts(at))
        self.assertFalse([b for b in at.button if b.label == "Send tilbakemelding"])
        self.assertEqual(1, len([p for p in self.sent if p["type"] == "rating"]))


if __name__ == "__main__":
    unittest.main()
