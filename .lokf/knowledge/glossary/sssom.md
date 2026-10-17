---
type: GlossaryTerm
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/glossary/sssom
title: SSSOM
description: "Simple Standard for Sharing Ontological Mappings: the tab-separated format with a YAML metadata header in which this repository keeps its cross-vocabulary mappings."
resource: https://mapping-commons.github.io/sssom/
abbreviation: SSSOM
definition: A tab-separated table format, preceded by a commented YAML metadata block, in which each row maps a subject term to an object term through a mapping predicate and records the justification for the match.
sources:
- resource: https://mapping-commons.github.io/sssom/
- resource: tests/test_sssom_files.py
  title: the JUSTIFICATIONS set and its note on semapv:LLMBasedMatching
- resource: https://pypi.org/project/sssom-schema/
  title: sssom-schema releases, 1.1.0a5 the latest
- resource: https://github.com/mapping-commons/sssom/blob/master/src/sssom_schema/schema/sssom_schema.yaml
  title: the SSSOM schema on its master branch, whose mapping_justification pattern lists LLMBasedMatching
generated:
  by: process:ktl-librarian
  at: "2026-10-17T00:13:57Z"
status: draft
---

# SSSOM

SSSOM (Simple Standard for Sharing Ontological Mappings) is the format of the three files under `src/gist/mappings/`. Each starts with `#`-prefixed metadata, then a header row and one mapping per row. The metadata keys are `mapping_set_id`, `mapping_set_version`, `curie_map`, `license`, `subject_source`, `object_source` and `mapping_date`. Here, the predicates are SKOS mapping properties and the justifications come from the semapv vocabulary: `semapv:ManualMappingCuration` for the [CDM set](../datasets/gist-cdm-mappings.md), and `semapv:LLMBasedMatching` for the [DPV](../datasets/gist-dpvs-mappings.md) and [ISO/IEC 22989](../datasets/gist-iso22989-mappings.md) sets. SEMAPV defines `LLMBasedMatching`, but no SSSOM schema release lists it yet: sssom-schema 1.1.0a5, the latest on PyPI, does not, so sssom-py rejects those two sets on that field alone. The schema's `master` branch on GitHub already lists it. `tests/test_sssom_files.py` checks the rest of the format.
