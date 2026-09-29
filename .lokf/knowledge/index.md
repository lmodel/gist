---
lokf_version: "0.2"
okf_version: "0.2"
base_iri: https://w3id.org/lmodel/gist/knowledge/
context: https://w3id.org/lokf/context.jsonld
title: gist Knowledge Bundle
description: GIST (Semantic Arts, Upper Enterprise Ontology) - LinkML Schema
license: https://creativecommons.org/licenses/by/4.0/
publisher:
  type: Person
  id: https://w3id.org/lmodel/gist/knowledge/person/noel-mcloughlin
  name: Noel McLoughlin
---

# gist Knowledge Bundle

A [LOKF](https://lokf.nolan-nichols.com) knowledge base for gist. Every Markdown file under `knowledge/` is one concept; together they form a queryable knowledge graph, derived from this repository's code and docs.

# Datasets

* [gist 14.1.0 upstream Turtle release](datasets/gist-upstream-turtle.md) - the five Semantic Arts Turtle modules the build starts from.
* [gist LinkML schema](datasets/gist-linkml-schema.md) - the six generated LinkML modules under `src/gist/schema/`.
* [gist to Common Domain Model mappings](datasets/gist-cdm-mappings.md) - 34 manually curated SSSOM rows.
* [gist to DPV mappings](datasets/gist-dpvs-mappings.md) - 11 LLM-matched SSSOM rows.
* [gist to ISO/IEC 22989 mappings](datasets/gist-iso22989-mappings.md) - 9 LLM-matched SSSOM rows.
* [gist generated schema artefacts](datasets/generated-artefacts.md) - OWL, SHACL, JSON Schema and the other LinkML generator outputs.
* [gist example and test data](datasets/test-data.md) - valid, invalid and known-problem instances.
* [Semantic Arts gist SHACL shapes (vendored)](datasets/semantic-arts-shapes.md) - shapes and a CONSTRUCT query used by the SHACL tests.

# Services

* [gist-to-LinkML transform](services/gist-to-linkml.md) - `just gen-linkml`, Turtle to LinkML.
* [SSSOM overlay](services/apply-sssom-overlay.md) - `just apply-sssom-overlay`, mappings into the schema.
* [Mapping verifier](services/verify-mappings.md) - `just verify-mappings`, read-only check of the overlay.
* [gist documentation site](services/documentation-site.md) - <https://lmodel.github.io/gist>, deployed from `main`.

# References

* [gist upper ontology (Semantic Arts)](references/gist-ontology.md) - the upstream authority, release 14.1.0.
* [Common Domain Model LinkML schema (lmodel)](references/common-domain-model.md) - object side of the CDM mappings.
* [DPV LinkML schema (lmodel)](references/dpvs.md) - object side of the DPV mappings.
* [ISO/IEC 22989:2022 LinkML schema (lmodel)](references/iso22989.md) - object side of the ISO/IEC 22989 mappings.

# Policies

* [gist namespace policy](policies/gist-namespace-policy.md) - gist's terms keep Semantic Arts' IRIs; this project's additions live under `gist_linkml`.

# Playbooks

* [Regenerate the schema and its artefacts](playbooks/regenerate-schema.md) - the `just gen-project` pipeline and checks.
* [Release the gist Python package](playbooks/release.md) - releasing merge to tagged release to PyPI, via semantic-release.
* [Knowledge sources map](playbooks/knowledge-sources.md) - where every concept here comes from and how to re-check it.

# Glossary

* [SSSOM](glossary/sssom.md) - the mapping file format.

# Organizations

* [Semantic Arts](org/semantic-arts.md) - publisher of gist.
