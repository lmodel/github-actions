---
type: Playbook
id: https://w3id.org/lmodel/github-actions/knowledge/playbooks/release
genre: how-to
title: Release the schema
description: How a releasing commit merged to main makes semantic-release promote the changelog's Unreleased section, tag vX.Y.Z and publish a GitHub Release, then dispatch the Knowledge Release workflow once KNOWLEDGE_RELEASE_ENABLED is true; below 1.0.0 from a v0.0.0 baseline tag, with a breaking change as a minor bump and nothing published to PyPI.
resource: CONTRIBUTING.md
references:
  - https://w3id.org/lmodel/github-actions/knowledge/workflows/semantic-release
  - https://w3id.org/lmodel/github-actions/knowledge/workflows/knowledge-release
sources:
  - id: contributing.md
    resource: CONTRIBUTING.md
    title: Releasing (maintainers)
  - id: pyproject.toml
    resource: pyproject.toml
    title: the project name, the comment on PyPI and the versioning settings
  - id: changelog.md
    resource: CHANGELOG.md
    title: the paragraph on the v0.0.0 tag
  - id: releaserc.json
    resource: .releaserc.json
    title: the release rules and the release commit message
  - id: security.md
    resource: SECURITY.md
    title: the settings not yet in force
  - resource: .github/workflows/semantic-release.yml
    title: the header comment and both jobs
  - resource: .github/scripts/changelog-release.mjs
    title: the check, notes and promote commands
generated:
  by: process:ktl-librarian
  at: "2026-10-28T20:03:46Z"
  revision: a86d8591547d1112e880fd60e399749a70698be0
status: draft
---

# Release the schema

CONTRIBUTING.md's Releasing section and the [Semantic release](../workflows/semantic-release.md) workflow say how a release is cut.[^contributing.md] The release tags are the schema's own versions, `vX.Y.Z`, and no file carries the version. The package `github-actions-linkml` takes its version from git through uv-dynamic-versioning, and a comment in `pyproject.toml` says that PyPI publishing is off.[^pyproject.toml]

## Before the first release

- Push the `v0.0.0` baseline tag on `main` before the first releasing merge, which then releases 0.1.0. Both release jobs refuse to run without a `v*` tag, because semantic-release would otherwise make the first release 1.0.0. `CHANGELOG.md` calls `v0.0.0` a baseline, not a release.[^changelog.md]
- Configure required reviewers on the `release` GitHub Environment in the repository's settings, or every qualifying merge is released with no human step. SECURITY.md says that this setting is not yet in force.[^security.md]
- Leave off any branch rule that requires pull requests, status checks or signed commits on `main`, because it would reject the release job's own push.

## For each change

1. Write the change under `## [Unreleased]` in `CHANGELOG.md` as you go. The release refuses an empty section, through `node .github/scripts/changelog-release.mjs check`.
2. Type the commit with Conventional Commits for what the change is. Only `feat:`, `fix:`, `security:` and a breaking `!` cut a release, and other types leave their entries for the next release that does. When a pull request would release, give it a releasing type in its title too, since a squash merge takes its subject from the title.
3. Merge to `main`. semantic-release retitles the section to `## [X.Y.Z] - YYYY-MM-DD`, commits `CHANGELOG.md`, tags `vX.Y.Z` and publishes the GitHub Release with the section's text as its notes. Once the repository variable `KNOWLEDGE_RELEASE_ENABLED` is `true`, it then dispatches [Knowledge Release](../workflows/knowledge-release.md) for the tag, which attaches the schema copy and the bundle when the bundle changed. Run that workflow by hand with `force` when only the schema changed.

## Staying below 1.0.0

`.releaserc.json` maps a breaking change to a minor release and a `security` commit to a patch release.[^releaserc.json] So the schema stays in 0.x until someone removes the first rule, which CONTRIBUTING.md asks to be done in a pull request of its own. The release commit's message is `chore(release): ${nextRelease.version} - changelog promoted [skip ci]`, so the commit skips CI.

[^contributing.md]: CONTRIBUTING.md, Releasing (maintainers)
[^pyproject.toml]: pyproject.toml, the comment above name and the uv-dynamic-versioning settings
[^changelog.md]: CHANGELOG.md, the paragraph on the v0.0.0 tag
[^releaserc.json]: .releaserc.json, releaseRules and the git plugin's message
[^security.md]: SECURITY.md, the paragraph after the table
