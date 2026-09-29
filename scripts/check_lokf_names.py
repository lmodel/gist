#!/usr/bin/env python3
"""Check that a gist schema file can be imported beside LOKF's lokf.yaml.

LinkML merges every imported element name into one namespace and the last
import wins, so a class, slot, enum, type or subset name the two files share
silently drops one side's definition. The copy is also shipped as a single
file, so it may import nothing but ``linkml:types``.

Usage::

    python scripts/check_lokf_names.py COPY_YAML LOKF_YAML

Exits 1 and names each shared element when there is one. A new shared name
means LOKF has added it since the last release: add a ``--rename`` for it to
``lokf_renames`` in project.justfile.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

_SECTIONS = ("classes", "slots", "enums", "types", "subsets")


def names(schema: dict) -> set[str]:
    """Every element name *schema* defines itself, whatever its section."""
    return {name for section in _SECTIONS for name in (schema.get(section) or {})}


def problems(copy: dict, lokf: dict) -> list[str]:
    found = []
    extra = [i for i in copy.get("imports") or [] if i != "linkml:types"]
    if extra:
        found.append(f"imports {', '.join(extra)}; the copy must stand alone")
    shared = sorted(names(copy) & names(lokf))
    if shared:
        found.append(f"shares element names with lokf.yaml: {', '.join(shared)}")
    return found


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    copy_path, lokf_path = map(Path, args)
    copy = yaml.safe_load(copy_path.read_text(encoding="utf-8"))
    lokf = yaml.safe_load(lokf_path.read_text(encoding="utf-8"))
    found = problems(copy, lokf)
    for problem in found:
        print(f"ERROR: {copy_path.name} {problem}", file=sys.stderr)
    if found:
        return 1
    print(f"{copy_path.name}: no element name shared with lokf.yaml {lokf.get('version', '')}".rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
