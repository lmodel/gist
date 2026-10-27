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
  at: "2026-10-27T14:09:11Z"
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-16T23:47:53Z"
sources:
  - resource: tests/test_data.py
    title: the validation test, and REASONS, the failure each counter-example must give
---

# Test data

`tests/data/` holds YAML instances named `<ClassName>-<anything>.yaml`, where the part before the first hyphen must be a class of the [gist LinkML schema](gist-linkml-schema.md). Its subfolders divide the data:

- `valid/` holds data that must validate;
- `invalid/` holds counter-examples that must fail: Account-name-not-text, Organization-undeclared-slots and Person-slot-outside-domain;
- `problem/valid/` and `problem/invalid/` are for cases the current schema does not yet handle, and are empty.

In `valid/`, Account-basic, Organization-sample, Person-example and System-example give the `name` and `description` that every class carries. GeoPoint-spire, Magnitude-with-unit and UnitOfMeasure-foot also give slots that their class carries because a property's `rdfs:domain` names it.

`tests/test_data.py` (10 tests) validates each file against its class with closed classes, as `linkml-validate` does. A valid file must give no result. A counter-example must give exactly one result, and its message must contain the reason that `REASONS` in the test gives for that file. `just test` also converts the files with `linkml-run-examples` into the git-ignored `examples/output/`.
