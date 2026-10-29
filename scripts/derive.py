#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Derive the facts github_actions describes from a repository's files.

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

With ``--rulesets FILE``, it also reads the rulesets ``github_export.py
rulesets`` printed, or a ruleset saved as the REST API returns it, and prints
the frontmatter of each ruleset's concept and the facts of each status check
the rulesets require.

With ``--check BUNDLE``, it compares the facts with the concepts in a
knowledge bundle, and exits 1 on drift:

- a file with no concept, or a concept whose file is gone;
- a fact the file and the concept disagree on;
- a required check that no job of its ``emitted_by`` workflow reports, unless
  another app reports it;
- a skip condition that a required check's body does not name;
- with ``--rulesets``, a ruleset or a required check with no concept, a
  concept no ruleset holds or requires, or a fact the two disagree on;
- with ``--check-runs FILE``, which ``github_export.py check-runs`` printed
  for one commit, a required check that no check run or status matched.

Each skip condition of a required check is a finding. A job skipped by its
own ``if``, or because a job it ``needs`` failed or was skipped, reports
success, so the check passes without running; ``if: always()`` never skips.
A path filter skips the run, and a calling job's ``if`` or ``needs`` skips
the call, so no check run carries the name and the check stays pending.
``--strict`` makes findings fail too.

The files are read as data and never run, and the script calls no network,
so it is safe on files a pull request changed. Usage::

    uv run scripts/derive.py [--root DIR] [--exclude PATH ...] [--rulesets FILE ...]
    uv run scripts/derive.py --check .lokf/knowledge [--rulesets FILE ...] [--check-runs FILE] [--strict]
"""

from __future__ import annotations

import argparse
import itertools
import json
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
# An `if` that never skips its job.
ALWAYS = re.compile(r"^\s*(\$\{\{\s*)?always\(\s*\)(\s*\}\})?\s*$")
# A status function that runs a job whatever its `needs` concluded.
STATUS_FUNCTION = re.compile(r"\b(always|failure|cancelled)\(\s*\)")
# The app GitHub Actions reports its check runs as.
ACTIONS_APP_ID = 15368


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
    """What can skip a job: its own `if`, and a job it needs that failed or was skipped."""
    condition = str(job.get("if", ""))
    skips = [f"jobs.{job_id}.if"] if "if" in job and not ALWAYS.match(condition) else []
    if job.get("needs") and not STATUS_FUNCTION.search(condition):
        skips.append(f"jobs.{job_id}.needs")
    return skips


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
                # A skipped job reports success under its own name. A path
                # filter skips the whole run, and a calling job's `if` or
                # `needs` skips the call, which GitHub reports under the
                # caller's name alone, so no check run carries this name.
                _put(record, "leaves_pending", skips + inherited)
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


def _exported(path: Path):
    """The JSON in what github_export.py printed, in the ingest's mirror of it, or in a JSON file."""
    try:
        text = path.read_text(encoding="utf-8")
        start = text.find("```json\n")
        if start >= 0:
            end = text.find("\n```", start + 8)
            text = text[start + 8 : end if end >= 0 else None]
        return json.loads(text)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as err:
        raise SystemExit(
            f"derive: {path} holds no JSON github_export.py printed ({err})"
        ) from None


def read_rulesets(paths: list[Path]) -> dict:
    """The rulesets in the files given, and the rules in effect on the default branch when a file lists them."""
    evidence = {"rulesets": [], "branch_rules": None, "default_branch": None}
    seen = set()
    for path in paths:
        data = _exported(path)
        if isinstance(data, dict) and "rulesets" in data:
            rulesets = data.get("rulesets") or []
            if data.get("branch_rules") is not None:
                evidence["branch_rules"] = (evidence["branch_rules"] or []) + data[
                    "branch_rules"
                ]
                evidence["default_branch"] = data.get("default_branch")
        else:
            rulesets = data if isinstance(data, list) else [data]
        for ruleset in rulesets:
            if ruleset.get("id") not in seen:
                seen.add(ruleset.get("id"))
                evidence["rulesets"].append(ruleset)
    return evidence


def _required(rules: list[dict]):
    """Each required status check in a list of rules, with its rule's parameters."""
    for rule in rules or []:
        if rule.get("type") == "required_status_checks":
            params = rule.get("parameters") or {}
            for entry in params.get("required_status_checks") or []:
                if entry.get("context"):
                    yield entry, params


