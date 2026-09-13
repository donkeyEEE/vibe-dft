---
name: calc-review
description: Review one exact prepared Calc Project Run as a transient, read-only pre-submit gate.
---

# Calc Review

Judge one exact prepared Run. Input must resolve uniquely to its task, current
Spec, complete `inputs/` snapshot, named upstream handoffs, intended submission
environment, and resource configuration. Read those authorities directly and
use safe read-only inspection to resolve missing operational detail before
deciding whether the user is needed.

## Review

1. Establish enough reproducible evidence to identify the Run, task, Spec,
   reviewed bytes, handoffs, target environment, resources, and expected
   products. Choose the clearest evidence form for the risks present; no fixed
   report schema is required. Keep the review transient and write no review
   cache or authorization marker.
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

   Inspect only; the review step itself performs no preparation, repair,
   transfer, submission, cancellation, or domain write.
3. Return `pass` when the snapshot faithfully and safely implements its task,
   or `pass_with_warnings` when every observation is informational and requires
   no action or choice before submission. For any repairable defect, explain
   the evidence and unfinished action, then return control to the active
   execution flow. That flow diagnoses and repairs the defect, chooses a safe
   eligible Run, and obtains fresh validation and review before submission.

## Stop conditions

Stop and ask the user only when continuing requires one of these:

- a new scientific judgment that approved authorities cannot determine,
  including a changed structure, magnetic order, scientific parameter, method,
  provenance-bearing source, acceptance criterion, or stopping criterion;
- new external authorization for submission, enlarged resources or cost,
  synchronization, cancellation, overwrite, deletion, or another external side
  effect outside the current authorization scope;
- resolution of a concurrent writer when no wait, new Run, or other
  non-destructive path can make progress safely; or
- resolution of an authoritative object that safe inspection cannot identify
  uniquely or reconcile across the current Spec, task, Run, and named sources.

Honor an explicit user pause. Otherwise continue automatically through the
appropriate execution, configuration, or safe diagnostic path. A missing
fixed-format report, repairable snapshot defect, stale configuration, or choice
among equivalent technical implementations is not a reason to ask the user.
Choose the lowest-risk, smallest, most directly verifiable implementation that
preserves the approved scientific meaning.

## Transient boundary

The judgment applies only to the exact snapshot and environment in the current
execution chain. Any input, submission script, resource, handoff, target
environment, or authoritative-task change requires another review. A direct
user invocation is diagnostic only and cannot authorize a future submission.
An unsubmitted prepared Run found in a new session is reviewed again. This
skill grants no submission authorization and performs no pre-closure review.
