"""Tests of scripts/derive.py against the fixture repository in tests/derive/repo."""

import copy
import importlib.util
from pathlib import Path

import pytest
import yaml
from linkml.validator import validate

ROOT = Path(__file__).parent.parent
REPO = Path(__file__).parent / "derive" / "repo"
SCHEMA = ROOT / "src" / "github_actions" / "schema" / "github_actions.yaml"
BASE = "https://example.org/knowledge/"

spec = importlib.util.spec_from_file_location("derive", ROOT / "scripts" / "derive.py")
derive = importlib.util.module_from_spec(spec)
spec.loader.exec_module(derive)


@pytest.fixture(scope="module")
def derived():
    return derive.derive(REPO)


def _contexts(derived, path):
    return [c["check_context"] for c in derived["checks"][path]]


def test_reusable_workflow_facts(derived):
    """A reusable workflow's inputs, outputs and secrets, with their types."""
    facts = derived["workflows"][".github/workflows/tests.yml"]
    assert facts["type"] == "GhaReusableWorkflow"
    assert facts["triggers"] == ["workflow_call"]
    assert facts["permissions"] == ["{}"]
    assert facts["inputs"] == [
        {
            "input_id": "python-version",
            "description": "The Python version to test on.",
            "input_type": "string",
            "default": "3.13",
        },
        {"input_id": "coverage", "input_type": "boolean", "default": "false"},
        {"input_id": "shards", "required": True, "input_type": "number"},
    ]
    assert facts["outputs"] == [
        {
            "output_id": "report-url",
            "description": "Where the test report was uploaded.",
            "output_expression": "${{ jobs.pytest.outputs.report-url }}",
        }
    ]
    assert facts["secrets"] == [{"secret_id": "CODECOV_TOKEN", "required": False}]


def test_workflow_facts(derived):
    """`on` read despite YAML 1.1, each form of runs-on, and job permissions."""
    facts = derived["workflows"][".github/workflows/pull-request.yml"]
    assert facts["type"] == "GhaWorkflow"
    assert facts["triggers"] == ["pull_request", "push"]
    assert facts["permissions"] == ["contents: read"]
    jobs = {job["job_id"]: job for job in facts["jobs"]}
    assert jobs["lint"]["runs_on"] == ["ubuntu-latest"]
    assert jobs["docs"] == {
        "job_id": "docs",
        "job_name": "Build the docs",
        "runs_on": ["self-hosted", "linux"],
    }
    assert jobs["test"]["runs_on"] == ["linux", "x64"]
    assert jobs["test"]["runner_group"] == "ci-runners"
    assert jobs["test"]["job_permissions"] == ["contents: read", "checks: write"]
    assert jobs["unit"] == {"job_id": "unit", "calls": "./.github/workflows/tests.yml"}
    assert derived["workflows"][".github/workflows/lint.yaml"]["permissions"] == [
        "read-all"
    ]
    assert derived["workflows"][".github/workflows/release.yml"]["permissions"] == [
        "write-all"
    ]


def test_action_facts(derived):
    """An action's runtime, its inputs with a deprecation, and its outputs."""
    setup = derived["actions"][".github/actions/setup/action.yml"]
    assert setup["using"] == "composite"
    assert setup["inputs"][1] == {
        "input_id": "cache",
        "description": "Whether to cache the dependencies.",
        "required": False,
        "default": "true",
        "deprecation_message": "The cache is always on; this input is ignored.",
    }
    assert (
        setup["outputs"][0]["output_expression"]
        == "${{ steps.setup.outputs.python-path }}"
    )
    labels = derived["actions"]["actions/labels/action.yaml"]
    assert labels == {
        "type": "GhaAction",
        "action_path": "actions/labels/action.yaml",
        "using": "node24",
        "outputs": [
            {
                "output_id": "labels",
                "description": "The labels the pull request carries.",
            }
        ],
    }


def test_check_names(derived):
    """The id or name, the matrix values, and caller / called at every depth."""
    assert _contexts(derived, ".github/workflows/pull-request.yml") == [
        "lint",
        "Build the docs",
        "test (ubuntu-latest, 3.10)",
        "test (ubuntu-latest, 3.13)",
        "test (windows-latest, 3.13)",
        "test (ubuntu-latest, 3.14)",
        "Python 3.12",
        "Python 3.13",
        None,
        "unit / pytest",
        "unit / lint / ruff",
        "Security scan / *",
    ]
    assert _contexts(derived, ".github/workflows/release.yml") == ["publish"]
    assert ".github/workflows/tests.yml" not in derived["checks"]


def test_unresolved_checks(derived):
    """A matrix from an expression and a call to another repository are named as unresolved."""
    unresolved = {
        c["job_path"][-1]: c["unresolved"]
        for c in derived["checks"][".github/workflows/pull-request.yml"]
        if "unresolved" in c
    }
    assert unresolved == {
        "from-expression": "matrix set by an expression",
        "scan": "calls a workflow outside this repository",
    }


def test_skip_conditions(derived):
    """A path filter, the job's own `if`, and a called job's `if` can each skip a check."""
    checks = {
        c["check_context"]: c
        for c in derived["checks"][".github/workflows/pull-request.yml"]
    }
    assert checks["lint"]["skip_conditions"] == ["on.pull_request.paths"]
    assert checks["Build the docs"]["skip_conditions"] == [
        "on.pull_request.paths",
        "jobs.docs.if",
    ]
    assert checks["unit / pytest"]["skip_conditions"] == [
        "on.pull_request.paths",
        "jobs.pytest.if",
    ]
    assert checks["unit / pytest"]["job_path"] == ["unit", "pytest"]
    assert (
        "skip_conditions" not in derived["checks"][".github/workflows/release.yml"][0]
    )


