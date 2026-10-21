"""Final answer-quality smoke: the nine areal C questions in both synthesis modes.

Runs retrieve + synthesise with the app's settings, sequentially, 18 runs in
total (9 questions x researcher / non_researcher). Saves one JSON file with
per-run answers and quality flags. Run once from the repo root before the workshop:
    python eval/areal_smoke_runs/final_smoke_2026-10-21.py
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "app"))
load_dotenv(REPO / ".env", override=True)

from retrieval import AREAL_DATA_FILE, retrieve  # noqa: E402
from synthesis import synthesise  # noqa: E402

CASES = [
    ("A0", "Hva bestemmer hvor og i hvilket omfang havbruk kan etableres og utvikles, og hvordan avveies hensynet til miljø, næringsutvikling og annen arealbruk i dagens arealforvaltning?"),
    ("A1", "Hvilke faktorer påvirker muligheten for utvikling av havbruk langs kysten, og hvordan samvirker forhold som arealtilgang, tillatelsessystem, arealplanlegging, og miljø- og fiskehelsehensyn?"),
    ("A2", "Hvordan praktiseres søknadsprosessen om lokaliteter, og i hvilke deler av prosessen oppstår søknadsstopp, forsinkelser eller konflikter oftest?"),
    ("A3", "Hvordan vurderes kumulative effekter av akvakulturproduksjon i arealplanlegging og lokaliseringsbeslutninger for havbruk, og hvilke kunnskapsmessige og metodiske utfordringer beskrives?"),
    ("A4", "Hvordan påvirker økonomiske virkemidler og regulering insentivene til arealbruk og lokaliseringsvalg, og hvordan fordeles gevinster og kostnader mellom aktørene?"),
    ("A5", "Hvilket kunnskapsgrunnlag legges til grunn for arealbeslutninger i havbruk, og hvordan kan ny teknologi endre forutsetningene for arealbruk, miljøpåvirkning og lokaliseringsmuligheter?"),
    ("A6", "Hvilke konflikter oppstår i plan- og lokaliseringsprosesser mellom havbruk og andre interesser, og hva bidrar til legitime, effektive og forutsigbare beslutningsprosesser?"),
    ("A7", "Hvilke muligheter har næringen selv for å gjøre sin arealbruk mest mulig effektiv og bærekraftig?"),
    ("A8", "På hvilken måte er biosikkerhet, smittehensyn og vannkontakt mellom anlegg viktig for produksjon og drift av akvakulturanlegg?"),
]

MODES = ["researcher", "non_researcher"]
MODEL = "gpt-6-luna"
ROOM = "areal"
OUTPUT_LANGUAGE = "Norwegian Bokmål"
ANSWER_FORMAT = "freeform"
TOP_K = 10

KORT_SVAR = "**Kort svar**"
BULLET_RE = re.compile(r"^\s*(?:[-*]|\d+\.)\s+\S")
WILD_FISH_TERMS = ("villaks", "villfisk", "vill laksefisk")
YEAR_RE = re.compile(r"(?<!\d)(199\d|200\d|201\d|202[0-7])(?!\d)")
CONNECTORS = {"og", "and", "&", "med", "kolleger", "m.fl.", "et", "al.", "al", "mfl.", "m.fl"}

# Words that are not author surnames (institutions, places, sentence starters).
NOT_SURNAMES = {
    "meld", "st", "nofima", "salt", "ipbes", "gullestad-utvalget", "hordaland",
    "trøndelag", "helgeland", "samtidig", "rapporten", "utvalget",
    "det", "den", "dette", "disse", "denne", "dermed", "blant", "videre",
    "imidlertid", "også", "når", "hvis", "som", "for", "ved", "norge", "norsk",
    "norske", "havbruk", "akvakultur", "kommunene", "regjeringen", "mattilsynet",
    "fiskeridirektoratet", "havforskningsinstituttet", "kystsonen", "ifølge",
}


def _plain(value):
    """Convert numpy scalars and similar to plain JSON types."""
    if value is None:
        return None
    if isinstance(value, (str, bool)):
        return value
    try:
        return float(value) if not float(value).is_integer() else int(value)
    except (TypeError, ValueError):
        return str(value)


def _retrieved_surnames(retrieved: list[dict]) -> set[str]:
    surnames: set[str] = set()
    for doc in retrieved:
        authors = doc.get("authors") or ""
        if isinstance(authors, (list, tuple)):
            authors = "; ".join(str(a) for a in authors)
        for author in str(authors).split(";"):
            parts = author.strip().split()
            if parts:
                surnames.add(parts[-1].strip(",.").lower())
    return surnames


def _citation_names(text: str) -> list[str]:
    """Capitalised name runs directly before a 1990-2027 year, e.g. 'Hersoug, Mikkelsen og Osmundsen (2020)'."""
    names: list[str] = []
    for match in YEAR_RE.finditer(text):
        window = text[max(0, match.start() - 60):match.start()]
        window = re.split(r"\.\s|;|\n|\)", window)[-1]
        words = re.findall(r"[^\s,()]+", window)[-8:]
        run = []
        for word in reversed(words):
            if word[0].isupper() or word.lower() in CONNECTORS:
                run.append(word)
            else:
                break
        names.extend(w.strip(".") for w in run if w[0].isupper() and w.lower() not in CONNECTORS)
    seen: list[str] = []
    for name in names:
        if name not in seen:
            seen.append(name)
    return seen


def analyse_answer(answer: str, retrieved: list[dict]) -> dict:
    text = (answer or "").lstrip()
    lines = text.split("\n")
    kort_svar_ok = False
    if text.startswith(KORT_SVAR):
        header_rest = lines[0][len(KORT_SVAR):].strip()
        i = 1
        while i < len(lines) and not lines[i].strip():
            i += 1  # allow blank lines between the header and the bullets
        block = []
        while i < len(lines) and lines[i].strip():
            block.append(lines[i])
            i += 1
        bullets = [line for line in block if BULLET_RE.match(line)]
        kort_svar_ok = (not header_rest) and len(block) == 3 and len(bullets) == 3
        body = "\n".join(lines[i:])
    else:
        body = text

    body_stripped = body.lstrip()
    surnames = _retrieved_surnames(retrieved)
    suspect = []
    for name in _citation_names(body):
        key = name.lower()
        if key in NOT_SURNAMES or key in surnames:
            continue
        suspect.append(name)

    head = body_stripped[:300].lower()
    return {
        "kort_svar_ok": kort_svar_ok,
        "body_words": len(body.split()),
        "suspect_citations": suspect,
        "opens_with_wild_fish": any(term in head for term in WILD_FISH_TERMS),
    }


def run_one(client: OpenAI, case_id: str, query: str, mode: str) -> dict:
    row = {
        "id": case_id,
        "mode": mode,
        "query": query,
        "latency_s": None,
        "error": None,
        "retrieved": [],
        "answer": "",
    }
    started = time.perf_counter()
    try:
        results = retrieve(client, query, top_k=TOP_K, data_file=AREAL_DATA_FILE)
        row["retrieved"] = [
            {
                "doc_id": r.get("doc_id"),
                "authors": r.get("authors"),
                "year": _plain(r.get("year")),
                "score": _plain(r.get("score")),
            }
            for r in results
        ]
        row["answer"] = synthesise(
            client,
            query=query,
            results=results,
            mode=mode,
            answer_format=ANSWER_FORMAT,
            output_language=OUTPUT_LANGUAGE,
            model=MODEL,
            room=ROOM,
        ) or ""
    except Exception as exc:  # noqa: BLE001
        row["error"] = f"{type(exc).__name__}: {exc}"
    row["latency_s"] = round(time.perf_counter() - started, 2)
    if row["error"] is None:
        row.update(analyse_answer(row["answer"], row["retrieved"]))
    else:
        row.update({"kort_svar_ok": False, "body_words": 0, "suspect_citations": [], "opens_with_wild_fish": False})
    return row


def save(out: Path, stamp: str, records: list[dict]) -> None:
    payload = {
        "run_utc": stamp,
        "model": MODEL,
        "room": ROOM,
        "answer_format": ANSWER_FORMAT,
        "output_language": OUTPUT_LANGUAGE,
        "top_k": TOP_K,
        "n_expected": len(CASES) * len(MODES),
        "n": len(records),
        "results": records,
    }
    out.write_text(json.dumps(payload, indent=1, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set", file=sys.stderr)
        return 2
    client = OpenAI(api_key=api_key, max_retries=3, timeout=120.0)

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    out = REPO / "eval" / "areal_smoke_runs" / f"{stamp}_final_both_modes.json"

    records: list[dict] = []
    for case_id, query in CASES:
        for mode in MODES:
            row = run_one(client, case_id, query, mode)
            records.append(row)
            status = "ERROR " + row["error"] if row["error"] else f"ok kort_svar={row['kort_svar_ok']} words={row['body_words']}"
            print(f"{case_id} {mode:<14} {row['latency_s']}s {status}", flush=True)
            save(out, stamp, records)  # save after every run so paid results survive a crash

    print(f"wrote {out.relative_to(REPO)}", flush=True)
    return 1 if any(r["error"] for r in records) else 0


if __name__ == "__main__":
    raise SystemExit(main())
