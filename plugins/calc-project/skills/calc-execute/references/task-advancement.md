# Task Advancement

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
