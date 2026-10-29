"""Tests of scripts/derive.py against the fixture repository in tests/derive/repo."""

import copy
import importlib.util
import urllib.parse
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
    assert _contexts(derived, ".github/workflows/labels.yml") == ["label / ruff"]
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


def test_conditions_that_leave_a_check_pending(derived):
    """A path filter and a calling job's `if` leave the check pending; the reporting job's own `if` does not."""
    checks = {
        c["check_context"]: c
        for path in (
            ".github/workflows/pull-request.yml",
            ".github/workflows/labels.yml",
        )
        for c in derived["checks"][path]
    }
    assert checks["Build the docs"]["leaves_pending"] == ["on.pull_request.paths"]
    assert checks["unit / pytest"]["leaves_pending"] == ["on.pull_request.paths"]
    assert checks["label / ruff"]["skip_conditions"] == ["jobs.label.if"]
    assert checks["label / ruff"]["leaves_pending"] == ["jobs.label.if"]
    assert "leaves_pending" not in derived["checks"][".github/workflows/release.yml"][0]


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


def _write_bundle(tmp_path, derived, checks, bodies=None):
    """A bundle with a concept for each derived file and the given concepts.

    A concept's body names each of its skip conditions, unless ``bodies``
    gives it another.
    """
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
        body = (bodies or {}).get(name) or f"# {name}\n" + "".join(
            f"\n- `{c}` can skip it.\n" for c in data.get("skip_conditions") or []
        )
        (bundle / "workflows" / f"{name}.md").write_text(
            f"---\n{yaml.safe_dump(data, sort_keys=False)}---\n\n{body}"
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
    """No drift when every file has its concept and the check is reported; each kind of skip is a finding."""
    bundle = _write_bundle(tmp_path, derived, {"unit-pytest": UNIT})
    drift, found = derive.compare(derived, bundle)
    assert drift == []
    assert found == [
        "workflows/unit-pytest.md: 'unit / pytest' is required, but jobs.pytest.if can skip its job,"
        " and a skipped job reports success, so the check passes without running",
        "workflows/unit-pytest.md: 'unit / pytest' is required, but on.pull_request.paths can skip"
        " the run or the call before its job starts, so no check run carries its name and the check"
        " stays pending, which blocks the merge",
    ]
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


def test_a_skip_condition_the_body_does_not_name_is_drift(tmp_path, derived):
    """A skippable required check says in its body what can skip it."""
    bundle = _write_bundle(
        tmp_path,
        derived,
        {"unit-pytest": UNIT},
        {"unit-pytest": "# unit / pytest\n\nOnly `jobs.pytest.if` is named here.\n"},
    )
    drift, _ = derive.compare(derived, bundle)
    assert drift == [
        "workflows/unit-pytest.md: 'unit / pytest' can be skipped by on.pull_request.paths,"
        " which its body does not name"
    ]


def test_a_check_another_app_reports_is_not_matched_to_a_job(tmp_path, derived):
    """A check whose integration_id names another app needs no emitting workflow."""
    external = {
        "type": "GhaRequiredStatusCheck",
        "title": "external / scan",
        "description": "A required check another app reports.",
        "check_context": "external / scan",
        "integration_id": 9999,
    }
    drift, found = derive.compare(
        derived, _write_bundle(tmp_path, derived, {"external-scan": external})
    )
    assert drift == []
    assert found == [
        "workflows/external-scan.md: app 9999 reports 'external / scan', not GitHub Actions,"
        " so no job here is matched to it"
    ]


# --- rulesets and check runs -------------------------------------------------

RULESETS = Path(__file__).parent / "derive" / "rulesets.md"
CHECK_RUNS = Path(__file__).parent / "derive" / "check-runs.md"
LABELS = BASE + "workflows/-github-workflows-labels-yml"


def _rules_concepts():
    """Concepts that match tests/derive/rulesets.md, by file name."""
    check = {"type": "GhaRequiredStatusCheck", "description": "A required check."}
    return {
        "ruleset-main": {
            "type": "GhaRepositoryRuleset",
            "title": "main",
            "description": "The main ruleset.",
            "ruleset_id": 101,
            "ruleset_source_type": "Repository",
            "ruleset_source": "example-org/repo",
            "ruleset_target": "branch",
            "enforcement": "active",
            "ref_name_include": ["~DEFAULT_BRANCH"],
            "bypass_actors": [
                {
                    "bypass_mode": "pull_request",
                    "actor_type": "RepositoryRole",
                    "actor_id": 5,
                }
            ],
            "rule_types": ["required_status_checks", "deletion"],
            "requires_check": [
                BASE + "workflows/unit-pytest",
                BASE + "workflows/label-ruff",
                BASE + "workflows/external-scan",
            ],
        },
        # GitHub hid this ruleset's bypass actors from the export, so the
        # concept's own are not compared.
        "ruleset-docs": {
            "type": "GhaRepositoryRuleset",
            "title": "docs trial",
            "description": "An organization ruleset on trial.",
            "ruleset_id": 202,
            "ruleset_source_type": "Organization",
            "ruleset_source": "example-org",
            "ruleset_target": "branch",
            "enforcement": "evaluate",
            "ref_name_include": ["~ALL"],
            "bypass_actors": [
                {"actor_type": "OrganizationAdmin", "bypass_mode": "always"}
            ],
            "rule_types": ["required_status_checks"],
            "requires_check": [BASE + "workflows/build-the-docs"],
        },
        "unit-pytest": {
            **UNIT,
            "integration_id": 15368,
            "strict_policy": True,
            "do_not_enforce_on_create": False,
        },
        "label-ruff": {
            **check,
            "title": "label / ruff",
            "check_context": "label / ruff",
            "integration_id": 15368,
            "strict_policy": True,
            "do_not_enforce_on_create": False,
            "job_path": ["label", "ruff"],
            "skip_conditions": ["jobs.label.if"],
            "emitted_by": LABELS,
        },
        "external-scan": {
            **check,
            "title": "external / scan",
            "check_context": "external / scan",
            "integration_id": 9999,
            "strict_policy": True,
            "do_not_enforce_on_create": False,
        },
        "build-the-docs": {
            **check,
            "title": "Build the docs",
            "check_context": "Build the docs",
            "strict_policy": False,
            "do_not_enforce_on_create": True,
            "job_path": ["docs"],
            "skip_conditions": ["on.pull_request.paths", "jobs.docs.if"],
            "emitted_by": EMITTER,
        },
    }


def test_read_rulesets_takes_each_form(tmp_path):
    """The export, the ingest's mirror of it, one ruleset, and a list, with no ruleset twice."""
    text = RULESETS.read_text(encoding="utf-8")
    mirror = tmp_path / "rulesets-mirror.md"
    mirror.write_text(
        "---\norigin: command:scripts/github_export.py\ningest: rulesets\n---\n"
        "<!-- A mirror of command:scripts/github_export.py, kept by the ingest. -->\n\n"
        + text
    )
    one = tmp_path / "ruleset-303.json"
    one.write_text('{"id": 303, "name": "tags", "target": "tag", "rules": []}')
    many = tmp_path / "rulesets.json"
    many.write_text('[{"id": 303, "name": "tags"}, {"id": 404, "name": "push"}]')
    evidence = derive.read_rulesets([RULESETS, mirror, one, many])
    assert [r["id"] for r in evidence["rulesets"]] == [101, 202, 303, 404]
    assert evidence["default_branch"] == "main"
    assert len(evidence["branch_rules"]) == 4


def test_ruleset_and_check_facts():
    """A ruleset's frontmatter, and each required check with its rulesets and whether it binds main."""
    evidence = derive.read_rulesets([RULESETS])
    derived = derive.derive(REPO, rulesets=evidence)
    assert derived["rulesets"][101] == {
        "type": "GhaRepositoryRuleset",
        "ruleset_id": 101,
        "ruleset_source_type": "Repository",
        "ruleset_source": "example-org/repo",
        "ruleset_target": "branch",
        "enforcement": "active",
        "ref_name_include": ["~DEFAULT_BRANCH"],
        "bypass_actors": [
            {
                "actor_id": 5,
                "actor_type": "RepositoryRole",
                "bypass_mode": "pull_request",
            }
        ],
        "rule_types": ["deletion", "required_status_checks"],
    }
    assert "bypass_actors" not in derived["rulesets"][202]
    assert derived["required_checks"]["unit / pytest"] == {
        "check_context": "unit / pytest",
        "integration_id": 15368,
        "strict_policy": True,
        "do_not_enforce_on_create": False,
        "required_by": [101],
        "in_effect": True,
    }
    assert derived["required_checks"]["Build the docs"]["in_effect"] is False
    for rid, record in derived["rulesets"].items():
        data = {k: v for k, v in record.items() if k != "type"}
        data["ruleset_uri"] = f"https://github.com/example-org/repo/rules/{rid}"
        report = validate(data, str(SCHEMA), "GhaRepositoryRuleset")
        assert not report.results, (rid, [r.message for r in report.results])
    for context, record in derived["required_checks"].items():
        data = {
            k: v for k, v in record.items() if k not in ("required_by", "in_effect")
        }
        data["check_uri"] = "https://example.org/checks/" + urllib.parse.quote(context)
        report = validate(data, str(SCHEMA), "GhaRequiredStatusCheck")
        assert not report.results, (context, [r.message for r in report.results])


def test_rulesets_match_their_concepts(tmp_path, derived):
    """No drift when each ruleset and required check has a concept that agrees with it."""
    evidence = derive.read_rulesets([RULESETS])
    bundle = _write_bundle(tmp_path, derived, _rules_concepts())
    drift, found = derive.compare(derived, bundle, rulesets=evidence)
    assert drift == []
    assert (
        "workflows/build-the-docs.md: ruleset 202 requires 'Build the docs',"
        " but no rule in effect on main does" in found
    )
    assert any("app 9999 reports 'external / scan'" in f for f in found)
    assert any(
        "'label / ruff' is required, but jobs.label.if can skip the run or the call"
        in f
        for f in found
    )


def test_rulesets_report_drift(tmp_path, derived):
    """A changed fact, a ruleset or check with no concept, and concepts nothing holds any more."""
    concepts = _rules_concepts()
    concepts["ruleset-main"]["enforcement"] = "evaluate"
    concepts["ruleset-main"]["bypass_actors"] = []
    concepts["unit-pytest"]["strict_policy"] = False
    del concepts["external-scan"]
    del concepts["ruleset-docs"]
    concepts["ruleset-gone"] = {
        **concepts["ruleset-main"],
        "ruleset_id": 303,
        "requires_check": [],
    }
    concepts["orphan"] = {
        **concepts["label-ruff"],
        "check_context": "gone",
        "emitted_by": None,
    }
    bundle = _write_bundle(tmp_path, derived, concepts)
    evidence = derive.read_rulesets([RULESETS])
    drift, _ = derive.compare_rulesets(evidence, derive.read_bundle(bundle)[0])
    assert drift == [
        "workflows/ruleset-main.md: enforcement is 'evaluate', but ruleset 101 says 'active'",
        "workflows/ruleset-main.md: bypass_actors is [], but ruleset 101 says"
        " [{'actor_id': 5, 'actor_type': 'RepositoryRole', 'bypass_mode': 'pull_request'}]",
        "workflows/ruleset-main.md: requires_check names ['"
        + BASE
        + "workflows/external-scan',"
        " 'label / ruff', 'unit / pytest'], but ruleset 101 requires"
        " ['external / scan', 'label / ruff', 'unit / pytest']",
        "ruleset 202 (docs trial) has no concept",
        "workflows/ruleset-gone.md: ruleset 303 is not among the rulesets given",
        "workflows/unit-pytest.md: strict_policy is False, but ruleset 101 says True",
        "'external / scan', which ruleset 101 requires, has no concept",
        "workflows/orphan.md: no ruleset given requires 'gone'",
    ]


def test_check_runs(tmp_path, derived):
    """What one commit recorded: a match, a skip, a pending call, another app, a status and a missing run."""
    concepts = _rules_concepts()
    concepts["lint"] = {
        **concepts["label-ruff"],
        "check_context": "lint",
        "job_path": ["lint"],
        "skip_conditions": ["on.pull_request.paths"],
        "emitted_by": EMITTER,
    }
    # Only GitHub Actions may report this one, but another app did.
    concepts["build-the-docs"]["integration_id"] = 15368
    concepts["publish"] = {
        **concepts["label-ruff"],
        "check_context": "publish",
        "job_path": ["publish"],
        "emitted_by": BASE + "workflows/-github-workflows-release-yml",
    }
    del concepts["publish"]["skip_conditions"]
    bundle = _write_bundle(tmp_path, derived, concepts)
    runs = derive._exported(CHECK_RUNS)
    drift, found = derive.compare_check_runs(
        runs, derive.read_bundle(bundle)[0], derived
    )
    assert drift == [
        "workflows/build-the-docs.md: 'Build the docs' ran on 0123456789ab from other-ci,"
        " but only app 15368 may report it",
        "workflows/publish.md: no check run or status on 0123456789ab is named 'publish',"
        " so a merge would wait for it",
    ]
    assert found == [
        "workflows/label-ruff.md: no check run on 0123456789ab is named 'label / ruff', so the"
        " check stayed pending: jobs.label.if can skip it before its job starts; GitHub"
        " recorded 'label' as skipped instead",
        "workflows/lint.md: 'lint' was skipped on 0123456789ab, and GitHub counts a skipped"
        " check as passed",
    ]


def test_check_runs_need_check():
    """--check-runs compares with a bundle, so it needs --check."""
    with pytest.raises(SystemExit):
        derive.main(["--root", str(REPO), "--check-runs", str(CHECK_RUNS)])


def test_main_with_both_files(tmp_path, derived, capsys):
    """The command line reads the rulesets and the check runs and prints one line per result."""
    bundle = _write_bundle(tmp_path, derived, _rules_concepts())
    code = derive.main(
        [
            "--root",
            str(REPO),
            "--check",
            str(bundle),
            "--rulesets",
            str(RULESETS),
            "--check-runs",
            str(CHECK_RUNS),
        ]
    )
    out = capsys.readouterr().out
    assert code == 0
    assert "finding: workflows/label-ruff.md: no check run on 0123456789ab" in out
    assert "finding: workflows/build-the-docs.md: ruleset 202 requires" in out
    assert out.rstrip().endswith("0 drift, 14 finding(s)")
