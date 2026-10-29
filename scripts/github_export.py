#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Print what GitHub records about a repository's rulesets or a commit's checks.

derive.py reads files and calls no network, so this script asks GitHub's
REST API what a ruleset requires and what a commit reported. Each command
makes a few read-only calls at the API version the rulesets module follows.
It prints Markdown: a heading, a sentence that says what the text holds, and
the JSON in a fenced block, its keys sorted so that the same answer prints
the same text.

- ``rulesets`` prints each ruleset of the repository as the REST API returns
  it, and the rules in effect on the default branch. A host's ingest runs it
  as an entry of ``kind: command``, and ``derive.py --rulesets`` reads the
  mirror file the ingest writes. On a private repository it needs a token with
  Metadata read.
- ``check-runs REF`` prints the name, app and conclusion of each check run on
  a commit, and the context and state of each commit status, for
  ``derive.py --check-runs``. On a private repository it needs Checks read and
  Commit statuses read.

A public repository needs no token, at a lower rate limit. Otherwise the
token is the first of KNOWLEDGE_INGEST_GITHUB_TOKEN, GH_TOKEN and GITHUB_TOKEN
that is set. It goes to the API's address only, never to an address a
redirect names. GitHub returns a ruleset's bypass actors only to a token that
can edit the ruleset, so without one the field is missing, and derive.py
leaves it out of the comparison.

The address is ``--api-url``, or GITHUB_API_URL, or https://api.github.com.
The ingest passes a command only the variables its ``auth`` block names, so
an entry for GitHub Enterprise Server puts ``--api-url`` in its args. The
repository is ``--repository``, or the one the origin remote names.

It needs Python 3.10 and nothing else, so the ingest can run it as a tracked
command with whatever ``python3`` the job has. Usage::

    python3 scripts/github_export.py rulesets [--repository OWNER/REPO]
    python3 scripts/github_export.py check-runs REF [--repository OWNER/REPO]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

# The REST API version the rulesets module follows; a test holds it to the
# schema's rest_api_version annotation.
API_VERSION = "2026-03-10"
# OWNER/REPO, neither of them `.` or `..`, which would leave the path.
REPOSITORY = re.compile(r"^(?!\.\.?/)[A-Za-z0-9_.-]+/(?!\.\.?$)[A-Za-z0-9_.-]+$")
# The origin remote's owner and name, over https or ssh, with or without .git.
REMOTE = re.compile(r"[:/]([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?/?$")
TOKENS = ("KNOWLEDGE_INGEST_GITHUB_TOKEN", "GH_TOKEN", "GITHUB_TOKEN")
PER_PAGE = 100
# Fields whose value depends on who asks rather than on the ruleset, left out
# so that two tokens print the same text.
ASKER_FIELDS = ("current_user_can_bypass",)


def _token() -> str | None:
    return next((os.environ[n] for n in TOKENS if os.environ.get(n)), None)


def _get(api: str, path: str, **params):
    """One GET of the REST API, parsed. The token is never sent on to a redirect."""
    query = urllib.parse.urlencode(params)
    req = urllib.request.Request(
        f"{api}{path}{'?' + query if query else ''}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "lmodel-github-actions-export",
            "X-GitHub-Api-Version": API_VERSION,
        },
    )
    token = _token()
    if token:
        req.add_unredirected_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as err:
        hint = {
            404: ": the repository, ref or ruleset is not there, or the token cannot read it",
            403: ": the token lacks a permission, or the rate limit is spent",
            429: ": the rate limit is spent",
        }.get(err.code, "")
        raise SystemExit(
            f"github_export: GET {path} answered {err.code} {err.reason}{hint}"
        ) from None
    except urllib.error.URLError as err:
        raise SystemExit(
            f"github_export: {api} cannot be reached ({err.reason})"
        ) from None


def _pages(api: str, path: str, key: str | None = None) -> tuple[list, dict]:
    """Every item of a paged list, and the last page's body for its other keys."""
    items, page = [], 1
    while True:
        body = _get(api, path, per_page=PER_PAGE, page=page)
        batch = (body.get(key) or []) if key else body
        items += batch
        if len(batch) < PER_PAGE:
            return items, (body if key else {})
        page += 1


def origin_repository() -> str | None:
    """The OWNER/REPO the origin remote of the current directory names."""
    try:
        url = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    match = REMOTE.search(url)
    return match.group(1) if match else None


