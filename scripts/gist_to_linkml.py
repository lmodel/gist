#!/usr/bin/env python3
"""
Transform GIST OWL/Turtle ontology files into five LinkML schema YAMLs.

Generates one schema per input TTL file into an output directory:
  gist_core.yaml                 — classes, slots, enums; enriched by
                                   RdfsAnnotations + SubClassAssertions
  gist_media_types.yaml          — IANA MediaType enum (imports gist_core)
  gist_prefix_declarations.yaml  — SHACL PrefixDeclaration enum (standalone)
  gist_rdfs_annotations.yaml     — class/slot stubs from rdfs:label/comment
  gist_sub_class_assertions.yaml — class stubs with is_a hierarchy

Usage
-----
    uv run python scripts/gist_to_linkml.py [TTL_FILE ...] [-d OUTPUT_DIR]

100% coverage goals:
  - Every owl:Class                              -> LinkML class
  - Every owl:ObjectProperty / DatatypeProperty  -> LinkML slot
  - Every owl:AnnotationProperty (gist: ns)      -> LinkML slot
  - Named individuals (gistd:*, media-*)         -> enum permissible values
  - SHACL PrefixDeclarations                    -> PrefixDeclarationInstance enum
  - All SKOS/RDFS annotations preserved
    (definition, prefLabel, altLabel, example, scopeNote, editorialNote,
     rdfs:label, rdfs:comment DEFINITION:/EXAMPLE:/NOTE: prefixes)
  - OWL axioms without direct LinkML equivalents  -> notes/comments
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import rdflib
import rdflib.collection
import yaml
from rdflib import BNode, Graph, Literal, URIRef
from rdflib.compare import to_canonical_graph
from rdflib.namespace import OWL, RDF, RDFS, SKOS, XSD

# ---------------------------------------------------------------------------
# Namespace constants
# ---------------------------------------------------------------------------
GIST_SA_NS = "https://w3id.org/semanticarts/ns/ontology/gist/"
GISTD_NS = "https://w3id.org/semanticarts/ns/data/gist/"
LMODEL_NS = "https://w3id.org/lmodel/gist/"
LMODEL_BASE = "https://w3id.org/lmodel/gist"

GIST = rdflib.Namespace(GIST_SA_NS)
GISTD = rdflib.Namespace(GISTD_NS)
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")

MEDIA_APP = rdflib.Namespace("https://www.iana.org/assignments/media-types/application/")
MEDIA_IMG = rdflib.Namespace("https://www.iana.org/assignments/media-types/image/")
MEDIA_TXT = rdflib.Namespace("https://www.iana.org/assignments/media-types/text/")

MEDIA_PREFIXES = {
    "https://www.iana.org/assignments/media-types/application/": "media_app",
    "https://www.iana.org/assignments/media-types/image/": "media_img",
    "https://www.iana.org/assignments/media-types/text/": "media_txt",
}

# Ordered prefix table used by uri_to_curie() — longest namespace first avoids prefix ambiguity
_CURIE_PREFIXES: list[tuple[str, str]] = [
    (GIST_SA_NS, "gist_semanticarts"),
    (GISTD_NS, "gistd"),
    (LMODEL_NS, "gist"),
    ("http://schema.org/", "schema"),
    ("https://schema.org/", "schema"),
    ("http://www.w3.org/2004/02/skos/core#", "skos"),
    ("http://purl.org/dc/terms/", "dct"),
    ("https://www.wikidata.org/wiki/", "WIKIDATA"),
    ("http://purl.obolibrary.org/obo/BFO_", "BFO"),
    ("http://purl.obolibrary.org/obo/IAO_", "IAO"),
    ("http://purl.obolibrary.org/obo/RO_", "RO"),
]

# Prefixes used in gistRdfsAnnotations rdfs:comment values
_DEFINITION_RE = re.compile(r"^DEFINITION:\s*")
_EXAMPLE_RE = re.compile(r"^EXAMPLE:\s*")
_NOTE_RE = re.compile(r"^NOTE:\s*")

# ---------------------------------------------------------------------------
# XSD  -> LinkML type mapping
# ---------------------------------------------------------------------------
XSD_TO_LINKML: dict[str, str] = {
    str(XSD.string): "string",
    str(XSD.normalizedString): "string",
    str(XSD.token): "string",
    str(XSD.language): "string",
    str(XSD.integer): "integer",
    str(XSD.int): "integer",
    str(XSD.long): "integer",
    str(XSD.short): "integer",
    str(XSD.byte): "integer",
    str(XSD.nonNegativeInteger): "integer",
    str(XSD.nonPositiveInteger): "integer",
    str(XSD.positiveInteger): "integer",
    str(XSD.negativeInteger): "integer",
    str(XSD.unsignedLong): "integer",
    str(XSD.unsignedInt): "integer",
    str(XSD.unsignedShort): "integer",
    str(XSD.unsignedByte): "integer",
    str(XSD.float): "float",
    str(XSD.double): "float",
    str(XSD.decimal): "decimal",
    str(XSD.boolean): "boolean",
    str(XSD.dateTime): "datetime",
    str(XSD.date): "date",
    str(XSD.time): "time",
    str(XSD.gYear): "string",
    str(XSD.gMonth): "string",
    str(XSD.gDay): "string",
    str(XSD.anyURI): "uri",
    str(XSD.base64Binary): "string",
    str(XSD.hexBinary): "string",
}


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def camel_to_snake(name: str) -> str:
    """Convert camelCase or PascalCase to snake_case."""
    s1 = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    return re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s1).lower()


def local_name(uri: URIRef) -> str:
    s = str(uri)
    if "#" in s:
        return s.rsplit("#", 1)[-1]
    return s.rsplit("/", 1)[-1]


def gist_local(uri: URIRef) -> str | None:
    s = str(uri)
    if s.startswith(GIST_SA_NS):
        return s[len(GIST_SA_NS):]
    return None


def gistd_local(uri: URIRef) -> str | None:
    s = str(uri)
    if s.startswith(GISTD_NS):
        return s[len(GISTD_NS):]
    return None


def uri_to_curie(uri: URIRef) -> str | None:
    """Convert a URIRef to a CURIE using the known prefix table. Returns None if unknown."""
    s = str(uri)
    for ns, prefix in _CURIE_PREFIXES:
        if s.startswith(ns):
            return f"{prefix}:{s[len(ns):]}"
    return None


def media_curie(uri: URIRef) -> str | None:
    s = str(uri)
    for ns, prefix in MEDIA_PREFIXES.items():
        if s.startswith(ns):
            return f"{prefix}:{s[len(ns):]}"
    return None


class _SortedGraph(Graph):
    """Graph whose ``triples()`` yields in a fixed order.

    rdflib's memory store iterates Python sets, so without this the element
    and list order of the generated YAML (and choices such as ``is_a``, taken
    from the first superclass found) changes from run to run.
    """

    def triples(self, triple, *args, **kwargs):
        found = super().triples(triple, *args, **kwargs)
        yield from sorted(found, key=lambda t: tuple(term.n3() for term in t))


def canonical_graph(g: Graph) -> Graph:
    """Copy ``g`` with blank nodes relabelled canonically and sorted iteration."""
    out = _SortedGraph()
    for t in to_canonical_graph(g):
        out.add(t)
    return out


def get_literals(g: Graph, subj, pred) -> list[str]:
    return [str(o) for o in g.objects(subj, pred) if isinstance(o, Literal)]


def first_literal(g: Graph, subj, pred) -> str | None:
    vals = get_literals(g, subj, pred)
    return vals[0] if vals else None


def named_objects(g: Graph, subj, pred) -> list[URIRef]:
    return [o for o in g.objects(subj, pred) if isinstance(o, URIRef)]


def union_members(g: Graph, node) -> list[URIRef] | None:
    if not isinstance(node, BNode):
        return None
    union_list = list(g.objects(node, OWL.unionOf))
    if not union_list:
        return None
    return [
        m for m in rdflib.collection.Collection(g, union_list[0])
        if isinstance(m, URIRef)
    ]


def owl_expr_str(g: Graph, node, depth: int = 0) -> str:
    """Render an OWL class expression as a compact human-readable string."""
    if depth > 6:
        return "..."
    if isinstance(node, URIRef):
        gl = gist_local(node)
        if gl:
            return f"gist:{gl}"
        ln = local_name(node)
        return f"owl:{ln}" if str(node).startswith(str(OWL)) else f"<{node}>"
    if not isinstance(node, BNode):
        return str(node)

    # union
    u = list(g.objects(node, OWL.unionOf))
    if u:
        members = list(rdflib.collection.Collection(g, u[0]))
        return "(" + " | ".join(owl_expr_str(g, m, depth + 1) for m in members) + ")"

    # intersection
    inter = list(g.objects(node, OWL.intersectionOf))
    if inter:
        members = list(rdflib.collection.Collection(g, inter[0]))
        return "(" + " & ".join(owl_expr_str(g, m, depth + 1) for m in members) + ")"

    # restriction
    on_prop = list(g.objects(node, OWL.onProperty))
    if on_prop:
        p = on_prop[0]
        p_str = gist_local(p) or local_name(p) if isinstance(p, URIRef) else "?"
        # inverse property
        inv_p = list(g.objects(p, OWL.inverseOf)) if isinstance(p, BNode) else []
        if inv_p:
            p_str = f"^{gist_local(inv_p[0]) or local_name(inv_p[0])}"

        some = list(g.objects(node, OWL.someValuesFrom))
        if some:
            return f"∃{p_str}.{owl_expr_str(g, some[0], depth + 1)}"
        all_v = list(g.objects(node, OWL.allValuesFrom))
        if all_v:
            return f"∀{p_str}.{owl_expr_str(g, all_v[0], depth + 1)}"
        has_v = list(g.objects(node, OWL.hasValue))
        if has_v:
            val = has_v[0]
            val_s = gistd_local(val) or (gist_local(val) if isinstance(val, URIRef) else str(val))
            return f"∃{p_str}={val_s}"
        min_qc = list(g.objects(node, OWL.minQualifiedCardinality))
        if min_qc:
            on_cls = list(g.objects(node, OWL.onClass))
            cls_s = owl_expr_str(g, on_cls[0], depth + 1) if on_cls else "owl:Thing"
            return f"≥{min_qc[0]}{p_str}.{cls_s}"
        max_qc = list(g.objects(node, OWL.maxQualifiedCardinality))
        if max_qc:
            on_cls = list(g.objects(node, OWL.onClass))
            cls_s = owl_expr_str(g, on_cls[0], depth + 1) if on_cls else "owl:Thing"
            return f"≤{max_qc[0]}{p_str}.{cls_s}"
        min_c = list(g.objects(node, OWL.minCardinality))
        if min_c:
            return f"≥{min_c[0]}{p_str}"
        max_c = list(g.objects(node, OWL.maxCardinality))
        if max_c:
            return f"≤{max_c[0]}{p_str}"
        exact_c = list(g.objects(node, OWL.cardinality))
        if exact_c:
            return f"={exact_c[0]}{p_str}"

    # complement
    comp = list(g.objects(node, OWL.complementOf))
    if comp:
        return f"¬{owl_expr_str(g, comp[0], depth + 1)}"

    return "_bnode_"


# ---------------------------------------------------------------------------
# Core extraction functions
# ---------------------------------------------------------------------------

def _ifp_slots_by_domain_class(g: Graph) -> dict[str, list[str]]:
    """Map each gist class to the snake_case slot names of every
    owl:InverseFunctionalProperty whose rdfs:domain (named or unionOf) includes it.
    Used to attach LinkML unique_keys at the class level.
    """
    by_class: dict[str, list[str]] = defaultdict(list)
    for prop in g.subjects(RDF.type, OWL.InverseFunctionalProperty):
        if not isinstance(prop, URIRef):
            continue
        prop_local = gist_local(prop)
        if not prop_local:
            continue
        slot_name = camel_to_snake(prop_local)
        for d in g.objects(prop, RDFS.domain):
            if isinstance(d, URIRef) and gist_local(d):
                by_class[gist_local(d)].append(slot_name)
            elif isinstance(d, BNode):
                members = union_members(g, d) or []
                for m in members:
                    if gist_local(m):
                        by_class[gist_local(m)].append(slot_name)
    return by_class


def extract_classes(g: Graph) -> dict[str, dict]:
    """Extract owl:Class entries defined in the gist: namespace."""
    classes: dict[str, dict] = {}
    ifp_slots_by_class = _ifp_slots_by_domain_class(g)

    for cls in g.subjects(RDF.type, OWL.Class):
        if not isinstance(cls, URIRef):
            continue
        cls_local = gist_local(cls)
        if not cls_local:
            continue

        entry: dict[str, Any] = {}

        # --- description ---
        defn = first_literal(g, cls, SKOS.definition)
        if not defn:
            # Fall back to rdfs:comment DEFINITION: prefix (from gistRdfsAnnotations)
            for c in get_literals(g, cls, RDFS.comment):
                if _DEFINITION_RE.match(c):
                    defn = _DEFINITION_RE.sub("", c)
                    break
        if defn:
            entry["description"] = defn

        # --- deprecated ---
        depr = first_literal(g, cls, OWL.deprecated)
        if depr and depr.lower() == "true":
            entry["deprecated"] = "true"

        # --- is_a: first simple named gist: superclass ---
        simple_parents = [
            o for o in g.objects(cls, RDFS.subClassOf)
            if isinstance(o, URIRef) and gist_local(o)
        ]
        anon_parents = [
            o for o in g.objects(cls, RDFS.subClassOf)
            if isinstance(o, BNode)
        ]

        if simple_parents:
            entry["is_a"] = gist_local(simple_parents[0])
            if len(simple_parents) > 1:
                mixins = [gist_local(p) for p in simple_parents[1:]]
                entry["notes"] = entry.get("notes", []) + [
                    f"Additional named superclasses (modelled as OWL multiple inheritance): "
                    + ", ".join(str(m) for m in mixins)
                ]

        # --- restriction-based subClassOf as notes ---
        if anon_parents:
            axioms = [owl_expr_str(g, p) for p in anon_parents]
            entry["notes"] = entry.get("notes", []) + [
                f"OWL subClassOf restrictions: " + "; ".join(axioms)
            ]

        # --- class_uri maps to the upstream OWL class URI ---
        entry["class_uri"] = f"gist:{cls_local}"

        # --- equivalentClass ---
        # Named URIs  -> exact_mappings (owl:equivalentClass = owl:equivalentClass semantics)
        # Anonymous BNode expressions (intersections, restrictions)  -> notes
        equiv_nodes = list(g.objects(cls, OWL.equivalentClass))
        named_equiv = [o for o in equiv_nodes if isinstance(o, URIRef)]
        anon_equiv = [o for o in equiv_nodes if isinstance(o, BNode)]

        if named_equiv:
            equiv_curies = []
            for o in named_equiv:
                curie = uri_to_curie(o)
                if curie:
                    equiv_curies.append(curie)
                else:
                    equiv_curies.append(str(o))  # fall back to full URI
            entry["exact_mappings"] = entry.get("exact_mappings", []) + equiv_curies
        if anon_equiv:
            axioms = [owl_expr_str(g, e) for e in anon_equiv]
            entry["notes"] = entry.get("notes", []) + [
                f"OWL equivalentClass: " + "; ".join(axioms)
            ]

        # --- aliases (prefLabel, altLabel, rdfs:label) ---
        pref = first_literal(g, cls, SKOS.prefLabel)
        alts = get_literals(g, cls, SKOS.altLabel)
        rdfs_labels = get_literals(g, cls, RDFS.label)
        aliases: list[str] = []
        if pref:
            aliases.append(pref)
        aliases.extend(alts)
        # Add rdfs:label if not already present via SKOS
        for lbl in rdfs_labels:
            if lbl not in aliases:
                aliases.append(lbl)
        if aliases:
            entry["aliases"] = aliases

        # --- examples from SKOS and rdfs:comment EXAMPLE: prefix ---
        examples = get_literals(g, cls, SKOS.example)
        rdfs_examples = [
            _EXAMPLE_RE.sub("", c)
            for c in get_literals(g, cls, RDFS.comment)
            if _EXAMPLE_RE.match(c)
        ]
        all_examples = examples + [e for e in rdfs_examples if e not in examples]
        if all_examples:
            entry["examples"] = [{"value": ex} for ex in all_examples]

        # --- comments from scopeNote and rdfs:comment NOTE: prefix ---
        scope = get_literals(g, cls, SKOS.scopeNote)
        rdfs_notes = [
            _NOTE_RE.sub("", c)
            for c in get_literals(g, cls, RDFS.comment)
            if _NOTE_RE.match(c)
        ]
        all_comments = scope + [n for n in rdfs_notes if n not in scope]
        if all_comments:
            entry["comments"] = all_comments

        # --- notes from editorialNote ---
        ed_notes = get_literals(g, cls, SKOS.editorialNote)
        if ed_notes:
            entry["notes"] = entry.get("notes", []) + ed_notes

        # --- disjointWith  -> LinkML disjoint_with (class level) ---
        disjoints = [gist_local(o) for o in named_objects(g, cls, OWL.disjointWith)
                     if gist_local(o)]
        if disjoints:
            entry["disjoint_with"] = disjoints if len(disjoints) > 1 else disjoints[0]

        # --- InverseFunctionalProperty  -> unique_keys ---
        # An IFP whose rdfs:domain (named or unionOf) includes this class becomes
        # a single-slot unique_keys entry on the class. The slot uniquely
        # identifies the subject (inverse functional semantics).
        ifp_slots = ifp_slots_by_class.get(cls_local, [])
        if ifp_slots:
            entry["unique_keys"] = {
                f"by_{slot}": {"unique_key_slots": [slot]}
                for slot in dict.fromkeys(ifp_slots)  # dedupe, preserve order
            }

        # --- historyNote ---
        hist = get_literals(g, cls, SKOS.historyNote)
        if hist:
            entry["notes"] = entry.get("notes", []) + [f"History: {h}" for h in hist]

        classes[cls_local] = entry

    return classes


def extract_slots(g: Graph) -> dict[str, dict]:
    """Extract all property definitions in the gist: namespace."""
    slots: dict[str, dict] = {}

    prop_types = {
        OWL.ObjectProperty: "object",
        OWL.DatatypeProperty: "datatype",
        OWL.AnnotationProperty: "annotation",
    }

    for prop_type, kind in prop_types.items():
        for prop in g.subjects(RDF.type, prop_type):
            if not isinstance(prop, URIRef):
                continue
            prop_local = gist_local(prop)
            if not prop_local:
                continue

            sname = camel_to_snake(prop_local)
            entry: dict[str, Any] = {}

            # slot_uri maps to the upstream predicate URI
            entry["slot_uri"] = f"gist:{prop_local}"

            # --- description ---
            defn = first_literal(g, prop, SKOS.definition)
            if not defn:
                defn = first_literal(g, prop, RDFS.comment)
            if defn:
                entry["description"] = defn

            # --- is_a: subPropertyOf (gist: only) ---
            sub_of = [
                o for o in g.objects(prop, RDFS.subPropertyOf)
                if isinstance(o, URIRef) and gist_local(o)
            ]
            if sub_of:
                entry["is_a"] = camel_to_snake(gist_local(sub_of[0]))
                if len(sub_of) > 1:
                    entry["notes"] = entry.get("notes", []) + [
                        "OWL additional subPropertyOf (gist:): "
                        + ", ".join(camel_to_snake(gist_local(o)) for o in sub_of[1:])
                    ]
            # Cross-namespace subPropertyOf  -> related_mappings
            cross_sub = [
                o for o in g.objects(prop, RDFS.subPropertyOf)
                if isinstance(o, URIRef) and not gist_local(o)
            ]
            if cross_sub:
                entry["related_mappings"] = [str(o) for o in cross_sub]

            # --- domain (rdfs:domain  -> LinkML domain; unionOf  -> domain + any_of) ---
            gist_domains = [
                gist_local(o) for o in g.objects(prop, RDFS.domain)
                if isinstance(o, URIRef) and gist_local(o)
            ]
            anon_domains = [o for o in g.objects(prop, RDFS.domain) if isinstance(o, BNode)]

            union_domain_members: list[str] = []
            for ad in anon_domains:
                members = union_members(g, ad)
                if members:
                    union_domain_members.extend(
                        gist_local(m) for m in members if gist_local(m)
                    )
                else:
                    entry["notes"] = entry.get("notes", []) + [
                        "OWL domain restriction: " + owl_expr_str(g, ad)
                    ]

            all_domains = list(gist_domains) + union_domain_members
            # Deduplicate while preserving order
            seen = set()
            all_domains = [d for d in all_domains if not (d in seen or seen.add(d))]

            if all_domains:
                entry["domain"] = all_domains[0]
                if len(all_domains) > 1:
                    entry["any_of"] = (entry.get("any_of") or []) + [
                        {"range": d} for d in all_domains
                    ]

            # --- range ---
            range_uris = [o for o in g.objects(prop, RDFS.range) if isinstance(o, URIRef)]
            range_bnodes = [o for o in g.objects(prop, RDFS.range) if isinstance(o, BNode)]

            if kind == "datatype":
                if range_uris:
                    linkml_type = XSD_TO_LINKML.get(str(range_uris[0]), "string")
                    entry["range"] = linkml_type
                # multivalued defaults to false; no need to state explicitly
            else:
                gist_ranges = [gist_local(o) for o in range_uris if gist_local(o)]
                if len(gist_ranges) == 1:
                    entry["range"] = gist_ranges[0]
                elif len(gist_ranges) > 1:
                    entry["any_of"] = [{"range": r} for r in gist_ranges]

                for rb in range_bnodes:
                    members = union_members(g, rb)
                    if members:
                        gist_ms = [gist_local(m) for m in members if gist_local(m)]
                        if gist_ms:
                            entry["any_of"] = [{"range": m} for m in gist_ms]
                    else:
                        entry["notes"] = entry.get("notes", []) + [
                            "OWL range restriction: " + owl_expr_str(g, rb)
                        ]

                # gist:rangeIncludes (soft range hints) — use when no hard rdfs:range
                if "range" not in entry and "any_of" not in entry:
                    range_includes = [
                        gist_local(o) for o in g.objects(prop, GIST.rangeIncludes)
                        if isinstance(o, URIRef) and gist_local(o)
                    ]
                    if len(range_includes) == 1:
                        entry["range"] = range_includes[0]
                    elif len(range_includes) > 1:
                        entry["any_of"] = [{"range": r} for r in range_includes]

                if kind == "object":
                    entry.setdefault("multivalued", True)

            # --- inverseOf ---
            inv = [
                gist_local(o) for o in named_objects(g, prop, OWL.inverseOf)
                if gist_local(o)
            ]
            if inv:
                entry["inverse"] = camel_to_snake(inv[0])

            # --- equivalentProperty  -> exact_mappings ---
            equiv_props = [o for o in named_objects(g, prop, OWL.equivalentProperty)
                           if isinstance(o, URIRef)]
            if equiv_props:
                equiv_curies = []
                for o in equiv_props:
                    curie = uri_to_curie(o)
                    equiv_curies.append(curie if curie else str(o))
                entry["exact_mappings"] = entry.get("exact_mappings", []) + equiv_curies

            # --- property characteristics ---
            all_types = set(g.objects(prop, RDF.type))
            if OWL.TransitiveProperty in all_types:
                entry["transitive"] = True
            if OWL.SymmetricProperty in all_types:
                entry["symmetric"] = True
            if OWL.ReflexiveProperty in all_types:
                entry["reflexive"] = True
            if OWL.FunctionalProperty in all_types:
                entry["notes"] = entry.get("notes", []) + ["OWL FunctionalProperty (at most one value)"]
            if OWL.InverseFunctionalProperty in all_types:
                # OWL InverseFunctionalProperty  -> LinkML unique_keys (added at class
                # level by extract_classes); also annotate the slot for visibility
                ann = entry.setdefault("annotations", {})
                ann["owl_inverse_functional"] = True

            # --- deprecated ---
            depr = first_literal(g, prop, OWL.deprecated)
            if depr and depr.lower() == "true":
                entry["deprecated"] = "true"
                superseded = [
                    gist_local(o) for o in named_objects(g, prop, GIST.isSupersededBy)
                    if gist_local(o)
                ]
                if superseded:
                    entry["deprecated_element_has_exact_replacement"] = camel_to_snake(superseded[0])

            # --- aliases (prefLabel, altLabel) ---
            pref = first_literal(g, prop, SKOS.prefLabel)
            alts = get_literals(g, prop, SKOS.altLabel)
            aliases: list[str] = []
            if pref:
                aliases.append(pref)
            aliases.extend(alts)
            if aliases:
                entry["aliases"] = aliases

            # --- examples ---
            examples = get_literals(g, prop, SKOS.example)
            if examples:
                entry["examples"] = [{"value": ex} for ex in examples]

            # --- comments from scopeNote ---
            scope = get_literals(g, prop, SKOS.scopeNote)
            if scope:
                entry["comments"] = scope

            # --- notes from editorialNote ---
            ed_notes = get_literals(g, prop, SKOS.editorialNote)
            if ed_notes:
                entry["notes"] = entry.get("notes", []) + ed_notes

            # --- propertyDisjointWith  -> LinkML disjoint_with ---
            disj = [
                camel_to_snake(gist_local(o))
                for o in named_objects(g, prop, OWL.propertyDisjointWith)
                if gist_local(o)
            ]
            if disj:
                entry["disjoint_with"] = disj if len(disj) > 1 else disj[0]

            slots[sname] = entry

    return slots


def _enum_val_key(raw: str) -> str:
    """
    Normalise an ontology local name to a LinkML-compliant UPPER_SNAKE_CASE
    enum value key, removing leading underscores and mapping symbols to words.
    """
    s = raw.lstrip("_")
    s = re.sub(r"[+]", "_PLUS_", s)
    s = re.sub(r"[^A-Za-z0-9_]", "_", s)
    s = re.sub(r"_+", "_", s)
    s = s.strip("_")
    return s.upper()


def extract_enums(g: Graph) -> dict[str, dict]:
    """
    Extract named individuals in gistd: and IANA media-* namespaces as enums.
    Groups them by their rdf:type (gist: class) into separate enum entries.
    """
    enums: dict[str, dict] = {}

    schema_types = {OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty,
                    OWL.AnnotationProperty, OWL.Ontology}

    groups: dict[str, list[URIRef]] = defaultdict(list)

    for subj in g.subjects(RDF.type, None):
        if not isinstance(subj, URIRef):
            continue
        s = str(subj)

        is_gistd = s.startswith(GISTD_NS)
        is_media = any(s.startswith(ns) for ns in MEDIA_PREFIXES)
        if not (is_gistd or is_media):
            continue

        gist_types = [
            gist_local(t) for t in g.objects(subj, RDF.type)
            if isinstance(t, URIRef) and gist_local(t)
            and t not in schema_types
        ]
        for t in gist_types:
            groups[t].append(subj)

    for gist_type, individuals in sorted(groups.items()):
        enum_name = f"{gist_type}Instance"
        pv: dict[str, dict] = {}
        seen_keys: dict[str, str] = {}

        for ind in sorted(individuals, key=str):
            s = str(ind)

            if s.startswith(GISTD_NS):
                raw_local = s[len(GISTD_NS):]
                meaning = f"gistd:{raw_local}"
            else:
                curie = media_curie(ind)
                raw_local = curie.split(":", 1)[-1] if curie else local_name(ind)
                meaning = curie if curie else str(ind)

            val_key = _enum_val_key(raw_local)
            if val_key in seen_keys:
                val_key = val_key + "_2"
            seen_keys[val_key] = raw_local

            pv_entry: dict = {}

            defn = first_literal(g, ind, SKOS.definition)
            if not defn:
                defn = first_literal(g, ind, RDFS.comment)
            if defn:
                defn = _DEFINITION_RE.sub("", defn)
                pv_entry["description"] = defn

            pref = first_literal(g, ind, SKOS.prefLabel)
            if not pref:
                pref = first_literal(g, ind, RDFS.label)
            if pref:
                pv_entry["title"] = pref

            pv_entry["meaning"] = meaning
            pv[val_key] = pv_entry

        enums[enum_name] = {
            "description": f"Named instances of gist:{gist_type} from gist reference data.",
            "permissible_values": pv,
        }

    return enums


# ---------------------------------------------------------------------------
# Per-file extraction functions
# ---------------------------------------------------------------------------

def extract_rdfs_annotations(
    g: Graph,
    ctx: Graph | None = None,
) -> tuple[dict[str, dict], dict[str, dict]]:
    """
    Extract rdfs:label and rdfs:comment for gist: entities.

    Returns (classes_dict, slots_dict).  Uses ctx (context graph, typically
    gistCore) to classify each entity as a class or slot; defaults to class
    when type is unknown.
    """
    classes: dict[str, dict] = {}
    slots: dict[str, dict] = {}

    # Collect all gist: subjects that have rdfs:label or rdfs:comment
    subj_set: set[URIRef] = set()
    for pred in (RDFS.label, RDFS.comment):
        for s in g.subjects(pred, None):
            if isinstance(s, URIRef) and gist_local(s):
                subj_set.add(s)

    prop_types = {OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty}

    for subj in sorted(subj_set, key=str):
        gist_name = gist_local(subj)
        if not gist_name:
            continue

        # Determine class vs slot using context graph
        is_slot = False
        if ctx:
            entity_types = set(ctx.objects(subj, RDF.type))
            is_slot = bool(entity_types & prop_types)

        entry: dict[str, Any] = {}

        labels = get_literals(g, subj, RDFS.label)
        if labels:
            entry["aliases"] = labels

        description: str | None = None
        examples: list[dict] = []
        notes: list[str] = []

        for c in get_literals(g, subj, RDFS.comment):
            if _DEFINITION_RE.match(c):
                description = _DEFINITION_RE.sub("", c)
            elif _EXAMPLE_RE.match(c):
                examples.append({"value": _EXAMPLE_RE.sub("", c)})
            elif _NOTE_RE.match(c):
                notes.append(_NOTE_RE.sub("", c))
            elif description is None:
                description = c  # bare comment without prefix

        if description:
            entry["description"] = description
        if examples:
            entry["examples"] = examples
        if notes:
            entry["comments"] = notes

        if is_slot:
            entry["slot_uri"] = f"gist:{gist_name}"
            slots[camel_to_snake(gist_name)] = entry
        else:
            entry["class_uri"] = f"gist:{gist_name}"
            classes[gist_name] = entry

    return classes, slots


def extract_sub_class_assertions(g: Graph) -> dict[str, dict]:
    """
    Extract rdfs:subClassOf triples for gist: classes into class stubs with is_a.
    Ensures all referenced parent classes are also present in the schema so
    the output is self-consistent.
    """
    classes: dict[str, dict] = {}

    for subj, obj in g.subject_objects(RDFS.subClassOf):
        if not isinstance(subj, URIRef) or not isinstance(obj, URIRef):
            continue
        subj_name = gist_local(subj)
        obj_name = gist_local(obj)
        if not subj_name or not obj_name:
            continue

        if subj_name not in classes:
            classes[subj_name] = {
                "class_uri": f"gist:{subj_name}",
                "is_a": obj_name,
            }
        else:
            existing = classes[subj_name].get("is_a")
            if existing and existing != obj_name:
                notes = classes[subj_name].get("notes", [])
                notes.append(f"OWL additional subClassOf: {obj_name}")
                classes[subj_name]["notes"] = notes

    # Declare any parent that is not yet a subject (root classes)
    all_parents = {entry["is_a"] for entry in classes.values() if "is_a" in entry}
    for parent in sorted(all_parents):
        if parent not in classes:
            classes[parent] = {"class_uri": f"gist:{parent}"}

    return classes


def extract_prefix_declarations(g: Graph) -> dict[str, dict]:
    """
    Extract sh:PrefixDeclaration individuals into enum permissible_values.
    Returns {key: {title, description, meaning}} mapping.
    """
    pv: dict[str, dict] = {}

    for subj in sorted(g.subjects(RDF.type, SH.PrefixDeclaration), key=str):
        if not isinstance(subj, URIRef):
            continue

        prefix_val = first_literal(g, subj, SH.prefix)
        namespace_val = first_literal(g, subj, SH.namespace)
        if not prefix_val:
            continue

        gist_name = gist_local(subj)
        key = _enum_val_key(gist_name) if gist_name else _enum_val_key(prefix_val)
        meaning = f"gist:{gist_name}" if gist_name else str(subj)

        pv[key] = {
            "title": prefix_val,
            "description": f"Prefix '{prefix_val}' for namespace <{namespace_val}>.",
            "meaning": meaning,
        }

    return pv


# ---------------------------------------------------------------------------
# YAML output — canonical key ordering + literal block scalars
# ---------------------------------------------------------------------------

# Top-level schema header fields in canonical order (mirrors skill template)
_SCHEMA_KEY_ORDER = [
    "id", "name", "title", "description", "license", "see_also",
    "source", "version", "annotations",
    "prefixes", "default_prefix", "default_range", "imports",
    "subsets", "types", "enums", "slots", "classes",
]

# Canonical key order for class and slot entries
_ELEMENT_KEY_ORDER = [
    # inheritance / type modifiers
    "is_a", "mixins", "abstract", "mixin", "tree_root",
    # identity mappings
    "class_uri", "slot_uri",
    # documentation
    "description", "title", "aliases", "comments", "examples", "notes",
    # domain / range / cardinality (slots)
    "domain", "range", "multivalued", "required", "recommended", "identifier", "any_of",
    # object-property characteristics
    "inverse", "transitive", "symmetric", "antisymmetric", "reflexive", "disjoint_with",
    # deprecation
    "deprecated", "deprecated_element_has_exact_replacement",
    # partitioning
    "in_subset",
    # ontology alignment
    "exact_mappings", "close_mappings", "narrow_mappings",
    "broad_mappings", "related_mappings", "see_also",
    # class-level structural
    "slots", "slot_usage", "id_prefixes", "union_of", "unique_keys",
    "rules", "defining_slots",
    # slot constraints
    "ifabsent", "inlined", "inlined_as_list", "unit",
    "minimum_value", "maximum_value", "pattern", "string_serialization",
    "annotations",
]


def _order_keys(d: dict, key_order: list[str]) -> dict:
    """Return d with keys in key_order first, remaining keys in insertion order."""
    result = {k: d[k] for k in key_order if k in d}
    result.update({k: v for k, v in d.items() if k not in result})
    return result


def _order_elements(elements: dict, subset_name: str | None = None) -> dict:
    """Order each element dict's keys canonically and optionally add in_subset."""
    result = {}
    for name, elem in elements.items():
        entry = dict(elem)
        if subset_name:
            entry.setdefault("in_subset", [subset_name])
        result[name] = _order_keys(entry, _ELEMENT_KEY_ORDER)
    return result


