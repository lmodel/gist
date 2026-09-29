---
type: Playbook
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/playbooks/knowledge-sources
title: Knowledge sources map
description: "The librarian's scrape map: every repository location and external URL this bundle derives concepts from, and how to re-verify each on a refresh run."
resource: https://github.com/lmodel/gist
generated:
  by: process:ktl-librarian
  at: "2026-09-29T21:02:46Z"
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
| `scripts/gist_to_linkml.py`, `scripts/apply_sssom_overlay.py`, `scripts/verify_mappings.py`, `scripts/verify_mapping_targets.py` | the four `services/` CLIs | re-read each docstring and `argparse` block; run `uv run python scripts/verify_mappings.py` |
| `project.justfile`, `justfile` | `playbooks/regenerate-schema`, recipe facts in the services | re-read the `gen-linkml`, `apply-sssom-overlay`, `verify-mappings`, `gen-project` and `test` recipe chains |
| `project/`, `src/gist/datamodel/`, `config.yaml` | `datasets/generated-artefacts` | re-list `project/*/`; re-read `config.yaml` excludes |
| `tests/data/`, `tests/test_*.py` | `datasets/test-data`, test counts in the concepts | re-list `tests/data/`; `uv run pytest --collect-only -q` per file |
| `tests/vendor/semanticarts/` | `datasets/semantic-arts-shapes` | re-list; compare `LICENSE.txt` with the upstream copy |
| `mkdocs.yml`, `.github/workflows/deploy-docs.yaml`, `https://lmodel.github.io/gist` | `services/documentation-site` | confirm the trigger and the `gen-doc` plus `gh-deploy` steps; fetch the site and the w3id redirect |
| `.github/workflows/semantic-release.yml`, `.releaserc.json`, `.github/workflows/pypi-publish.yaml`, `pyproject.toml`, `CONTRIBUTING.md` (Releasing), `https://pypi.org/pypi/gist-linkml/json` | `playbooks/release` | re-read the release guards, the dispatch, the triggers, environments and distribution name; check whether the PyPI name is taken or published |
| `README.md` (License and attribution), `https://github.com/semanticarts/gist/blob/v14.1.0/README.md`, `config.yaml`, `config.public.mk`, `TestGistNamespace` and `TestGistIrisInArtifacts` | `policies/gist-namespace-policy` | re-read Semantic Arts' license paragraph at the release tag in use; grep `LINKML_GENERATORS_OWL_ARGS` and the `owl`/`shacl` generator args; run the two test classes |
| `.github/workflows/main.yaml`, `scripts/check_generated_current.py` | CI facts in `services/verify-mappings`, `services/verify-mapping-targets` and `playbooks/regenerate-schema` | confirm it still runs the `src/gist/schema/` drift check, `just verify-mapping-targets`, `just verify-generated`, the lint step and `just test` |
| `.github/workflows/upstream-watch.yaml`, `scripts/check_upstream_release.py`, `.github/scripts/report-issue.sh` | `services/upstream-watch` | re-read the schedule, both jobs and the issue step |
| `https://www.semanticarts.com/gist/`, `https://w3id.org/lmodel/{common-domain-model,dpv,iso22989}` | the `references/` concepts | external authorities: cite on change |

Not knowledge sources (consciously excluded): `docs/elements/` and `examples/output/` (git-ignored build output), `docs/templates-linkml/` and `docs/js/` (site theming), `CODE_OF_CONDUCT.md`, `AI_COVENANT.md`, `SECURITY.md`, `NOTICE` and the rest of `CONTRIBUTING.md` (governance text the README links to), `uv.lock`, `.pre-commit-config.yaml`, `.yamllint.yaml`, `.editorconfig` (tooling), `.github/dependabot.yml`, and the `.lokf/` sidecar itself including `.github/workflows/knowledge-*.yaml`.
