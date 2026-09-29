"""Unit tests for scripts/gist_to_linkml.py."""
import textwrap
from pathlib import Path

import pytest
import rdflib
from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS, XSD

import gist_to_linkml as M

# ---------------------------------------------------------------------------
# Convenience namespace shortcuts
# ---------------------------------------------------------------------------

GIST = rdflib.Namespace(M.GIST_SA_NS)
GISTD = rdflib.Namespace(M.GISTD_NS)
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")

# ---------------------------------------------------------------------------
# Helper to build a minimal gist: class triple set
# ---------------------------------------------------------------------------


def _cls(local: str) -> URIRef:
    return GIST[local]


def _prop(local: str) -> URIRef:
    return GIST[local]


def _individual(local: str) -> URIRef:
    return GISTD[local]


# ===========================================================================
# 1. Utility helpers
# ===========================================================================


class TestCamelToSnake:
    def test_pascal_case(self):
        assert M.camel_to_snake("ActingFor") == "acting_for"

    def test_camel_case(self):
        assert M.camel_to_snake("hasPartDirectly") == "has_part_directly"

    def test_single_word(self):
        assert M.camel_to_snake("Thing") == "thing"

    def test_all_lower(self):
        assert M.camel_to_snake("simple") == "simple"

    def test_consecutive_caps(self):
        assert M.camel_to_snake("hasSKOSLabel") == "has_skos_label"

    def test_already_snake(self):
        assert M.camel_to_snake("already_snake") == "already_snake"


class TestLocalName:
    def test_hash_uri(self):
        assert M.local_name(URIRef("http://example.org/ns#Thing")) == "Thing"

    def test_slash_uri(self):
        assert M.local_name(URIRef("https://w3id.org/semanticarts/ns/ontology/gist/Category")) == "Category"

    def test_trailing_slash_preserves_empty(self):
        assert M.local_name(URIRef("http://example.org/ns/")) == ""


class TestGistLocal:
    def test_gist_uri_returns_local(self):
        uri = URIRef(M.GIST_SA_NS + "Category")
        assert M.gist_local(uri) == "Category"

    def test_non_gist_uri_returns_none(self):
        assert M.gist_local(URIRef("http://schema.org/Thing")) is None

    def test_empty_local(self):
        assert M.gist_local(URIRef(M.GIST_SA_NS)) == ""


class TestGistdLocal:
    def test_gistd_uri_returns_local(self):
        uri = URIRef(M.GISTD_NS + "_Aspect_mass")
        assert M.gistd_local(uri) == "_Aspect_mass"

    def test_non_gistd_returns_none(self):
        assert M.gistd_local(URIRef("https://example.org/foo")) is None


class TestMediaCurie:
    def test_application_namespace(self):
        uri = URIRef("https://www.iana.org/assignments/media-types/application/json")
        assert M.media_curie(uri) == "media_app:json"

    def test_image_namespace(self):
        uri = URIRef("https://www.iana.org/assignments/media-types/image/png")
        assert M.media_curie(uri) == "media_img:png"

    def test_text_namespace(self):
        uri = URIRef("https://www.iana.org/assignments/media-types/text/csv")
        assert M.media_curie(uri) == "media_txt:csv"

    def test_unknown_namespace_returns_none(self):
        assert M.media_curie(URIRef("https://example.org/foo")) is None


class TestEnumValKey:
    def test_plain(self):
        assert M._enum_val_key("json") == "JSON"

    def test_strips_leading_underscore(self):
        assert M._enum_val_key("_Aspect_mass") == "ASPECT_MASS"

    def test_plus_becomes_PLUS(self):
        assert M._enum_val_key("ld+json") == "LD_PLUS_JSON"

    def test_special_chars_replaced(self):
        assert M._enum_val_key("rdf+xml") == "RDF_PLUS_XML"

    def test_multiple_underscores_collapsed(self):
        assert M._enum_val_key("__foo__bar__") == "FOO_BAR"

    def test_already_upper(self):
        assert M._enum_val_key("JSON") == "JSON"


# ===========================================================================
# 2. RDF graph helpers
# ===========================================================================


def _make_graph_with_literal(subj, pred, val: str) -> Graph:
    g = Graph()
    g.add((subj, pred, Literal(val)))
    return g


class TestGetLiterals:
    def test_returns_literals(self):
        g = _make_graph_with_literal(GIST.Thing, SKOS.definition, "A definition.")
        assert M.get_literals(g, GIST.Thing, SKOS.definition) == ["A definition."]

    def test_ignores_uri_objects(self):
        g = Graph()
        g.add((GIST.Thing, RDFS.subClassOf, GIST.Entity))
        assert M.get_literals(g, GIST.Thing, RDFS.subClassOf) == []

    def test_empty_graph(self):
        g = Graph()
        assert M.get_literals(g, GIST.Thing, SKOS.definition) == []


class TestFirstLiteral:
    def test_returns_first(self):
        g = _make_graph_with_literal(GIST.Thing, SKOS.definition, "First")
        assert M.first_literal(g, GIST.Thing, SKOS.definition) == "First"

    def test_returns_none_when_absent(self):
        g = Graph()
        assert M.first_literal(g, GIST.Thing, SKOS.definition) is None


class TestNamedObjects:
    def test_returns_only_urirefs(self):
        g = Graph()
        g.add((GIST.A, RDFS.subClassOf, GIST.B))
        g.add((GIST.A, SKOS.definition, Literal("text")))
        result = M.named_objects(g, GIST.A, RDFS.subClassOf)
        assert result == [GIST.B]

    def test_excludes_bnodes(self):
        g = Graph()
        bn = BNode()
        g.add((GIST.A, RDFS.subClassOf, bn))
        assert M.named_objects(g, GIST.A, RDFS.subClassOf) == []


class TestCanonicalGraph:
    def test_iteration_order_is_fixed(self):
        g = Graph()
        for local in ("C", "A", "B"):
            g.add((GIST[local], RDF.type, OWL.Class))
        found = list(M.canonical_graph(g).subjects(RDF.type, OWL.Class))
        assert found == [GIST.A, GIST.B, GIST.C]

    def test_blank_nodes_relabelled_the_same_way_each_time(self):
        def build():
            g = Graph()
            bn = BNode()
            g.add((GIST.A, RDFS.subClassOf, bn))
            g.add((bn, OWL.onProperty, GIST.hasB))
            return g
        assert list(M.canonical_graph(build())) == list(M.canonical_graph(build()))


class TestUnionMembers:
    def test_simple_union(self):
        g = Graph()
        bn = BNode()
        items = [GIST.A, GIST.B]
        col_head = rdflib.collection.Collection(g, None, items)
        g.add((bn, OWL.unionOf, col_head.uri))
        result = M.union_members(g, bn)
        assert set(result) == {GIST.A, GIST.B}

    def test_non_bnode_returns_none(self):
        g = Graph()
        assert M.union_members(g, GIST.A) is None

    def test_bnode_without_union_of(self):
        g = Graph()
        bn = BNode()
        assert M.union_members(g, bn) is None


