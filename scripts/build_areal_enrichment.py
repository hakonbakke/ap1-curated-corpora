"""
build_areal_enrichment.py — Read the full texts of the Areal documents once and keep
what the curated summaries leave out.

Three products, all checked against the extracted full text (extracted.md):
  - key figures: verbatim quotes that carry a number, with page where the extract
    has page markers, and a one-line English statement of what the figure measures;
  - chapter summaries for the large reports (>= LARGE_DOC_CHARS), each searchable
    on its own so a point deep in a 500-page report can be found;
  - priority-question notes: one note per (document, A0–A8 tag) on what the full
    text says about that question.

Map: each document is cut into segments (whole chapters where possible) and one
model call per segment returns figures, notes on all nine questions and, for large
reports, a chapter summary. Raw replies are cached per document under
corpora/area-and-aquaculture/enrichment/segments/, so a later retag only needs the
reduce step (--reduce-only).
Reduce: segment notes for each tagged pair are merged into one note.
Check: a figure is kept only when its quote occurs in the full text and the
statement's numbers occur in the quote. In notes and chapter summaries, a sentence
whose numbers do not occur in the source is dropped.

Output: data/area-enrichment.parquet with one row per figure, chapter or note
(embeddings stored as float32 lists).

Usage:
  python scripts/build_areal_enrichment.py                 # all documents
  python scripts/build_areal_enrichment.py --doc 2023_evenset_sameksistens
  python scripts/build_areal_enrichment.py --reduce-only   # reuse cached segments
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = ROOT / "corpora" / "area-and-aquaculture"
DOCS_DIR = CORPUS_DIR / "documents"
CACHE_DIR = CORPUS_DIR / "enrichment" / "segments"
OUT_FILE = ROOT / "data" / "area-enrichment.parquet"
PAGE_FILE = ROOT / "app" / "pages" / "2_Areal_og_havbruk.py"

MODEL = os.getenv("AP1_ENRICH_MODEL", "gpt-6-luna")
EMBEDDING_MODEL = "text-embedding-3-large"
LARGE_DOC_CHARS = 290_000
SEGMENT_MIN, SEGMENT_TARGET, SEGMENT_MAX = 15_000, 50_000, 70_000
WORKERS = 6

PAGE_MARK = re.compile(r"<!--\s*page\s+(\d+)\s*-->", re.I)
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.M)
CHAPTER_HEADING = re.compile(
    r"^(?:\d{1,2}\.?\s+[^\d\s]|(?:chapter|kapittel|del|part)\s+\d|vedlegg|appendix|annex"
    r"|summary for policymakers|sammendrag|summary|executive summary)",
    re.I,
)
REFERENCE_HEADING = re.compile(r"^(?:\d[\d.]*\s+)?(?:references|referanser|litteratur(?:liste)?|kilder|bibliography)\b", re.I)


# ---------------------------------------------------------------- text checks

_QUOTE_CHARS = str.maketrans({"“": '"', "”": '"', "«": '"', "»": '"', "„": '"', "’": "'", "‘": "'",
                              "–": "-", "—": "-", " ": " ", " ": " ", " ": " "})


def normalise(text: str) -> str:
    """Fold case, markdown, quotes, dashes, hyphenation and whitespace so a quote
    copied from the extract still matches after line breaks and formatting."""
    s = unicodedata.normalize("NFKC", text or "").translate(_QUOTE_CHARS).casefold()
    s = s.replace("­", "")
    s = PAGE_MARK.sub(" ", s)
    s = re.sub(r"[*_`#>|]", " ", s)
    s = re.sub(r"(\w)-\s+(\w)", r"\1\2", s)
    return re.sub(r"\s+", " ", s).strip()


def squash(text: str) -> str:
    """normalise() without any spaces. Extracts split words at old line breaks
    ("område regulering") or use soft hyphens as spaces."""
    return normalise(text).replace(" ", "")


_NUMBER = re.compile(r"\d+(?:[ .,]\d+)*")
_YEAR = re.compile(r"(?:19|20)\d\d")


def numbers(text: str) -> set[str]:
    """Numbers as digit strings ("1 539" and "1,539" -> "1539", "0,6" -> "06"),
    ignoring A0–A8 codes and single digits, which are often written as words.
    A run like "3 030 0,597" may be several numbers, so every join of up to six
    neighbouring parts counts ("3030", "0597", ...)."""
    clean = re.sub(r"\bA\d\b", " ", unicodedata.normalize("NFKC", text or "").translate(_QUOTE_CHARS))
    found = set()
    for match in _NUMBER.findall(clean):
        parts = re.split(r"[ .,]", match)
        for i in range(len(parts)):
            for j in range(i, min(len(parts), i + 6)):
                joined = "".join(parts[i:j + 1])
                if len(joined) > 1:
                    found.add(joined)
    return found


def quote_found(quote: str, squashed_source: str) -> bool:
    """`squashed_source` is squash(full text)."""
    q = squash(quote).strip(".\"'")
    if len(q) < 12:
        return False
    if q in squashed_source:
        return True
    parts = [p.strip(".\"'") for p in re.split(r"\.\.\.|…|\[\.\.\.\]", q)]
    parts = [p for p in parts if p]
    return len(parts) > 1 and all(len(p) >= 15 and p in squashed_source for p in parts)


def statement_numbers_ok(statement: str, quote: str, source_numbers: set[str] = frozenset()) -> bool:
    """Every number in the statement is in the quote, except a year the source has."""
    in_quote = numbers(quote)
    return all(n in in_quote or (_YEAR.fullmatch(n) and n in source_numbers) for n in numbers(statement))


def keep_sentences_with_known_numbers(text: str, source_numbers: set[str]) -> tuple[str, int]:
    """Drop sentences that carry a number the source does not have anywhere. This
    catches invented or calculated numbers, not a real number put in the wrong place."""
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-ZÆØÅ\"(])", (text or "").strip())
    kept, dropped = [], 0
    for sentence in sentences:
        if numbers(sentence) <= source_numbers:
            kept.append(sentence)
        else:
            dropped += 1
    return " ".join(kept).strip(), dropped


# ---------------------------------------------------------------- segmentation

def page_of(text: str, pos: int) -> int | None:
    last = None
    for match in PAGE_MARK.finditer(text, 0, pos + 1):
        last = int(match.group(1))
    return last


def _blocks(text: str) -> list[tuple[str, str]]:
    """Cut at heading lines; each block is (heading or '', text)."""
    starts = [m.start() for m in HEADING.finditer(text)]
    if not starts or starts[0] != 0:
        starts = [0] + starts
    blocks = []
    for a, b in zip(starts, starts[1:] + [len(text)]):
        chunk = text[a:b]
        m = HEADING.match(chunk)
        blocks.append((m.group(1).strip() if m else "", chunk))
    return blocks


def _split_long(chunk: str, size: int) -> list[str]:
    paragraphs = re.split(r"(\n\s*\n)", chunk)
    pieces, current = [], ""
    for p in paragraphs:
        if len(current) + len(p) > size and current.strip():
            pieces.append(current)
            current = ""
        while len(p) > size:  # a single paragraph longer than the limit
            pieces.append(p[:size])
            p = p[size:]
        current += p
    if current.strip():
        pieces.append(current)
    return pieces


def segment(text: str) -> list[dict]:
    """Pack heading blocks into segments of about SEGMENT_TARGET characters,
    starting a new segment at a chapter heading once the current one is big
    enough. Reference lists are left out."""
    segments: list[dict] = []
    current: list[tuple[str, str]] = []
    size = 0

    def flush():
        nonlocal current, size
        body = "".join(chunk for _, chunk in current)
        if body.strip():
            headings = [h for h, _ in current if h]
            segments.append({"text": body, "headings": headings})
        current, size = [], 0

    for heading, chunk in _blocks(text):
        is_chapter = bool(heading and CHAPTER_HEADING.match(heading))
        if heading and REFERENCE_HEADING.match(heading):
            continue
        if len(chunk) > SEGMENT_MAX:
            flush()
            for piece in _split_long(chunk, SEGMENT_TARGET):
                current, size = [(heading, piece)], len(piece)
                flush()
            continue
        if size >= SEGMENT_MIN and (is_chapter or size + len(chunk) > SEGMENT_TARGET):
            flush()
        current.append((heading, chunk))
        size += len(chunk)
    flush()

    # Page range of each segment, read from the markers in and before it.
    offset = 0
    for seg in segments:
        start = text.find(seg["text"][:200], offset)
        start = offset if start < 0 else start
        end = start + len(seg["text"])
        seg["page_from"] = page_of(text, start) or (min(map(int, PAGE_MARK.findall(seg["text"])), default=None))
        seg["page_to"] = page_of(text, end)
        offset = end
    return segments


def page_index(text: str) -> list[tuple[int, str]]:
    """(page number, normalised page text) for extracts with page markers."""
    marks = list(PAGE_MARK.finditer(text))
    pages = []
    for m, nxt in zip(marks, marks[1:] + [None]):
        body = text[m.end(): nxt.start() if nxt else len(text)]
        pages.append((int(m.group(1)), squash(body)))
    return pages


def page_for_quote(quote: str, pages: list[tuple[int, str]]) -> int | None:
    probe = squash(quote).strip(".\"'")[:80]
    for number, body in pages:
        if probe in body:
            return number
    for (number, body), (_, following) in zip(pages, pages[1:]):  # quote runs over a page break
        if probe in body + following:
            return number
    return None


# ---------------------------------------------------------------- inputs

def priority_questions() -> dict[str, str]:
    """A0–A8 English texts, read from the FAULTS literal on the Areal page."""
    tree = ast.parse(PAGE_FILE.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "FAULTS" for t in node.targets):
            faults = ast.literal_eval(node.value)
            return {f"A{i}": item[2] for i, item in enumerate(faults["en"])}
    raise RuntimeError("FAULTS not found on the Areal page")


def documents() -> list[dict]:
    docs = []
    for folder in sorted(p for p in DOCS_DIR.iterdir() if p.is_dir()):
        meta_file, text_file = folder / "metadata.yaml", folder / "extracted.md"
        if not (meta_file.exists() and text_file.exists()):
            continue
        meta = yaml.safe_load(meta_file.read_text(encoding="utf-8")) or {}
        docs.append({
            "doc_id": folder.name,
            "title": meta.get("title") or folder.name,
            "year": meta.get("year") or "",
            "authors": meta.get("authors") or [],
            "pqs": [c for c in (meta.get("priority_questions") or []) if re.fullmatch(r"A[0-8]", str(c))],
            "text": text_file.read_text(encoding="utf-8"),
        })
    return docs


# ---------------------------------------------------------------- model calls

MAP_PROMPT = """\
You read one segment of a document for an evidence service on aquaculture and \
coastal area use in Norway. Use only this segment. Reply with JSON only.