def _tag_enums(enums: dict, subset_name: str) -> dict:
    """Add in_subset to each top-level enum definition dict."""
    return {k: {**v, "in_subset": [subset_name]} for k, v in enums.items()}


class _LiteralStr(str):
    pass


def _literal_representer(dumper, data):
    if "\n" in data or len(data) > 80:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


def _setup_yaml() -> yaml.Dumper:
    class _Dumper(yaml.Dumper):
        pass

    _Dumper.add_representer(str, _literal_representer)
    _Dumper.add_representer(_LiteralStr, _literal_representer)
    return _Dumper


# Top-level keys that get a blank line before them (section boundaries)
_SECTION_KEYS = frozenset([
    "prefixes",        # after header metadata group
    "default_prefix",  # after prefixes dict
    "imports",         # after default_prefix/default_range scalars
    "subsets", "types", "enums", "slots", "classes",
])
# Sections whose named entries get blank lines between them
_ELEMENT_SECTION_KEYS = frozenset(["classes", "slots", "enums", "subsets"])


def _add_blank_lines(text: str) -> str:
    """Add blank lines between schema sections and between element entries."""
    lines = text.split("\n")
    output: list[str] = []
    in_elements = False

    for line in lines:
        if not line.strip():
            output.append(line)
            continue

        indent = len(line) - len(line.lstrip())

        if indent == 0 and ":" in line:
            key = line.split(":")[0].strip()
            if key in _SECTION_KEYS and output and output[-1] != "":
                output.append("")
            in_elements = key in _ELEMENT_SECTION_KEYS
        elif indent == 2 and in_elements and not line.lstrip().startswith("-"):
            if output and output[-1] != "":
                output.append("")

        output.append(line)

    # Collapse multiple consecutive blank lines to one
    result: list[str] = []
    prev_blank = False
    for line in output:
        is_blank = not line.strip()
        if is_blank and prev_blank:
            continue
        result.append(line)
        prev_blank = is_blank

    return "\n".join(result)


