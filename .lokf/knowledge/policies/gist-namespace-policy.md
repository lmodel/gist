---
type: Policy
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/policies/gist-namespace-policy
title: gist namespace policy
description: gist's terms keep Semantic Arts' IRIs and this project defines nothing in Semantic Arts' namespace; what the LinkML rendering adds lives under gist_linkml (https://w3id.org/lmodel/gist/).
resource: https://github.com/lmodel/gist/blob/main/README.md
source:
  - https://w3id.org/lmodel/gist/knowledge/org/semantic-arts
about:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
  - https://w3id.org/lmodel/gist/knowledge/datasets/generated-artefacts
references:
  - https://w3id.org/lmodel/gist/knowledge/references/gist-ontology
  - https://w3id.org/lmodel/gist/knowledge/services/gist-to-linkml
sources:
  - resource: https://github.com/semanticarts/gist/blob/v14.1.0/README.md
    title: gist README, release 14.1.0 (license and namespace conditions)
  - resource: https://github.com/lmodel/gist/blob/main/README.md
    title: This repository's README, License and attribution
generated:
  by: process:ktl-librarian
  at: "2026-09-29T11:23:18Z"
status: draft
---

# gist namespace policy

Semantic Arts publishes [gist](../references/gist-ontology.md) under CC BY 4.0 and adds two conditions: "any terms used from gist remain in the gist namespace", and "you do not define your own terms in the gist namespace" (gist README, release 14.1.0). This repository holds to both.

| Prefix | Namespace | Holds |
| --- | --- | --- |
| `gist` | `https://w3id.org/semanticarts/ns/ontology/gist/` | gist's classes and properties, under their own IRIs |
| `gistd` | `https://w3id.org/semanticarts/ns/data/gist/` | gist's named individuals |
| `gist_linkml` | `https://w3id.org/lmodel/gist/` | what the LinkML rendering adds: the schema documents, the `GistThing` mixin, the enums, the subsets, the SHACL shapes, and the LinkML element definitions that the OWL links to gist's classes with `skos:exactMatch` |

Three mechanisms hold it:

1. **Converter.** `scripts/gist_to_linkml.py` binds `gist` to Semantic Arts' namespace, writes `class_uri` and `slot_uri` as `gist:` CURIEs, and sets every module's `default_prefix` to `gist_linkml`, so an element without its own IRI lands in lmodel's namespace ([transform](../services/gist-to-linkml.md)).
2. **Generator flags.** The published OWL comes from a separate `gen-owl` call that takes `LINKML_GENERATORS_OWL_ARGS` from `config.public.mk` (`--no-use-native-uris --default-permissible-value-type owl:NamedIndividual`). `config.yaml` gives `gen-project` the same OWL settings, and gives `gen-shacl` `use_class_uri_names: false` with the suffix `Shape` ([generated artefacts](../datasets/generated-artefacts.md)).
3. **Tests.** `TestGistNamespace` in `tests/test_schema_validation.py` and `TestGistIrisInArtifacts` in `tests/test_generated_artifacts.py` check the schema modules and the committed OWL and SHACL against the vendored release, and run in CI through `just test`.
