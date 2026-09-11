---
name: calc-execute
description: Execute one selected ready or active Calc Project Spec by preparing, reviewing, submitting, tracking, synchronizing, and accepting its Runs.
---

# Calc Execute

Advance one whole ready or active Spec. Resolve one exact Spec through its RQ
and configured Tracker location, or use the exact path supplied by the caller.
Do not resolve a bare, parentless Spec ID by repository scanning. Read the
current Spec, its referenced task and Run paths, stable project configuration,
software profile, current scheduler/accounting state, and relevant remote
files before deciding what can advance. A missing or conflicting authority
stops the affected action; do not repair it through a parallel state file.

Before any mutation or advancement, read the concrete RQ, Spec, task, and Run
records used by that action and require their needed document shape. The RQ has
`ID`, `Status: active | concluded`, and `Question`, `Boundary`, `Success
Criterion`, `Decisions`, and `Specs`. The Spec has `ID`, `Status: ready | active`,
`RQ`, `Judgment`, and `Tasks`. Each task has `Status`, `Path`, `Blocked by`,
`Condition`, `Purpose`, `Acceptance`, and `Runs`; task status is `pending |
current | completed | skipped | cancelled | needs-review`, dependencies name
same-Spec tasks and are acyclic, conditions use recorded upstream results, and
paths follow the configured relative-path convention. Each recorded Run row has
Run ID, `Status`, `Current`, `Path`, and `Result`; Run status is `prepared |
submitted | finished | failed | cancelled`, `Current` is `yes | no`, and a task
has at most one current Run. A closure action additionally requires the current
task dispositions and the proposed `Closure` fields defined below. This is a
direct pre-action check of the named authorities, not a general schema validator.

If that check fails, make no affected mutation and report the specific missing
or conflicting field, document, and task or Run. Identify the owner: RQ shape
belongs to `$calc-rq`; Judgment, DAG, task declarations, conditions, and
acceptance belong to `$calc-to-spec`; execution status, Run records, and current
Run designation belong here; stable project configuration belongs to
`$calc-setup`. Do not silently supply a missing value or translate an invalid
status. An ordinary read-only status diagnostic may still report the facts that
are present and the malformed authority, but it writes nothing and does not
advance the Spec.

The Spec is the sole authority for its task graph, statuses, Run records,
current Runs, acceptance, execution record, and closure. Derive the ready
frontier from it on demand with [task advancement](references/task-advancement.md);
persist no frontier, review result, task metadata, Run metadata, workflow
record, or session cache. Independent ready tasks may advance in parallel when
the user's current bounds and submission authorization permit it. A false
condition makes a task `skipped`; an ambiguous condition or scientific
criterion returns to `$calc-to-spec` without guessing.

## Run sequence

For each frontier task, allocate a new stable Run ID and path under that task.
Materialize only the approved task path and the new Run's `inputs/`, `outputs/`,
and `logs/`; preserve every older Run. Read [Run
preparation](references/run-preparation.md) while preparing it and [PBS
execution](references/pbs.md) while rendering or validating its PBS script.
Select the exact backend bundle below and render scientific inputs only from
the current approved Spec plus the explicitly named project sources. A source
instruction supplies mechanics, never missing scientific values and never an
override of the Spec.

Run `inputs/run.sh prepare`, then `inputs/run.sh validate`, recheck the intended
submission environment and every named upstream current Run, and invoke
`$calc-review` on that exact prepared snapshot. Review is transient: continue
to submission only for `pass` or `pass_with_warnings` returned in this same
execution chain, with byte-identical inputs, unchanged resources and target
environment, and a concrete submission authorization that covers this Run.
Report warnings. A changed snapshot or environment requires validation and a
fresh review. A direct diagnostic review or a review from another session is
never submission authorization.

A submission scope may bound cluster, queue, resources or cost, eligible
tasks, concurrency, and validity. Display and obtain approval for the concrete
submission when no existing scope covers it; approval for synchronization or
a different proposal does not apply. After `submit`, capture the actual
scheduler response and job identity in the Run logs and update the Spec Run row
to `submitted` only from that evidence. A digest proves byte identity, not
review or authorization.

For upload or result synchronization, read [reviewed
synchronization](references/sync.md) and consume only its current reviewed plan.
For tracking and receipt, read [remote
completion](references/remote-completion.md); queue disappearance alone is not
success. Correlate scheduler/accounting evidence, logs, expected products, and
timestamps, then synchronize only reviewed lightweight outputs. Keep HDF5,
`CHGCAR`, and `WAVECAR` server-side. Record concise actual Run evidence in the
Spec and set the Run to `finished`, `failed`, or `cancelled` only when current
evidence supports it; never claim a remote cancellation that did not occur.

Apply the approved task acceptance rule through [task
advancement](references/task-advancement.md). Use [simple
correction](references/simple-correction.md) only at its narrow evidence and
authorization seam; correction and every overwrite-style recomputation use a
new preserved Run. If the frontier becomes empty, propose closure only when
the current Spec justifies it. Present the principal judgment, accepted task
and Run evidence, disposition of every remaining task, closure reason, and
proposed RQ impact. Only explicit approval of that exact proposal permits the
single immutable `concluded`/`## Closure` write. Later formal RQ impact is a
separate `$calc-rq` proposal and approval.

Stop for a required approval, an explicit pause, a complex diagnosis or design
change, an unjustified empty frontier, or while awaiting external work unless
the invocation is an active monitoring request. A later invocation resumes
from the same current authorities and external state.

## Exact backend bundles

For a backend branch, load exactly its row below. Stop if any listed file is missing; do not scan the backend directory or substitute a related file.

| Branch | Exact bundle |
|---|---|
| `vasp-scf` | `vasp/common.md`, `vasp/scf.md` |
| `vasp-band` | `vasp/common.md`, `vasp/band.md`, `vasp/handoff.md` |
| `vasp-wannier-prerun` | `vasp/common.md`, `vasp/wannier-prerun.md`, `vasp/handoff.md` |
| `vasp-mae` | `vasp/common.md`, `vasp/mae.md`, `vasp/handoff.md` |
| `dmft` | `dmft/common.md` |
| `dmft-postprocessing` | `dmft/common.md`, `dmft/postprocessing.md` |
| `namd` | `namd/common.md` |
| `namdwithsoc` | `namd/common.md`, `namd/namdwithsoc.md` |
| `wannier90` | `wannier90/common.md` |
| `tb2j` | `tb2j/common.md` |
| `vampire` | `vampire/common.md`, `vampire/handoff.md` |

The backend reference names each exact template, helper, handoff source, required product, and stage-specific body inserted into the common `run.sh.template`. Every inserted command propagates failure with `|| return 1`. Preparation writes only the new Run; PBS reads immutable `inputs/`, works in `outputs/`, and writes command logs in `logs/`. Preserve older Runs and refuse a nonempty output directory instead of deleting or overwriting products.

## Sibling boundaries

Return an execution repair to this skill and review the repaired new snapshot
again. Carry exact project, RQ, Spec, task, and Run identities and paths plus
the unfinished action when recommending a sibling. Carry no unapproved
scientific inference. Send a design change or ambiguous acceptance to
`$calc-to-spec`, a stable configuration gap to `$calc-setup`, and separately
approved closure impact to `$calc-rq`. Recommend siblings rather than invoking
them automatically unless the user explicitly authorized that concrete chain.
