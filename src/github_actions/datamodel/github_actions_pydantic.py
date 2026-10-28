from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.12.0"
version = "2026-10-28"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'annotations': {'docs_read': {'tag': 'docs_read', 'value': '2026-10-28'},
                     'rest_api_version': {'tag': 'rest_api_version',
                                          'value': '2026-03-10'},
                     'schemastore_commit': {'tag': 'schemastore_commit',
                                            'value': 'f7c2f3bcb512651bd980ed6896639ea8ded9ddf0'}},
     'comments': ["GitHub's documentation is versionless, so the version is the "
                  'date its pages were read. With the SchemaStore commit in source '
                  'and the REST API version in the annotations, it says which '
                  'state of GitHub the model renders; '
                  'scripts/check_upstream_release.py reads the same three pins and '
                  "reports when one moves. The release tags are the schema's own "
                  'versions.',
                  'github_actions_core imports only the LinkML types, the workflow '
                  'and action modules import the core, the rules module imports '
                  'the workflow module, and this file adds only the document root, '
                  'so an importer can take one module.'],
     'default_prefix': 'gha',
     'default_range': 'string',
     'description': 'A LinkML model of what GitHub Actions files and repository '
                    'rulesets state: workflows and their jobs, reusable workflows '
                    'with their inputs, outputs and secrets, actions with their '
                    'runtimes, and the rulesets and required status checks that '
                    "tie a workflow's jobs to the refs a ruleset protects.",
     'id': 'https://w3id.org/lmodel/github-actions',
     'imports': ['linkml:types',
                 './github_actions_core',
                 './github_actions_workflow',
                 './github_actions_action',
                 './github_actions_rules'],
     'license': 'Apache-2.0',
     'name': 'github_actions',
     'prefixes': {'gha': {'prefix_prefix': 'gha',
                          'prefix_reference': 'https://w3id.org/lmodel/github-actions/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'}},
     'see_also': ['https://lmodel.github.io/github-actions',
                  'https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax',
                  'https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax',
                  'https://docs.github.com/en/rest/repos/rules',
                  'https://docs.github.com/en/rest/checks/runs',
                  'https://actions.github.io/buildtypes/workflow/v1'],
     'source': 'https://github.com/SchemaStore/schemastore/tree/f7c2f3bcb512651bd980ed6896639ea8ded9ddf0/src/schemas/json',
     'source_file': 'src/github_actions/schema/github_actions.yaml',
     'title': 'GitHub Actions workflows, actions and repository rulesets'} )

class GhaWorkflowInputType(str, Enum):
    """
    The types a reusable workflow's input may state.
    """
    boolean = "boolean"
    """
    True or false.
    """
    number = "number"
    """
    A number.
    """
    string = "string"
    """
    A string.
    """


class GhaRunnerEnvironment(str, Enum):
    """
    Who hosts the runner a job runs on, as GitHub's build type records it.
    """
    GitHub_hosted = "github-hosted"
    """
    A runner that GitHub hosts.
    """
    Self_hosted = "self-hosted"
    """
    A runner that the repository's owner hosts.
    """


class GhaActionRuntime(str, Enum):
    """
    The runtimes an action's `runs.using` may name.
    """
    composite = "composite"
    """
    Steps that run in the calling job, as a workflow's steps do.
    """
    docker = "docker"
    """
    A Docker container.
    """
    node20 = "node20"
    """
    JavaScript, run by Node.js 20.
    """
    node24 = "node24"
    """
    JavaScript, run by Node.js 24.
    """


class GhaRulesetSourceType(str, Enum):
    """
    What can own a ruleset, as the REST field `source_type` names it.
    """
    Repository = "Repository"
    """
    A repository's own ruleset.
    """
    Organization = "Organization"
    """
    An organization's ruleset, applied to the repositories it targets.
    """
    Enterprise = "Enterprise"
    """
    An enterprise's ruleset, applied to the repositories it targets.
    """


class GhaRulesetTarget(str, Enum):
    """
    What a ruleset applies to, as the REST field `target` names it.
    """
    branch = "branch"
    """
    Branches; GitHub's default.
    """
    tag = "tag"
    """
    Tags.
    """
    push = "push"
    """
    Pushes, by the files they change.
    """


class GhaRulesetEnforcement(str, Enum):
    """
    Whether GitHub enforces a ruleset, as the REST field `enforcement` names it.
    """
    active = "active"
    """
    Enforced.
    """
    evaluate = "evaluate"
    """
    Evaluated and reported but not enforced, so administrators can test its rules; only on GitHub Enterprise.
    """
    disabled = "disabled"
    """
    Neither enforced nor evaluated.
    """



