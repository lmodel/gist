---
type: Service
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/services/upstream-watch
title: Upstream watch
description: Weekly GitHub workflow (upstream-watch.yaml) that checks the vendored gist release is Semantic Arts' latest and intact, and that mapped target terms still exist on each target's default branch, opening an issue on failure.
resource: https://github.com/lmodel/gist/blob/main/.github/workflows/upstream-watch.yaml
tags:
  - ci
dependsOn:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-upstream-turtle
  - https://w3id.org/lmodel/gist/knowledge/services/verify-mapping-targets
references:
  - https://w3id.org/lmodel/gist/knowledge/references/gist-ontology
sources:
  - resource: https://github.com/lmodel/gist/blob/main/scripts/check_upstream_release.py
  - resource: https://github.com/lmodel/gist/blob/main/.github/scripts/report-issue.sh
generated:
  by: process:ktl-librarian
  at: "2026-09-29T21:02:46Z"
status: draft
---

# Upstream watch

`.github/workflows/upstream-watch.yaml` runs on Mondays at 07:00 UTC and on manual dispatch. It watches what the repository is built from but does not control, so nothing in a pull request could catch a change there.

- **gist-release** runs `scripts/check_upstream_release.py` (`just check-upstream` locally). It asks the GitHub API for semanticarts/gist's latest release and compares every file under `upstream/gist<version>_webDownload/` byte for byte with that version's web-download zip. It exits 1 when a newer release exists or a vendored file differs.
- **mapping-targets** runs the [mapping target checker](verify-mapping-targets.md) with `--latest`, to hear of a renamed or dropped target term before anyone re-pins.

When either check fails, `.github/scripts/report-issue.sh` opens an issue, or comments on the one already open, so the finding does not depend on anyone reading the run log. Acting on a new gist release follows the [regenerate playbook](../playbooks/regenerate-schema.md).
