---
name: calc-review
description: Review one exact prepared Calc Project Run as a transient, read-only pre-submit gate.
---

# Calc Review

Judge one exact prepared Run. Input must resolve uniquely to its task, current
Spec, complete `inputs/` snapshot, named upstream handoffs, intended submission
environment, and resource configuration. Read those authorities directly.
If the Run is not `prepared`, the snapshot is incomplete, a reference or parent
identity conflicts, or required backend or environment information cannot be
read, stop without a judgment.

## Review

1. Record the exact Run, task, Spec, input paths and byte identities, handoff
   sources, cluster/queue/resources, executable environment, and expected
   products being inspected. This record is returned in the response only; do
   not write it into the Run, Spec, Tracker, project, or a review cache.
2. Read [pre-submit checks](references/pre-submit.md) and [PBS
   checks](references/pbs.md). Load only the backend checks required by the
   prepared task:

   - VASP: [VASP](references/backends/vasp.md), plus [magnetic
     ordering](references/backends/vasp-magnetic.md) for a magnetic task.
   - DFT+DMFT: [DMFT](references/backends/dmft.md).
   - Hefei-NAMD or NAMDwithSOC: [NAMD](references/backends/namd.md).
   - Wannier90: [Wannier90](references/backends/wannier90.md).
   - TB2J: [TB2J](references/backends/tb2j.md).
   - VAMPIRE: [VAMPIRE](references/backends/vampire.md).

   Missing listed knowledge stops without a judgment. Inspect only; run no
   preparation, repair, transfer, submission, cancellation, or domain write.
3. Return exactly one of these judgments with evidence and an owner for every
   finding:

   - `pass`: the snapshot faithfully and safely implements its task and no
     finding needs attention before submission.
   - `pass_with_warnings`: findings are informational; none requires an action,
     choice, changed proposal, or new authorization before submission.
   - `block`: at least one risk requires action, choice, repair, design change,
     configuration change, or new authorization.

Route an execution repair to `$calc-execute`, a scientific or task-design issue
to `$calc-to-spec`, and a stable project/profile configuration issue to
`$calc-setup`. Return exact IDs, paths, evidence, and the unfinished action;
do not supply an unapproved scientific choice.

## Transient boundary

The judgment applies only to the exact snapshot and environment in the current
execution chain. Any input, submission script, resource, handoff, target
environment, or authoritative-task change requires another review. A direct
user invocation is diagnostic only and cannot authorize a future submission.
An unsubmitted prepared Run found in a new session is reviewed again. This
skill grants no submission authorization and performs no pre-closure review.
