---
type: Dataset
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
title: gist LinkML schema
description: LinkML rendering of gist 14.1.0 (schema id `https://w3id.org/lmodel/gist`), generated from the upstream Turtle modules with the curated SSSOM mappings overlaid.
resource: src/gist/schema/gist.yaml
version: 14.1.0
license: https://creativecommons.org/licenses/by/4.0/
distribution:
  - name: gist.yaml
    access_url: https://github.com/lmodel/gist/blob/main/src/gist/schema/gist.yaml
    media_type: application/yaml
    description: Aggregator schema; imports gist_core, gist_media_types and gist_prefix_declarations.
  - name: gist_core.yaml
    access_url: https://github.com/lmodel/gist/blob/main/src/gist/schema/gist_core.yaml
    media_type: application/yaml
    description: 98 classes (gist's 96, the GistThing mixin with the 89 slots gist declares without a domain, and Any, the range of the object properties gist leaves open), 120 slots, 14 types for the datatypes linkml:types lacks, and the AspectInstance enum (8 values).
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
  at: "2026-10-27T14:09:11Z"
status: draft
sources:
  - resource: src/gist/schema/gist_core.yaml
    title: the core module, for its counts of classes, slots, types and enum values
  - resource: .linkmllint.yaml
    title: the lint rules, LinkML's recommended set less no_xsd_int_type
  - resource: docs/about.md
    title: how the classes carry gist's properties, and where the schema is stricter than gist
---

# gist LinkML schema

`src/gist/schema/` holds six LinkML modules. `gist.yaml` is the entry point that the generators, the tests and the documentation site read. Its id is `https://w3id.org/lmodel/gist`. The two supplementary modules, `gist_rdfs_annotations.yaml` and `gist_sub_class_assertions.yaml`, are not imported by `gist.yaml`. They exist for annotation enrichment and OWL RL reasoner support.

The prefix `gist:` binds to Semantic Arts' namespace `https://w3id.org/semanticarts/ns/ontology/gist/`, so every `class_uri` and `slot_uri` names gist's own term. Every module's default prefix is `gist_linkml:` (`https://w3id.org/lmodel/gist/`), which holds only what the rendering adds: the `GistThing` mixin, the types for the datatypes `linkml:types` lacks, the enums and the subsets ([gist namespace policy](../policies/gist-namespace-policy.md)).

The modules are generated, not hand-written. The [gist-to-LinkML transform](../services/gist-to-linkml.md) rewrites them from the [upstream Turtle](gist-upstream-turtle.md), and the [SSSOM overlay](../services/apply-sssom-overlay.md) then merges the three curated mapping sets into their `*_mappings` slots. `just gen-project` runs both first, so an edit made directly in `src/gist/schema/` is lost on the next build. The copier-template README still says to edit this folder: change the transform script or a mapping TSV instead ([Regenerate the schema](../playbooks/regenerate-schema.md)).

Each class carries the slot of every property whose `rdfs:domain` names it or one of its superclasses. Through the `GistThing` mixin, it also carries the 89 slots of the properties gist declares without a domain. `docs/about.md` says where the schema checks data more strictly than gist's OWL.

`just lint` checks the modules with LinkML's recommended rules, less one. `.linkmllint.yaml` turns off `no_xsd_int_type`, because gist allows `xsd:int` literals, and a type with that IRI keeps them valid in the SHACL shapes.
