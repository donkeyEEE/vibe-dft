---
name: TRK-008-calculation-notes-task-matrix
type: calc-experience-candidate
source_plugin: calc-project
status: candidate
updated_at: 2026-08-18
---

# TRK-008: Concise calculation-note description and task matrix

## Problem

Material-level calculation notes can accumulate paths, scheduler facts, and
physical interpretation as disconnected bullets. When one calculation section
contains several related tasks, readers cannot reliably identify the single
parameter varied by each task, its diagnostic purpose, the expected decision,
or whether a result is merely queued, completed, or physically converged.

## Targeted evidence

- `skills/calc-project-structure/references/calculation-note-template.md`
- `skills/calc-workflows/SKILL.md`
- `skills/calc-task/SKILL.md`: task metadata is the task-level source of truth
- `skills/calc-sync/SKILL.md`: calculation notes and task boards are updated
  only from verified facts

## Proposed affected skills and assets

- `calc-project-structure`: provides the calculation-note template with the task
  matrix format and rules.
- `calc-workflows` and method workflow skills: when documenting a multi-task
  calculation campaign, require a concise task purpose before task-specific detail, and
  a task matrix for two or more related tasks.
- `calc-task`: retains `calc-task.yaml` as the source for paths and lifecycle;
  the matrix summarizes from it, never the reverse.

## Requested rule

For any material-level calculation-note section that covers two or more related
tasks, write a brief opening description followed by a concise task matrix.
The matrix must include at least: task identifier, the parameter(s) that
differ from the designated baseline, purpose, expected result or decision
criterion, and factual status. Keep physical interpretation in the
calculation note, but keep `calc-task.yaml` as the source of paths and
lifecycle state.

The rule must distinguish queued/submitted/program-completed tasks from
physically converged results, and must not label a single run as a statistical
repeat. It must not create a global scientific parameter default from one
historical campaign.

## Status

Resolved. Implemented as a template and convention update:

- `calc-project-structure` provides `references/calculation-note-template.md`
  with the task matrix format, status labels, and rules.
- `calc-workflows` requires a task purpose and matrix for multi-task note
  sections, referencing the template.
- `calc-task` retains its role as the metadata truth source (no change needed).

## Versions

- First recorded: `0.1.0+codex.20260724072220`
- Last verified: implemented in dev (not yet released)
