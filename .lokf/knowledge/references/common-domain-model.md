---
type: Reference
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/references/common-domain-model
title: Common Domain Model LinkML schema (lmodel)
description: The lmodel LinkML rendering of the FINOS Common Domain Model, the object side of the gist-to-CDM mapping set.
resource: https://w3id.org/lmodel/common-domain-model
generated:
  by: process:ktl-librarian
  at: "2026-10-17T00:13:57Z"
status: draft
sources:
- resource: src/gist/mappings/gist-cdm.sssom.tsv
  title: the mapping set's metadata header
---

# Common Domain Model (lmodel)

This is the `object_source` of the [gist to CDM mappings](../datasets/gist-cdm-mappings.md), whose metadata describes its objects as "classes of the FINOS Common Domain Model (CDM), as rendered in LinkML by lmodel/common-domain-model", and binds the prefix `common_domain_model:` to `https://w3id.org/lmodel/common-domain-model/`, the namespace the schemas of `lmodel/common-domain-model` declare. The w3id identifier redirects to `https://lmodel.github.io/common-domain-model`. This repository holds no copy of it. The mappings name its classes by CURIE only, and `just verify-mapping-targets` fetches its schema folder at a pinned commit to check that every mapped class exists.
