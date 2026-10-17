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

* [gist 14.1.0 upstream Turtle release](datasets/gist-upstream-turtle.md) - The five gist 14.1.0 Turtle modules from Semantic Arts' web download, vendored as the input to the LinkML transform.
* [gist LinkML schema](datasets/gist-linkml-schema.md) - LinkML rendering of gist 14.1.0 (schema id `https://w3id.org/lmodel/gist`), generated from the upstream Turtle modules with the curated SSSOM mappings overlaid.
* [gist to Common Domain Model mappings](datasets/gist-cdm-mappings.md) - 34 manually curated SSSOM mappings from gist classes to FINOS Common Domain Model classes in the lmodel CDM schema.
* [gist to DPV mappings](datasets/gist-dpvs-mappings.md) - 11 LLM-matched SSSOM mappings from gist classes to the lmodel DPV schema.
* [gist to ISO/IEC 22989 mappings](datasets/gist-iso22989-mappings.md) - 9 LLM-matched SSSOM mappings from gist classes to the lmodel ISO/IEC 22989:2022 AI concepts and terminology schema.
* [gist generated schema artefacts](datasets/generated-artefacts.md) - The OWL, SHACL, ShEx, JSON Schema, JSON-LD, SQL, GraphQL, Protobuf, TypeScript, Excel and Python renderings that LinkML generators produce from the gist schema.
* [gist example and test data](datasets/test-data.md) - Example instance files that the test suite validates against the gist schema, sorted into valid, invalid and known-problem folders.
* [Semantic Arts gist SHACL shapes (vendored)](datasets/semantic-arts-shapes.md) - Semantic Arts' gist ontology SHACL shapes and a SPARQL CONSTRUCT query, vendored under tests/vendor/semanticarts for the SHACL test suite.
* [LOKF copy of gist_core.yaml](datasets/gist-lokf-copy.md) - `gist_core.yaml` with the five names LOKF's lokf.yaml also defines renamed (Person, Organization, name, description, license), built by `just gen-lokf-copy` and attached to every GitHub Release as `gist-linkml-lokf-<tag>.yaml`, so a LOKF domain schema can import gist beside lokf.yaml.

# Services

* [gist-to-LinkML transform](services/gist-to-linkml.md) - Command-line script (scripts/gist_to_linkml.py, run as just gen-linkml) that turns the gist Turtle modules into the gist LinkML schema modules, keeping each term's gist IRI.
* [SSSOM overlay](services/apply-sssom-overlay.md) - Command-line script (scripts/apply_sssom_overlay.py, run as just apply-sssom-overlay) that merges the curated SSSOM mappings into the gist LinkML schema.
* [Mapping verifier](services/verify-mappings.md) - Read-only command-line check (scripts/verify_mappings.py, run as just verify-mappings) that every SSSOM row is present on the gist LinkML schema and nothing extra is.
* [gist documentation site](services/documentation-site.md) - The MkDocs site at `https://lmodel.github.io/gist`, generated from the gist schema and deployed to GitHub Pages on every push to main.
* [Upstream watch](services/upstream-watch.md) - Weekly GitHub workflow (upstream-watch.yaml) that checks the vendored gist release is Semantic Arts' latest and intact, and that mapped target terms still exist on each target's default branch, opening an issue on failure.
* [Mapping target checker](services/verify-mapping-targets.md) - Network command-line check (scripts/verify_mapping_targets.py, run as just verify-mapping-targets) that every SSSOM object term exists in the lmodel target schema it names, at a pinned commit.

# References

* [gist upper ontology (Semantic Arts)](references/gist-ontology.md) - Semantic Arts' minimalist upper ontology for enterprise knowledge graphs; release 14.1.0 is the upstream authority this repository transforms into LinkML.
* [Common Domain Model LinkML schema (lmodel)](references/common-domain-model.md) - The lmodel LinkML rendering of the FINOS Common Domain Model, the object side of the gist-to-CDM mapping set.
* [DPV LinkML schema (lmodel)](references/dpvs.md) - The lmodel LinkML rendering of the Data Privacy Vocabulary (DPV), the object side of the gist-to-DPV mapping set.
* [ISO/IEC 22989:2022 LinkML schema (lmodel)](references/iso22989.md) - The lmodel LinkML schema for ISO/IEC 22989:2022 (Artificial intelligence concepts and terminology), the object side of the gist-to-ISO/IEC 22989 mapping set.

# Policies

* [gist namespace policy](policies/gist-namespace-policy.md) - gist's terms keep Semantic Arts' IRIs and this project defines nothing in Semantic Arts' namespace; what the LinkML rendering adds lives under gist_linkml (`https://w3id.org/lmodel/gist/`).

# Playbooks

* [Regenerate the schema and its artefacts](playbooks/regenerate-schema.md) - How to rebuild the gist LinkML schema, its mappings and every generated artefact from the upstream Turtle release, and check the result.
* [Release the gist Python package](playbooks/release.md) - How a releasing merge to main becomes a tagged GitHub Release through semantic-release, with the LOKF copy of gist_core.yaml attached, and is uploaded to PyPI as gist-linkml.
* [Knowledge sources map](playbooks/knowledge-sources.md) - The librarian's scrape map: every repository location and external URL this bundle derives concepts from, and how to re-verify each on a refresh run.

# Glossary

* [SSSOM](glossary/sssom.md) - Simple Standard for Sharing Ontological Mappings: the tab-separated format with a YAML metadata header in which this repository keeps its cross-vocabulary mappings.

# Organizations

* [Semantic Arts](org/semantic-arts.md) - Publisher of the gist upper ontology and of the gist SHACL shapes this repository vendors for its tests.
