# github-actions

A LinkML model of what GitHub Actions files and repository rulesets state:
workflows and their jobs, reusable workflows with their inputs, outputs and
secrets, actions with their runtimes, and the rulesets and required status
checks that tie a workflow's jobs to the refs a ruleset protects.

- [Schema documentation](elements/index.md), generated from the schema
- [About](about.md): what the model renders and where its elements come from
- [`github_actions.yaml`](schema/github_actions.yaml): the schema with its
  modules' elements folded in, and
  [`github_actions_merged.yaml`](schema/github_actions_merged.yaml): the same
  with no imports, for vendoring or loading offline

The schema is modular. `github_actions_core` holds what workflows and actions
share; `github_actions_workflow`, `github_actions_action` and
`github_actions_rules` each hold one kind of file or setting; and
`github_actions.yaml` imports them all and adds the document root. An
importer may take one module.

## Validating data

`linkml-validate -s src/github_actions/schema/github_actions.yaml -C GhaReusableWorkflow workflow.yaml`
checks a file against the JSON Schema generated from the schema. The models in
`src/github_actions/datamodel/` check less. The dataclasses check required
fields and enum values but no patterns. The Pydantic models also check
patterns, but they leave out the rules: that a reusable workflow's triggers
include `workflow_call`, and that a job that calls a reusable workflow names
no runner labels or runner group. Validate a file before loading it into
either model.

Some rules have no check at all:

- that a list never repeats a key, such as two inputs with the same
  `input_id` or two jobs with the same `job_id`;
- that `read-all`, `write-all` or `{}` stands alone in a `permissions` list,
  and that `id-token` takes `write` or `none`, never `read`;
- that a ruleset whose `requires_check` names a check lists
  `required_status_checks` among its `rule_types`;
- that only a composite action's outputs carry an `output_expression`.

Python's regular expressions also let a value end in one line break, so
`linkml-validate` accepts a permission followed by a newline.
