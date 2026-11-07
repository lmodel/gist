---
type: Service
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/services/verify-mapping-targets
title: Mapping target checker
description: Network command-line check (scripts/verify_mapping_targets.py, run as just verify-mapping-targets) that every SSSOM object term exists in the target it names, an lmodel schema or DPV's Turtle file, at a pinned commit.
resource: scripts/verify_mapping_targets.py
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
  at: "2026-11-07T15:54:12Z"
status: draft
verified:
- by: process:ktl-librarian
  at: "2026-10-16T23:47:53Z"
---

# Mapping target checker

The [mapping verifier](verify-mappings.md) only checks that each row reached the gist schema. `just verify-mapping-targets` checks the other end. It sparse-fetches each target at the commit pinned in the script's `TARGETS` table. For `common_domain_model` and `iso22989`, both under `https://w3id.org/lmodel/`, that is the schema folder. For `dpv`, bound to `https://w3id.org/dpv#`, it is DPV's core Turtle file as lmodel/dpv vendors it. Then it fails a row when:

- its object prefix is not a pinned target;
- its object IRI names no class, slot, enum or type there, or no term the Turtle file labels;
- its `object_label` is not that element's name, title or alias, or that term's label;
- the target does not declare its `object_source_version`.

It needs `git` and network access to GitHub.

`--latest` checks each target's default branch instead of the pin, and `--report FILE` also writes a Markdown report. A pin behind its default branch is noted but does not fail the check. Re-pin a target when the mappings are revised against a newer release of it.

CI runs it on the Python 3.14 leg of `.github/workflows/main.yaml`, against the pins, and the weekly [upstream watch](upstream-watch.md) runs it with `--latest`.
