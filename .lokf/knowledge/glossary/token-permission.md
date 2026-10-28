---
type: GlossaryTerm
id: https://w3id.org/lmodel/github-actions/knowledge/glossary/token-permission
genre: reference
title: GITHUB_TOKEN permission
definition: One grant of access to a workflow's GITHUB_TOKEN, written as a scope, a colon and read, write or none, or as one of the shorthands read-all, write-all and {}.
description: "One grant of access to a workflow's GITHUB_TOKEN, such as contents: read, or the shorthand read-all, write-all or {}; the schema's gha_permission type, used by a workflow's permissions and a job's job_permissions, and what this repository's workflows grant."
resource: src/github_actions/schema/github_actions_workflow.yaml
definedBy:
  - https://w3id.org/lmodel/github-actions/knowledge/references/workflow-syntax
sources:
  - id: github_actions_workflow.yaml
    resource: src/github_actions/schema/github_actions_workflow.yaml
    title: the gha_permission type, permissions and job_permissions
  - id: docs-index.md
    resource: docs/index.md
    title: the Validating data section
  - id: security.md
    resource: SECURITY.md
    title: the paragraph after the table
  - resource: tests/test_schema_rules.py
    title: the permission pattern test
generated:
  by: process:ktl-librarian
  at: "2026-10-28T19:53:06Z"
  revision: 4e47f1efc96b84011e7016edd847a71bfc692a33
status: draft
---

# GITHUB_TOKEN permission

The workflow module's `gha_permission` type is one grant of access to a workflow's `GITHUB_TOKEN`. It is written as the scope, a colon and `read`, `write` or `none`, such as `contents: read`. The shorthands `read-all` and `write-all`, and `{}` for the empty map, stand alone.[^github_actions_workflow.yaml] The type is a pattern rather than an enumeration of scopes, because GitHub adds scopes. `tests/test_schema_rules.py` checks that it admits every scope that SchemaStore's schema lists at the pinned commit.

## Where it is used

- A workflow's `permissions` records the grants of the file's top-level `permissions` key, which apply to every job's token. It is absent when the file sets none, and then the repository's or organization's default applies. A scope that the map leaves out gets no access.
- A job's `job_permissions` records the grants of the job's own `permissions` key, which replace the workflow's for that job. A called workflow can lower its token's access, never raise it.

## What no tool checks

`docs/index.md` says that no tool checks that `read-all`, `write-all` or `{}` stands alone in a list, or that `id-token` takes `write` or `none`, never `read`. It adds that the Pydantic models do not check the type's pattern, and that `linkml-validate` accepts a permission followed by one line break.[^docs-index.md]

## In this repository

SECURITY.md says that every workflow declares `permissions: {}` at the top.[^security.md] Each job then asks for the scopes it needs, which the concepts under `workflows/` record.

[^github_actions_workflow.yaml]: src/github_actions/schema/github_actions_workflow.yaml, gha_permission, permissions and job_permissions
[^docs-index.md]: docs/index.md, the Validating data section
[^security.md]: SECURITY.md, the paragraph after the table
