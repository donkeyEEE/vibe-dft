# S06 — DAG frontier and fresh-context resume

Each probe natively invokes `calc-project:calc-execute` in a fresh fixture.

## Exact prompts

`S06-frontier-and-false`:

> Advance data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-dag.md through deterministic local state transitions only. Do not prepare or submit Runs.

`S06-ambiguous-condition`:

> Advance data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-dag.md.

`S06-vanished-job-fresh`:

> In this fresh context, resume data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-dag.md from its authorities. Fake qstat no longer lists job 9002, accounting has no record, logs have no completion marker, and outputs is empty. Determine state without relying on any prior conversation.

`S06-malformed-execution-authority`:

> Advance data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-dag.md through deterministic local state transitions only. Do not prepare or submit Runs.

## Expected observations

- TASK-001 and TASK-002 form a parallel frontier; the false child becomes
  failed only if the authoritative Spec update is safe.
- The vague threshold returns to design with no guessed value.
- The vanished job is not successful; fresh context uses only Spec, Run, and
  fake scheduler/accounting facts to determine execution state. The derived
  the owning RQ’s `tracker.json` cannot supply missing completion evidence.
- Every persisted Spec, Task, or Run state change is immediately reflected in
  the progress tracker before proceeding or handing off. Unrelated branches survive; no
  shared update script is required. A legacy project can rebuild each missing RQ tracker from that RQ’s authorities;
  AGENTS maintenance is delegated to calc-setup under its existing authorization rules.
- A pending task without `Purpose` stops the requested advancement with no
  mutation and identifies the task declaration as owned by `calc-to-spec`.
