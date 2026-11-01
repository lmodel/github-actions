# Reviewing a pull request with ktl-docent

Check out the pull or merge request's branch in a host whose bundle uses this schema, then give an agent that has ktl-docent installed the prompt below. It reviews the branch's workflow and action changes against what the bundle records on the default branch. Where the default branch is not `main`, put its name in place of `origin/main`.

```text
Review the checked-out branch against origin/main with ktl-docent. The baseline is origin/main, never this branch: read each concept as `git show origin/main:.lokf/knowledge/<path>` prints it, and take the changes from `git diff origin/main...HEAD`.

1. Bundle first. Read index.md as origin/main holds it, and open the concepts whose `resource` is a changed file.

2. Contract drift. For each changed reusable workflow or action, compare the concept's inputs, outputs and secrets (`input_id`, `output_id`, `secret_id`, `required`, `default`, `input_type`) with the branch's YAML. Report each renamed or removed entry, each new required input and each changed default as a change that breaks callers, and cite the concept as the baseline. For each renamed job, name the required check (`check_context`) whose name it changes.

3. Policy check. Read the policies and playbooks that the changed concepts reference or are about, such as supply-chain evidence or action pinning, and report anything the diff contradicts. Quote any open question in them that the diff touches.

4. Fall back to the source for anything the bundle does not cover, and say that you did.

5. End with the footer: the concepts used with their trust labels, what you checked at the source, and the gaps recorded. Record a Miss or a Disagreement only for what origin/main holds. A file or change that only this branch has is a review finding, not missing knowledge: the librarian picks it up once the branch merges.
```

The docent records each gap with its feedback script and never opens `.lokf/feedback.md`. [feedback-example.md](feedback-example.md) shows what one such review recorded.

A host that copies `scripts/derive.py` from a release can run the step 2 comparison by machine: `derive.py --check` on the branch exits 1 where a workflow or action file has drifted from its concept.
