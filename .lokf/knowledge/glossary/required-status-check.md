---
type: GlossaryTerm
id: https://w3id.org/lmodel/github-actions/knowledge/glossary/required-status-check
genre: reference
title: Required status check
definition: A status check that a ruleset requires to pass before a change reaches a ref the ruleset targets, named by the context that a check run must report.
description: A status check that a ruleset requires to pass before a change reaches a ref it targets; its name is the context a check run reports, which GitHub Actions takes from the job's name or id, as caller / called for a job of a called workflow. The schema models it as GhaRequiredStatusCheck.
resource: src/github_actions/schema/github_actions_rules.yaml
definedBy:
  - https://w3id.org/lmodel/github-actions/knowledge/references/rest-api-rules
relatedTo:
  - https://w3id.org/lmodel/github-actions/knowledge/glossary/repository-ruleset
sources:
  - id: github_actions_rules.yaml
    resource: src/github_actions/schema/github_actions_rules.yaml
    title: GhaRequiredStatusCheck, its attributes and its comments
  - id: readme.md
    resource: README.md
    title: the Influences section
  - id: contributing.md
    resource: CONTRIBUTING.md
    title: the last item of Releasing (maintainers)
  - id: derive.py
    resource: scripts/derive.py
    title: the docstring's statement of the naming rule
generated:
  by: process:ktl-librarian
  at: "2026-10-28T20:03:46Z"
  revision: 4e47f1efc96b84011e7016edd847a71bfc692a33
status: draft
---

# Required status check

The rules module defines a required status check as a status check that a ruleset requires to pass before a change reaches a ref it targets, named by the context that a check run must report.[^github_actions_rules.yaml] The schema models it as `GhaRequiredStatusCheck`, with `check_context` for that context. A ruleset names the checks it requires in `requires_check`, and `emitted_by` names the top-level workflow whose job reports a check.

## How a check is named

The class's comments state the rule:

- GitHub Actions reports each job as a check run named after the job: its `name`, or its id when it has none;
- a job of a called workflow is named after the calling job and the called job, joined by a slash with a space on each side, such as `test / unit`;
- a matrix job's check name adds its matrix values in parentheses, such as `docs (3.13)`.

The comment says that the otterdog documentation states the rule for a called job, and the README adds that none of GitHub's pages states it.[^readme.md] `job_path` records the job ids from the top-level workflow's job to the job that reports the check, with the calling job's id first for a job of a called workflow.

`scripts/derive.py` applies the rule to a repository's workflow files.[^derive.py] Its docstring adds that a matrix job's values are joined by a comma and a space, that a `name` which reads the matrix context takes the values in its own place, and that the check names of a job that calls a workflow in another repository are reported as unresolved. See [Derive and check concepts from workflow files](../playbooks/derive-and-check.md).

## What else the class records

- `integration_id` names the GitHub App the check must come from; GitHub Actions is app 15368.
- `strict_policy` says whether a pull request must be tested against the latest code of the branch it targets.
- `do_not_enforce_on_create` says whether a branch may be created although the check would otherwise stop it.
- `skip_conditions` records what in the workflow can skip the job, as key paths such as `on.pull_request.paths` or `jobs.test.if`. A comment says that a job that a path filter or an `if` skips reports success and does not block a merge, even when its check is required.

The comments relate the class to two outside vocabularies. SLSA's Source track lets an organization carry such a control into a Source Verification Summary Attestation as an `ORG_SOURCE_` property, and slsa-framework's source-tool emits one as `GH_REQUIRED_CHECK_` followed by the check's name. in-toto's Test Result predicate is the shape of an attestation of what the check found.

## In this repository

CONTRIBUTING.md asks maintainers to leave off any branch rule that requires status checks on `main`, because it would reject the release job's own push to `main`.[^contributing.md]

[^github_actions_rules.yaml]: src/github_actions/schema/github_actions_rules.yaml, GhaRequiredStatusCheck
[^readme.md]: README.md, the otterdog item of the Influences section
[^contributing.md]: CONTRIBUTING.md, the last item of Releasing (maintainers)
[^derive.py]: scripts/derive.py, the docstring
