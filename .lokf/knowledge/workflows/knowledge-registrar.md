---
type: GhaWorkflow
id: https://w3id.org/lmodel/github-actions/knowledge/workflows/knowledge-registrar
genre: reference
title: Knowledge Registrar (knowledge-registrar.yaml)
description: "The Knowledge Registrar workflow, .github/workflows/knowledge-registrar.yaml: the gate on the knowledge bundle, run on pull requests that touch .lokf/, every Monday at 06:00 UTC and by hand; it validates the bundle and its relation targets, runs the conventions script, and checks that each new confirmation by a person is backed by an approval or a signed commit."
resource: .github/workflows/knowledge-registrar.yaml
workflow_path: .github/workflows/knowledge-registrar.yaml
triggers:
  - pull_request
  - schedule
  - workflow_dispatch
permissions:
  - "{}"
jobs:
  - job_id: validate
    job_name: Validate the LOKF bundle
    runs_on:
      - ubuntu-latest
    job_permissions:
      - "contents: read"
  - job_id: provenance
    job_name: Check new human confirmations
    runs_on:
      - ubuntu-latest
    job_permissions:
      - "contents: read"
      - "pull-requests: read"
  - job_id: attestation
    job_name: Attest to an unbacked confirmation
    runs_on:
      - ubuntu-latest
    job_permissions:
      - "{}"
sources:
  - id: knowledge-registrar.yaml
    resource: .github/workflows/knowledge-registrar.yaml
    title: the header comment, the on key and the three jobs
  - id: notice
    resource: NOTICE
    title: the Knowledge bundle section
  - resource: CONTRIBUTING.md
    title: the item on knowledge-bundle changes
generated:
  by: process:ktl-librarian
  at: "2026-10-28T19:53:06Z"
  revision: 6f80b089fc284228e011ec51ab45e26d333f68f0
status: draft
---

# Knowledge Registrar (knowledge-registrar.yaml)

`.github/workflows/knowledge-registrar.yaml` is the workflow named "Knowledge Registrar". A header comment says that it keeps the knowledge bundle's records well formed and provenanced, and never judges whether their content is true, which is the curator's job.[^knowledge-registrar.yaml] NOTICE says that it is a copy of a ktl-sidecar template from the Knowledge Trust Ladder (KTL) repository.[^notice] It runs on a pull request that touches `.lokf/`, `knowledge_bundle/` or the workflow itself, every Monday at 06:00 UTC, and by hand.

None of its three jobs can write to the repository: each runs with a read-only token, keeps no credential on disk, and runs no LLM or agent.

- **`validate`**, named "Validate the LOKF bundle", runs every time, with `contents: read`. It runs `just lokf-check-refs`, which is `lokf validate --check-refs` with the domain schema, and then the conventions script, `.lokf/scripts/knowledge-conventions.sh`.
- **`provenance`**, named "Check new human confirmations", runs on pull requests, with `contents: read` and `pull-requests: read`. For each new confirmation by a person in the diff, it passes when that person approved the pull request or signed the commit, as GitHub reports it, and otherwise calls the confirmation unbacked. With curators' keys in `.lokf/curators/`, a second check verifies the same signatures with plain git.
- **`attestation`**, named "Attest to an unbacked confirmation", runs only for an unbacked confirmation, with no token scope. It waits until a reviewer of the Environment that the repository variable `KNOWLEDGE_CURATION_ENVIRONMENT` names approves the run, and the approval is logged with the run.

The header comment adds that the evidence is GitHub's own record of approvals and signature checks, never the pull request's text, and that the workflow does not prove that the named person read the source. CONTRIBUTING.md says that it runs on any `.lokf/**` change.

[^knowledge-registrar.yaml]: .github/workflows/knowledge-registrar.yaml, the header comment, the on key and the three jobs
[^notice]: NOTICE, the Knowledge bundle section
