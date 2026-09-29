#!/usr/bin/env python3
"""Check that every SSSOM object term exists in the schema it names.

``verify_mappings.py`` only checks that each mapping reached the gist schema;
it cannot see a target that was misspelt, renamed or given the wrong
namespace. This script fetches each target LinkML schema at the commit
pinned in ``TARGETS`` (a sparse fetch of its schema folder only), collects
the IRI and labels of every class, slot, enum and type, and then checks each
row of every ``*.sssom.tsv``:

- the object prefix is a pinned target, bound to the namespace that target's
  schemas declare;
- the object IRI is an element of that target;
- the ``object_label``, when given, is the element's name, title or an alias;
- the ``object_source_version``, when both it and the target's schemas
  declare one, is a version the target declares at that commit.

Re-pin a target (its ``commit``) when the mappings are revised against a
newer release of it. ``--latest`` checks against each target's default
branch instead: the weekly ``upstream-watch.yaml`` runs it to catch a target
that renamed or dropped a mapped term before anyone re-pins. A pin behind
its default branch is noted in the output (as a warning annotation under
GitHub Actions) and in the report, but does not fail the check. Needs
``git`` and network access to GitHub.

Usage::

    python scripts/verify_mapping_targets.py [--latest] [--report FILE]
        [--mappings-dir DIR] [--cache-dir DIR]
"""
from __future__ import annotations

import argparse
import csv
import io
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

DEFAULT_MAPPINGS_DIR = Path(__file__).resolve().parent.parent / "src" / "gist" / "mappings"

# Object prefix -> the lmodel schema it names. ``namespace`` must equal both
# the TSV curie_map entry and the prefix the target's own schemas declare.
TARGETS: dict[str, dict[str, str]] = {
    "common_domain_model": {
        "namespace": "https://w3id.org/lmodel/common-domain-model/",
        "repo": "https://github.com/lmodel/common-domain-model.git",
        "commit": "d01a4734ab79b0be04117765e1a36b6154fa31f8",
        "schema_dir": "src/common_domain_model/schema",
    },
    "dpv": {
        "namespace": "https://w3id.org/lmodel/dpv/",
        "repo": "https://github.com/lmodel/dpv.git",
        "commit": "4ad685aa6ded9cec6f41c205021046f868c7a27c",
        "schema_dir": "src/dpv/schema",
    },
    "iso22989": {
        "namespace": "https://w3id.org/lmodel/iso22989/",
        "repo": "https://github.com/lmodel/iso22989.git",
        "commit": "ad82ffafa38c4dd10ba76fa1d03775c797784a4c",
        "schema_dir": "src/iso22989/schema",
    },
}

_URI_KEYS = {"classes": "class_uri", "slots": "slot_uri", "enums": "enum_uri", "types": "uri"}


def read_sssom(path: Path) -> tuple[dict, list[dict[str, str]]]:
    """Return the ``#`` metadata block (parsed as YAML) and the data rows."""
    meta_lines: list[str] = []
    body: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            meta_lines.append(line[1:])
        elif line.strip():
            body.append(line)
    meta = yaml.safe_load("\n".join(meta_lines)) or {}
    rows = list(csv.DictReader(io.StringIO("\n".join(body)), delimiter="\t"))
    return meta, rows


def fetch(target: dict[str, str], dest: Path, ref: str) -> tuple[Path, str]:
    """Sparse-fetch the target's schema folder at ``ref`` (a commit, or HEAD
    for the default branch) into ``dest``. Returns the folder and the commit."""
    def git(*args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(dest), *args], check=True, capture_output=True, text=True,
        ).stdout.strip()

    if ref != "HEAD" and (dest / ".git").exists() and git("rev-parse", "HEAD") == ref:
        return dest / target["schema_dir"], ref
    dest.mkdir(parents=True, exist_ok=True)
    git("init", "-q")
    if "origin" in git("remote").split():
        git("remote", "remove", "origin")
    git("remote", "add", "origin", target["repo"])
    git("sparse-checkout", "set", "--no-cone", f"/{target['schema_dir']}/**")
    git("fetch", "-q", "--depth", "1", "--filter=blob:none", "origin", ref)
    git("checkout", "-q", "FETCH_HEAD")
    return dest / target["schema_dir"], git("rev-parse", "HEAD")


