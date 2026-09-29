---
type: Dataset
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/datasets/generated-artefacts
title: gist generated schema artefacts
description: The OWL, SHACL, ShEx, JSON Schema, JSON-LD, SQL, GraphQL, Protobuf, TypeScript, Excel and Python renderings that LinkML generators produce from the gist schema.
resource: https://github.com/lmodel/gist/tree/main/project
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
  - name: sqlschema
    access_url: https://github.com/lmodel/gist/blob/main/project/sqlschema/gist.sql
    media_type: application/sql
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
  at: "2026-09-29T10:32:37Z"
status: draft
---

# Generated artefacts

`just gen-project` runs LinkML's `gen-project` over `src/gist/schema/gist.yaml` with the generator settings in `config.yaml` (every generator except markdown, most with `mergeimports: true`), writes the results under `project/`, moves the Python dataclasses into `src/gist/datamodel/gist.py` and writes a Pydantic model beside it as `gist_pydantic.py`. All of these are committed. None is edited by hand: regenerate them from the [gist LinkML schema](gist-linkml-schema.md) instead ([Regenerate the schema](../playbooks/regenerate-schema.md)). `tests/test_generated_artifacts.py` (14 tests) checks the JSON Schema, OWL and related outputs.
