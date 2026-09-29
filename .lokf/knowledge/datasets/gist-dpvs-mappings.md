---
type: Dataset
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/datasets/gist-dpvs-mappings
title: gist to DPV mappings
description: 11 LLM-matched SSSOM mappings from gist classes to the lmodel DPV schema.
resource: https://github.com/lmodel/gist/blob/main/src/gist/mappings/gist-dpv.sssom.tsv
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
    description: Note on the match.
distribution:
  - name: gist-dpv.sssom.tsv
    access_url: https://github.com/lmodel/gist/blob/main/src/gist/mappings/gist-dpv.sssom.tsv
    media_type: text/tab-separated-values
about:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
  - https://w3id.org/lmodel/gist/knowledge/references/dpvs
references:
  - https://w3id.org/lmodel/gist/knowledge/glossary/sssom
generated:
  by: process:ktl-librarian
  at: "2026-09-29T10:32:37Z"
status: draft
---

# gist to DPV mappings

`src/gist/mappings/gist-dpv.sssom.tsv` declares the mapping set `https://w3id.org/lmodel/gist/mappings/gist-dpv`, version 1.1, dated 2026-09-29 and licensed CC BY 4.0. It holds 11 rows: 4 `skos:narrowMatch`, 3 `skos:relatedMatch`, 2 `skos:broadMatch` and 2 `skos:exactMatch`, from gist classes such as Agreement, Contract, Organization, Person and GeoLocation to terms of the [DPV schema](../references/dpvs.md). Every row is justified `semapv:LLMBasedMatching`, so a reviewer should treat each row as a machine suggestion until a person has checked it. The [SSSOM overlay](../services/apply-sssom-overlay.md) merges them into the [gist LinkML schema](gist-linkml-schema.md).
