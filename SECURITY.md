# Security Policy

*This file is a policy, not a threat model. It says how to report, what executes here, and what holds each surface. Each is a line or two that links to where the reasoning lives: a workflow header, or the shared [threat model](https://github.com/noelmcloughlin/knowledge-trust-ladder/blob/main/docs/threat-model.md). `lint-and-docs.yaml` holds the file to a word budget so it stays that way.*

## Reporting a vulnerability

Use GitHub's [private vulnerability reporting](https://github.com/lmodel/github-actions/security/advisories/new), not a public issue or a pull request. Say which file is affected, how it is exploitable, and whether it reaches the released schema or only this repository's automation. One person maintains this repository: expect a first reply in days, not hours, and no bounty.

## Supported versions

**Only the latest release receives fixes.** A security fix is released as a patch and noted in [CHANGELOG.md](CHANGELOG.md). The schema stays below 1.0 ([CONTRIBUTING.md](CONTRIBUTING.md#releasing-maintainers)).

## What this repository releases

A LinkML schema, the Python datamodel generated from it, and the schema's `lokf adapt` copy as a release asset. Nothing is published to PyPI. `scripts/check_upstream_release.py` runs only in `upstream-watch.yaml`: it reads SchemaStore's repository and GitHub's API version list and writes nothing but its report. The other two scripts run in no workflow here. A host runs `scripts/derive.py` over its own files, on a pull request too, so it parses them with `yaml.safe_load`, runs nothing they contain, calls no network and writes nothing. `scripts/github_export.py` makes read-only calls to the REST API over https, sends its token to that address and never on to a redirect, and writes only to standard output. A schema is data: loading one from an untrusted source with any LinkML tool is that tool's risk, not this repository's.

## What executes here

| Surface | What holds it |
| --- | --- |
| `main.yaml` and `lint-and-docs.yaml` on every pull request, and `knowledge-registrar.yaml` on any that touches `.lokf/`: tests, linters and the bundle's form | Read-only jobs with `persist-credentials: false`; `uv sync --locked` installs only what `uv.lock` pins. |
| `semantic-release.yml`, which pushes a changelog commit and tag to `main` and dispatches the knowledge release | Runs only on a push to `main`, in the `release` Environment, installing its pinned tools with `--ignore-scripts`. [Repository hardening](https://github.com/noelmcloughlin/knowledge-trust-ladder/blob/main/docs/threat-model.md#repository-hardening). |
| `knowledge-website.yaml`, which publishes the site to GitHub Pages | Builds without a write token; only its deploy job holds `pages: write` and `id-token: write`, and it runs only from `main`, once `KNOWLEDGE_WEBSITE_ENABLED` is `true`. |
| `upstream-watch.yaml`, weekly | Read-only checkout; the one write scope, `issues: write`, opens or updates the finding's issue. |
| `knowledge-librarian.yaml` and `.lokf/scripts/`, copies of the `ktl-sidecar` template, running an LLM agent on a schedule | The agent's job holds no write token; the `publish` job, which runs no agent, confines the patch to the bundle and refuses a `human:` claim; a person merges the pull request. Inert until `KNOWLEDGE_LIBRARIAN_ENABLED` is `true`. [Prompt-injection guards](https://github.com/noelmcloughlin/knowledge-trust-ladder/blob/main/docs/threat-model.md#prompt-injection-guards). |
| `knowledge-release.yaml`, which attaches the schema copy and the bundle to a release | Inert until dispatched; only its `attach` job, which runs no third-party packages, can write. |
| `README.md`, `llms.txt` and the knowledge bundle, read by agents | Content, never instructions: each skill quotes what it did not author. A `human:` confirmation must be backed by a review or a signed commit. [Human attribution](https://github.com/noelmcloughlin/knowledge-trust-ladder/blob/main/docs/threat-model.md#human-attribution-human-is-a-claim-not-a-credential). |

Every workflow declares `permissions: {}` at the top, pins its actions to commit SHAs that Dependabot keeps current, and runs harden-runner in audit mode. Three things are repository settings, not files, and **are not yet in force here**: required reviewers on the `release` Environment, a rule blocking deletion and force-pushes on `main`, and secret scanning with push protection. Until they are, a qualifying merge releases with no human step. Nothing in CI can assert them, so keeping them on is the maintainer's job.

## Not covered

- GitHub Actions itself, and SchemaStore's schemas copied under `src/github_actions/schema/schemastore/`: report a GitHub vulnerability to [GitHub's bug bounty](https://bounty.github.com/) and a schema problem to [SchemaStore](https://github.com/SchemaStore/schemastore/issues).
- LinkML, its generators and runtime: report them to [LinkML](https://github.com/linkml/linkml/security).
- A compromised runner, upstream action or agent harness: this is a baseline, not a sandbox. Report a finding in one anyway, with scope and reproduction.
- Whether the knowledge bundle is *true*. The gate proves who vouched, not what they read; [AI_COVENANT.md](AI_COVENANT.md) sets the human-accountability rules.