def ruleset_facts(ruleset: dict) -> dict:
    """The frontmatter of the concept that describes one ruleset."""
    ref = (ruleset.get("conditions") or {}).get("ref_name") or {}
    rules = ruleset.get("rules") or []
    record = {"type": "GhaRepositoryRuleset", "ruleset_id": ruleset.get("id")}
    _put(record, "ruleset_source_type", ruleset.get("source_type"))
    _put(record, "ruleset_source", ruleset.get("source"))
    _put(record, "ruleset_target", ruleset.get("target") or "branch")
    _put(record, "enforcement", ruleset.get("enforcement"))
    _put(record, "ref_name_include", ref.get("include"))
    _put(record, "ref_name_exclude", ref.get("exclude"))
    _put(
        record,
        "bypass_actors",
        [
            {
                key: actor[key]
                for key in ("actor_id", "actor_type", "bypass_mode")
                if actor.get(key) is not None
            }
            for actor in ruleset.get("bypass_actors") or []
        ],
    )
    _put(
        record,
        "rule_types",
        list(dict.fromkeys(r["type"] for r in rules if r.get("type"))),
    )
    return record


def required_checks(evidence: dict) -> dict[str, dict]:
    """The facts of each status check the rulesets require, by its context.

    ``required_by`` lists the rulesets that require it. ``in_effect`` says
    whether a rule in effect on the default branch requires it, when the
    evidence lists those rules.
    """
    branch_rules = evidence.get("branch_rules")
    in_effect = (
        None
        if branch_rules is None
        else {entry["context"] for entry, _ in _required(branch_rules)}
    )
    checks: dict[str, dict] = {}
    for ruleset in evidence["rulesets"]:
        for entry, params in _required(ruleset.get("rules")):
            context = entry["context"]
            if context not in checks:
                record = {"check_context": context}
                _put(record, "integration_id", entry.get("integration_id"))
                for key, field in (
                    ("strict_policy", "strict_required_status_checks_policy"),
                    ("do_not_enforce_on_create", "do_not_enforce_on_create"),
                ):
                    if isinstance(params.get(field), bool):
                        record[key] = params[field]
                record["required_by"] = []
                if in_effect is not None:
                    record["in_effect"] = context in in_effect
                checks[context] = record
            if ruleset.get("id") not in checks[context]["required_by"]:
                checks[context]["required_by"].append(ruleset.get("id"))
    return checks


def derive(
    root: Path, exclude: list[str] | None = None, rulesets: dict | None = None
) -> dict:
    """Everything the script prints, as one mapping."""
    workflows, actions = read_repository(root, exclude or [])
    top = [
        p
        for p, w in workflows.items()
        if any(t != "workflow_call" for t in _triggers(_on(w)))
    ]
    derived = {
        "workflows": {path: workflow_facts(path, w) for path, w in workflows.items()},
        "actions": {path: action_facts(path, a) for path, a in actions.items()},
        "checks": {path: checks_of(path, workflows) for path in top},
        "findings": findings_of(workflows, actions),
    }
    if rulesets is not None:
        derived["rulesets"] = {
            r.get("id"): ruleset_facts(r) for r in rulesets["rulesets"]
        }
        derived["required_checks"] = required_checks(rulesets)
    return derived


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
        return sorted(
            json.dumps(v, sort_keys=True) if isinstance(v, dict) else _text(v)
            for v in value
        )
    if isinstance(value, list):
        return [_text(v) for v in value]
    return value


