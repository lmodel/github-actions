#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Derive the facts github_actions describes from a repository's own files.

Reads the workflow files under ``.github/workflows/`` and every ``action.yml``
or ``action.yaml`` of a repository, with ``yaml.safe_load``. For each, it
prints the frontmatter a knowledge concept of the matching class carries:
``GhaWorkflow`` or ``GhaReusableWorkflow`` for a workflow and ``GhaAction``
for an action. It also prints the name of each check run a top-level
workflow's jobs report, as the ``check_context`` a ruleset would require, with
the ``job_path`` and ``skip_conditions`` of the ``GhaRequiredStatusCheck``
that names it.

A check run is named after its job: the job's ``name``, or its id when it has
none. A job of a called workflow is named after the calling job and the
called job, joined by a slash with a space on each side. A matrix job's name
adds its matrix values in parentheses, joined by a comma and a space.
A ``name`` that reads the matrix context takes the values in its own place
instead. A job that calls a workflow in another repository cannot be followed,
since this script reads only the repository it is given; its check names are
reported as unresolved.

It also reports, as findings, what the OpenSSF Baseline and Scorecard call
out: a ``write`` permission at the top level of a workflow, a caller that
passes ``secrets: inherit``, and a ``uses`` that is not pinned to a commit.

With ``--check BUNDLE``, it compares the facts with the concepts in a
knowledge bundle, and exits 1 on drift. Drift is a file with no concept, a
concept whose file is gone, a fact the two disagree on, or a required check
that no job of the workflow its ``emitted_by`` names reports. A required check
whose job a path filter or an ``if`` can skip is a finding, since a skipped
job reports success; ``--strict`` makes findings fail too.

The files are read as data and never run, so the script is safe on files a
pull request changed. Usage::

    uv run scripts/derive.py [--root DIR] [--exclude PATH ...]
    uv run scripts/derive.py --check .lokf/knowledge [--strict]
"""

from __future__ import annotations

import argparse
import itertools
import os
import re
import sys
from pathlib import Path

import yaml

# A commit SHA, the only ref that pins a `uses`.
PINNED_REF = re.compile(r"^[0-9a-f]{40}$")
# A matrix value in a job's name, such as ${{ matrix.python-version }}.
MATRIX_EXPRESSION = re.compile(r"\$\{\{\s*matrix\.([A-Za-z0-9_-]+)\s*\}\}")
# Folders no action of the repository's own lives in.
SKIPPED_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__"}
# GitHub's own limit on how deep workflows can call one another.
MAX_DEPTH = 10
# The events whose filters can skip a whole workflow run.
FILTER_KEYS = ("paths", "paths-ignore")


class _Dumper(yaml.SafeDumper):
    """Indent a list under its key, as the knowledge bundle writes YAML."""

    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def _load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _on(workflow: dict):
    """The `on` key. YAML 1.1 reads a bare `on` as true, and safe_load follows it."""
    return workflow.get("on", workflow.get(True))


def _text(value) -> str:
    """A scalar as GitHub writes it in a name or a default."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def _triggers(on) -> list[str]:
    if isinstance(on, str):
        return [on]
    if isinstance(on, list):
        return [str(event) for event in on]
    if isinstance(on, dict):
        return [str(event) for event in on]
    return []


def _permissions(value) -> list[str] | None:
    """A `permissions` value as the schema's gha_permission strings."""
    if value is None:
        return None
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return (
            [f"{scope}: {level}" for scope, level in value.items()] if value else ["{}"]
        )
    return None


def _put(record: dict, key: str, value) -> None:
    """Set a key only when the file states it, so absent stays absent."""
    if value is not None and value != []:
        record[key] = value


