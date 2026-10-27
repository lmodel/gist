---
type: Playbook
genre: how-to
id: https://w3id.org/lmodel/gist/knowledge/playbooks/release
title: Release the gist Python package
description: How a releasing merge to main becomes a tagged GitHub Release through semantic-release, with the LOKF copy of gist_core.yaml attached, and is uploaded to PyPI as gist-linkml.
resource: .github/workflows/semantic-release.yml
sources:
  - resource: .github/workflows/pypi-publish.yaml
  - resource: .releaserc.json
  - resource: CONTRIBUTING.md
  - resource: .github/workflows/lokf-copy-release.yaml
references:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
  - https://w3id.org/lmodel/gist/knowledge/datasets/generated-artefacts
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-lokf-copy
generated:
  by: process:ktl-librarian
  at: "2026-10-27T08:54:25Z"
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-27T14:09:11Z"
---

# Release the gist Python package

The package version comes from the git tag through `uv-dynamic-versioning`. `pyproject.toml` declares `dynamic = ["version"]` and the distribution name `gist-linkml`, because the PyPI name `gist` belongs to an unrelated project (kracekumar/gist). The import package is still `gist`. No file is bumped on release.

1. Once, before the first release, push the `v0.1.0` baseline tag on `main`. Both jobs of `.github/workflows/semantic-release.yml` refuse to release without a `v*` tag, because semantic-release would otherwise make the first release 1.0.0. The baseline is not uploaded anywhere.
2. Write the change under `## [Unreleased]` in `CHANGELOG.md`, and type the commit and the pull-request title `feat:`, `fix:` or `security:`, or mark any type breaking with a `!`. A `BREAKING CHANGE` footer marks a commit breaking too. Other types release nothing. The `plan` job refuses a releasing pull request whose changelog section is empty or whose title carries no releasing type.
3. Merge to `main`. The `release` job, in the `release` Environment, retitles the section `## [X.Y.Z] - YYYY-MM-DD`, commits `CHANGELOG.md`, tags `vX.Y.Z` and publishes the GitHub Release from that text. While below 1.0.0, `.releaserc.json` makes a breaking change a minor bump.
4. Once the `PYPI_RELEASE_ENABLED` repository variable is `true`, the same job dispatches `.github/workflows/pypi-publish.yaml` on the new tag, which builds with `uv build` and uploads to PyPI through trusted publishing in the `pypi-release` environment (`https://pypi.org/p/gist-linkml`). PyPI accepts the first upload only once a pending trusted publisher for `gist-linkml` naming that workflow and environment is registered there.

With the variable on, a `v*` tag that a person pushes uploads to TestPyPI instead, unless it is the baseline, and a release published by hand in the GitHub UI uploads to PyPI. With it unset, `pypi-publish.yaml` skips every trigger.

PyPI releases are off for now, and nothing is on PyPI or TestPyPI.

Every release also gets the [LOKF copy](../datasets/gist-lokf-copy.md) of `gist_core.yaml`, whatever `PYPI_RELEASE_ENABLED` says. The `release` job dispatches `.github/workflows/lokf-copy-release.yaml` on the new tag, and that workflow attaches the copy to the GitHub Release as `gist-linkml-lokf-<tag>.yaml`, with a `.sha256` checksum.
