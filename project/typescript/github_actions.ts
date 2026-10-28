export type GhaWorkflowWorkflowUri = string;
export type GhaReusableWorkflowWorkflowUri = string;
export type GhaActionActionUri = string;
export type GhaRepositoryRulesetRulesetUri = string;
export type GhaRequiredStatusCheckCheckUri = string;
/**
* The types a reusable workflow's input may state.
*/
export enum GhaWorkflowInputType {
    
    /** True or false. */
    boolean = "boolean",
    /** A number. */
    number = "number",
    /** A string. */
    string = "string",
};
/**
* Who hosts the runner a job runs on, as GitHub's build type records it.
*/
export enum GhaRunnerEnvironment {
    
    /** A runner that GitHub hosts. */
    GitHub_hosted = "github-hosted",
    /** A runner that the repository's owner hosts. */
    Self_hosted = "self-hosted",
};
/**
* The runtimes an action's `runs.using` may name.
*/
export enum GhaActionRuntime {
    
    /** Steps that run in the calling job, as a workflow's steps do. */
    composite = "composite",
    /** A Docker container. */
    docker = "docker",
    /** JavaScript, run by Node.js 20. */
    node20 = "node20",
    /** JavaScript, run by Node.js 24. */
    node24 = "node24",
};
/**
* What can own a ruleset, as the REST field `source_type` names it.
*/
export enum GhaRulesetSourceType {
    
    /** A repository's own ruleset. */
    Repository = "Repository",
    /** An organization's ruleset, applied to the repositories it targets. */
    Organization = "Organization",
    /** An enterprise's ruleset, applied to the repositories it targets. */
    Enterprise = "Enterprise",
};
/**
* What a ruleset applies to, as the REST field `target` names it.
*/
export enum GhaRulesetTarget {
    
    /** Branches; GitHub's default. */
    branch = "branch",
    /** Tags. */
    tag = "tag",
    /** Pushes, by the files they change. */
    push = "push",
};
/**
* Whether GitHub enforces a ruleset, as the REST field `enforcement` names it.
*/
export enum GhaRulesetEnforcement {
    
    /** Enforced. */
    active = "active",
    /** Evaluated and reported but not enforced, so administrators can test its rules; only on GitHub Enterprise. */
    evaluate = "evaluate",
    /** Neither enforced nor evaluated. */
    disabled = "disabled",
};


/**
 * The field that says whether a caller must supply a value.
 */
export interface GhaRequiredMixin {
    /** Whether a caller must supply a value. */
    required?: boolean,
}


/**
 * An input that a reusable workflow or an action declares, under the key a caller writes in its `with` map.
 */
export interface GhaInput extends GhaRequiredMixin {
    /** What the input, output or secret is for, as the file describes it. */
    description?: string,
    /** The key a caller writes in its `with` map. */
    input_id: string,
    /** The value used when a caller supplies none, written as a string even where the input's type is a boolean or a number. */
    default?: string,
}


/**
 * An output that a reusable workflow or an action declares for the job or step that calls it to read.
 */
export interface GhaOutput {
    /** What the input, output or secret is for, as the file describes it. */
    description?: string,
    /** The expression that sets the output, the file's `value` key, such as one that reads an output of a job or a step. */
    output_expression?: string,
    /** The key a caller reads the output by. */
    output_id: string,
}


/**
 * A workflow file in a repository's `.github/workflows` directory: the events that run it, the access its GITHUB_TOKEN gets, and its jobs.
 */
export interface GhaWorkflow {
    /** The names of the events under the file's `on` key, such as `push`, `pull_request`, `schedule` or `workflow_call`. */
    triggers: string[],
    /** The file's address on its forge without a ref: `https://github.com/<owner>/<repo>/.github/workflows/<file>`. */
    workflow_uri: string,
    /** The file's path from the repository root, as GitHub's build type writes workflow.path. GitHub reads no subdirectory of `.github/workflows`. */
    workflow_path: string,
    /** The repository that holds the file, as GitHub's build type writes workflow.repository: an HTTPS address without `.git`. */
    workflow_repository?: string,
    /** The access the file's top-level `permissions` key gives every job's GITHUB_TOKEN. Absent when the file sets none, so the repository's or organization's default applies; a scope the map leaves out gets no access. */
    permissions?: string[],
    /** The jobs under the file's `jobs` key. */
    jobs: GhaWorkflowJob[],
}


