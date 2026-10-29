<a href="https://github.com/linkml/linkml-project-copier"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-teal.json" alt="Copier Badge" style="max-width:100%;"/></a>

# github-actions

GitHub Actions workflows, actions and repository rulesets (LinkML)

> **Only want to ask?** Install `ktl-docent` into any agent you use, by a route from [the install page](https://w3id.org/ktl/docs/install/), and ask it about this project. It answers from the bundle and says how far each answer has been checked.
>
> **Agents:** if `.lokf/knowledge/index.md` exists, read it first. `llms.txt` says how to weigh it.

## Documentation Website

[https://lmodel.github.io/github-actions](https://lmodel.github.io/github-actions)

## What it models

From GitHub's documentation:

* **Workflows** (`GhaWorkflow`, from [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)): the events that run one, the access its `GITHUB_TOKEN` gets, and its jobs, each with its runner labels, runner group and permissions, or the reusable workflow it calls.
* **Reusable workflows** (`GhaReusableWorkflow`, from workflow syntax and [reusable workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations)): the inputs, outputs and secrets under `on.workflow_call`.
* **Actions** (`GhaAction`, from [metadata syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax)): the inputs and outputs of an `action.yml`, and the runtime `runs.using` names.
* **Rulesets and required checks** (`GhaRepositoryRuleset` and `GhaRequiredStatusCheck`, from the REST API's [rules](https://docs.github.com/en/rest/repos/rules) and [check runs](https://docs.github.com/en/rest/checks/runs) at version 2026-03-10): a ruleset's target, enforcement, ref conditions, bypass actors and rule types, and each status check it requires. `emitted_by` ties a check to the workflow whose job reports it.
* **A workflow's identity in provenance**: `workflow_path`, `workflow_repository` and `runner_environment`, as GitHub's [build type](https://actions.github.io/buildtypes/workflow/v1) writes them.

GitHub's pages are versionless, so the schema's `version` is their retrieval date, 2026-10-28. The schema header pins the REST API version and the SchemaStore commit of the `github-workflow.json` and `github-action.json` copied into [src/github_actions/schema/schemastore/](src/github_actions/schema/schemastore). A weekly workflow opens an issue when either changes. Release tags number the schema's versions.

## Influences

These shaped the schema's design:

* **SLSA**: a workflow's identity comes from GitHub's build type for SLSA provenance, where a reusable workflow that signs provenance is the `builder`. A required check is a technical control of SLSA's Source track, so [lmodel/slsa](https://github.com/lmodel/slsa) holds the evidence that it held.
* **The OpenSSF Baseline and Scorecard**: their controls read a workflow's inputs, its permissions, a branch's required status checks and dependency pinning, so those facts are fields.
* **otterdog**: a called job's check is named `caller job / called job`, spaced around the slash.
* **LOKF and KTL**: the naming rule below, the classes rooted on `Concept`, and the inlined value classes, which let `lokf adapt` run without `--fold`.
* **lmodel/slsa**: the module layout, the release asset and the governance files.

## Mappings

The schema maps to three vocabularies. `GhaWorkflow` and `GhaAction` are close to [CycloneDX 1.7](https://cyclonedx.org/specification/overview/)'s `workflow` and `task`, and its `trigger` is related to `triggers`. [SPDX 3.0.1](https://spdx.github.io/spdx-spec/v3.0.1/)'s `Build` records a run of a workflow, and in-toto's [Test Result](https://github.com/in-toto/attestation/blob/main/spec/predicates/test-result.md) predicate records what a required check found. Both are related terms, not close ones.

## Not modelled here

Runs and events, such as CDEvents and GitHub's run logs, are records, not facts of a file. GUAC, a graph of SBOMs, provenance and scores, consumes models like this one. SCITT and RATS, which define how evidence is carried and what it means, need no class here.

## Deriving the facts from a repository

`scripts/derive.py` reads a repository's workflow and action metadata files with `yaml.safe_load`. It prints:

* the frontmatter of the concept that describes each file;
* the name of each check run a top-level workflow's jobs report (the `check_context` a ruleset requires), with the job path and what can skip the job;
* what the OpenSSF Baseline and Scorecard call out: write access at a workflow's top level, a caller that passes `secrets: inherit`, and a `uses` not pinned to a commit.

With `--check` and a bundle, it exits 1 on drift between the files and the concepts, on a required check that no job of its `emitted_by` workflow reports, or on a skip condition that a check's body does not name. Each skip condition is a finding, which fails the check under `--strict`. A job skipped by its own `if`, or by a failed or skipped job it `needs`, lets a required check pass without running. A path filter, or a calling job's `if` or `needs`, leaves the check pending, which blocks the merge.

`scripts/github_export.py` asks GitHub's REST API what the files cannot say. `rulesets` prints the repository's rulesets and the rules in effect on its default branch, which `derive.py --rulesets` compares with the ruleset and check concepts. `check-runs` prints what GitHub recorded on one commit, such as the head of a recent pull request, and `derive.py --check-runs` reports each required check that no run on it matched. On a private repository, `GH_TOKEN` holds a token with Metadata read, and Checks and Commit statuses read for `check-runs`.

```bash
uv run scripts/derive.py --root ../host-repository
uv run scripts/derive.py --root ../host-repository --check ../host-repository/.lokf/knowledge
python3 scripts/github_export.py rulesets --repository OWNER/REPO > rulesets.md
python3 scripts/github_export.py check-runs SHA --repository OWNER/REPO > check-runs.md
uv run scripts/derive.py --root ../host-repository --check ../host-repository/.lokf/knowledge \
  --rulesets rulesets.md --check-runs check-runs.md
```

derive.py's only dependency, PyYAML, is declared in its PEP 723 header, so `uv run` needs no project, and github_export.py needs Python 3.10 alone. A host copies both from a pinned release and records the version beside them. Its ingest can run `github_export.py rulesets` as an entry of `kind: command`, and the mirror file becomes the rulesets' source. The fixtures in [tests/derive/](tests/derive/) show each rule.

## Repository Structure

* [docs/](docs/): the website's pages, with the generated schema pages in [elements/](docs/elements/)
* [examples/](examples/): usage examples
* [project/](project/): generated project files (do not edit them)
* [scripts/](scripts/): the upstream watch, the derivation script and the export script
* [src/github_actions/schema/](src/github_actions/schema): the LinkML schema, `github_actions.yaml` and the modules it imports (edit these)
* [src/github_actions/datamodel/](src/github_actions/datamodel): the generated Python datamodel
* [tests/](tests/): Python tests, with example data in [data/](tests/data)
* [website/](website/): the Astro Starlight site built from the README, `docs/`, the schema's pages and the knowledge bundle

## Developer Tools

Run `just` to list the project's [just](https://github.com/casey/just/) recipes.

## Knowledge Trust Ladder (KTL)

`.lokf/` holds this project's [KTL](https://w3id.org/ktl/) knowledge bundle. Its domain schema is `.lokf/github-actions.yaml`, which `lokf adapt` writes from `src/github_actions/schema/github_actions.yaml`. Edit the source, never the copy. A release carries the copy as `schema-<tag>-github-actions.yaml`, on the terms [CONTRIBUTING.md](CONTRIBUTING.md#releasing-maintainers) gives.

`just lokf-adapt` rewrites the copy, and `just lokf-adapt-check` says when it is stale. `project.justfile` names the classes the copy roots on `Concept`, and a concept may name any of them, or a subclass, as its `type`. In Obsidian, add these classes to the KTL Registrar and KTL Curator plugins' *Known LOKF types* setting:

```text
GhaWorkflow, GhaReusableWorkflow, GhaAction, GhaRepositoryRuleset, GhaRequiredStatusCheck
```

In the copy, LOKF's `id` replaces each class's identifier (`workflow_uri`, `action_uri`, `ruleset_uri` and `check_uri`), and an action's name and description are the concept's `title` and `description`.

A host imports the copy beside `lokf.yaml` and slsa's copy, and LinkML merges the three into one namespace, where the last definition of a name wins silently. So no class, enum or type shares a name with either. A slot shares a name only where it carries LOKF's meaning and IRI (`description` and `required`), and [docs/about.md](docs/about.md) lists the slots renamed to avoid LOKF's names. `tests/test_schema_rules.py` checks both neighbours.

## License

The schema and the code are under the Apache License 2.0 ([LICENSE](LICENSE)).

SchemaStore's two schemas in [src/github_actions/schema/schemastore/](src/github_actions/schema/schemastore) keep their own notice, and GitHub's documentation is cited, never copied: see [NOTICE](NOTICE).

This is not an official GitHub project, and its use implies no endorsement by GitHub.

## Contributing and security

[CONTRIBUTING.md](CONTRIBUTING.md) is the checklist for pull requests and
releases, [AI_COVENANT.md](AI_COVENANT.md) sets the rules for AI-assisted work,
[SECURITY.md](SECURITY.md) says how to report a vulnerability, and
[CHANGELOG.md](CHANGELOG.md) records the changes.

## Credits

Built from the [linkml-project-copier](https://github.com/linkml/linkml-project-copier) template ([doi:10.5281/zenodo.15163584](https://doi.org/10.5281/zenodo.15163584)).
