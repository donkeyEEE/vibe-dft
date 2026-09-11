# Simple Correction

Use this branch only when all of these facts are established:

- the failure is reproducible;
- logs, deterministic checks, or the loaded backend rules establish one direct
  root cause rather than competing diagnoses;
- the repair leaves the task's scientific commitment, DAG, acceptance, and
  stopping rule unchanged;
- the exact repair is authorized; and
- verification will occur through a new Run while every old Run is preserved.

Present the evidence, root cause, exact changed inputs or mechanics, new Run
path, and effects. A changed proposal needs new authorization. Every action the
user describes as overwrite, reuse, or recomputation remains individually
gated, but its physical implementation is still a new `RUN-NNN`; never delete,
empty, or modify an old Run to simulate overwrite.

Prepare the new Run from the current Spec and current upstream Runs. Execute
the full `prepare → validate → transient review → unchanged submit` chain under
the current concrete submission scope, then accept it only through the task's
approved criteria. A correction review does not inherit the failed Run's or a
previous snapshot's verdict.

Competing diagnoses, exploratory debugging, a proposed diagnostic task, or a
possible change to scientific commitment is not simple correction. Preserve
the evidence and stop. Route a design change to `$calc-to-spec`; when no
approved capability owns a complex technical diagnosis, report that boundary
instead of expanding this interface.
