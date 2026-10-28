# github-actions

This project is a LinkML model of what GitHub Actions files and repository
rulesets state. It covers workflows and their jobs, reusable workflows with
their inputs, outputs and secrets, actions with their runtimes, and the
rulesets and required status checks that tie a workflow's jobs to the refs a
ruleset protects.

- [Schema documentation](elements/index.md), generated from the schema
- [About](about.md): how the elements are named and what the model leaves out
- [`github_actions.yaml`](schema/github_actions.yaml): the schema with its
  modules' elements folded in
- [`github_actions_merged.yaml`](schema/github_actions_merged.yaml): the same
  with no imports, for vendoring or loading offline

The schema is modular, and an importer may take one module:

- `github_actions_core` holds what workflows and actions share.
- `github_actions_workflow`, `github_actions_action` and `github_actions_rules`
  each hold one kind of file or setting.
- `github_actions.yaml` imports them all and adds the document root.

## Validating data

`linkml-validate -s src/github_actions/schema/github_actions.yaml -C GhaReusableWorkflow workflow.yaml`
checks a file against the JSON Schema generated from the schema, and
`tests/test_data.py` holds every example to it.

Validate a file before loading it into either model in
`src/github_actions/datamodel/`. LinkML 1.12.1 generates models that check
less:

- The dataclasses check required fields and enum values, but no pattern or
  minimum.
- The Pydantic models also check minimums and the patterns a field carries
  itself, but not those of the `gha_identifier` and `gha_permission` types, so
  a job, input, output or secret key and a permission go unchecked.
- Neither checks the rules: that a reusable workflow's triggers include
  `workflow_call`, and that a job that calls a reusable workflow names no
  runner labels or runner group.

No check covers these rules:

- that a list never repeats a key, such as two inputs with the same `input_id`
  or two jobs with the same `job_id`;
- that `read-all`, `write-all` or `{}` stands alone in a `permissions` list,
  and that `id-token` takes `write` or `none`, never `read`;
- that a ruleset whose `requires_check` names a check lists
  `required_status_checks` among its `rule_types`;
- that only a composite action's outputs carry an `output_expression`.

Python's regular expressions also let a value end in one line break, so
`linkml-validate` accepts a permission followed by a newline.
