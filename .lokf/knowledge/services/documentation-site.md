---
type: Service
id: https://w3id.org/lmodel/github-actions/knowledge/services/documentation-site
genre: reference
title: github-actions documentation site
description: The Hugo site in website/, built from the README, docs/, the schema's gen-doc pages, the changelog and the knowledge bundle. The Knowledge website workflow deploys it to GitHub Pages under lmodel.github.io/github-actions once KNOWLEDGE_WEBSITE_ENABLED is true.
resource: website
dependsOn:
  - https://w3id.org/lmodel/github-actions/knowledge/workflows/knowledge-website
sources:
  - id: readme.md
    resource: README.md
    title: the Repository Structure section
  - id: site.toml
    resource: website/site.toml
    title: the site's address, title and redirects
  - id: website-readme.md
    resource: website/README.md
    title: what each page comes from, previewing and editing
  - id: hugo.toml
    resource: website/hugo.toml
    title: docsExclude
  - resource: NOTICE
    title: the Knowledge bundle section
generated:
  by: process:ktl-librarian
  at: "2026-11-15T03:06:55Z"
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T21:21:37Z"
---

# github-actions documentation site

`website/` holds a Hugo site, which the README describes as built from the README, `docs/`, the schema's pages and the knowledge bundle.[^readme.md] `website/site.toml` names the repository `lmodel/github-actions`, the address `https://lmodel.github.io` and the base path `/github-actions`.[^site.toml] So its pages are served under `https://lmodel.github.io/github-actions/`. NOTICE says that the site derives from the ktl-website templates.

## What the pages come from

`website/README.md` says that every page comes from a file the repository already holds, so a change to the site is a change to that file:[^website-readme.md]

- each concept in `.lokf/knowledge/` becomes a page under `knowledge/`, with its trust label from `knowledge-report.sh`, its sources and its typed relations both ways, and the four files `lokf export` writes are served beside them, with the bundle log as an Atom feed, `knowledge/log.xml`;
- the README becomes the home page, and each page under `docs/` a page under `docs/`;
- `CHANGELOG.md` becomes a page per release under `changelog/`;
- each class, slot, enumeration and type of the schema, which LinkML's `gen-doc` writes, becomes a page under `schema/`, also at `elements/<Name>/`, where the schema's w3id rules point.

`website/hugo.toml` leaves out `docs/templates-linkml/` and `docs/elements/`, the pages gen-doc keeps there, since the site builds the schema's pages afresh.[^hugo.toml] `site.toml` names no `browse` folder, so the site shows no data pages. It redirects `about` to the page built from `docs/about.md`, and each old address under `schema/` to the schema's page of the same name.

## Previewing it

Previewing needs bash, git and uv. In `website/`, `scripts/build.sh` writes `dist/` with the search index, then checks every link between its pages. `scripts/build.sh serve` serves the site at `http://localhost:1313/github-actions/` and rebuilds it as you edit. `scripts/build.sh preview` serves the site as it will be published, at `http://localhost:1313/`. Hugo and Pagefind come from PyPI, at the versions `website/pyproject.toml` names and the hashes `website/uv.lock` holds.

## Publishing it

[Knowledge website](../workflows/knowledge-website.md) builds the site on pull requests and on the default branch, and deploys it to GitHub Pages only once the repository variable `KNOWLEDGE_WEBSITE_ENABLED` is `true`.

## Editing it

Change a page's words in the file it comes from: the README, a page under `docs/`, the schema, or a concept, which goes through the librarian and the curator like any other change to the bundle. Change the site's own values in `site.toml`, and its look in `assets/css/custom.css`, which is the repository's own.

[^readme.md]: README.md, the website item of Repository Structure
[^site.toml]: website/site.toml, the site's address, title and redirects
[^website-readme.md]: website/README.md, the list of page sources, Preview it and What to edit
[^hugo.toml]: website/hugo.toml, docsExclude and its comment
