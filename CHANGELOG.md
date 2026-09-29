# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Nothing has been released yet. The `v0.1.0` tag is a baseline, not a release: it marks where versioning starts so the first real release is `0.2.0` rather than `1.0.0`. The schema stays below 1.0.0 until its shape settles, so a breaking change bumps the minor version. See [CONTRIBUTING.md](CONTRIBUTING.md#releasing-maintainers).

## [Unreleased]

### Added

- **A LinkML rendering of gist 14.1.0.** `scripts/gist_to_linkml.py` converts the vendored release under `upstream/`, folds in its RDFS annotations and subclass assertions, and gives the same output on every run.
- **SSSOM mappings to other vocabularies**, in `src/gist/mappings/`, matched to schema elements by IRI and merged into the schema by `scripts/apply_sssom_overlay.py`.
- **Every gist term keeps its Semantic Arts IRI.** What this project adds lives under `gist_linkml:`, and the tests check both rules against the vendored release.
- **The package is built for PyPI as `lmodel-gist`**; the import package stays `gist`. Nothing is uploaded until PyPI releases are switched on.
- **A `.lokf/` knowledge bundle** describes the repository, kept current by the scheduled librarian and checked by `knowledge-registrar.yaml`.
- **`NOTICE` credits the third-party work this project carries or derives from**: gist and its validation files (CC BY 4.0, with the changes made), the mapping sets' terms, linkml-project-copier (MIT) and the sidecar templates. The package ships it beside `LICENSE`.
- **Governance files to the family standard**: `AI_COVENANT.md`, `SECURITY.md`, a checklist `CONTRIBUTING.md`, Contributor Covenant 2.1, and issue and pull-request templates.
- **Semantic release.** The version is computed from Conventional Commits on `main`; this file's `## [Unreleased]` section becomes the release notes, behind the `release` Environment. The PyPI upload it dispatches stays off until the `PYPI_RELEASE_ENABLED` repository variable is `true`.
- **`lint-and-docs.yaml`** runs ShellCheck, actionlint, markdownlint, lychee and codespell over every tracked Markdown file, and holds `CONTRIBUTING.md` and `SECURITY.md` to their word budgets.
- **CI fails when `src/gist/schema/` differs from what the converter generates**, so a hand edit to the schema cannot land.
- **No release before the `v0.1.0` baseline tag exists**, which would otherwise make the first release 1.0.0.

### Security

- **Every workflow pins its actions to commit SHAs and runs harden-runner in audit mode.** Dependabot now also watches the Python trees at `/` and `/.lokf`, and CI installs with `uv sync --locked`.
