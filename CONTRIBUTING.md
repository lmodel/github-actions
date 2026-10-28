# Contributing to github-actions

*This file is a checklist, not a design log. Each rule is a line or two that links to where its reasoning lives: a code comment, a workflow header, or a linked page. `lint-and-docs.yaml` holds the file to a word budget so it stays that way.*

Thanks for your interest in improving this LinkML schema for GitHub Actions.

## What this project is

A LinkML schema for what a GitHub Actions workflow file, an action's metadata file and a repository ruleset state: triggers, permissions, jobs and runners, inputs, outputs and secrets, and the status checks a ruleset requires. A knowledge bundle types its concepts with it, and a script checks those concepts against the files.

| Path | Holds |
| --- | --- |
| `src/github_actions/schema/*.yaml` | The LinkML schema and its modules. Edit these. |
| `src/github_actions/schema/schemastore/` | SchemaStore's workflow and action JSON Schemas at the pinned commit. Never edit. |
| `src/github_actions/datamodel/`, `project/`, `docs/schema/` | Artefacts generated from the schema. |
| `docs/` | The documentation site's pages. |
| `tests/`, `tests/data/` | Python tests; valid and invalid example data. |
| `.lokf/knowledge/` | This repository's own knowledge bundle. |

## Development setup

Python 3.10+, [uv](https://docs.astral.sh/uv/) and [just](https://github.com/casey/just) are required.

```bash
git clone https://github.com/lmodel/github-actions.git
cd github-actions
uv sync --group dev
just --list
```

`just gen-project` regenerates `project/` and the Python datamodel; `just gen-doc` and `just gen-merged` regenerate `docs/schema/` and the site's element pages.

### Agent skills (optional, only for this repo's `.lokf/` bundle)

The bundle is maintained with the Knowledge Trust Ladder (KTL) skills, **installed, never committed**; CI installs the librarian skill at run time, pinned to a release. Nothing in the schema depends on them. [The install page](https://w3id.org/ktl/docs/install/) lists every route; with npm:

```bash
npx skills add noelmcloughlin/knowledge-trust-ladder --skill ktl-librarian --yes   # derive concepts
npx skills add noelmcloughlin/knowledge-trust-ladder --skill ktl-curator --yes     # confirm them as a person
```

## Before opening a pull request

- **Edit the schema, then regenerate.** Edit `src/github_actions/schema/`, run `just gen-project`, `just gen-doc`, `just gen-merged` and `just lokf-adapt`, and commit the output; `project/`, `src/github_actions/datamodel/`, `docs/schema/` and `.lokf/github-actions.yaml` are generated.
- **Name the page a description renders.** A class, slot or enum value says what GitHub's documentation or SchemaStore's schema says, in your own words; give the page's address in `see_also` and the pull request. [AI_COVENANT.md](AI_COVENANT.md) says why.
- **Leave `src/github_actions/schema/schemastore/` as upstream wrote it.** Replace both files from one SchemaStore commit instead and move the pin in `scripts/check_upstream_release.py` and the schema header; [NOTICE](NOTICE) records the commit, and `upstream-watch.yaml` checks it.
- **Keep the names apart from LOKF's and slsa's.** A host imports this schema's adapt copy beside `lokf.yaml` and slsa's, so a shared name must mean the same and carry the same IRI; `tests/test_schema_rules.py` checks.
- **Run the tests**: `just test` (schema generation, `pytest`, and the examples under `tests/data/`). Example data goes in `tests/data/valid/` and `tests/data/invalid/`, named `ClassName-###.yaml`; each constraint has an invalid example.
- **Follow the schema's conventions**: UpperCamelCase classes and enums, snake_case slots, GitHub's own strings as permissible values (`.linkmllint.yaml` says why), attributes unless two classes share a field, a short description on every element. `just lint` checks.
- **Run the pre-commit hooks** on what you staged (`uvx pre-commit run`): ruff, yamllint, codespell, typos and the `uv.lock` check.
- **Lock files are part of the change.** CI installs with `uv sync --locked`; a dependency edit that does not update `uv.lock` (or `.lokf/uv.lock`) fails the run.
- **Knowledge-bundle changes**: `cd .lokf && just lokf-validate` must pass, and `knowledge-registrar.yaml` runs on any `.lokf/**` change.
- **`lint-and-docs.yaml` is easy to trip locally**: ShellCheck, actionlint, markdownlint against `.markdownlint-cli2.jsonc`, link-checking against `lychee.toml`, and codespell over every `*.md`.
- **Actions are pinned to commit SHAs**, the version in a trailing comment, and bumped by Dependabot, never by hand to a tag.
- **The skills pin moves with the sidecar copies.** When moving `TRUST_LADDER_SKILLS_REF` in `.github/workflows/knowledge-librarian.yaml`, copy the other `knowledge-*.yaml` workflows and `.lokf/scripts/` and `.lokf/m365/` from that release's `skills/ktl-sidecar/templates/` in the same pull request.
- **If your change alters behaviour** (not just wording), add an entry under `## [Unreleased]` in [CHANGELOG.md](CHANGELOG.md).
- Keep changes focused, reference the issue they close, and fill in the PR template's checklist.

## Code of conduct

Participation here is covered by the [Contributor Covenant](CODE_OF_CONDUCT.md).

## Using AI tools

AI assistance is welcome; [AI_COVENANT.md](AI_COVENANT.md) sets the rules, for people and the scheduled `knowledge-librarian` agent alike. You are the author of what you submit, and a claim about what GitHub does must be checked against its documentation.

## Reporting issues

Use the [issue tracker](https://github.com/lmodel/github-actions/issues) for problems with the schema and requests for new elements. A problem with SchemaStore's schemas belongs [upstream](https://github.com/SchemaStore/schemastore/issues).

## Releasing (maintainers)

- Write `## [Unreleased]` in [CHANGELOG.md](CHANGELOG.md) as you go; the release job refuses an empty one (`.github/scripts/changelog-release.mjs check`).
- Type the commit ([Conventional Commits](https://www.conventionalcommits.org/)) for what the change *is*. Only `feat:`, `fix:`, `security:` and a breaking `!` cut a release; other types leave their entries for the next release that does. A pull request that would release must carry a releasing type in its title too, since a squash merge takes its subject from it.
- On merge, [`semantic-release.yml`](.github/workflows/semantic-release.yml) retitles the section to `## [X.Y.Z] - YYYY-MM-DD`, commits `CHANGELOG.md`, tags `vX.Y.Z` and publishes the GitHub Release. No file is bumped. It then dispatches `.github/workflows/knowledge-release.yaml` for the tag once `KNOWLEDGE_RELEASE_ENABLED` is `true`, which attaches the schema copy and the bundle.
- That step runs behind the `release` GitHub Environment; configure required reviewers on it in Settings → Environments, or every qualifying merge is released unattended.
- Below 1.0.0: `v0.1.0` is the first release and the baseline semantic-release counts from; both release jobs refuse to run without a `v*` tag, as semantic-release would otherwise start at 1.0.0. `.releaserc.json` maps `breaking: true` to `minor`; reaching 1.0.0 means removing that rule in its own PR.
- PyPI publishing is off: the template's `gh_action_pypi` answer is `false`. The package name is `github-actions-linkml` if a consumer ever needs it.
- A branch rule requiring pull requests, status checks or signed commits would reject the release job's own push to `main`; leave them off. [SECURITY.md](SECURITY.md) says what holds `main` instead, and the shared design is on [KTL's releasing page](https://github.com/noelmcloughlin/knowledge-trust-ladder/blob/main/docs/releasing.md).

## License

By contributing, you agree that your contributions are licensed under the [Apache License 2.0](LICENSE). The SchemaStore copy is third-party work under its own notice; [NOTICE](NOTICE) lists it, so update it when you add something new from elsewhere.
