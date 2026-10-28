-- # Class: GhaDocument Description: A document that holds the workflows, actions, rulesets and required status checks of one or more repositories.
--     * Slot: id
-- # Class: GhaRequiredMixin Description: The field that says whether a caller must supply a value.
--     * Slot: id
--     * Slot: required Description: Whether a caller must supply a value.
-- # Abstract Class: GhaInput Description: An input that a reusable workflow or an action declares, under the key a caller writes in its `with` map.
--     * Slot: id
--     * Slot: description Description: What the input, output or secret is for, as the file describes it.
--     * Slot: input_id Description: The key a caller writes in its `with` map.
--     * Slot: default Description: The value used when a caller supplies none, written as a string even where the input's type is a boolean or a number.
--     * Slot: required Description: Whether a caller must supply a value.
-- # Abstract Class: GhaOutput Description: An output that a reusable workflow or an action declares for the job or step that calls it to read.
--     * Slot: id
--     * Slot: description Description: What the input, output or secret is for, as the file describes it.
--     * Slot: output_expression Description: The expression that sets the output, the file's `value` key, such as one that reads an output of a job or a step.
--     * Slot: output_id Description: The key a caller reads the output by.
-- # Class: GhaWorkflow Description: A workflow file in a repository's `.github/workflows` directory: the events that run it, the access its GITHUB_TOKEN gets, and its jobs.
--     * Slot: workflow_uri Description: The file's address on its forge without a ref: `https://github.com/<owner>/<repo>/.github/workflows/<file>`.
--     * Slot: workflow_path Description: The file's path from the repository root, as GitHub's build type writes workflow.path. GitHub reads no subdirectory of `.github/workflows`.
--     * Slot: workflow_repository Description: The repository that holds the file, as GitHub's build type writes workflow.repository: an HTTPS address without `.git`.
--     * Slot: GhaDocument_id Description: Autocreated FK slot
-- # Class: GhaReusableWorkflow Description: A workflow that other workflows call as a job, because its `on` key names `workflow_call`; it declares the inputs, outputs and secrets its callers pass and read.
--     * Slot: workflow_uri Description: The file's address on its forge without a ref: `https://github.com/<owner>/<repo>/.github/workflows/<file>`.
--     * Slot: workflow_path Description: The file's path from the repository root, as GitHub's build type writes workflow.path. GitHub reads no subdirectory of `.github/workflows`.
--     * Slot: workflow_repository Description: The repository that holds the file, as GitHub's build type writes workflow.repository: an HTTPS address without `.git`.
--     * Slot: GhaDocument_id Description: Autocreated FK slot
-- # Class: GhaWorkflowJob Description: A job under a workflow's `jobs` key: steps that run on a runner, or a call to a reusable workflow.
--     * Slot: id
--     * Slot: job_id Description: The job's key under `jobs`.
--     * Slot: job_name Description: The job's `name`, which GitHub shows and its check run takes; the check run takes the job's id when it has none.
--     * Slot: calls Description: The reusable workflow the job runs, its `uses` value: `./.github/workflows/<file>` in the same repository, or `<owner>/<repo>/.github/workflows/<file>@<ref>`.
--     * Slot: runner_group Description: The runner group the job's `runs-on.group` names.
--     * Slot: runner_environment Description: Whether the job's runner is hosted by GitHub or by the repository's owner, as GitHub's build type records runner_environment for a run.
--     * Slot: GhaWorkflow_workflow_uri Description: Autocreated FK slot
--     * Slot: GhaReusableWorkflow_workflow_uri Description: Autocreated FK slot
-- # Class: GhaWorkflowInput Description: An input under a reusable workflow's `on.workflow_call.inputs` key.
--     * Slot: id
--     * Slot: input_type Description: The input's `type`, which a reusable workflow's input must state. Named input_type because a knowledge bundle reads `type` as the class of the concept.
--     * Slot: description Description: What the input, output or secret is for, as the file describes it.
--     * Slot: input_id Description: The key a caller writes in its `with` map.
--     * Slot: default Description: The value used when a caller supplies none, written as a string even where the input's type is a boolean or a number.
--     * Slot: required Description: Whether a caller must supply a value.
--     * Slot: GhaReusableWorkflow_workflow_uri Description: Autocreated FK slot
-- # Class: GhaWorkflowOutput Description: An output under a reusable workflow's `on.workflow_call.outputs` key, set from an output of one of its jobs.
--     * Slot: id
--     * Slot: description Description: What the input, output or secret is for, as the file describes it.
--     * Slot: output_expression Description: The expression that sets the output, the file's `value` key, such as one that reads an output of a job or a step.
--     * Slot: output_id Description: The key a caller reads the output by.
--     * Slot: GhaReusableWorkflow_workflow_uri Description: Autocreated FK slot
-- # Class: GhaWorkflowSecret Description: A secret under a reusable workflow's `on.workflow_call.secrets` key, by name; its value is never recorded.
--     * Slot: id
--     * Slot: description Description: What the input, output or secret is for, as the file describes it.
--     * Slot: secret_id Description: The key a caller passes the secret under.
--     * Slot: required Description: Whether a caller must supply a value.
--     * Slot: GhaReusableWorkflow_workflow_uri Description: Autocreated FK slot
-- # Class: GhaAction Description: An action: a directory whose `action.yml` or `action.yaml` file names its inputs, its outputs and the runtime that executes it. A workflow step runs it with `uses`.
--     * Slot: action_uri Description: The action's address on its forge without a ref: `https://github.com/<owner>/<repo>`, followed by the directory's path when the action is not at the repository root. A step's `uses` names it as `<owner>/<repo>/<path>@<ref>`.
--     * Slot: action_path Description: The metadata file's path from the repository root.
--     * Slot: using Description: The runtime that executes the action, its `runs.using` value.
--     * Slot: GhaDocument_id Description: Autocreated FK slot
-- # Class: GhaActionInput Description: An input under an action's `inputs` key.
--     * Slot: id
--     * Slot: deprecation_message Description: The message GitHub shows a workflow that still passes the input, the file's `deprecationMessage`; present only when the input is deprecated.
--     * Slot: description Description: What the input, output or secret is for, as the file describes it.
--     * Slot: input_id Description: The key a caller writes in its `with` map.
--     * Slot: default Description: The value used when a caller supplies none, written as a string even where the input's type is a boolean or a number.
--     * Slot: required Description: Whether a caller must supply a value.
--     * Slot: GhaAction_action_uri Description: Autocreated FK slot
-- # Class: GhaActionOutput Description: An output under an action's `outputs` key.
--     * Slot: id
--     * Slot: description Description: What the input, output or secret is for, as the file describes it.
--     * Slot: output_expression Description: The expression that sets the output, the file's `value` key, such as one that reads an output of a job or a step.
--     * Slot: output_id Description: The key a caller reads the output by.
--     * Slot: GhaAction_action_uri Description: Autocreated FK slot
-- # Class: GhaRepositoryRuleset Description: A ruleset: named rules that GitHub enforces on the branches, tags or pushes of a repository, or of every repository in an organization or enterprise that it targets.
--     * Slot: ruleset_uri Description: The ruleset's page, the REST response's `_links.html.href`, such as `https://github.com/<owner>/<repo>/rules/<id>`.
--     * Slot: ruleset_id Description: The ruleset's numeric `id` in the REST API.
--     * Slot: ruleset_source_type Description: What owns the ruleset, the REST field `source_type`: a repository, an organization or an enterprise.
--     * Slot: ruleset_source Description: The name of the repository, organization or enterprise that owns the ruleset, the REST field `source`, such as `<owner>/<repo>`.
--     * Slot: ruleset_target Description: What the ruleset applies to, the REST field `target`. Named ruleset_target because LOKF defines a target slot of its own.
--     * Slot: enforcement Description: Whether GitHub enforces the ruleset, the REST field `enforcement`.
--     * Slot: GhaDocument_id Description: Autocreated FK slot
-- # Class: GhaBypassActor Description: An actor who may bypass a ruleset, and when.
--     * Slot: id
--     * Slot: actor_id Description: The actor's numeric id; absent for an actor type GitHub takes no id for, such as DeployKey or OrganizationAdmin.
--     * Slot: actor_type Description: The kind of actor, the REST field `actor_type`, such as `Team`, `RepositoryRole`, `Integration` or `OrganizationAdmin`.
--     * Slot: bypass_mode Description: When the actor may bypass, the REST field `bypass_mode`, such as `always`, `pull_request` or `exempt`; GitHub's default is `always`.
--     * Slot: GhaRepositoryRuleset_ruleset_uri Description: Autocreated FK slot
-- # Class: GhaRequiredStatusCheck Description: A status check that a ruleset requires to pass before a change reaches a ref it targets, named by the context a check run must report.
--     * Slot: check_uri Description: An identifier for the requirement. GitHub gives a required check no address of its own; in a knowledge bundle the concept's `id` takes its place.
--     * Slot: check_context Description: The context a check run must report, the rule's `required_status_checks[].context`. Named check_context because LOKF defines a context slot of its own.
--     * Slot: integration_id Description: The GitHub App the check must come from, the rule's `integration_id`; GitHub Actions is app 15368.
--     * Slot: strict_policy Description: Whether a pull request must be tested against the latest code of the branch it targets, the rule's `strict_required_status_checks_policy`.
--     * Slot: do_not_enforce_on_create Description: Whether a branch may be created although the check would otherwise stop it, the rule's `do_not_enforce_on_create`.
--     * Slot: emitted_by Description: The top-level workflow whose job reports the check.
--     * Slot: GhaDocument_id Description: Autocreated FK slot
-- # Class: GhaWorkflow_triggers
--     * Slot: GhaWorkflow_workflow_uri Description: Autocreated FK slot
--     * Slot: triggers Description: The names of the events under the file's `on` key, such as `push`, `pull_request`, `schedule` or `workflow_call`.
-- # Class: GhaWorkflow_permissions
--     * Slot: GhaWorkflow_workflow_uri Description: Autocreated FK slot
--     * Slot: permissions Description: The access the file's top-level `permissions` key gives every job's GITHUB_TOKEN. Absent when the file sets none, so the repository's or organization's default applies; a scope the map leaves out gets no access.
-- # Class: GhaReusableWorkflow_triggers
--     * Slot: GhaReusableWorkflow_workflow_uri Description: Autocreated FK slot
--     * Slot: triggers Description: The names of the events under the file's `on` key, such as `push`, `pull_request`, `schedule` or `workflow_call`.
-- # Class: GhaReusableWorkflow_permissions
--     * Slot: GhaReusableWorkflow_workflow_uri Description: Autocreated FK slot
--     * Slot: permissions Description: The access the file's top-level `permissions` key gives every job's GITHUB_TOKEN. Absent when the file sets none, so the repository's or organization's default applies; a scope the map leaves out gets no access.
-- # Class: GhaWorkflowJob_runs_on
--     * Slot: GhaWorkflowJob_id Description: Autocreated FK slot
--     * Slot: runs_on Description: The runner labels from the job's `runs-on`: one label, a list, or the `labels` of a group. A runner must carry every one.
-- # Class: GhaWorkflowJob_job_permissions
--     * Slot: GhaWorkflowJob_id Description: Autocreated FK slot
--     * Slot: job_permissions Description: The access the job's own `permissions` key gives its GITHUB_TOKEN, in place of the workflow's. A called workflow can lower its token's access, never raise it.
-- # Class: GhaRepositoryRuleset_ref_name_include
--     * Slot: GhaRepositoryRuleset_ruleset_uri Description: Autocreated FK slot
--     * Slot: ref_name_include Description: The refs the ruleset applies to, from `conditions.ref_name.include`: names or patterns such as `refs/heads/main`, or `~DEFAULT_BRANCH` or `~ALL`. A ref must match one of them.
-- # Class: GhaRepositoryRuleset_ref_name_exclude
--     * Slot: GhaRepositoryRuleset_ruleset_uri Description: Autocreated FK slot
--     * Slot: ref_name_exclude Description: The refs the ruleset leaves out, from `conditions.ref_name.exclude`, even when they match an included one.
-- # Class: GhaRepositoryRuleset_rule_types
--     * Slot: GhaRepositoryRuleset_ruleset_uri Description: Autocreated FK slot
--     * Slot: rule_types Description: The `type` of each rule the ruleset holds, such as `deletion`, `non_fast_forward`, `pull_request` or `required_status_checks`.
-- # Class: GhaRepositoryRuleset_requires_check
--     * Slot: GhaRepositoryRuleset_ruleset_uri Description: Autocreated FK slot
--     * Slot: requires_check_check_uri Description: The status checks the ruleset's required_status_checks rule requires, each a concept of its own.
-- # Class: GhaRequiredStatusCheck_job_path
--     * Slot: GhaRequiredStatusCheck_check_uri Description: Autocreated FK slot
--     * Slot: job_path Description: The ids of the jobs from the top-level workflow's job to the job that reports the check: one id for a job of the workflow itself, the calling job's id first for a job of a called workflow.
-- # Class: GhaRequiredStatusCheck_skip_conditions
--     * Slot: GhaRequiredStatusCheck_check_uri Description: Autocreated FK slot
--     * Slot: skip_conditions Description: What in the workflow can skip the job that reports the check, each written as its key's path in the file, such as `on.pull_request.paths` or `jobs.test.if`.

