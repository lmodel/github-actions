---
type: Dataset
id: https://w3id.org/lmodel/github-actions/knowledge/datasets/github-actions-linkml-schema
genre: reference
title: github-actions LinkML schema
description: "The modular LinkML schema of what GitHub Actions workflow files, action metadata files and repository rulesets state (schema id `https://w3id.org/lmodel/github-actions`, version 2026-10-28): `github_actions.yaml` imports a core, a workflow, an action and a rules module, and its `lokf adapt` copy in `.lokf/github-actions.yaml` is the bundle's domain schema."
resource: src/github_actions/schema/github_actions.yaml
version: "2026-10-28"
license: Apache-2.0
derivedFrom:
  - https://w3id.org/lmodel/github-actions/knowledge/references/workflow-syntax
  - https://w3id.org/lmodel/github-actions/knowledge/references/metadata-syntax
  - https://w3id.org/lmodel/github-actions/knowledge/references/rest-api-rules
  - https://w3id.org/lmodel/github-actions/knowledge/references/github-build-type
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/schemastore-copy
sources:
  - id: github_actions.yaml
    resource: src/github_actions/schema/github_actions.yaml
    title: the header's version, source, annotations and comments, and the GhaDocument root
  - id: schema-readme.md
    resource: src/github_actions/schema/README.md
    title: the table of modules
  - id: github_actions_core.yaml
    resource: src/github_actions/schema/github_actions_core.yaml
    title: the core module
  - id: github_actions_workflow.yaml
    resource: src/github_actions/schema/github_actions_workflow.yaml
    title: the workflow module
  - id: github_actions_action.yaml
    resource: src/github_actions/schema/github_actions_action.yaml
    title: the action module
  - id: github_actions_rules.yaml
    resource: src/github_actions/schema/github_actions_rules.yaml
    title: the rules module
  - id: readme.md
    resource: README.md
    title: the What it models and Knowledge Trust Ladder (KTL) sections
  - id: project.justfile
    resource: project.justfile
    title: the lokf-adapt recipes and their roots
  - id: github-actions.yaml
    resource: .lokf/github-actions.yaml
    title: the notes lokf adapt wrote
  - resource: .lokf/justfile
    title: the schema line
generated:
  by: process:ktl-librarian
  at: "2026-10-28T21:21:37Z"
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T22:46:12Z"
---

# github-actions LinkML schema

`src/github_actions/schema/github_actions.yaml` is the umbrella schema, titled "GitHub Actions workflows, actions and repository rulesets". Its header gives `version: "2026-10-28"`, the date GitHub's documentation pages were read, because those pages are versionless.[^github_actions.yaml] The header's `source` is SchemaStore's tree at commit `f7c2f3bcb512651bd980ed6896639ea8ded9ddf0`, and its annotations pin the same commit, the REST API version `2026-03-10` and the reading date. A comment says that `scripts/check_upstream_release.py` reads the same three pins, and that the release tags are the schema's own versions. The schema declares the prefix `gha:` as `https://w3id.org/lmodel/github-actions/` and the license Apache-2.0.

## Modules

The schema directory's README lists the umbrella and four modules.[^schema-readme.md] `LINKML_SCHEMA_NAME` in `config.public.mk` names the umbrella, so the `just` recipes generate from it. The core module imports only `linkml:types`. The workflow and action modules import the core, and the rules module imports the workflow module, because a required check names the workflow that reports it. Each module lints alone, and no module imports the umbrella, so an importer can take one module.

- **`github_actions_core.yaml`** holds what workflows and actions share: the `gha_identifier` type, which is the key form GitHub accepts for a job, an input, an output or a secret; the abstract classes `GhaInput` and `GhaOutput`; and the mixin `GhaRequiredMixin`, which carries `required`.[^github_actions_core.yaml]
- **`github_actions_workflow.yaml`** holds `GhaWorkflow` and its jobs (`GhaWorkflowJob`), and `GhaReusableWorkflow` with `GhaWorkflowInput`, `GhaWorkflowOutput` and `GhaWorkflowSecret`. It also holds the `gha_permission` type and the `GhaWorkflowInputType` and `GhaRunnerEnvironment` enums.[^github_actions_workflow.yaml]
- **`github_actions_action.yaml`** holds `GhaAction` with `GhaActionInput` and `GhaActionOutput`, and the `GhaActionRuntime` enum of the runtimes that `runs.using` may name: `composite`, `docker`, `node20` and `node24`.[^github_actions_action.yaml]
- **`github_actions_rules.yaml`** holds `GhaRepositoryRuleset`, `GhaBypassActor` and `GhaRequiredStatusCheck`, and the `GhaRulesetSourceType`, `GhaRulesetTarget` and `GhaRulesetEnforcement` enums.[^github_actions_rules.yaml]

The umbrella adds only the tree root, `GhaDocument`, which holds the workflows, reusable workflows, actions, rulesets and required checks of one or more repositories. Counted across the five files, the schema defines 16 classes, 6 enums and 2 types, and no subsets.

## What the classes record