def dump_yaml(schema: dict) -> str:
    dumper = _setup_yaml()
    raw = yaml.dump(
        schema,
        Dumper=dumper,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        width=120,
    )
    return _add_blank_lines(raw)


# ---------------------------------------------------------------------------
# Schema assembly
# ---------------------------------------------------------------------------

def get_ontology_iri(g: Graph) -> str | None:
    """Return the owl:Ontology IRI from a graph, or None if absent."""
    for s in g.subjects(RDF.type, OWL.Ontology):
        if isinstance(s, URIRef):
            return str(s)
    return None


def _base_prefixes() -> dict[str, str]:
    return {
        "gist": LMODEL_NS,
        "gist_semanticarts": GIST_SA_NS,
        "gistd": GISTD_NS,
        "linkml": "https://w3id.org/linkml/",
        "schema": "http://schema.org/",
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "dcterms": "http://purl.org/dc/terms/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "owl": "http://www.w3.org/2002/07/owl#",
    }


def build_schema(
    classes: dict,
    slots: dict,
    enums: dict,
    version: str = "14.1.0",
    schema_id: str = f"{LMODEL_BASE}/core",
    schema_name: str = "gist_core",
    source: str | None = None,
) -> dict:
    subset_name = "gist_core"
    prefixes = _base_prefixes()
    prefixes.update({
        "media_app": "https://www.iana.org/assignments/media-types/application/",
        "media_img": "https://www.iana.org/assignments/media-types/image/",
        "media_txt": "https://www.iana.org/assignments/media-types/text/",
    })
    schema: dict[str, Any] = {
        "id": schema_id,
        "name": schema_name,
        "title": "gist Core",
        "description": (
            "gist, a upper ontology for the Enterprise."
            "This LinkML schema is generated from gistCore " + version + "."
        ),
        "license": "CC-BY-4.0",
        "see_also": [
            "https://lmodel.github.io/gist",
            "https://www.semanticarts.com/gist/",
        ],
        "version": version,
    }
    if source:
        schema["source"] = source

    # Inject GistThing mixin for universal slots (name, description have no OWL domain)
    classes = dict(classes)  # copy to avoid mutating caller's dict
    classes["GistThing"] = {
        "mixin": True,
        "description": (
            "Mixin providing universal slots applicable to any GIST entity. "
            "Covers OWL properties with no rdfs:domain (open-world)."
        ),
        "slots": ["name", "description"],
        "in_subset": [subset_name],
    }
    # Apply GistThing mixin to all root classes (no is_a  -> no inherited slots)
    for cls_entry in classes.values():
        if not cls_entry.get("is_a") and not cls_entry.get("mixin"):
            existing = cls_entry.get("mixins", [])
            if "GistThing" not in existing:
                cls_entry["mixins"] = ["GistThing"] + existing

    schema.update({
        "prefixes": prefixes,
        "default_prefix": "gist",
        "default_range": "string",
        "imports": ["linkml:types"],
        "subsets": {
            subset_name: {
                "description": "Classes and slots from the gist Core ontology module.",
            }
        },
        "classes": _order_elements(classes, subset_name),
        "slots": _order_elements(slots, subset_name),
        "enums": _tag_enums(enums, subset_name),
    })
    return _order_keys(schema, _SCHEMA_KEY_ORDER)


