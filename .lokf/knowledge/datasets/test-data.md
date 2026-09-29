---
type: Dataset
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/datasets/test-data
title: gist example and test data
description: Example instance files that the test suite validates against the gist schema, sorted into valid, invalid and known-problem folders.
resource: https://github.com/lmodel/gist/tree/main/tests/data
about:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
generated:
  by: process:ktl-librarian
  at: "2026-09-29T10:32:37Z"
status: draft
---

# Test data

`tests/data/` holds YAML instances named `<ClassName>-<anything>.yaml`, where the part before the first hyphen must be a class of the [gist LinkML schema](gist-linkml-schema.md). `valid/` holds data that must validate (Account-basic, Organization-sample, Person-example, System-example); `invalid/` holds data that must fail (Account-invalid-id-type, Organization-minimal, Person-invalid-aspect); `problem/valid/` and `problem/invalid/` are for cases the current schema does not yet handle and are empty. `tests/test_data.py` (11 tests) validates them, and `just test` also converts them with `linkml-run-examples` into the git-ignored `examples/output/`.
