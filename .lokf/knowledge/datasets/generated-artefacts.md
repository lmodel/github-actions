---
type: Dataset
id: https://w3id.org/lmodel/github-actions/knowledge/datasets/generated-artefacts
genre: reference
title: Generated artefacts
description: "Files generated from the github-actions schema and never edited by hand: project/ (Excel, GraphQL, Java, JSON-LD, JSON Schema, OWL, a prefix map, protobuf, SHACL, ShEx, SQL and TypeScript), the dataclass and Pydantic models in src/github_actions/datamodel/, the two schema files in docs/schema/, the gen-doc pages in docs/elements/ and the domain schema copy .lokf/github-actions.yaml."
resource: project
derivedFrom:
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/github-actions-linkml-schema
sources:
  - id: contributing.md
    resource: CONTRIBUTING.md
    title: the table of paths and the rule to regenerate
  - id: generators.yaml
    resource: .linkml/generators.yaml
    title: the excludes and the generator arguments
  - id: justfile
    resource: justfile
    title: the gen-project, gen-python, gen-doc and _gen-yaml recipes
  - id: project.justfile
    resource: project.justfile
    title: the gen-merged recipe
  - resource: src/github_actions/datamodel
    title: the generated Python models
  - resource: docs/schema
    title: the two schema files
  - resource: docs/elements
    title: the folder gen-doc writes
  - resource: .pre-commit-config.yaml
    title: the exclude list
  - resource: .gitignore
    title: the docs/elements rule
generated:
  by: process:ktl-librarian
  at: "2026-10-28T19:53:06Z"
  revision: 4e47f1efc96b84011e7016edd847a71bfc692a33
status: draft
---

# Generated artefacts

These files are generated from the schema in `src/github_actions/schema/` and never edited by hand. CONTRIBUTING.md asks that the output be committed after each schema edit.[^contributing.md] The pre-commit configuration excludes them, so that no hook rewrites what the next run would rewrite back.

## project/

`just gen-project` runs LinkML's `gen-project` with `.linkml/generators.yaml`, which skips the markdown generator and merges imports for the others.[^generators.yaml] The recipe then moves the Python output into `src/github_actions/datamodel/`, writes the Pydantic model with `gen-pydantic`, and runs `gen-java`, `gen-typescript` and `gen-owl` on their own, because some generators ignore the configuration file or cannot create directories.[^justfile] `project/` holds one folder for each of `excel`, `graphql`, `java` (one file per class), `jsonld` (the context and the schema), `jsonschema`, `owl`, `prefixmap`, `protobuf`, `shacl`, `shex`, `sqlschema` and `typescript`.

## The Python models

`src/github_actions/datamodel/github_actions.py` holds the dataclasses, and `github_actions_pydantic.py` holds the Pydantic models. [Validate data against the schema](../playbooks/validate-data.md) says what each checks.

## docs/schema/ and docs/elements/

`just gen-doc` writes `docs/schema/github_actions.yaml` with `gen-yaml`, and the schema's Markdown pages into `docs/elements/`. `project.justfile` says that the first file folds in the modules' elements but keeps the `imports:` list, so a tool that loads it looks for the modules beside it.[^project.justfile] `just gen-merged`, run after `gen-doc`, writes `docs/schema/github_actions_merged.yaml`, which has no imports at all, for vendoring or loading offline. Git ignores the pages in `docs/elements/`, and the [documentation site](../services/documentation-site.md) builds them when it needs them.

## The domain schema copy

`just lokf-adapt` writes `.lokf/github-actions.yaml`, the bundle's domain schema, and `just lokf-adapt-check` fails when it is stale. [github-actions LinkML schema](github-actions-linkml-schema.md) says what the copy changes.

[^contributing.md]: CONTRIBUTING.md, the table of paths and the first item of Before opening a pull request
[^generators.yaml]: .linkml/generators.yaml, excludes and generator_args
[^justfile]: justfile, the gen-project recipe
[^project.justfile]: project.justfile, the comment above gen-merged