def test_findings(derived):
    """Top-level write access, inherited secrets, and every unpinned uses."""
    assert set(derived["findings"]) == {
        ".github/workflows/lint.yaml: job ruff step 1: `docker://ghcr.io/astral-sh/ruff:0.15.14` is not pinned to a digest",
        ".github/workflows/pull-request.yml: job scan passes every secret with `secrets: inherit`",
        ".github/workflows/pull-request.yml: job scan: "
        "`example-org/ci-workflows/.github/workflows/scan.yml@main` is not pinned to a commit",
        ".github/workflows/release.yml: grants write access at the top level, to every job",
        ".github/workflows/tests.yml: job pytest step 1: `actions/setup-python@v6` is not pinned to a commit",
        ".github/actions/setup/action.yml: step 1: `actions/setup-python@v6` is not pinned to a commit",
    }


IDENTIFIERS = {
    "GhaWorkflow": "workflow_uri",
    "GhaReusableWorkflow": "workflow_uri",
    "GhaAction": "action_uri",
}


def test_derived_facts_validate_against_the_schema(derived):
    """Every record the script prints is valid data for the class it names."""
    for path, record in {**derived["workflows"], **derived["actions"]}.items():
        data = {k: v for k, v in record.items() if k != "type"}
        data[IDENTIFIERS[record["type"]]] = (
            f"https://github.com/example-org/repo/{path}"
        )
        report = validate(data, str(SCHEMA), record["type"])
        assert not report.results, (path, [r.message for r in report.results])


def _write_bundle(tmp_path, derived, checks):
    """A bundle with a concept for each derived file and the given check concepts."""
    bundle = tmp_path / "knowledge"
    (bundle / "workflows").mkdir(parents=True)
    (bundle / "index.md").write_text(
        f"---\nbase_iri: {BASE}\ntitle: Test\n---\n\n# Test\n"
    )
    for path, record in {**derived["workflows"], **derived["actions"]}.items():
        slug = path.replace("/", "-").replace(".", "-")
        data = {"title": slug, "description": f"The file {path}.", **record}
        (bundle / "workflows" / f"{slug}.md").write_text(
            f"---\n{yaml.safe_dump(data, sort_keys=False)}---\n\n# {slug}\n"
        )
    for name, data in checks.items():
        (bundle / "workflows" / f"{name}.md").write_text(
            f"---\n{yaml.safe_dump(data, sort_keys=False)}---\n\n# {name}\n"
        )
    return bundle


EMITTER = BASE + "workflows/-github-workflows-pull-request-yml"
UNIT = {
    "type": "GhaRequiredStatusCheck",
    "title": "unit / pytest",
    "description": "A required check.",
    "check_context": "unit / pytest",
    "job_path": ["unit", "pytest"],
    "skip_conditions": ["on.pull_request.paths", "jobs.pytest.if"],
    "emitted_by": EMITTER,
}


def test_check_passes_on_a_matching_bundle(tmp_path, derived):
    """No drift when every file has its concept and the check is reported; the skippable check is a finding."""
    bundle = _write_bundle(tmp_path, derived, {"unit-pytest": UNIT})
    drift, found = derive.compare(derived, bundle)
    assert drift == []
    assert len(found) == 1 and "can skip its job" in found[0]
    assert derive.main(["--root", str(REPO), "--check", str(bundle)]) == 0
    assert derive.main(["--root", str(REPO), "--check", str(bundle), "--strict"]) == 1


def test_check_reports_drift(tmp_path, derived):
    """A changed fact, a missing concept, a stale one and a check no job reports."""
    changed = copy.deepcopy(derived)
    job = changed["workflows"][".github/workflows/pull-request.yml"]["jobs"][1]
    job["job_name"] = "Docs"
    del changed["actions"]["actions/labels/action.yaml"]
    changed["actions"]["actions/gone/action.yml"] = {
        "type": "GhaAction",
        "action_path": "actions/gone/action.yml",
        "using": "node20",
    }
    checks = {
        "unit-pytest": {**UNIT, "check_context": "unit / tests"},
        "orphan": {
            **UNIT,
            "check_context": "lint",
            "emitted_by": BASE + "workflows/nowhere",
        },
    }
    bundle = _write_bundle(tmp_path, changed, checks)
    drift, _ = derive.compare(derived, bundle)
    assert any("jobs is" in d and "Docs" in d for d in drift)
    assert "actions/labels/action.yaml has no concept" in drift
    assert any(
        "actions/gone/action.yml, which the repository does not hold" in d
        for d in drift
    )
    assert any(
        "no job of .github/workflows/pull-request.yml reports 'unit / tests'" in d
        for d in drift
    )
    assert any("'lint' names no workflow concept in emitted_by" in d for d in drift)
    assert derive.main(["--root", str(REPO), "--check", str(bundle)]) == 1


def test_check_on_a_called_workflow_outside_the_repository(tmp_path, derived):
    """A check of a job in another repository's workflow is a finding, not drift."""
    scan = {
        **UNIT,
        "check_context": "Security scan / sast",
        "job_path": ["scan", "sast"],
        "skip_conditions": [],
    }
    drift, found = derive.compare(
        derived, _write_bundle(tmp_path, derived, {"scan": scan})
    )
    assert drift == []
    assert any("cannot be checked" in f for f in found)