class GhaRequiredMixin(ConfiguredBaseModel):
    """
    The field that says whether a caller must supply a value.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/lmodel/github-actions/github_actions_core',
         'mixin': True})

    required: Optional[bool] = Field(default=None, description="""Whether a caller must supply a value.""", json_schema_extra = { "linkml_meta": {'comments': ["An attribute rather than a slot: it carries LOKF's IRI for "
                      "required, and lokf adapt keeps an attribute's name, where it "
                      'would rename a slot that shares one with lokf.yaml.'],
         'domain_of': ['GhaRequiredMixin'],
         'slot_uri': 'schema:valueRequired'} })


class GhaInput(GhaRequiredMixin):
    """
    An input that a reusable workflow or an action declares, under the key a caller writes in its `with` map.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'gha:Input',
         'from_schema': 'https://w3id.org/lmodel/github-actions/github_actions_core',
         'mixins': ['GhaRequiredMixin']})

    description: Optional[str] = Field(default=None, description="""What the input, output or secret is for, as the file describes it.""", json_schema_extra = { "linkml_meta": {'comments': ["It means what LOKF's description means and carries the same "
                      "IRI, so lokf adapt folds it into LOKF's slot and a knowledge "
                      'bundle reads one description key.'],
         'domain_of': ['GhaInput', 'GhaOutput', 'GhaWorkflowSecret'],
         'slot_uri': 'schema:description'} })
    input_id: str = Field(default=..., description="""The key a caller writes in its `with` map.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaInput']} })
    default: Optional[str] = Field(default=None, description="""The value used when a caller supplies none, written as a string even where the input's type is a boolean or a number.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaInput']} })
    required: Optional[bool] = Field(default=None, description="""Whether a caller must supply a value.""", json_schema_extra = { "linkml_meta": {'comments': ["An attribute rather than a slot: it carries LOKF's IRI for "
                      "required, and lokf adapt keeps an attribute's name, where it "
                      'would rename a slot that shares one with lokf.yaml.'],
         'domain_of': ['GhaRequiredMixin'],
         'slot_uri': 'schema:valueRequired'} })


