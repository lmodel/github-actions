---
type: GhaWorkflow
id: https://w3id.org/lmodel/github-actions/knowledge/workflows/lint-and-docs
genre: reference
title: Lint & docs (lint-and-docs.yaml)
description: "The Lint & docs workflow, .github/workflows/lint-and-docs.yaml: on a push to main, every pull request, a Monday 06:00 UTC schedule and by hand, four jobs run ShellCheck, actionlint, the word budgets of CONTRIBUTING.md (1000) and SECURITY.md (900), and markdownlint, lychee and codespell over the Markdown."
resource: .github/workflows/lint-and-docs.yaml
workflow_path: .github/workflows/lint-and-docs.yaml
triggers:
  - push
  - pull_request
  - schedule
  - workflow_dispatch
permissions:
  - "{}"
jobs:
  - job_id: lint-scripts
    job_name: Lint shell scripts
    runs_on:
      - ubuntu-latest
    job_permissions:
      - "contents: read"
  - job_id: lint-workflows
    job_name: Lint GitHub Actions workflows
    runs_on:
      - ubuntu-latest
    job_permissions:
      - "contents: read"
  - job_id: word-budgets
    job_name: Hold the governance files to their word budgets
    runs_on:
      - ubuntu-latest
    job_permissions:
      - "contents: read"
  - job_id: validate-markdown
    job_name: Lint Markdown & check links
    runs_on:
      - ubuntu-latest
    job_permissions:
      - "contents: read"
sources:
  - id: lint-and-docs.yaml
    resource: .github/workflows/lint-and-docs.yaml
    title: the header comment, the on key and the four jobs
  - resource: lychee.toml
    title: the exclusions and the remap
  - resource: .markdownlint-cli2.jsonc
    title: the ignores and the rules turned off
generated:
  by: process:ktl-librarian
  at: "2026-10-28T19:53:06Z"
  revision: b4742604d1fb81d991b7b46bc3cc09d6d863ba92
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T21:21:37Z"
---

# Lint & docs (lint-and-docs.yaml)

`.github/workflows/lint-and-docs.yaml` is the workflow named "Lint & docs". It runs static checks on the shell scripts, the workflows and the prose. A header comment says that it never touches the schema, the Python test suite or the knowledge bundle's semantics, which [Build and test](main.md) and [Knowledge Registrar](knowledge-registrar.md) check.[^lint-and-docs.yaml] It runs on a push to `main`, on every pull request, every Monday at 06:00 UTC to catch link rot, and by hand.

Each of its four jobs runs on `ubuntu-latest` with `contents: read`, after harden-runner in audit mode and a checkout without persisted credentials:

- **`lint-scripts`** runs ShellCheck over the whole repository.
- **`lint-workflows`** runs actionlint 1.7.12 from its container image, told to ignore the `copilot-requests` scope. A comment says that actionlint 1.7.12 predates that scope, which [Knowledge Librarian](knowledge-librarian.md) requests.
- **`word-budgets`** fails when `CONTRIBUTING.md` has more than 1000 words or `SECURITY.md` more than 900. A comment says that the first is a checklist and the second a policy, not design logs.
- **`validate-markdown`** runs markdownlint-cli2 on every Markdown file against `.markdownlint-cli2.jsonc`, checks links with lychee against `lychee.toml`, and runs codespell 2.4.2 on the Markdown files git tracks. The lychee step maps the repository's own links on `main` to the checkout, so a pull request that moves a linked file fails here rather than after merge.

`lychee.toml` reads the hidden folders too, so the links in `.lokf/knowledge/` are checked like the README's.

[^lint-and-docs.yaml]: .github/workflows/lint-and-docs.yaml, the header comment, the on key and the four jobs
