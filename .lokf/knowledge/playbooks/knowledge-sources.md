---
type: Playbook
id: https://w3id.org/lmodel/github-actions/knowledge/playbooks/knowledge-sources
genre: reference
title: Knowledge sources map
description: "The librarian's scrape map: every repository location and external page this bundle derives concepts from, the concepts each yields, how to re-check each on a refresh run, and the paths left out on purpose."
resource: .
sources:
  - resource: README.md
  - resource: docs/about.md
  - resource: docs/index.md
  - resource: src/github_actions/schema
  - resource: src/github_actions/datamodel
  - resource: project.justfile
  - resource: .lokf/github-actions.yaml
  - resource: .lokf/justfile
  - resource: NOTICE
  - resource: LICENSE
  - resource: scripts/check_upstream_release.py
  - resource: scripts/derive.py
  - resource: .github/scripts
  - resource: .github/workflows
  - resource: .github/dependabot.yml
  - resource: justfile
  - resource: .linkml/generators.yaml
  - resource: .linkmllint.yaml
  - resource: .copier-answers.yml
  - resource: .pre-commit-config.yaml
  - resource: project
  - resource: docs/schema
  - resource: docs/elements
  - resource: tests
  - resource: examples/README.md
  - resource: CONTRIBUTING.md
  - resource: .releaserc.json
  - resource: CHANGELOG.md
  - resource: pyproject.toml
  - resource: website
  - resource: SECURITY.md
  - resource: AI_COVENANT.md
  - resource: .github/ISSUE_TEMPLATE
  - resource: .github/pull_request_template.md
  - resource: .github/PULL_REQUEST_TEMPLATE
  - resource: CODE_OF_CONDUCT.md
  - resource: uv.lock
  - resource: .gitignore
  - resource: .editorconfig
  - resource: .yamllint.yaml
  - resource: .markdownlint-cli2.jsonc
  - resource: lychee.toml
  - resource: config.public.mk
  - resource: src/README.md
  - resource: docs/templates-linkml
  - resource: src/github_actions/__init__.py
  - resource: src/github_actions/_version.py
  - resource: llms.txt
  - resource: knowledge_bundle
generated:
  by: process:ktl-librarian
  at: "2026-10-28T20:03:46Z"
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T21:21:37Z"
---

# Knowledge sources

Steady-state refresh runs re-verify these sources instead of discovering them again. Update this map whenever a knowledge source in the repository is added, moved or removed.

Each concept derived from a file or folder of this repository names it by its path from the repository root, in `resource` and in `sources`. `knowledge-report.sh worklist` lists the concepts whose source moved since their stamp. It never fetches a page, so re-read the external pages this table names when the schema header's reading date moves.