def _job(job_id: str, job: dict) -> dict:
    record = {"job_id": job_id}
    _put(record, "job_name", job.get("name"))
    _put(record, "calls", job.get("uses"))
    runs_on = job.get("runs-on")
    if isinstance(runs_on, dict):
        labels = runs_on.get("labels")
        _put(record, "runs_on", [labels] if isinstance(labels, str) else labels)
        _put(record, "runner_group", runs_on.get("group"))
    elif isinstance(runs_on, str):
        record["runs_on"] = [runs_on]
    elif isinstance(runs_on, list):
        _put(record, "runs_on", [str(label) for label in runs_on])
    _put(record, "job_permissions", _permissions(job.get("permissions")))
    return record


def _declared(spec: dict | None, key: str, fields: dict[str, str]) -> list[dict]:
    """The inputs, outputs or secrets of a workflow_call or an action."""
    records = []
    for name, item in (spec or {}).items():
        item = item or {}
        record = {key: name}
        for schema_key, file_key in fields.items():
            value = item.get(file_key)
            if schema_key == "required" and isinstance(value, str):
                value = value.strip().lower() == "true"
            if schema_key == "default" and value is not None:
                value = _text(value)
            _put(record, schema_key, value)
        records.append(record)
    return records


def workflow_facts(path: str, workflow: dict) -> dict:
    """The frontmatter of the concept that describes one workflow file."""
    on = _on(workflow)
    triggers = _triggers(on)
    reusable = "workflow_call" in triggers
    record = {
        "type": "GhaReusableWorkflow" if reusable else "GhaWorkflow",
        "workflow_path": path,
    }
    _put(record, "triggers", triggers)
    _put(record, "permissions", _permissions(workflow.get("permissions")))
    if reusable:
        call = (on.get("workflow_call") if isinstance(on, dict) else None) or {}
        _put(
            record,
            "inputs",
            _declared(
                call.get("inputs"),
                "input_id",
                {
                    "description": "description",
                    "required": "required",
                    "input_type": "type",
                    "default": "default",
                },
            ),
        )
        _put(
            record,
            "outputs",
            _declared(
                call.get("outputs"),
                "output_id",
                {"description": "description", "output_expression": "value"},
            ),
        )
        _put(
            record,
            "secrets",
            _declared(
                call.get("secrets"),
                "secret_id",
                {"description": "description", "required": "required"},
            ),
        )
    _put(
        record,
        "jobs",
        [
            _job(job_id, job or {})
            for job_id, job in (workflow.get("jobs") or {}).items()
        ],
    )
    return record


def action_facts(path: str, action: dict) -> dict:
    """The frontmatter of the concept that describes one action."""
    record = {"type": "GhaAction", "action_path": path}
    _put(record, "using", (action.get("runs") or {}).get("using"))
    _put(
        record,
        "inputs",
        _declared(
            action.get("inputs"),
            "input_id",
            {
                "description": "description",
                "required": "required",
                "default": "default",
                "deprecation_message": "deprecationMessage",
            },
        ),
    )
    _put(
        record,
        "outputs",
        _declared(
            action.get("outputs"),
            "output_id",
            {"description": "description", "output_expression": "value"},
        ),
    )
    return record


def _combinations(matrix) -> list[dict] | None:
    """The matrix's combinations, or None when an expression sets it."""
    if not isinstance(matrix, dict):
        return None
    base = {
        key: value for key, value in matrix.items() if key not in ("include", "exclude")
    }
    if any(not isinstance(value, list) for value in base.values()):
        return None
    keys = list(base)
    combos = (
        [dict(zip(keys, values)) for values in itertools.product(*base.values())]
        if keys
        else []
    )
    for excluded in matrix.get("exclude") or []:
        combos = [
            c for c in combos if not all(c.get(k) == v for k, v in excluded.items())
        ]
    for included in matrix.get("include") or []:
        # An include extends each combination whose original values it
        # matches, and adds a combination of its own when it matches none.
        matched = False
        for combo in combos:
            if all(combo.get(k) == v for k, v in included.items() if k in keys):
                combo.update({k: v for k, v in included.items() if k not in keys})
                matched = True
        if not matched:
            combos.append(dict(included))
    return combos


