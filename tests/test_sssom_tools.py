"""Tests for scripts/apply_sssom_overlay.py and scripts/verify_mappings.py."""
import textwrap

import pytest
import yaml

import apply_sssom_overlay as overlay
import verify_mappings as verify

SA = "https://w3id.org/semanticarts/ns/ontology/gist/"
LM = "https://w3id.org/lmodel/gist/"

SCHEMA = f"""\
id: https://w3id.org/lmodel/gist/test
name: gist_test
prefixes:
  gist: {SA}
  gist_linkml: {LM}
  linkml: https://w3id.org/linkml/
default_prefix: gist_linkml
imports:
  - linkml:types
classes:
  GistThing:
    mixin: true
  Person:
    class_uri: gist:Person
slots:
  has_party:
    slot_uri: gist:hasParty
enums:
  AspectInstance:
    permissible_values:
      _Aspect_mass:
        description: Mass.
"""


def _tsv(rows, gist_ns=SA):
    header = textwrap.dedent(f"""\
        # mapping_set_id: https://example.org/test
        # curie_map:
        #   gist: {gist_ns}
        #   gist_linkml: {LM}
        #   ex: https://example.org/
        #   skos: http://www.w3.org/2004/02/skos/core#
        subject_id\tpredicate_id\tobject_id
        """)
    return header + "".join(f"{s}\t{p}\t{o}\n" for s, p, o in rows)


@pytest.fixture
def project(tmp_path):
    schema_dir = tmp_path / "schema"
    mappings_dir = tmp_path / "mappings"
    schema_dir.mkdir()
    mappings_dir.mkdir()
    (schema_dir / "gist_test.yaml").write_text(SCHEMA)

    def run(rows, gist_ns=SA):
        (mappings_dir / "test.sssom.tsv").write_text(_tsv(rows, gist_ns))
        overlay.main(["--schema-dir", str(schema_dir), "--mappings-dir", str(mappings_dir)])
        status = verify.main(["--schema-dir", str(schema_dir), "--mappings-dir", str(mappings_dir)])
        return status, yaml.safe_load((schema_dir / "gist_test.yaml").read_text())

    return run


class TestMatchByIri:
    def test_slot_matched_by_slot_uri_not_name(self, project):
        status, schema = project([("gist:hasParty", "skos:closeMatch", "ex:party")])
        assert status == 0
        assert schema["slots"]["has_party"]["close_mappings"] == ["ex:party"]

    def test_class_matched_by_class_uri(self, project):
        status, schema = project([("gist:Person", "skos:exactMatch", "ex:Human")])
        assert status == 0
        assert schema["classes"]["Person"]["exact_mappings"] == ["ex:Human"]

    def test_element_without_uri_matched_by_default_prefix(self, project):
        status, schema = project([("gist_linkml:GistThing", "skos:relatedMatch", "ex:Thing")])
        assert status == 0
        assert schema["classes"]["GistThing"]["related_mappings"] == ["ex:Thing"]

    def test_permissible_value_still_matches_after_meaning_is_set(self, project):
        rows = [("gist_linkml:_Aspect_mass", "skos:exactMatch", "ex:mass")]
        status, schema = project(rows)
        assert status == 0
        assert schema["enums"]["AspectInstance"]["permissible_values"]["_Aspect_mass"]["meaning"] == "ex:mass"
        status, _ = project(rows)
        assert status == 0


class TestNamespaceDisagreement:
    def test_subject_in_another_namespace_is_reported(self, project):
        # The TSV says gist: is lmodel's namespace; the schema says Semantic Arts'.
        status, schema = project([("gist:Person", "skos:exactMatch", "ex:Human")], gist_ns=LM)
        assert status == 1
        assert "exact_mappings" not in schema["classes"]["Person"]
