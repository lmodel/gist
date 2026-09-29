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

# gist names that LOKF's lokf.yaml also defines. Renamed, the classes and
# slots keep their gist IRIs.
lokf_renames := "--rename Person=GistPerson --rename Organization=GistOrganization --rename name=gist_name --rename description=gist_description --rename license=gist_license"

# Writes <out>/gist_core.yaml, one self-contained file with the SSSOM
# mappings applied, then checks it shares no element name with the lokf.yaml
# the .lokf sidecar locks. lokf-copy-release.yaml attaches it to each release.
# Build gist_core.yaml renamed to import beside LOKF's lokf.yaml
[group('model development')]
gen-lokf-copy out="dist/lokf":
  rm -rf tmp/lokf-copy
  uv run python scripts/gist_to_linkml.py -d tmp/lokf-copy {{lokf_renames}}
  uv run python scripts/apply_sssom_overlay.py --schema-dir tmp/lokf-copy --mappings-dir src/gist/mappings
  mkdir -p "{{out}}"
  cp tmp/lokf-copy/gist_core.yaml "{{out}}/gist_core.yaml"
  uv run python scripts/check_lokf_names.py "{{out}}/gist_core.yaml" \
    "$(uv run --project .lokf python -c "from importlib.resources import files; print(files('lokf') / 'data' / 'lokf.yaml')")"

# Needs network.
# Check upstream/ is Semantic Arts' latest gist release, byte for byte
[group('model development')]
check-upstream:
  uv run python scripts/check_upstream_release.py
