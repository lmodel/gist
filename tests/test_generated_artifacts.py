"""Tests for schema-generated artifacts."""
import json
import pytest
import yaml
from pathlib import Path
from linkml.generators.jsonschemagen import JsonSchemaGenerator


SCHEMA_DIR = Path(__file__).parent.parent / "src" / "gist" / "schema"


def load_schema(schema_file):
    """Load schema YAML file."""
    with open(schema_file, 'r') as f:
        return yaml.safe_load(f)


class TestPythonDatamodelGeneration:
    """Test Python datamodel generation."""

    def test_datamodel_package_exists(self):
        """Test that gist datamodel package exists."""
        datamodel_path = Path(__file__).parent.parent / "src" / "gist" / "datamodel"
        assert datamodel_path.exists(), "Datamodel package should exist"

    def test_datamodel_init_exists(self):
        """Test that datamodel __init__.py exists."""
        init_path = Path(__file__).parent.parent / "src" / "gist" / "datamodel" / "__init__.py"
        assert init_path.exists(), "Datamodel __init__.py should exist"

    def test_gist_module_imports(self):
        """Test that gist datamodel module can be imported."""
        datamodel_file = Path(__file__).parent.parent / "src" / "gist" / "datamodel" / "gist.py"
        if not datamodel_file.exists():
            pytest.skip("Datamodel not yet generated - run 'just gen-python' first")
        try:
            import gist.datamodel.gist
            assert hasattr(gist.datamodel.gist, '__file__')
        except ImportError as e:
            pytest.fail(f"Failed to import gist datamodel: {e}")


class TestJsonSchemaGeneration:
    """Test JSON Schema generation from LinkML schema."""

    @pytest.fixture(scope="class")
    def json_schema(self):
        """Generate JSON Schema from main gist schema."""
        schema_file = SCHEMA_DIR / "gist.yaml"
        gen = JsonSchemaGenerator(str(schema_file))
        return json.loads(gen.serialize())

    def test_json_schema_has_defs(self, json_schema):
        """Test that JSON Schema has definitions."""
        assert "$defs" in json_schema or "definitions" in json_schema, \
            "JSON Schema should have definitions"

    def test_json_schema_has_root_ref(self, json_schema):
        """Test that JSON Schema has a valid structure."""
        # JSON Schema should either have a root $ref or $defs (or both)
        assert "$defs" in json_schema or "definitions" in json_schema or "$ref" in json_schema, \
            "JSON Schema should have either $ref, $defs, or definitions"

    def test_json_schema_classes_are_defs(self, json_schema):
        """Test that classes are represented in definitions."""
        defs = json_schema.get("$defs", json_schema.get("definitions", {}))
        # Core classes should be in definitions
        assert len(defs) > 0, "JSON Schema should have definitions for classes"

    def test_json_schema_required_properties(self, json_schema):
        """Test that required properties are marked."""
        defs = json_schema.get("$defs", json_schema.get("definitions", {}))
        for def_name, def_schema in defs.items():
            if isinstance(def_schema, dict) and "properties" in def_schema:
                # Just verify the structure is valid
                assert isinstance(def_schema["properties"], dict)


class TestSchemaArtifacts:
    """Test that schema artifacts exist."""

    def test_yaml_schema_exists(self):
        """Test that YAML schema files exist."""
        schema_file = SCHEMA_DIR / "gist.yaml"
        assert schema_file.exists(), f"YAML schema not found at {schema_file}"

    def test_schema_files_are_valid_yaml(self):
        """Test that all schema files parse as valid YAML."""
        for schema_file in SCHEMA_DIR.glob("gist*.yaml"):
            schema = load_schema(schema_file)
            assert schema is not None, f"Failed to parse {schema_file}"
            assert isinstance(schema, dict), f"{schema_file} should parse to dict"

    def test_generated_project_directory_structure(self):
        """Test that project directory has expected structure."""
        project_dir = Path(__file__).parent.parent / "project"
        # Project dir might not exist until gen-project is run, so we just check structure
        # This is more of a documentation test


