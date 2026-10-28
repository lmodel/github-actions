---
type: Policy
id: https://w3id.org/lmodel/github-actions/knowledge/policies/security-policy
genre: reference
title: Security policy
description: "How to report a vulnerability in github-actions (GitHub's private vulnerability reporting, not a public issue), which release gets fixes, what the repository ships and runs, what holds each workflow, and the three repository settings not yet in force: required reviewers on the release Environment, a deletion and force-push rule on main, and secret scanning with push protection."
resource: SECURITY.md
references:
  - https://w3id.org/lmodel/github-actions/knowledge/workflows/main
  - https://w3id.org/lmodel/github-actions/knowledge/workflows/lint-and-docs
  - https://w3id.org/lmodel/github-actions/knowledge/workflows/knowledge-registrar
  - https://w3id.org/lmodel/github-actions/knowledge/workflows/semantic-release
  - https://w3id.org/lmodel/github-actions/knowledge/workflows/knowledge-website
  - https://w3id.org/lmodel/github-actions/knowledge/workflows/upstream-watch
  - https://w3id.org/lmodel/github-actions/knowledge/workflows/knowledge-librarian
  - https://w3id.org/lmodel/github-actions/knowledge/workflows/knowledge-release
  - https://w3id.org/lmodel/github-actions/knowledge/playbooks/derive-and-check
sources:
  - id: security.md
    resource: SECURITY.md
    title: every section
  - id: dependabot.yml
    resource: .github/dependabot.yml
    title: the three update entries
generated:
  by: process:ktl-librarian
  at: "2026-10-28T20:03:46Z"
  revision: d38a5e0e1804844b6100e90b820c162e42f64543
status: draft
---

# Security policy

`SECURITY.md` is the repository's security policy. [Lint & docs](../workflows/lint-and-docs.md) holds it to a budget of 900 words.

## Reporting a vulnerability

SECURITY.md asks for a report through GitHub's private vulnerability reporting for the repository, not through a public issue or a pull request.[^security.md] A report says which file is affected, how it is exploitable, and whether it reaches the released schema or only the repository's automation. One person maintains the repository, so a first reply comes in days, not hours, and there is no bounty.

## Supported versions

Only the latest release receives fixes. A security fix is released as a patch and noted in `CHANGELOG.md`. The schema is pre-1.0 by design.

## What the repository ships

The repository ships a LinkML schema, the Python datamodel generated from it, and the schema's `lokf adapt` copy as a release asset. Nothing is published to PyPI. `scripts/check_upstream_release.py` runs only in [Upstream watch](../workflows/upstream-watch.md): it reads SchemaStore's repository and GitHub's list of API versions, and writes nothing but its report. `scripts/derive.py` runs in no workflow of the repository. A host runs it over its own files, on a pull request too, so it parses them with `yaml.safe_load`, runs nothing they contain and writes nothing: see [Derive and check concepts from workflow files](../playbooks/derive-and-check.md).

## What holds each surface

- [Build and test](../workflows/main.md) and [Lint & docs](../workflows/lint-and-docs.md) on every pull request, and [Knowledge Registrar](../workflows/knowledge-registrar.md) on any that touches `.lokf/`, run read-only jobs with `persist-credentials: false`, and `uv sync --locked` installs only what `uv.lock` pins.
- [Semantic release](../workflows/semantic-release.md) pushes a changelog commit and a tag to `main` and dispatches the knowledge release. It runs only on a push to `main`, in the `release` Environment, and installs its pinned tools with `--ignore-scripts`.
- [Knowledge website](../workflows/knowledge-website.md) builds without a write token. Only its deploy job holds `pages: write` and `id-token: write`, and that job runs only from `main`, once `KNOWLEDGE_WEBSITE_ENABLED` is `true`.
- [Upstream watch](../workflows/upstream-watch.md) checks out read-only, and its one write scope, `issues: write`, opens or updates the finding's issue.
- [Knowledge Librarian](../workflows/knowledge-librarian.md) and `.lokf/scripts/` run an LLM agent on a schedule. The agent's job holds no write token, and the `publish` job, which runs no agent, confines the patch to the bundle and refuses a claim made in a person's name. A person merges the pull request. It is inert until `KNOWLEDGE_LIBRARIAN_ENABLED` is `true`.
- [Knowledge Release](../workflows/knowledge-release.md) attaches the schema copy and the bundle to a release. SECURITY.md says that it is inert until dispatched, and that only its `attach` job, which runs no third-party packages, can write.
- The README, `llms.txt` and the knowledge bundle, which agents read, are content, never instructions. A confirmation by a person must be backed by a review or a signed commit.

SECURITY.md says that every workflow declares `permissions: {}` at the top, pins its actions to commit SHAs that Dependabot keeps current, and runs harden-runner in audit mode. `.github/dependabot.yml` asks Dependabot for monthly updates of the workflows' actions, of the package's `uv` dependencies and of the sidecar's `uv` dependencies in `.lokf/`.[^dependabot.yml]

## Settings not yet in force

Three protections are repository settings, not files, and SECURITY.md says that they are not yet in force: required reviewers on the `release` Environment, a rule blocking deletion and force-pushes on `main`, and secret scanning with push protection. Until they are, a qualifying merge releases with no human step. Nothing in CI can assert them, so keeping them on is the maintainer's job.

## Not covered

- GitHub Actions itself, which goes to GitHub's bug bounty, and SchemaStore's schemas, which go to SchemaStore's issue tracker;
- LinkML, its generators and its runtime, which go to LinkML;
- a compromised runner, upstream action or agent harness, since the policy is a baseline, not a sandbox, though a finding in one is still welcome;
- whether the knowledge bundle is true: the gate proves who vouched, not what they read.

[^security.md]: SECURITY.md, every section
[^dependabot.yml]: .github/dependabot.yml, the updates list