- **`GhaWorkflow`** is a workflow file in a repository's `.github/workflows` directory. It records the events under the file's `on` key (`triggers`), the access its `GITHUB_TOKEN` gets (`permissions`) and its jobs (`jobs`). Each job records its runner labels, its runner group and its permissions, or the reusable workflow it calls. `workflow_path` must name a file directly in `.github/workflows`, because GitHub reads no subdirectory of it.
- **`GhaReusableWorkflow`** is a `GhaWorkflow` whose triggers include `workflow_call`. It records the inputs, outputs and secrets under `on.workflow_call`, and names each secret without its value. See [Reusable workflow](../glossary/reusable-workflow.md).
- **`GhaAction`** records the path of an action's `action.yml` or `action.yaml`, the inputs and outputs it declares, and the runtime that executes it (`using`). The metadata file's name and description are the concept's `title` and `description`, so the class adds neither.
- **`GhaRepositoryRuleset`** records a ruleset's target, its enforcement, the refs it includes and excludes, its bypass actors, the type of each rule it holds and the status checks it requires. Of the rules' parameters, only those of `required_status_checks` are modelled. See [Repository ruleset](../glossary/repository-ruleset.md).
- **`GhaRequiredStatusCheck`** records the context a check run must report and the app it must come from. It also records the path of job ids from the top-level workflow's job to the job that reports it, what can skip that job, and `emitted_by`, the workflow whose job reports it. See [Required status check](../glossary/required-status-check.md).

The schema requires `triggers`, `workflow_path` and `jobs` on a workflow, `action_path` and `using` on an action, `ruleset_target` and `enforcement` on a ruleset, and `check_context` on a required check. The README says that `workflow_path`, `workflow_repository` and `runner_environment` are written as GitHub's [build type](../references/github-build-type.md) for SLSA provenance writes them.[^readme.md]

## Rules and patterns

`GhaWorkflowJob` carries two rules: a job that calls a reusable workflow names no runner labels, and it names no runner group. `GhaReusableWorkflow` requires `workflow_call` among its triggers. Patterns hold the keys (`gha_identifier`), the grants (`gha_permission`), event names, rule types, actor types and bypass modes. For each of the last five, a comment says that a pattern stands in for an enumeration because GitHub adds values. [Validate data against the schema](../playbooks/validate-data.md) says which tool checks what.

## Mappings

`GhaWorkflow` has a close mapping to CycloneDX 1.7's `workflow` and a related mapping to SPDX 3.0.1's `Build`, and `triggers` has a related mapping to CycloneDX's `trigger`. `GhaAction` has a close mapping to CycloneDX's `task`, and `GhaRequiredStatusCheck` a related mapping to in-toto's Test Result predicate. [Scope, influences and mappings](../explanations/scope-and-influences.md) says why each mapping is close or related.

## As the bundle's domain schema

A LOKF domain schema is a LinkML schema that imports LOKF's `lokf.yaml` and adds a host's classes and keys, so that `lokf validate` checks the concepts typed with them. The README says that this bundle's domain schema is `.lokf/github-actions.yaml`, a copy that `lokf adapt` wrote from `src/github_actions/schema/github_actions.yaml`. Edit the source, never the copy. `just lokf-adapt` rewrites the copy, and `just lokf-adapt-check` fails when the copy is stale against the schema or `.lokf/lokf.yaml`. The `schema :=` line of `.lokf/justfile` names the copy, so `just lokf-validate` and `just lokf-check-refs` pass it to the validator.

`project.justfile` passes four roots to `lokf adapt`: `GhaWorkflow`, `GhaAction`, `GhaRepositoryRuleset` and `GhaRequiredStatusCheck`. It says that `GhaReusableWorkflow` follows `GhaWorkflow`. It also says that the recipes run the `lokf` that the sidecar's floor pins, 0.9.0 or later, unless `LOKF_CMD` names another.[^project.justfile] The copy's notes say that `lokf adapt` re-rooted the four classes on `lokf:Concept`. It dropped `workflow_uri`, `action_uri`, `ruleset_uri` and `check_uri` for LOKF's `id`, and folded `description` into LOKF's.[^github-actions.yaml] So a concept may name any of the five classes as its `type`, and writes `id` in place of the class's own identifier. The concepts under `workflows/` in this bundle are typed `GhaWorkflow`.

The README lists the five classes for Obsidian users of the KTL Registrar and KTL Curator plugins to add to the *Known LOKF types* setting. It also says that `knowledge-release.yaml` attaches the same copy to a release as `schema-<tag>-github-actions.yaml`, beside the bundle. The workflow attaches it when the bundle has changed since the last release that carries one. The README adds that a release that changes only the schema needs a run by hand with `force`. See [Knowledge Release](../workflows/knowledge-release.md).

[Element names and the shared namespace](../explanations/element-names.md) says why no class, enum or type shares a name with `lokf.yaml` or slsa's copy, and which keys are renamed. The merged copies in `docs/schema/`, the Python models, `project/` and the adapt copy are generated from these files: see [Generated artefacts](generated-artefacts.md).

[^github_actions.yaml]: src/github_actions/schema/github_actions.yaml, the header
[^schema-readme.md]: src/github_actions/schema/README.md, the table of modules
[^github_actions_core.yaml]: src/github_actions/schema/github_actions_core.yaml, the types, slots and classes
[^github_actions_workflow.yaml]: src/github_actions/schema/github_actions_workflow.yaml, the classes, types and enums
[^github_actions_action.yaml]: src/github_actions/schema/github_actions_action.yaml, the classes and the GhaActionRuntime enum
[^github_actions_rules.yaml]: src/github_actions/schema/github_actions_rules.yaml, the classes and enums
[^readme.md]: README.md, the What it models and Knowledge Trust Ladder (KTL) sections
[^project.justfile]: project.justfile, the knowledge bundle recipes
[^github-actions.yaml]: .lokf/github-actions.yaml, the notes at the end
