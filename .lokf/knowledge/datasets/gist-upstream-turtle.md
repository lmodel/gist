---
type: Dataset
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/datasets/gist-upstream-turtle
title: gist 14.1.0 upstream Turtle release
description: The five gist 14.1.0 Turtle modules from Semantic Arts' web download, vendored as the input to the LinkML transform.
resource: https://github.com/lmodel/gist/tree/main/upstream/gist14.1.0_webDownload/ontologies/turtle
version: "14.1.0"
license: https://creativecommons.org/licenses/by/4.0/
distribution:
  - name: gistCore14.1.0.ttl
    access_url: https://github.com/lmodel/gist/blob/main/upstream/gist14.1.0_webDownload/ontologies/turtle/gistCore14.1.0.ttl
    media_type: text/turtle
  - name: gistMediaTypes14.1.0.ttl
    access_url: https://github.com/lmodel/gist/blob/main/upstream/gist14.1.0_webDownload/ontologies/turtle/gistMediaTypes14.1.0.ttl
    media_type: text/turtle
  - name: gistPrefixDeclarations14.1.0.ttl
    access_url: https://github.com/lmodel/gist/blob/main/upstream/gist14.1.0_webDownload/ontologies/turtle/gistPrefixDeclarations14.1.0.ttl
    media_type: text/turtle
  - name: gistRdfsAnnotations14.1.0.ttl
    access_url: https://github.com/lmodel/gist/blob/main/upstream/gist14.1.0_webDownload/ontologies/turtle/gistRdfsAnnotations14.1.0.ttl
    media_type: text/turtle
  - name: gistSubClassAssertions14.1.0.ttl
    access_url: https://github.com/lmodel/gist/blob/main/upstream/gist14.1.0_webDownload/ontologies/turtle/gistSubClassAssertions14.1.0.ttl
    media_type: text/turtle
derivedFrom:
  - https://w3id.org/lmodel/gist/knowledge/references/gist-ontology
generated:
  by: process:ktl-librarian
  at: "2026-09-29T10:32:37Z"
status: draft
---

# Upstream Turtle release

`upstream/gist14.1.0_webDownload/` holds Semantic Arts' gist 14.1.0 web download: the five Turtle modules under `ontologies/turtle/` and the CC BY 4.0 `LICENSE.txt`. They are the input the [gist-to-LinkML transform](../services/gist-to-linkml.md) reads (`just gen-linkml`), and nothing in the build writes to them. Replacing them with a newer gist release is how the [LinkML schema](gist-linkml-schema.md) moves to a new upstream version.
