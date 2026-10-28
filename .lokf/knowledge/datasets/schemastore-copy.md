---
type: Dataset
id: https://w3id.org/lmodel/github-actions/knowledge/datasets/schemastore-copy
genre: reference
title: SchemaStore copy
description: SchemaStore's `github-workflow.json` and `github-action.json`, the machine-readable form of a workflow file and an action's metadata file, copied with SchemaStore's LICENSE and NOTICE into `src/github_actions/schema/schemastore/` at commit f7c2f3b; never edited here, compared by tests with the schema, and checked weekly against upstream.
resource: src/github_actions/schema/schemastore
license: Apache-2.0
source:
  - https://github.com/SchemaStore/schemastore/tree/f7c2f3bcb512651bd980ed6896639ea8ded9ddf0/src/schemas/json
sources:
  - id: notice
    resource: NOTICE
    title: the section on SchemaStore's GitHub Actions schemas
  - id: contributing.md
    resource: CONTRIBUTING.md
    title: the rule on the SchemaStore copy
  - id: test_schema_rules.py
    resource: tests/test_schema_rules.py
    title: the tests that compare the schema with the copy
  - id: check_upstream_release.py
    resource: scripts/check_upstream_release.py
    title: the docstring, the pins and the comparison
  - resource: README.md
    title: the What it models section
  - resource: src/github_actions/schema/schemastore/github-workflow.json
    title: the $id and $schema keys
  - resource: src/github_actions/schema/schemastore/github-action.json
    title: the $id and $schema keys
  - resource: .pre-commit-config.yaml
    title: the exclude list
generated:
  by: process:ktl-librarian
  at: "2026-10-28T19:53:06Z"
  revision: 9c3541e73cc92d04fdb429a1b340eeeccdae2d37
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T20:03:46Z"
---

# SchemaStore copy

NOTICE says that `src/github_actions/schema/schemastore/` holds a copy of two files from JSON Schema Store, retrieved from SchemaStore's tree at commit `f7c2f3bcb512651bd980ed6896639ea8ded9ddf0`.[^notice] `github-workflow.json` is the schema of a GitHub Actions workflow file, and `github-action.json` is the schema of an action's metadata file. SchemaStore's own LICENSE and NOTICE sit beside them, copied from the root of the same commit. NOTICE says that every file is identical to its counterpart there, and that the files are licensed under the Apache License 2.0 and carry the notice "JSON Schema Store, Copyright 2015-Current Mads Kristensen and Contributors".

The two schemas give their `$id` as `https://json.schemastore.org/github-workflow.json` and `https://json.schemastore.org/github-action.json`, and are written in JSON Schema draft-07. The README calls them the machine-readable form of the two files that GitHub's pages describe.

## Never edited here

CONTRIBUTING.md says to leave the folder as upstream wrote it, and to replace both files from one SchemaStore commit instead.[^contributing.md] The pre-commit configuration excludes the folder, so that no hook rewrites a file that the upstream watch matches by git object hash.

## How the schema uses it

`tests/test_schema_rules.py` compares the schema with the copy:[^test_schema_rules.py]

- the `gha_permission` pattern admits every scope and level that SchemaStore's workflow schema lists, refuses the level `admin`, and admits SchemaStore's shorthands;
- the `GhaActionRuntime` enum differs from SchemaStore's runtimes only by `node12` and `node16`, which SchemaStore still accepts and GitHub's metadata syntax page no longer lists;
- the `GhaWorkflowInputType` enum holds the input types that SchemaStore lists;
- the `triggers` pattern admits every event that SchemaStore names;
- the key pattern for a job, an input, an output or a secret, and the `uses` pattern of a calling job, are SchemaStore's.

## The upstream watch

`scripts/check_upstream_release.py` pins the commit as `PINNED_COMMIT`, with each copied file's path in SchemaStore's tree.[^check_upstream_release.py] It compares every copied file with its blob at that commit by git object hash, so it downloads only listings. It reports when SchemaStore's default branch has changed either schema, and when a copied file differs in a way that `KNOWN_DIFFERENCES` does not list. That set is empty, because the copy is exact. [Upstream watch](../workflows/upstream-watch.md) runs the script weekly, and [Move the upstream pins](../playbooks/update-upstream-pins.md) says what to do when it reports.

[^notice]: NOTICE, the section SchemaStore's GitHub Actions schemas, by JSON Schema Store
[^contributing.md]: CONTRIBUTING.md, the Before opening a pull request checklist
[^test_schema_rules.py]: tests/test_schema_rules.py, the first six tests
[^check_upstream_release.py]: scripts/check_upstream_release.py, the docstring, PINNED_COMMIT, FILES and KNOWN_DIFFERENCES
