"""Checks that the schema agrees with the upstream copy it is pinned to."""

import importlib.util
import json
import re
from pathlib import Path

import yaml
from linkml_runtime.utils.schemaview import SchemaView

ROOT = Path(__file__).parent.parent
SCHEMA_DIR = ROOT / "src" / "github_actions" / "schema"
SCHEMA = SCHEMA_DIR / "github_actions.yaml"
WORKFLOW_JSON = json.loads(
    (SCHEMA_DIR / "schemastore" / "github-workflow.json").read_text()
)
ACTION_JSON = json.loads(
    (SCHEMA_DIR / "schemastore" / "github-action.json").read_text()
)

# Runtimes SchemaStore's schema still accepts but GitHub's metadata syntax
# page no longer lists. The schema leaves them out on purpose.
RETIRED_RUNTIMES = {"node12", "node16"}


def _watch():
    spec = importlib.util.spec_from_file_location(
        "watch", ROOT / "scripts" / "check_upstream_release.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _pattern(sv, slot, cls):
    """The slot's pattern on the class, or its range type's when it has none."""
    induced = sv.induced_slot(slot, cls)
    return re.compile(induced.pattern or sv.get_type(induced.range).pattern)


def test_header_pins_match_the_watch():
    """The header records the pins the upstream watch checks."""
    watch = _watch()
    header = yaml.safe_load(SCHEMA.read_text())
    notes = header["annotations"]
    assert notes["schemastore_commit"] == watch.PINNED_COMMIT
    assert notes["rest_api_version"] == watch.PINNED_API_VERSION
    assert notes["docs_read"] == watch.DOCS_READ == header["version"]
    assert watch.PINNED_COMMIT in header["source"]


def test_permission_pattern_admits_every_scope_schemastore_lists():
    """Every scope and level SchemaStore's schema accepts is a valid grant."""
    sv = SchemaView(str(SCHEMA))
    pattern = _pattern(sv, "permissions", "GhaWorkflow")
    assert pattern.pattern == _pattern(sv, "job_permissions", "GhaWorkflowJob").pattern
    defs = WORKFLOW_JSON["definitions"]
    for scope, rule in defs["permissions-event"]["properties"].items():
        levels = rule.get("enum") or defs["permissions-level"]["enum"]
        for level in levels:
            assert pattern.match(f"{scope}: {level}"), (scope, level)
        assert not pattern.match(f"{scope}: admin")
    for shorthand in defs["permissions"]["oneOf"][0]["enum"]:
        assert pattern.match(shorthand)


def test_runtimes_are_schemastores_less_the_retired():
    """The runtime enumeration differs from SchemaStore's only by the retired ones."""
    sv = SchemaView(str(SCHEMA))
    ours = set(sv.get_enum("GhaActionRuntime").permissible_values)
    defs = ACTION_JSON["definitions"]
    theirs = set(defs["runs-javascript"]["properties"]["using"]["enum"])
    theirs |= {
        defs["runs-composite"]["properties"]["using"]["const"],
        defs["runs-docker"]["properties"]["using"]["const"],
    }
    assert theirs - ours == RETIRED_RUNTIMES
    assert ours <= theirs


def test_input_types_are_schemastores():
    """A reusable workflow's input takes the types SchemaStore's schema lists."""
    sv = SchemaView(str(SCHEMA))
    call = WORKFLOW_JSON["properties"]["on"]["oneOf"][2]["properties"]["workflow_call"][
        "oneOf"
    ][1]
    inputs = next(iter(call["properties"]["inputs"]["patternProperties"].values()))
    assert set(sv.get_enum("GhaWorkflowInputType").permissible_values) == set(
        inputs["properties"]["type"]["enum"]
    )


def test_trigger_pattern_admits_every_event_schemastore_lists():
    """Every event SchemaStore's schema names is a valid trigger."""
    sv = SchemaView(str(SCHEMA))
    pattern = _pattern(sv, "triggers", "GhaWorkflow")
    events = set(WORKFLOW_JSON["definitions"]["event"]["enum"])
    events |= set(WORKFLOW_JSON["properties"]["on"]["oneOf"][2]["properties"])
    for event in events:
        assert pattern.match(event), event


def test_key_and_uses_patterns_are_schemastores():
    """Job, input, output and secret keys, and a job's uses, follow SchemaStore's patterns."""
    sv = SchemaView(str(SCHEMA))
    call = WORKFLOW_JSON["properties"]["on"]["oneOf"][2]["properties"]["workflow_call"][
        "oneOf"
    ][1]
    for section in ("inputs", "outputs", "secrets"):
        (key,) = call["properties"][section]["patternProperties"]
        assert sv.get_type("gha_identifier").pattern == key
    (key,) = WORKFLOW_JSON["properties"]["jobs"]["patternProperties"]
    assert sv.get_type("gha_identifier").pattern == key
    uses = WORKFLOW_JSON["definitions"]["reusableWorkflowCallJob"]["properties"][
        "uses"
    ]["pattern"]
    assert _pattern(sv, "calls", "GhaWorkflowJob").pattern == uses