class GhaOutput(ConfiguredBaseModel):
    """
    An output that a reusable workflow or an action declares for the job or step that calls it to read.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'gha:Output',
         'from_schema': 'https://w3id.org/lmodel/github-actions/github_actions_core'})

    description: Optional[str] = Field(default=None, description="""What the input, output or secret is for, as the file describes it.""", json_schema_extra = { "linkml_meta": {'comments': ["It means what LOKF's description means and carries the same "
                      "IRI, so lokf adapt folds it into LOKF's slot and a knowledge "
                      'bundle reads one description key.'],
         'domain_of': ['GhaInput', 'GhaOutput', 'GhaWorkflowSecret'],
         'slot_uri': 'schema:description'} })
    output_expression: Optional[str] = Field(default=None, description="""The expression that sets the output, the file's `value` key, such as one that reads an output of a job or a step.""", json_schema_extra = { "linkml_meta": {'comments': ['A slot rather than an attribute because GhaWorkflowOutput '
                      'refines it.'],
         'domain_of': ['GhaOutput'],
         'slot_uri': 'gha:output_expression'} })
    output_id: str = Field(default=..., description="""The key a caller reads the output by.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaOutput']} })


class GhaWorkflow(ConfiguredBaseModel):
    """
    A workflow file in a repository's `.github/workflows` directory: the events that run it, the access its GITHUB_TOKEN gets, and its jobs.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'gha:Workflow',
         'close_mappings': ['cdx:workflow'],
         'comments': ["SPDX 3.0.1's Build records one run of a build, such as a run of "
                      'this workflow, so it is a related term and not a close one.',
                      'The ref a run checks the file out at belongs to the run, and '
                      "GitHub's build type records it in provenance as workflow.ref; "
                      'it is not a fact of the file, so it is not modelled here.'],
         'from_schema': 'https://w3id.org/lmodel/github-actions/github_actions_workflow',
         'related_mappings': ['spdx_build:Build'],
         'see_also': ['https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax'],
         'slot_usage': {'triggers': {'name': 'triggers', 'required': True}}})

    triggers: list[str] = Field(default=..., description="""The names of the events under the file's `on` key, such as `push`, `pull_request`, `schedule` or `workflow_call`.""", json_schema_extra = { "linkml_meta": {'comments': ['A slot rather than an attribute because GhaReusableWorkflow '
                      'refines it; a pattern rather than an enumeration, because '
                      'GitHub adds events.'],
         'domain_of': ['GhaWorkflow'],
         'related_mappings': ['cdx:trigger'],
         'see_also': ['https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows'],
         'slot_uri': 'gha:triggers'} })
    workflow_uri: str = Field(default=..., description="""The file's address on its forge without a ref: `https://github.com/<owner>/<repo>/.github/workflows/<file>`.""", json_schema_extra = { "linkml_meta": {'comments': ["GitHub's build type forms a reusable workflow's builder.id from "
                      'this address, followed by `@` and the ref.'],
         'domain_of': ['GhaWorkflow']} })
    workflow_path: str = Field(default=..., description="""The file's path from the repository root, as GitHub's build type writes workflow.path. GitHub reads no subdirectory of `.github/workflows`.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaWorkflow'],
         'see_also': ['https://actions.github.io/buildtypes/workflow/v1']} })
    workflow_repository: Optional[str] = Field(default=None, description="""The repository that holds the file, as GitHub's build type writes workflow.repository: an HTTPS address without `.git`.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaWorkflow'],
         'see_also': ['https://actions.github.io/buildtypes/workflow/v1']} })
    permissions: Optional[list[str]] = Field(default=None, description="""The access the file's top-level `permissions` key gives every job's GITHUB_TOKEN. Absent when the file sets none, so the repository's or organization's default applies; a scope the map leaves out gets no access.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaWorkflow']} })
    jobs: list[GhaWorkflowJob] = Field(default=..., description="""The jobs under the file's `jobs` key.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaWorkflow']} })

    @field_validator('triggers')
    def pattern_triggers(cls, v):
        pattern=re.compile(r"^[a-z_]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid triggers format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid triggers format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('workflow_path')
    def pattern_workflow_path(cls, v):
        pattern=re.compile(r"^\.github/workflows/[^/]+\.ya?ml$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid workflow_path format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid workflow_path format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('workflow_repository')
    def pattern_workflow_repository(cls, v):
        pattern=re.compile(r"^https://[^/]+/[^/]+/[^/]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid workflow_repository format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid workflow_repository format: {v}"
            raise ValueError(err_msg)
        return v


class GhaReusableWorkflow(GhaWorkflow):
    """
    A workflow that other workflows call as a job, because its `on` key names `workflow_call`; it declares the inputs, outputs and secrets its callers pass and read.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'gha:ReusableWorkflow',
         'comments': ["When it generates provenance it is the builder: GitHub's build "
                      "type sets builder.id to the server's address followed by the "
                      "job's workflow reference, which names this file and its ref."],
         'from_schema': 'https://w3id.org/lmodel/github-actions/github_actions_workflow',
         'see_also': ['https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations',
                      'https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onworkflow_call'],
         'slot_usage': {'inputs': {'description': "The inputs under the file's "
                                                  '`on.workflow_call.inputs` key.',
                                   'name': 'inputs',
                                   'range': 'GhaWorkflowInput'},
                        'outputs': {'description': "The outputs under the file's "
                                                   '`on.workflow_call.outputs` key.',
                                    'name': 'outputs',
                                    'range': 'GhaWorkflowOutput'},
                        'triggers': {'has_member': {'equals_string': 'workflow_call'},
                                     'name': 'triggers'}}})

    inputs: Optional[list[GhaWorkflowInput]] = Field(default=None, description="""The inputs under the file's `on.workflow_call.inputs` key.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaReusableWorkflow', 'GhaAction']} })
    outputs: Optional[list[GhaWorkflowOutput]] = Field(default=None, description="""The outputs under the file's `on.workflow_call.outputs` key.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaReusableWorkflow', 'GhaAction']} })
    secrets: Optional[list[GhaWorkflowSecret]] = Field(default=None, description="""The secrets under the file's `on.workflow_call.secrets` key, by name only; no value is ever recorded.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaReusableWorkflow']} })
    triggers: list[str] = Field(default=..., description="""The names of the events under the file's `on` key, such as `push`, `pull_request`, `schedule` or `workflow_call`.""", json_schema_extra = { "linkml_meta": {'comments': ['A slot rather than an attribute because GhaReusableWorkflow '
                      'refines it; a pattern rather than an enumeration, because '
                      'GitHub adds events.'],
         'domain_of': ['GhaWorkflow'],
         'has_member': {'equals_string': 'workflow_call'},
         'related_mappings': ['cdx:trigger'],
         'see_also': ['https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows'],
         'slot_uri': 'gha:triggers'} })
    workflow_uri: str = Field(default=..., description="""The file's address on its forge without a ref: `https://github.com/<owner>/<repo>/.github/workflows/<file>`.""", json_schema_extra = { "linkml_meta": {'comments': ["GitHub's build type forms a reusable workflow's builder.id from "
                      'this address, followed by `@` and the ref.'],
         'domain_of': ['GhaWorkflow']} })
    workflow_path: str = Field(default=..., description="""The file's path from the repository root, as GitHub's build type writes workflow.path. GitHub reads no subdirectory of `.github/workflows`.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaWorkflow'],
         'see_also': ['https://actions.github.io/buildtypes/workflow/v1']} })
    workflow_repository: Optional[str] = Field(default=None, description="""The repository that holds the file, as GitHub's build type writes workflow.repository: an HTTPS address without `.git`.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaWorkflow'],
         'see_also': ['https://actions.github.io/buildtypes/workflow/v1']} })
    permissions: Optional[list[str]] = Field(default=None, description="""The access the file's top-level `permissions` key gives every job's GITHUB_TOKEN. Absent when the file sets none, so the repository's or organization's default applies; a scope the map leaves out gets no access.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaWorkflow']} })
    jobs: list[GhaWorkflowJob] = Field(default=..., description="""The jobs under the file's `jobs` key.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaWorkflow']} })

    @field_validator('triggers')
    def pattern_triggers(cls, v):
        pattern=re.compile(r"^[a-z_]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid triggers format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid triggers format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('workflow_path')
    def pattern_workflow_path(cls, v):
        pattern=re.compile(r"^\.github/workflows/[^/]+\.ya?ml$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid workflow_path format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid workflow_path format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('workflow_repository')
    def pattern_workflow_repository(cls, v):
        pattern=re.compile(r"^https://[^/]+/[^/]+/[^/]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid workflow_repository format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid workflow_repository format: {v}"
            raise ValueError(err_msg)
        return v


class GhaWorkflowJob(ConfiguredBaseModel):
    """
    A job under a workflow's `jobs` key: steps that run on a runner, or a call to a reusable workflow.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'gha:WorkflowJob',
         'from_schema': 'https://w3id.org/lmodel/github-actions/github_actions_workflow',
         'rules': [{'description': 'A job that calls a reusable workflow names no '
                                   'runner labels: a calling job takes no `runs-on` '
                                   "key, and the called workflow's jobs choose their "
                                   'own runners.',
                    'postconditions': {'slot_conditions': {'runs_on': {'name': 'runs_on',
                                                                       'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'calls': {'name': 'calls',
                                                                    'value_presence': 'PRESENT'}}}},
                   {'description': 'A job that calls a reusable workflow names no '
                                   'runner group.',
                    'postconditions': {'slot_conditions': {'runner_group': {'name': 'runner_group',
                                                                            'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'calls': {'name': 'calls',
                                                                    'value_presence': 'PRESENT'}}}}],
         'see_also': ['https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobs']})

    job_id: str = Field(default=..., description="""The job's key under `jobs`.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaWorkflowJob']} })
    job_name: Optional[str] = Field(default=None, description="""The job's `name`, which GitHub shows and its check run takes; the check run takes the job's id when it has none.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaWorkflowJob'],
         'see_also': ['https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idname']} })
    calls: Optional[str] = Field(default=None, description="""The reusable workflow the job runs, its `uses` value: `./.github/workflows/<file>` in the same repository, or `<owner>/<repo>/.github/workflows/<file>@<ref>`.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaWorkflowJob'],
         'see_also': ['https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_iduses']} })
    runs_on: Optional[list[str]] = Field(default=None, description="""The runner labels from the job's `runs-on`: one label, a list, or the `labels` of a group. A runner must carry every one.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaWorkflowJob'],
         'see_also': ['https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idruns-on']} })
    runner_group: Optional[str] = Field(default=None, description="""The runner group the job's `runs-on.group` names.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaWorkflowJob'],
         'see_also': ['https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#choosing-runners-in-a-group']} })
    runner_environment: Optional[GhaRunnerEnvironment] = Field(default=None, description="""Whether the job's runner is hosted by GitHub or by the repository's owner, as GitHub's build type records runner_environment for a run.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaWorkflowJob']} })
    job_permissions: Optional[list[str]] = Field(default=None, description="""The access the job's own `permissions` key gives its GITHUB_TOKEN, in place of the workflow's. A called workflow can lower its token's access, never raise it.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaWorkflowJob'],
         'see_also': ['https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idpermissions']} })

    @field_validator('calls')
    def pattern_calls(cls, v):
        pattern=re.compile(r"^(.+\/)+(.+)\.(ya?ml)(@.+)?$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid calls format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid calls format: {v}"
            raise ValueError(err_msg)
        return v


class GhaWorkflowInput(GhaInput):
    """
    An input under a reusable workflow's `on.workflow_call.inputs` key.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'gha:WorkflowInput',
         'from_schema': 'https://w3id.org/lmodel/github-actions/github_actions_workflow',
         'see_also': ['https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onworkflow_callinputs']})

    input_type: GhaWorkflowInputType = Field(default=..., description="""The input's `type`, which a reusable workflow's input must state. Named input_type because a knowledge bundle reads `type` as the class of the concept.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaWorkflowInput'],
         'see_also': ['https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onworkflow_callinputsinput_idtype']} })
    description: Optional[str] = Field(default=None, description="""What the input, output or secret is for, as the file describes it.""", json_schema_extra = { "linkml_meta": {'comments': ["It means what LOKF's description means and carries the same "
                      "IRI, so lokf adapt folds it into LOKF's slot and a knowledge "
                      'bundle reads one description key.'],
         'domain_of': ['GhaInput', 'GhaOutput', 'GhaWorkflowSecret'],
         'slot_uri': 'schema:description'} })
    input_id: str = Field(default=..., description="""The key a caller writes in its `with` map.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaInput']} })
    default: Optional[str] = Field(default=None, description="""The value used when a caller supplies none, written as a string even where the input's type is a boolean or a number.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaInput']} })
    required: Optional[bool] = Field(default=None, description="""Whether a caller must supply a value.""", json_schema_extra = { "linkml_meta": {'comments': ["An attribute rather than a slot: it carries LOKF's IRI for "
                      "required, and lokf adapt keeps an attribute's name, where it "
                      'would rename a slot that shares one with lokf.yaml.'],
         'domain_of': ['GhaRequiredMixin'],
         'slot_uri': 'schema:valueRequired'} })