class TestOwlExprStr:
    def test_gist_uri(self):
        g = Graph()
        result = M.owl_expr_str(g, GIST.Category)
        assert result == "gist:Category"

    def test_owl_uri(self):
        g = Graph()
        result = M.owl_expr_str(g, OWL.Thing)
        assert result.startswith("owl:")

    def test_some_values_from(self):
        g = Graph()
        bn = BNode()
        g.add((bn, OWL.onProperty, GIST.hasA))
        g.add((bn, OWL.someValuesFrom, GIST.Category))
        result = M.owl_expr_str(g, bn)
        assert "hasA" in result
        assert "Category" in result
        assert result.startswith("∃")

    def test_complement_of(self):
        g = Graph()
        bn = BNode()
        g.add((bn, OWL.complementOf, GIST.Category))
        result = M.owl_expr_str(g, bn)
        assert result.startswith("¬")
        assert "Category" in result


# ===========================================================================
# 3. extract_classes
# ===========================================================================


def _core_class_graph() -> Graph:
    """Minimal graph with one gist:Category owl:Class."""
    g = Graph()
    g.add((GIST.Category, RDF.type, OWL.Class))
    g.add((GIST.Category, SKOS.definition, Literal("A category of things.")))
    g.add((GIST.Category, SKOS.prefLabel, Literal("Category")))
    return g


class TestExtractClasses:
    def test_returns_gist_class(self):
        g = _core_class_graph()
        classes = M.extract_classes(g)
        assert "Category" in classes

    def test_description_from_skos(self):
        g = _core_class_graph()
        classes = M.extract_classes(g)
        assert classes["Category"]["description"] == "A category of things."

    def test_aliases_from_pref_label(self):
        g = _core_class_graph()
        classes = M.extract_classes(g)
        assert "Category" in classes["Category"]["aliases"]

    def test_class_uri_set(self):
        g = _core_class_graph()
        classes = M.extract_classes(g)
        assert classes["Category"]["class_uri"] == "gist:Category"

    def test_is_a_from_subclassof(self):
        g = _core_class_graph()
        g.add((GIST.Category, RDFS.subClassOf, GIST.Thing))
        g.add((GIST.Thing, RDF.type, OWL.Class))
        classes = M.extract_classes(g)
        assert classes["Category"]["is_a"] == "Thing"

    def test_non_gist_class_ignored(self):
        g = Graph()
        g.add((URIRef("http://schema.org/Thing"), RDF.type, OWL.Class))
        classes = M.extract_classes(g)
        assert not classes

    def test_blank_node_class_ignored(self):
        g = Graph()
        g.add((BNode(), RDF.type, OWL.Class))
        classes = M.extract_classes(g)
        assert not classes

    def test_deprecated_flag(self):
        g = Graph()
        g.add((GIST.OldClass, RDF.type, OWL.Class))
        g.add((GIST.OldClass, OWL.deprecated, Literal("true")))
        classes = M.extract_classes(g)
        assert classes["OldClass"]["deprecated"] == "true"

    def test_examples_from_skos(self):
        g = _core_class_graph()
        g.add((GIST.Category, SKOS.example, Literal("An example value.")))
        classes = M.extract_classes(g)
        assert {"value": "An example value."} in classes["Category"]["examples"]

    def test_comments_from_scope_note(self):
        g = _core_class_graph()
        g.add((GIST.Category, SKOS.scopeNote, Literal("Use for broad categories.")))
        classes = M.extract_classes(g)
        assert "Use for broad categories." in classes["Category"]["comments"]

    def test_multiple_superclasses_uses_first_as_is_a(self):
        g = _core_class_graph()
        g.add((GIST.Category, RDFS.subClassOf, GIST.Thing))
        g.add((GIST.Category, RDFS.subClassOf, GIST.Topic))
        g.add((GIST.Thing, RDF.type, OWL.Class))
        g.add((GIST.Topic, RDF.type, OWL.Class))
        classes = M.extract_classes(g)
        assert "is_a" in classes["Category"]
        notes_text = " ".join(classes["Category"].get("notes", []))
        assert "Additional named superclasses" in notes_text

    def test_rdfs_comment_definition_prefix(self):
        g = Graph()
        g.add((GIST.Foo, RDF.type, OWL.Class))
        g.add((GIST.Foo, RDFS.comment, Literal("DEFINITION: A foo thing.")))
        classes = M.extract_classes(g)
        assert classes["Foo"]["description"] == "A foo thing."


# ===========================================================================
# 4. extract_slots
# ===========================================================================


def _object_prop_graph() -> Graph:
    g = Graph()
    g.add((GIST.hasParty, RDF.type, OWL.ObjectProperty))
    g.add((GIST.hasParty, SKOS.definition, Literal("Links to a party.")))
    g.add((GIST.hasParty, RDFS.range, GIST.Actor))
    return g


