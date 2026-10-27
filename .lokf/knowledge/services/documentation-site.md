---
type: Service
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/services/documentation-site
title: gist documentation site
description: The Astro Starlight site at `https://lmodel.github.io/gist`, built from the README, `docs/`, the schema's generated pages and this knowledge bundle, and deployed to GitHub Pages by the Knowledge website workflow.
resource: website/README.md
endpoint: https://lmodel.github.io/gist
documentation: https://lmodel.github.io/gist
dependsOn:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
generated:
  by: process:ktl-librarian
  at: "2026-10-27T08:54:25Z"
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-27T14:09:11Z"
sources:
  - resource: website/README.md
  - resource: website/site.config.mjs
  - resource: .github/workflows/knowledge-website.yaml
  - resource: justfile
---

# Documentation site

The site is the Astro Starlight project in `website/`. `.github/workflows/knowledge-website.yaml` builds it on every push to `main` and every pull request that touches one of its sources, on Mondays at 05:23 UTC, and when a person runs it. Its `deploy` job publishes the build to GitHub Pages only when the repository variable `KNOWLEDGE_WEBSITE_ENABLED` is `true`, and never from a pull request.

## What each page comes from

- The README becomes the home page, and each page under `docs/` a page under `docs/`. `website/site.config.mjs` leaves out `docs/templates-linkml/`.
- `CHANGELOG.md` becomes a page per release under `changelog/`.
- The schema's pages become a page each under `schema/`. `just gen-doc` writes them into the git-ignored `docs/elements/`, and the build runs it when that folder is missing.
- Each concept in `.lokf/knowledge/` becomes a page under `knowledge/`, with its trust label, its sources and its typed relations both ways. The four files `lokf export` writes are served under `knowledge/` too.

`website/site.config.mjs` keeps the old site's addresses working: `/elements/` and every page under it lead to the same page under `/schema/`, and `/about` leads to `/docs/about/`.

## Preview it

With Node.js 22.12 or later and uv, run `npm ci --ignore-scripts` in `website/`, then `npm run dev` to serve the site at `http://localhost:4321/gist/`, or `npm run build` to write `dist/` and check every link between its pages.

## Identifiers

The schema id `https://w3id.org/lmodel/gist` redirects to the site, and w3id forwards any longer path under it to the same path on the site. So this bundle's identifiers under `https://w3id.org/lmodel/gist/knowledge/` resolve to their pages.