def build_media_types_schema(
    enums: dict,
    version: str = "14.1.0",
    source: str | None = None,
) -> dict:
    subset_name = "gist_media_types"
    prefixes = _base_prefixes()
    prefixes.update({
        "media_app": "https://www.iana.org/assignments/media-types/application/",
        "media_img": "https://www.iana.org/assignments/media-types/image/",
        "media_txt": "https://www.iana.org/assignments/media-types/text/",
    })
    schema: dict[str, Any] = {
        "id": f"{LMODEL_BASE}/media-types",
        "name": "gist_media_types",
        "title": "gist Media Types",
        "description": (
            f"IANA Media Type named individuals from gist {version}. "
            "Imports gist_core for class definitions."
        ),
        "license": "CC-BY-4.0",
        "see_also": ["https://www.semanticarts.com/gist/"],
        "version": version,
    }
    if source:
        schema["source"] = source
    schema.update({
        "prefixes": prefixes,
        "default_prefix": "gist",
        "default_range": "string",
        "imports": ["linkml:types", "./gist_core"],
        "subsets": {
            subset_name: {
                "description": "IANA Media Type instances from the gist Media Types module.",
            }
        },
        "enums": _tag_enums(enums, subset_name),
    })
    return _order_keys(schema, _SCHEMA_KEY_ORDER)


