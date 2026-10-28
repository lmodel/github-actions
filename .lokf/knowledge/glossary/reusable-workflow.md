---
type: GlossaryTerm
id: https://w3id.org/lmodel/github-actions/knowledge/glossary/reusable-workflow
genre: reference
title: Reusable workflow
definition: A workflow that other workflows call as a job, because its on key names workflow_call; it declares the inputs, outputs and secrets that its callers pass and read.
description: A workflow that other workflows call as a job because its on key names workflow_call, declaring the inputs, outputs and secrets its callers pass and read; the schema models it as GhaReusableWorkflow, and a calling job names it in uses with no runs-on or runner group.
resource: src/github_actions/schema/github_actions_workflow.yaml
definedBy:
  - https://w3id.org/lmodel/github-actions/knowledge/references/workflow-syntax
sources:
  - id: github_actions_workflow.yaml
    resource: src/github_actions/schema/github_actions_workflow.yaml
    title: GhaReusableWorkflow, GhaWorkflowJob, GhaWorkflowInput, GhaWorkflowOutput, GhaWorkflowSecret and GhaWorkflowInputType
  - id: github_actions_core.yaml
    resource: src/github_actions/schema/github_actions_core.yaml
    title: GhaInput, GhaOutput and gha_identifier
  - resource: .github/workflows
    title: the on key of each workflow
generated:
  by: process:ktl-librarian
  at: "2026-10-28T19:53:06Z"
  revision: 4e47f1efc96b84011e7016edd847a71bfc692a33
status: draft
---

# Reusable workflow

The workflow module defines a reusable workflow as a workflow that other workflows call as a job, because its `on` key names `workflow_call`. It declares the inputs, outputs and secrets that its callers pass and read.[^github_actions_workflow.yaml] The schema models it as `GhaReusableWorkflow`, a subclass of `GhaWorkflow` that requires `workflow_call` among its triggers.

## What it declares

- **Inputs**, under `on.workflow_call.inputs`. Each has an `input_id`, the key a caller writes in its `with` map, and must state its `input_type`: `boolean`, `number` or `string`. It may give a `description`, say whether it is `required`, and give a `default`, which is written as a string even where the type is a boolean or a number.[^github_actions_core.yaml]
- **Outputs**, under `on.workflow_call.outputs`. Each has an `output_id` and an `output_expression`, the file's `value` key, which sets the output from an output of one of its jobs.
- **Secrets**, under `on.workflow_call.secrets`. Each is recorded by its `secret_id` alone, and its value never is.

The keys of jobs, inputs, outputs and secrets follow the `gha_identifier` pattern: a letter or an underscore, then letters, digits, hyphens or underscores.

## How a job calls it

A calling job names the file in its `uses` key, recorded as `calls`: `./.github/workflows/<file>` in the same repository, or `<owner>/<repo>/.github/workflows/<file>@<ref>`. Such a job names no runner labels and no runner group, because the called workflow's jobs choose their own runners. A called workflow can lower its token's access, never raise it.

When a reusable workflow generates provenance, it is the build's builder: see [GitHub Actions build type](../references/github-build-type.md).

## In this repository

None of the nine workflows under `.github/workflows/` names `workflow_call`, so the repository holds no reusable workflow.

[^github_actions_workflow.yaml]: src/github_actions/schema/github_actions_workflow.yaml, GhaReusableWorkflow, GhaWorkflowJob and the input, output and secret classes
[^github_actions_core.yaml]: src/github_actions/schema/github_actions_core.yaml, GhaInput, GhaOutput and gha_identifier
