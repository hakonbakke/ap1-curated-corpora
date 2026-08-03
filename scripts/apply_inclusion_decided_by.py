"""One-shot: set inclusion_decided_by / added_by per TASKS Task 4 (Thord 2026-08-03)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_paths import doc_dir, list_doc_ids  # noqa: E402

STIGE = "2022_aei_stige-model-sensitivity-calibration"
RAGNAR = "Ragnar Tveterås"
THORD = "Thord Håkon Bakke"


def set_fields(raw: str, decided: str, added: str | None) -> str:
    if re.search(r"^inclusion_decided_by:\s*", raw, re.M):
        raw = re.sub(
            r"^inclusion_decided_by:\s*.*$",
            f"inclusion_decided_by: {decided}",
            raw,
            count=1,
            flags=re.M,
        )
    else:
        raw = raw.rstrip() + f"\n\ninclusion_decided_by: {decided}\n"
    if added is not None:
        if re.search(r"^added_by:\s*", raw, re.M):
            raw = re.sub(
                r"^added_by:\s*.*$",
                f"added_by: {added}",
                raw,
                count=1,
                flags=re.M,
            )
        else:
            raw = raw.rstrip() + f"\nadded_by: {added}\n"
    return raw


def main() -> int:
    n = 0
    for doc_id in list_doc_ids():
        path = doc_dir(doc_id) / "metadata.yaml"
        raw = path.read_text(encoding="utf-8")
        if doc_id == STIGE:
            decided, added = THORD, None
        else:
            decided, added = RAGNAR, "ai_curate_pipeline"
        new = set_fields(raw, decided, added)
        if new != raw:
            path.write_text(new, encoding="utf-8")
            n += 1
            print(f"updated {doc_id} -> {decided}")
    print(f"files changed {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
