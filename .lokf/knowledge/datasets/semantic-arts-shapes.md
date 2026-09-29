---
type: Dataset
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/datasets/semantic-arts-shapes
title: Semantic Arts gist SHACL shapes (vendored)
description: Semantic Arts' gist ontology SHACL shapes and a SPARQL CONSTRUCT query, vendored under tests/vendor/semanticarts for the SHACL test suite.
resource: https://github.com/lmodel/gist/tree/main/tests/vendor/semanticarts
license: https://creativecommons.org/licenses/by/4.0/
distribution:
  - name: ontologyShapes.ttl
    access_url: https://github.com/lmodel/gist/blob/main/tests/vendor/semanticarts/ontologyShapes.ttl
    media_type: text/turtle
  - name: property_type_construct.rq
    access_url: https://github.com/lmodel/gist/blob/main/tests/vendor/semanticarts/property_type_construct.rq
    media_type: application/sparql-query
source:
  - https://w3id.org/lmodel/gist/knowledge/org/semantic-arts
about:
  - https://w3id.org/lmodel/gist/knowledge/references/gist-ontology
generated:
  by: process:ktl-librarian
  at: "2026-09-29T10:32:37Z"
status: draft
---

# Semantic Arts SHACL shapes

`tests/vendor/semanticarts/ontologyShapes.ttl` declares shapes in Semantic Arts' `https://shapes.semanticarts.com/gist/` namespace over the upstream [gist ontology](../references/gist-ontology.md) terms, and `property_type_construct.rq` is a SPARQL CONSTRUCT that builds an `sh:ValidationReport`. The folder's `LICENSE.txt` is byte-identical to the upstream release's CC BY 4.0 text. `tests/test_shacl_validation.py` (18 tests) uses both.
