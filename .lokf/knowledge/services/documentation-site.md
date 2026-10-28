---
type: Service
id: https://w3id.org/lmodel/github-actions/knowledge/services/documentation-site
genre: reference
title: github-actions documentation site
description: The Astro Starlight site in website/, built from the README, docs/, the schema's gen-doc pages, the changelog and the knowledge bundle by the Knowledge website workflow, which deploys it to GitHub Pages under lmodel.github.io/github-actions once the repository is published and KNOWLEDGE_WEBSITE_ENABLED is true; its REDIRECTS send the retired mkdocs addresses on to the new pages.
resource: website
dependsOn:
  - https://w3id.org/lmodel/github-actions/knowledge/workflows/knowledge-website
sources:
  - id: readme.md
    resource: README.md
    title: the Repository Structure section
  - id: site.config.mjs
    resource: website/site.config.mjs
    title: REPO, SITE, BASE, DOCS, REDIRECTS, CHANGELOG, SCHEMA and BROWSE
  - id: website-readme.md
    resource: website/README.md
    title: what each page comes from, previewing and editing
  - resource: NOTICE
    title: the Knowledge bundle section
generated:
  by: process:ktl-librarian
  at: "2026-10-28T19:53:06Z"
  revision: 67d51bcffa835417e6f4785bb2d9a6945a15d95f
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T20:03:46Z"
---

# github-actions documentation site

`website/` holds an Astro Starlight site, which the README describes as built from the README, `docs/`, the schema's pages and the knowledge bundle.[^readme.md] `website/site.config.mjs` names the repository `lmodel/github-actions`, the address `https://lmodel.github.io` and the base path `/github-actions`.[^site.config.mjs] So once the repository is published and the site deployed, its pages sit under `https://lmodel.github.io/github-actions/`. NOTICE says that the site derives from the ktl-website templates.

## What the pages come from

`website/README.md` says that every page comes from a file the repository already holds, so a change to the site is a change to that file:[^website-readme.md]

- each concept in `.lokf/knowledge/` becomes a page under `knowledge/`, with its trust label from `knowledge-report.sh`, its sources and its typed relations both ways, and the four files `lokf export` writes are served beside them;
- the README becomes the home page, and each page under `docs/` a page under `docs/`, except `docs/templates-linkml/`, which `site.config.mjs` leaves out;
- `CHANGELOG.md` becomes a page per release under `changelog/`, once it holds a released version;
- the schema's pages, which `gen-doc` writes into `docs/elements/`, become a page each under `schema/`.

`site.config.mjs` shows no data pages, since `BROWSE` is `null`. Its `REDIRECTS` send the addresses that the retired mkdocs site gave its pages on to the new ones: `/elements` and each `/elements/<name>` to `/schema/`, and `/about` to `/docs/about/`.

## Previewing it

Previewing needs Node.js 22.12 or later and uv. In `website/`, run `npm ci --ignore-scripts`, then `npm run dev` for a local server, or `npm run build`, which writes `dist/` and then checks every link between its pages. Both run `npm run sync` first, which runs `lokf export` from the sidecar's environment in `.lokf/` and writes the generated pages. Nothing the sync writes is committed.

## Publishing it

[Knowledge website](../workflows/knowledge-website.md) builds the site on pull requests and on the default branch, and deploys it to GitHub Pages only once the repository variable `KNOWLEDGE_WEBSITE_ENABLED` is `true`.

## Editing it

Change a page's words in the file it comes from: the README, a page under `docs/`, the schema, or a concept, which goes through the librarian and the curator like any other change to the bundle. Change the site's options in `site.config.mjs`, and its look in `src/styles/custom.css`, which is the repository's own.

[^readme.md]: README.md, the website item of Repository Structure
[^site.config.mjs]: website/site.config.mjs, REPO, SITE, BASE, DOCS, REDIRECTS, CHANGELOG, SCHEMA and BROWSE
[^website-readme.md]: website/README.md, the list of page sources, Preview it and What to edit
