---
type: Dataset
id: https://w3id.org/lmodel/gist/knowledge/datasets/gist-lokf-copy
genre: reference
title: LOKF copy of gist_core.yaml
description: "`gist_core.yaml` with the five names LOKF's lokf.yaml also defines renamed (Person, Organization, name, description, license), built by `just gen-lokf-copy` and attached to every GitHub Release as `gist-linkml-lokf-<tag>.yaml`, so a LOKF domain schema can import gist beside lokf.yaml."
resource: .github/workflows/lokf-copy-release.yaml
distribution:
  - name: gist-linkml-lokf-<tag>.yaml
    access_url: https://github.com/lmodel/gist/releases
    media_type: application/yaml
    description: Release asset with a .sha256 checksum beside it; save it as gist_core.yaml and import gist_core.
sources:
  - resource: project.justfile
    title: the gen-lokf-copy recipe and lokf_renames
  - resource: scripts/check_lokf_names.py
    title: the check that the copy shares no element name with lokf.yaml
  - resource: scripts/gist_to_linkml.py
    title: the --rename option
  - resource: .github/workflows/main.yaml
    title: the CI step that builds the copy
derivedFrom:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-upstream-turtle
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-cdm-mappings
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-dpvs-mappings
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-iso22989-mappings
references:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
  - https://w3id.org/lmodel/gist/knowledge/services/gist-to-linkml
  - https://w3id.org/lmodel/gist/knowledge/services/apply-sssom-overlay
generated:
  by: process:ktl-librarian
  at: "2026-10-27T14:09:11Z"
status: draft
---

# LOKF copy of gist_core.yaml

LinkML merges every imported element name into one namespace, and keeps the definition from the last import. LOKF's `lokf.yaml` also defines `Person`, `Organization`, `name`, `description` and `license`. So a LOKF domain schema that imported the [gist LinkML schema](gist-linkml-schema.md) beside `lokf.yaml` would silently lose one side's definition of each.

The LOKF copy is `gist_core.yaml` with those five names changed: `Person` becomes `GistPerson`, `Organization` becomes `GistOrganization`, and `name`, `description` and `license` become `gist_name`, `gist_description` and `gist_license`. Each renamed class or slot keeps its gist IRI, and keeps gist's label as its title. For all five, that label is the old name, so the old name is not repeated as an alias. A note in the schema header lists the renames. The SSSOM mappings are applied, and the file imports nothing but `linkml:types`. Save it as `gist_core.yaml` and import `gist_core`.

`just gen-lokf-copy [out]` builds it into `out`, which defaults to `dist/lokf`. The recipe runs the [gist-to-LinkML transform](../services/gist-to-linkml.md) with one `--rename` for each of the five names, then the [SSSOM overlay](../services/apply-sssom-overlay.md), and copies `gist_core.yaml` into `out`. `scripts/check_lokf_names.py` then fails the build when the copy imports anything but `linkml:types`, or shares a class, slot, enum, type or subset name with the `lokf.yaml` that the `.lokf` sidecar locks. CI runs the same recipe in the Python 3.14 job of `.github/workflows/main.yaml`. So if a lokf upgrade adds a name that gist also has, its pull request fails, rather than a release that is already tagged.

`.github/workflows/lokf-copy-release.yaml` attaches the copy to a GitHub Release as `gist-linkml-lokf-<tag>.yaml`, with a `.sha256` checksum beside it. semantic-release dispatches it for every tag it releases ([release playbook](../playbooks/release.md)), and it also runs when a person publishes a release by hand. A person can run it for an existing tag to repair that tag's asset. Its `build` job has a read-only token. Only the `attach` job can write: it checks the file against its checksum before it uploads it, and in a public repository it also attests the file's build provenance.
