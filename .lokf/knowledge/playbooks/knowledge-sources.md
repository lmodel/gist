---
type: Playbook
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/playbooks/knowledge-sources
title: Knowledge sources map
description: "The librarian's scrape map: every repository location and external URL this bundle derives concepts from, and how to re-verify each on a refresh run."
resource: https://github.com/lmodel/gist
generated:
  by: process:ktl-librarian
  at: "2026-10-22T09:11:36Z"
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-18T00:19:20Z"
---

# Knowledge sources

Bootstrap discovery ran 2026-09-29. Steady-state refresh runs re-verify these sources instead of discovering them again. Update this map whenever the repository's knowledge geography changes.

Each concept derived from a file or folder of this repository names it by its path from the repository root, in `resource` and in `sources`. `knowledge-report.sh worklist` compares each such path's last commit with the commit that recorded the concept's stamp, and lists the concepts whose source moved. It never fetches a URL, so re-read the external sources this table names on every refresh.

| Source | Yields | Re-check by |
|--------|--------|-------------|
| `pyproject.toml`, `README.md`, `docs/about.md`, `.copier-answers.yml` | bundle metadata, `references/gist-ontology` | diff manifest name, description and authors |
| `upstream/gist14.1.0_webDownload/` | `datasets/gist-upstream-turtle`, `references/gist-ontology`, `org/semantic-arts` | re-list `ontologies/turtle/`; a new release folder means a new upstream version |
| `src/gist/schema/*.yaml` | `datasets/gist-linkml-schema` | reload each module and recount classes, slots and enum values; re-read `gist.yaml` imports |
| `src/gist/mappings/*.sssom.tsv` | the three `datasets/gist-*-mappings`, the three object-side `references/`, `glossary/sssom` | re-list the folder; recount rows, predicates and justifications per file; re-read each metadata header |
| `scripts/gist_to_linkml.py`, `scripts/apply_sssom_overlay.py`, `scripts/verify_mappings.py`, `scripts/verify_mapping_targets.py` | the four `services/` CLIs | re-read each docstring and `argparse` block; run `uv run python scripts/verify_mappings.py` |
| `project.justfile`, `justfile` | `playbooks/regenerate-schema`, recipe facts in the services | re-read the `gen-linkml`, `apply-sssom-overlay`, `verify-mappings`, `gen-project` and `test` recipe chains |
| `project/`, `src/gist/datamodel/`, `.linkml/generators.yaml` | `datasets/generated-artefacts` | re-list `project/*/`; re-read the `excludes` in `.linkml/generators.yaml` |
| `tests/data/`, `tests/test_*.py` | `datasets/test-data`, test counts in the concepts | re-list `tests/data/`; `uv run pytest --collect-only -q` per file |
| `tests/vendor/semanticarts/` | `datasets/semantic-arts-shapes` | re-list; compare `LICENSE.txt` with the upstream copy |
| `mkdocs.yml`, `.github/workflows/deploy-docs.yaml`, `https://lmodel.github.io/gist` | `services/documentation-site` | confirm the trigger and the `gen-doc` plus `gh-deploy` steps; fetch the site and the w3id redirect |
| `.github/workflows/lokf-copy-release.yaml`, the `gen-lokf-copy` recipe and `lokf_renames` in `project.justfile`, `scripts/check_lokf_names.py` | `datasets/gist-lokf-copy` | re-read the rename list, the name check and both jobs; list the latest release's assets with `gh release view --json assets` |
| `.github/workflows/semantic-release.yml`, `.releaserc.json`, `.github/scripts/changelog-release.mjs`, `.github/workflows/pypi-publish.yaml`, `pyproject.toml`, `CONTRIBUTING.md` (Releasing), `https://pypi.org/pypi/gist-linkml/json` | `playbooks/release` | re-read the release guards, the dispatches, the triggers, environments and distribution name; check whether the PyPI name is taken or published |
| `README.md` (License and attribution), `https://github.com/semanticarts/gist/blob/v14.1.0/README.md`, `.linkml/generators.yaml`, `config.public.mk`, `TestGistNamespace` and `TestGistIrisInArtifacts` | `policies/gist-namespace-policy` | re-read Semantic Arts' license paragraph at the release tag in use; grep `LINKML_GENERATORS_OWL_ARGS` and the `owl`/`shacl` generator args; run the two test classes |
| `.github/workflows/main.yaml`, `scripts/check_generated_current.py` | CI facts in `services/verify-mappings`, `services/verify-mapping-targets`, `playbooks/regenerate-schema` and `datasets/gist-lokf-copy` | confirm it still runs the `src/gist/schema/` drift check, `just verify-mapping-targets`, `just verify-generated`, `just gen-lokf-copy`, the lint step and `just test` |
| `.github/workflows/upstream-watch.yaml`, `scripts/check_upstream_release.py`, `.github/scripts/report-issue.sh` | `services/upstream-watch` | re-read the schedule, both jobs and the issue step |
| `https://www.semanticarts.com/gist/`, `https://w3id.org/lmodel/{common-domain-model,dpv,iso22989}`, `https://mapping-commons.github.io/sssom/`, `https://pypi.org/project/sssom-schema/` | the `references/` concepts, `glossary/sssom` | external authorities: cite on change |

These are not knowledge sources, and are left out on purpose:

- `docs/elements/` and `examples/output/` (git-ignored build output);
- `docs/templates-linkml/` and `docs/js/` (site theming);
- `docs/index.md`, `examples/README.md` and `src/README.md` (short pages from the project template);
- `CODE_OF_CONDUCT.md`, `AI_COVENANT.md`, `SECURITY.md`, `NOTICE`, `LICENSE`, `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md` and the rest of `CONTRIBUTING.md` (governance text the README links to);
- `CHANGELOG.md` (release history);
- `uv.lock`, `.gitignore`, `.pre-commit-config.yaml`, `.yamllint.yaml`, `.editorconfig`, `.markdownlint-cli2.jsonc`, `lychee.toml` and `.github/workflows/lint-and-docs.yaml` (tooling and its static checks);
- `src/gist/__init__.py`, `src/gist/_version.py`, `tests/__init__.py` and `tests/conftest.py` (package and test plumbing);
- `.github/dependabot.yml`;
- `llms.txt` (the pointer that sends agents to this bundle);
- the `.lokf/` sidecar itself, including the `knowledge_bundle` link, `.github/workflows/knowledge-*.yaml` and `.github/PULL_REQUEST_TEMPLATE/knowledge-sync.md`.
