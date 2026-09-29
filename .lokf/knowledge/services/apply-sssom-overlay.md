---
type: Service
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/services/apply-sssom-overlay
title: SSSOM overlay
description: Command-line script (scripts/apply_sssom_overlay.py, run as just apply-sssom-overlay) that merges the curated SSSOM mappings into the gist LinkML schema.
resource: https://github.com/lmodel/gist/blob/main/scripts/apply_sssom_overlay.py
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
  at: "2026-09-29T10:32:37Z"
status: draft
---

# SSSOM overlay

`just apply-sssom-overlay` runs `scripts/apply_sssom_overlay.py --schema-dir src/gist/schema --mappings-dir src/gist/mappings` after `just gen-linkml`. For every class, enum, type or slot whose name is the subject of a row in one of the three mapping sets ([CDM](../datasets/gist-cdm-mappings.md), [DPVs](../datasets/gist-dpvs-mappings.md), [ISO/IEC 22989](../datasets/gist-iso22989-mappings.md)), it merges the object CURIE into the matching `exact_mappings`, `close_mappings`, `broad_mappings`, `narrow_mappings` or `related_mappings` slot of the [gist LinkML schema](../datasets/gist-linkml-schema.md), and declares any new object-side prefix from the TSV's `curie_map`. It keeps existing entries, drops duplicates, rewrites the YAML with ruamel.yaml in round-trip mode, and is idempotent. The script is schema-independent: `--schema` and `--subject-prefix` let it target another lmodel schema.
