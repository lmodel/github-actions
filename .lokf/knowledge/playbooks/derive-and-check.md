---
type: Playbook
id: https://w3id.org/lmodel/github-actions/knowledge/playbooks/derive-and-check
genre: how-to
title: Derive and check concepts from workflow files
description: How to run scripts/derive.py, which derives concept frontmatter and check names from a repository's workflow and action files and reports drift from a knowledge bundle, and scripts/github_export.py, which fetches the rulesets and check runs that derive.py also compares; here derive.py runs with --exclude tests/.
resource: scripts/derive.py
about:
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/github-actions-linkml-schema
references:
  - https://w3id.org/lmodel/github-actions/knowledge/glossary/required-status-check
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/test-data
sources:
  - id: derive.py
    resource: scripts/derive.py
    title: the PEP 723 header, the docstring, the options and the comparisons
  - id: github_export.py
    resource: scripts/github_export.py
    title: the docstring and the two commands
  - id: readme.md
    resource: README.md
    title: the Deriving the facts from a repository section
  - id: security.md
    resource: SECURITY.md
    title: the What this repository releases section
  - id: test_derive.py
    resource: tests/test_derive.py
    title: the twenty-one tests
  - id: test_github_export.py
    resource: tests/test_github_export.py
    title: the tests of the export script
  - id: changelog.md
    resource: CHANGELOG.md
    title: the Unreleased section
  - resource: tests/derive
    title: the fixture repository and the two export files
generated:
  by: process:ktl-librarian
  at: "2026-10-29T16:18:12Z"
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T22:46:12Z"
---

# Derive and check concepts from workflow files

`scripts/derive.py` derives the facts that the github-actions schema describes from a repository's files.[^derive.py] It reads the workflow files under `.github/workflows/` and every `action.yml` or `action.yaml` in the repository, with `yaml.safe_load`. It never runs what the files contain, calls no network and writes nothing, so it is safe on files that a pull request changed.

`scripts/github_export.py` asks GitHub's REST API for what the files cannot say: a repository's rulesets, and the checks that one commit recorded.[^github_export.py] `CHANGELOG.md` lists both comparisons under Unreleased.[^changelog.md]

## Run it

derive.py's only dependency is PyYAML, declared in its PEP 723 header, so `uv run` needs no project. github_export.py needs Python 3.10 alone. The README gives the commands:[^readme.md]

```bash
uv run scripts/derive.py --root ../host-repository
uv run scripts/derive.py --root ../host-repository --check ../host-repository/.lokf/knowledge
python3 scripts/github_export.py rulesets --repository OWNER/REPO > rulesets.md
python3 scripts/github_export.py check-runs SHA --repository OWNER/REPO > check-runs.md
uv run scripts/derive.py --root ../host-repository --check ../host-repository/.lokf/knowledge \
  --rulesets rulesets.md --check-runs check-runs.md
```

derive.py takes these options:

- `--root` names the repository to read, and defaults to the current directory.
- `--exclude PATH`, which may be repeated, leaves out the files under a path relative to the root.
- `--rulesets FILE`, which may be repeated, reads what `github_export.py rulesets` printed, the ingest's mirror of it, or a ruleset saved as the REST API returns it.
- `--check BUNDLE` compares the facts with a knowledge bundle.
- `--check-runs FILE`, with `--check`, reads what `github_export.py check-runs` printed for one commit, such as the head of a recent pull request.
- `--strict` makes the check fail on findings as well as on drift.

On a private repository, `GH_TOKEN` holds a token with Metadata read, and Checks and Commit statuses read for `check-runs`. The README says that a host copies both scripts from a pinned release and records the version beside them. Its ingest can run `github_export.py rulesets` as an entry of `kind: command`, and the mirror file becomes the rulesets' source.

In this repository, pass `--exclude tests/`. The script looks for action files in the whole tree, and would otherwise also read the two fixture actions under `tests/derive/repo/`, which no concept describes. So the check of this bundle, run from the repository root, is:

```bash
uv run --quiet scripts/derive.py --exclude tests/ --check .lokf/knowledge
```

## What it prints

Without `--check`, derive.py prints one YAML mapping:

- **`workflows`** gives, for each workflow file, the frontmatter of the concept that describes it. A file whose triggers include `workflow_call` is a `GhaReusableWorkflow`, with its inputs, outputs and secrets, and any other file is a `GhaWorkflow`. Each records `workflow_path`, `triggers`, `permissions` and `jobs`, and sets a key only when the file states it. The script reads the `on` key even where YAML 1.1 reads a bare `on` as `true`.
- **`actions`** gives, for each action file, the frontmatter of a `GhaAction`: `action_path`, `using`, and its inputs and outputs.
- **`checks`** gives, for each top-level workflow, the name of each check run its jobs report, which is the `check_context` a ruleset would require. It adds the `job_path` and `skip_conditions` of the `GhaRequiredStatusCheck` that would name it, and `leaves_pending`, the skip conditions that leave the check pending rather than passed.
- **`findings`** lists what the OpenSSF Baseline and Scorecard call out. It names a `write` permission at a workflow's top level, a caller that passes `secrets: inherit`, and a `uses` that is not pinned to a commit, or, for a `docker://` image, to a digest.
- With `--rulesets`, **`rulesets`** gives the frontmatter of each ruleset's `GhaRepositoryRuleset` concept. **`required_checks`** gives each context the rulesets require, with its `integration_id`, `strict_policy` and `do_not_enforce_on_create`, the rulesets that require it, and whether a rule in effect on the default branch requires it.

