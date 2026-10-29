# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The `v0.0.0` tag is a baseline, not a release: it marks where versioning starts so the first real release is `0.1.0` rather than `1.0.0`. The schema stays below 1.0.0 until its shape settles, so a breaking change bumps the minor version. See [CONTRIBUTING.md](CONTRIBUTING.md#releasing-maintainers).

## [Unreleased]

### Security

- **The sidecar copies and the skills pin are at Knowledge Trust Ladder [v0.59.0](https://github.com/noelmcloughlin/knowledge-trust-ladder/compare/v0.57.0...v0.59.0).** The release changed `.github/workflows/knowledge-release.yaml`, `.lokf/scripts/knowledge-conventions.sh`, `.lokf/scripts/knowledge-conventions.py`, `.lokf/scripts/knowledge-preflight.sh`, `.lokf/scripts/knowledge-report.sh` and `.lokf/m365/ktl-docent-m365.md` here.

## [0.1.1] - 2026-10-29

### Fixed

- **`GhaRequiredStatusCheck` names in-toto's Test Result predicate as `in_toto:test-result/v0.1`, under a new `in_toto:` prefix.** A `lokf convert --schema` over the adapt copy no longer warns that the address has no namespace.

## [0.1.0] - 2026-10-28

### Added

- **A LinkML schema of GitHub Actions workflows, reusable workflows, actions, repository rulesets and required status checks.** Five classes a knowledge concept can take as its `type`, with jobs, inputs, outputs, secrets and bypass actors inlined, rendered from GitHub's documentation as read on 2026-10-28 and the REST API at version 2026-03-10.
- **`emitted_by` ties a required status check to the workflow whose job reports it**, and `job_path` and `skip_conditions` record how the check is named and what can skip it.
- **`.lokf/github-actions.yaml`, the schema's `lokf adapt` copy, which the knowledge release attaches beside the bundle as `schema-<tag>-github-actions.yaml`.** It shares no element name with `lokf.yaml` or slsa's copy, and a test holds it to that.
- **A copy of SchemaStore's `github-workflow.json` and `github-action.json` at a pinned commit, and a weekly upstream watch.** The watch opens an issue when SchemaStore changes either file or GitHub releases a newer REST API version.
- **An example for each class and a counter-example for each constraint**, all held to the validator by `tests/test_data.py`.
- **The repository's own KTL knowledge bundle and its sidecar automation**, from the KTL v0.58.0 templates with the lokf floor at 0.9.0; the librarian's skills pin, which those templates leave at v0.57.0, moves at the first weekly sync.
- **`scripts/derive.py` derives the concepts' facts and the check names from a repository's workflow and action files**, reports unpinned `uses`, `secrets: inherit` and top-level write access, and with `--check` fails on drift from a bundle.
