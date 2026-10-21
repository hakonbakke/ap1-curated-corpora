"""
Answer logging, ratings and the shared answer cache for the Areal og havbruk room.

Answers and ratings are POSTed as JSON to a Google Apps Script web app whose
URL is the secret FEEDBACK_WEBHOOK_URL. Without the secret, logging is skipped
silently so local development works. Sending runs in a daemon thread with a
short timeout and swallows every error, so it can never slow down or break the UI.
"""

from __future__ import annotations

import json
import os
import threading
import urllib.request
from datetime import datetime, timezone

import streamlit as st

WEBHOOK_TIMEOUT_S = 5
CACHE_MAX_ENTRIES = 500


def _webhook_url() -> str:
    url = os.environ.get("FEEDBACK_WEBHOOK_URL", "").strip()
    if url:
        return url
    try:
        return str(st.secrets["FEEDBACK_WEBHOOK_URL"]).strip()
    except Exception:
        return ""


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def build_answer_payload(
    *,
    session_id: str,
    answer_id: str,
    question: str,
    mode: str,
    language: str,
    model: str,
    top_k: int,
    n_active_docs: int,
    retrieved: list[str],
    answer: str,
    latency_s: float,
    cached: bool,
    error: str = "",
    room: str = "areal",
) -> dict:
    return {
        "type": "answer",
        "ts": _now_iso(),
        "session_id": session_id,
        "answer_id": answer_id,
        "room": room,
        "question": question,
        "mode": mode,
        "language": language,
        "model": model,
        "top_k": top_k,
        "n_active_docs": n_active_docs,
        "retrieved": ", ".join(str(d) for d in retrieved),
        "answer": answer,
        "latency_s": round(float(latency_s), 1),
        "cached": bool(cached),
        "error": error,
    }


def build_rating_payload(
    *,
    session_id: str,
    answer_id: str,
    thumbs: str = "",
    answered_question: str = "",
    fair_disagreement: str = "",
    comment: str = "",
) -> dict:
    return {
        "type": "rating",
        "ts": _now_iso(),
        "session_id": session_id,
        "answer_id": answer_id,
        "thumbs": thumbs,
        "answered_question": answered_question,
        "fair_disagreement": fair_disagreement,
        "comment": comment,
    }


def _post(url: str, payload: dict) -> None:
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=WEBHOOK_TIMEOUT_S) as resp:
            resp.read()
    except Exception:
        pass


def send_async(payload: dict, url: str | None = None) -> threading.Thread | None:
    """Fire-and-forget POST. Returns the thread (for tests), or None when no URL is set."""
    try:
        url = _webhook_url() if url is None else url
        if not url:
            return None
        thread = threading.Thread(target=_post, args=(url, payload), daemon=True)
        thread.start()
        return thread
    except Exception:
        return None


def log_answer(**fields) -> None:
    try:
        send_async(build_answer_payload(**fields))
    except Exception:
        pass


def log_rating(**fields) -> None:
    try:
        send_async(build_rating_payload(**fields))
    except Exception:
        pass


# ── Shared answer cache ───────────────────────────────────────────────────────


def answer_cache_key(
    query: str,
    mode: str,
    lang: str,
    top_k: int,
    selected_doc_ids,
    model: str,
) -> tuple:
    return (query.strip(), mode, lang, top_k, tuple(sorted(selected_doc_ids or [])), model)


@st.cache_resource
def _answer_cache() -> tuple[dict, threading.Lock]:
    """One dict and lock shared by every session of this server process."""
    return {}, threading.Lock()


def cache_get(key: tuple, store: tuple[dict, threading.Lock] | None = None):
    cache, lock = store or _answer_cache()
    with lock:
        return cache.get(key)


def cache_put(key: tuple, value: tuple, store: tuple[dict, threading.Lock] | None = None) -> None:
    cache, lock = store or _answer_cache()
    with lock:
        if key not in cache and len(cache) >= CACHE_MAX_ENTRIES:
            cache.pop(next(iter(cache)))  # drop the oldest entry
        cache[key] = value
