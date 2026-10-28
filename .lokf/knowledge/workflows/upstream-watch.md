---
type: GhaWorkflow
id: https://w3id.org/lmodel/github-actions/knowledge/workflows/upstream-watch
genre: reference
title: Upstream watch (upstream-watch.yaml)
description: "The Upstream watch workflow, .github/workflows/upstream-watch.yaml: every Monday at 07:00 UTC and by hand, it runs scripts/check_upstream_release.py against SchemaStore and GitHub's REST API versions, and on a finding opens or updates the issue titled Upstream watch: SchemaStore or the REST API version has moved."
resource: .github/workflows/upstream-watch.yaml
workflow_path: .github/workflows/upstream-watch.yaml
triggers:
  - schedule
  - workflow_dispatch
permissions:
  - "{}"
jobs:
  - job_id: schemastore
    job_name: SchemaStore copy and REST API version are current
    runs_on:
      - ubuntu-latest
    job_permissions:
      - "contents: read"
      - "issues: write"
relatedTo:
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/schemastore-copy
  - https://w3id.org/lmodel/github-actions/knowledge/references/rest-api-rules
sources:
  - id: upstream-watch.yaml
    resource: .github/workflows/upstream-watch.yaml
    title: the header comment, the on key and the schemastore job
  - id: report-issue.sh
    resource: .github/scripts/report-issue.sh
    title: the issue body and the reuse of an open issue
  - resource: scripts/check_upstream_release.py
    title: the checks it makes
generated:
  by: process:ktl-librarian
  at: "2026-10-28T19:53:06Z"
  revision: 9c3541e73cc92d04fdb429a1b340eeeccdae2d37
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T21:21:37Z"
---

# Upstream watch (upstream-watch.yaml)

`.github/workflows/upstream-watch.yaml` is the workflow named "Upstream watch". A header comment says that it checks weekly what the repository is built from but does not control: SchemaStore's workflow and action schemas and GitHub's REST API versions.[^upstream-watch.yaml] Nothing in a pull request can change them, so it runs on a schedule: every Monday at 07:00 UTC, after the knowledge workflows, and by hand.

Its one job, `schemastore`, named "SchemaStore copy and REST API version are current", runs on `ubuntu-latest` with `contents: read` and `issues: write`. It runs `scripts/check_upstream_release.py` with the job's token, using only Python's standard library, so the runner's Python is enough. When the check fails, `.github/scripts/report-issue.sh` opens an issue titled "Upstream watch: SchemaStore or the REST API version has moved", or comments on the open issue with that title. The body is the check's report and a link to the run.[^report-issue.sh] So a weekly finding is one issue, and it does not depend on anyone reading the run log.

[SchemaStore copy](../datasets/schemastore-copy.md) says what the script compares, and [Move the upstream pins](../playbooks/update-upstream-pins.md) says what to do about the issue.

[^upstream-watch.yaml]: .github/workflows/upstream-watch.yaml, the header comment, the on key and the schemastore job
[^report-issue.sh]: .github/scripts/report-issue.sh, the header comment and the body it writes
