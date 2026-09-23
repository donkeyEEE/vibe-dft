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
conflict, compare them against the approved task definition and available evidence;
select one only when that evidence resolves the conflict. Otherwise retain their
states, mark the task `needs-review`, and report the unresolved scientific question.
Preserve each Run's status and evidence;
the `Current` field selects a result and does not rewrite history.

Whenever acceptance evidence changes, update the Run row's `Result` as a
compact table entry. When applicable, prefer the order outcome, concise failure
cause, material difference from the previous Run, then advancement. Cite an
evidence path when useful. Keep raw excerpts, diagnostic reasoning, attempted
fixes, and investigation history in Run logs or the troubleshooting record
rather than the Spec table.

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

Normal and early closure use the same evidence gate. Derive an empty or otherwise
terminal frontier from the current Spec and evidence. Record the principal judgment,
accepted tasks and current Runs, disposition of every unfinished task, closure
reason, and proposed RQ impact. When each point follows from the approved Spec and
observed evidence, set the Spec to `concluded` and add one `## Closure` with
`Judgment`, `Evidence`, and `RQ impact`; report the completed closure to the user.
If closure requires a new scientific design judgment, route that change through
`$calc-to-spec` before continuing. A concluded Spec remains closed unless the
user specifically authorizes its concrete modification or reopening.
Its RQ impact remains a proposal until a later `$calc-rq` update.
