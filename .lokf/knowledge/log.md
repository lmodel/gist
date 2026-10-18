# Change Log

## 2026-10-18

* **Changed**: the source map leaves out the sync's pull request template with the rest of the sidecar, and the two test plumbing files with the package's, so every tracked file has a place in it.

## 2026-10-17

* **Changed**: 21 concepts now name this repository's own files and folders by their path from the repository root, in `resource` and in `sources`, instead of by a GitHub URL on `main`. The work list now compares those sources, and the source map says so.

## 2026-10-16

* **Prose**: reworded 20 concept bodies in plain English. No fact, link, number or frontmatter changed.
* **Added**: the LOKF copy of `gist_core.yaml`, from `.github/workflows/lokf-copy-release.yaml`, the `gen-lokf-copy` recipe and `scripts/check_lokf_names.py`, which arrived on 2026-09-30 with no concept.
* **Changed**: the transform page now covers the `--rename` option and the `Any` range for unranged object properties, both added to `scripts/gist_to_linkml.py` on 2026-09-30, and the test count, which is now 200.
* **Changed**: the suite now collects 302 tests, and CI now also builds the LOKF copy, as `.github/workflows/main.yaml` has done since 2026-09-30.
* **Changed**: the release playbook now says that every release dispatches the LOKF copy workflow, as `semantic-release.yml` and `CONTRIBUTING.md` have said since 2026-09-30.
* **Changed**: `gist_core.yaml` now holds 98 classes, since the converter added the `Any` class on 2026-09-30.
* **Changed**: the quoted phrase "FINOS CDM classes" left the CDM mapping set's metadata on 2026-09-29, so the page now quotes the description the file holds.
* **Changed**: the SSSOM page now carries the qualifier from `tests/test_sssom_files.py` that no release up to sssom-schema 1.1.0a5 lists `LLMBasedMatching`, and notes that the schema's `master` branch now does.
* **Source map**: added the LOKF copy's workflow, recipe and name check, and `changelog-release.mjs` to the release row; listed the files the map had not accounted for as left out on purpose; and noted that the work list cannot compare this bundle's URL sources.

## 2026-10-15

* **Changed**: the schema id in the description is set as code, so the index bullet derived from it is not a bare URL.
* **Changed**: the namespace in the description is set as code, so the index bullet derived from it is not a bare URL.
* **Changed**: the site address in the description is set as code, so the index bullet derived from it is not a bare URL.

## 2026-09-29

* **Upstream and target checks**: Added `services/verify-mapping-targets` and `services/upstream-watch` for the target-term checker and the weekly upstream workflow; the source map now lists their scripts and `check_generated_current.py`.
* **PyPI switch**: `playbooks/release` records that uploads to TestPyPI and PyPI wait for the `PYPI_RELEASE_ENABLED` repository variable, which is unset.
* **Release and CI refresh**: `playbooks/release` now follows semantic-release, the baseline-tag guard and the dispatched PyPI upload; `services/verify-mappings` and `playbooks/regenerate-schema` record that CI now fails a schema that differs from its converter. The source map follows, and names the new governance files it leaves out.
* **Namespace policy**: Added `policies/gist-namespace-policy.md`, recording Semantic Arts' two namespace conditions and the converter, generator flags and tests that hold them.
* **Namespace refresh**: `gist:` now names Semantic Arts' namespace and this project's additions use `gist_linkml:`, so the claims in `references/gist-ontology`, `datasets/gist-linkml-schema`, `datasets/generated-artefacts` and `services/gist-to-linkml` were corrected; the transform is now deterministic.
* **Mapping tools and release**: The overlay and verifier match subjects by IRI, and the distribution is `gist-linkml`, which answers the release playbook's open question. The source map and test counts follow.
* **Bootstrap discovery**: Replaced the two placeholder services with 21 concepts derived from the repository: the upstream gist release, the LinkML schema, three SSSOM mapping sets and their object schemas, the transform, overlay and verifier scripts, generated artefacts, test data, the documentation site, and the regenerate and release playbooks.
* **Source map**: Recorded `playbooks/knowledge-sources.md`, the map every later refresh re-verifies against.
* **Initialization**: Scaffolded the LOKF bundle for gist with placeholder
  services. Real concepts to follow.