CREATE TABLE "GhaDocument" (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_GhaDocument_id" ON "GhaDocument" (id);

CREATE TABLE "GhaRequiredMixin" (
	id INTEGER NOT NULL,
	required BOOLEAN,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_GhaRequiredMixin_id" ON "GhaRequiredMixin" (id);

CREATE TABLE "GhaInput" (
	id INTEGER NOT NULL,
	description TEXT,
	input_id TEXT NOT NULL,
	"default" TEXT,
	required BOOLEAN,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_GhaInput_id" ON "GhaInput" (id);

CREATE TABLE "GhaOutput" (
	id INTEGER NOT NULL,
	description TEXT,
	output_expression TEXT,
	output_id TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_GhaOutput_id" ON "GhaOutput" (id);

CREATE TABLE "GhaWorkflow" (
	workflow_uri TEXT NOT NULL,
	workflow_path TEXT NOT NULL,
	workflow_repository TEXT,
	"GhaDocument_id" INTEGER,
	PRIMARY KEY (workflow_uri),
	FOREIGN KEY("GhaDocument_id") REFERENCES "GhaDocument" (id)
);
CREATE INDEX "ix_GhaWorkflow_workflow_uri" ON "GhaWorkflow" (workflow_uri);

CREATE TABLE "GhaReusableWorkflow" (
	workflow_uri TEXT NOT NULL,
	workflow_path TEXT NOT NULL,
	workflow_repository TEXT,
	"GhaDocument_id" INTEGER,
	PRIMARY KEY (workflow_uri),
	FOREIGN KEY("GhaDocument_id") REFERENCES "GhaDocument" (id)
);
CREATE INDEX "ix_GhaReusableWorkflow_workflow_uri" ON "GhaReusableWorkflow" (workflow_uri);

CREATE TABLE "GhaAction" (
	action_uri TEXT NOT NULL,
	action_path TEXT NOT NULL,
	"using" VARCHAR(9) NOT NULL,
	"GhaDocument_id" INTEGER,
	PRIMARY KEY (action_uri),
	FOREIGN KEY("GhaDocument_id") REFERENCES "GhaDocument" (id)
);
CREATE INDEX "ix_GhaAction_action_uri" ON "GhaAction" (action_uri);

CREATE TABLE "GhaRepositoryRuleset" (
	ruleset_uri TEXT NOT NULL,
	ruleset_id INTEGER,
	ruleset_source_type VARCHAR(12),
	ruleset_source TEXT,
	ruleset_target VARCHAR(6) NOT NULL,
	enforcement VARCHAR(8) NOT NULL,
	"GhaDocument_id" INTEGER,
	PRIMARY KEY (ruleset_uri),
	FOREIGN KEY("GhaDocument_id") REFERENCES "GhaDocument" (id)
);
CREATE INDEX "ix_GhaRepositoryRuleset_ruleset_uri" ON "GhaRepositoryRuleset" (ruleset_uri);

CREATE TABLE "GhaWorkflowJob" (
	id INTEGER NOT NULL,
	job_id TEXT NOT NULL,
	job_name TEXT,
	calls TEXT,
	runner_group TEXT,
	runner_environment VARCHAR(13),
	"GhaWorkflow_workflow_uri" TEXT,
	"GhaReusableWorkflow_workflow_uri" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("GhaWorkflow_workflow_uri") REFERENCES "GhaWorkflow" (workflow_uri),
	FOREIGN KEY("GhaReusableWorkflow_workflow_uri") REFERENCES "GhaReusableWorkflow" (workflow_uri)
);
CREATE INDEX "ix_GhaWorkflowJob_id" ON "GhaWorkflowJob" (id);

CREATE TABLE "GhaWorkflowInput" (
	id INTEGER NOT NULL,
	input_type VARCHAR(7) NOT NULL,
	description TEXT,
	input_id TEXT NOT NULL,
	"default" TEXT,
	required BOOLEAN,
	"GhaReusableWorkflow_workflow_uri" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("GhaReusableWorkflow_workflow_uri") REFERENCES "GhaReusableWorkflow" (workflow_uri)
);
CREATE INDEX "ix_GhaWorkflowInput_id" ON "GhaWorkflowInput" (id);

CREATE TABLE "GhaWorkflowOutput" (
	id INTEGER NOT NULL,
	description TEXT,
	output_expression TEXT NOT NULL,
	output_id TEXT NOT NULL,
	"GhaReusableWorkflow_workflow_uri" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("GhaReusableWorkflow_workflow_uri") REFERENCES "GhaReusableWorkflow" (workflow_uri)
);
CREATE INDEX "ix_GhaWorkflowOutput_id" ON "GhaWorkflowOutput" (id);

CREATE TABLE "GhaWorkflowSecret" (
	id INTEGER NOT NULL,
	description TEXT,
	secret_id TEXT NOT NULL,
	required BOOLEAN,
	"GhaReusableWorkflow_workflow_uri" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("GhaReusableWorkflow_workflow_uri") REFERENCES "GhaReusableWorkflow" (workflow_uri)
);
CREATE INDEX "ix_GhaWorkflowSecret_id" ON "GhaWorkflowSecret" (id);

CREATE TABLE "GhaActionInput" (
	id INTEGER NOT NULL,
	deprecation_message TEXT,
	description TEXT NOT NULL,
	input_id TEXT NOT NULL,
	"default" TEXT,
	required BOOLEAN,
	"GhaAction_action_uri" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("GhaAction_action_uri") REFERENCES "GhaAction" (action_uri)
);
CREATE INDEX "ix_GhaActionInput_id" ON "GhaActionInput" (id);

CREATE TABLE "GhaActionOutput" (
	id INTEGER NOT NULL,
	description TEXT NOT NULL,
	output_expression TEXT,
	output_id TEXT NOT NULL,
	"GhaAction_action_uri" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("GhaAction_action_uri") REFERENCES "GhaAction" (action_uri)
);
CREATE INDEX "ix_GhaActionOutput_id" ON "GhaActionOutput" (id);

CREATE TABLE "GhaBypassActor" (
	id INTEGER NOT NULL,
	actor_id INTEGER,
	actor_type TEXT NOT NULL,
	bypass_mode TEXT,
	"GhaRepositoryRuleset_ruleset_uri" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("GhaRepositoryRuleset_ruleset_uri") REFERENCES "GhaRepositoryRuleset" (ruleset_uri)
);
CREATE INDEX "ix_GhaBypassActor_id" ON "GhaBypassActor" (id);

CREATE TABLE "GhaRequiredStatusCheck" (
	check_uri TEXT NOT NULL,
	check_context TEXT NOT NULL,
	integration_id INTEGER,
	strict_policy BOOLEAN,
	do_not_enforce_on_create BOOLEAN,
	emitted_by TEXT,
	"GhaDocument_id" INTEGER,
	PRIMARY KEY (check_uri),
	FOREIGN KEY(emitted_by) REFERENCES "GhaWorkflow" (workflow_uri),
	FOREIGN KEY("GhaDocument_id") REFERENCES "GhaDocument" (id)
);
CREATE INDEX "ix_GhaRequiredStatusCheck_check_uri" ON "GhaRequiredStatusCheck" (check_uri);

CREATE TABLE "GhaWorkflow_triggers" (
	"GhaWorkflow_workflow_uri" TEXT,
	triggers TEXT NOT NULL,
	PRIMARY KEY ("GhaWorkflow_workflow_uri", triggers),
	FOREIGN KEY("GhaWorkflow_workflow_uri") REFERENCES "GhaWorkflow" (workflow_uri)
);
CREATE INDEX "ix_GhaWorkflow_triggers_GhaWorkflow_workflow_uri" ON "GhaWorkflow_triggers" ("GhaWorkflow_workflow_uri");
CREATE INDEX "ix_GhaWorkflow_triggers_triggers" ON "GhaWorkflow_triggers" (triggers);

CREATE TABLE "GhaWorkflow_permissions" (
	"GhaWorkflow_workflow_uri" TEXT,
	permissions TEXT,
	PRIMARY KEY ("GhaWorkflow_workflow_uri", permissions),
	FOREIGN KEY("GhaWorkflow_workflow_uri") REFERENCES "GhaWorkflow" (workflow_uri)
);
CREATE INDEX "ix_GhaWorkflow_permissions_permissions" ON "GhaWorkflow_permissions" (permissions);
CREATE INDEX "ix_GhaWorkflow_permissions_GhaWorkflow_workflow_uri" ON "GhaWorkflow_permissions" ("GhaWorkflow_workflow_uri");

CREATE TABLE "GhaReusableWorkflow_triggers" (
	"GhaReusableWorkflow_workflow_uri" TEXT,
	triggers TEXT NOT NULL,
	PRIMARY KEY ("GhaReusableWorkflow_workflow_uri", triggers),
	FOREIGN KEY("GhaReusableWorkflow_workflow_uri") REFERENCES "GhaReusableWorkflow" (workflow_uri)
);
CREATE INDEX "ix_GhaReusableWorkflow_triggers_GhaReusableWorkflow_workflow_uri" ON "GhaReusableWorkflow_triggers" ("GhaReusableWorkflow_workflow_uri");
CREATE INDEX "ix_GhaReusableWorkflow_triggers_triggers" ON "GhaReusableWorkflow_triggers" (triggers);

CREATE TABLE "GhaReusableWorkflow_permissions" (
	"GhaReusableWorkflow_workflow_uri" TEXT,
	permissions TEXT,
	PRIMARY KEY ("GhaReusableWorkflow_workflow_uri", permissions),
	FOREIGN KEY("GhaReusableWorkflow_workflow_uri") REFERENCES "GhaReusableWorkflow" (workflow_uri)
);
CREATE INDEX "ix_GhaReusableWorkflow_permissions_permissions" ON "GhaReusableWorkflow_permissions" (permissions);
CREATE INDEX "ix_GhaReusableWorkflow_permissions_GhaReusableWorkflow_workflow_uri" ON "GhaReusableWorkflow_permissions" ("GhaReusableWorkflow_workflow_uri");

CREATE TABLE "GhaRepositoryRuleset_ref_name_include" (
	"GhaRepositoryRuleset_ruleset_uri" TEXT,
	ref_name_include TEXT,
	PRIMARY KEY ("GhaRepositoryRuleset_ruleset_uri", ref_name_include),
	FOREIGN KEY("GhaRepositoryRuleset_ruleset_uri") REFERENCES "GhaRepositoryRuleset" (ruleset_uri)
);
CREATE INDEX "ix_GhaRepositoryRuleset_ref_name_include_GhaRepositoryRuleset_ruleset_uri" ON "GhaRepositoryRuleset_ref_name_include" ("GhaRepositoryRuleset_ruleset_uri");
CREATE INDEX "ix_GhaRepositoryRuleset_ref_name_include_ref_name_include" ON "GhaRepositoryRuleset_ref_name_include" (ref_name_include);

CREATE TABLE "GhaRepositoryRuleset_ref_name_exclude" (
	"GhaRepositoryRuleset_ruleset_uri" TEXT,
	ref_name_exclude TEXT,
	PRIMARY KEY ("GhaRepositoryRuleset_ruleset_uri", ref_name_exclude),
	FOREIGN KEY("GhaRepositoryRuleset_ruleset_uri") REFERENCES "GhaRepositoryRuleset" (ruleset_uri)
);
CREATE INDEX "ix_GhaRepositoryRuleset_ref_name_exclude_GhaRepositoryRuleset_ruleset_uri" ON "GhaRepositoryRuleset_ref_name_exclude" ("GhaRepositoryRuleset_ruleset_uri");
CREATE INDEX "ix_GhaRepositoryRuleset_ref_name_exclude_ref_name_exclude" ON "GhaRepositoryRuleset_ref_name_exclude" (ref_name_exclude);

CREATE TABLE "GhaRepositoryRuleset_rule_types" (
	"GhaRepositoryRuleset_ruleset_uri" TEXT,
	rule_types TEXT,
	PRIMARY KEY ("GhaRepositoryRuleset_ruleset_uri", rule_types),
	FOREIGN KEY("GhaRepositoryRuleset_ruleset_uri") REFERENCES "GhaRepositoryRuleset" (ruleset_uri)
);
CREATE INDEX "ix_GhaRepositoryRuleset_rule_types_GhaRepositoryRuleset_ruleset_uri" ON "GhaRepositoryRuleset_rule_types" ("GhaRepositoryRuleset_ruleset_uri");
CREATE INDEX "ix_GhaRepositoryRuleset_rule_types_rule_types" ON "GhaRepositoryRuleset_rule_types" (rule_types);

CREATE TABLE "GhaWorkflowJob_runs_on" (
	"GhaWorkflowJob_id" INTEGER,
	runs_on TEXT,
	PRIMARY KEY ("GhaWorkflowJob_id", runs_on),
	FOREIGN KEY("GhaWorkflowJob_id") REFERENCES "GhaWorkflowJob" (id)
);
CREATE INDEX "ix_GhaWorkflowJob_runs_on_runs_on" ON "GhaWorkflowJob_runs_on" (runs_on);
CREATE INDEX "ix_GhaWorkflowJob_runs_on_GhaWorkflowJob_id" ON "GhaWorkflowJob_runs_on" ("GhaWorkflowJob_id");

CREATE TABLE "GhaWorkflowJob_job_permissions" (
	"GhaWorkflowJob_id" INTEGER,
	job_permissions TEXT,
	PRIMARY KEY ("GhaWorkflowJob_id", job_permissions),
	FOREIGN KEY("GhaWorkflowJob_id") REFERENCES "GhaWorkflowJob" (id)
);
CREATE INDEX "ix_GhaWorkflowJob_job_permissions_job_permissions" ON "GhaWorkflowJob_job_permissions" (job_permissions);
CREATE INDEX "ix_GhaWorkflowJob_job_permissions_GhaWorkflowJob_id" ON "GhaWorkflowJob_job_permissions" ("GhaWorkflowJob_id");

CREATE TABLE "GhaRepositoryRuleset_requires_check" (
	"GhaRepositoryRuleset_ruleset_uri" TEXT,
	requires_check_check_uri TEXT,
	PRIMARY KEY ("GhaRepositoryRuleset_ruleset_uri", requires_check_check_uri),
	FOREIGN KEY("GhaRepositoryRuleset_ruleset_uri") REFERENCES "GhaRepositoryRuleset" (ruleset_uri),
	FOREIGN KEY(requires_check_check_uri) REFERENCES "GhaRequiredStatusCheck" (check_uri)
);
CREATE INDEX "ix_GhaRepositoryRuleset_requires_check_GhaRepositoryRuleset_ruleset_uri" ON "GhaRepositoryRuleset_requires_check" ("GhaRepositoryRuleset_ruleset_uri");
CREATE INDEX "ix_GhaRepositoryRuleset_requires_check_requires_check_check_uri" ON "GhaRepositoryRuleset_requires_check" (requires_check_check_uri);

CREATE TABLE "GhaRequiredStatusCheck_job_path" (
	"GhaRequiredStatusCheck_check_uri" TEXT,
	job_path TEXT,
	PRIMARY KEY ("GhaRequiredStatusCheck_check_uri", job_path),
	FOREIGN KEY("GhaRequiredStatusCheck_check_uri") REFERENCES "GhaRequiredStatusCheck" (check_uri)
);
CREATE INDEX "ix_GhaRequiredStatusCheck_job_path_GhaRequiredStatusCheck_check_uri" ON "GhaRequiredStatusCheck_job_path" ("GhaRequiredStatusCheck_check_uri");
CREATE INDEX "ix_GhaRequiredStatusCheck_job_path_job_path" ON "GhaRequiredStatusCheck_job_path" (job_path);

CREATE TABLE "GhaRequiredStatusCheck_skip_conditions" (
	"GhaRequiredStatusCheck_check_uri" TEXT,
	skip_conditions TEXT,
	PRIMARY KEY ("GhaRequiredStatusCheck_check_uri", skip_conditions),
	FOREIGN KEY("GhaRequiredStatusCheck_check_uri") REFERENCES "GhaRequiredStatusCheck" (check_uri)
);
CREATE INDEX "ix_GhaRequiredStatusCheck_skip_conditions_skip_conditions" ON "GhaRequiredStatusCheck_skip_conditions" (skip_conditions);
CREATE INDEX "ix_GhaRequiredStatusCheck_skip_conditions_GhaRequiredStatusCheck_check_uri" ON "GhaRequiredStatusCheck_skip_conditions" ("GhaRequiredStatusCheck_check_uri");