def load_terms(schema_dir: Path, prefix: str) -> tuple[dict[str, set[str]], set[str], set[str]]:
    """IRI -> labels for every element, the namespaces bound to ``prefix``, and
    the ``version`` values the schemas declare."""
    terms: dict[str, set[str]] = {}
    bound: set[str] = set()
    versions: set[str] = set()
    for f in sorted(schema_dir.rglob("*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        prefixes = {k: (v["prefix_reference"] if isinstance(v, dict) else v)
                    for k, v in (doc.get("prefixes") or {}).items()}
        if prefix in prefixes:
            bound.add(prefixes[prefix])
        if doc.get("version") is not None:
            versions.add(str(doc["version"]))
        default_ns = prefixes.get(doc.get("default_prefix", ""), "")

        def expand(curie: str) -> str:
            p, _, local = curie.partition(":")
            return prefixes[p] + local if p in prefixes and not local.startswith("//") else curie

        for kind, uri_key in _URI_KEYS.items():
            for name, el in (doc.get(kind) or {}).items():
                el = el or {}
                iri = expand(el[uri_key]) if el.get(uri_key) else default_ns + name
                labels = terms.setdefault(iri, set())
                labels.update([name, *(el.get("aliases") or [])])
                if el.get("title"):
                    labels.add(el["title"])
    return terms, bound, versions


def check(mappings_dir: Path, cache_dir: Path, latest: bool = False) -> tuple[list[str], list[str]]:
    """Return the problems, and notes on pins that are behind (``latest`` only)."""
    problems: list[str] = []
    notes: list[str] = []
    loaded: dict[str, dict[str, set[str]]] = {}
    declared_versions: dict[str, set[str]] = {}
    for prefix, target in TARGETS.items():
        ref = "HEAD" if latest else target["commit"]
        schema_dir, commit = fetch(target, cache_dir / ("latest" if latest else "pinned") / prefix, ref)
        if latest and commit != target["commit"]:
            notes.append(f"{prefix}: pinned {target['commit'][:7]}, default branch now {commit[:7]}")
        terms, bound, versions = load_terms(schema_dir, prefix)
        if bound != {target["namespace"]}:
            problems.append(
                f"{prefix}: pinned namespace {target['namespace']} but its schemas bind {sorted(bound)}"
            )
        loaded[prefix] = terms
        declared_versions[prefix] = versions

    for tsv in sorted(mappings_dir.glob("*.sssom.tsv")):
        meta, rows = read_sssom(tsv)
        curie_map = meta.get("curie_map") or {}
        # The set's object_source_version must be one the target declares, when
        # both say one: a re-pin without a metadata bump is caught here.
        source_version = meta.get("object_source_version")
        object_prefixes = {row["object_id"].partition(":")[0] for row in rows}
        for prefix in sorted(object_prefixes & TARGETS.keys()):
            if source_version is not None and declared_versions[prefix]:
                if str(source_version) not in declared_versions[prefix]:
                    problems.append(
                        f"{tsv.name}: object_source_version {source_version!r} is not a version "
                        f"{prefix} declares {sorted(declared_versions[prefix])}"
                    )
        for n, row in enumerate(rows, start=1):
            where = f"{tsv.name} row {n} ({row['subject_id']} {row['predicate_id']} {row['object_id']})"
            prefix, _, local = row["object_id"].partition(":")
            if prefix not in TARGETS:
                problems.append(f"{where}: object prefix {prefix!r} is not a pinned target")
                continue
            ns = TARGETS[prefix]["namespace"]
            if curie_map.get(prefix) != ns:
                problems.append(f"{where}: curie_map binds {prefix!r} to {curie_map.get(prefix)!r}, not {ns}")
            labels = loaded[prefix].get(ns + local)
            if labels is None:
                problems.append(f"{where}: {ns + local} is not an element of {prefix}")
            elif row.get("object_label") and row["object_label"] not in labels:
                problems.append(f"{where}: object_label {row['object_label']!r} is not one of {sorted(labels)}")
    return problems, notes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--mappings-dir", type=Path, default=DEFAULT_MAPPINGS_DIR)
    parser.add_argument("--cache-dir", type=Path, default=None,
                        help="Keep the fetched target schemas here (default: a temporary directory)")
    parser.add_argument("--latest", action="store_true",
                        help="Check against each target's default branch, not its pinned commit")
    parser.add_argument("--report", type=Path, help="Also write a Markdown report to this file")
    args = parser.parse_args(argv)

    if args.cache_dir:
        problems, notes = check(args.mappings_dir, args.cache_dir, args.latest)
    else:
        with tempfile.TemporaryDirectory() as tmp:
            problems, notes = check(args.mappings_dir, Path(tmp), args.latest)

    for p in problems:
        print(f"ERROR: {p}", file=sys.stderr)
    for n in notes:
        # Under GitHub Actions a warning annotation shows on the run summary,
        # where a log line would not be read on a passing run.
        print(f"::warning::pin behind: {n}" if os.environ.get("GITHUB_ACTIONS") else f"NOTE: {n}")
    n_rows = sum(len(read_sssom(t)[1]) for t in args.mappings_dir.glob("*.sssom.tsv"))
    against = f"the default branches of {len(TARGETS)}" if args.latest else f"{len(TARGETS)} pinned"
    summary = (f"Checked {n_rows} mappings against {against} target schemas: "
               f"{len(problems)} problem(s)")
    print(summary)
    if args.report:
        lines = [f"- {summary}."]
        lines += [f"- **{p}**" for p in problems]
        lines += [f"- Pin behind: {n}. Re-pin in `scripts/verify_mapping_targets.py` once the mappings are "
                  f"reviewed against it." for n in notes]
        args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
