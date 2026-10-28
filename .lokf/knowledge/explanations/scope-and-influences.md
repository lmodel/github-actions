---
type: Explanation
id: https://w3id.org/lmodel/github-actions/knowledge/explanations/scope-and-influences
genre: explanation
title: Scope, influences and mappings
description: "What the github-actions schema renders and leaves out, and why: GitHub's documentation as its source, the designs that shaped it (SLSA, the OpenSSF Baseline and Scorecard, otterdog, LOKF and KTL, lmodel/slsa), its close and related mappings to CycloneDX 1.7, SPDX 3.0.1 and in-toto, and the runs, steps and evidence it does not model."
resource: README.md
about:
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/github-actions-linkml-schema
sources:
  - id: readme.md
    resource: README.md
    title: the What it models, Influences, Mappings and Not modelled here sections
  - id: about.md
    resource: docs/about.md
    title: the What is left out section
  - id: github_actions_workflow.yaml
    resource: src/github_actions/schema/github_actions_workflow.yaml
    title: the prefixes, mappings and their comments
  - resource: src/github_actions/schema/github_actions_action.yaml
    title: the close mapping of GhaAction
  - id: github_actions_rules.yaml
    resource: src/github_actions/schema/github_actions_rules.yaml
    title: the prefixes, the related mapping and the comment of GhaRequiredStatusCheck
generated:
  by: process:ktl-librarian
  at: "2026-10-28T22:46:12Z"
  revision: 8ec02d94004392285d419058b78e894d0d0d7802
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T20:03:46Z"
---

# Scope, influences and mappings

## What the schema renders

The README says that the schema models what GitHub's documentation says about workflows, reusable workflows, actions, rulesets and required checks, and about a workflow's identity in provenance.[^readme.md] It names the source of each class: GitHub's workflow syntax, reusable workflows and metadata syntax pages, the REST API's rules and check runs pages at version 2026-03-10, and GitHub's build type for SLSA provenance.

The schema header pins the REST API version and the SchemaStore commit of `github-workflow.json` and `github-action.json`, which are copied into `src/github_actions/schema/schemastore/`. A weekly workflow opens an issue when either changes.

## Influences

The README names what shaped the design:

- **SLSA.** A workflow's identity comes from GitHub's build type for SLSA provenance, where a reusable workflow that signs provenance is the `builder`. A required check is a technical control of SLSA's Source track, so lmodel/slsa holds the evidence that it held.
- **The OpenSSF Baseline and Scorecard.** Their controls read a workflow's inputs, its permissions, a branch's required status checks and dependency pinning, so those facts are fields.
- **otterdog.** It gave the rule that a called job's check is named `caller job / called job`, with a space on each side of the slash.
- **LOKF and the Knowledge Trust Ladder (KTL).** They gave the naming rule, the classes rooted on `Concept`, and the inlined value classes, which let `lokf adapt` run without `--fold`.
- **lmodel/slsa.** It gave the module layout, the release asset and the governance files.

## Mappings

The README says that the schema maps to three vocabularies.

- **CycloneDX 1.7.** `GhaWorkflow` and `GhaAction` are close to its `workflow` and `task`, and `triggers` is related to its `trigger`.
- **SPDX 3.0.1.** Its `Build` records a run of a workflow, so it is a related term for `GhaWorkflow`, not a close one.
- **in-toto's Test Result predicate.** It records what a required check found, so it is a related term for `GhaRequiredStatusCheck`, not a close one.

The workflow module declares the prefixes `cdx:` and `spdx_build:` for the first two.[^github_actions_workflow.yaml] The rules module declares `in_toto:` as `https://in-toto.io/attestation/` and names the predicate `in_toto:test-result/v0.1`.[^github_actions_rules.yaml]

## Not modelled

- Runs and events, such as CDEvents and GitHub's run logs, are records, not facts of a file. `docs/about.md` adds that the model holds no run, job run or check run, and no workflow `ref`.[^about.md]
- GUAC, a graph of SBOMs, provenance and scores, consumes models like this one.
- SCITT and RATS define how evidence is carried and what it means, and need no class here.
- `docs/about.md` also says that the model has no step of a job and no parameter of a ruleset's rules other than its required status checks, and that it names secrets and never holds their values.

[^readme.md]: README.md, the What it models, Influences, Mappings and Not modelled here sections
[^about.md]: docs/about.md, the What is left out section
[^github_actions_workflow.yaml]: src/github_actions/schema/github_actions_workflow.yaml, the prefixes and the mappings of GhaWorkflow and triggers
[^github_actions_rules.yaml]: src/github_actions/schema/github_actions_rules.yaml, the prefixes and the related mapping of GhaRequiredStatusCheck
