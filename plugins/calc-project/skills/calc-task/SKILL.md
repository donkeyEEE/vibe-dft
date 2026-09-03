---
name: calc-task
description: "Manage concrete calculation-task metadata and routing through calc-task.yaml: identity, paths, status, indexes, and specialist handoffs. Use when creating, registering, or updating a specific calculation task; do not use for method-specific inputs or remote synchronization."
---

# Calculation Task

Own concrete task records and the contents of the project's data directory.
When project terminology or boundaries are relevant, read the project
`CONTEXT.md`; use the standard [project context](../calc-project-structure/references/project-context.md)
only when the project file is absent.
Read [the task schema](references/calc-task-schema.md) before creating or changing
task metadata.

## Task contract

Every new task uses this skeleton:

```text
<task>/
├── calc-task.yaml
├── README.md
└── inputs/
```

`calc-task.yaml` is the only task-level fact source. `README.md` is a concise
human summary and never overrides it. `inputs/` holds confirmed input snapshots
and task-local submission, PBS, and environment scripts. Each `<run-tag>/`
directory is one execution attempt's output and log archive. Its content belongs
to the owning downstream workflow; `script-management` maintains only the
approved templates. Existing task-level `scripts/` directories are preserved as
historical provenance and are not changed.

## Flow

1. Read project rules; confirm the data root and each task's identity, local path,
   and server path. For a batch, show the complete task and path mapping first.
2. After confirmation, create the required material, calculation-line, and task
   directories; calculation-line prefixes below the data root are project-defined.
   Create each task skeleton and README summary, then call the
   bundled `sync_calc_data.py init <task-dir>` command to generate its initial YAML.
   The initializer drafts `material`, `line`, and `name` from the final three path
   segments; correct a draft that does not match the confirmed project meaning.
3. Maintain `<data-root>/NOTE-doing.md` after creation and each verified status or
   path change. Its rows summarize task ID, local path, server path, status, and
   next action; YAML remains authoritative.
4. Route workflow dependencies and cross-method handoffs to `calc-workflows`;
   route method inputs and task-local script generation to the relevant downstream
   workflow, and route remote inspection or transfer to `calc-sync`.
5. Update YAML, README, and the running note only from confirmed or verified
   evidence. Record failures in the README and running note; do not invent a
   lifecycle status outside the schema.

## Boundaries

- `calc-workflows` may define task relationships and handoffs but never task
  identity, paths, directories, or lifecycle state.
- Do not create the project-level data-root container or change project data policy.
- Never infer an unknown server path, alter remote jobs, or move, delete, rename,
  or overwrite calculation data without explicit approval.
