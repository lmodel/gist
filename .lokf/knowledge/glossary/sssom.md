---
type: GlossaryTerm
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/glossary/sssom
title: SSSOM
description: "Simple Standard for Sharing Ontological Mappings: the tab-separated format with a YAML metadata header in which this repository keeps its cross-vocabulary mappings."
resource: https://mapping-commons.github.io/sssom/
abbreviation: SSSOM
definition: "A tab-separated table format, preceded by a commented YAML metadata block, in which each row maps a subject term to an object term through a mapping predicate and records the justification for the match."
sources:
  - resource: https://mapping-commons.github.io/sssom/
generated:
  by: process:ktl-librarian
  at: "2026-09-29T10:32:37Z"
status: draft
---

# SSSOM

SSSOM (Simple Standard for Sharing Ontological Mappings) is the format of the three files under `src/gist/mappings/`. Each starts with `#`-prefixed metadata (`mapping_set_id`, `mapping_set_version`, `curie_map`, `license`, `subject_source`, `object_source`, `mapping_date`), then a header row and one mapping per row. Here, the predicates are SKOS mapping properties and the justifications come from the semapv vocabulary: `semapv:ManualMappingCuration` for the [CDM set](../datasets/gist-cdm-mappings.md), and `semapv:LLMBasedMatching` for the [DPV](../datasets/gist-dpvs-mappings.md) and [ISO/IEC 22989](../datasets/gist-iso22989-mappings.md) sets. SEMAPV defines `LLMBasedMatching`, but the SSSOM schema does not yet allow it, so sssom-py rejects those two sets on that field alone. `tests/test_sssom_files.py` checks the rest of the format.
