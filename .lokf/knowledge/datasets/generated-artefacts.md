---
type: Dataset
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/datasets/generated-artefacts
title: gist generated schema artefacts
description: The OWL, SHACL, ShEx, JSON Schema, JSON-LD, GraphQL, Protobuf, TypeScript, Excel and Python renderings that LinkML generators produce from the gist schema.
resource: project
distribution:
  - name: excel
    access_url: https://github.com/lmodel/gist/blob/main/project/excel/gist.xlsx
    media_type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
  - name: graphql
    access_url: https://github.com/lmodel/gist/blob/main/project/graphql/gist.graphql
  - name: jsonld
    access_url: https://github.com/lmodel/gist/blob/main/project/jsonld/gist.context.jsonld
    media_type: application/ld+json
  - name: jsonld
    access_url: https://github.com/lmodel/gist/blob/main/project/jsonld/gist.jsonld
    media_type: application/ld+json
  - name: jsonschema
    access_url: https://github.com/lmodel/gist/blob/main/project/jsonschema/gist.schema.json
    media_type: application/schema+json
  - name: owl
    access_url: https://github.com/lmodel/gist/blob/main/project/owl/gist.owl.ttl
    media_type: text/turtle
  - name: prefixmap
    access_url: https://github.com/lmodel/gist/blob/main/project/prefixmap/gist.yaml
    media_type: application/yaml
  - name: protobuf
    access_url: https://github.com/lmodel/gist/blob/main/project/protobuf/gist.proto
  - name: shacl
    access_url: https://github.com/lmodel/gist/blob/main/project/shacl/gist.shacl.ttl
    media_type: text/turtle
  - name: shex
    access_url: https://github.com/lmodel/gist/blob/main/project/shex/gist.shex
    media_type: text/shex
  - name: typescript
    access_url: https://github.com/lmodel/gist/blob/main/project/typescript/gist.ts
  - name: python (gist.py)
    access_url: https://github.com/lmodel/gist/blob/main/src/gist/datamodel/gist.py
    media_type: text/x-python
  - name: python (gist_pydantic.py)
    access_url: https://github.com/lmodel/gist/blob/main/src/gist/datamodel/gist_pydantic.py
    media_type: text/x-python
derivedFrom:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
generated:
  by: process:ktl-librarian
  at: "2026-10-27T14:09:11Z"
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-16T23:47:53Z"
sources:
  - resource: .linkml/generators.yaml
    title: gen-project's settings, named by LINKML_GENERATORS_CONFIG_YAML in config.public.mk
  - resource: config.public.mk
    title: LINKML_GENERATORS_OWL_ARGS, the flags of the published OWL
  - resource: src/gist/datamodel
    title: the Python datamodel, gist.py and gist_pydantic.py
  - resource: scripts/check_generated_current.py
    title: just verify-generated, the check that the committed artefacts are current
  - resource: tests/test_generated_artifacts.py
    title: the tests of the committed artefacts
---

# Generated artefacts

`just gen-project` runs LinkML's `gen-project` over `src/gist/schema/gist.yaml` with the generator settings in `.linkml/generators.yaml`, and writes the results under `project/`. Most generators take `mergeimports: true`, and the JSON Schema takes each element's gist label as its title. The settings leave out two generators:

- the SQL DDL, which would hold some 5,400 tables, one for each multivalued slot of each class, because every class carries the 89 slots gist declares without a domain;
- Java, because the recipe runs `gen-java` separately afterwards, into the git-ignored `project/java/`, so `gen-project` would write that folder twice.

The recipe moves the Python dataclasses into `src/gist/datamodel/gist.py` and writes a Pydantic model beside it as `gist_pydantic.py`. It then rewrites `project/owl/gist.owl.ttl` with a separate `gen-owl` call whose flags come from `LINKML_GENERATORS_OWL_ARGS` in `config.public.mk`, so those flags, not `.linkml/generators.yaml`, shape the published OWL. Three of those flags leave out the restrictions that only repeat a property's range or a minimum of none.

`gen-project` and the separate `gen-owl` call both keep gist's own IRIs for gist's terms. The SHACL shapes are this project's, and their IRIs are in `gist_linkml:` (`gist_linkml:PersonShape` targets `gist:Person`).

Each class's definition repeats every slot it inherits, so the JSON Schema, the Pydantic module and the SHACL shapes are about 5 MB, 7 MB and 2.4 MB.

All of these files are committed, and none is edited by hand: regenerate them from the [gist LinkML schema](gist-linkml-schema.md) instead ([Regenerate the schema](../playbooks/regenerate-schema.md)). CI runs `just verify-generated`, which regenerates them and fails when a committed file differs in content.

`tests/test_generated_artifacts.py` (22 tests) checks the JSON Schema, OWL and related outputs. Four of its tests check the committed OWL and SHACL against the [gist namespace policy](../policies/gist-namespace-policy.md). Four more check that the OWL's property types, datatype ranges and deprecations, and the datatypes the SHACL shapes accept, match gist's.
