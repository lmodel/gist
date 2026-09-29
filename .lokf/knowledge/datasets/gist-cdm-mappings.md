---
type: Dataset
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/datasets/gist-cdm-mappings
title: gist to Common Domain Model mappings
description: 35 manually curated SSSOM mappings from gist classes to FINOS Common Domain Model classes in the lmodel CDM schema.
resource: https://github.com/lmodel/gist/blob/main/src/gist/mappings/gist-cmd.sssom.tsv
license: https://creativecommons.org/licenses/by/4.0/
fields:
  - name: subject_id
    description: gist CURIE being mapped (subject side is always gist).
  - name: subject_label
    description: Label of the gist term.
  - name: subject_source
    description: Schema the subject comes from.
  - name: predicate_id
    description: SKOS mapping predicate (exactMatch, closeMatch, broadMatch, narrowMatch, relatedMatch).
  - name: object_id
    description: CURIE of the term in the other vocabulary.
  - name: object_label
    description: Label of the other term.
  - name: object_source
    description: Schema the object comes from.
  - name: mapping_justification
    description: semapv justification for the row.
  - name: comment
    description: Curator's note on the match.
distribution:
  - name: gist-cmd.sssom.tsv
    access_url: https://github.com/lmodel/gist/blob/main/src/gist/mappings/gist-cmd.sssom.tsv
    media_type: text/tab-separated-values
about:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
  - https://w3id.org/lmodel/gist/knowledge/references/common-domain-model
references:
  - https://w3id.org/lmodel/gist/knowledge/glossary/sssom
generated:
  by: process:ktl-librarian
  at: "2026-09-29T10:32:37Z"
status: draft
---

# gist to Common Domain Model mappings

`src/gist/mappings/gist-cmd.sssom.tsv` declares the mapping set `https://w3id.org/lmodel/gist/mappings/gist-cdm`, dated 2026-06-01 and licensed CC BY 4.0. It holds 35 rows, every one justified `semapv:ManualMappingCuration`: 24 `skos:closeMatch`, 8 `skos:relatedMatch`, 2 `skos:broadMatch` and 1 `skos:exactMatch`, from gist classes such as Organization, Person, Agreement, Magnitude and ID to classes of the [Common Domain Model schema](../references/common-domain-model.md). The [SSSOM overlay](../services/apply-sssom-overlay.md) merges them into the [gist LinkML schema](gist-linkml-schema.md).

## Open questions

- 2026-09-29, process:ktl-librarian: the file is named `gist-cmd.sssom.tsv` but its `mapping_set_id` ends `gist-cdm`, and its metadata describes the Common Domain Model (CDM). Is `cmd` a typo in the file name, and should the file be renamed to `gist-cdm.sssom.tsv`?
