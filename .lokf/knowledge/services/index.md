# Services

* [gist-to-LinkML transform](gist-to-linkml.md) - Command-line script (scripts/gist_to_linkml.py, run as just gen-linkml) that turns the gist Turtle modules into the gist LinkML schema modules, keeping each term's gist IRI.
* [SSSOM overlay](apply-sssom-overlay.md) - Command-line script (scripts/apply_sssom_overlay.py, run as just apply-sssom-overlay) that merges the curated SSSOM mappings into the gist LinkML schema.
* [Mapping verifier](verify-mappings.md) - Read-only command-line check (scripts/verify_mappings.py, run as just verify-mappings) that every SSSOM row is present on the gist LinkML schema and nothing extra is.
* [Mapping target checker](verify-mapping-targets.md) - Network command-line check (scripts/verify_mapping_targets.py, run as just verify-mapping-targets) that every SSSOM object term exists in the lmodel target schema it names, at a pinned commit.
* [Upstream watch](upstream-watch.md) - Weekly GitHub workflow (upstream-watch.yaml) that checks the vendored gist release is Semantic Arts' latest and intact, and that mapped target terms still exist on each target's default branch, opening an issue on failure.
* [gist documentation site](documentation-site.md) - The MkDocs site at `https://lmodel.github.io/gist`, generated from the gist schema and deployed to GitHub Pages on every push to main.
