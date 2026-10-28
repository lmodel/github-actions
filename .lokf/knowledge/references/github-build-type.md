---
type: Reference
id: https://w3id.org/lmodel/github-actions/knowledge/references/github-build-type
genre: reference
title: GitHub Actions build type
description: "GitHub's build type for SLSA provenance of a GitHub Actions workflow run (actions.github.io/buildtypes/workflow/v1): the schema writes workflow_path, workflow_repository and runner_environment as it does, and takes from it that a reusable workflow that signs provenance is the build's builder."
resource: https://actions.github.io/buildtypes/workflow/v1
sources:
  - id: readme.md
    resource: README.md
    title: the What it models and Influences sections
  - id: github_actions_workflow.yaml
    resource: src/github_actions/schema/github_actions_workflow.yaml
    title: the GhaWorkflow attributes and comments, the GhaReusableWorkflow comment and the GhaRunnerEnvironment enum
  - id: github_actions_action.yaml
    resource: src/github_actions/schema/github_actions_action.yaml
    title: the GhaAction comment
  - resource: docs/about.md
    title: the list of sources
generated:
  by: process:ktl-librarian
  at: "2026-10-28T19:53:06Z"
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T20:03:46Z"
---

# GitHub Actions build type

`docs/about.md` names GitHub's [build type](https://actions.github.io/buildtypes/workflow/v1) for SLSA provenance among the model's sources. The README says that a workflow's identity in provenance is `workflow_path`, `workflow_repository` and `runner_environment`, as the build type writes them, and that the identity of a workflow comes from the build type.[^readme.md]

The workflow module says how each field follows it:[^github_actions_workflow.yaml]

- `workflow_path` is the file's path from the repository root, as the build type writes `workflow.path`;
- `workflow_repository` is the repository that holds the file, as the build type writes `workflow.repository`: an HTTPS address without `.git`;
- `runner_environment` says whether a job's runner is hosted by GitHub or by the repository's owner, as the build type records it for a run, with the values `github-hosted` and `self-hosted`.

The module's comments add that the build type forms a reusable workflow's `builder.id` from the server's address followed by the job's workflow reference, which names the file and its ref. So a reusable workflow that generates provenance is the builder. The ref at which a run checks out the file belongs to the run, and the build type records it as `workflow.ref`, so the schema does not model it. The action module's comment says that SLSA counts the actions a build runs among its steps, which the tenant defines. It adds that an action is never a build's trust boundary, as a reusable workflow that signs provenance is.[^github_actions_action.yaml]

[^readme.md]: README.md, the What it models and Influences sections
[^github_actions_workflow.yaml]: src/github_actions/schema/github_actions_workflow.yaml, the GhaWorkflow attributes and comments and the GhaReusableWorkflow comment
[^github_actions_action.yaml]: src/github_actions/schema/github_actions_action.yaml, the first GhaAction comment
