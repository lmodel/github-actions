# Auto generated from github_actions.yaml by pythongen.py version: 0.0.1
# Schema: github_actions
#
# id: https://w3id.org/lmodel/github-actions
# description: A LinkML model of what GitHub Actions files and repository rulesets state: workflows and their jobs, reusable workflows with their inputs, outputs and secrets, actions with their runtimes, and the rulesets and required status checks that tie a workflow's jobs to the refs a ruleset protects.
# license: Apache-2.0

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Integer, String, Uri
from linkml_runtime.utils.metamodelcore import Bool, URI

metamodel_version = "1.12.0"
version = "2026-10-28"

# Namespaces
CDX = CurieNamespace('cdx', 'http://cyclonedx.org/schema/bom-1.7.schema.json#/definitions/')
GHA = CurieNamespace('gha', 'https://w3id.org/lmodel/github-actions/')
IN_TOTO = CurieNamespace('in_toto', 'https://in-toto.io/attestation/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SPDX_BUILD = CurieNamespace('spdx_build', 'https://spdx.org/rdf/3.0.1/terms/Build/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = GHA


# Types
class GhaIdentifier(String):
    """ A key GitHub accepts for a job, an input, an output or a secret: a letter or an underscore, then letters, digits, hyphens or underscores. """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "gha_identifier"
    type_model_uri = GHA.GhaIdentifier


class GhaPermission(String):
    """ One grant of access to a workflow's GITHUB_TOKEN, written as the scope, a colon and `read`, `write` or `none`; `read-all`, `write-all` or `{}` stands alone for the shorthand of the same name or the empty map. """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "gha_permission"
    type_model_uri = GHA.GhaPermission


# Class references
class GhaWorkflowWorkflowUri(URI):
    pass


class GhaReusableWorkflowWorkflowUri(GhaWorkflowWorkflowUri):
    pass


class GhaActionActionUri(URI):
    pass


class GhaRepositoryRulesetRulesetUri(URI):
    pass


class GhaRequiredStatusCheckCheckUri(URI):
    pass


@dataclass(repr=False)
class GhaDocument(YAMLRoot):
    """
    A document that holds the workflows, actions, rulesets and required status checks of one or more repositories.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GHA["Document"]
    class_class_curie: ClassVar[str] = "gha:Document"
    class_name: ClassVar[str] = "GhaDocument"
    class_model_uri: ClassVar[URIRef] = GHA.GhaDocument

    workflows: Optional[Union[dict[Union[str, GhaWorkflowWorkflowUri], Union[dict, "GhaWorkflow"]], list[Union[dict, "GhaWorkflow"]]]] = empty_dict()
    reusable_workflows: Optional[Union[dict[Union[str, GhaReusableWorkflowWorkflowUri], Union[dict, "GhaReusableWorkflow"]], list[Union[dict, "GhaReusableWorkflow"]]]] = empty_dict()
    actions: Optional[Union[dict[Union[str, GhaActionActionUri], Union[dict, "GhaAction"]], list[Union[dict, "GhaAction"]]]] = empty_dict()
    rulesets: Optional[Union[dict[Union[str, GhaRepositoryRulesetRulesetUri], Union[dict, "GhaRepositoryRuleset"]], list[Union[dict, "GhaRepositoryRuleset"]]]] = empty_dict()
    required_checks: Optional[Union[dict[Union[str, GhaRequiredStatusCheckCheckUri], Union[dict, "GhaRequiredStatusCheck"]], list[Union[dict, "GhaRequiredStatusCheck"]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_list(slot_name="workflows", slot_type=GhaWorkflow, key_name="workflow_uri", keyed=True)

        self._normalize_inlined_as_list(slot_name="reusable_workflows", slot_type=GhaReusableWorkflow, key_name="workflow_uri", keyed=True)

        self._normalize_inlined_as_list(slot_name="actions", slot_type=GhaAction, key_name="action_uri", keyed=True)

        self._normalize_inlined_as_list(slot_name="rulesets", slot_type=GhaRepositoryRuleset, key_name="ruleset_uri", keyed=True)

        self._normalize_inlined_as_list(slot_name="required_checks", slot_type=GhaRequiredStatusCheck, key_name="check_uri", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GhaRequiredMixin(YAMLRoot):
    """
    The field that says whether a caller must supply a value.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GHA["GhaRequiredMixin"]
    class_class_curie: ClassVar[str] = "gha:GhaRequiredMixin"
    class_name: ClassVar[str] = "GhaRequiredMixin"
    class_model_uri: ClassVar[URIRef] = GHA.GhaRequiredMixin

    required: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.required is not None and not isinstance(self.required, Bool):
            self.required = Bool(self.required)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GhaInput(YAMLRoot):
    """
    An input that a reusable workflow or an action declares, under the key a caller writes in its `with` map.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GHA["Input"]
    class_class_curie: ClassVar[str] = "gha:Input"
    class_name: ClassVar[str] = "GhaInput"
    class_model_uri: ClassVar[URIRef] = GHA.GhaInput

    input_id: Union[str, GhaIdentifier] = None
    description: Optional[str] = None
    default: Optional[str] = None
    required: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.input_id):
            self.MissingRequiredField("input_id")
        if not isinstance(self.input_id, GhaIdentifier):
            self.input_id = GhaIdentifier(self.input_id)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.default is not None and not isinstance(self.default, str):
            self.default = str(self.default)

        if self.required is not None and not isinstance(self.required, Bool):
            self.required = Bool(self.required)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GhaOutput(YAMLRoot):
    """
    An output that a reusable workflow or an action declares for the job or step that calls it to read.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GHA["Output"]
    class_class_curie: ClassVar[str] = "gha:Output"
    class_name: ClassVar[str] = "GhaOutput"
    class_model_uri: ClassVar[URIRef] = GHA.GhaOutput

    output_id: Union[str, GhaIdentifier] = None
    description: Optional[str] = None
    output_expression: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.output_id):
            self.MissingRequiredField("output_id")
        if not isinstance(self.output_id, GhaIdentifier):
            self.output_id = GhaIdentifier(self.output_id)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.output_expression is not None and not isinstance(self.output_expression, str):
            self.output_expression = str(self.output_expression)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GhaWorkflow(YAMLRoot):
    """
    A workflow file in a repository's `.github/workflows` directory: the events that run it, the access its
    GITHUB_TOKEN gets, and its jobs.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GHA["Workflow"]
    class_class_curie: ClassVar[str] = "gha:Workflow"
    class_name: ClassVar[str] = "GhaWorkflow"
    class_model_uri: ClassVar[URIRef] = GHA.GhaWorkflow

    workflow_uri: Union[str, GhaWorkflowWorkflowUri] = None
    triggers: Union[str, list[str]] = None
    workflow_path: str = None
    jobs: Union[Union[dict, "GhaWorkflowJob"], list[Union[dict, "GhaWorkflowJob"]]] = None
    workflow_repository: Optional[Union[str, URI]] = None
    permissions: Optional[Union[Union[str, GhaPermission], list[Union[str, GhaPermission]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.workflow_uri):
            self.MissingRequiredField("workflow_uri")
        if not isinstance(self.workflow_uri, GhaWorkflowWorkflowUri):
            self.workflow_uri = GhaWorkflowWorkflowUri(self.workflow_uri)

        if self._is_empty(self.triggers):
            self.MissingRequiredField("triggers")
        if not isinstance(self.triggers, list):
            self.triggers = [self.triggers] if self.triggers is not None else []
        self.triggers = [v if isinstance(v, str) else str(v) for v in self.triggers]

        if self._is_empty(self.workflow_path):
            self.MissingRequiredField("workflow_path")
        if not isinstance(self.workflow_path, str):
            self.workflow_path = str(self.workflow_path)

        if self._is_empty(self.jobs):
            self.MissingRequiredField("jobs")
        self._normalize_inlined_as_list(slot_name="jobs", slot_type=GhaWorkflowJob, key_name="job_id", keyed=False)

        if self.workflow_repository is not None and not isinstance(self.workflow_repository, URI):
            self.workflow_repository = URI(self.workflow_repository)

        if not isinstance(self.permissions, list):
            self.permissions = [self.permissions] if self.permissions is not None else []
        self.permissions = [v if isinstance(v, GhaPermission) else GhaPermission(v) for v in self.permissions]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GhaReusableWorkflow(GhaWorkflow):
    """
    A workflow that other workflows call as a job, because its `on` key names `workflow_call`; it declares the inputs,
    outputs and secrets its callers pass and read.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GHA["ReusableWorkflow"]
    class_class_curie: ClassVar[str] = "gha:ReusableWorkflow"
    class_name: ClassVar[str] = "GhaReusableWorkflow"
    class_model_uri: ClassVar[URIRef] = GHA.GhaReusableWorkflow

    workflow_uri: Union[str, GhaReusableWorkflowWorkflowUri] = None
    workflow_path: str = None
    jobs: Union[Union[dict, "GhaWorkflowJob"], list[Union[dict, "GhaWorkflowJob"]]] = None
    triggers: Union[str, list[str]] = None
    inputs: Optional[Union[Union[dict, "GhaWorkflowInput"], list[Union[dict, "GhaWorkflowInput"]]]] = empty_list()
    outputs: Optional[Union[Union[dict, "GhaWorkflowOutput"], list[Union[dict, "GhaWorkflowOutput"]]]] = empty_list()
    secrets: Optional[Union[Union[dict, "GhaWorkflowSecret"], list[Union[dict, "GhaWorkflowSecret"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.workflow_uri):
            self.MissingRequiredField("workflow_uri")
        if not isinstance(self.workflow_uri, GhaReusableWorkflowWorkflowUri):
            self.workflow_uri = GhaReusableWorkflowWorkflowUri(self.workflow_uri)

        if self._is_empty(self.triggers):
            self.MissingRequiredField("triggers")
        if not isinstance(self.triggers, list):
            self.triggers = [self.triggers] if self.triggers is not None else []
        self.triggers = [v if isinstance(v, str) else str(v) for v in self.triggers]

        self._normalize_inlined_as_list(slot_name="inputs", slot_type=GhaWorkflowInput, key_name="input_id", keyed=False)

        self._normalize_inlined_as_list(slot_name="outputs", slot_type=GhaWorkflowOutput, key_name="output_id", keyed=False)

        self._normalize_inlined_as_list(slot_name="secrets", slot_type=GhaWorkflowSecret, key_name="secret_id", keyed=False)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GhaWorkflowJob(YAMLRoot):
    """
    A job under a workflow's `jobs` key: steps that run on a runner, or a call to a reusable workflow.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GHA["WorkflowJob"]
    class_class_curie: ClassVar[str] = "gha:WorkflowJob"
    class_name: ClassVar[str] = "GhaWorkflowJob"
    class_model_uri: ClassVar[URIRef] = GHA.GhaWorkflowJob

    job_id: Union[str, GhaIdentifier] = None
    job_name: Optional[str] = None
    calls: Optional[str] = None
    runs_on: Optional[Union[str, list[str]]] = empty_list()
    runner_group: Optional[str] = None
    runner_environment: Optional[Union[str, "GhaRunnerEnvironment"]] = None
    job_permissions: Optional[Union[Union[str, GhaPermission], list[Union[str, GhaPermission]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.job_id):
            self.MissingRequiredField("job_id")
        if not isinstance(self.job_id, GhaIdentifier):
            self.job_id = GhaIdentifier(self.job_id)

        if self.job_name is not None and not isinstance(self.job_name, str):
            self.job_name = str(self.job_name)

        if self.calls is not None and not isinstance(self.calls, str):
            self.calls = str(self.calls)

        if not isinstance(self.runs_on, list):
            self.runs_on = [self.runs_on] if self.runs_on is not None else []
        self.runs_on = [v if isinstance(v, str) else str(v) for v in self.runs_on]

        if self.runner_group is not None and not isinstance(self.runner_group, str):
            self.runner_group = str(self.runner_group)

        if self.runner_environment is not None and not isinstance(self.runner_environment, GhaRunnerEnvironment):
            self.runner_environment = GhaRunnerEnvironment(self.runner_environment)

        if not isinstance(self.job_permissions, list):
            self.job_permissions = [self.job_permissions] if self.job_permissions is not None else []
        self.job_permissions = [v if isinstance(v, GhaPermission) else GhaPermission(v) for v in self.job_permissions]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GhaWorkflowInput(GhaInput):
    """
    An input under a reusable workflow's `on.workflow_call.inputs` key.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GHA["WorkflowInput"]
    class_class_curie: ClassVar[str] = "gha:WorkflowInput"
    class_name: ClassVar[str] = "GhaWorkflowInput"
    class_model_uri: ClassVar[URIRef] = GHA.GhaWorkflowInput

    input_id: Union[str, GhaIdentifier] = None
    input_type: Union[str, "GhaWorkflowInputType"] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.input_type):
            self.MissingRequiredField("input_type")
        if not isinstance(self.input_type, GhaWorkflowInputType):
            self.input_type = GhaWorkflowInputType(self.input_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GhaWorkflowOutput(GhaOutput):
    """
    An output under a reusable workflow's `on.workflow_call.outputs` key, set from an output of one of its jobs.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GHA["WorkflowOutput"]
    class_class_curie: ClassVar[str] = "gha:WorkflowOutput"
    class_name: ClassVar[str] = "GhaWorkflowOutput"
    class_model_uri: ClassVar[URIRef] = GHA.GhaWorkflowOutput

    output_id: Union[str, GhaIdentifier] = None
    output_expression: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.output_expression):
            self.MissingRequiredField("output_expression")
        if not isinstance(self.output_expression, str):
            self.output_expression = str(self.output_expression)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GhaWorkflowSecret(YAMLRoot):
    """
    A secret under a reusable workflow's `on.workflow_call.secrets` key, by name; its value is never recorded.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GHA["WorkflowSecret"]
    class_class_curie: ClassVar[str] = "gha:WorkflowSecret"
    class_name: ClassVar[str] = "GhaWorkflowSecret"
    class_model_uri: ClassVar[URIRef] = GHA.GhaWorkflowSecret

    secret_id: Union[str, GhaIdentifier] = None
    description: Optional[str] = None
    required: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.secret_id):
            self.MissingRequiredField("secret_id")
        if not isinstance(self.secret_id, GhaIdentifier):
            self.secret_id = GhaIdentifier(self.secret_id)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.required is not None and not isinstance(self.required, Bool):
            self.required = Bool(self.required)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GhaAction(YAMLRoot):
    """
    An action: a directory whose `action.yml` or `action.yaml` file names its inputs, its outputs and the runtime that
    executes it. A workflow step runs it with `uses`.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GHA["Action"]
    class_class_curie: ClassVar[str] = "gha:Action"
    class_name: ClassVar[str] = "GhaAction"
    class_model_uri: ClassVar[URIRef] = GHA.GhaAction

    action_uri: Union[str, GhaActionActionUri] = None
    action_path: str = None
    using: Union[str, "GhaActionRuntime"] = None
    inputs: Optional[Union[Union[dict, "GhaActionInput"], list[Union[dict, "GhaActionInput"]]]] = empty_list()
    outputs: Optional[Union[Union[dict, "GhaActionOutput"], list[Union[dict, "GhaActionOutput"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.action_uri):
            self.MissingRequiredField("action_uri")
        if not isinstance(self.action_uri, GhaActionActionUri):
            self.action_uri = GhaActionActionUri(self.action_uri)

        if self._is_empty(self.action_path):
            self.MissingRequiredField("action_path")
        if not isinstance(self.action_path, str):
            self.action_path = str(self.action_path)

        if self._is_empty(self.using):
            self.MissingRequiredField("using")
        if not isinstance(self.using, GhaActionRuntime):
            self.using = GhaActionRuntime(self.using)

        self._normalize_inlined_as_list(slot_name="inputs", slot_type=GhaActionInput, key_name="input_id", keyed=False)

        self._normalize_inlined_as_list(slot_name="outputs", slot_type=GhaActionOutput, key_name="output_id", keyed=False)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GhaActionInput(GhaInput):
    """
    An input under an action's `inputs` key.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GHA["ActionInput"]
    class_class_curie: ClassVar[str] = "gha:ActionInput"
    class_name: ClassVar[str] = "GhaActionInput"
    class_model_uri: ClassVar[URIRef] = GHA.GhaActionInput

    input_id: Union[str, GhaIdentifier] = None
    description: str = None
    deprecation_message: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.description):
            self.MissingRequiredField("description")
        if not isinstance(self.description, str):
            self.description = str(self.description)

        if self.deprecation_message is not None and not isinstance(self.deprecation_message, str):
            self.deprecation_message = str(self.deprecation_message)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GhaActionOutput(GhaOutput):
    """
    An output under an action's `outputs` key.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GHA["ActionOutput"]
    class_class_curie: ClassVar[str] = "gha:ActionOutput"
    class_name: ClassVar[str] = "GhaActionOutput"
    class_model_uri: ClassVar[URIRef] = GHA.GhaActionOutput

    output_id: Union[str, GhaIdentifier] = None
    description: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.description):
            self.MissingRequiredField("description")
        if not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GhaRepositoryRuleset(YAMLRoot):
    """
    A ruleset: named rules that GitHub enforces on the branches, tags or pushes of a repository, or of every
    repository in an organization or enterprise that it targets.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GHA["RepositoryRuleset"]
    class_class_curie: ClassVar[str] = "gha:RepositoryRuleset"
    class_name: ClassVar[str] = "GhaRepositoryRuleset"
    class_model_uri: ClassVar[URIRef] = GHA.GhaRepositoryRuleset

    ruleset_uri: Union[str, GhaRepositoryRulesetRulesetUri] = None
    ruleset_target: Union[str, "GhaRulesetTarget"] = None
    enforcement: Union[str, "GhaRulesetEnforcement"] = None
    ruleset_id: Optional[int] = None
    ruleset_source_type: Optional[Union[str, "GhaRulesetSourceType"]] = None
    ruleset_source: Optional[str] = None
    ref_name_include: Optional[Union[str, list[str]]] = empty_list()
    ref_name_exclude: Optional[Union[str, list[str]]] = empty_list()
    bypass_actors: Optional[Union[Union[dict, "GhaBypassActor"], list[Union[dict, "GhaBypassActor"]]]] = empty_list()
    rule_types: Optional[Union[str, list[str]]] = empty_list()
    requires_check: Optional[Union[Union[str, GhaRequiredStatusCheckCheckUri], list[Union[str, GhaRequiredStatusCheckCheckUri]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.ruleset_uri):
            self.MissingRequiredField("ruleset_uri")
        if not isinstance(self.ruleset_uri, GhaRepositoryRulesetRulesetUri):
            self.ruleset_uri = GhaRepositoryRulesetRulesetUri(self.ruleset_uri)

        if self._is_empty(self.ruleset_target):
            self.MissingRequiredField("ruleset_target")
        if not isinstance(self.ruleset_target, GhaRulesetTarget):
            self.ruleset_target = GhaRulesetTarget(self.ruleset_target)

        if self._is_empty(self.enforcement):
            self.MissingRequiredField("enforcement")
        if not isinstance(self.enforcement, GhaRulesetEnforcement):
            self.enforcement = GhaRulesetEnforcement(self.enforcement)

        if self.ruleset_id is not None and not isinstance(self.ruleset_id, int):
            self.ruleset_id = int(self.ruleset_id)

        if self.ruleset_source_type is not None and not isinstance(self.ruleset_source_type, GhaRulesetSourceType):
            self.ruleset_source_type = GhaRulesetSourceType(self.ruleset_source_type)

        if self.ruleset_source is not None and not isinstance(self.ruleset_source, str):
            self.ruleset_source = str(self.ruleset_source)

        if not isinstance(self.ref_name_include, list):
            self.ref_name_include = [self.ref_name_include] if self.ref_name_include is not None else []
        self.ref_name_include = [v if isinstance(v, str) else str(v) for v in self.ref_name_include]

        if not isinstance(self.ref_name_exclude, list):
            self.ref_name_exclude = [self.ref_name_exclude] if self.ref_name_exclude is not None else []
        self.ref_name_exclude = [v if isinstance(v, str) else str(v) for v in self.ref_name_exclude]

        self._normalize_inlined_as_list(slot_name="bypass_actors", slot_type=GhaBypassActor, key_name="actor_type", keyed=False)

        if not isinstance(self.rule_types, list):
            self.rule_types = [self.rule_types] if self.rule_types is not None else []
        self.rule_types = [v if isinstance(v, str) else str(v) for v in self.rule_types]

        if not isinstance(self.requires_check, list):
            self.requires_check = [self.requires_check] if self.requires_check is not None else []
        self.requires_check = [v if isinstance(v, GhaRequiredStatusCheckCheckUri) else GhaRequiredStatusCheckCheckUri(v) for v in self.requires_check]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GhaBypassActor(YAMLRoot):
    """
    An actor who may bypass a ruleset, and when.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GHA["BypassActor"]
    class_class_curie: ClassVar[str] = "gha:BypassActor"
    class_name: ClassVar[str] = "GhaBypassActor"
    class_model_uri: ClassVar[URIRef] = GHA.GhaBypassActor

    actor_type: str = None
    actor_id: Optional[int] = None
    bypass_mode: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.actor_type):
            self.MissingRequiredField("actor_type")
        if not isinstance(self.actor_type, str):
            self.actor_type = str(self.actor_type)

        if self.actor_id is not None and not isinstance(self.actor_id, int):
            self.actor_id = int(self.actor_id)

        if self.bypass_mode is not None and not isinstance(self.bypass_mode, str):
            self.bypass_mode = str(self.bypass_mode)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GhaRequiredStatusCheck(YAMLRoot):
    """
    A status check that a ruleset requires to pass before a change reaches a ref it targets, named by the context a
    check run must report.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GHA["RequiredStatusCheck"]
    class_class_curie: ClassVar[str] = "gha:RequiredStatusCheck"
    class_name: ClassVar[str] = "GhaRequiredStatusCheck"
    class_model_uri: ClassVar[URIRef] = GHA.GhaRequiredStatusCheck

    check_uri: Union[str, GhaRequiredStatusCheckCheckUri] = None
    check_context: str = None
    integration_id: Optional[int] = None
    strict_policy: Optional[Union[bool, Bool]] = None
    do_not_enforce_on_create: Optional[Union[bool, Bool]] = None
    job_path: Optional[Union[Union[str, GhaIdentifier], list[Union[str, GhaIdentifier]]]] = empty_list()
    skip_conditions: Optional[Union[str, list[str]]] = empty_list()
    emitted_by: Optional[Union[str, GhaWorkflowWorkflowUri]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.check_uri):
            self.MissingRequiredField("check_uri")
        if not isinstance(self.check_uri, GhaRequiredStatusCheckCheckUri):
            self.check_uri = GhaRequiredStatusCheckCheckUri(self.check_uri)

        if self._is_empty(self.check_context):
            self.MissingRequiredField("check_context")
        if not isinstance(self.check_context, str):
            self.check_context = str(self.check_context)

        if self.integration_id is not None and not isinstance(self.integration_id, int):
            self.integration_id = int(self.integration_id)

        if self.strict_policy is not None and not isinstance(self.strict_policy, Bool):
            self.strict_policy = Bool(self.strict_policy)

        if self.do_not_enforce_on_create is not None and not isinstance(self.do_not_enforce_on_create, Bool):
            self.do_not_enforce_on_create = Bool(self.do_not_enforce_on_create)

        if not isinstance(self.job_path, list):
            self.job_path = [self.job_path] if self.job_path is not None else []
        self.job_path = [v if isinstance(v, GhaIdentifier) else GhaIdentifier(v) for v in self.job_path]

        if not isinstance(self.skip_conditions, list):
            self.skip_conditions = [self.skip_conditions] if self.skip_conditions is not None else []
        self.skip_conditions = [v if isinstance(v, str) else str(v) for v in self.skip_conditions]

        if self.emitted_by is not None and not isinstance(self.emitted_by, GhaWorkflowWorkflowUri):
            self.emitted_by = GhaWorkflowWorkflowUri(self.emitted_by)

        super().__post_init__(**kwargs)


# Enumerations
class GhaWorkflowInputType(EnumDefinitionImpl):
    """
    The types a reusable workflow's input may state.
    """
    boolean = PermissibleValue(
        text="boolean",
        description="True or false.")
    number = PermissibleValue(
        text="number",
        description="A number.")
    string = PermissibleValue(
        text="string",
        description="A string.")

    _defn = EnumDefinition(
        name="GhaWorkflowInputType",
        description="The types a reusable workflow's input may state.",
    )

class GhaRunnerEnvironment(EnumDefinitionImpl):
    """
    Who hosts the runner a job runs on, as GitHub's build type records it.
    """
    _defn = EnumDefinition(
        name="GhaRunnerEnvironment",
        description="Who hosts the runner a job runs on, as GitHub's build type records it.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "github-hosted",
            PermissibleValue(
                text="github-hosted",
                title="GitHub-hosted",
                description="A runner that GitHub hosts."))
        setattr(cls, "self-hosted",
            PermissibleValue(
                text="self-hosted",
                title="Self-hosted",
                description="A runner that the repository's owner hosts."))

class GhaActionRuntime(EnumDefinitionImpl):
    """
    The runtimes an action's `runs.using` may name.
    """
    composite = PermissibleValue(
        text="composite",
        description="Steps that run in the calling job, as a workflow's steps do.")
    docker = PermissibleValue(
        text="docker",
        description="A Docker container.")
    node20 = PermissibleValue(
        text="node20",
        description="JavaScript, run by Node.js 20.")
    node24 = PermissibleValue(
        text="node24",
        description="JavaScript, run by Node.js 24.")

    _defn = EnumDefinition(
        name="GhaActionRuntime",
        description="The runtimes an action's `runs.using` may name.",
    )

class GhaRulesetSourceType(EnumDefinitionImpl):
    """
    What can own a ruleset, as the REST field `source_type` names it.
    """
    Repository = PermissibleValue(
        text="Repository",
        description="A repository's own ruleset.")
    Organization = PermissibleValue(
        text="Organization",
        description="An organization's ruleset, applied to the repositories it targets.")
    Enterprise = PermissibleValue(
        text="Enterprise",
        description="An enterprise's ruleset, applied to the repositories it targets.")

    _defn = EnumDefinition(
        name="GhaRulesetSourceType",
        description="What can own a ruleset, as the REST field `source_type` names it.",
    )

class GhaRulesetTarget(EnumDefinitionImpl):
    """
    What a ruleset applies to, as the REST field `target` names it.
    """
    branch = PermissibleValue(
        text="branch",
        description="Branches; GitHub's default.")
    tag = PermissibleValue(
        text="tag",
        description="Tags.")
    push = PermissibleValue(
        text="push",
        description="Pushes, by the files they change.")

    _defn = EnumDefinition(
        name="GhaRulesetTarget",
        description="What a ruleset applies to, as the REST field `target` names it.",
    )

class GhaRulesetEnforcement(EnumDefinitionImpl):
    """
    Whether GitHub enforces a ruleset, as the REST field `enforcement` names it.
    """
    active = PermissibleValue(
        text="active",
        description="Enforced.")
    evaluate = PermissibleValue(
        text="evaluate",
        description="""Evaluated and reported but not enforced, so administrators can test its rules; only on GitHub Enterprise.""")
    disabled = PermissibleValue(
        text="disabled",
        description="Neither enforced nor evaluated.")

    _defn = EnumDefinition(
        name="GhaRulesetEnforcement",
        description="Whether GitHub enforces a ruleset, as the REST field `enforcement` names it.",
    )

# Slots
class slots:
    pass

slots.description = Slot(uri=SCHEMA.description, name="description", curie=SCHEMA.curie('description'),
                   model_uri=GHA.description, domain=None, range=Optional[str])

slots.inputs = Slot(uri=GHA.inputs, name="inputs", curie=GHA.curie('inputs'),
                   model_uri=GHA.inputs, domain=None, range=Optional[Union[Union[dict, GhaInput], list[Union[dict, GhaInput]]]])

slots.outputs = Slot(uri=GHA.outputs, name="outputs", curie=GHA.curie('outputs'),
                   model_uri=GHA.outputs, domain=None, range=Optional[Union[Union[dict, GhaOutput], list[Union[dict, GhaOutput]]]])

slots.output_expression = Slot(uri=GHA.output_expression, name="output_expression", curie=GHA.curie('output_expression'),
                   model_uri=GHA.output_expression, domain=None, range=Optional[str])

slots.triggers = Slot(uri=GHA.triggers, name="triggers", curie=GHA.curie('triggers'),
                   model_uri=GHA.triggers, domain=None, range=Optional[Union[str, list[str]]],
                   pattern=re.compile(r'^[a-z_]+$'))

slots.ghaDocument__workflows = Slot(uri=GHA.workflows, name="ghaDocument__workflows", curie=GHA.curie('workflows'),
                   model_uri=GHA.ghaDocument__workflows, domain=None, range=Optional[Union[dict[Union[str, GhaWorkflowWorkflowUri], Union[dict, GhaWorkflow]], list[Union[dict, GhaWorkflow]]]])

slots.ghaDocument__reusable_workflows = Slot(uri=GHA.reusable_workflows, name="ghaDocument__reusable_workflows", curie=GHA.curie('reusable_workflows'),
                   model_uri=GHA.ghaDocument__reusable_workflows, domain=None, range=Optional[Union[dict[Union[str, GhaReusableWorkflowWorkflowUri], Union[dict, GhaReusableWorkflow]], list[Union[dict, GhaReusableWorkflow]]]])

slots.ghaDocument__actions = Slot(uri=GHA.actions, name="ghaDocument__actions", curie=GHA.curie('actions'),
                   model_uri=GHA.ghaDocument__actions, domain=None, range=Optional[Union[dict[Union[str, GhaActionActionUri], Union[dict, GhaAction]], list[Union[dict, GhaAction]]]])

slots.ghaDocument__rulesets = Slot(uri=GHA.rulesets, name="ghaDocument__rulesets", curie=GHA.curie('rulesets'),
                   model_uri=GHA.ghaDocument__rulesets, domain=None, range=Optional[Union[dict[Union[str, GhaRepositoryRulesetRulesetUri], Union[dict, GhaRepositoryRuleset]], list[Union[dict, GhaRepositoryRuleset]]]])

slots.ghaDocument__required_checks = Slot(uri=GHA.required_checks, name="ghaDocument__required_checks", curie=GHA.curie('required_checks'),
                   model_uri=GHA.ghaDocument__required_checks, domain=None, range=Optional[Union[dict[Union[str, GhaRequiredStatusCheckCheckUri], Union[dict, GhaRequiredStatusCheck]], list[Union[dict, GhaRequiredStatusCheck]]]])

slots.ghaRequiredMixin__required = Slot(uri=SCHEMA.valueRequired, name="ghaRequiredMixin__required", curie=SCHEMA.curie('valueRequired'),
                   model_uri=GHA.ghaRequiredMixin__required, domain=None, range=Optional[Union[bool, Bool]])

slots.ghaInput__input_id = Slot(uri=GHA.input_id, name="ghaInput__input_id", curie=GHA.curie('input_id'),
                   model_uri=GHA.ghaInput__input_id, domain=None, range=Union[str, GhaIdentifier])

slots.ghaInput__default = Slot(uri=GHA.default, name="ghaInput__default", curie=GHA.curie('default'),
                   model_uri=GHA.ghaInput__default, domain=None, range=Optional[str])

slots.ghaOutput__output_id = Slot(uri=GHA.output_id, name="ghaOutput__output_id", curie=GHA.curie('output_id'),
                   model_uri=GHA.ghaOutput__output_id, domain=None, range=Union[str, GhaIdentifier])

slots.ghaWorkflow__workflow_uri = Slot(uri=GHA.workflow_uri, name="ghaWorkflow__workflow_uri", curie=GHA.curie('workflow_uri'),
                   model_uri=GHA.ghaWorkflow__workflow_uri, domain=None, range=URIRef)

slots.ghaWorkflow__workflow_path = Slot(uri=GHA.workflow_path, name="ghaWorkflow__workflow_path", curie=GHA.curie('workflow_path'),
                   model_uri=GHA.ghaWorkflow__workflow_path, domain=None, range=str,
                   pattern=re.compile(r'^\.github/workflows/[^/]+\.ya?ml$'))

slots.ghaWorkflow__workflow_repository = Slot(uri=GHA.workflow_repository, name="ghaWorkflow__workflow_repository", curie=GHA.curie('workflow_repository'),
                   model_uri=GHA.ghaWorkflow__workflow_repository, domain=None, range=Optional[Union[str, URI]],
                   pattern=re.compile(r'^https://[^/]+/[^/]+/[^/]+$'))

slots.ghaWorkflow__permissions = Slot(uri=GHA.permissions, name="ghaWorkflow__permissions", curie=GHA.curie('permissions'),
                   model_uri=GHA.ghaWorkflow__permissions, domain=None, range=Optional[Union[Union[str, GhaPermission], list[Union[str, GhaPermission]]]])

slots.ghaWorkflow__jobs = Slot(uri=GHA.jobs, name="ghaWorkflow__jobs", curie=GHA.curie('jobs'),
                   model_uri=GHA.ghaWorkflow__jobs, domain=None, range=Union[Union[dict, GhaWorkflowJob], list[Union[dict, GhaWorkflowJob]]])

slots.ghaReusableWorkflow__secrets = Slot(uri=GHA.secrets, name="ghaReusableWorkflow__secrets", curie=GHA.curie('secrets'),
                   model_uri=GHA.ghaReusableWorkflow__secrets, domain=None, range=Optional[Union[Union[dict, GhaWorkflowSecret], list[Union[dict, GhaWorkflowSecret]]]])

slots.ghaWorkflowJob__job_id = Slot(uri=GHA.job_id, name="ghaWorkflowJob__job_id", curie=GHA.curie('job_id'),
                   model_uri=GHA.ghaWorkflowJob__job_id, domain=None, range=Union[str, GhaIdentifier])

slots.ghaWorkflowJob__job_name = Slot(uri=GHA.job_name, name="ghaWorkflowJob__job_name", curie=GHA.curie('job_name'),
                   model_uri=GHA.ghaWorkflowJob__job_name, domain=None, range=Optional[str])

slots.ghaWorkflowJob__calls = Slot(uri=GHA.calls, name="ghaWorkflowJob__calls", curie=GHA.curie('calls'),
                   model_uri=GHA.ghaWorkflowJob__calls, domain=None, range=Optional[str],
                   pattern=re.compile(r'^(.+\/)+(.+)\.(ya?ml)(@.+)?$'))

slots.ghaWorkflowJob__runs_on = Slot(uri=GHA.runs_on, name="ghaWorkflowJob__runs_on", curie=GHA.curie('runs_on'),
                   model_uri=GHA.ghaWorkflowJob__runs_on, domain=None, range=Optional[Union[str, list[str]]])

slots.ghaWorkflowJob__runner_group = Slot(uri=GHA.runner_group, name="ghaWorkflowJob__runner_group", curie=GHA.curie('runner_group'),
                   model_uri=GHA.ghaWorkflowJob__runner_group, domain=None, range=Optional[str])

slots.ghaWorkflowJob__runner_environment = Slot(uri=GHA.runner_environment, name="ghaWorkflowJob__runner_environment", curie=GHA.curie('runner_environment'),
                   model_uri=GHA.ghaWorkflowJob__runner_environment, domain=None, range=Optional[Union[str, "GhaRunnerEnvironment"]])

slots.ghaWorkflowJob__job_permissions = Slot(uri=GHA.job_permissions, name="ghaWorkflowJob__job_permissions", curie=GHA.curie('job_permissions'),
                   model_uri=GHA.ghaWorkflowJob__job_permissions, domain=None, range=Optional[Union[Union[str, GhaPermission], list[Union[str, GhaPermission]]]])

slots.ghaWorkflowInput__input_type = Slot(uri=GHA.input_type, name="ghaWorkflowInput__input_type", curie=GHA.curie('input_type'),
                   model_uri=GHA.ghaWorkflowInput__input_type, domain=None, range=Union[str, "GhaWorkflowInputType"])

slots.ghaWorkflowSecret__secret_id = Slot(uri=GHA.secret_id, name="ghaWorkflowSecret__secret_id", curie=GHA.curie('secret_id'),
                   model_uri=GHA.ghaWorkflowSecret__secret_id, domain=None, range=Union[str, GhaIdentifier])

slots.ghaAction__action_uri = Slot(uri=GHA.action_uri, name="ghaAction__action_uri", curie=GHA.curie('action_uri'),
                   model_uri=GHA.ghaAction__action_uri, domain=None, range=URIRef)

slots.ghaAction__action_path = Slot(uri=GHA.action_path, name="ghaAction__action_path", curie=GHA.curie('action_path'),
                   model_uri=GHA.ghaAction__action_path, domain=None, range=str,
                   pattern=re.compile(r'^(.+/)?action\.ya?ml$'))

slots.ghaAction__using = Slot(uri=GHA.using, name="ghaAction__using", curie=GHA.curie('using'),
                   model_uri=GHA.ghaAction__using, domain=None, range=Union[str, "GhaActionRuntime"])

slots.ghaActionInput__deprecation_message = Slot(uri=GHA.deprecation_message, name="ghaActionInput__deprecation_message", curie=GHA.curie('deprecation_message'),
                   model_uri=GHA.ghaActionInput__deprecation_message, domain=None, range=Optional[str])

slots.ghaRepositoryRuleset__ruleset_uri = Slot(uri=GHA.ruleset_uri, name="ghaRepositoryRuleset__ruleset_uri", curie=GHA.curie('ruleset_uri'),
                   model_uri=GHA.ghaRepositoryRuleset__ruleset_uri, domain=None, range=URIRef)

slots.ghaRepositoryRuleset__ruleset_id = Slot(uri=GHA.ruleset_id, name="ghaRepositoryRuleset__ruleset_id", curie=GHA.curie('ruleset_id'),
                   model_uri=GHA.ghaRepositoryRuleset__ruleset_id, domain=None, range=Optional[int])

slots.ghaRepositoryRuleset__ruleset_source_type = Slot(uri=GHA.ruleset_source_type, name="ghaRepositoryRuleset__ruleset_source_type", curie=GHA.curie('ruleset_source_type'),
                   model_uri=GHA.ghaRepositoryRuleset__ruleset_source_type, domain=None, range=Optional[Union[str, "GhaRulesetSourceType"]])

slots.ghaRepositoryRuleset__ruleset_source = Slot(uri=GHA.ruleset_source, name="ghaRepositoryRuleset__ruleset_source", curie=GHA.curie('ruleset_source'),
                   model_uri=GHA.ghaRepositoryRuleset__ruleset_source, domain=None, range=Optional[str])

slots.ghaRepositoryRuleset__ruleset_target = Slot(uri=GHA.ruleset_target, name="ghaRepositoryRuleset__ruleset_target", curie=GHA.curie('ruleset_target'),
                   model_uri=GHA.ghaRepositoryRuleset__ruleset_target, domain=None, range=Union[str, "GhaRulesetTarget"])

slots.ghaRepositoryRuleset__enforcement = Slot(uri=GHA.enforcement, name="ghaRepositoryRuleset__enforcement", curie=GHA.curie('enforcement'),
                   model_uri=GHA.ghaRepositoryRuleset__enforcement, domain=None, range=Union[str, "GhaRulesetEnforcement"])

slots.ghaRepositoryRuleset__ref_name_include = Slot(uri=GHA.ref_name_include, name="ghaRepositoryRuleset__ref_name_include", curie=GHA.curie('ref_name_include'),
                   model_uri=GHA.ghaRepositoryRuleset__ref_name_include, domain=None, range=Optional[Union[str, list[str]]])

slots.ghaRepositoryRuleset__ref_name_exclude = Slot(uri=GHA.ref_name_exclude, name="ghaRepositoryRuleset__ref_name_exclude", curie=GHA.curie('ref_name_exclude'),
                   model_uri=GHA.ghaRepositoryRuleset__ref_name_exclude, domain=None, range=Optional[Union[str, list[str]]])

slots.ghaRepositoryRuleset__bypass_actors = Slot(uri=GHA.bypass_actors, name="ghaRepositoryRuleset__bypass_actors", curie=GHA.curie('bypass_actors'),
                   model_uri=GHA.ghaRepositoryRuleset__bypass_actors, domain=None, range=Optional[Union[Union[dict, GhaBypassActor], list[Union[dict, GhaBypassActor]]]])

slots.ghaRepositoryRuleset__rule_types = Slot(uri=GHA.rule_types, name="ghaRepositoryRuleset__rule_types", curie=GHA.curie('rule_types'),
                   model_uri=GHA.ghaRepositoryRuleset__rule_types, domain=None, range=Optional[Union[str, list[str]]],
                   pattern=re.compile(r'^[a-z_]+$'))

slots.ghaRepositoryRuleset__requires_check = Slot(uri=GHA.requires_check, name="ghaRepositoryRuleset__requires_check", curie=GHA.curie('requires_check'),
                   model_uri=GHA.ghaRepositoryRuleset__requires_check, domain=None, range=Optional[Union[Union[str, GhaRequiredStatusCheckCheckUri], list[Union[str, GhaRequiredStatusCheckCheckUri]]]])

slots.ghaBypassActor__actor_id = Slot(uri=GHA.actor_id, name="ghaBypassActor__actor_id", curie=GHA.curie('actor_id'),
                   model_uri=GHA.ghaBypassActor__actor_id, domain=None, range=Optional[int])

slots.ghaBypassActor__actor_type = Slot(uri=GHA.actor_type, name="ghaBypassActor__actor_type", curie=GHA.curie('actor_type'),
                   model_uri=GHA.ghaBypassActor__actor_type, domain=None, range=str,
                   pattern=re.compile(r'^[A-Z][A-Za-z]+$'))

slots.ghaBypassActor__bypass_mode = Slot(uri=GHA.bypass_mode, name="ghaBypassActor__bypass_mode", curie=GHA.curie('bypass_mode'),
                   model_uri=GHA.ghaBypassActor__bypass_mode, domain=None, range=Optional[str],
                   pattern=re.compile(r'^[a-z_]+$'))

slots.ghaRequiredStatusCheck__check_uri = Slot(uri=GHA.check_uri, name="ghaRequiredStatusCheck__check_uri", curie=GHA.curie('check_uri'),
                   model_uri=GHA.ghaRequiredStatusCheck__check_uri, domain=None, range=URIRef)

slots.ghaRequiredStatusCheck__check_context = Slot(uri=GHA.check_context, name="ghaRequiredStatusCheck__check_context", curie=GHA.curie('check_context'),
                   model_uri=GHA.ghaRequiredStatusCheck__check_context, domain=None, range=str,
                   pattern=re.compile(r'\S'))

slots.ghaRequiredStatusCheck__integration_id = Slot(uri=GHA.integration_id, name="ghaRequiredStatusCheck__integration_id", curie=GHA.curie('integration_id'),
                   model_uri=GHA.ghaRequiredStatusCheck__integration_id, domain=None, range=Optional[int])

slots.ghaRequiredStatusCheck__strict_policy = Slot(uri=GHA.strict_policy, name="ghaRequiredStatusCheck__strict_policy", curie=GHA.curie('strict_policy'),
                   model_uri=GHA.ghaRequiredStatusCheck__strict_policy, domain=None, range=Optional[Union[bool, Bool]])

slots.ghaRequiredStatusCheck__do_not_enforce_on_create = Slot(uri=GHA.do_not_enforce_on_create, name="ghaRequiredStatusCheck__do_not_enforce_on_create", curie=GHA.curie('do_not_enforce_on_create'),
                   model_uri=GHA.ghaRequiredStatusCheck__do_not_enforce_on_create, domain=None, range=Optional[Union[bool, Bool]])

slots.ghaRequiredStatusCheck__job_path = Slot(uri=GHA.job_path, name="ghaRequiredStatusCheck__job_path", curie=GHA.curie('job_path'),
                   model_uri=GHA.ghaRequiredStatusCheck__job_path, domain=None, range=Optional[Union[Union[str, GhaIdentifier], list[Union[str, GhaIdentifier]]]])

slots.ghaRequiredStatusCheck__skip_conditions = Slot(uri=GHA.skip_conditions, name="ghaRequiredStatusCheck__skip_conditions", curie=GHA.curie('skip_conditions'),
                   model_uri=GHA.ghaRequiredStatusCheck__skip_conditions, domain=None, range=Optional[Union[str, list[str]]],
                   pattern=re.compile(r'^(on|jobs)\.\S+$'))

slots.ghaRequiredStatusCheck__emitted_by = Slot(uri=GHA.emitted_by, name="ghaRequiredStatusCheck__emitted_by", curie=GHA.curie('emitted_by'),
                   model_uri=GHA.ghaRequiredStatusCheck__emitted_by, domain=None, range=Optional[Union[str, GhaWorkflowWorkflowUri]])

slots.GhaWorkflow_triggers = Slot(uri=GHA.triggers, name="GhaWorkflow_triggers", curie=GHA.curie('triggers'),
                   model_uri=GHA.GhaWorkflow_triggers, domain=GhaWorkflow, range=Union[str, list[str]],
                   pattern=re.compile(r'^[a-z_]+$'))

slots.GhaReusableWorkflow_triggers = Slot(uri=GHA.triggers, name="GhaReusableWorkflow_triggers", curie=GHA.curie('triggers'),
                   model_uri=GHA.GhaReusableWorkflow_triggers, domain=GhaReusableWorkflow, range=Union[str, list[str]],
                   pattern=re.compile(r'^[a-z_]+$'))

slots.GhaReusableWorkflow_inputs = Slot(uri=GHA.inputs, name="GhaReusableWorkflow_inputs", curie=GHA.curie('inputs'),
                   model_uri=GHA.GhaReusableWorkflow_inputs, domain=GhaReusableWorkflow, range=Optional[Union[Union[dict, "GhaWorkflowInput"], list[Union[dict, "GhaWorkflowInput"]]]])

slots.GhaReusableWorkflow_outputs = Slot(uri=GHA.outputs, name="GhaReusableWorkflow_outputs", curie=GHA.curie('outputs'),
                   model_uri=GHA.GhaReusableWorkflow_outputs, domain=GhaReusableWorkflow, range=Optional[Union[Union[dict, "GhaWorkflowOutput"], list[Union[dict, "GhaWorkflowOutput"]]]])

slots.GhaWorkflowOutput_output_expression = Slot(uri=GHA.output_expression, name="GhaWorkflowOutput_output_expression", curie=GHA.curie('output_expression'),
                   model_uri=GHA.GhaWorkflowOutput_output_expression, domain=GhaWorkflowOutput, range=str)

slots.GhaAction_inputs = Slot(uri=GHA.inputs, name="GhaAction_inputs", curie=GHA.curie('inputs'),
                   model_uri=GHA.GhaAction_inputs, domain=GhaAction, range=Optional[Union[Union[dict, "GhaActionInput"], list[Union[dict, "GhaActionInput"]]]])

slots.GhaAction_outputs = Slot(uri=GHA.outputs, name="GhaAction_outputs", curie=GHA.curie('outputs'),
                   model_uri=GHA.GhaAction_outputs, domain=GhaAction, range=Optional[Union[Union[dict, "GhaActionOutput"], list[Union[dict, "GhaActionOutput"]]]])

slots.GhaActionInput_description = Slot(uri=SCHEMA.description, name="GhaActionInput_description", curie=SCHEMA.curie('description'),
                   model_uri=GHA.GhaActionInput_description, domain=GhaActionInput, range=str)

slots.GhaActionOutput_description = Slot(uri=SCHEMA.description, name="GhaActionOutput_description", curie=SCHEMA.curie('description'),
                   model_uri=GHA.GhaActionOutput_description, domain=GhaActionOutput, range=str)