def build_prefix_declarations_schema(
    pv: dict,
    version: str = "14.1.0",
    source: str | None = None,
) -> dict:
    subset_name = "gist_prefix_declarations"
    prefixes = _base_prefixes()
    prefixes["sh"] = "http://www.w3.org/ns/shacl#"
    schema: dict[str, Any] = {
        "id": f"{LMODEL_BASE}/prefix-declarations",
        "name": "gist_prefix_declarations",
        "title": "gist Prefix Declarations",
        "description": (
            f"SHACL prefix declarations from gist {version}. "
            "Defines namespace-to-prefix bindings used by the gist ontology."
        ),
        "license": "CC-BY-4.0",
        "see_also": ["https://www.semanticarts.com/gist/"],
        "version": version,
    }
    if source:
        schema["source"] = source
    schema.update({
        "prefixes": prefixes,
        "default_prefix": "gist",
        "default_range": "string",
        "imports": ["linkml:types"],
        "subsets": {
            subset_name: {
                "description": "SHACL prefix declaration instances from the gist Prefix Declarations module.",
            }
        },
        "enums": {
            "PrefixDeclarationInstance": {
                "description": "Named SHACL prefix declarations from the gist ontology.",
                "in_subset": [subset_name],
                "permissible_values": pv,
            }
        },
    })
    return _order_keys(schema, _SCHEMA_KEY_ORDER)


