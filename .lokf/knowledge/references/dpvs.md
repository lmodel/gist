---
type: Reference
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/references/dpvs
title: Data Privacy Vocabulary (DPV)
description: The Data Privacy Vocabulary (DPV) 2.3 of the W3C Data Privacy Vocabularies and Controls Community Group, the object side of the gist-to-DPV mapping set.
resource: https://w3id.org/dpv
generated:
  by: process:ktl-librarian
  at: "2026-11-07T15:54:12Z"
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-18T00:19:20Z"
---

# Data Privacy Vocabulary (DPV)

This is the `object_source` of the [gist to DPV mappings](../datasets/gist-dpvs-mappings.md), which bind the prefix `dpv:` to `https://w3id.org/dpv#`, DPV's own namespace, at DPV 2.3. Until 2026-11-07 the prefix named `https://w3id.org/lmodel/dpv/`, the namespace of lmodel/dpv's LinkML classes. Since its first release, lmodel/dpv holds DPV's terms as records rather than classes, so those IRIs name nothing, and the mappings now name DPV's terms directly. This repository holds no copy of DPV. `just verify-mapping-targets` fetches DPV's core Turtle file, `upstream/<version>/dpv/dpv.ttl`, from lmodel/dpv at a pinned commit, where it is matched to DPV's release by git object hash, and checks that every mapped term exists there.
