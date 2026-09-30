## Add your own just recipes here. This is imported by the main justfile.

# Overriding recipes from the root justfile by adding a recipe with the same
# name in this file is not possible until a known issue in just is fixed,
# https://github.com/casey/just/issues/2540

# Generate LinkML schema YAMLs from the upstream GIST OWL/Turtle ontology files.
# Reads upstream/gist14.1.0_webDownload/ontologies/turtle/*.ttl and writes to src/gist/schema/.
# Build order: `gen-linkml` -> `apply-sssom-overlay` -> `gen-project`.
[group('model development')]
gen-linkml:
  uv run python scripts/gist_to_linkml.py

# Apply curated SSSOM mapping TSVs to the generated LinkML schema YAMLs.
# Merges SKOS exact/close/broad/narrow/related matches into the matching
# class / enum / type bodies and declares any referenced object-side prefixes.
# Idempotent: re-running on a clean tree produces no further changes.
[group('model development')]
apply-sssom-overlay: gen-linkml
  uv run python scripts/apply_sssom_overlay.py \
    --schema-dir src/gist/schema \
    --mappings-dir src/gist/mappings

# Verify the mappings were applied correctly to LinkML files.
[group('model development')]
verify-mappings: apply-sssom-overlay
  uv run python scripts/verify_mappings.py

# Fetches each target's schema folder at the commit pinned in
# scripts/verify_mapping_targets.py; needs git and network. `just --list`
# shows a recipe's last comment line, so the summary comes last.
# Check every SSSOM object term exists in its target schema
[group('model development')]
verify-mapping-targets:
  uv run python scripts/verify_mapping_targets.py

# Compares by content, ignoring generation dates and Turtle triple order,
# and puts the committed files back afterwards.
# Check the committed project/ and datamodel artefacts match a fresh gen-project
[group('model development')]
verify-generated:
  uv run python scripts/check_generated_current.py

# The lokf toolkit the .lokf sidecar locks. To try another, override it:
# just lokf="uv run --project .lokf --with ../lokf lokf" gen-lokf-copy
lokf := "uv run --project .lokf lokf"

# Writes <out>/gist_core_lokf.yaml: gist_core.yaml through `lokf adapt`, which
# renames each name lokf.yaml also defines (Person, name, ...) with its gist
# IRI kept, and re-roots gist's top classes on LOKF's Concept, so a bundle
# writes `type: Requirement` and a relation names its target by IRI. `Any`,
# the range of an object property gist leaves open, stays out. adapt verifies
# the copy against the lokf.yaml the .lokf sidecar locks and fails on a problem.
# lokf-copy-release.yaml attaches it to each release.
# Build gist_core.yaml adapted to import beside LOKF's lokf.yaml
[group('model development')]
gen-lokf-copy out="dist/lokf":
  mkdir -p "{{out}}"
  {{lokf}} adapt src/gist/schema/gist_core.yaml -o "{{out}}/gist_core_lokf.yaml" --prefix gist \
    $(uv run python -c 'import yaml; c = yaml.safe_load(open("src/gist/schema/gist_core.yaml"))["classes"]; print(" ".join(f"--root {n}" for n, v in c.items() if not v.get("is_a") and not v.get("mixin") and v.get("class_uri") != "linkml:Any"))')

# Needs network.
# Check upstream/ is Semantic Arts' latest gist release, byte for byte
[group('model development')]
check-upstream:
  uv run python scripts/check_upstream_release.py
