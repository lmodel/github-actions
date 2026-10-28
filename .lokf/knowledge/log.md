# Change Log

## 2026-10-28

* **Prose**: reworded 16 concept bodies in plain English. No fact, link, number or frontmatter changed.
* **Added**: Derive and check concepts from workflow files, from `scripts/derive.py`, its tests and the README's section on it, which d38a5e0 added.
* **Changed**: the test data concept gives the naming rule as `ClassName-###.yaml`, as `tests/data/README.md` has since a86d859, and names `tests/test_derive.py` and its fixtures, which d38a5e0 added.
* **Changed**: the security policy names both scripts under `scripts/`, says that `scripts/derive.py` runs in no workflow here, and words the librarian's row as `SECURITY.md` has since a86d859 and d38a5e0.
* **Changed**: the schema concept says when the knowledge release attaches the adapt copy, as the README's Knowledge Trust Ladder (KTL) section has since a86d859.
* **Changed**: the knowledge release concept says that the README and CONTRIBUTING.md now agree with the workflow on when the schema copy is attached, since a86d859.
* **Resolved**: README.md and CONTRIBUTING.md say since a86d859 that the knowledge release attaches the schema copy when the bundle has changed, and that a run with `force` attaches it otherwise.
* **Changed**: the librarian workflow concept says that the skills pin stays at v0.57.0 until the first weekly sync moves it, as `CHANGELOG.md` has since a86d859.
* **Resolved**: CHANGELOG.md says since a86d859 that the v0.58.0 templates leave the skills pin at v0.57.0 and that the first weekly sync moves it.
* **Changed**: the release playbook says when the knowledge release attaches the schema copy, and to run it with `force` when only the schema changed, as CONTRIBUTING.md's Releasing section has since a86d859.
* **Changed**: the required status check term adds the details of the naming rule that `scripts/derive.py` states, from d38a5e0.
* **Changed**: the source map adds `scripts/derive.py`, its fixtures and tests, and the README's section on it, and names the derivation check as a way to re-check the workflow concepts.
* **Added**: github-actions LinkML schema, from `src/github_actions/schema/github_actions.yaml`.
* **Added**: SchemaStore copy, from `src/github_actions/schema/schemastore`.
* **Added**: Generated artefacts, from `project`.
* **Added**: Test data and schema tests, from `tests/data`.
* **Added**: GitHub workflow syntax, from `https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax`.
* **Added**: GitHub metadata syntax, from `https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax`.
* **Added**: GitHub REST API rules and check runs, from `https://docs.github.com/en/rest/repos/rules`.
* **Added**: GitHub Actions build type, from `https://actions.github.io/buildtypes/workflow/v1`.
* **Added**: Required status check, from `src/github_actions/schema/github_actions_rules.yaml`.
* **Added**: Repository ruleset, from `src/github_actions/schema/github_actions_rules.yaml`.
* **Added**: Reusable workflow, from `src/github_actions/schema/github_actions_workflow.yaml`.
* **Added**: GITHUB_TOKEN permission, from `src/github_actions/schema/github_actions_workflow.yaml`.
* **Added**: Element names and the shared namespace, from `docs/about.md`.
* **Added**: Scope, influences and mappings, from `README.md`.
* **Added**: Regenerate and test the schema, from `CONTRIBUTING.md`.
* **Added**: Release the schema, from `CONTRIBUTING.md`.
* **Added**: Validate data against the schema, from `docs/index.md`.
* **Added**: Move the upstream pins, from `scripts/check_upstream_release.py`.
* **Added**: github-actions documentation site, from `website`.
* **Added**: License and attribution, from `NOTICE`.
* **Added**: Security policy, from `SECURITY.md`.
* **Added**: AI covenant, from `AI_COVENANT.md`.
* **Added**: Build and test (main.yaml), from `.github/workflows/main.yaml`.
* **Added**: Lint & docs (lint-and-docs.yaml), from `.github/workflows/lint-and-docs.yaml`.
* **Added**: Semantic release (semantic-release.yml), from `.github/workflows/semantic-release.yml`.
* **Added**: Upstream watch (upstream-watch.yaml), from `.github/workflows/upstream-watch.yaml`.
* **Added**: Knowledge website (knowledge-website.yaml), from `.github/workflows/knowledge-website.yaml`.
* **Added**: Knowledge Registrar (knowledge-registrar.yaml), from `.github/workflows/knowledge-registrar.yaml`.
* **Added**: Knowledge Librarian (knowledge-librarian.yaml), from `.github/workflows/knowledge-librarian.yaml`.
* **Added**: Knowledge Release (knowledge-release.yaml), from `.github/workflows/knowledge-release.yaml`.
* **Added**: Knowledge sync (knowledge-sync.yaml), from `.github/workflows/knowledge-sync.yaml`.
* **Added**: Knowledge sources map, which lists every repository path and page this bundle derives from, how to re-check each, and the paths left out and why.
* **Open question**: Knowledge Release (knowledge-release.yaml): README.md says that each release attaches the schema copy as `schema-<tag>-github-actions.yaml`, and CONTRIBUTING.md and CHANGELOG.md say the same, but knowledge-release.yaml packs the domain schema only when the bundle's tree differs from the newest earlier release that carries a bundle, or when force is set. Should a release whose bundle is unchanged still carry the schema copy, or should the README say when it does?
* **Open question**: Knowledge Librarian (knowledge-librarian.yaml): CHANGELOG.md says that the sidecar automation comes from the KTL v0.58.0 templates, and CONTRIBUTING.md says that the skills pin moves with the sidecar copies, but knowledge-librarian.yaml sets TRUST_LADDER_SKILLS_REF to v0.57.0. Which release should the scheduled librarian install?
* **Removal**: Example Service A and Example Service B, the sidecar's placeholders, now that real concepts describe the repository.
* **Initialization**: Scaffolded the LOKF bundle for github-actions with placeholder
  services. Real concepts to follow.