## How it names a check

The script names a check by the rule in [Required status check](../glossary/required-status-check.md):

- a check run is named after its job's `name`, or the job's id when it has none;
- a job of a called workflow is named after the calling job and the called job, joined by a slash with a space on each side;
- a matrix job's name adds its matrix values in parentheses, joined by a comma and a space, and a `name` that reads the matrix context takes the values in its own place instead.

A path filter under an event (`paths` or `paths-ignore`) and a job's `if` are recorded as skip conditions, and a called job's check carries its caller's `if` too. They differ in what they do to a required check. A job that its own `if` skips reports success, so the check passes without running. A path filter skips the whole run, and a calling job's `if` skips the call, which GitHub reports under the caller's name alone. In both cases no check run carries the check's name, so the check stays pending and blocks the merge.

A job whose matrix an expression sets, and a job that calls a workflow in another repository, are reported as unresolved, because the script reads only the repository it is given. It stops following calls at ten levels, which a comment calls GitHub's limit on how deep workflows can call one another.

## What the check compares

With `--check BUNDLE`, the script compares the facts with the concepts in the bundle, and exits 1 on drift:

- a file with no concept;
- a concept whose file is gone;
- a fact that the file and the concept disagree on;
- a required check that no job of the workflow its `emitted_by` names reports;
- a skip condition that a required check's body does not name.

A concept takes part when its `type` starts with `Gha` and it has a `workflow_path` or an `action_path`. The script compares only the keys it derives, compares lists in any order except `job_path`, and matches the items of `jobs`, `inputs`, `outputs` and `secrets` by their ids. So a key that the files cannot give, such as `workflow_repository` or `runner_environment`, is not compared.

A required check whose `integration_id` names an app other than GitHub Actions is not matched to a job, and that is a finding. Each skip condition of a required check is a finding, worded by what it does to the check, and so is a check of a job in another repository's workflow. Findings fail the check only with `--strict`. The last line counts both, as in `0 drift, 0 finding(s)`.

With `--rulesets`, these are drift too:

- a ruleset with no `GhaRepositoryRuleset` concept, or a concept whose ruleset is not among those given;
- a fact that a ruleset and its concept disagree on, or a `requires_check` that names other checks than the ruleset requires;
- a required context with no `GhaRequiredStatusCheck` concept, or a check concept that no ruleset requires.

Bypass actors are compared only when the export holds them, because GitHub returns them only to a token that can edit the ruleset. A check that a ruleset requires, but that no rule in effect on the default branch requires, is a finding.

With `--check-runs`, a required check that no check run or status on the commit matched is drift, and so is a run of that name from an app other than its `integration_id`. When a skip condition can leave the check pending, a missing run is a finding instead, and it names the caller's run that GitHub recorded as skipped. A matched run that was skipped is a finding too, since GitHub counts a skipped check as passed.

In this bundle, the nine concepts under `workflows/` are the `GhaWorkflow` concepts that the check compares with `.github/workflows/`. The bundle holds no `GhaRequiredStatusCheck`, so the check compares no check name.

## Where it runs

SECURITY.md says that neither script runs in a workflow of this repository.[^security.md] A host runs derive.py over its own files, on a pull request too. github_export.py makes read-only calls to the REST API over https, and sends its token to that address and never on to a redirect.

## Its tests

`tests/test_derive.py` runs derive.py against a fixture repository in `tests/derive/repo/`, and against `tests/derive/rulesets.md` and `tests/derive/check-runs.md`, which hold what github_export.py prints.[^test_derive.py] The fixture repository holds five workflow files, `labels.yml`, `lint.yaml`, `pull-request.yml`, `release.yml` and `tests.yml`, and two action files, `.github/actions/setup/action.yml` and `actions/labels/action.yaml`. Its twenty-one tests cover:

- a reusable workflow's inputs, outputs and secrets, each form of `runs-on`, and an action's deprecated input;
- the check names at every depth, the unresolved checks, the skip conditions, and those that leave a check pending;
- the findings;
- that every record the script prints validates against the schema for the class it names, rulesets and required checks included;
- that `--check` passes a matching bundle and reports each kind of drift, including an unexplained skip condition;
- that a check another app reports, and a check of a job in another repository's workflow, are findings and not drift;
- each form that `--rulesets` reads, and what `--rulesets` and `--check-runs` find.

`tests/test_github_export.py` replaces the REST API with fixed answers.[^test_github_export.py] Its tests cover the pinned API version, paging, both commands, the Markdown that derive.py reads back, where the token goes, and the arguments the script refuses. The README says that the fixtures show each rule. `just test` runs these tests with the other pytest tests.

[^derive.py]: scripts/derive.py, the docstring, the options and the comparisons
[^github_export.py]: scripts/github_export.py, the docstring and the two commands
[^changelog.md]: CHANGELOG.md, the Unreleased section
[^readme.md]: README.md, the Deriving the facts from a repository section
[^security.md]: SECURITY.md, the What this repository releases section
[^test_derive.py]: tests/test_derive.py, the twenty-one test functions
[^test_github_export.py]: tests/test_github_export.py, the test functions