def build_rdfs_annotations_schema(
    classes: dict,
    slots: dict,
    version: str = "14.1.0",
    source: str | None = None,
) -> dict:
    subset_name = "gist_rdfs_annotations"
    schema: dict[str, Any] = {
        "id": f"{LMODEL_BASE}/rdfs-annotations",
        "name": "gist_rdfs_annotations",
        "title": "gist RDFS Annotations",
        "description": (
            f"RDFS label and comment annotations for gist classes and properties ({version}). "
            "Documentation-layer schema: rdfs:label  -> aliases; "
            "rdfs:comment DEFINITION:/EXAMPLE:/NOTE: prefixes  -> description/examples/comments."
        ),
        "license": "CC-BY-4.0",
        "see_also": ["https://www.semanticarts.com/gist/"],
        "version": version,
    }
    if source:
        schema["source"] = source
    schema.update({
        "prefixes": _base_prefixes(),
        "default_prefix": "gist",
        "default_range": "string",
        "imports": ["linkml:types"],
        "subsets": {
            subset_name: {
                "description": "Classes and slots annotated from the gist RDFS Annotations module.",
            }
        },
        "classes": _order_elements(classes, subset_name),
        "slots": _order_elements(slots, subset_name),
    })
    return _order_keys(schema, _SCHEMA_KEY_ORDER)


