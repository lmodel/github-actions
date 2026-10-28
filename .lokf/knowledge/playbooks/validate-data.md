---
type: Playbook
id: https://w3id.org/lmodel/github-actions/knowledge/playbooks/validate-data
genre: how-to
title: Validate data against the schema
description: How to check a YAML file against the github-actions schema with linkml-validate (for example with -C GhaReusableWorkflow), what the generated dataclass and Pydantic models check less, and the rules no tool checks, such as a repeated input_id or a read-all that does not stand alone.
resource: docs/index.md
about:
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/github-actions-linkml-schema
sources:
  - id: docs-index.md
    resource: docs/index.md
    title: the Validating data section
  - id: test_data.py
    resource: tests/test_data.py
    title: the validator tests
generated:
  by: process:ktl-librarian
  at: "2026-10-28T19:53:06Z"
  revision: 4c6d307b6b74004e1acabb092ae1ffb14c49c214
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T21:21:37Z"
---

# Validate data against the schema

`docs/index.md` says that `linkml-validate` checks a file against the JSON Schema generated from the schema.[^docs-index.md] Name the class the file holds with `-C`, for example:

```bash
linkml-validate -s src/github_actions/schema/github_actions.yaml -C GhaReusableWorkflow workflow.yaml
```

`tests/test_data.py` holds every example in `tests/data/` to the same validator: a valid example must pass, and a counter-example must fail.[^test_data.py]

## What the generated models check

The models in `src/github_actions/datamodel/` check less, as LinkML 1.12.1 generates them:

- the dataclasses check required fields and enum values, but no pattern or minimum;
- the Pydantic models also check minimums and the patterns a field carries itself, but not those of the `gha_identifier` and `gha_permission` types, so a job, input, output or secret key and a permission go unchecked.

Neither model checks the rules: that a reusable workflow's triggers include `workflow_call`, and that a job that calls a reusable workflow names no runner labels or runner group. So validate a file before loading it into either model.

## What no tool checks

- that a list never repeats a key, such as two inputs with the same `input_id` or two jobs with the same `job_id`;
- that `read-all`, `write-all` or `{}` stands alone in a `permissions` list, and that `id-token` takes `write` or `none`, never `read`;
- that a ruleset whose `requires_check` names a check lists `required_status_checks` among its `rule_types`;
- that only a composite action's outputs carry an `output_expression`.

Python's regular expressions also let a value end in one line break, so `linkml-validate` accepts a permission followed by a newline.

[^docs-index.md]: docs/index.md, the Validating data section
[^test_data.py]: tests/test_data.py, the comment above SCHEMA and the two validator tests