class TestExtractSlots:
    def test_object_property_snake_case_name(self):
        g = _object_prop_graph()
        slots = M.extract_slots(g)
        assert "has_party" in slots

    def test_object_property_multivalued_true(self):
        g = _object_prop_graph()
        slots = M.extract_slots(g)
        assert slots["has_party"].get("multivalued") is True

    def test_object_property_slot_uri(self):
        g = _object_prop_graph()
        slots = M.extract_slots(g)
        assert slots["has_party"]["slot_uri"] == "gist:hasParty"

    def test_object_property_range(self):
        g = _object_prop_graph()
        slots = M.extract_slots(g)
        assert slots["has_party"]["range"] == "Actor"

    def test_datatype_property_xsd_range(self):
        g = Graph()
        g.add((GIST.uniqueText, RDF.type, OWL.DatatypeProperty))
        g.add((GIST.uniqueText, RDFS.range, XSD.string))
        slots = M.extract_slots(g)
        assert slots["unique_text"]["range"] == "string"

    def test_datatype_property_no_multivalued(self):
        g = Graph()
        g.add((GIST.numericValue, RDF.type, OWL.DatatypeProperty))
        g.add((GIST.numericValue, RDFS.range, XSD.decimal))
        slots = M.extract_slots(g)
        assert "multivalued" not in slots["numeric_value"]

    def test_functional_object_property_is_single_valued(self):
        g = Graph()
        g.add((GIST.hasMagnitude, RDF.type, OWL.ObjectProperty))
        g.add((GIST.hasMagnitude, RDF.type, OWL.FunctionalProperty))
        slots = M.extract_slots(g)
        assert slots["has_magnitude"]["multivalued"] is False
        assert "notes" not in slots["has_magnitude"]

    def test_functional_datatype_property_is_single_valued(self):
        g = Graph()
        g.add((GIST.uniqueText, RDF.type, OWL.DatatypeProperty))
        g.add((GIST.uniqueText, RDF.type, OWL.FunctionalProperty))
        slots = M.extract_slots(g)
        assert slots["unique_text"]["multivalued"] is False

    def test_datatype_union_range_becomes_any_of(self):
        g = Graph()
        g.add((GIST.numericValue, RDF.type, OWL.DatatypeProperty))
        bn = BNode()
        col = rdflib.collection.Collection(g, None, [XSD.byte, XSD.long, XSD.decimal, OWL.real])
        g.add((bn, OWL.unionOf, col.uri))
        g.add((GIST.numericValue, RDFS.range, bn))
        slots = M.extract_slots(g)
        entry = slots["numeric_value"]
        assert [a["range"] for a in entry["any_of"]] == ["integer", "decimal"]
        assert "range" not in entry
        assert entry["notes"] == ["OWL range: (xsd:byte | xsd:long | xsd:decimal | owl:real)"]

    def test_datatype_union_of_one_type_becomes_range(self):
        g = Graph()
        g.add((GIST.itemCount, RDF.type, OWL.DatatypeProperty))
        bn = BNode()
        col = rdflib.collection.Collection(g, None, [XSD.int, XSD.integer])
        g.add((bn, OWL.unionOf, col.uri))
        g.add((GIST.itemCount, RDFS.range, bn))
        slots = M.extract_slots(g)
        assert slots["item_count"]["range"] == "integer"
        assert "any_of" not in slots["item_count"]

    def test_transitive_property(self):
        g = Graph()
        g.add((GIST.hasSubPart, RDF.type, OWL.ObjectProperty))
        g.add((GIST.hasSubPart, RDF.type, OWL.TransitiveProperty))
        slots = M.extract_slots(g)
        assert slots["has_sub_part"]["transitive"] is True

    def test_symmetric_property(self):
        g = Graph()
        g.add((GIST.isConnectedTo, RDF.type, OWL.ObjectProperty))
        g.add((GIST.isConnectedTo, RDF.type, OWL.SymmetricProperty))
        slots = M.extract_slots(g)
        assert slots["is_connected_to"]["symmetric"] is True

    def test_inverse_of(self):
        g = Graph()
        g.add((GIST.hasParent, RDF.type, OWL.ObjectProperty))
        g.add((GIST.hasChild, RDF.type, OWL.ObjectProperty))
        g.add((GIST.hasParent, OWL.inverseOf, GIST.hasChild))
        slots = M.extract_slots(g)
        assert slots["has_parent"]["inverse"] == "has_child"

    def test_domain_named_class_becomes_domain_key(self):
        g = Graph()
        g.add((GIST.hasRole, RDF.type, OWL.ObjectProperty))
        g.add((GIST.hasRole, RDFS.domain, GIST.Actor))
        slots = M.extract_slots(g)
        assert slots["has_role"]["domain"] == "Actor"

    def test_domain_union_is_noted_not_a_range(self):
        g = Graph()
        g.add((GIST.owns, RDF.type, OWL.ObjectProperty))
        bn = BNode()
        items = [GIST.Organization, GIST.Person]
        col = rdflib.collection.Collection(g, None, items)
        g.add((bn, OWL.unionOf, col.uri))
        g.add((GIST.owns, RDFS.domain, bn))
        slots = M.extract_slots(g)
        assert "domain" not in slots["owns"]
        assert "any_of" not in slots["owns"]
        assert slots["owns"]["notes"] == ["OWL domain: (gist:Organization | gist:Person)"]

    def test_domain_includes_kept_as_annotation(self):
        g = Graph()
        g.add((GIST.containedText, RDF.type, OWL.DatatypeProperty))
        g.add((GIST.containedText, GIST.domainIncludes, GIST.Text))
        g.add((GIST.containedText, GIST.domainIncludes, GIST.Tag))
        slots = M.extract_slots(g)
        entry = slots["contained_text"]
        assert entry["annotations"]["domain_includes"] == "gist:Tag, gist:Text"
        assert "domain" not in entry  # two hints do not pick one hard domain

    def test_single_domain_includes_fills_absent_domain(self):
        g = Graph()
        g.add((GIST.sequence, RDF.type, OWL.DatatypeProperty))
        g.add((GIST.sequence, GIST.domainIncludes, GIST.OrderedMember))
        slots = M.extract_slots(g)
        assert slots["sequence"]["domain"] == "OrderedMember"

    def test_domain_includes_does_not_override_hard_domain(self):
        g = Graph()
        g.add((GIST.hasRole, RDF.type, OWL.ObjectProperty))
        g.add((GIST.hasRole, RDFS.domain, GIST.Actor))
        g.add((GIST.hasRole, GIST.domainIncludes, GIST.Person))
        slots = M.extract_slots(g)
        assert slots["has_role"]["domain"] == "Actor"
        assert slots["has_role"]["annotations"]["domain_includes"] == "gist:Person"

    def test_range_includes_kept_as_annotation_and_range(self):
        g = Graph()
        g.add((GIST.isMemberOf, RDF.type, OWL.ObjectProperty))
        g.add((GIST.isMemberOf, GIST.rangeIncludes, GIST.Collection))
        g.add((GIST.isMemberOf, GIST.rangeIncludes, GIST.Organization))
        slots = M.extract_slots(g)
        entry = slots["is_member_of"]
        assert entry["annotations"]["range_includes"] == "gist:Collection, gist:Organization"
        assert [a["range"] for a in entry["any_of"]] == ["Collection", "Organization"]

    def test_see_also_on_slot(self):
        g = Graph()
        g.add((GIST.conversionFactor, RDF.type, OWL.DatatypeProperty))
        g.add((GIST.conversionFactor, RDFS.seeAlso, GIST.conversionOffset))
        g.add((GIST.conversionFactor, RDFS.seeAlso, URIRef("https://example.org/units")))
        slots = M.extract_slots(g)
        assert slots["conversion_factor"]["see_also"] == [
            "gist:conversionOffset", "https://example.org/units",
        ]

    def test_slot_reads_rdfs_label_and_prefixed_comments(self):
        g = Graph()
        g.add((GIST.hasParty, RDF.type, OWL.ObjectProperty))
        g.add((GIST.hasParty, RDFS.label, Literal("has party")))
        g.add((GIST.hasParty, RDFS.comment, Literal("DEFINITION: Links to a party.")))
        g.add((GIST.hasParty, RDFS.comment, Literal("EXAMPLE: A buyer.")))
        g.add((GIST.hasParty, RDFS.comment, Literal("NOTE: Not the counterparty.")))
        slots = M.extract_slots(g)
        entry = slots["has_party"]
        assert entry["aliases"] == ["has party"]
        assert entry["description"] == "Links to a party."
        assert entry["examples"] == [{"value": "A buyer."}]
        assert entry["comments"] == ["Not the counterparty."]

    def test_alt_comment_becomes_alias_without_duplicating_skos(self):
        g = Graph()
        g.add((GIST.ElectronicAddress, RDF.type, OWL.Class))
        g.add((GIST.ElectronicAddress, SKOS.prefLabel, Literal("Electronic Address")))
        g.add((GIST.ElectronicAddress, SKOS.altLabel, Literal("Virtual Address")))
        g.add((GIST.ElectronicAddress, RDFS.label, Literal("Electronic Address")))
        g.add((GIST.ElectronicAddress, RDFS.comment, Literal("ALT: Virtual Address")))
        classes = M.extract_classes(g)
        assert classes["ElectronicAddress"]["aliases"] == ["Electronic Address", "Virtual Address"]

    def test_unknown_comment_prefix_kept_verbatim(self):
        g = Graph()
        g.add((GIST.Foo, RDF.type, OWL.Class))
        g.add((GIST.Foo, SKOS.definition, Literal("A foo.")))
        g.add((GIST.Foo, RDFS.comment, Literal("WARNING: Handle with care.")))
        classes = M.extract_classes(g)
        assert classes["Foo"]["comments"] == ["WARNING: Handle with care."]

    def test_qualified_cardinality_rendered(self):
        g = Graph()
        g.add((GIST.Duration, RDF.type, OWL.Class))
        r = BNode()
        g.add((r, RDF.type, OWL.Restriction))
        g.add((r, OWL.onProperty, GIST.hasMagnitude))
        g.add((r, OWL.onClass, GIST.Magnitude))
        g.add((r, OWL.qualifiedCardinality, Literal(1, datatype=XSD.nonNegativeInteger)))
        g.add((GIST.Duration, RDFS.subClassOf, r))
        classes = M.extract_classes(g)
        assert classes["Duration"]["notes"] == [
            "OWL subClassOf restrictions: =1hasMagnitude.gist:Magnitude"
        ]

    def test_non_gist_terms_in_axioms_use_curies(self):
        g = Graph()
        g.add((GIST.Text, RDF.type, OWL.Class))
        r = BNode()
        g.add((r, RDF.type, OWL.Restriction))
        g.add((r, OWL.onProperty, GIST.containedText))
        g.add((r, OWL.someValuesFrom, XSD.string))
        g.add((GIST.Text, RDFS.subClassOf, r))
        classes = M.extract_classes(g)
        assert classes["Text"]["notes"] == ["OWL subClassOf restrictions: ∃containedText.xsd:string"]

    def test_property_disjoint_with_becomes_disjoint_with_key(self):
        g = Graph()
        g.add((GIST.hasGiver, RDF.type, OWL.ObjectProperty))
        g.add((GIST.hasRecipient, RDF.type, OWL.ObjectProperty))
        g.add((GIST.hasGiver, OWL.propertyDisjointWith, GIST.hasRecipient))
        slots = M.extract_slots(g)
        assert slots["has_giver"]["disjoint_with"] == ["has_recipient"]

    def test_inverse_functional_property_annotated(self):
        g = Graph()
        g.add((GIST.isIdentifiedBy, RDF.type, OWL.ObjectProperty))
        g.add((GIST.isIdentifiedBy, RDF.type, OWL.InverseFunctionalProperty))
        slots = M.extract_slots(g)
        assert slots["is_identified_by"]["annotations"]["owl_inverse_functional"] is True

    def test_inverse_functional_property_with_domain_adds_unique_keys(self):
        g = Graph()
        g.add((GIST.Thing, RDF.type, OWL.Class))
        g.add((GIST.uniqueProp, RDF.type, OWL.ObjectProperty))
        g.add((GIST.uniqueProp, RDF.type, OWL.InverseFunctionalProperty))
        g.add((GIST.uniqueProp, RDFS.domain, GIST.Thing))
        classes = M.extract_classes(g)
        uk = classes["Thing"].get("unique_keys", {})
        assert "by_unique_prop" in uk
        assert uk["by_unique_prop"]["unique_key_slots"] == ["unique_prop"]

    def test_class_disjoint_with_becomes_disjoint_with_key(self):
        g = Graph()
        g.add((GIST.Aspect, RDF.type, OWL.Class))
        g.add((GIST.Event, RDF.type, OWL.Class))
        g.add((GIST.Aspect, OWL.disjointWith, GIST.Event))
        classes = M.extract_classes(g)
        assert classes["Aspect"]["disjoint_with"] == ["Event"]

    def test_deprecated_slot(self):
        g = Graph()
        g.add((GIST.oldProp, RDF.type, OWL.ObjectProperty))
        g.add((GIST.oldProp, OWL.deprecated, Literal("true")))
        slots = M.extract_slots(g)
        assert slots["old_prop"]["deprecated"] == "true"

    def test_deprecated_with_superseded_by(self):
        g = Graph()
        GIST_is_superseded = URIRef(M.GIST_SA_NS + "isSupersededBy")
        g.add((GIST.oldProp, RDF.type, OWL.ObjectProperty))
        g.add((GIST.oldProp, OWL.deprecated, Literal("true")))
        g.add((GIST.oldProp, GIST_is_superseded, GIST.newProp))
        slots = M.extract_slots(g)
        assert slots["old_prop"]["deprecated_element_has_exact_replacement"] == "new_prop"

    def test_non_gist_property_ignored(self):
        g = Graph()
        g.add((URIRef("http://schema.org/name"), RDF.type, OWL.DatatypeProperty))
        assert not M.extract_slots(g)

    def test_union_range_becomes_any_of(self):
        g = Graph()
        g.add((GIST.hasRelated, RDF.type, OWL.ObjectProperty))
        bn = BNode()
        items = [GIST.A, GIST.B]
        col = rdflib.collection.Collection(g, None, items)
        g.add((bn, OWL.unionOf, col.uri))
        g.add((GIST.hasRelated, RDFS.range, bn))
        slots = M.extract_slots(g)
        any_of = slots["has_related"].get("any_of", [])
        ranges = {entry["range"] for entry in any_of}
        assert "A" in ranges
        assert "B" in ranges