def build_sub_class_assertions_schema(
    classes: dict,
    version: str = "14.1.0",
    source: str | None = None,
) -> dict:
    subset_name = "gist_sub_class_assertions"
    schema: dict[str, Any] = {
        "id": f"{LMODEL_BASE}/sub-class-assertions",
        "name": "gist_sub_class_assertions",
        "title": "gist Subclass Assertions",
        "description": (
            f"Explicit rdfs:subClassOf assertions for gist classes ({version}). "
            "Supplement for RL reasoners that do not infer subclass relationships "
            "from OWL equivalentClass axioms."
        ),
        "license": "CC-BY-4.0",
        "see_also": ["https://www.semanticarts.com/gist/"],
        "version": version,
    }
    if source:
        schema["source"] = source
    schema.update({
        "prefixes": _base_prefixes(),
        "default_prefix": "gist",
        "default_range": "string",
        "imports": ["linkml:types"],
        "subsets": {
            subset_name: {
                "description": "Classes asserted via rdfs:subClassOf in the gist Sub Class Assertions module.",
            }
        },
        "classes": _order_elements(classes, subset_name),
    })
    return _order_keys(schema, _SCHEMA_KEY_ORDER)


def build_gist_schema(version: str = "14.1.0") -> dict:
    """Build the top-level gist.yaml that imports all compatible module schemas."""
    schema: dict[str, Any] = {
        "id": LMODEL_BASE,
        "name": "gist",
        "title": "gist",
        "description": (
            "gist  is a minimalist upper ontology "
            "created by Semantic Arts for enterprise knowledge graph applications. "
            "This LinkML schema (version " + version + ") aggregates the gist modules: "
            "Core (classes and properties), MediaTypes (IANA media type instances), and "
            "PrefixDeclarations (SHACL namespace bindings). "
            "Supplementary schemas gist_rdfs_annotations and gist_sub_class_assertions "
            "are available for annotation enrichment and OWL RL reasoner support."
        ),
        "license": "CC-BY-4.0",
        "see_also": [
            "https://www.semanticarts.com/gist/",
            "https://w3id.org/semanticarts/ontology/gistCore",
            "https://lmodel.github.io/gist",

        ],
        "version": version,
        "prefixes": {
            "gist": LMODEL_NS,
            "gist_semanticarts": GIST_SA_NS,
            "gistd": GISTD_NS,
            "linkml": "https://w3id.org/linkml/",
            "media_app": "https://www.iana.org/assignments/media-types/application/",
            "media_img": "https://www.iana.org/assignments/media-types/image/",
            "media_txt": "https://www.iana.org/assignments/media-types/text/",
        },
        "default_prefix": "gist",
        "default_range": "string",
        "imports": [
            "linkml:types",
            "./gist_core",
            "./gist_media_types",
            "./gist_prefix_declarations",
        ],
    }
    return _order_keys(schema, _SCHEMA_KEY_ORDER)


# ---------------------------------------------------------------------------
# Coverage report
# ---------------------------------------------------------------------------