def _list(value) -> list:
    """A key that holds one value or a list of them, as a list."""
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _document(path: Path) -> tuple[dict | None, str]:
    """A bundle file's frontmatter and the body after it."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None, text
    head = text.split("---", 2)
    return (yaml.safe_load(head[1]), head[2]) if len(head) == 3 else (None, text)


def read_bundle(bundle: Path) -> tuple[dict[str, tuple[str, dict, str]], str]:
    """Each concept by its IRI, with the file it is in and its body, and the base IRI."""
    index = (
        _document(bundle / "index.md")[0] if (bundle / "index.md").exists() else None
    )
    base = (index or {}).get("base_iri", "")
    concepts = {}
    for path in sorted(bundle.rglob("*.md")):
        if path.name in ("index.md", "log.md"):
            continue
        data, body = _document(path)
        if isinstance(data, dict):
            rel = path.relative_to(bundle).with_suffix("").as_posix()
            concepts[data.get("id") or base + rel] = (
                path.relative_to(bundle).as_posix(),
                data,
                body,
            )
    return concepts, base


def _skip_findings(file: str, context: str, check: dict) -> list[str]:
    """What each skip condition of a derived check does to the required check."""
    found = []
    pending = check.get("leaves_pending") or []
    passes = [c for c in check.get("skip_conditions") or [] if c not in pending]
    if passes:
        found.append(
            f"{file}: {context!r} is required, but {', '.join(passes)} can skip its job,"
            " and a skipped job reports success, so the check passes without running"
        )
    if pending:
        found.append(
            f"{file}: {context!r} is required, but {', '.join(pending)} can skip the run or the call"
            " before its job starts, so no check run carries its name and the check stays pending,"
            " which blocks the merge"
        )
    return found


# The keys of a ruleset's concept that the REST API states.
RULESET_KEYS = (
    "ruleset_source_type",
    "ruleset_source",
    "ruleset_target",
    "enforcement",
    "ref_name_include",
    "ref_name_exclude",
    "bypass_actors",
    "rule_types",
)
# The keys of a required check's concept that its ruleset states.
CHECK_KEYS = ("integration_id", "strict_policy", "do_not_enforce_on_create")


def compare_rulesets(evidence: dict, concepts: dict) -> tuple[list[str], list[str]]:
    """Drift between the rulesets and their concepts and those of the checks they require."""
    drift, found = [], []
    by_id = {
        data.get("ruleset_id"): (file, data)
        for file, data, _ in concepts.values()
        if data.get("type") == "GhaRepositoryRuleset"
    }
    held = set()
    for ruleset in evidence["rulesets"]:
        rid = ruleset.get("id")
        if rid not in by_id:
            drift.append(f"ruleset {rid} ({ruleset.get('name')}) has no concept")
            continue
        held.add(rid)
        file, data = by_id[rid]
        facts = ruleset_facts(ruleset)
        # GitHub returns bypass actors only to a token that can edit the
        # ruleset, so an export made without one says nothing about them.
        keys = [
            k
            for k in RULESET_KEYS
            if k != "bypass_actors" or "bypass_actors" in ruleset
        ]
        for key in keys:
            if _normal(key, data.get(key), None) != _normal(key, facts.get(key), None):
                drift.append(
                    f"{file}: {key} is {data.get(key)!r}, but ruleset {rid} says {facts.get(key)!r}"
                )
        requires = sorted(
            dict.fromkeys(
                entry["context"] for entry, _ in _required(ruleset.get("rules"))
            )
        )
        named = sorted(
            str(concepts[iri][1].get("check_context")) if iri in concepts else str(iri)
            for iri in _list(data.get("requires_check"))
        )
        if named != requires:
            drift.append(
                f"{file}: requires_check names {named}, but ruleset {rid} requires {requires}"
            )
    for rid, (file, _) in by_id.items():
        if rid not in held:
            drift.append(f"{file}: ruleset {rid} is not among the rulesets given")

    checks = {
        data.get("check_context"): (file, data)
        for file, data, _ in concepts.values()
        if data.get("type") == "GhaRequiredStatusCheck"
    }
    required = required_checks(evidence)
    branch = evidence.get("default_branch") or "the default branch"
    for context, facts in required.items():
        rulesets = ", ".join(str(r) for r in facts["required_by"])
        if context not in checks:
            drift.append(
                f"{context!r}, which ruleset {rulesets} requires, has no concept"
            )
            continue
        file, data = checks[context]
        for key in CHECK_KEYS:
            if data.get(key) != facts.get(key):
                drift.append(
                    f"{file}: {key} is {data.get(key)!r}, but ruleset {rulesets} says {facts.get(key)!r}"
                )
        if facts.get("in_effect") is False:
            found.append(
                f"{file}: ruleset {rulesets} requires {context!r}, but no rule in effect on {branch} does"
            )
    for context, (file, _) in checks.items():
        if context not in required:
            drift.append(f"{file}: no ruleset given requires {context!r}")
    return drift, found


def compare_check_runs(
    runs: dict, concepts: dict, derived: dict
) -> tuple[list[str], list[str]]:
    """Drift between the required checks and what GitHub recorded on one commit."""
    drift, found = [], []
    where = str(runs.get("sha") or runs.get("ref") or "the commit")[:12]
    pending = {
        c["check_context"]: c.get("leaves_pending") or []
        for checks in derived["checks"].values()
        for c in checks
        if c.get("check_context")
    }
    for file, data, _ in concepts.values():
        if data.get("type") != "GhaRequiredStatusCheck":
            continue
        context, app = data.get("check_context"), data.get("integration_id")
        named = [r for r in runs.get("check_runs") or [] if r.get("name") == context]
        accepted = [r for r in named if app is None or r.get("app_id") == app]
        statuses = [
            s for s in runs.get("statuses") or [] if s.get("context") == context
        ]
        if accepted or statuses:
            if any(r.get("conclusion") == "skipped" for r in accepted):
                found.append(
                    f"{file}: {context!r} was skipped on {where}, and GitHub counts a skipped check as passed"
                )
            continue
        if named:
            apps = ", ".join(
                sorted({str(r.get("app_slug") or r.get("app_id")) for r in named})
            )
            drift.append(
                f"{file}: {context!r} ran on {where} from {apps}, but only app {app} may report it"
            )
            continue
        if pending.get(context):
            # A skipped call is reported under the caller's name alone.
            parts = str(context).split(" / ")
            callers = sorted(
                {
                    r["name"]
                    for r in runs.get("check_runs") or []
                    if r.get("conclusion") == "skipped"
                    and r.get("name")
                    in {" / ".join(parts[:n]) for n in range(1, len(parts))}
                }
            )
            instead = (
                f"; GitHub recorded {', '.join(repr(c) for c in callers)} as skipped instead"
                if callers
                else ""
            )
            found.append(
                f"{file}: no check run on {where} is named {context!r}, so the check stayed pending:"
                f" {', '.join(pending[context])} can skip it before its job starts{instead}"
            )
        else:
            drift.append(
                f"{file}: no check run or status on {where} is named {context!r}, so a merge would wait for it"
            )
    return drift, found


def compare(
    derived: dict,
    bundle: Path,
    rulesets: dict | None = None,
    check_runs: dict | None = None,
) -> tuple[list[str], list[str]]:
    """Drift between the files and the bundle, and findings about the checks."""
    concepts, _ = read_bundle(bundle)
    drift, found = [], []
    by_path = {}
    for iri, (file, data, _) in concepts.items():
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

    for file, data, body in concepts.values():
        if data.get("type") != "GhaRequiredStatusCheck":
            continue
        context = data.get("check_context")
        for condition in _list(data.get("skip_conditions")):
            if str(condition) not in body:
                drift.append(
                    f"{file}: {context!r} can be skipped by {condition}, which its body does not name"
                )
        integration = data.get("integration_id")
        if integration is not None and integration != ACTIONS_APP_ID:
            found.append(
                f"{file}: app {integration} reports {context!r}, not GitHub Actions, so no job here is matched to it"
            )
            continue
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
        found += _skip_findings(file, context, match)
    for more in (
        compare_rulesets(rulesets, concepts) if rulesets is not None else ([], []),
        compare_check_runs(check_runs, concepts, derived)
        if check_runs is not None
        else ([], []),
    ):
        drift += more[0]
        found += more[1]
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
        "--rulesets",
        type=Path,
        action="append",
        default=[],
        metavar="FILE",
        help="What github_export.py rulesets printed, or a ruleset as the REST API returns it; repeatable",
    )
    parser.add_argument(
        "--check-runs",
        type=Path,
        metavar="FILE",
        help="With --check, what github_export.py check-runs printed for one commit",
    )
    parser.add_argument(
        "--strict", action="store_true", help="With --check, fail on findings too"
    )
    args = parser.parse_args(argv)
    if args.check_runs and args.check is None:
        parser.error("--check-runs needs --check")
    rulesets = read_rulesets(args.rulesets) if args.rulesets else None
    derived = derive(args.root, args.exclude, rulesets)
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
    check_runs = _exported(args.check_runs) if args.check_runs else None
    drift, found = compare(derived, args.check, rulesets, check_runs)
    found = derived["findings"] + found
    for line in drift:
        print(f"drift: {line}")
    for line in found:
        print(f"finding: {line}")
    print(f"{len(drift)} drift, {len(found)} finding(s)")
    return 1 if drift or (args.strict and found) else 0


if __name__ == "__main__":
    sys.exit(main())