# ===========================================================================
# 5. extract_enums
# ===========================================================================


class TestExtractEnums:
    def test_gistd_individual_creates_enum(self):
        g = Graph()
        ind = GISTD["_Aspect_mass"]
        g.add((ind, RDF.type, GIST.Aspect))
        enums = M.extract_enums(g)
        assert "AspectInstance" in enums

    def test_enum_value_key_upper_snake(self):
        g = Graph()
        ind = GISTD["_Aspect_mass"]
        g.add((ind, RDF.type, GIST.Aspect))
        enums = M.extract_enums(g)
        pv = enums["AspectInstance"]["permissible_values"]
        assert "ASPECT_MASS" in pv

    def test_enum_meaning_set(self):
        g = Graph()
        ind = GISTD["_Aspect_mass"]
        g.add((ind, RDF.type, GIST.Aspect))
        enums = M.extract_enums(g)
        pv = enums["AspectInstance"]["permissible_values"]
        assert pv["ASPECT_MASS"]["meaning"] == "gistd:_Aspect_mass"

    def test_media_type_individual(self):
        g = Graph()
        ind = URIRef("https://www.iana.org/assignments/media-types/application/json")
        media_type_class = GIST.MediaType
        g.add((ind, RDF.type, media_type_class))
        g.add((ind, SKOS.prefLabel, Literal("JSON")))
        enums = M.extract_enums(g)
        assert "MediaTypeInstance" in enums
        pv = enums["MediaTypeInstance"]["permissible_values"]
        assert "JSON" in pv

    def test_owl_schema_type_not_grouped_as_enum(self):
        g = Graph()
        g.add((GIST.Category, RDF.type, OWL.Class))
        enums = M.extract_enums(g)
        assert not enums

    def test_enum_description_from_skos(self):
        g = Graph()
        ind = GISTD["_Aspect_mass"]
        g.add((ind, RDF.type, GIST.Aspect))
        g.add((ind, SKOS.definition, Literal("The mass aspect.")))
        enums = M.extract_enums(g)
        pv = enums["AspectInstance"]["permissible_values"]
        assert pv["ASPECT_MASS"]["description"] == "The mass aspect."

    def test_enum_value_keeps_editorial_note_and_label_once(self):
        g = Graph()
        ind = GISTD["_Aspect_mass"]
        g.add((ind, RDF.type, GIST.Aspect))
        g.add((ind, SKOS.prefLabel, Literal("mass")))
        g.add((ind, RDFS.label, Literal("mass")))
        g.add((ind, SKOS.editorialNote, Literal("Duplicated from reference data.")))
        pv = M.extract_enums(g)["AspectInstance"]["permissible_values"]["ASPECT_MASS"]
        assert pv["title"] == "mass"
        assert "aliases" not in pv
        assert pv["notes"] == ["Duplicated from reference data."]

    def test_media_type_literal_becomes_annotation(self):
        g = Graph()
        ind = URIRef("https://www.iana.org/assignments/media-types/application/json")
        g.add((ind, RDF.type, GIST.MediaType))
        g.add((ind, GIST.uniqueText, Literal("application/json")))
        pv = M.extract_enums(g)["MediaTypeInstance"]["permissible_values"]["JSON"]
        assert pv["annotations"] == {"unique_text": "application/json"}


