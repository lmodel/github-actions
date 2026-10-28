# About github-actions

This project is a [LinkML](https://linkml.io) model of what GitHub's
documentation says a GitHub Actions workflow file, an action's metadata file
and a repository ruleset state. No single specification stands behind it.
Its sources are GitHub's
[workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax),
[metadata syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax)
and [reusable workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations)
pages, the REST API's [rules](https://docs.github.com/en/rest/repos/rules)
and [check runs](https://docs.github.com/en/rest/checks/runs) at version
2026-03-10, and GitHub's
[build type](https://actions.github.io/buildtypes/workflow/v1) for SLSA
provenance. SchemaStore's JSON Schemas for the two files are their
machine-readable form, and a copy of them at a pinned commit sits beside the
schema in `src/github_actions/schema/schemastore/`.

GitHub's pages are versionless, so the schema's `version` is the date they
were read, 2026-10-28. The schema header also pins the SchemaStore commit and
the REST API version, and a weekly workflow opens an issue when either moves.

Element names are the schema's own: classes carry the `Gha` prefix
(`GhaWorkflow`, `GhaRequiredStatusCheck`) so they can be imported beside other
vocabularies, slots are snake_case and named after GitHub's keys, and
permissible values keep GitHub's strings, such as `node24` and
`github-hosted`. A key is renamed only where a knowledge bundle already uses
the name: `input_type` for an input's `type`, `ruleset_target` for a
ruleset's `target` and `check_context` for a check's `context`. Every class
and enum links to the page it renders, and every element lives under `gha:`
(`https://w3id.org/lmodel/github-actions/`).

## What is left out

Runs and their logs are records, not facts of a file, so the model holds no
run, job run or check run, and no workflow `ref`. A step of a job is not
modelled, nor are the parameters of a ruleset's rules other than its required
status checks. Secrets are named, never valued.
