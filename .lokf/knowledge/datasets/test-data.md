---
type: Dataset
id: https://w3id.org/lmodel/github-actions/knowledge/datasets/test-data
genre: reference
title: Test data and schema tests
description: "Example instances of the github-actions schema in tests/data/: 9 valid files and 34 counter-examples, each named after the class it instantiates (GhaWorkflow-pull-request.yaml and the like), which tests/test_data.py holds to the validator, beside the tests in tests/test_schema_rules.py that compare the schema with the SchemaStore copy and its names with LOKF's and slsa's."
resource: tests/data
about:
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/github-actions-linkml-schema
references:
  - https://w3id.org/lmodel/github-actions/knowledge/datasets/schemastore-copy
sources:
  - id: data-readme.md
    resource: tests/data/README.md
    title: the folders and the naming rule
  - id: test_data.py
    resource: tests/test_data.py
    title: the three tests
  - id: test_schema_rules.py
    resource: tests/test_schema_rules.py
    title: the seven tests and the neighbour comment
  - id: justfile
    resource: justfile
    title: the test recipe and its three parts
  - resource: tests/neighbours/slsa.yaml
    title: the header lokf adapt wrote
  - resource: CONTRIBUTING.md
    title: the rule on example data
  - resource: examples/README.md
    title: the examples output folder
generated:
  by: process:ktl-librarian
  at: "2026-10-28T19:53:06Z"
  revision: 4c6d307b6b74004e1acabb092ae1ffb14c49c214
status: draft
---

# Test data and schema tests

`tests/data/README.md` sorts the example data into `valid/`, for data that conforms to the schema, `invalid/`, for data that must fail validation, and `problem/`, for data the current schema does not yet handle correctly.[^data-readme.md] A file name has the form `classname-###.yaml`: the part before the first hyphen is the name of a class in the schema, and `###` is a number or other characters a file name allows. CONTRIBUTING.md asks for an invalid example for each constraint.

## The examples

`tests/data/valid/` holds 9 files: 2 for `GhaWorkflow`, 1 for `GhaReusableWorkflow`, 2 for `GhaAction`, 1 for `GhaRepositoryRuleset`, 2 for `GhaRequiredStatusCheck` and 1 for `GhaDocument`. `GhaDocument-service.yaml` holds one repository's workflows, its reusable workflow, an action, its ruleset and the check the ruleset requires, which names the workflow that reports it. `tests/data/invalid/` holds 34 counter-examples: 12 for `GhaWorkflow`, 5 for `GhaReusableWorkflow`, 5 for `GhaAction`, 7 for `GhaRepositoryRuleset` and 5 for `GhaRequiredStatusCheck`. The two `problem/` folders hold no example yet. Every example names an `example-org` repository or an `example.org` address.

## tests/test_data.py

The first test loads each valid file into the generated dataclass of the class its name gives. The other two validate every file with `linkml.validator` against `src/github_actions/schema/github_actions.yaml`: a valid example must pass, and a counter-example must fail.[^test_data.py] A comment says that the JSON Schema the validator generates is the one check that applies every constraint.

## tests/test_schema_rules.py

Six tests compare the schema with the [SchemaStore copy](schemastore-copy.md) and with the upstream watch, and one compares its names with its neighbours':[^test_schema_rules.py]

- the schema header's pins equal those in `scripts/check_upstream_release.py`, and the reading date equals the header's `version`;
- the permission pattern admits every scope and level SchemaStore lists;
- the runtime enum differs from SchemaStore's only by the retired `node12` and `node16`;
- the input types are SchemaStore's;
- the trigger pattern admits every event SchemaStore names;
- the key and `uses` patterns are SchemaStore's;
- no class, enum, type or subset name in `.lokf/github-actions.yaml` appears in `.lokf/lokf.yaml` or `tests/neighbours/slsa.yaml`, and a slot or attribute name they share carries the same IRI.

`tests/neighbours/slsa.yaml` is lmodel/slsa's `lokf adapt` copy. The test file's comment says that it comes from slsa's branch `chore/lokf-0-9-0` as commit `80716f3` left it, which releases as slsa 0.7.0, and that it is to be replaced with that release's schema asset once that is published.

## How they run

`just test` runs three recipes.[^justfile] `_test-schema` generates the project into `tmp/`. `_test-python` regenerates the Python models and runs pytest. `_test-examples` runs `linkml-run-examples` over `tests/data/valid/` and `tests/data/invalid/` and writes what it converts into `examples/output/`, which git ignores. [Build and test](../workflows/main.md) runs `just test` on every pull request.

[^data-readme.md]: tests/data/README.md, the whole page
[^test_data.py]: tests/test_data.py, the three test functions
[^test_schema_rules.py]: tests/test_schema_rules.py, the seven test functions and the comment above COPY
[^justfile]: justfile, the `test`, `_test-schema`, `_test-python` and `_test-examples` recipes
