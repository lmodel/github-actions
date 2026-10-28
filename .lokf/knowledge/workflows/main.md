---
type: GhaWorkflow
id: https://w3id.org/lmodel/github-actions/knowledge/workflows/main
genre: reference
title: Build and test (main.yaml)
description: "The Build and test workflow, .github/workflows/main.yaml: on a push to main and on every pull request, its test job runs just test on Python 3.10 to 3.14, and on 3.13 also just lint and the check that .lokf/github-actions.yaml is current."
resource: .github/workflows/main.yaml
workflow_path: .github/workflows/main.yaml
triggers:
  - push
  - pull_request
permissions:
  - "{}"
jobs:
  - job_id: test
    runs_on:
      - ubuntu-latest
    job_permissions:
      - "contents: read"
relatedTo:
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/test-data
sources:
  - id: main.yaml
    resource: .github/workflows/main.yaml
    title: the on key, the concurrency group and the test job
generated:
  by: process:ktl-librarian
  at: "2026-10-28T19:53:06Z"
  revision: 3c6aabc4cfb8758627880b26002dba6dd7781a1d
status: draft
---

# Build and test (main.yaml)

`.github/workflows/main.yaml` is the workflow named "Build and test". It runs on a push to `main` and on every pull request, and a newer run on the same ref cancels an older one.[^main.yaml] The file sets `permissions: {}` at the top, and its one job asks for `contents: read`. A comment says that it was built from GitHub's guide to building and testing Python.

## The test job

The `test` job runs on `ubuntu-latest` once for each Python version from 3.10 to 3.14, and a failure on one version does not stop the others. It hardens the runner with harden-runner in audit mode, checks the repository out without persisting credentials, installs uv, Python and just, and installs the project with `uv sync --locked --group dev`. It then runs:

- `just lint`, on Python 3.13 only;
- `just test`, on every version;
- `uv sync --locked --project .lokf` and `just lokf-adapt-check`, on Python 3.13 only. A comment says that `.lokf/github-actions.yaml` is the copy the knowledge bundle validates against and the release attaches, so it must match the schema and `lokf.yaml`.

The job has no `name`. Under the naming rule in [Required status check](../glossary/required-status-check.md), each of its runs reports a check named after the job's id and its Python version, such as `test (3.13)`. [Regenerate and test the schema](../playbooks/regenerate-and-test.md) says what each recipe runs.

[^main.yaml]: .github/workflows/main.yaml, the on key, the concurrency group and the test job
