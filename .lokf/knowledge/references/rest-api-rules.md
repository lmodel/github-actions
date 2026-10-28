---
type: Reference
id: https://w3id.org/lmodel/github-actions/knowledge/references/rest-api-rules
genre: reference
title: GitHub REST API rules and check runs
description: "The GitHub REST API's rules and check runs pages at API version 2026-03-10: the source of GhaRepositoryRuleset, GhaBypassActor and GhaRequiredStatusCheck, whose fields are named after REST fields such as `source_type`, `enforcement` and `required_status_checks[].context`."
resource: https://docs.github.com/en/rest/repos/rules
sources:
  - id: readme.md
    resource: README.md
    title: the What it models section
  - id: github_actions_rules.yaml
    resource: src/github_actions/schema/github_actions_rules.yaml
    title: the module comment, the field descriptions and the see_also entries
  - id: check_upstream_release.py
    resource: scripts/check_upstream_release.py
    title: PINNED_API_VERSION and the version check
generated:
  by: process:ktl-librarian
  at: "2026-10-28T21:21:37Z"
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T20:03:46Z"
---

# GitHub REST API rules and check runs

The README says that `GhaRepositoryRuleset` and `GhaRequiredStatusCheck` come from the REST API's [rules](https://docs.github.com/en/rest/repos/rules) and [check runs](https://docs.github.com/en/rest/checks/runs) pages at API version 2026-03-10.[^readme.md] The rules module's comment says that its fields follow that version, and that none of the version's breaking changes touches rulesets, rules or check runs, so they read the same at 2022-11-28.[^github_actions_rules.yaml]

The module names each field after the REST field it renders:

- a ruleset's page, `_links.html.href`, is `ruleset_uri`, which the adapt copy replaces with LOKF's `id`, and the ruleset's numeric `id` becomes `ruleset_id`;
- `source_type`, `source` and `target` become `ruleset_source_type`, `ruleset_source` and `ruleset_target`, and `enforcement` keeps its name;
- `conditions.ref_name.include` and `conditions.ref_name.exclude` become `ref_name_include` and `ref_name_exclude`;
- a bypass actor's `actor_type` and `bypass_mode` keep their names;
- a required check's `required_status_checks[].context` becomes `check_context`, and `integration_id`, `strict_required_status_checks_policy` and `do_not_enforce_on_create` become `integration_id`, `strict_policy` and `do_not_enforce_on_create`.

`GhaRepositoryRuleset` also cites GitHub's pages about rulesets and the rules available to them, and `GhaRequiredStatusCheck` its pages about status checks and about troubleshooting required status checks.

`scripts/check_upstream_release.py` pins the version as `PINNED_API_VERSION` and asks GitHub's API for the list of supported versions on each run. It reports a newer version than the pin, and asks for its breaking changes to be read for changes to rulesets, rules or check runs.[^check_upstream_release.py]

[^readme.md]: README.md, the What it models section
[^github_actions_rules.yaml]: src/github_actions/schema/github_actions_rules.yaml, the module comment and the attribute descriptions
[^check_upstream_release.py]: scripts/check_upstream_release.py, PINNED_API_VERSION and the end of check()
