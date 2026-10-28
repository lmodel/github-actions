---
type: Reference
id: https://w3id.org/lmodel/github-actions/knowledge/references/metadata-syntax
genre: reference
title: GitHub metadata syntax
description: "GitHub's metadata syntax page for an action's action.yml or action.yaml: the source of GhaAction, its inputs and outputs and the runtimes runs.using may name (composite, docker, node20, node24), versionless, read on 2026-10-28 and cited, never copied, under CC BY 4.0."
resource: https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax
sources:
  - id: readme.md
    resource: README.md
    title: the What it models section and its paragraph on the reading date
  - id: github_actions_action.yaml
    resource: src/github_actions/schema/github_actions_action.yaml
    title: the see_also entries and the GhaActionRuntime comment
  - resource: NOTICE
    title: the paragraph on GitHub's documentation
generated:
  by: process:ktl-librarian
  at: "2026-10-28T21:21:37Z"
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T20:03:46Z"
---

# GitHub metadata syntax

The README says that `GhaAction` comes from GitHub's [metadata syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax) page: the inputs and outputs of an `action.yml`, and the runtime names that `runs.using` takes.[^readme.md]

The action module cites sections of the page in `see_also`: `inputs`, an input's `deprecationMessage`, the outputs of Docker container and JavaScript actions, the outputs of composite actions, and `runs` for composite, JavaScript and Docker container actions.[^github_actions_action.yaml] The `GhaActionRuntime` enum holds `composite`, `docker`, `node20` and `node24`. Its comment says that SchemaStore's schema at the pinned commit also accepts `node12` and `node16`, which the page no longer lists.

The page is versionless, so the schema's `version` is the date it was read, 2026-10-28. NOTICE says that GitHub's documentation is licensed under CC BY 4.0, and that the schema renders it in the project's own words with each page cited by address.

[^readme.md]: README.md, the What it models section and its paragraph on the reading date
[^github_actions_action.yaml]: src/github_actions/schema/github_actions_action.yaml, the see_also entries and the GhaActionRuntime comment
