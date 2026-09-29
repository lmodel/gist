"""Checks on the SSSOM files in src/gist/mappings/ that need no network.

They hold the rules the SSSOM validator (sssom-py) enforces and that the
mappings once broke: metadata that parses, CURIEs where SSSOM wants entity
references, a known justification, labels that match their terms. That the
object terms exist is checked against the pinned target schemas by
``scripts/verify_mapping_targets.py`` (``just verify-mapping-targets``).
"""
import re
from pathlib import Path

import pytest
import rdflib
from rdflib.namespace import SKOS

from .conftest import SEMANTIC_ARTS_NS, UPSTREAM_TTL
from verify_mapping_targets import TARGETS, read_sssom

MAPPINGS_DIR = Path(__file__).parent.parent / "src" / "gist" / "mappings"
TSVS = sorted(MAPPINGS_DIR.glob("*.sssom.tsv"))

# The SSSOM schema's mapping_justification pattern, plus
# semapv:LLMBasedMatching: SEMAPV defines it, but the SSSOM schema up to
# sssom-schema 1.1.0a5 does not list it yet. It is kept because it is the
# truthful provenance of the DPV and ISO/IEC 22989 rows.
JUSTIFICATIONS = {
    f"semapv:{j}" for j in (
        "MappingReview", "ManualMappingCuration", "LogicalReasoning", "LexicalMatching",
        "CompositeMatching", "UnspecifiedMatching", "SemanticSimilarityThresholdMatching",
        "LexicalSimilarityThresholdMatching", "MappingChaining", "MappingInversion",
        "StructuralMatching", "InstanceBasedMatching", "BackgroundKnowledgeBasedMatching",
        "LLMBasedMatching",
    )
}
PREDICATE_LABELS = {
    "skos:exactMatch": "exact match", "skos:closeMatch": "close match",
    "skos:broadMatch": "broad match", "skos:narrowMatch": "narrow match",
    "skos:relatedMatch": "related match",
}
ENTITY_TYPES = {
    "owl class", "owl object property", "owl data property", "owl annotation property",
    "owl named individual", "skos concept", "rdfs resource", "rdfs class", "rdfs literal",
    "rdfs datatype", "rdf property", "composed entity",
}
# Columns and metadata that SSSOM types as entity references: a CURIE in TSV.
ENTITY_COLUMNS = ("subject_id", "predicate_id", "object_id", "mapping_justification",
                  "subject_source", "object_source", "mapping_source",
                  "author_id", "reviewer_id", "creator_id")
ENTITY_METADATA = ("subject_source", "object_source", "mapping_set_source")
CURIE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.-]*:[^\s:/][^\s]*$")
STRING_METADATA = ("mapping_set_version", "subject_source_version", "object_source_version")


@pytest.fixture(scope="module")
def gist_labels() -> dict[str, str]:
    """gist local name -> skos:prefLabel, from the vendored release."""
    g = rdflib.Graph()
    g.parse(UPSTREAM_TTL / "gistCore14.1.0.ttl", format="turtle")
    return {
        str(s)[len(SEMANTIC_ARTS_NS):]: str(o)
        for s, o in g.subject_objects(SKOS.prefLabel)
        if str(s).startswith(SEMANTIC_ARTS_NS)
    }


def test_mapping_files_found():
    assert {t.name for t in TSVS} == {
        "gist-cdm.sssom.tsv", "gist-dpv.sssom.tsv", "gist-iso22989.sssom.tsv",
    }


@pytest.mark.parametrize("tsv", TSVS, ids=lambda p: p.name)
class TestSssomFile:
    def test_metadata(self, tsv):
        meta, _ = read_sssom(tsv)
        for key in ("mapping_set_id", "license", "curie_map", "mapping_date"):
            assert key in meta, f"missing {key}"
        # The file is named after its mapping set.
        set_name = meta["mapping_set_id"].rsplit("/", 1)[-1]
        assert set_name == tsv.name.removesuffix(".sssom.tsv"), f"file name differs from mapping set {set_name}"
        for key in STRING_METADATA:
            if key in meta:
                assert isinstance(meta[key], str), f"{key} must be quoted, or YAML reads a number"
        for key in ENTITY_METADATA:
            if key in meta:
                assert CURIE.match(meta[key]), f"{key} {meta[key]!r} is not a CURIE"
                assert meta[key].split(":", 1)[0] in meta["curie_map"], f"{key} prefix not in curie_map"

    def test_rows(self, tsv, gist_labels):
        meta, rows = read_sssom(tsv)
        curie_map = meta["curie_map"]
        assert rows
        assert curie_map.get("gist") == SEMANTIC_ARTS_NS
        seen = set()
        for row in rows:
            where = f"{row['subject_id']} {row['predicate_id']} {row['object_id']}"
            for col in ENTITY_COLUMNS:
                if row.get(col):
                    assert CURIE.match(row[col]), f"{where}: {col} {row[col]!r} is not a CURIE"
                    assert row[col].split(":", 1)[0] in curie_map, f"{where}: {col} prefix not in curie_map"
            assert row["predicate_id"] in PREDICATE_LABELS, where
            if row.get("predicate_label"):
                assert row["predicate_label"] == PREDICATE_LABELS[row["predicate_id"]], where
            assert row["mapping_justification"] in JUSTIFICATIONS, where
            for col in ("subject_type", "object_type"):
                if row.get(col):
                    assert row[col] in ENTITY_TYPES, f"{where}: {col} {row[col]!r}"

            prefix, _, local = row["subject_id"].partition(":")
            assert prefix == "gist", where
            assert local in gist_labels, f"{where}: no such gist term"
            if row.get("subject_label"):
                assert row["subject_label"] == gist_labels[local], f"{where}: subject_label"

            obj_prefix = row["object_id"].split(":", 1)[0]
            assert obj_prefix in TARGETS, f"{where}: {obj_prefix} is not a pinned target"
            assert curie_map[obj_prefix] == TARGETS[obj_prefix]["namespace"], where

            pair = (row["subject_id"], row["object_id"])
            assert pair not in seen, f"{where}: two predicates for one pair"
            seen.add(pair)