# ===========================================================================
# 6. extract_rdfs_annotations
# ===========================================================================


class TestExtractRdfsAnnotations:
    def test_label_becomes_aliases(self):
        g = Graph()
        g.add((GIST.Category, RDFS.label, Literal("Category Label")))
        classes, slots = M.extract_rdfs_annotations(g)
        assert "Category" in classes
        assert "Category Label" in classes["Category"]["aliases"]

    def test_definition_prefix(self):
        g = Graph()
        g.add((GIST.Category, RDFS.comment, Literal("DEFINITION: A category.")))
        classes, slots = M.extract_rdfs_annotations(g)
        assert classes["Category"]["description"] == "A category."

    def test_example_prefix(self):
        g = Graph()
        g.add((GIST.Category, RDFS.comment, Literal("EXAMPLE: Thing A is a Category.")))
        classes, slots = M.extract_rdfs_annotations(g)
        assert {"value": "Thing A is a Category."} in classes["Category"]["examples"]

    def test_note_prefix_goes_to_comments(self):
        g = Graph()
        g.add((GIST.Category, RDFS.comment, Literal("NOTE: Use carefully.")))
        classes, slots = M.extract_rdfs_annotations(g)
        assert "Use carefully." in classes["Category"]["comments"]

    def test_property_classified_as_slot_with_ctx(self):
        g = Graph()
        g.add((GIST.hasParty, RDFS.label, Literal("has party")))

        ctx = Graph()
        ctx.add((GIST.hasParty, RDF.type, OWL.ObjectProperty))

        classes, slots = M.extract_rdfs_annotations(g, ctx=ctx)
        assert "has_party" in slots
        assert "hasParty" not in classes

    def test_unknown_type_defaults_to_class(self):
        g = Graph()
        g.add((GIST.Obscure, RDFS.label, Literal("Obscure")))
        classes, slots = M.extract_rdfs_annotations(g, ctx=None)
        assert "Obscure" in classes


class TestExtractRdfsAnnotationEnums:
    def test_individuals_grouped_by_context_type(self):
        g = Graph()
        aspect = GISTD["_Aspect_mass"]
        media = URIRef("https://www.iana.org/assignments/media-types/text/csv")
        g.add((aspect, RDFS.label, Literal("mass")))
        g.add((aspect, RDFS.comment, Literal("DEFINITION: The aspect mass.")))
        g.add((media, RDFS.label, Literal("CSV")))
        g.add((GIST.Category, RDFS.label, Literal("Category")))  # a class, not an individual
        ctx = Graph()
        ctx.add((aspect, RDF.type, GIST.Aspect))
        ctx.add((media, RDF.type, GIST.MediaType))
        enums = M.extract_rdfs_annotation_enums(g, ctx=ctx)
        assert set(enums) == {"AspectInstance", "MediaTypeInstance"}
        assert enums["AspectInstance"]["permissible_values"]["ASPECT_MASS"] == {
            "title": "mass", "description": "The aspect mass.", "meaning": "gistd:_Aspect_mass",
        }
        assert enums["MediaTypeInstance"]["permissible_values"]["CSV"]["meaning"] == "media_txt:csv"

    def test_untyped_individual_left_out(self):
        g = Graph()
        g.add((GISTD["_Aspect_mass"], RDFS.label, Literal("mass")))
        assert M.extract_rdfs_annotation_enums(g, ctx=Graph()) == {}


# ===========================================================================
# 7. extract_sub_class_assertions
# ===========================================================================


class TestExtractSubClassAssertions:
    def test_basic_is_a(self):
        g = Graph()
        g.add((GIST.Category, RDFS.subClassOf, GIST.Thing))
        classes = M.extract_sub_class_assertions(g)
        assert classes["Category"]["is_a"] == "Thing"

    def test_root_parent_added(self):
        g = Graph()
        g.add((GIST.Category, RDFS.subClassOf, GIST.Thing))
        classes = M.extract_sub_class_assertions(g)
        assert "Thing" in classes

    def test_root_parent_has_no_is_a(self):
        g = Graph()
        g.add((GIST.Category, RDFS.subClassOf, GIST.Thing))
        classes = M.extract_sub_class_assertions(g)
        assert "is_a" not in classes["Thing"]

    def test_class_uri_set(self):
        g = Graph()
        g.add((GIST.Category, RDFS.subClassOf, GIST.Thing))
        classes = M.extract_sub_class_assertions(g)
        assert classes["Category"]["class_uri"] == "gist:Category"

    def test_non_gist_subjects_ignored(self):
        g = Graph()
        g.add((URIRef("http://schema.org/Cat"), RDFS.subClassOf, GIST.Thing))
        classes = M.extract_sub_class_assertions(g)
        assert not any(k for k in classes if "Cat" in k and "gist" not in k)

    def test_blank_node_subjects_ignored(self):
        g = Graph()
        g.add((BNode(), RDFS.subClassOf, GIST.Thing))
        classes = M.extract_sub_class_assertions(g)
        assert not classes

    def test_multiple_parents_noted(self):
        g = Graph()
        g.add((GIST.Sub, RDFS.subClassOf, GIST.ParentA))
        g.add((GIST.Sub, RDFS.subClassOf, GIST.ParentB))
        classes = M.extract_sub_class_assertions(g)
        notes = " ".join(classes["Sub"].get("notes", []))
        assert "additional subClassOf" in notes.lower() or "ParentB" in notes or "ParentA" in notes


# ===========================================================================
# 8. extract_prefix_declarations
# ===========================================================================


class TestExtractPrefixDeclarations:
    def _make_prefix_graph(self) -> Graph:
        g = Graph()
        decl = GIST["_PrefixDeclaration_gist"]
        g.add((decl, RDF.type, SH.PrefixDeclaration))
        g.add((decl, SH.prefix, Literal("gist")))
        g.add((decl, SH.namespace, Literal("https://w3id.org/semanticarts/ns/ontology/gist/")))
        return g

    def test_returns_pv_entry(self):
        pv = M.extract_prefix_declarations(self._make_prefix_graph())
        assert "PREFIXDECLARATION_GIST" in pv

    def test_title_is_prefix(self):
        pv = M.extract_prefix_declarations(self._make_prefix_graph())
        entry = pv["PREFIXDECLARATION_GIST"]
        assert entry["title"] == "gist"

    def test_description_contains_namespace(self):
        pv = M.extract_prefix_declarations(self._make_prefix_graph())
        entry = pv["PREFIXDECLARATION_GIST"]
        assert "https://w3id.org/semanticarts/ns/ontology/gist/" in entry["description"]

    def test_meaning_set(self):
        pv = M.extract_prefix_declarations(self._make_prefix_graph())
        assert "meaning" in pv["PREFIXDECLARATION_GIST"]


# ===========================================================================
# 9. YAML output helpers
# ===========================================================================


class TestOrderKeys:
    def test_canonical_order(self):
        d = {"classes": {}, "id": "x", "name": "y", "prefixes": {}}
        ordered = M._order_keys(d, M._SCHEMA_KEY_ORDER)
        keys = list(ordered.keys())
        assert keys.index("id") < keys.index("name")
        assert keys.index("name") < keys.index("prefixes")
        assert keys.index("prefixes") < keys.index("classes")

    def test_extra_keys_appended(self):
        d = {"id": "x", "extra_key": "v"}
        ordered = M._order_keys(d, M._SCHEMA_KEY_ORDER)
        assert "extra_key" in ordered
        assert list(ordered.keys())[-1] == "extra_key"

    def test_missing_canonical_keys_not_inserted(self):
        d = {"name": "x"}
        ordered = M._order_keys(d, M._SCHEMA_KEY_ORDER)
        assert list(ordered.keys()) == ["name"]


