---
type: Playbook
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/playbooks/knowledge-sources
title: Knowledge sources map
description: "The librarian's scrape map: every repository location and external URL this bundle derives concepts from, and how to re-verify each on a refresh run."
resource: https://github.com/lmodel/gist
generated:
  by: process:ktl-librarian
  at: "2026-09-29T10:32:37Z"
status: draft
---

# Knowledge sources

Bootstrap discovery ran 2026-09-29. Steady-state refresh runs re-verify these sources instead of re-discovering; update this map whenever the repository's knowledge geography changes.

| Source | Yields | Re-check by |
|--------|--------|-------------|
| `pyproject.toml`, `README.md`, `docs/about.md`, `.copier-answers.yml` | bundle metadata, `references/gist-ontology` | diff manifest name, description and authors |
| `upstream/gist14.1.0_webDownload/` | `datasets/gist-upstream-turtle`, `references/gist-ontology`, `org/semantic-arts` | re-list `ontologies/turtle/`; a new release folder means a new upstream version |
| `src/gist/schema/*.yaml` | `datasets/gist-linkml-schema` | reload each module and recount classes, slots and enum values; re-read `gist.yaml` imports |
| `src/gist/mappings/*.sssom.tsv` | the three `datasets/gist-*-mappings`, the three object-side `references/`, `glossary/sssom` | re-list the folder; recount rows, predicates and justifications per file; re-read each metadata header |
| `scripts/gist_to_linkml.py`, `scripts/apply_sssom_overlay.py`, `scripts/verify_mappings.py` | the three `services/` CLIs | re-read each docstring and `argparse` block; run `uv run python scripts/verify_mappings.py` |
| `project.justfile`, `justfile` | `playbooks/regenerate-schema`, recipe facts in the services | re-read the `gen-linkml`, `apply-sssom-overlay`, `verify-mappings`, `gen-project` and `test` recipe chains |
| `project/`, `src/gist/datamodel/`, `config.yaml` | `datasets/generated-artefacts` | re-list `project/*/`; re-read `config.yaml` excludes |
| `tests/data/`, `tests/test_*.py` | `datasets/test-data`, test counts in the concepts | re-list `tests/data/`; `uv run pytest --collect-only -q` per file |
| `tests/vendor/semanticarts/` | `datasets/semantic-arts-shapes` | re-list; compare `LICENSE.txt` with the upstream copy |
| `mkdocs.yml`, `.github/workflows/deploy-docs.yaml`, `https://lmodel.github.io/gist` | `services/documentation-site` | confirm the trigger and the `gen-doc` plus `gh-deploy` steps; fetch the site and the w3id redirect |
| `.github/workflows/pypi-publish.yaml`, `https://pypi.org/pypi/gist/json` | `playbooks/release` | re-read triggers and environment; check who owns the PyPI name |
| `.github/workflows/main.yaml` | CI facts in `services/verify-mappings` and `playbooks/regenerate-schema` | confirm it still runs only `just test` |
| `https://www.semanticarts.com/gist/`, `https://w3id.org/lmodel/{common_domain_model,dpvs,iso22989}` | the `references/` concepts | external authorities: cite on change |

Not knowledge sources (consciously excluded): `docs/elements/` and `examples/output/` (git-ignored build output), `docs/templates-linkml/` and `docs/js/` (site theming), `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` (copier-template process text), `uv.lock`, `.pre-commit-config.yaml`, `.yamllint.yaml`, `.editorconfig`, `config.public.mk` (tooling), `.github/dependabot.yml`, and the `.lokf/` sidecar itself including `.github/workflows/knowledge-*.yaml`.
