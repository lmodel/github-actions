---
type: Playbook
id: https://w3id.org/lmodel/github-actions/knowledge/playbooks/derive-and-check
genre: how-to
title: Derive and check concepts from workflow files
description: How to run scripts/derive.py, which reads a repository's workflow and action files with yaml.safe_load and prints the GhaWorkflow, GhaReusableWorkflow and GhaAction frontmatter, the name of each check run the workflows' jobs report and the OpenSSF findings; with --check it exits 1 on drift from a knowledge bundle, and here it runs with --exclude tests/.
resource: scripts/derive.py
about:
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/github-actions-linkml-schema
references:
  - https://w3id.org/lmodel/github-actions/knowledge/glossary/required-status-check
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/test-data
sources:
  - id: derive.py
    resource: scripts/derive.py
    title: the PEP 723 header, the docstring, the options and the comparison
  - id: readme.md
    resource: README.md
    title: the Deriving the facts from a repository section
  - id: security.md
    resource: SECURITY.md
    title: the What this repository releases section
  - id: test_derive.py
    resource: tests/test_derive.py
    title: the eleven tests
  - id: changelog.md
    resource: CHANGELOG.md
    title: the last item under Added
  - resource: tests/derive
    title: the fixture repository
generated:
  by: process:ktl-librarian
  at: "2026-10-28T21:21:37Z"
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T22:46:12Z"
---

# Derive and check concepts from workflow files

`scripts/derive.py` derives the facts that the github-actions schema describes from a repository's files.[^derive.py] It reads the workflow files under `.github/workflows/` and every `action.yml` or `action.yaml` in the repository, with `yaml.safe_load`. It never runs what the files contain and writes nothing, so it is safe on files that a pull request changed. `CHANGELOG.md` lists it among the unreleased additions.[^changelog.md]

## Run it

The script's only dependency is PyYAML, declared in its PEP 723 header, so `uv run` needs no project. The README gives two commands:[^readme.md]

```bash
uv run scripts/derive.py --root ../host-repository
uv run scripts/derive.py --root ../host-repository --check ../host-repository/.lokf/knowledge
```

- `--root` names the repository to read, and defaults to the current directory.
- `--exclude PATH`, which may be repeated, leaves out the files under a path relative to the root.
- `--check BUNDLE` compares the facts with a knowledge bundle.
- `--strict` makes the check fail on findings as well as on drift.

The README says that a host copies the script from a pinned release and records the version beside it.

In this repository, pass `--exclude tests/`. The script looks for action files in the whole tree, and would otherwise also read the two fixture actions under `tests/derive/repo/`, which no concept describes. So the check of this bundle, run from the repository root, is:

```bash
uv run --quiet scripts/derive.py --exclude tests/ --check .lokf/knowledge
```

## What it prints

Without `--check`, the script prints one YAML mapping with four keys:

- **`workflows`** gives, for each workflow file, the frontmatter of the concept that describes it. A file whose triggers include `workflow_call` is a `GhaReusableWorkflow`, with its inputs, outputs and secrets, and any other file is a `GhaWorkflow`. Each records `workflow_path`, `triggers`, `permissions` and `jobs`, and sets a key only when the file states it. The script reads the `on` key even where YAML 1.1 reads a bare `on` as `true`.
- **`actions`** gives, for each action file, the frontmatter of a `GhaAction`: `action_path`, `using`, and its inputs and outputs.
- **`checks`** gives, for each top-level workflow, the name of each check run its jobs report, which is the `check_context` a ruleset would require, with the `job_path` and `skip_conditions` of the `GhaRequiredStatusCheck` that would name it.
- **`findings`** lists what the OpenSSF Baseline and Scorecard call out. It names a `write` permission at a workflow's top level, a caller that passes `secrets: inherit`, and a `uses` that is not pinned to a commit, or, for a `docker://` image, to a digest.

## How it names a check

The script names a check by the rule in [Required status check](../glossary/required-status-check.md):

- a check run is named after its job's `name`, or the job's id when it has none;
- a job of a called workflow is named after the calling job and the called job, joined by a slash with a space on each side;
- a matrix job's name adds its matrix values in parentheses, joined by a comma and a space, and a `name` that reads the matrix context takes the values in its own place instead.

A path filter under an event (`paths` or `paths-ignore`) and a job's `if` are recorded as skip conditions, and a called job's check carries its caller's `if` too. A job whose matrix an expression sets, and a job that calls a workflow in another repository, are reported as unresolved, because the script reads only the repository it is given. It stops following calls at ten levels, which a comment calls GitHub's limit on how deep workflows can call one another.

## What the check compares

With `--check BUNDLE`, the script compares the facts with the concepts in the bundle, and exits 1 on drift:

- a file with no concept;
- a concept whose file is gone;
- a fact that the file and the concept disagree on;
- a required check that no job of the workflow its `emitted_by` names reports.

A concept takes part when its `type` starts with `Gha` and it has a `workflow_path` or an `action_path`. The script compares only the keys it derives, compares lists in any order except `job_path`, and matches the items of `jobs`, `inputs`, `outputs` and `secrets` by their ids. So a key that the files cannot give, such as `workflow_repository` or `runner_environment`, is not compared. A required check whose job a path filter or an `if` can skip is a finding, since a skipped job reports success, and so is a check of a job in another repository's workflow. Findings fail the check only with `--strict`. The last line counts both, as in `0 drift, 0 finding(s)`.

In this bundle, the nine concepts under `workflows/` are the `GhaWorkflow` concepts that the check compares with `.github/workflows/`. The bundle holds no `GhaRequiredStatusCheck`, so the check compares no check name.

## Where it runs

SECURITY.md says that the script runs in no workflow of this repository, and that a host runs it over its own files, on a pull request too.[^security.md]

## Its tests

`tests/test_derive.py` runs the script against a fixture repository in `tests/derive/repo/`.[^test_derive.py] The fixture holds four workflow files, `lint.yaml`, `pull-request.yml`, `release.yml` and `tests.yml`, and two action files, `.github/actions/setup/action.yml` and `actions/labels/action.yaml`. Its eleven tests cover:

- a reusable workflow's inputs, outputs and secrets, each form of `runs-on`, and an action's deprecated input;
- the check names at every depth, the unresolved checks and the skip conditions;
- the findings;
- that every record the script prints validates against the schema for the class it names;
- that `--check` passes a matching bundle, reports each kind of drift, and reports a check of a job in another repository's workflow as a finding, not drift.

The README says that the fixtures show each rule. `just test` runs these tests with the other pytest tests.

[^derive.py]: scripts/derive.py, the docstring, the options and compare()
[^changelog.md]: CHANGELOG.md, the last item under Added
[^readme.md]: README.md, the Deriving the facts from a repository section
[^security.md]: SECURITY.md, the What this repository releases section
[^test_derive.py]: tests/test_derive.py, the eleven test functions
