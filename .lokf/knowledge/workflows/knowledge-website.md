---
type: GhaWorkflow
id: https://w3id.org/lmodel/github-actions/knowledge/workflows/knowledge-website
genre: reference
title: Knowledge website (knowledge-website.yaml)
description: "The Knowledge website workflow, .github/workflows/knowledge-website.yaml: on pushes and pull requests that touch the site's sources, every Monday at 05:23 UTC and by hand, its build job builds website/ and checks its links read-only, and its deploy job publishes the default branch's build to GitHub Pages once KNOWLEDGE_WEBSITE_ENABLED is true."
resource: .github/workflows/knowledge-website.yaml
workflow_path: .github/workflows/knowledge-website.yaml
triggers:
  - push
  - pull_request
  - schedule
  - workflow_dispatch
permissions:
  - "{}"
jobs:
  - job_id: build
    job_name: Build the site (read-only)
    runs_on:
      - ubuntu-latest
    job_permissions:
      - "contents: read"
  - job_id: deploy
    job_name: Deploy to GitHub Pages
    runs_on:
      - ubuntu-latest
    job_permissions:
      - "pages: write"
      - "id-token: write"
sources:
  - id: knowledge-website.yaml
    resource: .github/workflows/knowledge-website.yaml
    title: the header comment, the on key and both jobs
  - id: notice
    resource: NOTICE
    title: the Knowledge bundle section
generated:
  by: process:ktl-librarian
  at: "2026-11-15T03:06:55Z"
status: draft
---

# Knowledge website (knowledge-website.yaml)

`.github/workflows/knowledge-website.yaml` is the workflow named "Knowledge website". It builds the site in `website/` and publishes the default branch's build to GitHub Pages.[^knowledge-website.yaml] NOTICE says that it derives from the ktl-website templates of the Knowledge Trust Ladder (KTL) repository.[^notice]

It runs on a push or a pull request that touches `website/`, `ktl-website/`, `.lokf/`, `knowledge_bundle/`, the README, `docs/`, `.assets/`, the changelog, `.linkml/`, a schema under `src/*/schema/`, the workflow itself or `knowledge-federation.yaml`. It also runs every Monday at 05:23 UTC and by hand. A header comment says that the weekly run rebuilds the site from the default branch, to catch a change that no push to those paths brings, such as the changelog's promotion, whose commit skips CI.

- **`build`**, named "Build the site (read-only)", runs with `contents: read`. A push builds on the default branch only, and a pull request or a dispatch always builds. It checks the repository out with its full history and sets up uv. It finds the site's folder: `ktl-website/` when it holds a `site.toml`, else `website/`. It installs just when `site.toml` builds the site's data with it. It then runs the site's `scripts/build.sh`, which runs `lokf export` and, for a LinkML schema, gen-doc, then builds the site with Hugo and Pagefind from the site's own `uv.lock`, cleans its raw HTML and checks its links. It uploads the site's `dist/` as the Pages artifact.
- **`deploy`**, named "Deploy to GitHub Pages", holds `pages: write` and `id-token: write`, and runs only harden-runner and GitHub's own deploy-pages action. It runs for the default branch once the repository variable `KNOWLEDGE_WEBSITE_ENABLED` is `true`. Until then the workflow builds but deploys nothing.

A header comment says to tell Pages once to take its site from Actions before setting the variable, and to keep the variable unset while another publisher still deploys Pages, since two publishers overwrite each other's site. [github-actions documentation site](../services/documentation-site.md) describes the site.

[^knowledge-website.yaml]: .github/workflows/knowledge-website.yaml, the header comment, the on key and both jobs
[^notice]: NOTICE, the Knowledge bundle section
