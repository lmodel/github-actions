---
type: Explanation
id: https://w3id.org/lmodel/github-actions/knowledge/explanations/element-names
genre: explanation
title: Element names and the shared namespace
description: "Why the github-actions schema names its elements as it does: the Gha prefix, snake_case slots after GitHub's keys, GitHub's own strings as permissible values, and no class, enum or type name shared with LOKF's lokf.yaml or slsa's adapt copy, because a host merges the three into one namespace; input_type, ruleset_target and check_context are the renamed keys."
resource: docs/about.md
about:
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/github-actions-linkml-schema
sources:
  - id: about.md
    resource: docs/about.md
    title: the naming paragraph
  - id: readme.md
    resource: README.md
    title: the Knowledge Trust Ladder (KTL) section
  - id: linkmllint.yaml
    resource: .linkmllint.yaml
    title: the comment and the standard_naming rule
  - id: github_actions_core.yaml
    resource: src/github_actions/schema/github_actions_core.yaml
    title: the comments on description and required
  - id: test_schema_rules.py
    resource: tests/test_schema_rules.py
    title: test_names_apart_from_lokf_and_slsa
  - resource: CONTRIBUTING.md
    title: the rules on names and conventions
generated:
  by: process:ktl-librarian
  at: "2026-10-28T19:53:06Z"
  revision: 4e47f1efc96b84011e7016edd847a71bfc692a33
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T20:03:46Z"
---

# Element names and the shared namespace

## The names GitHub gives

`docs/about.md` says that the schema's element names are its own.[^about.md] Classes carry the `Gha` prefix, such as `GhaWorkflow` and `GhaRequiredStatusCheck`, so that they can be imported beside other vocabularies. Slots are snake_case and named after GitHub's keys. Permissible values keep GitHub's strings, such as `node24` and `github-hosted`. Every class and enum links to the page it renders, and every element lives under `gha:`, which is `https://w3id.org/lmodel/github-actions/`.

`.linkmllint.yaml` keeps LinkML's recommended lint rules but lowers `standard_naming` to a warning.[^linkmllint.yaml] Its comment says that the permissible values are written as GitHub writes them (`node20`, `github-hosted`, `Repository`), so that a script compares a concept with a workflow file or a REST response without translating. It adds that no one case convention holds for all of them.

## Three schemas in one namespace

The README says that a host imports the schema's adapt copy beside `lokf.yaml` and slsa's copy, and that LinkML merges the three into one namespace, where the last definition of a name wins silently.[^readme.md] So no class, enum or type shares a name with either, and a slot shares a name only where it shares LOKF's meaning and IRI: `description` and `required`.

The core module's comments say how those two stay apart.[^github_actions_core.yaml] The `description` slot carries the IRI `schema:description`, so `lokf adapt` folds it into LOKF's slot and a bundle reads one `description` key. `required` is an attribute of `GhaRequiredMixin` rather than a slot, with the IRI `schema:valueRequired`, because `lokf adapt` keeps an attribute's name where it would rename a slot that shares one with `lokf.yaml`.

Where GitHub's key is a name LOKF already defines, the schema renames the slot:

- `input_type` for an input's `type`, because a bundle reads `type` as the class of the concept;
- `ruleset_target` for a ruleset's `target`;
- `check_context` for a required check's `context`.

In the adapt copy, LOKF's `id` stands in for each class's own identifier (`workflow_uri`, `action_uri`, `ruleset_uri` and `check_uri`), and an action's name and description are the concept's `title` and `description`.

## How the rule is checked

`test_names_apart_from_lokf_and_slsa` in `tests/test_schema_rules.py` reads `.lokf/github-actions.yaml`, `.lokf/lokf.yaml` and `tests/neighbours/slsa.yaml`.[^test_schema_rules.py] It fails when a class, enum, type or subset name appears in the copy and in a neighbour, or when a slot or attribute name they share expands to a different IRI. CONTRIBUTING.md asks contributors to keep names apart from LOKF's and slsa's for the same reason.

[^about.md]: docs/about.md, the third paragraph
[^linkmllint.yaml]: .linkmllint.yaml, the comment and rules
[^readme.md]: README.md, the Knowledge Trust Ladder (KTL) section
[^github_actions_core.yaml]: src/github_actions/schema/github_actions_core.yaml, the comments on description and on required
[^test_schema_rules.py]: tests/test_schema_rules.py, test_names_apart_from_lokf_and_slsa
