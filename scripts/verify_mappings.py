"""Verify that the LinkML schemas reflect the SSSOM mapping TSV files.

The SSSOM TSV files under ``src/<project>/mappings/`` are the
authoritative source of cross-vocabulary mappings. This script reads
them and confirms that the corresponding ``exact_mappings`` /
``close_mappings`` / ``broad_mappings`` / ``narrow_mappings`` /
``related_mappings`` fields are present on the matching elements in
the LinkML schemas under ``src/<project>/schema/`` (recursively, so
module YAMLs are included).

This is a *verifier* (read-only) so that the hand-curated YAML
comments and formatting in the schemas are never disturbed. If a
mapping is in the TSV but missing from the schema (or vice versa) the
script prints a diff and exits non-zero.

Schemas are auto-discovered: every ``*.yaml`` under ``--schema-dir``
is loaded, and each SSSOM subject is expanded to an IRI and matched to
the element with that IRI by the same rule as ``apply_sssom_overlay.py``
(its ``class_uri`` / ``slot_uri`` / ``enum_uri`` or permissible-value
``meaning``, else ``default_prefix:name``). Every element with that IRI,
in any schema, must carry the row's mapping.

Run via ``just verify-mappings`` (or directly:
``python scripts/verify_mappings.py``).
"""

from __future__ import annotations

import argparse
import csv
import io
import sys
from collections import defaultdict
from pathlib import Path

import yaml

