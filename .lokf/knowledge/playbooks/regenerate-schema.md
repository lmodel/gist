---
type: Playbook
genre: how-to
id: https://w3id.org/lmodel/gist/knowledge/playbooks/regenerate-schema
title: Regenerate the schema and its artefacts
description: How to rebuild the gist LinkML schema, its mappings and every generated artefact from the upstream Turtle release, and check the result.
resource: https://github.com/lmodel/gist/blob/main/project.justfile
references:
  - https://w3id.org/lmodel/gist/knowledge/services/gist-to-linkml
  - https://w3id.org/lmodel/gist/knowledge/services/apply-sssom-overlay
  - https://w3id.org/lmodel/gist/knowledge/services/verify-mappings
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
  - https://w3id.org/lmodel/gist/knowledge/datasets/generated-artefacts
generated:
  by: process:ktl-librarian
  at: "2026-09-29T12:29:55Z"
status: draft
---

# Regenerate the schema and its artefacts

1. Run `just install` once (`uv sync --group dev`).
2. Change the input, never the output: edit a mapping TSV under `src/gist/mappings/`, the [transform script](../services/gist-to-linkml.md), or replace the Turtle files under `upstream/` with a newer gist release. `just check-upstream` says whether one exists, and `upstream-watch.yaml` opens an issue when it does.
3. Run `just gen-project`. It runs, in order, `gen-linkml` (Turtle to LinkML), `apply-sssom-overlay` ([overlay](../services/apply-sssom-overlay.md)), `verify-mappings` ([verifier](../services/verify-mappings.md)), then LinkML's `gen-project` and `gen-pydantic` ([generated artefacts](../datasets/generated-artefacts.md)).
4. Run `just test`: it re-runs the generators into `tmp/`, regenerates the Python model, runs pytest (283 tests), and converts the test data.
5. Run `just testdoc` to preview the documentation site, then commit the regenerated `src/gist/schema/`, `src/gist/datamodel/` and `project/` together with the change that caused them.

CI regenerates `src/gist/schema/` the same way and fails a pull request whose committed schema differs, so skipping step 3 fails there. It also fails when `project/` or `src/gist/datamodel/` is out of date: `just verify-generated` compares them by content, since they embed their generation date and their Turtle comes out in a new triple order on each run.