def _names(job_id: str, job: dict) -> list[str] | None:
    """The check names one job reports, or None when its matrix is an expression."""
    name = job.get("name") or job_id
    strategy = job.get("strategy") or {}
    if "matrix" not in strategy:
        return [_text(name)]
    combos = _combinations(strategy.get("matrix"))
    if combos is None:
        return None
    if MATRIX_EXPRESSION.search(str(name)):
        return [
            MATRIX_EXPRESSION.sub(
                lambda m, c=c: _text(c.get(m.group(1), "")), str(name)
            )
            for c in combos
        ]
    return [
        f"{name} ({', '.join(_text(v) for v in combo.values())})" for combo in combos
    ]


def _local_workflow(uses: str) -> str | None:
    """The path a same-repository `uses` names, such as ./.github/workflows/x.yml."""
    return uses[2:] if uses.startswith("./") else None


def _job_skips(job_id: str, job: dict) -> list[str]:
    return [f"jobs.{job_id}.if"] if "if" in job else []


def checks_of(path: str, workflows: dict[str, dict]) -> list[dict]:
    """Each check a top-level workflow's jobs report, with how it is named."""
    workflow = workflows[path]
    on = _on(workflow)
    skips = []
    if isinstance(on, dict):
        for event, spec in on.items():
            for key in FILTER_KEYS:
                if isinstance(spec, dict) and key in spec:
                    skips.append(f"on.{event}.{key}")
    checks = []

    def walk(
        jobs: dict,
        prefix: list[str],
        names: list[str],
        inherited: list[str],
        depth: int,
    ) -> None:
        for job_id, job in (jobs or {}).items():
            job = job or {}
            own = _names(job_id, job)
            job_path = prefix + [job_id]
            conditions = inherited + _job_skips(job_id, job)
            if own is None:
                checks.append(
                    {
                        "check_context": None,
                        "job_path": job_path,
                        "unresolved": "matrix set by an expression",
                    }
                )
                continue
            full = [f"{p} / {n}" for p in names for n in own] if names else own
            uses = job.get("uses")
            if uses:
                called = _local_workflow(uses)
                if called is None or called not in workflows or depth >= MAX_DEPTH:
                    reason = (
                        "calls a workflow outside this repository"
                        if called is None
                        else f"calls {called}, which is not here"
                    )
                    for name in full:
                        checks.append(
                            {
                                "check_context": f"{name} / *",
                                "job_path": job_path,
                                "unresolved": reason,
                            }
                        )
                    continue
                walk(
                    workflows[called].get("jobs"), job_path, full, conditions, depth + 1
                )
                continue
            for name in full:
                record = {"check_context": name, "job_path": job_path}
                _put(record, "skip_conditions", skips + conditions)
                checks.append(record)

    walk(workflow.get("jobs"), [], [], [], 0)
    return checks


def _uses_findings(where: str, uses) -> list[str]:
    if not isinstance(uses, str) or uses.startswith("./"):
        return []
    if uses.startswith("docker://"):
        return (
            []
            if "@sha256:" in uses
            else [f"{where}: `{uses}` is not pinned to a digest"]
        )
    ref = uses.rpartition("@")[2] if "@" in uses else ""
    return (
        []
        if PINNED_REF.match(ref)
        else [f"{where}: `{uses}` is not pinned to a commit"]
    )


