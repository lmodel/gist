---
type: Service
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/services/gist-to-linkml
title: gist-to-LinkML transform
description: Command-line script (scripts/gist_to_linkml.py, run as just gen-linkml) that turns the gist Turtle modules into the gist LinkML schema modules, keeping each term's gist IRI.
resource: scripts/gist_to_linkml.py
tags:
- cli
dependsOn:
- https://w3id.org/lmodel/gist/knowledge/datasets/gist-upstream-turtle
generated:
  by: process:ktl-librarian
  at: "2026-10-17T00:13:57Z"
status: draft
---

# gist-to-LinkML transform

The transform reads the [upstream Turtle modules](../datasets/gist-upstream-turtle.md) with rdflib and writes one LinkML schema per module into `src/gist/schema/`: `gist_core.yaml` (enriched by the RdfsAnnotations and SubClassAssertions modules), `gist_media_types.yaml`, `gist_prefix_declarations.yaml`, `gist_rdfs_annotations.yaml` and `gist_sub_class_assertions.yaml`, plus the aggregator `gist.yaml`. The result is the [gist LinkML schema](../datasets/gist-linkml-schema.md). Run it as `uv run python scripts/gist_to_linkml.py [TTL_FILE ...] [-d OUTPUT_DIR] [--rename OLD=NEW ...]`, which `just gen-linkml` wraps.

Its stated goal is full coverage:

- every `owl:Class` becomes a class;
- every object, datatype and gist annotation property becomes a slot;
- named individuals become enum permissible values;
- SHACL prefix declarations become the `PrefixDeclarationInstance` enum;
- SKOS and RDFS annotations are kept on classes, slots, individuals and each module's ontology header;
- `gist:domainIncludes` and `rangeIncludes` become slot annotations;
- `owl:FunctionalProperty` becomes `multivalued: false`;
- an object property that gist leaves unranged gets the range `Any`, a class whose `class_uri` is `linkml:Any`;
- OWL axioms with no LinkML equivalent, such as restrictions, equivalent classes and union domains, are kept as notes.

It keeps each term's gist IRI: `class_uri` and `slot_uri` are `gist:` CURIEs in Semantic Arts' namespace, and only what it adds (the `GistThing` mixin, the enums and the subsets) takes lmodel's `gist_linkml:` namespace ([gist namespace policy](../policies/gist-namespace-policy.md)). Its output is deterministic: it relabels blank nodes canonically and reads the graph in sorted order, so a rerun reproduces the committed schema byte for byte. `tests/test_owl_to_linkml.py` holds 200 unit tests for it.

`--rename OLD=NEW`, which can be repeated, gives a gist class or slot another LinkML name. The element keeps its IRI and takes its old name as an alias, and every reference to it is rewritten. A schema that imports gist beside another vocabulary defining the same name needs this, because LinkML keeps only the last import's definition of a name. `just gen-lokf-copy` uses it to build the [LOKF copy](../datasets/gist-lokf-copy.md).
