---
type: Dataset
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/datasets/test-data
title: gist example and test data
description: Example instance files that the test suite validates against the gist schema, sorted into valid, invalid and known-problem folders.
resource: tests/data
about:
- https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
generated:
  by: process:ktl-librarian
  at: "2026-10-17T00:13:57Z"
status: draft
verified:
- by: process:ktl-librarian
  at: "2026-10-16T23:47:53Z"
---

# Test data

`tests/data/` holds YAML instances named `<ClassName>-<anything>.yaml`, where the part before the first hyphen must be a class of the [gist LinkML schema](gist-linkml-schema.md). Its subfolders divide the data:

- `valid/` holds data that must validate (Account-basic, Organization-sample, Person-example, System-example);
- `invalid/` holds data that must fail (Account-invalid-id-type, Organization-minimal, Person-invalid-aspect);
- `problem/valid/` and `problem/invalid/` are for cases the current schema does not yet handle, and are empty.

`tests/test_data.py` (11 tests) validates them, and `just test` also converts them with `linkml-run-examples` into the git-ignored `examples/output/`.
