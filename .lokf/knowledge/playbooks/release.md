---
type: Playbook
genre: how-to
id: https://w3id.org/lmodel/gist/knowledge/playbooks/release
title: Release the gist Python package
description: How a version tag and a published GitHub release build the gist package and publish it to TestPyPI and PyPI.
resource: https://github.com/lmodel/gist/blob/main/.github/workflows/pypi-publish.yaml
references:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
  - https://w3id.org/lmodel/gist/knowledge/datasets/generated-artefacts
generated:
  by: process:ktl-librarian
  at: "2026-09-29T10:32:37Z"
status: draft
---

# Release the gist Python package

The package version comes from the git tag through `uv-dynamic-versioning`; `pyproject.toml` declares `dynamic = ["version"]` and the distribution name `gist`.

1. Push a tag matching `vX.Y.Z` (or `vX.Y.ZrcN`). `.github/workflows/pypi-publish.yaml` builds with `uv build` and publishes to TestPyPI.
2. Publish a GitHub release for the tag. The same workflow publishes to PyPI through trusted publishing, in the `pypi-release` environment, whose URL is `https://pypi.org/p/gist`.

No tag exists yet, so nothing has been released.

## Open questions

- 2026-09-29, process:ktl-librarian: the PyPI name `gist` already belongs to an unrelated project (kracekumar/gist, a command-line client for gist.github.com), so a PyPI publish under that name should be refused. Should the distribution be renamed (for example `lmodel-gist`), or is PyPI publishing not intended for this repository?
