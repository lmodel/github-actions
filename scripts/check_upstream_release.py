#!/usr/bin/env python3
"""Check the SchemaStore copy and the REST API version against GitHub.

Three things can go wrong with what this schema is built from without any
change in this repository:

- SchemaStore changes ``github-workflow.json`` or ``github-action.json``, for
  example when GitHub adds a permission scope or a runtime, so the copy and
  the schema fall behind;
- the copied files drift from the commit they were taken from;
- GitHub releases a REST API version newer than the one the rulesets module
  follows.

The copy has no version in its path, so the commit it was taken from is
pinned below, with each copied file's path in SchemaStore's tree. This script
asks the GitHub API for those files' blobs at the pinned commit and on
SchemaStore's default branch, and for the list of supported REST API
versions. It compares every copied file with its pinned blob by git object
hash, so nothing is downloaded but listings. It prints a Markdown report and
exits 1 when SchemaStore has moved a file, a copied file differs in a way not
listed below, or a newer REST API version exists.

GitHub's documentation pages are versionless and are cited rather than
copied, so no script can watch them; the report repeats the date they were
read.

Set ``GITHUB_TOKEN`` to raise the API rate limit. Usage::

    python scripts/check_upstream_release.py [--report FILE]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COPY = ROOT / "src" / "github_actions" / "schema" / "schemastore"
API = "https://api.github.com"
REPO = "SchemaStore/schemastore"

# The commit the copy was taken from, and each copied file's path at it.
# Move the commit when the copy is replaced, together with the schema
# header's annotations (tests/test_schema_rules.py checks that they agree),
# and empty KNOWN_DIFFERENCES.
PINNED_COMMIT = "f7c2f3bcb512651bd980ed6896639ea8ded9ddf0"
FILES = {
    "github-workflow.json": "src/schemas/json/github-workflow.json",
    "github-action.json": "src/schemas/json/github-action.json",
    "LICENSE": "LICENSE",
    "NOTICE": "NOTICE",
}
# The two files the schema renders; a change to them upstream needs a review.
WATCHED = ("github-workflow.json", "github-action.json")

# The REST API version the rulesets and checks modules follow, and the date
# the documentation pages were read.
PINNED_API_VERSION = "2026-03-10"
DOCS_READ = "2026-10-28"

# Files known to differ from the pinned commit. The copy is exact, so there
# are none; list a file here and in NOTICE if one is ever edited on purpose.
KNOWN_DIFFERENCES: set[str] = set()


def _get(url: str) -> bytes:
    req = urllib.request.Request(
        url, headers={"Accept": "application/vnd.github+json", "User-Agent": "lmodel-github-actions-upstream-check"}
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def _blob_sha(path: Path) -> str:
    """The git object hash of a file, as the contents API reports it."""
    data = path.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def _upstream_sha(path: str, ref: str) -> str | None:
    """The blob hash of ``path`` at ``ref`` in SchemaStore, or None if absent."""
    url = f"{API}/repos/{REPO}/contents/{urllib.parse.quote(path)}?ref={ref}"
    try:
        return json.loads(_get(url))["sha"]
    except urllib.error.HTTPError as err:
        if err.code == 404:
            return None
        raise


def check() -> tuple[list[str], bool]:
    """Return the report lines and whether anything needs attention."""
    report = [
        f"- Pinned: SchemaStore commit `{PINNED_COMMIT}`, REST API version {PINNED_API_VERSION}, "
        f"GitHub's documentation pages read on {DOCS_READ}."
    ]
    attention = False

    matching, known, differing = 0, [], []
    for name, upstream_path in FILES.items():
        local = COPY / name
        if not local.is_file():
            differing.append(f"`{name}` is missing from the copy")
            continue
        pinned = _upstream_sha(upstream_path, PINNED_COMMIT)
        if pinned == _blob_sha(local):
            matching += 1
        elif name in KNOWN_DIFFERENCES:
            known.append(name)
        elif pinned is None:
            differing.append(f"`{name}` is not at `{upstream_path}` in the pinned commit")
        else:
            differing.append(f"`{name}` differs from `{upstream_path}` at the pinned commit")
    extra = sorted(p.name for p in COPY.iterdir() if p.is_file() and p.name not in FILES)
    differing += [f"`{name}` is in the copy but not in the pin list" for name in extra]
    report.append(f"- {matching} of {len(FILES)} copied files match the pinned commit byte for byte.")
    if known:
        report.append(f"- Known differences, listed in NOTICE: {', '.join(f'`{k}`' for k in known)}.")
    if differing:
        attention = True
        report.append(f"- **{len(differing)} copied file(s) differ from the pinned commit in a way not listed:**")
        report += [f"  - {d}" for d in differing]

    head = json.loads(_get(f"{API}/repos/{REPO}/commits/HEAD"))["sha"]
    moved = [name for name in WATCHED if _upstream_sha(FILES[name], head) != _upstream_sha(FILES[name], PINNED_COMMIT)]
    if moved:
        attention = True
        report.append(
            f"- **SchemaStore has changed {', '.join(f'`{m}`' for m in moved)} since the pin** "
            f"(default branch at `{head}`). Compare https://github.com/{REPO}/compare/{PINNED_COMMIT}...{head}, "
            f"replace the copy from one commit, move `PINNED_COMMIT` here and the schema header's annotations, "
            f"update NOTICE, and review the schema against the change."
        )
    else:
        report.append(f"- SchemaStore's default branch (`{head}`) holds the same two schemas as the pin.")

    versions = json.loads(_get(f"{API}/versions"))
    newer = sorted(v for v in versions if v > PINNED_API_VERSION)
    if newer:
        attention = True
        report.append(
            f"- **GitHub supports a newer REST API version: {', '.join(newer)}.** Read its section of "
            f"https://docs.github.com/en/rest/about-the-rest-api/breaking-changes for changes to rulesets, "
            f"rules or check runs, then move `PINNED_API_VERSION` here and the schema header's annotation."
        )
    else:
        report.append(f"- Supported REST API versions: {', '.join(sorted(versions))}; none newer than the pin.")
    return report, attention


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--report", type=Path, help="Also write the Markdown report to this file")
    args = parser.parse_args(argv)
    lines, attention = check()
    text = "\n".join(lines) + "\n"
    print(text, end="")
    if args.report:
        args.report.write_text(text, encoding="utf-8")
    return 1 if attention else 0


if __name__ == "__main__":
    sys.exit(main())
