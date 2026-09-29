---
type: Playbook
genre: how-to
id: https://w3id.org/lmodel/gist/knowledge/playbooks/release
title: Release the gist Python package
description: How a releasing merge to main becomes a tagged GitHub Release through semantic-release and is uploaded to PyPI as lmodel-gist.
resource: https://github.com/lmodel/gist/blob/main/.github/workflows/semantic-release.yml
sources:
  - resource: https://github.com/lmodel/gist/blob/main/.github/workflows/pypi-publish.yaml
  - resource: https://github.com/lmodel/gist/blob/main/.releaserc.json
  - resource: https://github.com/lmodel/gist/blob/main/CONTRIBUTING.md
references:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
  - https://w3id.org/lmodel/gist/knowledge/datasets/generated-artefacts
generated:
  by: process:ktl-librarian
  at: "2026-09-29T12:29:55Z"
status: draft
---

# Release the gist Python package

The package version comes from the git tag through `uv-dynamic-versioning`; `pyproject.toml` declares `dynamic = ["version"]` and the distribution name `lmodel-gist`, because the PyPI name `gist` belongs to an unrelated project (kracekumar/gist); the import package is still `gist`. No file is bumped on release.

1. Once, before the first release, push the `v0.1.0` baseline tag on `main`. Both jobs of `.github/workflows/semantic-release.yml` refuse to release without a `v*` tag, because semantic-release would otherwise make the first release 1.0.0. The baseline is not uploaded anywhere.
2. Write the change under `## [Unreleased]` in `CHANGELOG.md`, and type the commit and the pull-request title `feat:`, `fix:` or `security:`; other types release nothing. The `plan` job refuses a releasing pull request whose changelog section is empty or whose title carries no releasing type.
3. Merge to `main`. The `release` job, in the `release` Environment, retitles the section `## [X.Y.Z] - YYYY-MM-DD`, commits `CHANGELOG.md`, tags `vX.Y.Z` and publishes the GitHub Release from that text. While below 1.0.0, `.releaserc.json` makes a breaking change a minor bump.
4. The same job dispatches `.github/workflows/pypi-publish.yaml` on the new tag, which builds with `uv build` and uploads to PyPI through trusted publishing in the `pypi-release` environment (`https://pypi.org/p/lmodel-gist`). PyPI accepts the first upload only once a pending trusted publisher for `lmodel-gist` naming that workflow and environment is registered there.

A `v*` tag pushed by a person, other than the baseline, uploads to TestPyPI instead, and a release published by hand in the GitHub UI uploads to PyPI.

No tag exists yet, and nothing is on PyPI or TestPyPI.