Document: {who} ({year}), "{title}". Segment {k} of {n}.
Page markers in the text look like <!-- page N -->.

Priority questions:
{pq_list}

Return:
{{
  "key_figures": [{{"quote": "...", "statement": "..."}}],
  "pq_notes": {{"A0": "...", "A1": "...", "A2": "...", "A3": "...", "A4": "...", "A5": "...", "A6": "...", "A7": "...", "A8": "..."}}{summary_field}
}}

key_figures — up to 12 of the most important quantitative findings in this segment \
(results, counts, shares, amounts, distances, durations, thresholds, rates), the \
authors' own findings before figures they cite from others.
- "quote": one contiguous passage copied verbatim from the segment, 10–60 words, in \
its original language, containing the figure. No ellipses, no edits, no markdown, \
no page markers.
- "statement": one English sentence saying what the figure measures, for what \
place, period and population, and whether it is the authors' finding or cited. \
Write every number exactly as in the quote. Do not round, convert or compute.
- Leave out reference lists, tables of contents, page numbers and captions without \
a finding. Return [] if the segment has no such figures.

pq_notes — for each code, what this segment says that bears on that question: \
findings, arguments, mechanisms, cases, figures, disagreements and caveats. English, \
40–200 words of plain sentences. Say whether a point is the authors' finding, a \
cited study, a legal reading or a policy statement. Keep numbers exactly as written \
and never calculate new ones (no new percentages, sums, differences or ratios). \
Use "" when the segment has nothing on that question; do not stretch.
{summary_rules}
Segment:
<<<
{text}
>>>
"""

SUMMARY_FIELD = ',\n  "chapter_title": "...",\n  "summary": "..."'
SUMMARY_RULES = """
chapter_title — the chapter or section this segment covers, using the document's own heading words where there are any (e.g. "5 Planning and licensing"), at most 12 words.

