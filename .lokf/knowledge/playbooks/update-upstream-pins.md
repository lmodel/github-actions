---
type: Playbook
id: https://w3id.org/lmodel/github-actions/knowledge/playbooks/update-upstream-pins
genre: how-to
title: Move the upstream pins
description: "What to do when the upstream watch opens its issue: replace both SchemaStore files from one commit and move PINNED_COMMIT, the schema header's source and annotations and NOTICE; or read a newer REST API version's breaking changes and move PINNED_API_VERSION; tests/test_schema_rules.py checks that the header and the script agree on the pins and the reading date."
resource: scripts/check_upstream_release.py
about:
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/schemastore-copy
references:
  - https://w3id.org/lmodel/github-actions/knowledge/workflows/upstream-watch
  - https://w3id.org/lmodel/github-actions/knowledge/references/rest-api-rules
sources:
  - id: check_upstream_release.py
    resource: scripts/check_upstream_release.py
    title: the docstring, the pins and the report's instructions
  - id: test_schema_rules.py
    resource: tests/test_schema_rules.py
    title: test_header_pins_match_the_watch
  - id: contributing.md
    resource: CONTRIBUTING.md
    title: the rule on the SchemaStore copy
  - resource: src/github_actions/schema/github_actions.yaml
    title: the header's source and annotations
  - resource: NOTICE
    title: the SchemaStore section
generated:
  by: process:ktl-librarian
  at: "2026-10-28T19:53:06Z"
  revision: b7ea64b8925de0c87fca46c5be56f440e45a7c82
status: draft
---

# Move the upstream pins

[Upstream watch](../workflows/upstream-watch.md) runs `scripts/check_upstream_release.py` every week. The script's docstring names three things that can go wrong with no change in the repository:[^check_upstream_release.py]

- SchemaStore changes `github-workflow.json` or `github-action.json`, for example when GitHub adds a permission scope or a runtime, so the copy and the schema fall behind;
- the copied files drift from the commit they were taken from;
- GitHub releases a REST API version newer than the one the rules module follows.

The script exits 1 on any of them, and the workflow then opens its issue or comments on the one already open.

## The pins

- `PINNED_COMMIT` is the SchemaStore commit. The schema header gives it in `source` and in the `schemastore_commit` annotation, and NOTICE records it.
- `PINNED_API_VERSION` is the REST API version. The header gives it in the `rest_api_version` annotation.
- `DOCS_READ` is the date GitHub's pages were read. The header gives it as `version` and in the `docs_read` annotation.

`test_header_pins_match_the_watch` in `tests/test_schema_rules.py` fails when the header and the script disagree on any of them.[^test_schema_rules.py] So a new reading date moves `DOCS_READ`, `version` and `docs_read` together.

## When SchemaStore has moved

1. Compare the pinned commit with SchemaStore's default branch, at the address the report gives.
2. Replace both schema files from one SchemaStore commit, with SchemaStore's LICENSE and NOTICE; never edit them in place.[^contributing.md]
3. Move `PINNED_COMMIT` in the script, and the commit in the schema header's `source` and annotations. Empty `KNOWN_DIFFERENCES`.
4. Update NOTICE.
5. Review the schema against the change, and run `just test`, whose tests compare the schema's patterns and enums with the new copy.

## When GitHub has a newer REST API version

1. Read that version's section of GitHub's page on breaking changes in the REST API, for changes to rulesets, rules or check runs.
2. Move `PINNED_API_VERSION` in the script and the `rest_api_version` annotation in the schema header.

GitHub's documentation pages are versionless, so no script can watch them, and the report repeats the date they were read.

[^check_upstream_release.py]: scripts/check_upstream_release.py, the docstring and the instructions check() writes into the report
[^test_schema_rules.py]: tests/test_schema_rules.py, test_header_pins_match_the_watch
[^contributing.md]: CONTRIBUTING.md, the rule on src/github_actions/schema/schemastore/
