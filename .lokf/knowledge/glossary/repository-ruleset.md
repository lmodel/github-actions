---
type: GlossaryTerm
id: https://w3id.org/lmodel/github-actions/knowledge/glossary/repository-ruleset
genre: reference
title: Repository ruleset
definition: Named rules that GitHub enforces on the branches, tags or pushes of a repository, or of every repository in an organization or enterprise that the ruleset targets.
description: "A ruleset: named rules GitHub enforces on the branches, tags or pushes of a repository, organization or enterprise, with a target, an enforcement (active, evaluate or disabled), ref conditions, bypass actors and rule types. The schema models it as GhaRepositoryRuleset."
resource: src/github_actions/schema/github_actions_rules.yaml
definedBy:
  - https://w3id.org/lmodel/github-actions/knowledge/references/rest-api-rules
relatedTo:
  - https://w3id.org/lmodel/github-actions/knowledge/glossary/required-status-check
sources:
  - id: github_actions_rules.yaml
    resource: src/github_actions/schema/github_actions_rules.yaml
    title: GhaRepositoryRuleset, GhaBypassActor and the three enums
  - id: docs-index.md
    resource: docs/index.md
    title: the rules with no check
  - id: security.md
    resource: SECURITY.md
    title: the ruleset on main
generated:
  by: process:ktl-librarian
  at: "2026-10-30T15:31:58Z"
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T22:46:12Z"
---

# Repository ruleset

The rules module defines a ruleset as named rules that GitHub enforces on the branches, tags or pushes of a repository, or of every repository in an organization or enterprise that it targets.[^github_actions_rules.yaml] The schema models it as `GhaRepositoryRuleset`.

## What the class records

- `ruleset_source_type` and `ruleset_source` say what owns the ruleset: a `Repository`, an `Organization` or an `Enterprise`, and its name, such as `<owner>/<repo>`.
- `ruleset_target` says what the ruleset applies to: `branch`, which is GitHub's default, `tag`, or `push`, by the files a push changes.
- `enforcement` is `active`, `evaluate` or `disabled`. `evaluate` reports but does not enforce, so administrators can test the rules, and only GitHub Enterprise has it.
- `ref_name_include` names the refs it applies to, as names or patterns such as `refs/heads/main`, `~DEFAULT_BRANCH` or `~ALL`, and `ref_name_exclude` the refs it leaves out.
- `bypass_actors` lists who may bypass it. Each actor has an `actor_type`, such as `Team`, `RepositoryRole`, `Integration` or `OrganizationAdmin`, an `actor_id` where the type takes one, and a `bypass_mode`, such as `always`, `pull_request` or `exempt`, with `always` as GitHub's default.
- `rule_types` lists the `type` of each rule, such as `deletion`, `non_fast_forward`, `pull_request` or `required_status_checks`.
- `requires_check` names the [required status checks](required-status-check.md) that its `required_status_checks` rule requires. Of the rules' parameters, only those are modelled.

A comment says that SLSA's Source track calls such rules technical controls on protected named references, and asks that their meaning be documented and their enforcement recorded in attestations, which the slsa schema models.

`docs/index.md` says that no tool checks that a ruleset whose `requires_check` names a check lists `required_status_checks` among its `rule_types`.[^docs-index.md]

## In this repository

SECURITY.md says that a ruleset on `main`, a repository setting rather than a file, blocks deletion and force-pushes and keeps the history linear.[^security.md]

[^github_actions_rules.yaml]: src/github_actions/schema/github_actions_rules.yaml, GhaRepositoryRuleset, GhaBypassActor and the enums
[^docs-index.md]: docs/index.md, the Validating data section
[^security.md]: SECURITY.md, the paragraph after the table
