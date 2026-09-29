---
type: Playbook
genre: how-to
id: https://w3id.org/lmodel/gist/knowledge/playbooks/release
title: Release the gist Python package
description: How a version tag and a published GitHub release build the gist package and publish it to TestPyPI and PyPI as lmodel-gist.
resource: https://github.com/lmodel/gist/blob/main/.github/workflows/pypi-publish.yaml
references:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
  - https://w3id.org/lmodel/gist/knowledge/datasets/generated-artefacts
generated:
  by: process:ktl-librarian
  at: "2026-09-29T11:22:44Z"
status: draft
---

# Release the gist Python package

The package version comes from the git tag through `uv-dynamic-versioning`; `pyproject.toml` declares `dynamic = ["version"]` and the distribution name `lmodel-gist`, because the PyPI name `gist` belongs to an unrelated project (kracekumar/gist); the import package is still `gist`.

1. Push a tag matching `vX.Y.Z` (or `vX.Y.ZrcN`). `.github/workflows/pypi-publish.yaml` builds with `uv build` and publishes to TestPyPI.
2. Publish a GitHub release for the tag. The same workflow publishes to PyPI through trusted publishing, in the `pypi-release` environment, whose URL is `https://pypi.org/p/lmodel-gist`. PyPI accepts that upload only once a trusted publisher for `lmodel-gist` is registered on PyPI and TestPyPI (the workflow links the trusted-publishing documentation).

No tag exists yet, so nothing has been released.
