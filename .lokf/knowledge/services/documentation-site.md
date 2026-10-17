---
type: Service
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/services/documentation-site
title: gist documentation site
description: The MkDocs site at `https://lmodel.github.io/gist`, generated from the gist schema and deployed to GitHub Pages on every push to main.
resource: mkdocs.yml
endpoint: https://lmodel.github.io/gist
documentation: https://lmodel.github.io/gist
dependsOn:
- https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
generated:
  by: process:ktl-librarian
  at: "2026-10-17T00:13:57Z"
status: draft
verified:
- by: process:ktl-librarian
  at: "2026-10-16T23:47:53Z"
---

# Documentation site

`.github/workflows/deploy-docs.yaml` runs on every push to `main`. It runs `just gen-doc`, which writes per-element Markdown into the git-ignored `docs/elements/`, and then `mkdocs gh-deploy --force`, which publishes the site to the `gh-pages` branch. `just testdoc` builds it and serves it locally. The schema id `https://w3id.org/lmodel/gist` redirects to the site, and w3id forwards any longer path under it to the same path on the site. So this bundle's identifiers under `https://w3id.org/lmodel/gist/knowledge/` would resolve if the site ever published the bundle there.
