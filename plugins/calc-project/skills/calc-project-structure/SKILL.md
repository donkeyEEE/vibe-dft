---
name: calc-project-structure
description: Initialize or reorganize a calculation project's stable directory skeleton, top-level documents, and data boundaries. Use for project-level structure; use calc-task for a concrete calculation task and its calc-task.yaml.
---

# Calculation Project Structure

## Core Flow

1. Read existing project rules and architecture when present.
2. For initialization or reorganization, read [project structure](references/project-structure.md)
   and the standard [project context](references/project-context.md).
3. Ask whether the user wants to invoke `matt-skills:grill-me` to align
   project-specific terms. Invoke it only after the user agrees. Confirmed
   project terms may be inserted by topic into `CONTEXT.md`'s `Language` section
   and may directly redefine the standard baseline without an override marker.
   If the skill is unavailable or declined, ask only the direct questions needed
   to resolve terms that affect the proposed structure.
4. Identify proposed project root, context, notes, data, structures, templates,
   and scripts paths; show them and obtain confirmation before writing.
5. Create or update only the approved base structure and project documents;
   preserve existing calculation data. Generate project-root `CONTEXT.md` from
   the standard baseline plus any confirmed project-specific definitions.
6. Only when the user requests a cluster software profile, create project-root
   `software-profiles.md`. Read [cluster software profiles](references/cluster-software-profiles.md),
   test every listed path or command on the target host, and record the command,
   date, and `verified` or `unavailable` result.
7. Run `git status --short` and summarize changes.


## Boundaries

- Do not create concrete task directories or `calc-task.yaml` by default; route explicit task creation to `calc-task`.
- Create `06-文献笔记/` only as an empty container; the `paper-project` plugin's `zo2notes` skill owns its internal structure and literature-note storage contract.
- If `paper-project:zo2notes` is unavailable, leave `06-文献笔记/` empty; do not infer or create an internal literature-note structure.
- Do not create or maintain README-based project indexes by default; a task-directory README is allowed when requested.
- If a proposed path is uncertain, mark it `待确认` and ask the user.
- Never silently overwrite an existing project `CONTEXT.md`; compare it with the
  proposed baseline and obtain confirmation for each intended change.
- Do not submit, cancel, or alter cluster jobs.