/**
 * A workflow that other workflows call as a job, because its `on` key names `workflow_call`; it declares the inputs, outputs and secrets its callers pass and read.
 */
export interface GhaReusableWorkflow extends GhaWorkflow {
    /** The inputs under the file's `on.workflow_call.inputs` key. */
    inputs?: GhaWorkflowInput[],
    /** The outputs under the file's `on.workflow_call.outputs` key. */
    outputs?: GhaWorkflowOutput[],
    /** The secrets under the file's `on.workflow_call.secrets` key, by name only; no value is ever recorded. */
    secrets?: GhaWorkflowSecret[],
}


/**
 * A job under a workflow's `jobs` key: steps that run on a runner, or a call to a reusable workflow.
 */
export interface GhaWorkflowJob {
    /** The job's key under `jobs`. */
    job_id: string,
    /** The job's `name`, which GitHub shows and its check run takes; the check run takes the job's id when it has none. */
    job_name?: string,
    /** The reusable workflow the job runs, its `uses` value: `./.github/workflows/<file>` in the same repository, or `<owner>/<repo>/.github/workflows/<file>@<ref>`. */
    calls?: string,
    /** The runner labels from the job's `runs-on`: one label, a list, or the `labels` of a group. A runner must carry every one. */
    runs_on?: string[],
    /** The runner group the job's `runs-on.group` names. */
    runner_group?: string,
    /** Whether the job's runner is hosted by GitHub or by the repository's owner, as GitHub's build type records runner_environment for a run. */
    runner_environment?: string,
    /** The access the job's own `permissions` key gives its GITHUB_TOKEN, in place of the workflow's. A called workflow can lower its token's access, never raise it. */
    job_permissions?: string[],
}


/**
 * An input under a reusable workflow's `on.workflow_call.inputs` key.
 */
export interface GhaWorkflowInput extends GhaInput {
    /** The input's `type`, which a reusable workflow's input must state. Named input_type because a knowledge bundle reads `type` as the class of the concept. */
    input_type: string,
}


/**
 * An output under a reusable workflow's `on.workflow_call.outputs` key, set from an output of one of its jobs.
 */
export interface GhaWorkflowOutput extends GhaOutput {
}


/**
 * A secret under a reusable workflow's `on.workflow_call.secrets` key, by name; its value is never recorded.
 */
export interface GhaWorkflowSecret extends GhaRequiredMixin {
    /** What the input, output or secret is for, as the file describes it. */
    description?: string,
    /** The key a caller passes the secret under. */
    secret_id: string,
}


/**
 * An action: a directory whose `action.yml` or `action.yaml` file names its inputs, its outputs and the runtime that executes it. A workflow step runs it with `uses`.
 */
export interface GhaAction {
    /** The inputs under the metadata file's `inputs` key. */
    inputs?: GhaActionInput[],
    /** The outputs under the metadata file's `outputs` key. */
    outputs?: GhaActionOutput[],
    /** The action's address on its forge without a ref: `https://github.com/<owner>/<repo>`, followed by the directory's path when the action is not at the repository root. A step's `uses` names it as `<owner>/<repo>/<path>@<ref>`. */
    action_uri: string,
    /** The metadata file's path from the repository root. */
    action_path: string,
    /** The runtime that executes the action, its `runs.using` value. */
    using: string,
}


/**
 * An input under an action's `inputs` key.
 */
export interface GhaActionInput extends GhaInput {
    /** The message GitHub shows a workflow that still passes the input, the file's `deprecationMessage`; present only when the input is deprecated. */
    deprecation_message?: string,
}


/**
 * An output under an action's `outputs` key.
 */
export interface GhaActionOutput extends GhaOutput {
}


/**
 * A ruleset: named rules that GitHub enforces on the branches, tags or pushes of a repository, or of every repository in an organization or enterprise that it targets.
 */
