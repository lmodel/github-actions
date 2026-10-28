# Schema directory

The LinkML schema, as `github_actions.yaml` and the modules it imports:

| File | Holds |
| --- | --- |
| `github_actions.yaml` | The umbrella: imports every module and adds the `GhaDocument` root. Its header pins what the schema renders. The project names this file. |
| `github_actions_core.yaml` | What workflows and actions share: the key form GitHub accepts for a job, an input, an output or a secret, and the inputs and outputs both declare. Imports only `linkml:types`. |
| `github_actions_workflow.yaml` | Workflows and their jobs, and reusable workflows with their inputs, outputs and secrets. |
| `github_actions_action.yaml` | Actions, their inputs and outputs, and the runtimes `runs.using` names. |
| `github_actions_rules.yaml` | Repository rulesets, the actors who may bypass them, and the status checks they require; imports the workflow module, because a check names the workflow that reports it. |
| `schemastore/` | SchemaStore's `github-workflow.json` and `github-action.json` at the pinned commit, with SchemaStore's LICENSE and NOTICE, as `NOTICE` records. Never edited here. |

Each module imports the core, or a module that does, and lints alone; no module imports the umbrella.
