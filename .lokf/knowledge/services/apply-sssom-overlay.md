---
type: Service
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/services/apply-sssom-overlay
title: SSSOM overlay
description: Command-line script (scripts/apply_sssom_overlay.py, run as just apply-sssom-overlay) that merges the curated SSSOM mappings into the gist LinkML schema.
resource: scripts/apply_sssom_overlay.py
tags:
- cli
dependsOn:
- https://w3id.org/lmodel/gist/knowledge/datasets/gist-cdm-mappings
- https://w3id.org/lmodel/gist/knowledge/datasets/gist-dpvs-mappings
- https://w3id.org/lmodel/gist/knowledge/datasets/gist-iso22989-mappings
- https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
references:
- https://w3id.org/lmodel/gist/knowledge/glossary/sssom
generated:
  by: process:ktl-librarian
  at: "2026-10-17T00:13:57Z"
status: draft
verified:
- by: process:ktl-librarian
  at: "2026-10-16T23:47:53Z"
---

# SSSOM overlay

`just apply-sssom-overlay` runs `scripts/apply_sssom_overlay.py --schema-dir src/gist/schema --mappings-dir src/gist/mappings` after `just gen-linkml`. It reads the rows of the three mapping sets ([CDM](../datasets/gist-cdm-mappings.md), [DPV](../datasets/gist-dpvs-mappings.md), [ISO/IEC 22989](../datasets/gist-iso22989-mappings.md)). It expands each row's subject with its TSV's `curie_map` and matches it to the element with that IRI: its `class_uri`, `slot_uri`, `enum_uri` or permissible-value `meaning`, else `default_prefix:name`. For every class, slot, enum, type or permissible value so matched, it merges the object CURIE into the matching `exact_mappings`, `close_mappings`, `broad_mappings`, `narrow_mappings` or `related_mappings` slot of the [gist LinkML schema](../datasets/gist-linkml-schema.md). It also declares any new object-side prefix from the TSV's `curie_map`. It keeps existing entries, drops duplicates, rewrites the YAML with ruamel.yaml in round-trip mode, and is idempotent. Matching by IRI keeps a row on the right element where a gist term such as `gist:hasParty` is rendered as the snake_case slot `has_party`. The script is schema-independent: `--schema` lets it target another lmodel schema.
