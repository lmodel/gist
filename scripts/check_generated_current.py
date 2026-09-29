#!/usr/bin/env python3
"""Check that the committed generated artefacts match a fresh ``just gen-project``.

``main.yaml`` byte-compares ``src/gist/schema/`` because the converter is
deterministic. The artefacts that ``gen-project`` builds from the schema are
not, so they cannot be compared that way:

- the JSON-LD and the Python datamodel embed their generation date;
- the OWL and SHACL Turtle serialise their triples in a different order on
  each run.

This script snapshots every git-tracked file under ``project/`` and
``src/gist/datamodel/``, runs ``just gen-project``, and compares each file
with its regenerated self: Turtle as RDF graphs (isomorphism), JSON with the
date keys removed, other text with the date lines removed. The Excel
workbook is binary and is skipped. A difference means someone changed the
schema, the mappings or the converter without regenerating and committing
the artefacts. The snapshot is put back afterwards, so the check leaves the
working tree as it found it.

Usage::

    python scripts/check_generated_current.py
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from rdflib import Graph
from rdflib.compare import isomorphic

ROOT = Path(__file__).resolve().parent.parent
GENERATED = ("project", "src/gist/datamodel")
SKIPPED_SUFFIXES = {".xlsx"}
DATE_KEYS = {"generation_date", "source_file_date"}
DATE_LINE = re.compile(r"^# Generation date: ")


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--", *GENERATED],
        check=True, capture_output=True, text=True,
    ).stdout
    return out.splitlines()


def _strip_dates(value):
    if isinstance(value, dict):
        return {k: _strip_dates(v) for k, v in value.items() if k not in DATE_KEYS}
    if isinstance(value, list):
        return [_strip_dates(v) for v in value]
    return value


def same(before: Path, after: Path) -> bool:
    """Whether two versions of a generated file carry the same content."""
    if not after.exists():
        return False
    suffix = after.suffix
    if suffix == ".ttl":
        return isomorphic(Graph().parse(before, format="turtle"), Graph().parse(after, format="turtle"))
    if suffix in {".json", ".jsonld"}:
        return _strip_dates(json.loads(before.read_text())) == _strip_dates(json.loads(after.read_text()))
    keep = lambda p: [ln for ln in p.read_text().splitlines() if not DATE_LINE.match(ln)]  # noqa: E731
    return keep(before) == keep(after)


def main() -> int:
    tracked = tracked_files()
    files = [p for p in tracked if Path(p).suffix not in SKIPPED_SUFFIXES]
    with tempfile.TemporaryDirectory() as tmp:
        snapshot = Path(tmp)
        for rel in tracked:
            (snapshot / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, snapshot / rel)
        try:
            subprocess.run(["just", "gen-project"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
            stale = [rel for rel in files if not same(snapshot / rel, ROOT / rel)]
        finally:
            # Put every tracked file back, including the skipped workbook and
            # the stale ones: this is a check, not a regeneration.
            for rel in tracked:
                shutil.copy2(snapshot / rel, ROOT / rel)

    for rel in stale:
        print(f"::error file={rel}::{rel} differs from what 'just gen-project' generates")
    print(f"Compared {len(files)} generated files: {len(stale)} out of date"
          + (". Run 'just gen-project' and commit the result." if stale else ""))
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
