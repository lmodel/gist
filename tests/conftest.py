"""Pytest configuration: make scripts/ importable."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


import pytest  # noqa: E402

SEMANTIC_ARTS_NS = "https://w3id.org/semanticarts/ns/ontology/gist/"
SEMANTIC_ARTS_DATA_NS = "https://w3id.org/semanticarts/ns/data/gist/"
LMODEL_NS = "https://w3id.org/lmodel/gist/"
UPSTREAM_TTL = Path(__file__).parent.parent / "upstream" / "gist14.1.0_webDownload" / "ontologies" / "turtle"


@pytest.fixture(scope="session")
def upstream_gist():
    """IRIs and classes of the vendored Semantic Arts release, the yardstick for
    "terms used from gist stay in the gist namespace" and "define no terms there"."""
    import rdflib
    import rdflib.collection
    from rdflib.namespace import OWL, RDF, RDFS

    g = rdflib.Graph()
    for ttl in sorted(UPSTREAM_TTL.glob("*.ttl")):
        g.parse(ttl, format="turtle")
    iris = {str(t) for triple in g for t in triple if isinstance(t, rdflib.URIRef)}
    local_names = {
        i[len(ns):] for i in iris for ns in (SEMANTIC_ARTS_NS, SEMANTIC_ARTS_DATA_NS) if i.startswith(ns)
    }
    classes = {str(c) for c in g.subjects(RDF.type, OWL.Class) if str(c).startswith(SEMANTIC_ARTS_NS)}
    property_types: dict[str, set[str]] = {}
    for kind in (OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty):
        for p in g.subjects(RDF.type, kind):
            if str(p).startswith(SEMANTIC_ARTS_NS):
                property_types.setdefault(str(p), set()).add(str(kind))
    deprecated = {
        str(s) for s, o in g.subject_objects(OWL.deprecated)
        if str(s).startswith(SEMANTIC_ARTS_NS) and str(o).lower() == "true"
    }

    def named_or_union(node) -> set[str]:
        union = g.value(node, OWL.unionOf) if isinstance(node, rdflib.BNode) else None
        return {str(m) for m in rdflib.collection.Collection(g, union)} if union else {str(node)}

    # Each object or datatype property's rdfs:domain classes (empty without
    # one), each datatype property's range datatypes, and each class's named
    # superclasses
    domains, datatype_ranges = {}, {}
    for kind in (OWL.ObjectProperty, OWL.DatatypeProperty):
        for p in g.subjects(RDF.type, kind):
            if str(p).startswith(SEMANTIC_ARTS_NS):
                domains[str(p)] = set().union(*(named_or_union(d) for d in g.objects(p, RDFS.domain)))
                if kind == OWL.DatatypeProperty and (p, RDFS.range, None) in g:
                    datatype_ranges[str(p)] = set().union(*(named_or_union(r) for r in g.objects(p, RDFS.range)))
    superclasses = {
        c: {str(o) for o in g.objects(rdflib.URIRef(c), RDFS.subClassOf) if str(o) in classes}
        for c in classes
    }
    return {
        "iris": iris, "local_names": local_names, "classes": classes,
        "property_types": property_types, "deprecated": deprecated,
        "domains": domains, "datatype_ranges": datatype_ranges, "superclasses": superclasses,
        "gist_ns": SEMANTIC_ARTS_NS, "gistd_ns": SEMANTIC_ARTS_DATA_NS, "lmodel_ns": LMODEL_NS,
    }
