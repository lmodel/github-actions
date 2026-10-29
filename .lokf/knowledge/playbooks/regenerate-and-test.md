---
type: Playbook
id: https://w3id.org/lmodel/github-actions/knowledge/playbooks/regenerate-and-test
genre: how-to
title: Regenerate and test the schema
description: "How to change the github-actions schema: set up with uv and just, edit src/github_actions/schema/, regenerate with just gen-project, gen-doc, gen-merged and lokf-adapt, add examples, then run the checks CI runs (just test on Python 3.10 to 3.14, just lint and just lokf-adapt-check on 3.13) and the pre-commit hooks."
resource: CONTRIBUTING.md
about:
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/github-actions-linkml-schema
references:
  - https://w3id.org/lmodel/github-actions/knowledge/workflows/main
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/generated-artefacts
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/test-data
sources:
  - id: contributing.md
    resource: CONTRIBUTING.md
    title: Development setup and Before opening a pull request
  - id: justfile
    resource: justfile
    title: the setup, update, test, lint and gen recipes and the WSL2 check
  - id: copier-answers.yml
    resource: .copier-answers.yml
    title: the template source and commit
  - id: main.yaml
    resource: .github/workflows/main.yaml
    title: the test job
  - resource: project.justfile
    title: the gen-merged and lokf-adapt recipes
  - resource: .linkmllint.yaml
    title: the lint rules
  - resource: .pre-commit-config.yaml
    title: the hooks and the exclude list
generated:
  by: process:ktl-librarian
  at: "2026-10-28T19:53:06Z"
  revision: 9e5861ab5d13ea0b34600f4339557226b1dddc15
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T21:21:37Z"
---

# Regenerate and test the schema

## Set up

CONTRIBUTING.md asks for Python 3.10 or later, uv and just.[^contributing.md] Clone the repository, run `uv sync --group dev`, and list the recipes with `just --list`. On WSL2, run `export JUST_TEMPDIR=/tmp` first, because the justfile's shebang recipes otherwise fail.[^justfile] `.copier-answers.yml` records that the project was made from `gh:linkml/linkml-project-copier` at `v0.5.0-8-ga2117fc`.[^copier-answers.yml] `just update` runs `copier update` and upgrades `linkml` and `linkml-runtime` in `uv.lock`.

## Change the schema

1. Edit the files in `src/github_actions/schema/`. Leave `src/github_actions/schema/schemastore/` as upstream wrote it: [Move the upstream pins](update-upstream-pins.md) says how to replace it.
2. Follow the schema's conventions: UpperCamelCase classes and enums, snake_case slots, GitHub's strings as permissible values, attributes unless two classes share a field, and a short description on every element. Name in `see_also` the page each description renders, and keep every name apart from LOKF's and slsa's, as [Element names and the shared namespace](../explanations/element-names.md) explains.
3. Regenerate. `just gen-project` writes `project/` and the Python models, `just gen-doc` writes `docs/schema/github_actions.yaml` and the pages in `docs/elements/`, `just gen-merged` writes `docs/schema/github_actions_merged.yaml`, and `just lokf-adapt` writes `.lokf/github-actions.yaml`. Commit the output. [Generated artefacts](../datasets/generated-artefacts.md) lists what each writes.
4. Add example data to `tests/data/valid/` and `tests/data/invalid/`, named `ClassName-###.yaml`, with an invalid example for each constraint. [Test data and schema tests](../datasets/test-data.md) describes the folders.
5. If the change alters behaviour and not just wording, add an entry under `## [Unreleased]` in `CHANGELOG.md`.

## Check it

- `just test` runs `_test-schema`, `_test-python` and `_test-examples`: it generates the project into `tmp/`, regenerates the Python models and runs pytest, and runs `linkml-run-examples` over the example data.
- `just lint` runs `linkml-lint --ignore-warnings` on the schema directory, so it fails on errors only. `.linkmllint.yaml` applies LinkML's recommended rules with `standard_naming` at warning level.
- `just lokf-adapt-check` fails when `.lokf/github-actions.yaml` is stale against the schema or `.lokf/lokf.yaml`.
- `uvx pre-commit run` runs the hooks on what is staged, which CONTRIBUTING.md names as ruff, yamllint, codespell, typos and the `uv.lock` check. The hooks leave alone the SchemaStore copy, the generated files, `.lokf/lokf.yaml` and the adapt copy, `.lokf/scripts/` and `.lokf/m365/`, and `tests/neighbours/`.
- Update `uv.lock`, or `.lokf/uv.lock`, in the same change as a dependency edit, because CI installs with `uv sync --locked` and fails otherwise.
- Run `cd .lokf && just lokf-validate` after a change to `.lokf/`.

[Build and test](../workflows/main.md) runs `just test` on Python 3.10 to 3.14, and `just lint` and `just lokf-adapt-check` on Python 3.13 only.[^main.yaml] [Lint & docs](../workflows/lint-and-docs.md) runs ShellCheck, actionlint, markdownlint, lychee and codespell. CONTRIBUTING.md says that these checks are easy to trip locally.

[^contributing.md]: CONTRIBUTING.md, Development setup and Before opening a pull request
[^justfile]: justfile, the `_wsl2_compat_check`, `update`, `test` and `lint` recipes
[^copier-answers.yml]: .copier-answers.yml, `_src_path` and `_commit`
[^main.yaml]: .github/workflows/main.yaml, the test job
