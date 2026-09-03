# Root Workflow Handoff Record

For a calculation line with two or more stages, its root may contain a
human-maintained `WORKFLOW.md`. This is a lightweight stage table for reviewing
relationships and handoffs; it is not a machine-parsed workflow format.

For each stage, the table records:

- stage identifier and method;
- responsible task directory, submission script, and PBS script;
- required upstream artifacts and their intended downstream use;
- artifacts that the stage must produce for later stages;
- practical output acceptance condition; and
- factual handoff status, evidence path, and any unresolved note.

Keep input snapshots immutable. The stage submission script performs the direct,
task-specific preflight for the declared upstream handoff. The PBS script accepts
the stage only after its required output artifacts pass the method-owned check.

`WORKFLOW.md` explains relationships and evidence across tasks. `calc-task.yaml`
remains the authoritative source for task paths and lifecycle state. Do not use
this record to infer scientific parameters or to schedule downstream jobs.
