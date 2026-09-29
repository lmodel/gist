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
  - name: subject_type
    description: SSSOM entity type of the subject, here owl class.
  - name: predicate_id
    description: SKOS mapping predicate (exactMatch, closeMatch, broadMatch, narrowMatch, relatedMatch).
  - name: predicate_label
    description: Human-readable predicate name.
  - name: object_id
    description: CURIE of the term in the other vocabulary.
  - name: object_label
    description: Label of the other term.
  - name: object_type
    description: SSSOM entity type of the object, here owl class.
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

`src/gist/mappings/gist-iso22989.sssom.tsv` declares the mapping set `https://w3id.org/lmodel/gist/mappings/gist-iso22989`, version 0.2.0, dated 2026-09-29 and licensed CC BY 4.0. It holds 9 rows: 4 `skos:narrowMatch`, 4 `skos:relatedMatch` and 1 `skos:closeMatch`, relating gist's Organization, Person, Event, Task, Determination and KnowledgeConcept to terms of the [ISO/IEC 22989 schema](../references/iso22989.md) such as Organization, AIUser and Task. Every row is justified `semapv:LLMBasedMatching`. The [SSSOM overlay](../services/apply-sssom-overlay.md) merges them into the [gist LinkML schema](gist-linkml-schema.md).
