# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The `v0.1.0` tag is a baseline, not a release: it marks where versioning starts so the first real release is `0.2.0` rather than `1.0.0`. The schema stays below 1.0.0 until its shape settles, so a breaking change bumps the minor version. See [CONTRIBUTING.md](CONTRIBUTING.md#releasing-maintainers).

## [Unreleased]

### Added

- **`gist_to_linkml.py --rename OLD=NEW` gives a gist class or slot another LinkML name and keeps its gist IRI**, for a schema that imports gist beside another vocabulary with the same names. LOKF's `Person`, `Organization`, `name`, `description` and `license` are the case in point. Default output is unchanged.
- **Each release carries `gist-linkml-lokf-<tag>.yaml`**, gist_core.yaml with those five renamed, so a LOKF domain schema can import it beside `lokf.yaml` in either order. `just gen-lokf-copy` builds it and fails on any name still shared with the `lokf.yaml` the sidecar locks; CI runs the same check on every pull request.

### Changed

- **Release assets are named `gist-linkml`**, the published package name, instead of the repository's name `gist`: the bundle zip is `knowledge-<tag>-gist-linkml.zip` and the Copilot skill `ktl-docent-m365-<tag>-gist-linkml.zip`. `knowledge-release.yaml` is refreshed from the ktl-sidecar template, which reads the name from the `KNOWLEDGE_RELEASE_NAME` repository variable.

## [0.2.1] - 2026-09-29

### Added

- **CI also fails on stale artefacts and schema errors.** `just verify-generated` compares `project/` and the datamodel with a fresh `gen-project` by content, and `linkml-lint` fails the run on errors.
- **`upstream-watch.yaml` checks weekly what the build depends on but cannot control**: whether Semantic Arts has released a newer gist, whether `upstream/` still matches its release byte for byte, and whether every mapped target term still exists on its schema's default branch. A failure opens or updates an issue.
- **`just verify-mapping-targets` checks that every mapped term exists** in its target schema, fetched at a pinned commit, and runs in CI.

### Fixed

- **The converter no longer loses or bends what gist says.** A union domain was written as an `any_of` range and functional properties were marked multivalued; both are corrected. It now carries `gist:domainIncludes` and `rangeIncludes` as slot annotations, union datatype ranges as `any_of`, `owl:qualifiedCardinality`, `rdfs:seeAlso`, the editorial notes on reference individuals, the `gist:uniqueText` of each media type, and each module's ontology header (definition, license, release history, version IRI).
- **`disjoint_with` is always a list**, as the LinkML metamodel requires, so `linkml-lint` reports no errors on the schema.
- **The SSSOM mappings name real terms.** The CDM and DPV sets bound their prefixes to namespaces that do not exist, and one DPV target was misspelt; each mapping set's file is now named after its set. Reversed broad and narrow matches and overstated close and exact matches are corrected, two unsupported mappings are dropped, and the files pass the SSSOM validator except for `semapv:LLMBasedMatching`, which SEMAPV defines but the SSSOM schema does not yet list.

## [0.2.0] - 2026-09-29

### Added

- **A LinkML rendering of gist 14.1.0.** `scripts/gist_to_linkml.py` converts the vendored release under `upstream/`, folds in its RDFS annotations and subclass assertions, and gives the same output on every run.
- **SSSOM mappings to other vocabularies**, in `src/gist/mappings/`, matched to schema elements by IRI and merged into the schema by `scripts/apply_sssom_overlay.py`.
- **Every gist term keeps its Semantic Arts IRI.** What this project adds lives under `gist_linkml:`, and the tests check both rules against the vendored release.
- **The package is built for PyPI as `gist-linkml`**; the import package stays `gist`. Nothing is uploaded until PyPI releases are switched on.
- **A `.lokf/` knowledge bundle** describes the repository, kept current by the scheduled librarian and checked by `knowledge-registrar.yaml`.
- **`NOTICE` credits the third-party work this project carries or derives from**: gist and its validation files (CC BY 4.0, with the changes made), the mapping sets' terms, linkml-project-copier (MIT) and the sidecar templates. The package ships it beside `LICENSE`.
- **Governance files to the family standard**: `AI_COVENANT.md`, `SECURITY.md`, a checklist `CONTRIBUTING.md`, Contributor Covenant 2.1, and issue and pull-request templates.
- **Semantic release.** The version is computed from Conventional Commits on `main`; this file's `## [Unreleased]` section becomes the release notes, behind the `release` Environment. The PyPI upload it dispatches stays off until the `PYPI_RELEASE_ENABLED` repository variable is `true`.
- **`lint-and-docs.yaml`** runs ShellCheck, actionlint, markdownlint, lychee and codespell over every tracked Markdown file, and holds `CONTRIBUTING.md` and `SECURITY.md` to their word budgets.
- **CI fails when `src/gist/schema/` differs from what the converter generates**, so a hand edit to the schema cannot land.
- **No release before the `v0.1.0` baseline tag exists**, which would otherwise make the first release 1.0.0.

### Security

- **Every workflow pins its actions to commit SHAs and runs harden-runner in audit mode.** Dependabot now also watches the Python trees at `/` and `/.lokf`, and CI installs with `uv sync --locked`.
