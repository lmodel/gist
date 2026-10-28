---
type: Service
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/services/gist-to-linkml
title: gist-to-LinkML transform
description: Command-line script (scripts/gist_to_linkml.py, run as just gen-linkml) that turns the gist Turtle modules into the gist LinkML schema modules, keeping each term's gist IRI and putting each property's slot on the classes its domain allows.
resource: scripts/gist_to_linkml.py
tags:
  - cli
dependsOn:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-upstream-turtle
generated:
  by: process:ktl-librarian
  at: "2026-10-28T18:37:55Z"
status: draft
---

# gist-to-LinkML transform

The transform reads the [upstream Turtle modules](../datasets/gist-upstream-turtle.md) with rdflib and writes one LinkML schema per module into `src/gist/schema/`: `gist_core.yaml` (enriched by the RdfsAnnotations and SubClassAssertions modules), `gist_media_types.yaml`, `gist_prefix_declarations.yaml`, `gist_rdfs_annotations.yaml` and `gist_sub_class_assertions.yaml`, plus the aggregator `gist.yaml`. The result is the [gist LinkML schema](../datasets/gist-linkml-schema.md). Run it as `uv run python scripts/gist_to_linkml.py [TTL_FILE ...] [-d OUTPUT_DIR] [--rename OLD=NEW ...]`, which `just gen-linkml` runs.

Its stated goal is full coverage:

- every `owl:Class` becomes a class;
- every object, datatype and gist annotation property becomes a slot, and an annotation property's slot says so with `implements: owl:AnnotationProperty`;
- the slot of an object or datatype property belongs to each class its `rdfs:domain` names, alone or in a union, and to their subclasses;
- the slot of a property gist declares without a domain belongs to the `GistThing` mixin, which every class includes, because OWL lets that property describe any individual;
- `gist:domainIncludes` and `rangeIncludes` become slot annotations only, never a domain or a range;
- `owl:FunctionalProperty` becomes `multivalued: false`;
- an object property that gist leaves unranged takes the range of its nearest ranged superproperty, or else `Any`, a class whose `class_uri` is `linkml:Any`;
- a union range becomes `any_of`, with `Any` as its range;
- each XSD or OWL datatype becomes the `linkml:types` type with that datatype's IRI, or, where there is none, a type of `gist_core` with that IRI, such as `xsd_int`;
- an element's `skos:prefLabel`, or else its `rdfs:label`, becomes its `title`, and its other labels become aliases;
- a term gist marks `owl:deprecated` gets a reason in `deprecated` and an `owl:deprecated: true` annotation, which the generated OWL contains;
- named individuals become enum permissible values;
- SHACL prefix declarations become the `PrefixDeclarationInstance` enum;
- SKOS and RDFS annotations are kept on classes, slots, individuals and each module's ontology header, without their Windows line ends and the tab indent their lines share;
- OWL axioms with no LinkML equivalent, such as restrictions, equivalent classes and union domains, are kept as notes.

The transform stops with an error at a domain whose slot no set of classes carries faithfully:

- two domains, which OWL reads as their intersection;
- an anonymous class other than a union;
- a class that gist does not declare.

gist 14.1.0 has none of these.

The transform keeps each term's gist IRI: `class_uri` and `slot_uri` are `gist:` CURIEs in Semantic Arts' namespace. Only what it adds gets an IRI in lmodel's `gist_linkml:` namespace: the `GistThing` mixin, the types for the datatypes `linkml:types` lacks, the enums and the subsets ([gist namespace policy](../policies/gist-namespace-policy.md)). Its output is deterministic: it relabels blank nodes canonically and reads the graph in sorted order, so a rerun reproduces the committed schema byte for byte. `tests/test_owl_to_linkml.py` holds 231 unit tests for it.

`--rename OLD=NEW`, which can be repeated, gives a gist class or slot another LinkML name. The element keeps its IRI, and takes its old name as an alias unless that is already its title. Every reference to the element is rewritten. A schema that imports gist beside another vocabulary defining the same name needs this option, because LinkML keeps only the last import's definition of a name.
