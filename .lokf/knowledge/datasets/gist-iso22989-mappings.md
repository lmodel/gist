---
type: Dataset
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/datasets/gist-iso22989-mappings
title: gist to ISO/IEC 22989 mappings
description: 9 LLM-matched SSSOM mappings from gist classes to the lmodel ISO/IEC 22989:2022 AI concepts and terminology schema.
resource: https://github.com/lmodel/gist/blob/main/src/gist/mappings/gist-iso22989.sssom.tsv
license: https://creativecommons.org/licenses/by/4.0/
fields:
  - name: subject_id
    description: gist CURIE being mapped (subject side is always gist).
  - name: subject_label
    description: Label of the gist term.
  - name: subject_category
    description: Kind of subject element, e.g. owl:Class.
  - name: predicate_id
    description: SKOS mapping predicate (exactMatch, closeMatch, broadMatch, narrowMatch, relatedMatch).
  - name: predicate_label
    description: Human-readable predicate name.
  - name: object_id
    description: CURIE of the term in the other vocabulary.
  - name: object_label
    description: Label of the other term.
  - name: object_category
    description: Kind of object element, e.g. owl:Class.
  - name: mapping_justification
    description: semapv justification for the row.
  - name: comment
    description: Curator's note on the match.
distribution:
  - name: gist-iso22989.sssom.tsv
    access_url: https://github.com/lmodel/gist/blob/main/src/gist/mappings/gist-iso22989.sssom.tsv
    media_type: text/tab-separated-values
about:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
  - https://w3id.org/lmodel/gist/knowledge/references/iso22989
references:
  - https://w3id.org/lmodel/gist/knowledge/glossary/sssom
generated:
  by: process:ktl-librarian
  at: "2026-09-29T10:32:37Z"
status: draft
---

# gist to ISO/IEC 22989 mappings

`src/gist/mappings/gist-iso22989.sssom.tsv` declares the mapping set `https://w3id.org/lmodel/gist/mappings/gist-iso22989`, version 0.1.0, dated 2026-06-01 and licensed CC BY 4.0. It holds 9 rows: 5 `skos:closeMatch`, 2 `skos:narrowMatch`, 1 `skos:exactMatch` and 1 `skos:relatedMatch`, anchoring terms of the [ISO/IEC 22989 schema](../references/iso22989.md) such as Organization, AIUser and Task to gist's Organization, Person, Event, Task, Determination and KnowledgeConcept. Every row is justified `semapv:LLMBasedMatching`. The [SSSOM overlay](../services/apply-sssom-overlay.md) merges them into the [gist LinkML schema](gist-linkml-schema.md).