export interface GhaRepositoryRuleset {
    /** The ruleset's page, the REST response's `_links.html.href`, such as `https://github.com/<owner>/<repo>/rules/<id>`. */
    ruleset_uri: string,
    /** The ruleset's numeric `id` in the REST API. */
    ruleset_id?: number,
    /** What owns the ruleset, the REST field `source_type`: a repository, an organization or an enterprise. */
    ruleset_source_type?: string,
    /** The name of the repository, organization or enterprise that owns the ruleset, the REST field `source`, such as `<owner>/<repo>`. */
    ruleset_source?: string,
    /** What the ruleset applies to, the REST field `target`. Named ruleset_target because LOKF defines a target slot of its own. */
    ruleset_target: string,
    /** Whether GitHub enforces the ruleset, the REST field `enforcement`. */
    enforcement: string,
    /** The refs the ruleset applies to, from `conditions.ref_name.include`: names or patterns such as `refs/heads/main`, or `~DEFAULT_BRANCH` or `~ALL`. A ref must match one of them. */
    ref_name_include?: string[],
    /** The refs the ruleset leaves out, from `conditions.ref_name.exclude`, even when they match an included one. */
    ref_name_exclude?: string[],
    /** The actors who may bypass the ruleset. */
    bypass_actors?: GhaBypassActor[],
    /** The `type` of each rule the ruleset holds, such as `deletion`, `non_fast_forward`, `pull_request` or `required_status_checks`. */
    rule_types?: string[],
    /** The status checks the ruleset's required_status_checks rule requires, each a concept of its own. */
    requires_check?: GhaRequiredStatusCheckCheckUri[],
}


/**
 * An actor who may bypass a ruleset, and when.
 */
export interface GhaBypassActor {
    /** The actor's numeric id; absent for an actor type GitHub takes no id for, such as DeployKey or OrganizationAdmin. */
    actor_id?: number,
    /** The kind of actor, the REST field `actor_type`, such as `Team`, `RepositoryRole`, `Integration` or `OrganizationAdmin`. */
    actor_type: string,
    /** When the actor may bypass, the REST field `bypass_mode`, such as `always`, `pull_request` or `exempt`; GitHub's default is `always`. */
    bypass_mode?: string,
}


/**
 * A status check that a ruleset requires to pass before a change reaches a ref it targets, named by the context a check run must report.
 */
export interface GhaRequiredStatusCheck {
    /** An identifier for the requirement. GitHub gives a required check no address of its own; in a knowledge bundle the concept's `id` takes its place. */
    check_uri: string,
    /** The context a check run must report, the rule's `required_status_checks[].context`. Named check_context because LOKF defines a context slot of its own. */
    check_context: string,
    /** The GitHub App the check must come from, the rule's `integration_id`; GitHub Actions is app 15368. */
    integration_id?: number,
    /** Whether a pull request must be tested against the latest code of the branch it targets, the rule's `strict_required_status_checks_policy`. */
    strict_policy?: boolean,
    /** Whether a branch may be created although the check would otherwise stop it, the rule's `do_not_enforce_on_create`. */
    do_not_enforce_on_create?: boolean,
    /** The ids of the jobs from the top-level workflow's job to the job that reports the check: one id for a job of the workflow itself, the calling job's id first for a job of a called workflow. */
    job_path?: string[],
    /** What in the workflow can skip the job that reports the check, each written as its key's path in the file, such as `on.pull_request.paths` or `jobs.test.if`. */
    skip_conditions?: string[],
    /** The top-level workflow whose job reports the check. */
    emitted_by?: GhaWorkflowWorkflowUri,
}


/**
 * A document that holds the workflows, actions, rulesets and required status checks of one or more repositories.
 */
export interface GhaDocument {
    /** The workflows other than the reusable ones. */
    workflows?: GhaWorkflow[],
    /** The reusable workflows. */
    reusable_workflows?: GhaReusableWorkflow[],
    /** The actions. */
    actions?: GhaAction[],
    /** The rulesets. */
    rulesets?: GhaRepositoryRuleset[],
    /** The status checks the rulesets require. */
    required_checks?: GhaRequiredStatusCheck[],
}