def coverage_report(g: Graph, classes: dict, slots: dict, enums: dict) -> str:
    n_classes = sum(
        1 for s in g.subjects(RDF.type, OWL.Class)
        if isinstance(s, URIRef) and gist_local(s)
    )
    n_obj_props = sum(
        1 for s in g.subjects(RDF.type, OWL.ObjectProperty)
        if isinstance(s, URIRef) and gist_local(s)
    )
    n_data_props = sum(
        1 for s in g.subjects(RDF.type, OWL.DatatypeProperty)
        if isinstance(s, URIRef) and gist_local(s)
    )
    n_ann_props = sum(
        1 for s in g.subjects(RDF.type, OWL.AnnotationProperty)
        if isinstance(s, URIRef) and gist_local(s)
    )
    n_prefix_decls = sum(
        1 for s in g.subjects(RDF.type, SH.PrefixDeclaration)
        if isinstance(s, URIRef)
    )

    lines = [
        "Coverage report",
        "---------------",
        f"  OWL classes:              {n_classes:4d}   ->  LinkML classes: {len(classes):4d}",
        f"  OWL object properties:    {n_obj_props:4d}",
        f"  OWL datatype properties:  {n_data_props:4d}",
        f"  OWL annotation props:     {n_ann_props:4d}",
        f"                                     ->  LinkML slots:   {len(slots):4d}",
        f"  Enum groups:                       ->  LinkML enums:   {len(enums):4d}",
        f"  Enum values total:               {sum(len(e.get('permissible_values', {})) for e in enums.values()):5d}",
        f"  SHACL prefix decls:       {n_prefix_decls:4d}",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Per-file generation helpers
# ---------------------------------------------------------------------------

def _file_type(path: Path) -> str:
    """Classify a TTL file by content type based on filename patterns."""
    stem = re.sub(r"\d+\.\d+\.\d+$", "", path.stem)  # strip version suffix
    stem_lower = stem.lower()
    if "mediatype" in stem_lower:
        return "media_types"
    if "prefix" in stem_lower:
        return "prefix_declarations"
    if "rdfs" in stem_lower or "annotation" in stem_lower:
        return "rdfs_annotations"
    if "subclass" in stem_lower:
        return "sub_class_assertions"
    if "core" in stem_lower:
        return "core"
    return "core"  # default


def _write_schema_file(
    schema: dict,
    path: Path,
    report: bool = False,
    g: Graph | None = None,
) -> None:
    yaml_text = dump_yaml(schema)
    path.write_text(yaml_text, encoding="utf-8")
    n_cls = len(schema.get("classes", {}))
    n_slt = len(schema.get("slots", {}))
    n_enm = len(schema.get("enums", {}))
    n_pv = sum(
        len(e.get("permissible_values", {}))
        for e in schema.get("enums", {}).values()
    )
    print(
        f"   -> {path.name}  "
        f"(classes={n_cls}, slots={n_slt}, enums={n_enm}, enum_values={n_pv})",
        file=sys.stderr,
    )
    if report and g is not None:
        print(
            coverage_report(g, schema.get("classes", {}), schema.get("slots", {}), schema.get("enums", {})),
            file=sys.stderr,
        )


def generate_per_file_schemas(
    ttl_files: list[Path],
    output_dir: Path,
    version: str = "14.1.0",
    report: bool = False,
) -> None:
    """Generate one schema YAML per input TTL file into output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Classify input files by content type
    typed: dict[str, Path] = {}
    for f in ttl_files:
        ftype = _file_type(f)
        if ftype in typed:
            print(
                f"Warning: multiple files map to '{ftype}'; keeping {typed[ftype].name}, skipping {f.name}",
                file=sys.stderr,
            )
        else:
            typed[ftype] = f

    # Load each file into its own graph
    graphs: dict[str, Graph] = {}
    for ftype in ("core", "rdfs_annotations", "sub_class_assertions", "media_types", "prefix_declarations"):
        if ftype not in typed:
            continue
        g = Graph()
        print(f"  Loading {typed[ftype].name} ({ftype}) ...", file=sys.stderr)
        g.parse(str(typed[ftype]), format="turtle")
        graphs[ftype] = canonical_graph(g)
        print(f"    {len(g)} triples", file=sys.stderr)

    # ---- 1. gist_core.yaml ----
    # Enrich with rdfs annotations + subclass assertions for 100% coverage
    print("\nBuilding gist_core.yaml ...", file=sys.stderr)
    g_core_enriched = Graph()
    for ftype in ("core", "rdfs_annotations", "sub_class_assertions"):
        if ftype in graphs:
            g_core_enriched += graphs[ftype]
    g_core_enriched = canonical_graph(g_core_enriched)

    classes = extract_classes(g_core_enriched)
    slots = extract_slots(g_core_enriched)
    enums = extract_enums(g_core_enriched)
    core_schema = build_schema(
        classes, slots, enums,
        version=version,
        schema_id=f"{LMODEL_BASE}/core",
        schema_name="gist_core",
        source=get_ontology_iri(graphs.get("core", Graph())),
    )
    _write_schema_file(core_schema, output_dir / "gist_core.yaml", report, g_core_enriched)

    # ---- 2. gist_media_types.yaml ----
    if "media_types" in graphs:
        print("Building gist_media_types.yaml ...", file=sys.stderr)
        g_media = graphs["media_types"]
        media_enums = extract_enums(g_media)
        media_schema = build_media_types_schema(
            media_enums, version, source=get_ontology_iri(g_media)
        )
        _write_schema_file(media_schema, output_dir / "gist_media_types.yaml", report, g_media)

    # ---- 3. gist_prefix_declarations.yaml ----
    if "prefix_declarations" in graphs:
        print("Building gist_prefix_declarations.yaml ...", file=sys.stderr)
        g_prefix = graphs["prefix_declarations"]
        pv = extract_prefix_declarations(g_prefix)
        prefix_schema = build_prefix_declarations_schema(
            pv, version, source=get_ontology_iri(g_prefix)
        )
        _write_schema_file(prefix_schema, output_dir / "gist_prefix_declarations.yaml", report, g_prefix)

    # ---- 4. gist_rdfs_annotations.yaml ----
    if "rdfs_annotations" in graphs:
        print("Building gist_rdfs_annotations.yaml ...", file=sys.stderr)
        g_annot = graphs["rdfs_annotations"]
        # Use core as context for class-vs-slot classification
        g_ctx = graphs.get("core", Graph())
        annot_classes, annot_slots = extract_rdfs_annotations(g_annot, ctx=g_ctx)
        annot_schema = build_rdfs_annotations_schema(
            annot_classes, annot_slots, version, source=get_ontology_iri(g_annot)
        )
        _write_schema_file(annot_schema, output_dir / "gist_rdfs_annotations.yaml", report, g_annot)

    # ---- 5. gist_sub_class_assertions.yaml ----
    if "sub_class_assertions" in graphs:
        print("Building gist_sub_class_assertions.yaml ...", file=sys.stderr)
        g_sub = graphs["sub_class_assertions"]
        sub_classes = extract_sub_class_assertions(g_sub)
        sub_schema = build_sub_class_assertions_schema(
            sub_classes, version, source=get_ontology_iri(g_sub)
        )
        _write_schema_file(sub_schema, output_dir / "gist_sub_class_assertions.yaml", report, g_sub)

    # ---- 6. gist.yaml (main entry-point, imports core + media_types + prefix_declarations) ----
    print("Building gist.yaml ...", file=sys.stderr)
    gist_schema = build_gist_schema(version=version)
    _write_schema_file(gist_schema, output_dir / "gist.yaml")

    print(f"\nPer-file generation complete  -> {output_dir}", file=sys.stderr)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    default_ttl_dir = (
        Path(__file__).parent.parent
        / "upstream/gist14.1.0_webDownload/ontologies/turtle"
    )
    default_output_dir = Path(__file__).parent.parent / "src/gist/schema"

    parser = argparse.ArgumentParser(
        description="Generate five LinkML schemas from GIST OWL Turtle files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        metavar="TTL_FILE",
        help=f"Input Turtle/OWL files (default: {default_ttl_dir}/*.ttl)",
    )
    parser.add_argument(
        "-d", "--output-dir",
        metavar="DIR",
        default=str(default_output_dir),
        help=f"Output directory (default: {default_output_dir})",
    )
    parser.add_argument(
        "--version",
        default="14.1.0",
        help="GIST version string to embed in the schemas (default: 14.1.0)",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Print a coverage report to stderr",
    )
    args = parser.parse_args()

    if args.inputs:
        ttl_files = [Path(f) for f in args.inputs]
    else:
        ttl_files = sorted(default_ttl_dir.glob("*.ttl"))

    if not ttl_files:
        parser.error(f"No TTL files found in {default_ttl_dir}")

    generate_per_file_schemas(
        ttl_files,
        Path(args.output_dir),
        version=args.version,
        report=args.report,
    )


if __name__ == "__main__":
    main()
