---
type: Service
genre: reference
id: https://w3id.org/lmodel/gist/knowledge/services/documentation-site
title: gist documentation site
description: The Hugo site at `https://lmodel.github.io/gist`, built from the README, `docs/`, the schema's generated pages and this knowledge bundle, and deployed to GitHub Pages by the Knowledge website workflow.
resource: website/README.md
endpoint: https://lmodel.github.io/gist
documentation: https://lmodel.github.io/gist
dependsOn:
  - https://w3id.org/lmodel/gist/knowledge/datasets/gist-linkml-schema
generated:
  by: process:ktl-librarian
  at: "2026-11-15T03:04:36Z"
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-27T14:09:11Z"
sources:
  - resource: website/README.md
  - resource: website/site.toml
    title: the site's address, title and redirects
  - resource: website/hugo.toml
    title: docsExclude
  - resource: website/scripts/prepare.sh
  - resource: website/content/_content.gotmpl
    title: the redirects
  - resource: .github/workflows/knowledge-website.yaml
---

# Documentation site

The site is the Hugo project in `website/`. `.github/workflows/knowledge-website.yaml` builds it on every push to `main` and every pull request that touches one of its sources, on Mondays at 05:23 UTC, and when a person runs it. Its `deploy` job publishes the build to GitHub Pages only when the repository variable `KNOWLEDGE_WEBSITE_ENABLED` is `true`, and never from a pull request.

## What each page comes from

- The README becomes the home page, and each page under `docs/` a page under `docs/`. `website/hugo.toml` leaves out `docs/templates-linkml/` and `docs/elements/`. The home page has the five buttons every site has: the schema, the bundle, the architecture page, the glossary and the quick start. A button whose page is not there is greyed.
- `CHANGELOG.md` becomes a page per release under `changelog/`.
- The schema's pages become a page each under `schema/`. `website/scripts/prepare.sh` runs LinkML's `gen-doc` on `src/gist/schema/gist.yaml` and writes the pages into `website/generated/`, which is never committed.
- Each concept in `.lokf/knowledge/` becomes a page under `knowledge/`, with its trust label, its sources and its typed relations both ways. The four files `lokf export` writes are served under `knowledge/` too.

Old addresses keep working. `/elements/` and each `/elements/<name>/`, the addresses mkdocs gave the schema's pages, lead to the schema's overview and to each element's page, with no setting. `website/site.toml` sends `/about/` to the page built from `docs/about.md`, and each `/schema/<name>/` address to that element's page.

## Preview it

With bash, git and uv, run `scripts/build.sh` in `website/` to write `dist/` with its search index and check every link between its pages, or `scripts/build.sh serve` to serve the site at `http://localhost:1313/gist/`, rebuilt as you edit. Hugo and Pagefind come from PyPI, at the versions `website/pyproject.toml` names and the hashes `website/uv.lock` holds.

## Identifiers

The schema id `https://w3id.org/lmodel/gist` redirects to the site, and w3id forwards any longer path under it to the same path on the site. So this bundle's identifiers under `https://w3id.org/lmodel/gist/knowledge/` resolve to their pages.
