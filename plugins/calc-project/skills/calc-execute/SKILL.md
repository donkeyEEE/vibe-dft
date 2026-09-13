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
2. For each selected task, create a Run or use [simple
   correction](references/simple-correction.md) to repair an eligible current
   Run. Read [Run preparation](references/run-preparation.md), [PBS
   execution](references/pbs.md), and any applicable backend references while
   preparing it. If stable project configuration must change, first load
   `$calc-setup` and make the change through that workflow. If software usage is
   uncertain, ask the user whether to start an execution-research workflow with
   `$dev-engineering:research`.
3. Prepare and validate the Run, then invoke `$calc-review` on the prepared
   snapshot. Resolve execution findings and review again as needed. Submit only
   when the review passes and the submission is within the user's current
   authorization.
4. After submission, record the scheduler response and update the Spec Run row
   to `submitted`. When post-submission monitoring or continuation was
   explicitly requested, read [Calculation
   Monitor](references/calculation-monitor.md). Use [remote
   completion](references/remote-completion.md) to track the Run and [previewed
   synchronization](references/sync.md) when transferring files. Choose the Run
   status from the actual situation using the definitions below.
5. Apply the task's approved Acceptance with [task
   advancement](references/task-advancement.md), then continue with the next
   available task. When the Spec is complete, propose its closure and conclude
   it after the user accepts. If the RQ must then change, invoke `$calc-rq` and
   present its proposal to the user.

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
