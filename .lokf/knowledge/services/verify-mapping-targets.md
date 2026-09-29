---
type: Service
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/services/verify-mapping-targets
title: Mapping target checker
description: Network command-line check (scripts/verify_mapping_targets.py, run as just verify-mapping-targets) that every SSSOM object term exists in the lmodel target schema it names, at a pinned commit.
resource: https://github.com/lmodel/gist/blob/main/scripts/verify_mapping_targets.py
tags:
  - cli
dependsOn:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-cdm-mappings
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-dpvs-mappings
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-iso22989-mappings
  - https://w3id.org/lmodel/gist/knowledge/references/common-domain-model
  - https://w3id.org/lmodel/gist/knowledge/references/dpvs
  - https://w3id.org/lmodel/gist/knowledge/references/iso22989
relatedTo:
  - https://w3id.org/lmodel/gist/knowledge/services/verify-mappings
generated:
  by: process:ktl-librarian
  at: "2026-09-29T21:02:46Z"
status: draft
---

# Mapping target checker

The [mapping verifier](verify-mappings.md) only checks that each row reached the gist schema. `just verify-mapping-targets` checks the other end: it sparse-fetches each target's schema folder at the commit pinned in the script's `TARGETS` table (`common_domain_model`, `dpv` and `iso22989`, all under `https://w3id.org/lmodel/`), then fails a row whose object prefix is not a pinned target, whose object IRI names no class, slot, enum or type there, whose `object_label` is not that element's name, title or alias, or whose `object_source_version` the target does not declare. It needs `git` and network access to GitHub.

`--latest` checks each target's default branch instead of the pin, and `--report FILE` also writes a Markdown report. A pin behind its default branch is noted but does not fail the check. Re-pin a target when the mappings are revised against a newer release of it.

CI runs it on the Python 3.14 leg of `.github/workflows/main.yaml`, against the pins; the weekly [upstream watch](upstream-watch.md) runs it with `--latest`.
