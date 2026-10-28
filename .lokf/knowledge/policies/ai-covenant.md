---
type: Policy
id: https://w3id.org/lmodel/github-actions/knowledge/policies/ai-covenant
genre: reference
title: AI covenant
description: "The rules for AI-assisted work in github-actions: a contributor owns what they submit; a schema description says what its GitHub, SchemaStore or build-type source says and cites the page; GitHub's documentation is cited, never copied; the SchemaStore copy is never edited; and the scheduled librarian works through pull requests a person approves, with least privilege."
resource: AI_COVENANT.md
references:
  - https://w3id.org/lmodel/github-actions/knowledge/workflows/knowledge-librarian
sources:
  - id: ai_covenant.md
    resource: AI_COVENANT.md
    title: every section
generated:
  by: process:ktl-librarian
  at: "2026-10-28T19:53:06Z"
  revision: c55f3707fe7c8202c7eaa0303f1945b56b37f623
status: draft
---

# AI covenant

`AI_COVENANT.md` sets the norms for AI-assisted work in the repository.[^ai_covenant.md] Its core principle is that everything a contributor submits is theirs, whatever tools helped. The contributor must understand it, verify it, explain it in review and make it meet the project's standards.

## The rules specific to this project

The covenant says that the repository models someone else's platform, which makes one failure mode worse here than elsewhere: a field, value or rule that a model produced, presented as what GitHub does. So:

- a schema description says what its source says. Every class, slot and enum value renders a page of GitHub's documentation, SchemaStore's schema at the pinned commit, or GitHub's SLSA build type, and its class or enum names that page in `see_also`;
- GitHub's documentation is cited, never copied, and the schema header records the date its pages were read;
- the SchemaStore copy is upstream text: never edit it, replace it from the commit that NOTICE records, and `upstream-watch.yaml` checks that it still matches;
- everything the schema defines lives under `gha:`, and GitHub's own names, such as event names and permission scopes, appear only as values the schema documents.

## Reviews and agents

AI review comments are automated quality checks, not human reviews, and a pull request still needs a person's approval. The scheduled agent that [Knowledge Librarian](../workflows/knowledge-librarian.md) runs commits as `knowledge-librarian[bot]` or as the maintainer who ran it interactively, never both, and its commits carry no AI co-authorship trailer. Every change it proposes arrives as a pull request that a maintainer approves. It runs in a read-only job with no git credentials on disk and hands its change to a privileged job that runs no agent code, and its contract to edit only `.lokf/knowledge/` is checked after it runs. A skill that records a person's judgment writes only what that person said about that item, in that session.

## Disclosure

Disclosure is required for a fix to code that the contributor does not fully understand, and for a schema description that an AI drafted, together with the page it rests on. Routine AI use needs no disclosure, and AI co-authorship in commit messages is actively discouraged. The covenant says that it is adapted from the Knowledge Trust Ladder AI Covenant, which is adapted from LinkML's.

[^ai_covenant.md]: AI_COVENANT.md, every section
