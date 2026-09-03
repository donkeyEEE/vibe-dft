---
name: calc-sync
description: Validate calc-task.yaml, inspect remote task state, and plan or perform non-destructive calculation-data push or pull. Use for confirmed task-path synchronization; do not use for task creation, workflow input preparation, or job submission.
---

# Calculation Sync

Use this skill for online/offline calculation-data transfer configured by an
existing `calc-task.yaml`. Read [the task schema](../calc-task/references/calc-task-schema.md)
to validate the record; this skill does not create or update task metadata.
When interpreting local copies, remote copies, or task records, read the project
`CONTEXT.md`; use the standard [project context](../calc-project-structure/references/project-context.md)
only when the project file is absent.

## Core Flow

1. Read applicable project rules and the task record; confirm `paths.local` and `paths.server`. `validate` is performed internally by every remote command; run it directly when a standalone diagnostic is useful.
2. Inspect remotely with read-only commands only when the remote state needs investigation. Before a completed-task pull, read [remote completion verification](references/remote-completion.md).
3. Run `plan` (or `plan --direction push` before a push) so transfer and skipped-file lists are visible; review large files and `sync.exclude`. This writes the task-local reviewed plan required for transfer.
4. Execute push or pull only after user confirmation. A direct request to synchronize the identified task is confirmation; otherwise obtain it explicitly before `--yes`. Confirmed transfer consumes the reviewed plan; it does not inspect or rebuild a new list.
5. Verify expected local outputs and exclusions.
6. Report transfer evidence, exclusions, and unresolved uncertainty. Route verified
   results to `calc-task` so it can update task status, indexes, README, and
   `<data-root>/NOTE-doing.md`; YAML, README, and `NOTE-doing.md` remain based on
   confirmed or verified evidence only.

## Conditional References

- Read [sync CLI](references/cli.md) when invoking the bundled script.

## Safety

- Never use destructive sync flags such as `--delete`.
- Never sync HDF5 files.
- Always run and review a transfer plan before push or pull. It expires after 30 minutes; regenerate it if configuration changes or it expires.
- Never submit, cancel, or alter cluster jobs.
- Never read long logs in full.
- Never claim a task finished solely because it disappeared from the scheduler queue.
- Never overwrite verified project metadata with an unverified remote-state inference.
