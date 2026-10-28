---
type: Explanation
id: https://w3id.org/lmodel/github-actions/knowledge/explanations/scope-and-influences
genre: explanation
title: Scope, influences and mappings
description: "What the github-actions schema renders and leaves out, and why: GitHub's documentation as its source with no single specification behind it, the designs that shaped it (SLSA, the OpenSSF Baseline and Scorecard, otterdog, LOKF and KTL, lmodel/slsa), its close and related mappings to CycloneDX 1.7, SPDX 3.0.1 and in-toto, and the runs, steps and evidence it does not model."
resource: README.md
about:
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/github-actions-linkml-schema
sources:
  - id: readme.md
    resource: README.md
    title: the What it models, Influences, Mappings and Not modelled here sections
  - id: about.md
    resource: docs/about.md
    title: the first paragraph and What is left out
  - id: github_actions_workflow.yaml
    resource: src/github_actions/schema/github_actions_workflow.yaml
    title: the prefixes, mappings and their comments
  - resource: src/github_actions/schema/github_actions_action.yaml
    title: the close mapping of GhaAction
  - resource: src/github_actions/schema/github_actions_rules.yaml
    title: the related mapping and comment of GhaRequiredStatusCheck
generated:
  by: process:ktl-librarian
  at: "2026-10-28T19:53:06Z"
  revision: 67d51bcffa835417e6f4785bb2d9a6945a15d95f
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T20:03:46Z"
---

# Scope, influences and mappings

## What the schema renders

`docs/about.md` says that no single specification stands behind the model.[^about.md] Its sources are GitHub's workflow syntax, metadata syntax and reusable workflows pages, the REST API's rules and check runs pages at version 2026-03-10, and GitHub's build type for SLSA provenance. SchemaStore's JSON Schemas are the machine-readable form of the two files, and a copy of them at a pinned commit sits beside the schema. The README says that the model records what GitHub's documentation says a workflow file, an action's metadata file and a repository ruleset state, so that a knowledge bundle can type them and a script can check them against the files.[^readme.md]

## Influences

The README names what shaped the design, and nothing else:

- **SLSA.** The identity of a workflow comes from GitHub's build type for SLSA provenance, and a reusable workflow that signs provenance is its builder. A required check is a technical control in the sense of SLSA's Source track, so the evidence that a control held is left to lmodel/slsa.
- **The OpenSSF Baseline and Scorecard.** They decided which facts are fields, because their controls read a workflow's inputs, its permissions, the status checks a branch requires and whether a dependency is pinned.
- **otterdog.** It gave the rule that a called job's check is named `caller job / called job`, with a space on each side of the slash, which none of GitHub's pages states.
- **LOKF and the Knowledge Trust Ladder (KTL).** They gave the naming rule, the classes rooted on `Concept`, and the inlined value classes, so that `lokf adapt` needs no `--fold`.
- **lmodel/slsa.** It gave the module layout, the release asset and the governance files.

## Mappings

The README says that the schema names three vocabularies so that a reader can cross to them, and that none of them shaped it.

- **CycloneDX 1.7.** `GhaWorkflow` and `GhaAction` are close to its `workflow` and `task`, and `triggers` is related to its `trigger`.
- **SPDX 3.0.1.** Its `Build` records one run of a build, such as a run of a workflow, so it is a related term for `GhaWorkflow` and not a close one.
- **in-toto's Test Result predicate.** It is the shape of an attestation of what a required check found, so it is a related term for `GhaRequiredStatusCheck` and not a close one.

The workflow module declares the prefixes `cdx:` and `spdx_build:` for the first two, and the rules module names the in-toto predicate by its address.[^github_actions_workflow.yaml]

## Not modelled

- Runs and events, such as CDEvents and GitHub's run logs, are records, not facts of a file. So the model holds no run, job run or check run, and no workflow `ref`.
- GUAC gathers SBOMs, provenance and scores into a graph. The README calls it a consumer of models like this one, not a vocabulary to borrow from.
- SCITT and RATS define how evidence travels and what the word means, and need no class here.
- `docs/about.md` adds that a job's steps are not modelled, nor the parameters of a ruleset's rules other than its required status checks, and that secrets are named, never valued.

[^about.md]: docs/about.md, the first paragraph and What is left out
[^readme.md]: README.md, the What it models, Influences, Mappings and Not modelled here sections
[^github_actions_workflow.yaml]: src/github_actions/schema/github_actions_workflow.yaml, the prefixes and the mappings of GhaWorkflow and triggers