def findings_of(workflows: dict[str, dict], actions: dict[str, dict]) -> list[str]:
    found = []
    for path, workflow in workflows.items():
        top = workflow.get("permissions")
        if top == "write-all" or (isinstance(top, dict) and "write" in top.values()):
            found.append(f"{path}: grants write access at the top level, to every job")
        for job_id, job in (workflow.get("jobs") or {}).items():
            job = job or {}
            if job.get("secrets") == "inherit":
                found.append(
                    f"{path}: job {job_id} passes every secret with `secrets: inherit`"
                )
            found += _uses_findings(f"{path}: job {job_id}", job.get("uses"))
            for n, step in enumerate(job.get("steps") or []):
                found += _uses_findings(
                    f"{path}: job {job_id} step {n + 1}", (step or {}).get("uses")
                )
    for path, action in actions.items():
        for n, step in enumerate((action.get("runs") or {}).get("steps") or []):
            found += _uses_findings(f"{path}: step {n + 1}", (step or {}).get("uses"))
    return found


def read_repository(
    root: Path, exclude: list[str]
) -> tuple[dict[str, dict], dict[str, dict]]:
    """The repository's workflow files and action metadata files, parsed."""

    def kept(rel: str) -> bool:
        return not any(
            rel == e.rstrip("/") or rel.startswith(e.rstrip("/") + "/") for e in exclude
        )

    workflows = {}
    folder = root / ".github" / "workflows"
    if folder.is_dir():
        for path in sorted(folder.iterdir()):
            rel = path.relative_to(root).as_posix()
            if path.is_file() and path.suffix in (".yml", ".yaml") and kept(rel):
                workflows[rel] = _load(path) or {}
    actions = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIPPED_DIRS)
        for name in sorted(filenames):
            if name in ("action.yml", "action.yaml"):
                rel = (Path(dirpath) / name).relative_to(root).as_posix()
                if kept(rel):
                    actions[rel] = _load(Path(dirpath) / name) or {}
    return workflows, actions


def derive(root: Path, exclude: list[str] | None = None) -> dict:
    """Everything the script prints, as one mapping."""
    workflows, actions = read_repository(root, exclude or [])
    top = [
        p
        for p, w in workflows.items()
        if any(t != "workflow_call" for t in _triggers(_on(w)))
    ]
    return {
        "workflows": {path: workflow_facts(path, w) for path, w in workflows.items()},
        "actions": {path: action_facts(path, a) for path, a in actions.items()},
        "checks": {path: checks_of(path, workflows) for path in top},
        "findings": findings_of(workflows, actions),
    }


# --- comparison with a knowledge bundle ---------------------------------------

# The keys a list item is matched by, for each list the script derives.
ITEM_KEYS = {
    "jobs": "job_id",
    "inputs": "input_id",
    "outputs": "output_id",
    "secrets": "secret_id",
}
ORDERED = {"job_path"}


def _normal(key: str, value, derived_value):
    """A value in a form that compares equal whatever order a list is in,
    keeping only the keys the script derives in a list of records."""
    if key in ITEM_KEYS and isinstance(value, list):
        wanted = {k for item in derived_value or [] for k in item}
        return {
            item.get(ITEM_KEYS[key]): {
                k: _normal(k, v, None) for k, v in item.items() if k in wanted
            }
            for item in value
            if isinstance(item, dict)
        }
    if isinstance(value, list) and key not in ORDERED:
        return sorted(_text(v) for v in value)
    if isinstance(value, list):
        return [_text(v) for v in value]
    return value


def _frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    head = text.split("---", 2)
    return yaml.safe_load(head[1]) if len(head) == 3 else None


def read_bundle(bundle: Path) -> tuple[dict[str, tuple[str, dict]], str]:
    """Each concept by its IRI, with the file it is in, and the base IRI."""
    index = (
        _frontmatter(bundle / "index.md") if (bundle / "index.md").exists() else None
    )
    base = (index or {}).get("base_iri", "")
    concepts = {}
    for path in sorted(bundle.rglob("*.md")):
        if path.name in ("index.md", "log.md"):
            continue
        data = _frontmatter(path)
        if isinstance(data, dict):
            rel = path.relative_to(bundle).with_suffix("").as_posix()
            concepts[data.get("id") or base + rel] = (
                path.relative_to(bundle).as_posix(),
                data,
            )
    return concepts, base


