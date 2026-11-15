---
type: Service
id: https://w3id.org/lmodel/github-actions/knowledge/services/documentation-site
genre: reference
title: github-actions documentation site
description: The Hugo site in website/, built from the README, docs/, the schema's gen-doc pages, the changelog and the knowledge bundle by the Knowledge website workflow, which deploys it to GitHub Pages under lmodel.github.io/github-actions when KNOWLEDGE_WEBSITE_ENABLED is true; its REDIRECTS send the retired mkdocs addresses on to the new pages.
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
  - resource: NOTICE
    title: the Knowledge bundle section
generated:
  by: process:ktl-librarian
  at: "2026-11-15T02:57:18Z"
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
- the README becomes the home page, and each page under `docs/` a page under `docs/`, except `docs/templates-linkml/`, which `site.toml` leaves out;
- `CHANGELOG.md` becomes a page per release under `changelog/`;
- the schema's pages, which `gen-doc` writes into `docs/elements/`, become a page each under `schema/`.

`site.toml` shows no data pages, since `BROWSE` is `null`. Its `REDIRECTS` send the addresses that the retired mkdocs site gave its pages on to the new ones: `/elements` and each `/elements/<name>` to `/schema/`, and `/about` to `/docs/about/`.

## Previewing it

Previewing needs Node.js 22.12 or later and uv. In `website/`, run `npm ci --ignore-scripts`, then `npm run dev` for a local server, or `npm run build`, which writes `dist/` and then checks every link between its pages. Both run `npm run sync` first, which runs `lokf export` from the sidecar's environment in `.lokf/` and writes the generated pages. Nothing the sync writes is committed.

## Publishing it

[Knowledge website](../workflows/knowledge-website.md) builds the site on pull requests and on the default branch, and deploys it to GitHub Pages only once the repository variable `KNOWLEDGE_WEBSITE_ENABLED` is `true`.

## Editing it

Change a page's words in the file it comes from: the README, a page under `docs/`, the schema, or a concept, which goes through the librarian and the curator like any other change to the bundle. Change the site's options in `site.toml`, and its look in `src/styles/custom.css`, which is the repository's own.

[^readme.md]: README.md, the website item of Repository Structure
[^site.toml]: website/site.toml, the site's address, title and redirects
[^website-readme.md]: website/README.md, the list of page sources, Preview it and What to edit
