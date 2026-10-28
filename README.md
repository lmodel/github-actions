<a href="https://github.com/linkml/linkml-project-copier"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-teal.json" alt="Copier Badge" style="max-width:100%;"/></a>

# github-actions

GitHub Actions workflows, actions and repository rulesets (LinkML)

> **Two ways in.** This README is one; the other is a docent, a museum's name
> for a guide. Install
> [`ktl-docent`](https://github.com/noelmcloughlin/knowledge-trust-ladder) into
> whatever agent you already use, by a route from
> [the install page](https://w3id.org/ktl/docs/install/), and ask it anything
> about this project, such as which status checks a ruleset can require. It
> answers from `.lokf/knowledge/`, the checked part of what the project knows,
> and says how far each answer has been trusted (still a draft, checked by
> automation only, or confirmed by a named person). It opens the source for
> exact values, and records what it could not answer so the gap gets filled.
> The same docent serves a person at a prompt, an agent reading this file, or
> a chatbot that can load a skill.
>
> **Agents:** if `.lokf/knowledge/index.md` exists, read it first. `llms.txt`
> says how to weigh it.

## Documentation Website

[https://lmodel.github.io/github-actions](https://lmodel.github.io/github-actions)

## What it models

What GitHub's documentation says a workflow file, an action's metadata file and a repository ruleset state, so that a knowledge bundle can type them and a script can check them against the files:

* **Workflows** (`GhaWorkflow`): the events that run one, the access its `GITHUB_TOKEN` gets, and its jobs, each with its runner labels, runner group and permissions, or the reusable workflow it calls. From the [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) page.
* **Reusable workflows** (`GhaReusableWorkflow`): the inputs, outputs and secrets under `on.workflow_call`. From the workflow syntax and [reusable workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations) pages.
* **Actions** (`GhaAction`): the inputs and outputs of an `action.yml`, and the runtime `runs.using` names. From the [metadata syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax) page.
* **Rulesets and required checks** (`GhaRepositoryRuleset`, `GhaRequiredStatusCheck`): a ruleset's target, enforcement, ref conditions, bypass actors and rule types, and each status check it requires, tied by `emitted_by` to the workflow whose job reports it. From the REST API's [rules](https://docs.github.com/en/rest/repos/rules) and [check runs](https://docs.github.com/en/rest/checks/runs) at version 2026-03-10.
* **A workflow's identity in provenance**: `workflow_path`, `workflow_repository` and `runner_environment`, as GitHub's [build type](https://actions.github.io/buildtypes/workflow/v1) writes them.

GitHub's pages are versionless, so the schema's `version` is the date they were read, 2026-10-28. The schema header also pins the REST API version and the SchemaStore commit whose `github-workflow.json` and `github-action.json` are copied, as their machine-readable form, into [src/github_actions/schema/schemastore/](src/github_actions/schema/schemastore). A weekly workflow opens an issue when either changes. The release tags number the schema's versions.

## Influences

No single specification stands behind this schema. These shaped its design:

* **SLSA**: the identity of a workflow comes from GitHub's build type for SLSA provenance, and a reusable workflow that signs provenance is its `builder`. A required check is a technical control in the sense of SLSA's Source track, so the evidence that a control held is left to [lmodel/slsa](https://github.com/lmodel/slsa).
* **The OpenSSF Baseline and Scorecard**: their controls read a workflow's inputs, its permissions, the status checks a branch requires and whether a dependency is pinned, so those facts are fields.
* **otterdog**: the rule that a called job's check is named `caller job / called job`, with a space on each side of the slash. None of GitHub's pages states it.
* **LOKF and KTL**: the naming rule below, the classes rooted on `Concept`, and the inlined value classes, which let `lokf adapt` run without `--fold`.
* **lmodel/slsa**: the module layout, the release asset and the governance files.

## Mappings

The schema maps to three vocabularies that did not shape it, so a reader can cross to them. `GhaWorkflow` and `GhaAction` are close to [CycloneDX 1.7](https://cyclonedx.org/specification/overview/)'s `workflow` and `task`, and its `trigger` is related to `triggers`. [SPDX 3.0.1](https://spdx.github.io/spdx-spec/v3.0.1/)'s `Build` records a run of a workflow, and in-toto's [Test Result](https://github.com/in-toto/attestation/blob/main/spec/predicates/test-result.md) predicate records what a required check found. Both are related terms, not close ones.

## Not modelled here

Runs and events, such as CDEvents and GitHub's run logs, are records, not facts of a file. GUAC is a graph that gathers SBOMs, provenance and scores: it consumes models like this one and offers no vocabulary to borrow. SCITT and RATS define how evidence is carried and what evidence means, and need no class here.

## Deriving the facts from a repository

`scripts/derive.py` reads a repository's workflow files and action metadata files with `yaml.safe_load`, and nothing else. It prints:

* the frontmatter of the concept that describes each file;
* the name of each check run a top-level workflow's jobs report, which is the `check_context` a ruleset requires, with the job path and what can skip the job;
* what the OpenSSF Baseline and Scorecard call out: write access at a workflow's top level, a caller that passes `secrets: inherit`, and a `uses` not pinned to a commit.

With `--check` and a bundle, it exits 1 on drift between the files and the concepts, or on a required check that no job of its `emitted_by` workflow reports.

```bash
uv run scripts/derive.py --root ../host-repository
uv run scripts/derive.py --root ../host-repository --check ../host-repository/.lokf/knowledge
```

Its only dependency is PyYAML, named in its PEP 723 header, so `uv run` needs no project. A host copies the script at a pinned release of this repository and records the version beside it. The fixtures under [tests/derive/](tests/derive/) show each rule.

## Repository Structure

* [docs/](docs/): the documentation pages the website shows
  * [elements/](docs/elements/): generated schema documentation
* [examples/](examples/): examples of using the schema
* [project/](project/): generated project files (do not edit them)
* [scripts/](scripts/): the upstream watch and the derivation script
* [src/](src/): source files (edit these)
  * [github_actions](src/github_actions)
    * [schema/](src/github_actions/schema): the LinkML schema, `github_actions.yaml` and
      the modules it imports (edit these)
    * [datamodel/](src/github_actions/datamodel): generated
      Python datamodel
* [tests/](tests/): Python tests
  * [data/](tests/data): example data
* [website/](website/): the documentation website, an Astro Starlight site built from the README, `docs/`, the schema's pages and the knowledge bundle

## Developer Tools

The project's commands are [just](https://github.com/casey/just/) recipes. Run `just` or `just --list` to list them.

## Knowledge Trust Ladder (KTL)

`.lokf/` holds this project's [KTL](https://w3id.org/ktl/) knowledge bundle. Its domain schema is `.lokf/github-actions.yaml`, a copy that `lokf adapt` writes from `src/github_actions/schema/github_actions.yaml`. Edit the source, never the copy. `knowledge-release.yaml` attaches the copy to a release as `schema-<tag>-github-actions.yaml`, beside the bundle, when the bundle has changed since the last release that carries one. For a release that changes only the schema, run that workflow by hand with `force`.

`just lokf-adapt` rewrites the copy, and `just lokf-adapt-check` says when it is stale. `project.justfile` names the classes the copy roots on `Concept`. A concept may name any of them, or a subclass, as its `type`. If you use the KTL Registrar and KTL Curator plugins in Obsidian, add these classes to their *Known LOKF types* setting:

```text
GhaWorkflow, GhaReusableWorkflow, GhaAction, GhaRepositoryRuleset, GhaRequiredStatusCheck
```

In the copy, LOKF's `id` stands in for each class's identifier (`workflow_uri`, `action_uri`, `ruleset_uri` and `check_uri`), so a concept writes `id`. An action's name and description are the concept's `title` and `description`.

A host imports the copy beside `lokf.yaml` and slsa's copy, and LinkML merges the three into one namespace, where the last definition of a name wins silently. So no class, enum or type shares a name with either, and a slot shares a name only where it carries LOKF's meaning and IRI: `description` and `required`. Where GitHub's key is a name LOKF already defines, the slot is renamed: `input_type` for `type`, `ruleset_target` for `target` and `check_context` for `context`. `tests/test_schema_rules.py` checks the rule against both neighbours.

## License

The schema and the code are under the Apache License 2.0 ([LICENSE](LICENSE)).

The repository also carries SchemaStore's two schemas in [src/github_actions/schema/schemastore/](src/github_actions/schema/schemastore), under their own notice. GitHub's documentation is cited, never copied. See [NOTICE](NOTICE).

This is not an official GitHub project, and its use does not imply endorsement by GitHub.

## Contributing and security

[CONTRIBUTING.md](CONTRIBUTING.md) is the checklist for a pull request and
for releasing. [AI_COVENANT.md](AI_COVENANT.md) sets the rules for AI-assisted
work. [SECURITY.md](SECURITY.md) says how to report a vulnerability.
[CHANGELOG.md](CHANGELOG.md) records the changes.

## Credits

This project uses the template [linkml-project-copier](https://github.com/linkml/linkml-project-copier) published as [doi:10.5281/zenodo.15163584](https://doi.org/10.5281/zenodo.15163584).
