---
type: GhaWorkflow
id: https://w3id.org/lmodel/github-actions/knowledge/workflows/knowledge-librarian
genre: reference
title: Knowledge Librarian (knowledge-librarian.yaml)
description: "The Knowledge Librarian workflow, .github/workflows/knowledge-librarian.yaml: every Monday at 05:00 UTC and by hand, once KNOWLEDGE_LIBRARIAN_ENABLED is true, it runs an LLM agent with the ktl-librarian skill (pinned by TRUST_LADDER_SKILLS_REF) in a read-only job and opens a review pull request with the bundle change from a separate privileged job."
resource: .github/workflows/knowledge-librarian.yaml
workflow_path: .github/workflows/knowledge-librarian.yaml
triggers:
  - schedule
  - workflow_dispatch
permissions:
  - "{}"
jobs:
  - job_id: earlier
    job_name: Read what became of the earlier pull requests (read-only, no agent)
    runs_on:
      - ubuntu-latest
    job_permissions:
      - "pull-requests: read"
  - job_id: refresh
    job_name: Refresh the LOKF bundle (agent, read-only)
    runs_on:
      - ubuntu-latest
    job_permissions:
      - "contents: read"
      - "copilot-requests: write"
  - job_id: publish
    job_name: Open the review PR (privileged, no agent)
    runs_on:
      - ubuntu-latest
    job_permissions:
      - "contents: write"
      - "pull-requests: write"
sources:
  - id: knowledge-librarian.yaml
    resource: .github/workflows/knowledge-librarian.yaml
    title: the header comment, the on key, the three jobs and the setup comment
  - id: notice
    resource: NOTICE
    title: the Knowledge bundle section
  - id: changelog.md
    resource: CHANGELOG.md
    title: the item on the knowledge bundle
  - resource: CONTRIBUTING.md
    title: the item on the skills pin
generated:
  by: process:ktl-librarian
  at: "2026-10-28T20:03:46Z"
  revision: 6f80b089fc284228e011ec51ab45e26d333f68f0
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T22:46:12Z"
---

# Knowledge Librarian (knowledge-librarian.yaml)

`.github/workflows/knowledge-librarian.yaml` is the workflow named "Knowledge Librarian". A header comment says that it runs an LLM librarian that keeps `.lokf/` in step with the repository and opens a review pull request with whatever changed.[^knowledge-librarian.yaml] It never pushes to the default branch and never merges. It runs every Monday at 05:00 UTC and by hand, and it is inert until the repository variable `KNOWLEDGE_LIBRARIAN_ENABLED` is `true`. NOTICE says that it is a copy of a ktl-sidecar template from the Knowledge Trust Ladder (KTL) repository.[^notice]

## Its three jobs

- **`earlier`** reads what became of the pull requests the workflow opened before, with `pull-requests: read` only and no agent. While one is still open, a scheduled run opens no second one, and it does not propose again what a person declined by closing one without merging.
- **`refresh`** runs the agent under a read-only token with no git credentials on disk, with `contents: read` and `copilot-requests: write`, in the `knowledge-librarian` Environment. It installs the ktl-librarian skill from the tag that `TRUST_LADDER_SKILLS_REF` names, `v0.57.0`, and stops unless that tag names the commit `TRUST_LADDER_SKILLS_SHA` gives, `e7ec838780e9bc436970055a3cd5a5695015def6`. A check after the run fails if the agent wrote anything but `.lokf/patch.yaml`, which the wrapper `.lokf/scripts/knowledge-librarian.sh` then applies.
- **`publish`** holds `contents: write` and `pull-requests: write`, runs no agent code, and pushes the branch and opens the pull request when `refresh` changed something.

## Settings it reads

The agent command comes from repository settings. `AGENT_CLI` names it, and `AGENT_API_KEY_ENV` names the variable its credential goes in: `COPILOT_GITHUB_TOKEN` for Copilot CLI, or `ANTHROPIC_API_KEY` for Claude Code. Either `AGENT_USE_JOB_TOKEN` set to `true` or the `AGENT_API_KEY` secret supplies the credential. When `KNOWLEDGE_RETRIEVAL` is `true`, each run that changes the bundle scores whether the index leads the agent to the concept behind each question readers asked. That costs one more agent call. A scheduled week with nothing waiting for the librarian runs no agent, except in a month's first seven days.

`CHANGELOG.md` says that the sidecar automation comes from the KTL v0.58.0 templates. It adds that those templates leave the librarian's skills pin at v0.57.0, and that the first weekly sync, which [Knowledge sync](knowledge-sync.md) runs, moves it.[^changelog.md] CONTRIBUTING.md says that the skills pin moves with the sidecar copies. [AI covenant](../policies/ai-covenant.md) sets the rules that the agent's changes follow.

[^knowledge-librarian.yaml]: .github/workflows/knowledge-librarian.yaml, the header comment, the on key, the three jobs and the comment above the agent step
[^notice]: NOTICE, the Knowledge bundle section
[^changelog.md]: CHANGELOG.md, the last item under Added
