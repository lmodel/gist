# Change Log

## 2026-09-29

* **Namespace policy**: Added `policies/gist-namespace-policy.md`, recording Semantic Arts' two namespace conditions and the converter, generator flags and tests that hold them.
* **Namespace refresh**: `gist:` now names Semantic Arts' namespace and this project's additions use `gist_linkml:`, so the claims in `references/gist-ontology`, `datasets/gist-linkml-schema`, `datasets/generated-artefacts` and `services/gist-to-linkml` were corrected; the transform is now deterministic.
* **Mapping tools and release**: The overlay and verifier match subjects by IRI, and the distribution is `lmodel-gist`, which answers the release playbook's open question. The source map and test counts follow.
* **Bootstrap discovery**: Replaced the two placeholder services with 21 concepts derived from the repository: the upstream gist release, the LinkML schema, three SSSOM mapping sets and their object schemas, the transform, overlay and verifier scripts, generated artefacts, test data, the documentation site, and the regenerate and release playbooks.
* **Source map**: Recorded `playbooks/knowledge-sources.md`, the map every later refresh re-verifies against.
* **Initialization**: Scaffolded the LOKF bundle for gist with placeholder
  services. Real concepts to follow.
