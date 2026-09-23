# Simple Correction

Use this branch for a reproducible execution failure with one direct root cause
established by logs, deterministic checks, or the loaded backend rules. The
repair must leave the Spec's scientific commitments, task commitment, DAG,
acceptance, and stopping rule unchanged.

## Choose the Run

Reuse the current Run by default when it is `prepared`, `failed`, or `finished`,
no job for it is active or may still write, and its products have not been
adopted by task acceptance and need not remain available for provenance,
evidence, or comparison. Execution-only
repairs include command spelling, environment-loading order, paths, scheduler
directives, resource-launch mechanics, generated script mechanics, and file
placement. It may also revise an execution-owned parameter selected by
`$calc-execute` when the new value remains within the same deterministic basis
and scientific meaning. An explicit Spec value and upstream identity stay
unchanged.

Create a new Run when any of these applies:

- the current Run is accepted or supplies recorded scientific evidence;
- a scientific input, method, structure, parameter, upstream identity, task
  commitment, acceptance, or stopping rule changes;
- old and corrected results must remain comparable;
- the provenance of existing products is uncertain; or
- a submitted job is active, cancellation is unconfirmed, or another process
  may write the Run.

A required Spec change is not made here. Preserve the current Run and route the
change to `$calc-to-spec`; after safe replacement, execute it in a new Run.

## Apply and requalify

Establish the evidence, root cause, exact changes, selected Run path, artifacts
that will be replaced, and effects before writing. Continue automatically when
the repair preserves the approved scientific meaning and the user's explicit
constraints. Handle submission, cancellation, resource changes, and affected
Run-local replacement through the normal execution path. Before reusing a
failed Run, record its scheduler identity and concise failure cause in the Spec
Run row, leaving detailed diagnosis in the Run logs or troubleshooting record.
After correction, record only the material difference from the prior attempt
and the current advancement decision. Then replace only the affected Run-local
inputs and derived outputs or logs needed for a clean retry. Do not touch
another Run, an accepted artifact, an approved upstream source, or the
task-level sources.

Any in-place change invalidates the Run's previous digest, validation, and
review. Prepare and validate the corrected snapshot, invoke a fresh transient
review, and submit only that unchanged reviewed snapshot. Update the same Run record from new scheduler and
result evidence, and accept it only through the unchanged approved criteria.

When the root cause is not yet established, return to [calculation
troubleshooting](calculation-troubleshooting.md) and come back once evidence
supports a correction. A possible
change to scientific commitment is not simple correction and stops only when
approved authorities cannot determine the needed scientific judgment. Preserve
evidence across the diagnostic path.
