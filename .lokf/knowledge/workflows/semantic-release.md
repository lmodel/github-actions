---
type: GhaWorkflow
id: https://w3id.org/lmodel/github-actions/knowledge/workflows/semantic-release
genre: reference
title: Semantic release (semantic-release.yml)
description: "The Semantic release workflow, .github/workflows/semantic-release.yml: on a pull request into main, its plan job checks that the commits, the changelog and the title would release and previews the release; on a push to main, its release job in the release Environment tags vX.Y.Z, publishes the GitHub Release and dispatches Knowledge Release."
resource: .github/workflows/semantic-release.yml
workflow_path: .github/workflows/semantic-release.yml
triggers:
  - pull_request
  - push
permissions:
  - "{}"
jobs:
  - job_id: plan
    runs_on:
      - ubuntu-latest
    job_permissions:
      - "contents: read"
  - job_id: release
    runs_on:
      - ubuntu-latest
    job_permissions:
      - "contents: write"
      - "actions: write"
relatedTo:
  - https://w3id.org/lmodel/github-actions/knowledge/workflows/knowledge-release
sources:
  - id: semantic-release.yml
    resource: .github/workflows/semantic-release.yml
    title: the header comment, the on key and both jobs
  - resource: .releaserc.json
    title: the plugins and release rules
  - resource: .github/scripts/changelog-release.mjs
    title: the three commands
generated:
  by: process:ktl-librarian
  at: "2026-10-28T19:53:06Z"
  revision: 9e5861ab5d13ea0b34600f4339557226b1dddc15
status: draft
---

# Semantic release (semantic-release.yml)

`.github/workflows/semantic-release.yml` is the workflow named "Semantic release". It computes the next version from Conventional Commits on `main`, promotes `CHANGELOG.md`'s Unreleased section into a dated heading, tags the commit and publishes a GitHub Release built from the same text.[^semantic-release.yml] It runs on a pull request into `main` that is opened, synchronized, reopened or edited, and on a push to `main`. No file carries the version, so `CHANGELOG.md` is the only file it commits.

## The plan job, on a pull request

The `plan` job has `contents: read` and writes nothing. It installs pinned semantic-release packages with `--ignore-scripts`, and decides whether the commits would release: a `feat`, `fix` or `security` commit, or one marked breaking. When they would, it refuses to go on without a `v*` tag, refuses an empty Unreleased section, and refuses a pull request title without a releasing type, since a squash merge takes its subject from the title. Last, it previews the release with `semantic-release --dry-run`. A comment says that the `edited` type is there so that retitling a pull request reruns the title check.

## The release job, on a push to main

The `release` job runs in the `release` GitHub Environment with `contents: write` and `actions: write`. It refuses to run without a `v*` tag, then runs semantic-release, committing as `github-actions[bot]`. Once a version is released and the repository variable `KNOWLEDGE_RELEASE_ENABLED` is `true`, it dispatches [Knowledge Release](knowledge-release.md) for the new tag. A comment says that GitHub starts no workflow from a release made with the job's `GITHUB_TOKEN`, so the dispatch is how the knowledge release runs.

A header comment asks that required reviewers be configured on the `release` Environment in the repository's settings, or every qualifying merge to `main` cuts a release with no human step. [Release the schema](../playbooks/release.md) gives the whole procedure.

[^semantic-release.yml]: .github/workflows/semantic-release.yml, the header comment, the on key and both jobs
