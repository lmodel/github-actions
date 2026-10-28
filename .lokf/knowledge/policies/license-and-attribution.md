---
type: Policy
id: https://w3id.org/lmodel/github-actions/knowledge/policies/license-and-attribution
genre: reference
title: License and attribution
description: "Which license covers what in the github-actions repository: Apache-2.0 for the schema, the generated models and the code; SchemaStore's two schemas under Apache-2.0 with JSON Schema Store's notice; GitHub's documentation, under CC BY 4.0, cited and never copied; the linkml-project-copier scaffolding under MIT; the KTL sidecar and site templates under Apache-2.0; and the bundle under CC BY 4.0."
resource: NOTICE
relatedTo:
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/schemastore-copy
sources:
  - id: notice
    resource: NOTICE
    title: every section
  - id: readme.md
    resource: README.md
    title: the License and Credits sections
  - id: website-notice
    resource: website/NOTICE
    title: the graph explorer's notice
  - resource: LICENSE
    title: the Apache License, Version 2.0
  - resource: CONTRIBUTING.md
    title: the License section
  - resource: website/README.md
    title: the typefaces paragraph
  - resource: .lokf/knowledge/index.md
    title: the license key
generated:
  by: process:ktl-librarian
  at: "2026-10-28T19:53:06Z"
  revision: 67d51bcffa835417e6f4785bb2d9a6945a15d95f
status: draft
verified:
  - by: process:ktl-librarian
    at: "2026-10-28T21:21:37Z"
---

# License and attribution

`NOTICE` names the project "GitHub Actions LinkML Schema (github-actions)", copyright 2026 Noel McLoughlin, and says that its code is licensed under the Apache License, Version 2.0, which `LICENSE` holds.[^notice] The README says that the schema and the code are under that license, and that the project is not an official GitHub project and implies no endorsement by GitHub.[^readme.md] CONTRIBUTING.md says that a contribution is licensed under Apache-2.0, and asks that NOTICE be updated when something new comes from elsewhere.

## What NOTICE lists

- **The schema's rendering of GitHub's documentation.** `src/github_actions/schema/*.yaml`, `src/github_actions/datamodel/` and `project/` model what GitHub's documentation says, in the project's own words with each page cited by address. GitHub's documentation is licensed under the Creative Commons Attribution 4.0 International license (CC BY 4.0), and the README says that it is cited, never copied.
- **SchemaStore's GitHub Actions schemas.** The copy in `src/github_actions/schema/schemastore/` is under the Apache License 2.0 and carries JSON Schema Store's notice, "Copyright 2015-Current Mads Kristensen and Contributors". See [SchemaStore copy](../datasets/schemastore-copy.md).
- **linkml-project-copier.** The project was generated from this template, and its justfile, configuration and documentation scaffolding derive from it, under the MIT License, copyright 2025 David Linke. The README credits the template by its DOI, `10.5281/zenodo.15163584`.
- **The knowledge bundle's tooling.** The scripts under `.lokf/scripts/` and `.lokf/m365/` and the knowledge-librarian, knowledge-registrar, knowledge-release and knowledge-sync workflows are copies of the ktl-sidecar templates in knowledge-trust-ladder. `website/` and the knowledge-website workflow derive from its ktl-website templates. All of them are under Apache-2.0.

`website/NOTICE` says that `src/components/KnowledgeGraph.astro` is adapted from the LOKF toolkit's site, copyright 2026 Nolan Nichols, under Apache-2.0, and that the file's header comment lists the changes.[^website-notice] `website/README.md` says that the site's two typefaces are self-hosted from Fontsource under the SIL Open Font License 1.1.

The bundle's root `index.md` declares the license CC BY 4.0 for the knowledge bundle itself.

[^notice]: NOTICE, every section
[^readme.md]: README.md, the License and Credits sections
[^website-notice]: website/NOTICE, the whole file
