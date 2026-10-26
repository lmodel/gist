# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The `v0.1.0` tag is a baseline, not a release: it marks where versioning starts so the first real release is `0.2.0` rather than `1.0.0`. The schema stays below 1.0.0 until its shape settles, so a breaking change bumps the minor version. See [CONTRIBUTING.md](CONTRIBUTING.md#releasing-maintainers).

## [Unreleased]

## [0.3.13] - 2026-10-23

### Security

- **The sidecar copies and the skills pin are at Knowledge Trust Ladder [v0.55.2](https://github.com/noelmcloughlin/knowledge-trust-ladder/compare/600b61b91446922d12453cfbcc843a6ab86c8fd5...v0.55.2).** The release changed `.lokf/scripts/knowledge-preflight.sh` and `.lokf/scripts/knowledge-sync.sh` here.

## [0.3.12] - 2026-10-21

### Security

- **The sidecar copies and the skills pin are at Knowledge Trust Ladder [v0.55.0](https://github.com/noelmcloughlin/knowledge-trust-ladder/compare/d5c7817f57ac4e68cd48721a309825afaacd8994...600b61b91446922d12453cfbcc843a6ab86c8fd5).** The release changed `.github/workflows/knowledge-registrar.yaml`, `.github/workflows/knowledge-release.yaml`, `.github/workflows/knowledge-sync.yaml`, `.lokf/scripts/knowledge-librarian.sh`, `.lokf/scripts/knowledge-conventions.sh`, `.lokf/scripts/knowledge-conventions.py`, `.lokf/scripts/knowledge-preflight.sh`, `.lokf/scripts/knowledge-provenance.sh`, `.lokf/scripts/knowledge-feedback.sh`, `.lokf/scripts/knowledge-apply.sh`, `.lokf/scripts/knowledge-apply.py`, `.lokf/scripts/knowledge-report.sh`, `.lokf/scripts/knowledge-sync.sh`, `.lokf/.gitignore` and `.lokf/justfile` here.

## [0.3.11] - 2026-10-19

### Security

- **The sidecar copies and the skills pin are at Knowledge Trust Ladder [v0.53.0](https://github.com/noelmcloughlin/knowledge-trust-ladder/compare/2801e26f2fc99675eb395b639670ec789e49eb08...d5c7817f57ac4e68cd48721a309825afaacd8994).** The release changed `.github/workflows/knowledge-librarian.yaml`, `.github/workflows/knowledge-sync.yaml`, `.github/PULL_REQUEST_TEMPLATE/knowledge-sync.md`, `.lokf/scripts/knowledge-librarian.sh`, `.lokf/scripts/knowledge-apply.py` and `.lokf/scripts/knowledge-sync.sh` here.

## [0.3.10] - 2026-10-19

### Security

- **The sidecar copies and the skills pin are at Knowledge Trust Ladder [v0.52.0](https://github.com/noelmcloughlin/knowledge-trust-ladder/compare/b7d15e5c58554d6af4b71dfe35ef2a6bfe8c45d8...2801e26f2fc99675eb395b639670ec789e49eb08).** The release changed `.github/workflows/knowledge-registrar.yaml`, `.github/PULL_REQUEST_TEMPLATE/knowledge-sync.md`, `.lokf/scripts/knowledge-conventions.sh`, `.lokf/scripts/knowledge-conventions.py`, `.lokf/scripts/knowledge-preflight.sh`, `.lokf/scripts/knowledge-report.sh` and `.lokf/scripts/knowledge-sync.sh` here.

## [0.3.9] - 2026-10-17

### Security

- **The sidecar copies and the skills pin are at Knowledge Trust Ladder [v0.47.0](https://github.com/noelmcloughlin/knowledge-trust-ladder/compare/13f847f1988ec1a7f1c41f63cc3f1945c2010231...b7d15e5c58554d6af4b71dfe35ef2a6bfe8c45d8).** The release changed `.lokf/scripts/knowledge-preflight.sh`, `.github/workflows/knowledge-sync.yaml`, `.github/PULL_REQUEST_TEMPLATE/knowledge-sync.md` and `.lokf/scripts/knowledge-sync.sh` here.

## [0.3.8] - 2026-10-17

### Security

- **The sidecar copies and the skills pin match `v0.46.0`.** The release changed `.github/workflows/knowledge-release.yaml`, `.lokf/scripts/knowledge-federate.py`, `website/package-lock.json` and `website/package.json` here; its [changelog](https://github.com/noelmcloughlin/knowledge-trust-ladder/blob/13f847f1988ec1a7f1c41f63cc3f1945c2010231/CHANGELOG.md) says how.

## [0.3.7] - 2026-10-17

### Security

- **The sidecar copies and the skills pin match `v0.45.1`.** The release changed `.lokf/scripts/knowledge-apply.py` and `.lokf/scripts/knowledge-federate.py` here; its [changelog](https://github.com/noelmcloughlin/knowledge-trust-ladder/blob/d38e52b20d99c21ff201be9252a01b1da28fff57/CHANGELOG.md) says how.

## [0.3.6] - 2026-10-16

### Security

- **The sidecar copies and the skills pin match `v0.45.0`.** The release changed `.lokf/scripts/knowledge-report.sh`, `.lokf/m365/ktl-docent-m365.md`, `website/scripts/sync.mjs`, `website/src/components/ConceptCard.astro`, `website/src/content.config.ts` and `website/src/styles/catalogue.css` here; its [changelog](https://github.com/noelmcloughlin/knowledge-trust-ladder/blob/08c13b5e30a6e0c4c6a2373658ee2c3ebbf4ae8e/CHANGELOG.md) says how.

## [0.3.5] - 2026-10-16

### Security

- **The lock takes the patched tornado, urllib3, mistune and jupyter-server.** It closes every open security alert on `uv.lock`, the critical jupyter-server one included. The published package's own dependencies are unchanged.

## [0.3.4] - 2026-10-16

### Security

- **The skills pin matches `v0.44.0`.** The release changed none of the sidecar copies this repository carries.

## [0.3.3] - 2026-10-15

### Security

- **The sidecar copies and the skills pin match ktl-sidecar `v0.43.1`.** The pin had stayed at `v0.27.1`; the sync adds the apply and report scripts and the gate's newer conventions checks.

## [0.3.2] - 2026-10-15

### Fixed

- **`.lokf/justfile` takes a domain schema as one variable.** It was the copy from before ktl-sidecar `v0.38.0`, which the sidecar sync never carried. The generated schema is unchanged.

## [0.3.1] - 2026-09-30

### Fixed

- **An object property gist leaves unranged now ranges over `Any`, not `string`.** Its value is an individual, so a JSON-LD context reads it as an IRI, and the generated OWL declares it an object property again rather than a datatype property.

## [0.3.0] - 2026-09-29

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