summary — 180–320 words in English on this segment's content: what it covers, main \
findings and figures (numbers exactly as written, none calculated), method where \
stated, and limits. Plain sentences, no headings.
"""

REDUCE_PROMPT = """\
Below are notes written from consecutive segments of one document, {who} ({year}), \
"{title}". Merge them into one note on this priority question:

{code}: {pq}

Write 120–320 words in English for a researcher: the document's main points on the \
question first, then specifics (cases, figures, mechanisms), then caveats. Keep \
attribution (authors' finding, cited study, legal reading, policy statement). Keep \
numbers exactly as written and never calculate new ones. Mention the chapter or \
section when the notes name it. Do not add anything that is not in the notes. Reply \
with the note text only.

Notes:
{notes}
"""


def who(doc: dict) -> str:
    surnames = [str(a).split()[-1] for a in doc["authors"] if str(a).strip()]
    if not surnames:
        return doc["title"][:60]
    if len(surnames) == 1:
        return surnames[0]
    if len(surnames) == 2:
        return f"{surnames[0]} & {surnames[1]}"
    return f"{surnames[0]} et al."


def chat(client: OpenAI, prompt: str, *, json_mode: bool, max_tokens: int) -> str:
    kwargs = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_completion_tokens": max_tokens,
        "reasoning_effort": "low",
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    for attempt in range(3):
        try:
            return client.chat.completions.create(**kwargs).choices[0].message.content or ""
        except Exception as exc:  # retry transient API errors
            if attempt == 2:
                raise
            print(f"  retry after {type(exc).__name__}: {exc}", file=sys.stderr)
    return ""


def parse_json(reply: str) -> dict:
    match = re.search(r"\{.*\}", reply or "", re.S)
    try:
        return json.loads(match.group(0)) if match else {}
    except json.JSONDecodeError:
        return {}


def map_document(client: OpenAI, doc: dict, pqs: dict[str, str]) -> dict:
    """Run (or load) the per-segment calls for one document."""
    cache_file = CACHE_DIR / f"{doc['doc_id']}.json"
    large = len(doc["text"]) >= LARGE_DOC_CHARS
    segments = segment(doc["text"])
    if cache_file.exists():
        cached = json.loads(cache_file.read_text(encoding="utf-8"))
        if cached.get("n_segments") == len(segments) and cached.get("model") == MODEL:
            return cached
    pq_list = "\n".join(f"{code}: {text}" for code, text in pqs.items())

    def run(k: int, seg: dict) -> dict:
        prompt = MAP_PROMPT.format(
            who=who(doc), year=doc["year"], title=doc["title"], k=k + 1, n=len(segments),
            pq_list=pq_list, text=seg["text"],
            summary_field=SUMMARY_FIELD if large else "",
            summary_rules=SUMMARY_RULES if large else "",
        )
        reply = parse_json(chat(client, prompt, json_mode=True, max_tokens=8000))
        return {
            "index": k,
            "headings": seg["headings"][:6],
            "page_from": seg["page_from"],
            "page_to": seg["page_to"],
            "chars": len(seg["text"]),
            "key_figures": reply.get("key_figures") or [],
            "pq_notes": reply.get("pq_notes") or {},
            "summary": reply.get("summary") or "",
            "chapter_title": reply.get("chapter_title") or "",
        }

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        outputs = sorted(pool.map(lambda pair: run(*pair), enumerate(segments)), key=lambda o: o["index"])
    result = {"doc_id": doc["doc_id"], "model": MODEL, "large": large,
              "n_segments": len(segments), "segments": outputs}
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    return result


def chapter_title(seg: dict) -> str:
    if seg.get("chapter_title"):
        return re.sub(r"[*_`#]", "", str(seg["chapter_title"])).strip()[:120]
    headings = [h for h in seg["headings"] if CHAPTER_HEADING.match(h)] or seg["headings"]
    title = re.sub(r"[*_`]", "", headings[0]).strip() if headings else ""
    return title[:120] or f"Part {seg['index'] + 1}"


def reduce_document(client: OpenAI, doc: dict, mapped: dict, pqs: dict[str, str], stats: dict) -> list[dict]:
    squashed_text = squash(doc["text"])
    pages = page_index(doc["text"])
    source_numbers = numbers(doc["text"])
    rows: list[dict] = []

    seen_quotes: set[str] = set()
    for seg in mapped["segments"]:
        for fig in seg["key_figures"]:
            quote, statement = str(fig.get("quote") or "").strip(), str(fig.get("statement") or "").strip()
            stats["figures_proposed"] += 1
            key = normalise(quote)[:120]
            if not quote or not statement or key in seen_quotes:
                continue
            if (not quote_found(quote, squashed_text) or not numbers(quote)
                    or not statement_numbers_ok(statement, quote, source_numbers)):
                stats["figures_dropped"] += 1
                continue
            seen_quotes.add(key)
            rows.append({"kind": "figure", "doc_id": doc["doc_id"], "pq": "", "title": "",
                         "text": statement, "quote": re.sub(r"\s+", " ", quote),
                         "page_from": page_for_quote(quote, pages) if pages else None, "page_to": None})

        if mapped["large"] and seg["summary"]:
            summary, dropped = keep_sentences_with_known_numbers(seg["summary"], source_numbers)
            stats["sentences_dropped"] += dropped
            if summary:
                rows.append({"kind": "chapter", "doc_id": doc["doc_id"], "pq": "", "title": chapter_title(seg),
                             "text": summary, "quote": "",
                             "page_from": seg["page_from"], "page_to": seg["page_to"]})

    for code in doc["pqs"]:
        notes = [(seg, str(seg["pq_notes"].get(code) or "").strip()) for seg in mapped["segments"]]
        notes = [(seg, note) for seg, note in notes if note]
        if not notes:
            stats["pairs_without_note"].append(f"{doc['doc_id']}:{code}")
            continue
        if len(notes) == 1:
            merged = notes[0][1]
        else:
            listing = "\n\n".join(
                f"[Segment {seg['index'] + 1}{' — ' + chapter_title(seg) if seg['headings'] else ''}]\n{note}"
                for seg, note in notes
            )
            merged = chat(client, REDUCE_PROMPT.format(who=who(doc), year=doc["year"], title=doc["title"],
                                                       code=code, pq=pqs[code], notes=listing),
                          json_mode=False, max_tokens=2000).strip()
        merged, dropped = keep_sentences_with_known_numbers(merged, source_numbers)
        stats["sentences_dropped"] += dropped
        if merged:
            rows.append({"kind": "pq_note", "doc_id": doc["doc_id"], "pq": code, "title": "",
                         "text": merged, "quote": "", "page_from": None, "page_to": None})
    return rows


def embed(client: OpenAI, texts: list[str]) -> list[list[float]]:
    vectors: list[list[float]] = []
    for i in range(0, len(texts), 256):
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts[i:i + 256])
        vectors.extend(item.embedding for item in response.data)
    return vectors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--doc", action="append", help="Only this doc_id (repeatable); other rows are kept.")
    parser.add_argument("--reduce-only", action="store_true", help="Use cached segment replies; no map calls.")
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")
    client = OpenAI()
    pqs = priority_questions()
    docs = [d for d in documents() if not args.doc or d["doc_id"] in args.doc]

    mapped: dict[str, dict] = {}
    if args.reduce_only:
        for doc in docs:
            cache_file = CACHE_DIR / f"{doc['doc_id']}.json"
            if cache_file.exists():
                mapped[doc["doc_id"]] = json.loads(cache_file.read_text(encoding="utf-8"))
    else:
        # A few documents at a time, each with its segments in parallel.
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures = {pool.submit(map_document, client, doc, pqs): doc["doc_id"] for doc in docs}
            for n, future in enumerate(as_completed(futures), 1):
                mapped[futures[future]] = future.result()
                print(f"[{n}/{len(docs)}] {futures[future]}", flush=True)

    stats = {"figures_proposed": 0, "figures_dropped": 0, "sentences_dropped": 0, "pairs_without_note": []}
    rows: list[dict] = []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = [pool.submit(reduce_document, client, doc, mapped[doc["doc_id"]], pqs, stats)
                   for doc in docs if doc["doc_id"] in mapped]
        for future in as_completed(futures):
            rows.extend(future.result())

    new = pd.DataFrame(rows)
    texts = [
        f"{r.title}\n{r.text}" if r.kind == "chapter" else (f"{r.text}\n{r.quote}" if r.kind == "figure" else r.text)
        for r in new.itertuples()
    ]
    new["embedding"] = [np.asarray(v, dtype=np.float32) for v in embed(client, texts)]
    if args.doc and OUT_FILE.exists():
        old = pd.read_parquet(OUT_FILE)
        new = pd.concat([old[~old["doc_id"].isin(args.doc)], new], ignore_index=True)
    new = new.sort_values(["doc_id", "kind", "pq"], kind="stable").reset_index(drop=True)
    new["page_from"] = new["page_from"].astype("Int64")
    new["page_to"] = new["page_to"].astype("Int64")
    new.to_parquet(OUT_FILE, index=False)

    print(f"\nWrote {len(new)} rows to {OUT_FILE.relative_to(ROOT)}")
    print(new["kind"].value_counts().to_string())
    print(f"Figures proposed {stats['figures_proposed']}, dropped by the quote check {stats['figures_dropped']}")
    print(f"Sentences dropped for unknown numbers: {stats['sentences_dropped']}")
    if stats["pairs_without_note"]:
        print("Tagged pairs with nothing in the full text: " + ", ".join(sorted(stats["pairs_without_note"])))


if __name__ == "__main__":
    main()
