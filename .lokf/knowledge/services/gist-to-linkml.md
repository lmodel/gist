---
type: Service
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/services/gist-to-linkml
title: gist-to-LinkML transform
description: Command-line script (scripts/gist_to_linkml.py, run as just gen-linkml) that turns the gist Turtle modules into the five gist LinkML schema modules.
resource: https://github.com/lmodel/gist/blob/main/scripts/gist_to_linkml.py
tags:
  - cli
dependsOn:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-upstream-turtle
generated:
  by: process:ktl-librarian
  at: "2026-09-29T10:32:37Z"
status: draft
---

# gist-to-LinkML transform

`uv run python scripts/gist_to_linkml.py [TTL_FILE ...] [-d OUTPUT_DIR]`, wrapped as `just gen-linkml`, reads the [upstream Turtle modules](../datasets/gist-upstream-turtle.md) with rdflib and writes one LinkML schema per module into `src/gist/schema/`: `gist_core.yaml` (enriched by the RdfsAnnotations and SubClassAssertions modules), `gist_media_types.yaml`, `gist_prefix_declarations.yaml`, `gist_rdfs_annotations.yaml` and `gist_sub_class_assertions.yaml`. The result is the [gist LinkML schema](../datasets/gist-linkml-schema.md).

Its stated goal is full coverage: every `owl:Class` becomes a class; every object, datatype and gist annotation property becomes a slot; named individuals become enum permissible values; SHACL prefix declarations become the `PrefixDeclarationInstance` enum; SKOS and RDFS annotations are kept; and OWL axioms with no LinkML equivalent are kept as notes. It re-homes terms from the upstream namespace `https://w3id.org/semanticarts/ns/ontology/gist/` into `https://w3id.org/lmodel/gist/`. `tests/test_owl_to_linkml.py` holds 159 unit tests for it.
