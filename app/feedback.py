"""
Answer logging, ratings and the per-session answer cache for the Areal og havbruk room.

Answers and ratings are POSTed as JSON to a Google Apps Script web app whose
URL is the secret FEEDBACK_WEBHOOK_URL. Without the secret, logging is skipped
silently so local development works. Sending runs in a daemon thread with a
short timeout and swallows every error, so it can never slow down or break the UI.

The answer cache lives in the visitor's own `st.session_state` and is never shared:
a participant who repeats a question gets the same answer at once, while every other
participant gets a freshly generated answer.
"""

from __future__ import annotations

import json
import os
import re
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


# A short-answer block opens with a bold label line, in either language.
SHORT_ANSWER_LABELS = ("**Kort svar**", "**Short answer**")
_BULLET_RE = re.compile(r"^\s*(?:[-*]|\d+[.)])\s+\S")
_NUMBERED_RE = re.compile(r"^\s*\d+[.)]\s+\S")
_TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
_HEADING_RE = re.compile(r"^\s*#{1,4}\s+\S")


def split_short_answer(text: str) -> tuple[str, str]:
    """Split an answer into (short_block, rest).

    The short block is the bold label line plus its bullet lines (blank lines are
    allowed between the label and the first bullet). It ends at the first blank line
    or non-bullet line after at least one bullet. Without the label at the start of
    the text, or without any bullet under it, returns ("", text)."""
    text = text or ""
    lines = text.lstrip().split("\n")
    if not lines or lines[0].strip() not in SHORT_ANSWER_LABELS:
        return "", text
    i = 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    first_bullet = i
    while i < len(lines) and _BULLET_RE.match(lines[i]):
        i += 1
    if i == first_bullet:
        return "", text
    short = "\n".join([lines[0].strip()] + lines[first_bullet:i]).strip()
    rest = "\n".join(lines[i:]).strip()
    return short, rest


def answer_shape(text: str) -> str:
    """Comma-joined features of an answer: kort_svar, sections, steps, table. "plain" if none."""
    if not (text or "").strip():
        return ""
    short, rest = split_short_answer(text)
    lines = rest.split("\n")
    features = []
    if short:
        features.append("kort_svar")
    if any(_HEADING_RE.match(line) for line in lines):
        features.append("sections")
    if any(_NUMBERED_RE.match(line) for line in lines):
        features.append("steps")
    if any(_TABLE_ROW_RE.match(line) for line in lines):
        features.append("table")
    return ",".join(features) or "plain"


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
        "answer_words": len((answer or "").split()),
        "answer_shape": answer_shape(answer),
    }


def build_rating_payload(
    *,
    session_id: str,
    answer_id: str,
    thumbs: str = "",
    answered_question: str = "",
    fair_disagreement: str = "",
    comment: str = "",
    length: str = "",
    readability: str = "",
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
        "length": length,
        "readability": readability,
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


# ── Per-session answer cache ──────────────────────────────────────────────────

ANSWER_CACHE_STATE_KEY = "areal_answer_cache"


def answer_cache_key(
    query: str,
    mode: str,
    lang: str,
    top_k: int,
    selected_doc_ids,
    model: str,
) -> tuple:
    return (query.strip(), mode, lang, top_k, tuple(sorted(selected_doc_ids or [])), model)


def session_store() -> tuple[dict, threading.Lock]:
    """The answer cache of the current browser session: a dict and a lock kept in
    `st.session_state`. Nothing is shared between sessions."""
    store = st.session_state.get(ANSWER_CACHE_STATE_KEY)
    if store is None:
        store = ({}, threading.Lock())
        st.session_state[ANSWER_CACHE_STATE_KEY] = store
    return store


def cache_get(key: tuple, store: tuple[dict, threading.Lock] | None = None):
    """Look up an answer in `store` (default: this session's cache)."""
    cache, lock = store or session_store()
    with lock:
        return cache.get(key)


def cache_put(key: tuple, value: tuple, store: tuple[dict, threading.Lock] | None = None) -> None:
    """Store an answer in `store` (default: this session's cache), at most 500 entries."""
    cache, lock = store or session_store()
    with lock:
        if key not in cache and len(cache) >= CACHE_MAX_ENTRIES:
            cache.pop(next(iter(cache)))  # drop the oldest entry
        cache[key] = value