def rulesets(api: str, repository: str) -> dict:
    """The repository's rulesets in full, and the rules in effect on its default branch."""
    branch = _get(api, f"/repos/{repository}").get("default_branch")
    listed, _ = _pages(api, f"/repos/{repository}/rulesets")
    full = []
    for item in sorted(listed, key=lambda r: r.get("id") or 0):
        ruleset = _get(api, f"/repos/{repository}/rulesets/{int(item['id'])}")
        for field in ASKER_FIELDS:
            ruleset.pop(field, None)
        full.append(ruleset)
    rules = []
    if branch:
        rules, _ = _pages(
            api,
            f"/repos/{repository}/rules/branches/{urllib.parse.quote(branch, safe='/')}",
        )
    return {
        "api_version": API_VERSION,
        "repository": repository,
        "default_branch": branch,
        "rulesets": full,
        "branch_rules": sorted(
            rules, key=lambda r: (r.get("ruleset_id") or 0, r.get("type") or "")
        ),
    }


def check_runs(api: str, repository: str, ref: str) -> dict:
    """The check runs and commit statuses GitHub recorded on one commit."""
    at = f"/repos/{repository}/commits/{urllib.parse.quote(ref, safe='/')}"
    runs, _ = _pages(api, f"{at}/check-runs", "check_runs")
    statuses, combined = _pages(api, f"{at}/status", "statuses")
    return {
        "api_version": API_VERSION,
        "repository": repository,
        "ref": ref,
        "sha": combined.get("sha"),
        "check_runs": sorted(
            (
                {
                    "name": run.get("name"),
                    "app_id": (run.get("app") or {}).get("id"),
                    "app_slug": (run.get("app") or {}).get("slug"),
                    "status": run.get("status"),
                    "conclusion": run.get("conclusion"),
                }
                for run in runs
            ),
            key=lambda r: (r["name"] or "", r["app_id"] or 0),
        ),
        "statuses": sorted(
            ({"context": s.get("context"), "state": s.get("state")} for s in statuses),
            key=lambda s: s["context"] or "",
        ),
    }


def markdown(title: str, sentence: str, data: dict) -> str:
    """The text the script prints: a heading, a sentence and the JSON in a fenced block."""
    body = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
    return f"# {title}\n\n{sentence}\n\n```json\n{body}\n```\n"


def main(argv: list[str] | None = None) -> int:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--repository",
        metavar="OWNER/REPO",
        help="The repository to ask about (default: the origin remote's)",
    )
    common.add_argument(
        "--api-url",
        default=os.environ.get("GITHUB_API_URL") or "https://api.github.com",
        help="The REST API's address (default: GITHUB_API_URL, or https://api.github.com)",
    )
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser(
        "rulesets",
        parents=[common],
        help="The rulesets, and the rules in effect on the default branch",
    )
    runs = sub.add_parser(
        "check-runs",
        parents=[common],
        help="The check runs and commit statuses on one commit",
    )
    runs.add_argument("ref", help="A commit SHA, a branch name or a tag name")
    args = parser.parse_args(argv)
    api = args.api_url.rstrip("/")
    if not api.startswith("https://"):
        parser.error(
            "--api-url is an https address, so the token never travels in clear"
        )
    repository = args.repository or origin_repository()
    if not repository or not REPOSITORY.match(repository):
        parser.error("--repository is OWNER/REPO, or the origin remote names one")
    if args.command == "check-runs" and (
        not args.ref.strip() or args.ref.startswith("/") or ".." in args.ref
    ):
        parser.error("REF is a commit SHA, a branch name or a tag name")
    if args.command == "rulesets":
        data = rulesets(api, repository)
        sys.stdout.write(
            markdown(
                f"Rulesets of {repository}",
                f"The rulesets of {repository}, and the rules in effect on its default branch"
                f" `{data['default_branch']}`, as GitHub's REST API (version {API_VERSION})"
                " returns them. `scripts/github_export.py rulesets` printed this, and"
                " `scripts/derive.py --rulesets` reads the JSON below.",
                data,
            )
        )
    else:
        data = check_runs(api, repository, args.ref)
        sys.stdout.write(
            markdown(
                f"Checks on {str(data['sha'] or args.ref)[:12]} in {repository}",
                f"The check runs and commit statuses GitHub recorded on `{args.ref}` in"
                f" {repository}, as its REST API (version {API_VERSION}) returns them."
                " `scripts/github_export.py check-runs` printed this, and"
                " `scripts/derive.py --check-runs` reads the JSON below.",
                data,
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
