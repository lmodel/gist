---
type: Service
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/services/verify-mappings
title: Mapping verifier
description: Read-only command-line check (scripts/verify_mappings.py, run as just verify-mappings) that every SSSOM row is present on the gist LinkML schema and nothing extra is.
resource: https://github.com/lmodel/gist/blob/main/scripts/verify_mappings.py
tags:
  - cli
dependsOn:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-cdm-mappings
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-dpvs-mappings
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-iso22989-mappings
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
generated:
  by: process:ktl-librarian
  at: "2026-09-29T12:29:55Z"
status: draft
---

# Mapping verifier

`just verify-mappings` runs after the [SSSOM overlay](apply-sssom-overlay.md) and reads, never writes. It loads every `*.sssom.tsv` under `src/gist/mappings/` and every schema under `src/gist/schema/`, and exits non-zero with a diff when a row is missing from the schema or a schema mapping has no row. It matches each subject to schema elements by IRI, by the same rule as the overlay, so a TSV whose `curie_map` binds `gist:` differently from the schema reports its rows as naming no element. `skos:broader`, `skos:narrower`, `rdf:type` and `owl:equivalentClass` rows are skipped, as the overlay skips them. On 2026-09-29 it reported `rows=54 missing=0 extra=0 unknown=0`. It cannot see whether an object term exists in its target schema; `just verify-mapping-targets` checks that against pinned commits.

It runs inside `just gen-project` (its recipe chain is `gen-linkml`, `apply-sssom-overlay`, `verify-mappings`, then `gen-project`), and in CI: `.github/workflows/main.yaml` runs `just verify-mappings` on its Python 3.14 leg and then fails if `src/gist/schema/` differs from the committed copy, so a pull request that edits a mapping TSV or a schema module without regenerating is caught.