class GhaWorkflowOutput(GhaOutput):
    """
    An output under a reusable workflow's `on.workflow_call.outputs` key, set from an output of one of its jobs.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'gha:WorkflowOutput',
         'from_schema': 'https://w3id.org/lmodel/github-actions/github_actions_workflow',
         'see_also': ['https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onworkflow_calloutputs'],
         'slot_usage': {'output_expression': {'name': 'output_expression',
                                              'required': True}}})

    description: Optional[str] = Field(default=None, description="""What the input, output or secret is for, as the file describes it.""", json_schema_extra = { "linkml_meta": {'comments': ["It means what LOKF's description means and carries the same "
                      "IRI, so lokf adapt folds it into LOKF's slot and a knowledge "
                      'bundle reads one description key.'],
         'domain_of': ['GhaInput', 'GhaOutput', 'GhaWorkflowSecret'],
         'slot_uri': 'schema:description'} })
    output_expression: str = Field(default=..., description="""The expression that sets the output, the file's `value` key, such as one that reads an output of a job or a step.""", json_schema_extra = { "linkml_meta": {'comments': ['A slot rather than an attribute because GhaWorkflowOutput '
                      'refines it.'],
         'domain_of': ['GhaOutput'],
         'slot_uri': 'gha:output_expression'} })
    output_id: str = Field(default=..., description="""The key a caller reads the output by.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaOutput']} })


class GhaWorkflowSecret(GhaRequiredMixin):
    """
    A secret under a reusable workflow's `on.workflow_call.secrets` key, by name; its value is never recorded.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'gha:WorkflowSecret',
         'from_schema': 'https://w3id.org/lmodel/github-actions/github_actions_workflow',
         'mixins': ['GhaRequiredMixin'],
         'see_also': ['https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onworkflow_callsecrets']})

    description: Optional[str] = Field(default=None, description="""What the input, output or secret is for, as the file describes it.""", json_schema_extra = { "linkml_meta": {'comments': ["It means what LOKF's description means and carries the same "
                      "IRI, so lokf adapt folds it into LOKF's slot and a knowledge "
                      'bundle reads one description key.'],
         'domain_of': ['GhaInput', 'GhaOutput', 'GhaWorkflowSecret'],
         'slot_uri': 'schema:description'} })
    secret_id: str = Field(default=..., description="""The key a caller passes the secret under.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaWorkflowSecret']} })
    required: Optional[bool] = Field(default=None, description="""Whether a caller must supply a value.""", json_schema_extra = { "linkml_meta": {'comments': ["An attribute rather than a slot: it carries LOKF's IRI for "
                      "required, and lokf adapt keeps an attribute's name, where it "
                      'would rename a slot that shares one with lokf.yaml.'],
         'domain_of': ['GhaRequiredMixin'],
         'slot_uri': 'schema:valueRequired'} })


class GhaAction(ConfiguredBaseModel):
    """
    An action: a directory whose `action.yml` or `action.yaml` file names its inputs, its outputs and the runtime that executes it. A workflow step runs it with `uses`.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'gha:Action',
         'close_mappings': ['cdx:task'],
         'comments': ['SLSA counts the actions a build runs among its steps, which the '
                      "tenant defines; an action is never a build's trust boundary, as "
                      'a reusable workflow that signs provenance is.',
                      "The metadata file's name and description are the concept's "
                      'title and description in a knowledge bundle, so the class adds '
                      'neither.'],
         'from_schema': 'https://w3id.org/lmodel/github-actions/github_actions_action',
         'see_also': ['https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax'],
         'slot_usage': {'inputs': {'description': 'The inputs under the metadata '
                                                  "file's `inputs` key.",
                                   'name': 'inputs',
                                   'range': 'GhaActionInput'},
                        'outputs': {'description': 'The outputs under the metadata '
                                                   "file's `outputs` key.",
                                    'name': 'outputs',
                                    'range': 'GhaActionOutput'}}})

    inputs: Optional[list[GhaActionInput]] = Field(default=None, description="""The inputs under the metadata file's `inputs` key.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaReusableWorkflow', 'GhaAction']} })
    outputs: Optional[list[GhaActionOutput]] = Field(default=None, description="""The outputs under the metadata file's `outputs` key.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaReusableWorkflow', 'GhaAction']} })
    action_uri: str = Field(default=..., description="""The action's address on its forge without a ref: `https://github.com/<owner>/<repo>`, followed by the directory's path when the action is not at the repository root. A step's `uses` names it as `<owner>/<repo>/<path>@<ref>`.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaAction']} })
    action_path: str = Field(default=..., description="""The metadata file's path from the repository root.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaAction']} })
    using: GhaActionRuntime = Field(default=..., description="""The runtime that executes the action, its `runs.using` value.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaAction']} })

    @field_validator('action_path')
    def pattern_action_path(cls, v):
        pattern=re.compile(r"^(.+/)?action\.ya?ml$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid action_path format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid action_path format: {v}"
            raise ValueError(err_msg)
        return v


class GhaActionInput(GhaInput):
    """
    An input under an action's `inputs` key.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'gha:ActionInput',
         'from_schema': 'https://w3id.org/lmodel/github-actions/github_actions_action',
         'see_also': ['https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax#inputs'],
         'slot_usage': {'description': {'name': 'description', 'required': True}}})

    deprecation_message: Optional[str] = Field(default=None, description="""The message GitHub shows a workflow that still passes the input, the file's `deprecationMessage`; present only when the input is deprecated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaActionInput'],
         'see_also': ['https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax#inputsinput_iddeprecationmessage']} })
    description: str = Field(default=..., description="""What the input, output or secret is for, as the file describes it.""", json_schema_extra = { "linkml_meta": {'comments': ["It means what LOKF's description means and carries the same "
                      "IRI, so lokf adapt folds it into LOKF's slot and a knowledge "
                      'bundle reads one description key.'],
         'domain_of': ['GhaInput', 'GhaOutput', 'GhaWorkflowSecret'],
         'slot_uri': 'schema:description'} })
    input_id: str = Field(default=..., description="""The key a caller writes in its `with` map.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaInput']} })
    default: Optional[str] = Field(default=None, description="""The value used when a caller supplies none, written as a string even where the input's type is a boolean or a number.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaInput']} })
    required: Optional[bool] = Field(default=None, description="""Whether a caller must supply a value.""", json_schema_extra = { "linkml_meta": {'comments': ["An attribute rather than a slot: it carries LOKF's IRI for "
                      "required, and lokf adapt keeps an attribute's name, where it "
                      'would rename a slot that shares one with lokf.yaml.'],
         'domain_of': ['GhaRequiredMixin'],
         'slot_uri': 'schema:valueRequired'} })


class GhaActionOutput(GhaOutput):
    """
    An output under an action's `outputs` key.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'gha:ActionOutput',
         'comments': ['Only a composite action sets an output from an expression; a '
                      'Docker or JavaScript action writes its outputs while it runs, '
                      'so its outputs have no output_expression.'],
         'from_schema': 'https://w3id.org/lmodel/github-actions/github_actions_action',
         'see_also': ['https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax#outputs-for-docker-container-and-javascript-actions',
                      'https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax#outputs-for-composite-actions'],
         'slot_usage': {'description': {'name': 'description', 'required': True}}})

    description: str = Field(default=..., description="""What the input, output or secret is for, as the file describes it.""", json_schema_extra = { "linkml_meta": {'comments': ["It means what LOKF's description means and carries the same "
                      "IRI, so lokf adapt folds it into LOKF's slot and a knowledge "
                      'bundle reads one description key.'],
         'domain_of': ['GhaInput', 'GhaOutput', 'GhaWorkflowSecret'],
         'slot_uri': 'schema:description'} })
    output_expression: Optional[str] = Field(default=None, description="""The expression that sets the output, the file's `value` key, such as one that reads an output of a job or a step.""", json_schema_extra = { "linkml_meta": {'comments': ['A slot rather than an attribute because GhaWorkflowOutput '
                      'refines it.'],
         'domain_of': ['GhaOutput'],
         'slot_uri': 'gha:output_expression'} })
    output_id: str = Field(default=..., description="""The key a caller reads the output by.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaOutput']} })


class GhaRepositoryRuleset(ConfiguredBaseModel):
    """
    A ruleset: named rules that GitHub enforces on the branches, tags or pushes of a repository, or of every repository in an organization or enterprise that it targets.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'gha:RepositoryRuleset',
         'comments': ["SLSA's Source track calls such rules technical controls on "
                      'protected named references, and asks that their meaning be '
                      'documented and their enforcement recorded in attestations; the '
                      'slsa schema models that evidence.',
                      "Of the rules' parameters, only those of required_status_checks "
                      'are modelled, as GhaRequiredStatusCheck; rule_types says which '
                      'other rules the ruleset holds.'],
         'from_schema': 'https://w3id.org/lmodel/github-actions/github_actions_rules',
         'see_also': ['https://docs.github.com/en/rest/repos/rules',
                      'https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets']})

    ruleset_uri: str = Field(default=..., description="""The ruleset's page, the REST response's `_links.html.href`, such as `https://github.com/<owner>/<repo>/rules/<id>`.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaRepositoryRuleset']} })
    ruleset_id: Optional[int] = Field(default=None, description="""The ruleset's numeric `id` in the REST API.""", ge=1, json_schema_extra = { "linkml_meta": {'domain_of': ['GhaRepositoryRuleset']} })
    ruleset_source_type: Optional[GhaRulesetSourceType] = Field(default=None, description="""What owns the ruleset, the REST field `source_type`: a repository, an organization or an enterprise.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaRepositoryRuleset']} })
    ruleset_source: Optional[str] = Field(default=None, description="""The name of the repository, organization or enterprise that owns the ruleset, the REST field `source`, such as `<owner>/<repo>`.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaRepositoryRuleset']} })
    ruleset_target: GhaRulesetTarget = Field(default=..., description="""What the ruleset applies to, the REST field `target`. Named ruleset_target because LOKF defines a target slot of its own.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaRepositoryRuleset']} })
    enforcement: GhaRulesetEnforcement = Field(default=..., description="""Whether GitHub enforces the ruleset, the REST field `enforcement`.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaRepositoryRuleset']} })
    ref_name_include: Optional[list[str]] = Field(default=None, description="""The refs the ruleset applies to, from `conditions.ref_name.include`: names or patterns such as `refs/heads/main`, or `~DEFAULT_BRANCH` or `~ALL`. A ref must match one of them.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaRepositoryRuleset']} })
    ref_name_exclude: Optional[list[str]] = Field(default=None, description="""The refs the ruleset leaves out, from `conditions.ref_name.exclude`, even when they match an included one.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaRepositoryRuleset']} })
    bypass_actors: Optional[list[GhaBypassActor]] = Field(default=None, description="""The actors who may bypass the ruleset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaRepositoryRuleset']} })
    rule_types: Optional[list[str]] = Field(default=None, description="""The `type` of each rule the ruleset holds, such as `deletion`, `non_fast_forward`, `pull_request` or `required_status_checks`.""", json_schema_extra = { "linkml_meta": {'comments': ['A pattern rather than an enumeration, because GitHub adds rule '
                      'types.'],
         'domain_of': ['GhaRepositoryRuleset']} })
    requires_check: Optional[list[str]] = Field(default=None, description="""The status checks the ruleset's required_status_checks rule requires, each a concept of its own.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaRepositoryRuleset']} })

    @field_validator('rule_types')
    def pattern_rule_types(cls, v):
        pattern=re.compile(r"^[a-z_]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid rule_types format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid rule_types format: {v}"
            raise ValueError(err_msg)
        return v


class GhaBypassActor(ConfiguredBaseModel):
    """
    An actor who may bypass a ruleset, and when.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'gha:BypassActor',
         'from_schema': 'https://w3id.org/lmodel/github-actions/github_actions_rules',
         'see_also': ['https://docs.github.com/en/rest/repos/rules']})

    actor_id: Optional[int] = Field(default=None, description="""The actor's numeric id; absent for an actor type GitHub takes no id for, such as DeployKey or OrganizationAdmin.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaBypassActor']} })
    actor_type: str = Field(default=..., description="""The kind of actor, the REST field `actor_type`, such as `Team`, `RepositoryRole`, `Integration` or `OrganizationAdmin`.""", json_schema_extra = { "linkml_meta": {'comments': ['A pattern rather than an enumeration, because GitHub adds actor '
                      'types.'],
         'domain_of': ['GhaBypassActor']} })
    bypass_mode: Optional[str] = Field(default=None, description="""When the actor may bypass, the REST field `bypass_mode`, such as `always`, `pull_request` or `exempt`; GitHub's default is `always`.""", json_schema_extra = { "linkml_meta": {'comments': ['A pattern rather than an enumeration, because GitHub adds '
                      'bypass modes.'],
         'domain_of': ['GhaBypassActor']} })

    @field_validator('actor_type')
    def pattern_actor_type(cls, v):
        pattern=re.compile(r"^[A-Z][A-Za-z]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid actor_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid actor_type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('bypass_mode')
    def pattern_bypass_mode(cls, v):
        pattern=re.compile(r"^[a-z_]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid bypass_mode format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid bypass_mode format: {v}"
            raise ValueError(err_msg)
        return v


class GhaRequiredStatusCheck(ConfiguredBaseModel):
    """
    A status check that a ruleset requires to pass before a change reaches a ref it targets, named by the context a check run must report.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'gha:RequiredStatusCheck',
         'comments': ['GitHub Actions reports each job as a check run named after the '
                      'job: its name, or its id when it has none. A job of a called '
                      'workflow is named after the calling job and the called job, '
                      'joined by a slash with a space on each side, as the otterdog '
                      'documentation states '
                      '(https://otterdog.readthedocs.io/en/latest/reference/organization/repository/status-check/). '
                      "A matrix job's check name adds its matrix values in "
                      'parentheses.',
                      'A job that a path filter or an `if` skips reports success and '
                      'does not block a merge, even when its check is required; '
                      'skip_conditions records what can skip it, so a reader can see '
                      'the hole.',
                      "SLSA's Source track lets an organization carry such a control "
                      'into a Source Verification Summary Attestation as an '
                      'ORG_SOURCE_ property, whose meaning the organization defines; '
                      "slsa-framework's source-tool emits one as GH_REQUIRED_CHECK_ "
                      "followed by the check's name.",
                      "in-toto's Test Result predicate is the shape of an attestation "
                      'of what the check found, so it is a related term and not a '
                      'close one.'],
         'from_schema': 'https://w3id.org/lmodel/github-actions/github_actions_rules',
         'related_mappings': ['https://in-toto.io/attestation/test-result/v0.1'],
         'see_also': ['https://docs.github.com/en/rest/repos/rules',
                      'https://docs.github.com/en/rest/checks/runs',
                      'https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/about-status-checks',
                      'https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks']})

    check_uri: str = Field(default=..., description="""An identifier for the requirement. GitHub gives a required check no address of its own; in a knowledge bundle the concept's `id` takes its place.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaRequiredStatusCheck']} })
    check_context: str = Field(default=..., description="""The context a check run must report, the rule's `required_status_checks[].context`. Named check_context because LOKF defines a context slot of its own.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaRequiredStatusCheck']} })
    integration_id: Optional[int] = Field(default=None, description="""The GitHub App the check must come from, the rule's `integration_id`; GitHub Actions is app 15368.""", ge=1, json_schema_extra = { "linkml_meta": {'domain_of': ['GhaRequiredStatusCheck']} })
    strict_policy: Optional[bool] = Field(default=None, description="""Whether a pull request must be tested against the latest code of the branch it targets, the rule's `strict_required_status_checks_policy`.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaRequiredStatusCheck']} })
    do_not_enforce_on_create: Optional[bool] = Field(default=None, description="""Whether a branch may be created although the check would otherwise stop it, the rule's `do_not_enforce_on_create`.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaRequiredStatusCheck']} })
    job_path: Optional[list[str]] = Field(default=None, description="""The ids of the jobs from the top-level workflow's job to the job that reports the check: one id for a job of the workflow itself, the calling job's id first for a job of a called workflow.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaRequiredStatusCheck'], 'list_elements_ordered': True} })
    skip_conditions: Optional[list[str]] = Field(default=None, description="""What in the workflow can skip the job that reports the check, each written as its key's path in the file, such as `on.pull_request.paths` or `jobs.test.if`.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaRequiredStatusCheck']} })
    emitted_by: Optional[str] = Field(default=None, description="""The top-level workflow whose job reports the check.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaRequiredStatusCheck']} })

    @field_validator('check_context')
    def pattern_check_context(cls, v):
        pattern=re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid check_context format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid check_context format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('skip_conditions')
    def pattern_skip_conditions(cls, v):
        pattern=re.compile(r"^(on|jobs)\.\S+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid skip_conditions format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid skip_conditions format: {v}"
            raise ValueError(err_msg)
        return v


class GhaDocument(ConfiguredBaseModel):
    """
    A document that holds the workflows, actions, rulesets and required status checks of one or more repositories.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'gha:Document',
         'from_schema': 'https://w3id.org/lmodel/github-actions',
         'tree_root': True})

    workflows: Optional[list[GhaWorkflow]] = Field(default=None, description="""The workflows other than the reusable ones.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaDocument']} })
    reusable_workflows: Optional[list[GhaReusableWorkflow]] = Field(default=None, description="""The reusable workflows.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaDocument']} })
    actions: Optional[list[GhaAction]] = Field(default=None, description="""The actions.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaDocument']} })
    rulesets: Optional[list[GhaRepositoryRuleset]] = Field(default=None, description="""The rulesets.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaDocument']} })
    required_checks: Optional[list[GhaRequiredStatusCheck]] = Field(default=None, description="""The status checks the rulesets require.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GhaDocument']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
GhaRequiredMixin.model_rebuild()
GhaInput.model_rebuild()
GhaOutput.model_rebuild()
GhaWorkflow.model_rebuild()
GhaReusableWorkflow.model_rebuild()
GhaWorkflowJob.model_rebuild()
GhaWorkflowInput.model_rebuild()
GhaWorkflowOutput.model_rebuild()
GhaWorkflowSecret.model_rebuild()
GhaAction.model_rebuild()
GhaActionInput.model_rebuild()
GhaActionOutput.model_rebuild()
GhaRepositoryRuleset.model_rebuild()
GhaBypassActor.model_rebuild()
GhaRequiredStatusCheck.model_rebuild()
GhaDocument.model_rebuild()
