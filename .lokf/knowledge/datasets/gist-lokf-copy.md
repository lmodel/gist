---
type: Dataset
id: https://w3id.org/lmodel/gist/knowledge/datasets/gist-lokf-copy
genre: reference
title: LOKF copy of gist_core.yaml
description: The copy of `gist_core.yaml` that `lokf adapt` writes for a LOKF domain schema to import as `gist_core_lokf`, with gist's top classes re-rooted on `Concept` and the five names lokf.yaml also defines renamed. `just gen-lokf-copy` builds it, and every GitHub Release attaches it as `gist-linkml-lokf-<tag>.yaml`.
resource: .github/workflows/lokf-copy-release.yaml
distribution:
  - name: gist-linkml-lokf-<tag>.yaml
    access_url: https://github.com/lmodel/gist/releases
    media_type: application/yaml
    description: Release asset with a .sha256 checksum beside it; save it beside lokf.yaml as gist_core_lokf.yaml and import gist_core_lokf.
sources:
  - resource: project.justfile
    title: the gen-lokf-copy recipe, its lokf variable and the rule that picks gist's top classes
  - resource: .lokf/pyproject.toml
    title: the lokf 0.9.0 floor
  - resource: .github/workflows/main.yaml
    title: the CI step that builds the copy
  - resource: https://lokf.nolan-nichols.com/toolkit/adapt/
    title: lokf adapt, what it changes and how it verifies the copy
derivedFrom:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
references:
  - https://w3id.org/lmodel/gist/knowledge/playbooks/release
generated:
  by: process:ktl-librarian
  at: "2026-10-28T18:37:55Z"
  revision: 0d7b36b8f1f0e4d13061f8cf001ab864bbdea4e5
status: draft
---

# LOKF copy of gist_core.yaml

LinkML merges every imported element name into one namespace, and keeps the definition from the last import. A LOKF domain schema imports LOKF's `lokf.yaml`, and the classes its concepts name must descend from LOKF's `Concept`. The [gist LinkML schema](gist-linkml-schema.md) shares five names with `lokf.yaml` (`Person`, `Organization`, `name`, `description` and `license`), and none of gist's classes descends from `Concept`. So a domain schema cannot import `gist_core.yaml` as it is.

The LOKF copy is `gist_core.yaml` as `lokf adapt` rewrites it. adapt is in lokf from 0.9.0, the floor that `.lokf/pyproject.toml` sets. It makes these changes, and lists them in a note in the copy's header:

- It renames the five shared names. `Person` becomes `GistPerson`, `Organization` becomes `GistOrganization`, and `name`, `description` and `license` become `gist_name`, `gist_description` and `gist_license`. Each keeps its gist IRI and its title, and lists its old name as an alias.
- It re-roots gist's 19 top classes on `Concept`. These are the classes with no parent that are not a mixin, leaving out `Any`. So a concept may name any gist class except the `GistThing` mixin and `Any` as its `type`, for example `type: Requirement`. A slot ranged over a gist class then takes the IRI of the concept it names, and `lokf validate --check-refs` checks that the concept exists.
- It imports `lokf` beside `linkml:types`, and names the schema `gist_core_lokf`.

Save the copy beside `lokf.yaml` as `gist_core_lokf.yaml`, and import `gist_core_lokf` from the domain schema. `gist_core.yaml` already holds the SSSOM mappings, so the copy carries them.

`just gen-lokf-copy [out]` builds the copy into `out`, which defaults to `dist/lokf`. The recipe runs `lokf adapt` on `src/gist/schema/gist_core.yaml` with `--prefix gist`, and passes one `--root` for each top class, which it reads from the schema. gist declares no identifier slot, so adapt cannot find the top classes by itself. adapt checks the copy against the `lokf.yaml` that the `.lokf` sidecar locks, and writes nothing when the check fails. CI runs the same recipe in the Python 3.14 job of `.github/workflows/main.yaml`. So if a lokf upgrade breaks the copy, its pull request fails, rather than a release that is already tagged.

`.github/workflows/lokf-copy-release.yaml` attaches the copy to a GitHub Release as `gist-linkml-lokf-<tag>.yaml`, with a `.sha256` checksum beside it. semantic-release dispatches it for every tag it releases ([release playbook](../playbooks/release.md)), and it also runs when a person publishes a release by hand. A person can run it for an existing tag to repair that tag's asset. Its `build` job has a read-only token. Only the `attach` job can write: it checks the file against its checksum before it uploads it, and in a public repository it also attests the file's build provenance.
