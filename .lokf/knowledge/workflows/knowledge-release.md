---
type: GhaWorkflow
id: https://w3id.org/lmodel/github-actions/knowledge/workflows/knowledge-release
genre: reference
title: Knowledge Release (knowledge-release.yaml)
description: "The Knowledge Release workflow, .github/workflows/knowledge-release.yaml: dispatched with a release's tag, or started by a published release once KNOWLEDGE_RELEASE_ENABLED is true, it attaches `knowledge-<tag>-<name>.zip`, the domain schema as `schema-<tag>-<name>.yaml` and the Copilot skills to the release, but only when the bundle changed since the last release that carries one."
resource: .github/workflows/knowledge-release.yaml
workflow_path: .github/workflows/knowledge-release.yaml
triggers:
  - release
  - workflow_dispatch
permissions:
  - "{}"
jobs:
  - job_id: pack
    job_name: Validate and pack the bundle (read-only)
    runs_on:
      - ubuntu-latest
    job_permissions:
      - "contents: read"
  - job_id: attach
    job_name: Attach the zip to the release (privileged)
    runs_on:
      - ubuntu-latest
    job_permissions:
      - "contents: write"
      - "id-token: write"
      - "attestations: write"
relatedTo:
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/github-actions-linkml-schema
sources:
  - id: knowledge-release.yaml
    resource: .github/workflows/knowledge-release.yaml
    title: the header comment, the on key, the compare and pack steps and the attach job
  - id: notice
    resource: NOTICE
    title: the Knowledge bundle section
  - resource: README.md
    title: the Knowledge Trust Ladder (KTL) section
  - resource: CONTRIBUTING.md
    title: the item on the release in Releasing (maintainers)
generated:
  by: process:ktl-librarian
  at: "2026-10-28T20:03:46Z"
  revision: 6f80b089fc284228e011ec51ab45e26d333f68f0
status: draft
---

# Knowledge Release (knowledge-release.yaml)

`.github/workflows/knowledge-release.yaml` is the workflow named "Knowledge Release". It attaches the knowledge bundle to a GitHub release as a zip file, so that a reader can take the bundle as it stood at that release without cloning the repository.[^knowledge-release.yaml] Beside it go the domain schema and, when `.lokf/m365/` is installed, the Microsoft 365 Copilot skills. It runs no LLM or agent, and it never commits or pushes. NOTICE says that it is a copy of a ktl-sidecar template from the Knowledge Trust Ladder (KTL) repository.[^notice]

## How it starts

A person, or [Semantic release](semantic-release.md), dispatches it with an existing release's tag and an optional `force` input. A published release starts it too, but only once the repository variable `KNOWLEDGE_RELEASE_ENABLED` is `true`. A header comment says that GitHub starts no workflow for a release created with the default `GITHUB_TOKEN`, so a release job that makes the release that way dispatches this workflow instead.

## Its two jobs

- **`pack`**, named "Validate and pack the bundle (read-only)", runs with `contents: read`. It compares the bundle's git tree at the tag with its tree at the newest other published release that carries a bundle. When the two match and `force` is not set, the run ends with a notice and packs nothing. Otherwise it validates the bundle and its relation targets, runs the conventions script, and packs `knowledge-<tag>-<name>.zip` with its `.sha256`. `<name>` is the repository's name unless the repository variable `KNOWLEDGE_RELEASE_NAME` sets another. Because `.lokf/justfile` names a domain schema, it also packs that file as `schema-<tag>-<name>.yaml` with its `.sha256`, and one Copilot skill zip for each instructions file in `.lokf/m365/`.
- **`attach`**, named "Attach the zip to the release (privileged)", runs only when `pack` packed something, with `contents: write`, `id-token: write` and `attestations: write`. It runs no third-party packages, checks each file against its checksum, attests build provenance when the repository is public, and uploads the files to the release, replacing an earlier upload of the same name.

So the domain schema goes onto a release only when the bundle changed since the last release that carries a bundle, or when `force` is set. The README and CONTRIBUTING.md say the same, and that a release that changes only the schema needs a run by hand with `force`.

[^knowledge-release.yaml]: .github/workflows/knowledge-release.yaml, the header comment, the on key, the compare and pack steps and the attach job
[^notice]: NOTICE, the Knowledge bundle section
