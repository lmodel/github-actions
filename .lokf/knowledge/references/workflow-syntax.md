---
type: Reference
id: https://w3id.org/lmodel/github-actions/knowledge/references/workflow-syntax
genre: reference
title: GitHub workflow syntax
description: "GitHub's workflow syntax page for GitHub Actions, with its companion page on reusable workflows: the source of GhaWorkflow, GhaWorkflowJob, GhaReusableWorkflow and the gha_permission type, versionless, read on 2026-10-28 and cited, never copied, under CC BY 4.0."
resource: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
sources:
  - id: readme.md
    resource: README.md
    title: the What it models section and its paragraph on the reading date
  - id: github_actions_workflow.yaml
    resource: src/github_actions/schema/github_actions_workflow.yaml
    title: the see_also entries
  - id: notice
    resource: NOTICE
    title: the paragraph on GitHub's documentation
  - resource: AI_COVENANT.md
    title: the note specific to this project
generated:
  by: process:ktl-librarian
  at: "2026-10-28T21:21:37Z"
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T20:03:46Z"
---

# GitHub workflow syntax

The README says that `GhaWorkflow` comes from GitHub's [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) page, and `GhaReusableWorkflow` from that page and the [reusable workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations) page.[^readme.md]

The workflow module cites sections of the page in `see_also`: `jobs`, a job's `name`, `uses`, `runs-on` and `permissions`, choosing runners in a group, the top-level `permissions`, and `on.workflow_call` with its inputs, their `type`, its outputs and its secrets.[^github_actions_workflow.yaml] The `triggers` slot cites GitHub's companion page on the events that trigger workflows.

GitHub's pages are versionless, so the schema's `version` is the date they were read, 2026-10-28. NOTICE says that GitHub's documentation is licensed under the Creative Commons Attribution 4.0 International license (CC BY 4.0), and that the schema renders it in the project's own words with each page cited by address.[^notice] AI_COVENANT.md says that the documentation is cited, never copied.

[^readme.md]: README.md, the What it models section and its paragraph on the reading date
[^github_actions_workflow.yaml]: src/github_actions/schema/github_actions_workflow.yaml, the see_also entries
[^notice]: NOTICE, the paragraph on GitHub's documentation