def compare(derived: dict, bundle: Path) -> tuple[list[str], list[str]]:
    """Drift between the files and the bundle, and findings about the checks."""
    concepts, _ = read_bundle(bundle)
    drift, found = [], []
    by_path = {}
    for iri, (file, data) in concepts.items():
        path = data.get("workflow_path") or data.get("action_path")
        if path and str(data.get("type", "")).startswith("Gha"):
            by_path[path] = (iri, file, data)
    facts = {**derived["workflows"], **derived["actions"]}
    for path, record in facts.items():
        if path not in by_path:
            drift.append(f"{path} has no concept")
            continue
        _, file, data = by_path[path]
        if data.get("type") != record["type"]:
            drift.append(
                f"{file}: type is {data.get('type')}, but {path} makes it a {record['type']}"
            )
        for key, value in record.items():
            if key == "type":
                continue
            ours, theirs = (
                _normal(key, data.get(key), value),
                _normal(key, value, value),
            )
            if ours != theirs:
                drift.append(
                    f"{file}: {key} is {data.get(key)!r}, but {path} says {value!r}"
                )
        for key in set(data) & set(ITEM_KEYS) - set(record):
            drift.append(f"{file}: {key} is {data[key]!r}, but {path} declares none")
    for path, (_, file, _) in by_path.items():
        if path not in facts:
            drift.append(f"{file} describes {path}, which the repository does not hold")

    for iri, (file, data) in concepts.items():
        if data.get("type") != "GhaRequiredStatusCheck":
            continue
        context = data.get("check_context")
        emitter = concepts.get(data.get("emitted_by") or "")
        if emitter is None:
            drift.append(f"{file}: {context!r} names no workflow concept in emitted_by")
            continue
        workflow = emitter[1].get("workflow_path")
        reported = derived["checks"].get(workflow)
        if reported is None:
            drift.append(
                f"{file}: {emitter[0]} names {workflow}, which runs no jobs of its own"
            )
            continue
        match = next((c for c in reported if c["check_context"] == context), None)
        if match is None:
            pending = [
                c
                for c in reported
                if c.get("unresolved")
                and c["check_context"]
                and context.startswith(c["check_context"][:-1])
            ]
            if pending:
                found.append(
                    f"{file}: {context!r} cannot be checked: {workflow} {pending[0]['unresolved']}"
                )
            else:
                drift.append(f"{file}: no job of {workflow} reports {context!r}")
            continue
        for key in ("job_path", "skip_conditions"):
            if _normal(key, data.get(key), None) != _normal(key, match.get(key), None):
                drift.append(
                    f"{file}: {key} is {data.get(key)!r}, but {workflow} says {match.get(key)!r}"
                )
        if match.get("skip_conditions"):
            found.append(
                f"{file}: {context!r} is required, but {', '.join(match['skip_conditions'])} can skip its job,"
                " and a skipped job reports success"
            )
    return drift, found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="The repository to read (default: here)",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="PATH",
        help="A path, relative to the root, whose files are not read; repeatable",
    )
    parser.add_argument(
        "--check",
        type=Path,
        metavar="BUNDLE",
        help="Compare the facts with this knowledge bundle",
    )
    parser.add_argument(
        "--strict", action="store_true", help="With --check, fail on findings too"
    )
    args = parser.parse_args(argv)
    derived = derive(args.root, args.exclude)
    if args.check is None:
        yaml.dump(
            derived,
            sys.stdout,
            Dumper=_Dumper,
            sort_keys=False,
            allow_unicode=True,
            width=1000,
        )
        return 0
    drift, found = compare(derived, args.check)
    found = derived["findings"] + found
    for line in drift:
        print(f"drift: {line}")
    for line in found:
        print(f"finding: {line}")
    print(f"{len(drift)} drift, {len(found)} finding(s)")
    return 1 if drift or (args.strict and found) else 0


if __name__ == "__main__":
    sys.exit(main())
