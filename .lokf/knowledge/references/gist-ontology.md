---
type: Reference
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/references/gist-ontology
title: gist upper ontology (Semantic Arts)
description: Semantic Arts' minimalist upper ontology for enterprise knowledge graphs; release 14.1.0 is the upstream authority this repository transforms into LinkML.
resource: https://www.semanticarts.com/gist/
version: "14.1.0"
license: https://creativecommons.org/licenses/by/4.0/
source:
  - https://w3id.org/lmodel/gist/knowledge/org/semantic-arts
sources:
  - resource: https://www.semanticarts.com/gist/
  - resource: https://github.com/lmodel/gist/blob/main/upstream/gist14.1.0_webDownload/LICENSE.txt
  - resource: https://github.com/semanticarts/gist/blob/v14.1.0/README.md
    title: gist README, release 14.1.0 (license and namespace conditions)
generated:
  by: process:ktl-librarian
  at: "2026-09-29T11:22:44Z"
status: draft
---

# gist

gist is a minimalist upper ontology created by [Semantic Arts](../org/semantic-arts.md) for enterprise knowledge graph applications. The release this repository encodes is 14.1.0, whose Core module has the version IRI `https://w3id.org/semanticarts/ontology/gistCore14.1.0`; `https://w3id.org/semanticarts/ontology/gistCore` redirects to `https://ontologies.semanticarts.com/ontology/gistCore.ttl`.

The release ships five Turtle modules (Core, MediaTypes, PrefixDeclarations, RdfsAnnotations, SubClassAssertions), vendored here as the [upstream Turtle release](../datasets/gist-upstream-turtle.md) and rendered as the [gist LinkML schema](../datasets/gist-linkml-schema.md). Upstream terms live in `https://w3id.org/semanticarts/ns/ontology/gist/`, which the LinkML schema binds to the prefix `gist` as Semantic Arts does; named individuals live in `https://w3id.org/semanticarts/ns/data/gist/` (`gistd`). Semantic Arts asks that terms used from gist stay in that namespace and that nobody else defines terms in it; the [gist namespace policy](../policies/gist-namespace-policy.md) records how this repository holds to both.