class TestOrderElements:
    def test_in_subset_added_when_subset_name_given(self):
        elements = {"Foo": {"description": "A foo."}}
        result = M._order_elements(elements, "my_subset")
        assert result["Foo"]["in_subset"] == ["my_subset"]

    def test_existing_in_subset_not_overwritten(self):
        elements = {"Foo": {"in_subset": ["existing"]}}
        result = M._order_elements(elements, "my_subset")
        assert result["Foo"]["in_subset"] == ["existing"]

    def test_no_subset_when_none(self):
        elements = {"Foo": {}}
        result = M._order_elements(elements, None)
        assert "in_subset" not in result["Foo"]

    def test_key_order_applied(self):
        elements = {"Foo": {"in_subset": [], "description": "d", "is_a": "Bar"}}
        result = M._order_elements(elements, None)
        keys = list(result["Foo"].keys())
        assert keys.index("is_a") < keys.index("description")


class TestTagEnums:
    def test_adds_in_subset(self):
        enums = {"MyEnum": {"description": "x", "permissible_values": {}}}
        result = M._tag_enums(enums, "my_subset")
        assert result["MyEnum"]["in_subset"] == ["my_subset"]

    def test_preserves_existing_keys(self):
        enums = {"MyEnum": {"description": "x"}}
        result = M._tag_enums(enums, "s")
        assert result["MyEnum"]["description"] == "x"


class TestAddBlankLines:
    def test_blank_before_section_key(self):
        text = "id: x\nprefixes:\n  foo: bar"
        result = M._add_blank_lines(text)
        lines = result.split("\n")
        prefix_idx = next(i for i, l in enumerate(lines) if l.startswith("prefixes:"))
        assert lines[prefix_idx - 1] == ""

    def test_blank_between_element_entries(self):
        text = "classes:\n  Foo:\n    description: a\n  Bar:\n    description: b"
        result = M._add_blank_lines(text)
        lines = result.split("\n")
        bar_idx = next(i for i, l in enumerate(lines) if l.startswith("  Bar:"))
        assert lines[bar_idx - 1] == ""

    def test_no_double_blank_lines(self):
        text = "id: x\n\n\nprefixes:\n  foo: bar"
        result = M._add_blank_lines(text)
        lines = result.split("\n")
        for i in range(len(lines) - 1):
            assert not (lines[i] == "" and lines[i + 1] == ""), \
                f"Double blank at lines {i} and {i+1}"

    def test_no_blank_before_list_items(self):
        text = "imports:\n- linkml:types\n- ./gist_core"
        result = M._add_blank_lines(text)
        lines = result.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("- ") and i > 0:
                assert lines[i - 1] != "", f"Unexpected blank before list item at line {i}"


class TestDumpYaml:
    def test_key_order_preserved(self):
        schema = M._order_keys({"id": "x", "name": "y", "classes": {}}, M._SCHEMA_KEY_ORDER)
        text = M.dump_yaml(schema)
        id_pos = text.index("id:")
        name_pos = text.index("name:")
        assert id_pos < name_pos

    def test_long_string_uses_block_style(self):
        schema = {"description": "x" * 90}
        text = M.dump_yaml(schema)
        assert "|" in text

    def test_short_string_inline(self):
        schema = {"name": "short"}
        text = M.dump_yaml(schema)
        assert "name: short" in text

    def test_sort_keys_false(self):
        schema = {"z_key": 1, "a_key": 2}
        text = M.dump_yaml(schema)
        assert text.index("z_key") < text.index("a_key")


# ===========================================================================
# 10. Schema assembly functions
# ===========================================================================


class TestBuildSchema:
    def _make_schema(self, **kw):
        return M.build_schema(
            classes={"Thing": {"description": "Root thing."}},
            slots={"has_name": {"range": "string"}},
            enums={"MyEnum": {"description": "e", "permissible_values": {}}},
            **kw,
        )

    def test_required_top_level_keys(self):
        s = self._make_schema()
        for key in ("id", "name", "prefixes", "imports", "classes", "slots", "enums", "subsets"):
            assert key in s, f"Missing key: {key}"

    def test_canonical_key_order(self):
        s = self._make_schema()
        keys = list(s.keys())
        assert keys.index("id") < keys.index("name")
        assert keys.index("prefixes") < keys.index("classes")
        assert keys.index("subsets") < keys.index("enums")

    def test_gist_core_subset_declared(self):
        s = self._make_schema()
        assert "gist_core" in s["subsets"]

    def test_elements_tagged_with_subset(self):
        s = self._make_schema()
        assert s["classes"]["Thing"]["in_subset"] == ["gist_core"]
        assert s["slots"]["has_name"]["in_subset"] == ["gist_core"]

    def test_enum_tagged_with_subset(self):
        s = self._make_schema()
        assert s["enums"]["MyEnum"]["in_subset"] == ["gist_core"]

    def test_license_cc_by(self):
        s = self._make_schema()
        assert s["license"] == "CC-BY-4.0"

    def test_header_fills_description_license_notes_and_see_also(self):
        header = {
            "description": "gist is a minimalist upper ontology created by Semantic Arts.",
            "license": "https://creativecommons.org/licenses/by/4.0/",
            "notes": ["History: gist 14.1.0 released 2026-Apr-17."],
            "see_also": ["https://w3id.org/semanticarts/ontology/gistCore14.1.0"],
        }
        s = M.build_schema({}, {}, {}, header=header)
        assert s["description"].startswith("gist is a minimalist upper ontology")
        assert s["description"].endswith("generated from gistCore 14.1.0.")
        assert s["license"] == "https://creativecommons.org/licenses/by/4.0/"
        assert s["notes"] == ["History: gist 14.1.0 released 2026-Apr-17."]
        assert s["see_also"][-1] == "https://w3id.org/semanticarts/ontology/gistCore14.1.0"
        keys = list(s)
        assert keys.index("description") < keys.index("notes") < keys.index("license")

    def test_source_included_when_given(self):
        s = self._make_schema(source="https://example.org/onto")
        assert s["source"] == "https://example.org/onto"

    def test_source_omitted_when_none(self):
        s = self._make_schema(source=None)
        assert "source" not in s

    def test_imports_linkml_types(self):
        s = self._make_schema()
        assert "linkml:types" in s["imports"]


class TestBuildMediaTypesSchema:
    def _make_schema(self, **kw):
        enums = {"MediaTypeInstance": {"description": "d", "permissible_values": {"JSON": {}}}}
        return M.build_media_types_schema(enums, **kw)

    def test_imports_gist_core(self):
        s = self._make_schema()
        assert "./gist_core" in s["imports"]

    def test_subset_gist_media_types(self):
        s = self._make_schema()
        assert "gist_media_types" in s["subsets"]

    def test_enum_tagged(self):
        s = self._make_schema()
        assert s["enums"]["MediaTypeInstance"]["in_subset"] == ["gist_media_types"]

    def test_no_classes_or_slots(self):
        s = self._make_schema()
        assert "classes" not in s
        assert "slots" not in s


