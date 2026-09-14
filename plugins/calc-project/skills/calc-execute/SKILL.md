---
name: calc-execute
description: Execute one selected ready or active Calc Project Spec by preparing, reviewing, submitting, tracking, synchronizing, and accepting its Runs.
---

# Calc Execute

Advance one selected ready or active Calc Project Spec through its complete
execution lifecycle, from task advancement and Run execution to task acceptance
and Spec closure.

## Workflow

1. Read the existing Spec and the project state relevant to it. Use [task
   advancement](references/task-advancement.md) to identify every task that can
   advance now.
2. For an abnormal selected task, use
   [calculation troubleshooting](references/calculation-troubleshooting.md) to
   locate the problem; it routes a directly established execution error to
   [simple correction](references/simple-correction.md), then selects an
   eligible current Run for repair or creates a new Run only after the solution
   is selected. For a task without an anomaly, create a new Run.
3. Read [Run preparation](references/run-preparation.md) and prepare the selected
   Run with [PBS execution](references/pbs.md) and any applicable backend
   references. If stable project configuration must change, first load
   `$calc-setup` and make the change through that workflow. Treat unresolved
   software usage as an abnormal task and return to calculation troubleshooting;
   that branch owns any `$dev-engineering:research` invocation.
4. Validate the prepared Run, invoke `$calc-review` on the prepared
   snapshot. Resolve execution findings and review again as needed. Submit only
   when the review passes and the submission is within the user's current
   authorization.
5. After submission, record the scheduler response and update the Spec Run row
   to `submitted`. Read [remote completion](references/remote-completion.md),
   then start its Calculation Monitor when post-submission monitoring or
   continuation was explicitly requested. Use [previewed
   synchronization](references/sync.md) when transferring files. Choose the Run
   status from the actual situation using the definitions below.
6. Apply the task's approved Acceptance from the Spec, then continue with the
   next available task. When the Spec is complete, propose its closure and
   conclude it after the user accepts. If the RQ must then change, invoke
   `$calc-rq` and present its proposal to the user. Before returning control,
   invoke `$show-cot` with the resolved project root and the Task and Run
   handled by this execution step. Present its full project overview so the
   response names the Task at which execution ended.

## Principles

- Submission, synchronization, cancellation, increased resources or cost,
  deletion, and overwriting outside the current work scope require user
  authorization.
- A Run is `finished` when it ends normally and produces results available for
  task acceptance. It is `failed` when it ends unsuccessfully without complete
  results for task acceptance. It is `cancelled` when its execution has
  actually been cancelled and will not continue to run or write results.
- A change to scientific definition or provenance uses a new Run. When it also
  requires a Spec change, invoke `$calc-to-spec` to produce a modification
  proposal, ask the user whether to accept it, and continue only after
  acceptance.
