"""Tests of scripts/github_export.py, with the REST API replaced by fixed answers."""

import importlib.util
import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
SCHEMA = ROOT / "src" / "github_actions" / "schema" / "github_actions.yaml"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


export = _load("github_export")
derive = _load("derive")


def _answers(monkeypatch, answers):
    """Answer each GET from a mapping of path to body, and record the calls."""
    calls = []

    def get(api, path, **params):
        calls.append((path, params.get("page")))
        body = answers[path]
        return body(params.get("page")) if callable(body) else body

    monkeypatch.setattr(export, "_get", get)
    return calls


def test_api_version_matches_the_schema():
    """The script asks for the REST API version the schema follows."""
    header = yaml.safe_load(SCHEMA.read_text())
    assert export.API_VERSION == header["annotations"]["rest_api_version"]


def test_pages_reads_until_a_short_page(monkeypatch):
    """A full page asks for the next one; a short page ends the list."""
    calls = _answers(
        monkeypatch,
        {"/list": lambda page: [{"n": i} for i in range(100 if page == 1 else 3)]},
    )
    items, _ = export._pages("https://api.example", "/list")
    assert len(items) == 103
    assert calls == [("/list", 1), ("/list", 2)]


def test_rulesets(monkeypatch):
    """Each ruleset in full by id, without what depends on the asker, and the default branch's rules."""
    repo = "/repos/example-org/repo"
    _answers(
        monkeypatch,
        {
            repo: {"default_branch": "release/2"},
            f"{repo}/rulesets": [{"id": 9}, {"id": 4}],
            f"{repo}/rulesets/4": {"id": 4, "current_user_can_bypass": "never"},
            f"{repo}/rulesets/9": {"id": 9, "current_user_can_bypass": "always"},
            f"{repo}/rules/branches/release/2": [
                {"ruleset_id": 9, "type": "deletion"},
                {"ruleset_id": 4, "type": "required_status_checks"},
                {"ruleset_id": 4, "type": "deletion"},
            ],
        },
    )
    data = export.rulesets("https://api.example", "example-org/repo")
    assert data["default_branch"] == "release/2"
    assert data["rulesets"] == [{"id": 4}, {"id": 9}]
    assert [(r["ruleset_id"], r["type"]) for r in data["branch_rules"]] == [
        (4, "deletion"),
        (4, "required_status_checks"),
        (9, "deletion"),
    ]


def test_check_runs(monkeypatch):
    """Each check run's name, app and conclusion, and each status, sorted."""
    at = "/repos/example-org/repo/commits/feature/x"
    run = {"status": "completed", "head_sha": "abc", "output": {"title": "dropped"}}
    _answers(
        monkeypatch,
        {
            f"{at}/check-runs": {
                "total_count": 2,
                "check_runs": [
                    {
                        **run,
                        "name": "test",
                        "app": {"id": 15368, "slug": "github-actions"},
                        "conclusion": "success",
                    },
                    {
                        **run,
                        "name": "lint",
                        "app": {"id": 15368, "slug": "github-actions"},
                        "conclusion": "skipped",
                    },
                ],
            },
            f"{at}/status": {
                "sha": "0123456789abcdef",
                "statuses": [
                    {
                        "context": "ci/other",
                        "state": "success",
                        "creator": {"login": "x"},
                    }
                ],
            },
        },
    )
    data = export.check_runs("https://api.example", "example-org/repo", "feature/x")
    assert data["sha"] == "0123456789abcdef"
    assert data["check_runs"] == [
        {
            "name": "lint",
            "app_id": 15368,
            "app_slug": "github-actions",
            "status": "completed",
            "conclusion": "skipped",
        },
        {
            "name": "test",
            "app_id": 15368,
            "app_slug": "github-actions",
            "status": "completed",
            "conclusion": "success",
        },
    ]
    assert data["statuses"] == [{"context": "ci/other", "state": "success"}]


def test_derive_reads_what_the_script_prints(tmp_path):
    """The Markdown's JSON block is what derive.py reads back."""
    data = {"rulesets": [{"id": 1, "name": "A ``` fence in a name"}], "b": "é"}
    text = export.markdown("Title", "A sentence.", data)
    assert text.startswith("# Title\n\nA sentence.\n\n```json\n")
    path = Path(__file__).parent / "derive" / "rulesets.md"
    assert derive._exported(path)["repository"] == "example-org/repo"
    printed = tmp_path / "out.md"
    printed.write_text(text, encoding="utf-8")
    assert derive._exported(printed) == data


def test_the_token_goes_to_the_api_only(monkeypatch):
    """The ingest's token comes first, is never sent on to a redirect, and the version is pinned."""
    seen = {}

    class Answer:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self, *args):
            return b"{}"

    def urlopen(req, timeout):
        seen["req"] = req
        return Answer()

    monkeypatch.setenv("GITHUB_TOKEN", "from-actions")
    monkeypatch.setenv("KNOWLEDGE_INGEST_GITHUB_TOKEN", "from-ingest")
    monkeypatch.setattr(export.urllib.request, "urlopen", urlopen)
    export._get("https://api.example", "/repos/o/r", per_page=100)
    req = seen["req"]
    assert req.full_url == "https://api.example/repos/o/r?per_page=100"
    assert req.unredirected_hdrs == {"Authorization": "Bearer from-ingest"}
    assert "Authorization" not in req.headers
    assert req.headers["X-github-api-version"] == export.API_VERSION


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/example-org/repo.git",
        "https://github.com/example-org/repo",
        "git@github.com:example-org/repo.git",
        "ssh://git@ghe.example.com/example-org/repo",
    ],
)
def test_the_origin_remote_names_the_repository(url):
    assert export.REMOTE.search(url).group(1) == "example-org/repo"


def test_a_repository_named_with_a_dot_is_accepted():
    assert export.REPOSITORY.match("example-org/.github")


@pytest.mark.parametrize(
    "argv",
    [
        [
            "rulesets",
            "--repository",
            "example-org/repo",
            "--api-url",
            "http://api.example",
        ],
        ["rulesets", "--repository", "not a repository"],
        ["rulesets", "--repository", "example-org/.."],
        ["rulesets", "--repository", "../repo"],
        ["check-runs", "--repository", "example-org/repo"],
        ["check-runs", "../../user", "--repository", "example-org/repo"],
    ],
)
def test_main_refuses(argv):
    """Plain http, a malformed repository and a missing or malformed ref stop before any call."""
    with pytest.raises(SystemExit) as stop:
        export.main(argv)
    assert stop.value.code == 2


def test_main_prints_markdown(monkeypatch, capsys):
    """The rulesets command prints the heading, the sentence and the JSON."""
    monkeypatch.setattr(
        export,
        "rulesets",
        lambda api, repo: {
            "default_branch": "main",
            "rulesets": [],
            "branch_rules": [],
        },
    )
    assert export.main(["rulesets", "--repository", "example-org/repo"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("# Rulesets of example-org/repo\n")
    assert "default branch `main`" in out
    assert (
        json.loads(out[out.index("```json\n") + 8 : out.rindex("\n```")])["rulesets"]
        == []
    )
