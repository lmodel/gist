---
type: Dataset
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
title: gist LinkML schema
description: LinkML rendering of gist 14.1.0 (schema id https://w3id.org/lmodel/gist), generated from the upstream Turtle modules with the curated SSSOM mappings overlaid.
resource: https://github.com/lmodel/gist/blob/main/src/gist/schema/gist.yaml
version: "14.1.0"
license: https://creativecommons.org/licenses/by/4.0/
distribution:
  - name: gist.yaml
    access_url: https://github.com/lmodel/gist/blob/main/src/gist/schema/gist.yaml
    media_type: application/yaml
    description: Aggregator schema; imports gist_core, gist_media_types and gist_prefix_declarations.
  - name: gist_core.yaml
    access_url: https://github.com/lmodel/gist/blob/main/src/gist/schema/gist_core.yaml
    media_type: application/yaml
    description: 97 classes, 120 slots and the AspectInstance enum (8 values).
  - name: gist_media_types.yaml
    access_url: https://github.com/lmodel/gist/blob/main/src/gist/schema/gist_media_types.yaml
    media_type: application/yaml
    description: MediaTypeInstance enum (14 IANA media types); imports gist_core.
  - name: gist_prefix_declarations.yaml
    access_url: https://github.com/lmodel/gist/blob/main/src/gist/schema/gist_prefix_declarations.yaml
    media_type: application/yaml
    description: PrefixDeclarationInstance enum (7 SHACL prefix declarations).
  - name: gist_rdfs_annotations.yaml
    access_url: https://github.com/lmodel/gist/blob/main/src/gist/schema/gist_rdfs_annotations.yaml
    media_type: application/yaml
    description: "Supplementary: 96 class and 120 slot stubs carrying rdfs:label and rdfs:comment."
  - name: gist_sub_class_assertions.yaml
    access_url: https://github.com/lmodel/gist/blob/main/src/gist/schema/gist_sub_class_assertions.yaml
    media_type: application/yaml
    description: "Supplementary: 90 class stubs carrying the is_a hierarchy for OWL RL reasoners."
  - name: Documentation site
    access_url: https://lmodel.github.io/gist
    media_type: text/html
derivedFrom:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-upstream-turtle
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-cdm-mappings
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-dpvs-mappings
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-iso22989-mappings
generated:
  by: process:ktl-librarian
  at: "2026-09-29T11:22:44Z"
status: draft
---

# gist LinkML schema

`src/gist/schema/` holds six LinkML modules; `gist.yaml` is the entry point that the generators, the tests and the documentation site read. Its id is `https://w3id.org/lmodel/gist`. The prefix `gist:` binds to Semantic Arts' namespace `https://w3id.org/semanticarts/ns/ontology/gist/`, so every `class_uri` and `slot_uri` names gist's own term, and every module's default prefix is `gist_linkml:` (`https://w3id.org/lmodel/gist/`), which holds only what the rendering adds: the `GistThing` mixin, the enums and the subsets ([gist namespace policy](../policies/gist-namespace-policy.md)). The two supplementary modules, `gist_rdfs_annotations.yaml` and `gist_sub_class_assertions.yaml`, are not imported by `gist.yaml`; they exist for annotation enrichment and OWL RL reasoner support.

The modules are generated, not hand-written. The [gist-to-LinkML transform](../services/gist-to-linkml.md) rewrites them from the [upstream Turtle](gist-upstream-turtle.md), and the [SSSOM overlay](../services/apply-sssom-overlay.md) then merges the three curated mapping sets into their `*_mappings` slots. Because `just gen-project` runs both first, an edit made directly in `src/gist/schema/` is lost on the next build, although the copier-template README still says to edit this folder. Change the transform script or a mapping TSV instead ([Regenerate the schema](../playbooks/regenerate-schema.md)).
