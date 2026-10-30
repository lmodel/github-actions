---
lokf_version: "0.2"
okf_version: "0.2"
base_iri: https://w3id.org/lmodel/github-actions/knowledge/
context: https://w3id.org/lokf/context.jsonld
title: github-actions Knowledge Bundle
description: GitHub Actions workflows, actions and repository rulesets (LinkML)
license: https://creativecommons.org/licenses/by/4.0/
publisher:
  type: Person
  id: https://w3id.org/lmodel/github-actions/knowledge/person/noel-mcloughlin
  name: Noel McLoughlin
---

# github-actions Knowledge Bundle

A [LOKF](https://lokf.nolan-nichols.com) knowledge base for github-actions. Every Markdown file under `knowledge/` is one concept; together they form a queryable knowledge graph, derived from this repository's code and docs.

# Services

* [github-actions documentation site](services/documentation-site.md) - The Astro Starlight site in website/, built from the README, docs/, the schema's gen-doc pages, the changelog and the knowledge bundle by the Knowledge website workflow, which deploys it to GitHub Pages under lmodel.github.io/github-actions when KNOWLEDGE_WEBSITE_ENABLED is true; its REDIRECTS send the retired mkdocs addresses on to the new pages.

# Datasets

* [github-actions LinkML schema](datasets/github-actions-linkml-schema.md) - The modular LinkML schema of what GitHub Actions workflow files, action metadata files and repository rulesets state (schema id `https://w3id.org/lmodel/github-actions`, version 2026-10-28): `github_actions.yaml` imports a core, a workflow, an action and a rules module, and its `lokf adapt` copy in `.lokf/github-actions.yaml` is the bundle's domain schema.
* [SchemaStore copy](datasets/schemastore-copy.md) - SchemaStore's `github-workflow.json` and `github-action.json`, the JSON Schemas of a workflow file and an action's metadata file, copied with SchemaStore's LICENSE and NOTICE into `src/github_actions/schema/schemastore/` at commit f7c2f3b; never edited here, compared by tests with the schema, and checked weekly against upstream.
* [Generated artefacts](datasets/generated-artefacts.md) - Files generated from the github-actions schema and never edited by hand: project/ (Excel, GraphQL, Java, JSON-LD, JSON Schema, OWL, a prefix map, protobuf, SHACL, ShEx, SQL and TypeScript), the dataclass and Pydantic models in src/github_actions/datamodel/, the two schema files in docs/schema/, the gen-doc pages in docs/elements/ and the domain schema copy .lokf/github-actions.yaml.
* [Test data and schema tests](datasets/test-data.md) - Example instances of the github-actions schema in tests/data/: 9 valid files and 34 counter-examples, each named after the class it instantiates (GhaWorkflow-pull-request.yaml and the like), which tests/test_data.py holds to the validator; beside them, tests/test_schema_rules.py compares the schema with the SchemaStore copy, the adapt copy's names with LOKF's and slsa's, and the copy's mappings with its prefixes, tests/test_derive.py runs scripts/derive.py against the fixture repository in tests/derive/repo/, and tests/test_github_export.py runs scripts/github_export.py against fixed answers.

# References

* [GitHub workflow syntax](references/workflow-syntax.md) - GitHub's workflow syntax page for GitHub Actions, with its companion page on reusable workflows: the source of GhaWorkflow, GhaWorkflowJob, GhaReusableWorkflow and the gha_permission type, versionless, read on 2026-10-28 and cited, never copied, under CC BY 4.0.
* [GitHub metadata syntax](references/metadata-syntax.md) - GitHub's metadata syntax page for an action's action.yml or action.yaml: the source of GhaAction, its inputs and outputs and the runtimes runs.using may name (composite, docker, node20, node24), versionless, read on 2026-10-28 and cited, never copied, under CC BY 4.0.
* [GitHub REST API rules and check runs](references/rest-api-rules.md) - The GitHub REST API's rules and check runs pages at API version 2026-03-10: the source of GhaRepositoryRuleset, GhaBypassActor and GhaRequiredStatusCheck, whose fields are named after REST fields such as `source_type`, `enforcement` and `required_status_checks[].context`.
* [GitHub Actions build type](references/github-build-type.md) - GitHub's build type for SLSA provenance of a GitHub Actions workflow run (actions.github.io/buildtypes/workflow/v1): the schema writes workflow_path, workflow_repository and runner_environment as it does, and takes from it that a reusable workflow that signs provenance is the build's builder.

# Glossary

* [Required status check](glossary/required-status-check.md) - A status check that a ruleset requires to pass before a change reaches a ref it targets; its name is the context a check run reports, which GitHub Actions takes from the job's name or id, as caller / called for a job of a called workflow. The schema models it as GhaRequiredStatusCheck.
* [Repository ruleset](glossary/repository-ruleset.md) - A ruleset: named rules GitHub enforces on the branches, tags or pushes of a repository, organization or enterprise, with a target, an enforcement (active, evaluate or disabled), ref conditions, bypass actors and rule types. The schema models it as GhaRepositoryRuleset.
* [Reusable workflow](glossary/reusable-workflow.md) - A workflow that other workflows call as a job because its on key names workflow_call, declaring the inputs, outputs and secrets its callers pass and read; the schema models it as GhaReusableWorkflow, and a calling job names it in uses with no runs-on or runner group.
* [GITHUB_TOKEN permission](glossary/token-permission.md) - One grant of access to a workflow's GITHUB_TOKEN, such as contents: read, or the shorthand read-all, write-all or {}; the schema's gha_permission type, used by a workflow's permissions and a job's job_permissions, and what this repository's workflows grant.

# Explanations

* [Element names and the shared namespace](explanations/element-names.md) - Why the github-actions schema names its elements as it does: the Gha prefix, snake_case slots after GitHub's keys, GitHub's own strings as permissible values, and no class, enum or type name shared with LOKF's lokf.yaml or slsa's adapt copy, because a host merges the three into one namespace; input_type, ruleset_target and check_context are the renamed keys.
* [Scope, influences and mappings](explanations/scope-and-influences.md) - What the github-actions schema renders and leaves out, and why: GitHub's documentation as its source, the designs that shaped it (SLSA, the OpenSSF Baseline and Scorecard, otterdog, LOKF and KTL, lmodel/slsa), its close and related mappings to CycloneDX 1.7, SPDX 3.0.1 and in-toto, and the runs, steps and evidence it does not model.

# Playbooks

* [Regenerate and test the schema](playbooks/regenerate-and-test.md) - How to change the github-actions schema: set up with uv and just, edit src/github_actions/schema/, regenerate with just gen-project, gen-doc, gen-merged and lokf-adapt, add examples, then run the checks CI runs (just test on Python 3.10 to 3.14, just lint and just lokf-adapt-check on 3.13) and the pre-commit hooks.
* [Release the schema](playbooks/release.md) - How a releasing commit merged to main makes semantic-release promote the changelog's Unreleased section, tag vX.Y.Z and publish a GitHub Release, then dispatch the Knowledge Release workflow once KNOWLEDGE_RELEASE_ENABLED is true; below 1.0.0 from a v0.0.0 baseline tag, with a breaking change as a minor bump and nothing published to PyPI.
* [Validate data against the schema](playbooks/validate-data.md) - How to check a YAML file against the github-actions schema with linkml-validate (for example with -C GhaReusableWorkflow), what the generated dataclass and Pydantic models check less, and the rules no tool checks, such as a repeated input_id or a read-all that does not stand alone.
* [Move the upstream pins](playbooks/update-upstream-pins.md) - What to do when the upstream watch opens its issue: replace both SchemaStore files from one commit and move PINNED_COMMIT, the schema header's source and annotations and NOTICE; or read a newer REST API version's breaking changes and move PINNED_API_VERSION; tests/test_schema_rules.py checks that the header and the script agree on the pins and the reading date.
* [Knowledge sources map](playbooks/knowledge-sources.md) - The librarian's scrape map: every repository location and external page this bundle derives concepts from, the concepts each yields, how to re-check each on a refresh run, and the paths left out on purpose.
* [Derive and check concepts from workflow files](playbooks/derive-and-check.md) - How to run scripts/derive.py, which derives concept frontmatter and check names from a repository's workflow and action files and reports drift from a knowledge bundle, and scripts/github_export.py, which fetches the rulesets and check runs that derive.py also compares; here derive.py runs with --exclude tests/.

# Policies

* [License and attribution](policies/license-and-attribution.md) - Which license covers what in the github-actions repository: Apache-2.0 for the schema, the generated models and the code; SchemaStore's two schemas under Apache-2.0 with JSON Schema Store's notice; GitHub's documentation, under CC BY 4.0, cited and never copied; the linkml-project-copier scaffolding under MIT; the KTL sidecar and site templates under Apache-2.0; and the bundle under CC BY 4.0.
* [Security policy](policies/security-policy.md) - How to report a vulnerability in github-actions (GitHub's private vulnerability reporting, not a public issue), which release gets fixes, what the repository releases and runs, what holds each workflow, the ruleset that holds main, and the two repository settings not yet in force: required reviewers on the release Environment, and secret scanning with push protection.
* [AI covenant](policies/ai-covenant.md) - The rules for AI-assisted work in github-actions: a contributor owns what they submit; a schema description says what its GitHub, SchemaStore or build-type source says and cites the page; GitHub's documentation is cited, never copied; the SchemaStore copy is never edited; and the scheduled librarian works through pull requests a person approves, with least privilege.

# Workflows

* [Build and test (main.yaml)](workflows/main.md) - The Build and test workflow, .github/workflows/main.yaml: on a push to main and on every pull request, its test job runs just test on Python 3.10 to 3.14, and on 3.13 also just lint and the check that .lokf/github-actions.yaml is current.
* [Lint & docs (lint-and-docs.yaml)](workflows/lint-and-docs.md) - The Lint & docs workflow, .github/workflows/lint-and-docs.yaml: on a push to main, every pull request, a Monday 06:00 UTC schedule and by hand, four jobs run ShellCheck, actionlint, the word budgets of CONTRIBUTING.md (1000) and SECURITY.md (900), and markdownlint, lychee and codespell over the Markdown.
* [Semantic release (semantic-release.yml)](workflows/semantic-release.md) - The Semantic release workflow, .github/workflows/semantic-release.yml: on a pull request into main, its plan job checks that the commits, the changelog and the title would release and previews the release; on a push to main, its release job in the release Environment tags vX.Y.Z, publishes the GitHub Release and dispatches Knowledge Release.
* [Upstream watch (upstream-watch.yaml)](workflows/upstream-watch.md) - The Upstream watch workflow, .github/workflows/upstream-watch.yaml: every Monday at 07:00 UTC and by hand, it runs scripts/check_upstream_release.py against SchemaStore and GitHub's REST API versions, and on a finding opens or updates the issue titled Upstream watch: SchemaStore or the REST API version has moved.
* [Knowledge website (knowledge-website.yaml)](workflows/knowledge-website.md) - The Knowledge website workflow, .github/workflows/knowledge-website.yaml: on pushes and pull requests that touch the site's sources, every Monday at 05:23 UTC and by hand, its build job builds website/ and checks its links read-only, and its deploy job publishes the default branch's build to GitHub Pages once KNOWLEDGE_WEBSITE_ENABLED is true.
* [Knowledge Registrar (knowledge-registrar.yaml)](workflows/knowledge-registrar.md) - The Knowledge Registrar workflow, .github/workflows/knowledge-registrar.yaml: the gate on the knowledge bundle, run on pull requests that touch .lokf/, every Monday at 06:00 UTC and by hand; it validates the bundle and its relation targets, runs the conventions script, and checks that each new confirmation by a person is backed by an approval or a signed commit.
* [Knowledge Librarian (knowledge-librarian.yaml)](workflows/knowledge-librarian.md) - The Knowledge Librarian workflow, .github/workflows/knowledge-librarian.yaml: every Monday at 05:00 UTC and by hand, once KNOWLEDGE_LIBRARIAN_ENABLED is true, it runs an LLM agent with the ktl-librarian skill (pinned by TRUST_LADDER_SKILLS_REF) in a read-only job and opens a review pull request with the bundle change from a separate privileged job.
* [Knowledge Release (knowledge-release.yaml)](workflows/knowledge-release.md) - The Knowledge Release workflow, .github/workflows/knowledge-release.yaml: dispatched with a release's tag, or started by a published release once KNOWLEDGE_RELEASE_ENABLED is true, it attaches `knowledge-<tag>-<name>.zip`, the domain schema as `schema-<tag>-<name>.yaml` and the Copilot skills to the release, but only when the bundle changed since the last release that carries one.
* [Knowledge sync (knowledge-sync.yaml)](workflows/knowledge-sync.md) - The Knowledge sync workflow, .github/workflows/knowledge-sync.yaml: every Monday at 04:10 UTC and by hand, it moves the sidecar's copies and the skills pin to the newest Knowledge Trust Ladder release through one pull request from the knowledge-sync branch, opened with the KNOWLEDGE_SYNC_TOKEN secret, and holds the workflow changes for a person to apply.