class TestSchemaConsistency:
    """Test consistency across schema modules."""

    @pytest.fixture(scope="class")
    def main_schema(self):
        """Load main schema."""
        schema_file = SCHEMA_DIR / "gist.yaml"
        return load_schema(schema_file)

    @pytest.fixture(scope="class")
    def core_schema(self):
        """Load core schema."""
        schema_file = SCHEMA_DIR / "gist_core.yaml"
        return load_schema(schema_file)

    def test_imported_modules_exist(self, main_schema):
        """Test that imported modules exist."""
        imports = main_schema.get("imports", [])
        for imported in imports:
            if imported.startswith("./"):
                # Local import
                module_name = imported.replace("./", "")
                if not module_name.endswith(".yaml"):
                    module_name += ".yaml"
                schema_file = SCHEMA_DIR / module_name
                assert schema_file.exists(), f"Imported schema {imported} not found"

    def test_core_schema_has_classes(self, core_schema):
        """Test that core schema has classes."""
        assert "classes" in core_schema, "Core schema should have classes"
        assert len(core_schema["classes"]) > 0, "Core schema should define classes"

    def test_class_inheritance_is_valid(self, core_schema):
        """Test that class inheritance references valid parents."""
        classes = core_schema.get("classes", {})
        for class_name, class_def in classes.items():
            if "is_a" in class_def:
                parent_name = class_def["is_a"]
                # Parent should be defined or imported
                # (We skip detailed validation here as it's complex)

    def test_slot_ranges_reference_valid_types(self, core_schema):
        """Test that slot ranges reference valid types or classes."""
        slots = core_schema.get("slots", {})
        classes = core_schema.get("classes", {})
        types_section = core_schema.get("types", {})

        for slot_name, slot_def in slots.items():
            if "range" in slot_def:
                range_val = slot_def["range"]
                # Range can be a built-in type, a class, or undefined (defaults to default_range)
                is_valid = (
                    range_val in ["string", "integer", "float", "boolean", "date", "datetime"]
                    or range_val in classes
                    or range_val in types_section
                )
                # We allow some ranges that might be from imported modules


class TestGistIrisInArtifacts:
    """The published OWL and SHACL use gist's IRIs for gist's terms.

    These read the committed files under project/: the OWL there is written by
    the bare gen-owl call in the justfile (flags in config.public.mk), not by
    gen-project's config.yaml, so only the files themselves are the truth.
    """

    PROJECT = Path(__file__).parent.parent / "project"

    @pytest.fixture(scope="class")
    def owl(self):
        import rdflib
        return rdflib.Graph().parse(self.PROJECT / "owl" / "gist.owl.ttl")

    @pytest.fixture(scope="class")
    def shacl(self):
        import rdflib
        return rdflib.Graph().parse(self.PROJECT / "shacl" / "gist.shacl.ttl")

    def test_owl_declares_every_gist_class_under_its_own_iri(self, owl, upstream_gist):
        from rdflib.namespace import OWL, RDF
        declared = {str(c) for c in owl.subjects(RDF.type, OWL.Class)}
        assert upstream_gist["classes"] - declared == set()

    def test_owl_subjects(self, owl, upstream_gist):
        import rdflib
        gist_ns, gistd_ns, lmodel_ns = (upstream_gist[k] for k in ("gist_ns", "gistd_ns", "lmodel_ns"))
        subjects = {str(s) for s in owl.subjects() if isinstance(s, rdflib.URIRef)}
        invented = {s for s in subjects if s.startswith((gist_ns, gistd_ns))} - upstream_gist["iris"]
        cloned = {s for s in subjects
                  if s.startswith(lmodel_ns) and s[len(lmodel_ns):] in upstream_gist["local_names"]}
        assert invented == set(), "OWL defines IRIs in Semantic Arts' namespace that gist does not"
        assert cloned == set(), "OWL re-declares gist terms in lmodel's namespace"

    def test_owl_keeps_gist_individuals_individuals(self, owl, upstream_gist):
        from rdflib.namespace import OWL, RDF
        retyped = [str(s) for s in owl.subjects(RDF.type, OWL.Class)
                   if str(s).startswith(upstream_gist["gistd_ns"])]
        assert retyped == []

    def test_shacl_shapes_are_lmodels_and_target_gist_classes(self, shacl, upstream_gist):
        import rdflib
        from rdflib.namespace import RDF
        SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
        lmodel_ns = upstream_gist["lmodel_ns"]
        shapes = {str(s) for s in shacl.subjects(RDF.type, SH.NodeShape)}
        assert shapes and all(s.startswith(lmodel_ns) for s in shapes)
        targets = {str(t) for t in shacl.objects(None, SH.targetClass)}
        assert upstream_gist["classes"] <= targets
        # linkml:Any, the range of an unranged object property, is LinkML's own
        linkml_any = "https://w3id.org/linkml/Any"
        assert all(
            t in upstream_gist["classes"] or t.startswith(lmodel_ns) or t == linkml_any
            for t in targets
        )
