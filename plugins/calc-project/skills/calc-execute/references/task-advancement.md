# Task Advancement

Read this reference when deriving the frontier, accepting a task, changing a
current Run, propagating invalidation, or closing the Spec. The current Spec is
the only task/DAG/Run authority; task directories and external systems supply
evidence, not competing state.

## Derive the frontier

1. Re-read the Spec and require `Status: ready | active`, unique same-Spec task
   references, an acyclic dependency graph, permitted task and Run statuses,
   resolvable paths, and at most one current Run per task. Stop rather than
   repair a malformed or conflicting authority.
2. Re-read each referenced Run directory and the current scheduler/accounting,
   remote, log, and output state relevant to the invocation. Reconcile the
   Spec only from actual evidence. `submitted` covers queued and running work;
   scheduler disappearance without correlated completion evidence is not
   `finished`.
3. A `pending` task is ready only when every `Blocked by` task is completed and
   its `Condition` is `always` or decisively true from recorded upstream
   results. Mark a decisively false condition `skipped`. Return an ambiguous
   condition to `$calc-to-spec`. Existing `current` and `needs-review` tasks
   remain part of the frontier according to their current evidence.
4. Advance every independent ready task permitted by the user's stated work
   bound and concurrency/submission scope. Persist no computed frontier.

Set a ready Spec to `active` when its first task begins. A newly materialized
task becomes `current`; allocate its next unused `RUN-NNN`, add the concrete
relative path to the task's Runs table, and keep all earlier Run directories
and rows. Preparation, validation, review, submission, receipt, and correction
follow the sequence in `SKILL.md`.

## Accept results and select the current Run

Apply the task's current approved `Acceptance` statement to the declared Run
evidence. Decisive satisfaction completes the task without another approval.
Acceptance asks whether the Purpose received its minimum sufficient evidence,
not whether the scientific result was favorable. Do not add unrecorded quality,
convergence, or best-practice gates. Ambiguous criteria, conflicting evidence,
or a newly required scientific judgment stops acceptance and returns the exact
evidence to `$calc-to-spec`.

The first accepted Run that satisfies the current task definition may become
`Current: yes`. Replacing an existing current Run requires an explicit reason
grounded in the current definition and evidence. When multiple valid Runs
conflict, stop automatic selection. Preserve each Run's status and evidence;
the `Current` field selects a result and does not rewrite history.

After any upstream current-Run change, find every downstream task that used
the former Run:

- block an unsubmitted prepared snapshot until its dependency is rebuilt and
  reviewed;
- retain an already submitted Run and its scheduler facts, but do not
  automatically accept it against the changed dependency;
- set an already accepted downstream task to `needs-review` while preserving
  its Run evidence; and
- restore `completed` only after the current dependency and acceptance have
  been demonstrated again.

Propagate transitively through the Spec DAG. The propagation is a reasoned
update to the Spec's current task state, never a separate invalidation cache.

## Close once

Normal and early closure use the same gate. First derive an empty or otherwise
terminal frontier from the current Spec and evidence. Then present one concrete
proposal containing the principal judgment, accepted tasks and current Runs,
the disposition of every unfinished task, the closure reason, and proposed RQ
impact. Only explicit approval of this unchanged proposal permits setting the
same Spec to `concluded` and adding one `## Closure` with `Judgment`, `Evidence`,
and `RQ impact`. A concluded Spec is immutable. Its RQ impact remains a proposal
until a later, separately approved `$calc-rq` update.