class TestBuildPrefixDeclarationsSchema:
    def _make_schema(self, **kw):
        pv = {"GIST": {"title": "gist", "description": "d", "meaning": "gist:_PrefixDeclaration_gist"}}
        return M.build_prefix_declarations_schema(pv, **kw)

    def test_prefix_declaration_instance_enum(self):
        s = self._make_schema()
        assert "PrefixDeclarationInstance" in s["enums"]

    def test_subset_declared(self):
        s = self._make_schema()
        assert "gist_prefix_declarations" in s["subsets"]

    def test_no_classes_or_slots(self):
        s = self._make_schema()
        assert "classes" not in s
        assert "slots" not in s


class TestBuildRdfsAnnotationsSchema:
    def _make_schema(self, **kw):
        classes = {"Foo": {"class_uri": "gist:Foo"}}
        slots = {"has_foo": {"slot_uri": "gist:hasFoo"}}
        return M.build_rdfs_annotations_schema(classes, slots, **kw)

    def test_has_classes_and_slots(self):
        s = self._make_schema()
        assert "Foo" in s["classes"]
        assert "has_foo" in s["slots"]

    def test_no_enums(self):
        s = self._make_schema()
        assert "enums" not in s

    def test_subset_declared(self):
        s = self._make_schema()
        assert "gist_rdfs_annotations" in s["subsets"]

    def test_elements_tagged(self):
        s = self._make_schema()
        assert s["classes"]["Foo"]["in_subset"] == ["gist_rdfs_annotations"]


class TestBuildSubClassAssertionsSchema:
    def _make_schema(self, **kw):
        classes = {
            "Category": {"class_uri": "gist:Category", "is_a": "Thing"},
            "Thing": {"class_uri": "gist:Thing"},
        }
        return M.build_sub_class_assertions_schema(classes, **kw)

    def test_has_classes(self):
        s = self._make_schema()
        assert "Category" in s["classes"]

    def test_no_slots_or_enums(self):
        s = self._make_schema()
        assert "slots" not in s
        assert "enums" not in s

    def test_subset_declared(self):
        s = self._make_schema()
        assert "gist_sub_class_assertions" in s["subsets"]

    def test_elements_tagged(self):
        s = self._make_schema()
        assert s["classes"]["Category"]["in_subset"] == ["gist_sub_class_assertions"]


class TestBuildGistSchema:
    def test_imports_core(self):
        s = M.build_gist_schema()
        assert "./gist_core" in s["imports"]

    def test_imports_media_types(self):
        s = M.build_gist_schema()
        assert "./gist_media_types" in s["imports"]

    def test_imports_prefix_declarations(self):
        s = M.build_gist_schema()
        assert "./gist_prefix_declarations" in s["imports"]

    def test_no_classes_slots_enums(self):
        s = M.build_gist_schema()
        assert "classes" not in s
        assert "slots" not in s
        assert "enums" not in s

    def test_license(self):
        s = M.build_gist_schema()
        assert s["license"] == "CC-BY-4.0"

    def test_canonical_key_order(self):
        s = M.build_gist_schema()
        keys = list(s.keys())
        assert keys.index("id") < keys.index("name")
        assert keys.index("prefixes") > keys.index("version")


class TestRenames:
    @staticmethod
    def _schema():
        return {
            "default_prefix": "gist_linkml",
            "classes": {
                "GistThing": {"mixin": True, "slots": ["name", "description"]},
                "Person": {"is_a": "LivingThing", "class_uri": "gist:Person", "aliases": ["Person"]},
                "LivingThing": {"class_uri": "gist:LivingThing", "disjoint_with": ["Organization"]},
                "Organization": {"mixins": ["GistThing"], "class_uri": "gist:Organization"},
            },
            "slots": {
                "name": {"slot_uri": "gist:name"},
                "description": {},
                "comes_from_agent": {"any_of": [{"range": "Organization"}, {"range": "Person"}]},
                "has_member": {"domain": "Organization", "range": "Person"},
            },
            "enums": {"AspectInstance": {}},
        }

    def test_parse(self):
        assert M.parse_renames(["Person=GistPerson", " name = gist_name "]) == {
            "Person": "GistPerson", "name": "gist_name",
        }

    @pytest.mark.parametrize("pairs", [
        ["Person"], ["Person="], ["=GistPerson"], ["Per son=GistPerson"],
        ["Person=Person"], ["Person=A", "Person=B"], ["Person=Human", "Human=GistHuman"],
        ["Person=Agent", "Organization=Agent"],
    ])
    def test_parse_rejects(self, pairs):
        with pytest.raises(ValueError):
            M.parse_renames(pairs)

    def test_check_rejects_unknown_old_name(self):
        with pytest.raises(ValueError, match="Persn"):
            M.check_renames(self._schema(), {"Persn": "GistPerson"})

    def test_check_rejects_taken_new_name(self):
        with pytest.raises(ValueError, match="AspectInstance"):
            M.check_renames(self._schema(), {"Person": "AspectInstance"})

    def test_renames_keep_iri_and_order(self):
        s = M.rename_elements(self._schema(), {"Person": "GistPerson", "description": "gist_description"})
        assert list(s["classes"]) == ["GistThing", "GistPerson", "LivingThing", "Organization"]
        assert s["classes"]["GistPerson"]["class_uri"] == "gist:Person"
        assert list(s["slots"])[1] == "gist_description"
        assert s["slots"]["gist_description"]["slot_uri"] == "gist_linkml:description"

    def test_old_name_becomes_alias_once(self):
        s = M.rename_elements(self._schema(), {"Person": "GistPerson", "name": "gist_name"})
        assert s["classes"]["GistPerson"]["aliases"] == ["Person"]
        assert s["slots"]["gist_name"]["aliases"] == ["name"]

    def test_references_follow(self):
        renames = {"Organization": "GistOrganization", "Person": "GistPerson", "name": "gist_name"}
        s = M.rename_elements(self._schema(), renames)
        assert s["classes"]["GistThing"]["slots"] == ["gist_name", "description"]
        assert s["classes"]["LivingThing"]["disjoint_with"] == ["GistOrganization"]
        assert s["slots"]["comes_from_agent"]["any_of"] == [
            {"range": "GistOrganization"}, {"range": "GistPerson"},
        ]
        assert s["slots"]["has_member"]["domain"] == "GistOrganization"
        assert s["slots"]["has_member"]["range"] == "GistPerson"

    def test_header_notes_the_renames_that_apply(self):
        s = M.rename_elements(self._schema(), {"Person": "GistPerson", "Tag": "GistTag"})
        assert s["notes"] == ["LinkML names changed from gist's own, IRIs unchanged: Person -> GistPerson."]
        assert "notes" not in M.rename_elements({"enums": {}}, {"Person": "GistPerson"})

    def test_input_not_mutated(self):
        schema = self._schema()
        M.rename_elements(schema, {"Person": "GistPerson"})
        assert "Person" in schema["classes"]
        assert schema["slots"]["has_member"]["range"] == "Person"

    def test_no_renames_is_identity(self):
        schema = self._schema()
        assert M.rename_elements(schema, {}) is schema


# ===========================================================================
# 11. File type classification
# ===========================================================================


class TestFileType:
    @pytest.mark.parametrize("stem,expected", [
        ("gistCore14.1.0",                "core"),
        ("gistMediaTypes14.1.0",          "media_types"),
        ("gistPrefixDeclarations14.1.0",  "prefix_declarations"),
        ("gistRdfsAnnotations14.1.0",     "rdfs_annotations"),
        ("gistSubClassAssertions14.1.0",  "sub_class_assertions"),
        ("unknownFile",                   "core"),  # default
    ])
    def test_classification(self, stem: str, expected: str):
        path = Path(f"/tmp/{stem}.ttl")
        assert M._file_type(path) == expected