| Source | Yields | Re-check by |
| --- | --- | --- |
| `src/github_actions/schema/github_actions.yaml`, the four `github_actions_*.yaml` modules, `src/github_actions/schema/README.md` | `datasets/github-actions-linkml-schema`, the four `glossary/` terms | load `github_actions.yaml` with SchemaView and recount classes, enums, types and subsets per module; re-read the header's `version`, `source`, annotations and comments, each class's required slots, rules, mappings and comments |
| `project.justfile`, `.lokf/github-actions.yaml`, `.lokf/justfile`, the README's Knowledge Trust Ladder (KTL) section | the domain-schema section of `datasets/github-actions-linkml-schema` | re-read the `--root` list, the `LOKF_CMD` note, the copy's notes, the `schema :=` line and the renamed keys |
| `README.md` (What it models, Influences, Mappings, Not modelled here), `docs/about.md`, `.linkmllint.yaml` | `explanations/scope-and-influences`, `explanations/element-names`, the four `references/` | re-read each section and the lint comment |
| `src/github_actions/schema/schemastore/`, the SchemaStore section of `NOTICE` | `datasets/schemastore-copy` | re-read the pinned commit and each file's `$id`; the upstream watch compares the blobs weekly |
| `scripts/check_upstream_release.py`, `.github/scripts/report-issue.sh` | `playbooks/update-upstream-pins`, `workflows/upstream-watch` | re-read `PINNED_COMMIT`, `PINNED_API_VERSION`, `DOCS_READ`, `KNOWN_DIFFERENCES` and the issue title |
| `scripts/derive.py`, `tests/derive/`, `tests/test_derive.py`, the README's Deriving the facts from a repository section, the `scripts/derive.py` sentence of `SECURITY.md` | `playbooks/derive-and-check`, the `tests/test_derive.py` section of `datasets/test-data`, the naming details in `glossary/required-status-check` | re-read the docstring, the options, `ITEM_KEYS` and the finding rules; re-list the fixtures and re-count the tests; run `uv run --quiet scripts/derive.py --exclude tests/ --check .lokf/knowledge` and expect no drift |
| `justfile`, `.linkml/generators.yaml`, `project/`, `src/github_actions/datamodel/`, `docs/schema/`, `docs/elements/`, `.pre-commit-config.yaml` | `datasets/generated-artefacts` | re-read the `gen-project`, `gen-doc`, `gen-merged` and `lokf-adapt` recipes and the `excludes`; re-list `project/*/` |
| `tests/data/`, `tests/test_data.py`, `tests/test_schema_rules.py`, `tests/neighbours/slsa.yaml`, `examples/README.md` | `datasets/test-data` | re-count `valid/` and `invalid/` per class; re-read the naming rule, the tests and the comment on the slsa neighbour |
| the Validating data section of `docs/index.md` | `playbooks/validate-data` | re-read the section |
| `CONTRIBUTING.md`, `.copier-answers.yml`, the `test`, `lint` and `update` recipes of `justfile` | `playbooks/regenerate-and-test` | confirm the setup, the checklist and the recipes |
| `.releaserc.json`, `.github/scripts/changelog-release.mjs`, `CHANGELOG.md`, `pyproject.toml`, the Releasing section of `CONTRIBUTING.md` | `playbooks/release` | re-read the release rules, the commands, the baseline paragraph and the versioning settings |
| the nine files in `.github/workflows/` | the nine `workflows/` concepts | re-read each file's `on` keys, its top-level `permissions`, and each job's id, `name`, `runs-on` and `permissions`; check that none names `workflow_call`; the derivation check above compares the same facts |
| `website/` | `services/documentation-site` | re-read `site.config.mjs` and `website/README.md` |
| `NOTICE`, `LICENSE`, `website/NOTICE`, the License sections of `README.md` and `CONTRIBUTING.md` | `policies/license-and-attribution` | re-read each third-party entry |
| `SECURITY.md`, `.github/dependabot.yml` | `policies/security-policy` | re-read the table of surfaces and the settings not yet in force |
| `AI_COVENANT.md` | `policies/ai-covenant` | re-read the project note and the section on agent automation |
| GitHub's workflow syntax, reusable workflows and metadata syntax pages, the REST API's rules and check runs pages, and GitHub's build type at `https://actions.github.io/buildtypes/workflow/v1` | the four `references/` | external authorities, read on the date the schema header gives; the pages are versionless, so re-read them when that date moves |

These are not knowledge sources, and are left out:

- `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md` and `CODE_OF_CONDUCT.md` (governance text);
- `uv.lock`, `.gitignore`, `.editorconfig`, `.yamllint.yaml`, `.markdownlint-cli2.jsonc`, `lychee.toml` and `config.public.mk` (tooling);
- `src/README.md`, `docs/templates-linkml/` and `project/README.md` (text from the project template);
- `src/github_actions/__init__.py`, `src/github_actions/_version.py` and `tests/__init__.py` (package and test plumbing);
- `llms.txt` (the pointer that sends agents to this bundle);
- the `knowledge_bundle` link and `.github/PULL_REQUEST_TEMPLATE/knowledge-sync.md`, which belong to the sidecar, as does everything under `.lokf/` apart from the domain schema and the justfile's `schema :=` line.
