---
type: Dataset
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/datasets/gist-cdm-mappings
title: gist to Common Domain Model mappings
description: 34 manually curated SSSOM mappings from gist classes to FINOS Common Domain Model classes in the lmodel CDM schema.
resource: src/gist/mappings/gist-cdm.sssom.tsv
license: https://creativecommons.org/licenses/by/4.0/
fields:
- name: subject_id
  description: gist CURIE being mapped (subject side is always gist).
- name: subject_label
  description: Label of the gist term.
- name: predicate_id
  description: SKOS mapping predicate (exactMatch, closeMatch, broadMatch, narrowMatch, relatedMatch).
- name: object_id
  description: CURIE of the term in the other vocabulary.
- name: object_label
  description: Label of the other term.
- name: mapping_justification
  description: semapv justification for the row.
- name: comment
  description: Curator's note on the match.
distribution:
- name: gist-cdm.sssom.tsv
  access_url: https://github.com/lmodel/gist/blob/main/src/gist/mappings/gist-cdm.sssom.tsv
  media_type: text/tab-separated-values
about:
- https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
- https://w3id.org/lmodel/gist/knowledge/references/common-domain-model
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

# gist to Common Domain Model mappings

`src/gist/mappings/gist-cdm.sssom.tsv` maps gist classes such as Organization, Person, Agreement, Magnitude and ID to classes of the [Common Domain Model schema](../references/common-domain-model.md). It declares the mapping set `https://w3id.org/lmodel/gist/mappings/gist-cdm`, version 1.0, dated 2026-09-29 and licensed CC BY 4.0. It holds 34 rows, every one justified `semapv:ManualMappingCuration`: 11 `skos:closeMatch`, 11 `skos:relatedMatch`, 9 `skos:narrowMatch` and 3 `skos:broadMatch`. The [SSSOM overlay](../services/apply-sssom-overlay.md) merges them into the [gist LinkML schema](gist-linkml-schema.md).