# ===========================================================================
# 12. get_ontology_iri
# ===========================================================================


class TestGetOntologyIRI:
    def test_returns_iri(self):
        g = Graph()
        g.add((URIRef("https://example.org/myOntology"), RDF.type, OWL.Ontology))
        assert M.get_ontology_iri(g) == "https://example.org/myOntology"

    def test_returns_none_when_absent(self):
        g = Graph()
        assert M.get_ontology_iri(g) is None


# ===========================================================================
# 12b. ontology_header
# ===========================================================================


class TestOntologyHeader:
    def _graph(self) -> Graph:
        g = Graph()
        onto = URIRef("https://w3id.org/semanticarts/ontology/gistCore")
        g.add((onto, RDF.type, OWL.Ontology))
        g.add((onto, SKOS.prefLabel, Literal("gist")))
        g.add((onto, SKOS.definition, Literal("gist is a minimalist upper ontology.")))
        g.add((onto, SKOS.historyNote, Literal("\r\n\t\tgist 14.1.0 released 2026-Apr-17.\r\n\t\tgist 14.0.0 released 2025-Oct-31.\r\n\t")))
        g.add((onto, GIST.license, Literal("https://creativecommons.org/licenses/by/4.0/")))
        g.add((onto, OWL.versionIRI, URIRef("https://w3id.org/semanticarts/ontology/gistCore14.1.0")))
        return g

    def test_reads_skos_license_and_version_iri(self):
        h = M.ontology_header(self._graph())
        assert h["description"] == "gist is a minimalist upper ontology."
        assert h["license"] == "https://creativecommons.org/licenses/by/4.0/"
        assert h["notes"] == [
            "History: gist 14.1.0 released 2026-Apr-17.",
            "History: gist 14.0.0 released 2025-Oct-31.",
        ]
        assert h["see_also"] == ["https://w3id.org/semanticarts/ontology/gistCore14.1.0"]
        assert "aliases" not in h

    def test_annotations_module_read_without_duplicating(self):
        ann = Graph()
        onto = URIRef("https://w3id.org/semanticarts/ontology/gistCore")
        ann.add((onto, RDFS.label, Literal("gist")))
        ann.add((onto, RDFS.comment, Literal("DEFINITION: gist is a minimalist upper ontology.")))
        ann.add((onto, RDFS.comment, Literal("NOTE: Import it whole.")))
        h = M.ontology_header(self._graph(), ann)
        assert h["description"] == "gist is a minimalist upper ontology."
        assert h["comments"] == ["Import it whole."]

    def test_empty_without_ontology(self):
        assert M.ontology_header(Graph()) == {}


# ===========================================================================
# 13. coverage_report (smoke test — just check it runs and returns a string)
# ===========================================================================


class TestCoverageReport:
    def test_returns_string(self):
        g = Graph()
        g.add((GIST.Category, RDF.type, OWL.Class))
        report = M.coverage_report(g, {"Category": {}}, {}, {})
        assert isinstance(report, str)
        assert "Coverage report" in report

    def test_counts_included(self):
        g = Graph()
        g.add((GIST.Category, RDF.type, OWL.Class))
        report = M.coverage_report(
            g,
            {"Category": {}},
            {"has_name": {}},
            {"MyEnum": {"permissible_values": {"A": {}, "B": {}}}},
        )
        assert "1" in report   # 1 class in OWL graph
        assert "2" in report   # 2 enum values


# ===========================================================================
# 14. Integration: generate schemas from a minimal in-memory TTL
# ===========================================================================


_MINIMAL_TTL = textwrap.dedent("""\
    @prefix gist: <https://w3id.org/semanticarts/ns/ontology/gist/> .
    @prefix gistd: <https://w3id.org/semanticarts/ns/data/gist/> .
    @prefix owl: <http://www.w3.org/2002/07/owl#> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <https://example.org/testOntology> a owl:Ontology .

    gist:Category
        a owl:Class ;
        skos:definition "A broad category of things."^^xsd:string ;
        skos:prefLabel "Category"^^xsd:string .

    gist:SubCategory
        a owl:Class ;
        rdfs:subClassOf gist:Category ;
        skos:definition "A more specific category."^^xsd:string .

    gist:hasLabel
        a owl:DatatypeProperty ;
        rdfs:range xsd:string ;
        skos:definition "A human-readable label."^^xsd:string .

    gist:isPartOf
        a owl:ObjectProperty ;
        rdfs:range gist:Category ;
        skos:definition "Links to a containing category."^^xsd:string .

    gistd:_Aspect_mass
        a gist:Aspect .
""")


@pytest.fixture(scope="module")
def minimal_graph() -> Graph:
    g = Graph()
    g.parse(data=_MINIMAL_TTL, format="turtle")
    return g


class TestIntegrationMinimalGraph:
    def test_extract_classes_count(self, minimal_graph):
        classes = M.extract_classes(minimal_graph)
        assert len(classes) >= 2
        assert "Category" in classes
        assert "SubCategory" in classes

    def test_extract_slots_datatype(self, minimal_graph):
        slots = M.extract_slots(minimal_graph)
        assert "has_label" in slots
        assert slots["has_label"]["range"] == "string"

    def test_extract_slots_object(self, minimal_graph):
        slots = M.extract_slots(minimal_graph)
        assert "is_part_of" in slots
        assert slots["is_part_of"]["range"] == "Category"
        assert slots["is_part_of"].get("multivalued") is True

    def test_sub_category_is_a(self, minimal_graph):
        classes = M.extract_classes(minimal_graph)
        assert classes["SubCategory"]["is_a"] == "Category"

    def test_extract_enums_aspect(self, minimal_graph):
        enums = M.extract_enums(minimal_graph)
        assert "AspectInstance" in enums
        pv = enums["AspectInstance"]["permissible_values"]
        assert "ASPECT_MASS" in pv

    def test_build_schema_round_trip(self, minimal_graph):
        classes = M.extract_classes(minimal_graph)
        slots = M.extract_slots(minimal_graph)
        enums = M.extract_enums(minimal_graph)
        schema = M.build_schema(classes, slots, enums)
        yaml_text = M.dump_yaml(schema)
        assert "gist_core" in yaml_text
        assert "Category" in yaml_text
        assert "has_label" in yaml_text

    def test_dump_yaml_has_blank_lines_between_classes(self, minimal_graph):
        classes = M.extract_classes(minimal_graph)
        slots = M.extract_slots(minimal_graph)
        enums = M.extract_enums(minimal_graph)
        schema = M.build_schema(classes, slots, enums)
        yaml_text = M.dump_yaml(schema)
        lines = yaml_text.split("\n")
        class_lines = [i for i, l in enumerate(lines) if l.startswith("  ") and l.endswith(":") and not l.startswith("   ")]
        if len(class_lines) >= 2:
            gap_found = any(lines[class_lines[i] - 1] == "" for i in range(1, len(class_lines)))
            assert gap_found, "Expected blank lines between class entries"

    def test_generate_schemas_writes_files(self, tmp_path, minimal_graph):
        ttl_path = tmp_path / "gistCore14.1.0.ttl"
        ttl_path.write_text(_MINIMAL_TTL)
        M.generate_per_file_schemas([ttl_path], tmp_path / "out", version="14.1.0")
        out = tmp_path / "out"
        assert (out / "gist_core.yaml").exists()
        assert (out / "gist.yaml").exists()
