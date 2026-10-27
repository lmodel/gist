---
type: Playbook
genre: how-to
id: https://w3id.org/lmodel/gist/knowledge/playbooks/regenerate-schema
title: Regenerate the schema and its artefacts
description: How to rebuild the gist LinkML schema, its mappings and every generated artefact from the upstream Turtle release, and check the result.
resource: project.justfile
references:
  - https://w3id.org/lmodel/gist/knowledge/services/gist-to-linkml
  - https://w3id.org/lmodel/gist/knowledge/services/apply-sssom-overlay
  - https://w3id.org/lmodel/gist/knowledge/services/verify-mappings
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
  - https://w3id.org/lmodel/gist/knowledge/datasets/generated-artefacts
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-lokf-copy
generated:
  by: process:ktl-librarian
  at: "2026-10-27T14:09:11Z"
status: draft
sources:
  - resource: tests
    title: the test suite, which uv run pytest --collect-only -q counts
  - resource: scripts/check_generated_current.py
    title: just verify-generated
---

# Regenerate the schema and its artefacts

1. Run `just install` once (`uv sync --group dev`).
2. Change the input, never the output: edit a mapping TSV under `src/gist/mappings/`, the [transform script](../services/gist-to-linkml.md), or replace the Turtle files under `upstream/` with a newer gist release. `just check-upstream` says whether one exists, and `upstream-watch.yaml` opens an issue when it does.
3. Run `just gen-project`. It runs, in order, `gen-linkml` (Turtle to LinkML), `apply-sssom-overlay` ([overlay](../services/apply-sssom-overlay.md)), `verify-mappings` ([verifier](../services/verify-mappings.md)), then LinkML's `gen-project` and `gen-pydantic` ([generated artefacts](../datasets/generated-artefacts.md)).
4. Run `just test`: it re-runs the generators into `tmp/`, regenerates the Python model, runs pytest (342 tests), and converts the test data.
5. Commit the regenerated `src/gist/schema/`, `src/gist/datamodel/` and `project/` together with the change that caused them.

CI regenerates `src/gist/schema/` the same way and fails a pull request whose committed schema differs, so skipping step 3 fails there. It also fails when `project/` or `src/gist/datamodel/` is out of date: `just verify-generated` compares them by content, since they embed their generation date and their Turtle comes out in a new triple order on each run. CI also runs `just gen-lokf-copy`, which fails when the [LOKF copy](../datasets/gist-lokf-copy.md) shares an element name with LOKF's `lokf.yaml`.
