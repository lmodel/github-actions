# About github-actions

This page is for anyone reading the [LinkML](https://linkml.io) schema's
elements: it says how they are named and what the model leaves out.

Element names are the schema's own. Classes carry the `Gha` prefix
(`GhaWorkflow`, `GhaRequiredStatusCheck`) so they can be imported beside other
vocabularies. Slots are snake_case and named after GitHub's keys, and
permissible values keep GitHub's strings, such as `node24` and `github-hosted`.
A key is renamed only where a knowledge bundle already uses the name:
`input_type` for an input's `type`, `ruleset_target` for a ruleset's `target`
and `check_context` for a check's `context`. Every class and enum links to the
page it renders, and every element is in the `gha:` namespace
(`https://w3id.org/lmodel/github-actions/`).

## What is left out

Runs and their logs are records, not facts of a file, so the model holds no
run, job run or check run, and no workflow `ref`. It models no step of a job,
and no parameter of a ruleset's rules other than its required status checks. It
names secrets and never holds their values.
