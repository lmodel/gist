# Datasets

* [gist 14.1.0 upstream Turtle release](gist-upstream-turtle.md) - The five gist 14.1.0 Turtle modules from Semantic Arts' web download, vendored as the input to the LinkML transform.
* [gist LinkML schema](gist-linkml-schema.md) - LinkML rendering of gist 14.1.0 (schema id `https://w3id.org/lmodel/gist`), generated from the upstream Turtle modules with the curated SSSOM mappings overlaid.
* [gist to Common Domain Model mappings](gist-cdm-mappings.md) - 34 manually curated SSSOM mappings from gist classes to FINOS Common Domain Model classes in the lmodel CDM schema.
* [gist to DPV mappings](gist-dpvs-mappings.md) - 11 LLM-matched SSSOM mappings from gist classes to the lmodel DPV schema.
* [gist to ISO/IEC 22989 mappings](gist-iso22989-mappings.md) - 9 LLM-matched SSSOM mappings from gist classes to the lmodel ISO/IEC 22989:2022 AI concepts and terminology schema.
* [gist generated schema artefacts](generated-artefacts.md) - The OWL, SHACL, ShEx, JSON Schema, JSON-LD, SQL, GraphQL, Protobuf, TypeScript, Excel and Python renderings that LinkML generators produce from the gist schema.
* [gist example and test data](test-data.md) - Example instance files that the test suite validates against the gist schema, sorted into valid, invalid and known-problem folders.
* [Semantic Arts gist SHACL shapes (vendored)](semantic-arts-shapes.md) - Semantic Arts' gist ontology SHACL shapes and a SPARQL CONSTRUCT query, vendored under tests/vendor/semanticarts for the SHACL test suite.
* [LOKF copy of gist_core.yaml](gist-lokf-copy.md) - `gist_core.yaml` with the five names LOKF's lokf.yaml also defines renamed (Person, Organization, name, description, license), built by `just gen-lokf-copy` and attached to every GitHub Release as `gist-linkml-lokf-<tag>.yaml`, so a LOKF domain schema can import gist beside lokf.yaml.