from apply_sssom_overlay import (
    _parse_sssom_metadata,
    element_at,
    element_iris,
    expand_curie,
    schema_prefixes,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCHEMA_DIR = REPO_ROOT / "src" / "gist" / "schema"
DEFAULT_MAPPINGS_DIR = REPO_ROOT / "src" / "gist" / "mappings"

PREDICATE_TO_FIELD: dict[str, str] = {
    "skos:exactMatch": "exact_mappings",
    "skos:closeMatch": "close_mappings",
    "skos:broadMatch": "broad_mappings",
    "skos:narrowMatch": "narrow_mappings",
    "skos:relatedMatch": "related_mappings",
}

# Predicates that appear in upstream SSSOM TSVs but do not correspond to
# any LinkML mapping slot; silently skipped to match apply_sssom_overlay.
IGNORED_PREDICATES: frozenset[str] = frozenset(
    {"skos:broader", "skos:narrower", "rdf:type", "owl:equivalentClass"}
)

def parse_sssom_tsv(path: Path) -> list[dict[str, str]]:
    """Return the SSSOM data rows (header comment lines and blanks are skipped)."""
    text_lines = [
        ln
        for ln in path.read_text().splitlines()
        if ln.strip() and not ln.lstrip().startswith("#")
    ]
    reader = csv.DictReader(io.StringIO("\n".join(text_lines)), delimiter="\t")
    return [row for row in reader if row.get("subject_id")]


def expected_mappings(rows: list[dict[str, str]]) -> dict[str, dict[str, set[str]]]:
    """``{subject_curie: {field: {object_curie, ...}}}`` derived from TSV."""
    expected: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for row in rows:
        predicate = row["predicate_id"]
        if predicate in IGNORED_PREDICATES:
            continue
        if predicate not in PREDICATE_TO_FIELD:
            print(
                f"WARNING: unsupported predicate {predicate!r} (subject={row['subject_id']})",
                file=sys.stderr,
            )
            continue
        field = PREDICATE_TO_FIELD[predicate]
        expected[row["subject_id"]][field].add(row["object_id"])
    return expected


def element_mappings(element: dict, key: tuple[str, ...]) -> dict[str, set[str]]:
    """Read mapping fields off a schema element.

    On a permissible value the overlay puts the first exact match in
    ``meaning``, so it counts as an exact mapping there.
    """
    fields = {
        field: set(element.get(field) or [])
        for field in PREDICATE_TO_FIELD.values()
    }
    if len(key) == 3 and element.get("meaning"):
        fields["exact_mappings"].add(element["meaning"])
    return fields


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--schema-dir",
        type=Path,
        default=DEFAULT_SCHEMA_DIR,
        help=f"Directory of LinkML schemas (recursively scanned). Default: {DEFAULT_SCHEMA_DIR}",
    )
    parser.add_argument(
        "--mappings-dir",
        type=Path,
        default=DEFAULT_MAPPINGS_DIR,
        help=f"Directory of *.sssom.tsv files. Default: {DEFAULT_MAPPINGS_DIR}",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Also fail when the schema has mappings that the TSV does not declare.",
    )
    args = parser.parse_args(argv)

    if not args.schema_dir.is_dir():
        print(f"ERROR: schema dir not found: {args.schema_dir}", file=sys.stderr)
        return 2
    if not args.mappings_dir.is_dir():
        print(f"ERROR: mappings dir not found: {args.mappings_dir}", file=sys.stderr)
        return 2

    # Load every schema yaml under schema-dir (recursively so per-extension
    # sub-schemas such as ``extensions/loc.yaml`` are included).
    schemas: list[tuple[Path, dict, dict, dict]] = []
    for path in sorted(args.schema_dir.rglob("*.yaml")):
        try:
            doc = yaml.safe_load(path.read_text())
        except yaml.YAMLError as exc:
            print(f"  WARN: failed to parse {path}: {exc}", file=sys.stderr)
            continue
        if not isinstance(doc, dict):
            continue
        schemas.append((path, doc, element_iris(doc), schema_prefixes(doc)))

    if not schemas:
        print(f"ERROR: no schemas found under {args.schema_dir}", file=sys.stderr)
        return 2

    print(
        f"Loaded {len(schemas)} schema(s) naming "
        f"{len(set().union(*(iris for _, _, iris, _ in schemas)))} element IRIs"
    )

    overall_missing: list[str] = []
    overall_extra: list[str] = []
    overall_unknown: list[str] = []
    total_rows = 0

    for tsv in sorted(args.mappings_dir.glob("*.sssom.tsv")):
        rows = parse_sssom_tsv(tsv)
        total_rows += len(rows)
        print(f"== {tsv.name} ({len(rows)} mappings) ==")
        curie_map = _parse_sssom_metadata(tsv).get("curie_map") or {}
        tsv_prefixes = {str(k): str(v) for k, v in curie_map.items()}

        file_problems = 0
        for subject, fields in sorted(expected_mappings(rows).items()):
            tsv_iri = expand_curie(subject, tsv_prefixes)
            located: list[tuple[Path, str, dict]] = []
            for schema_path, schema_doc, iris, prefixes in schemas:
                iri = tsv_iri or expand_curie(subject, prefixes)
                for key in iris.get(iri or "", ()):
                    element = element_at(schema_doc, key)
                    located.append((schema_path, key, element))
            if not located:
                msg = (
                    f"{tsv.name}: subject {subject} "
                    f"(<{tsv_iri or 'no IRI from curie_map'}>) names no element in any schema"
                )
                overall_unknown.append(msg)
                print(f"  MISSING-ELEMENT: {msg}")
                file_problems += 1
                continue
            for schema_path, key, element in located:
                where = ".".join(key)
                actual = element_mappings(element, key)
                for field, exp_set in fields.items():
                    act_set = actual.get(field, set())
                    missing = exp_set - act_set
                    extra = act_set - exp_set
                    if missing:
                        msg = (
                            f"{schema_path.name}: {where}.{field} "
                            f"missing: {sorted(missing)}"
                        )
                        overall_missing.append(msg)
                        print(f"  MISSING: {msg}")
                        file_problems += 1
                    if extra and args.strict:
                        msg = (
                            f"{schema_path.name}: {where}.{field} "
                            f"extra (not in TSV): {sorted(extra)}"
                        )
                        overall_extra.append(msg)
                        print(f"  EXTRA: {msg}")
                        file_problems += 1
        if file_problems == 0:
            print(f"  OK")

    print()
    print(
        f"Summary: rows={total_rows} missing={len(overall_missing)} "
        f"extra={len(overall_extra)} unknown={len(overall_unknown)}"
    )
    if overall_missing or overall_unknown:
        print(
            "\nApply the missing mappings to the schema YAML, "
            "or remove the rows from the SSSOM TSV.",
            file=sys.stderr,
        )
        return 1
    if overall_extra and args.strict:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
