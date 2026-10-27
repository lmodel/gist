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
with its regenerated self: Turtle as RDF graphs (isomorphism, see
``tree_signature``), JSON with the date keys removed, other text with the
date lines removed. The Excel
workbook is binary and is skipped. A difference means someone changed the
schema, the mappings or the converter without regenerating and committing
the artefacts. The snapshot is put back afterwards, so the check leaves the
working tree as it found it.

Usage::

    python scripts/check_generated_current.py
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

from rdflib import BNode, Graph
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


def tree_signature(g: Graph) -> Counter | None:
    """The triples of *g*, each blank node replaced by a digest of the tree
    below it, or None when a blank node has two parents or sits on a cycle.

    gen-owl and gen-shacl hang every blank node (a restriction, a property
    shape, a list cell) from one subject, so the blank nodes form trees, and
    two such graphs are isomorphic exactly when their signatures are equal.
    rdflib's isomorphic(), which handles any graph, takes many minutes on the
    shapes' twelve thousand blank nodes; this takes a second.
    """
    below: dict[BNode, list] = defaultdict(list)
    parents: Counter = Counter()
    signature: Counter = Counter()
    for s, p, o in g:
        if isinstance(o, BNode):
            parents[o] += 1
        if isinstance(s, BNode):
            below[s].append((p, o))
        else:
            signature[(s.n3(), p.n3(), o)] += 1
    if any(n > 1 for n in parents.values()):
        return None

    digests: dict[BNode, str] = {}
    for root in [b for b in below if not parents[b]] + list(parents):
        stack, open_ = [(root, False)], set()
        while stack:
            node, done = stack.pop()
            if node in digests:
                continue
            if not done:
                if node in open_:
                    return None
                open_.add(node)
                stack.append((node, True))
                stack.extend((o, False) for _, o in below[node] if isinstance(o, BNode))
                continue
            parts = sorted(
                (p.n3(), digests[o] if isinstance(o, BNode) else o.n3()) for p, o in below[node]
            )
            digests[node] = "_:" + hashlib.sha256(json.dumps(parts).encode()).hexdigest()

    out: Counter = Counter()
    for (s, p, o), n in signature.items():
        out[(s, p, digests[o] if isinstance(o, BNode) else o.n3())] += n
    for b in below:
        if not parents[b]:
            out[("", "", digests[b])] += 1
    return out


def same_graph(before: Graph, after: Graph) -> bool:
    """Whether two graphs are isomorphic, by ``tree_signature`` when both
    have tree-shaped blank nodes, else by rdflib."""
    if len(before) != len(after):
        return False
    sig_before, sig_after = tree_signature(before), tree_signature(after)
    if sig_before is None and sig_after is None:
        return isomorphic(before, after)
    return sig_before == sig_after


def same(before: Path, after: Path) -> bool:
    """Whether two versions of a generated file carry the same content."""
    if not after.exists():
        return False
    suffix = after.suffix
    if suffix == ".ttl":
        return same_graph(Graph().parse(before, format="turtle"), Graph().parse(after, format="turtle"))
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
