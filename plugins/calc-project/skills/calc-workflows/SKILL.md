---
name: calc-workflows
description: Route cross-method calculation workflows and prepare Wannier90, shared PBS, or result packaging assets. Use when a task spans methods or needs Wannier tooling; use vasp-workflow, dmft-workflow, or namd-workflow directly for method-only work.
---

# Calculation Workflows

Own global routing and cross-method orchestration. Every new task starts with
`calc-task`, which creates its skeleton before this skill assigns downstream work.
When defining task relationships or handoffs, read the project `CONTEXT.md`; use
the standard [project context](../calc-project-structure/references/project-context.md)
only when the project file is absent.

## Orchestration contract

1. Before any new task copy, read the [template copy and conversation
   preflight](references/template-copy-preflight.md). Shared preparation helpers
   live under `../../resources/calculation-templates/common/`; the owning
   downstream workflow selects exact method templates. Confirm task IDs,
   order, dependencies, source and target assets, template
   source, target `inputs/` path, and acceptance check.
2. Route each stage to its owning workflow. Software workflows own VASP, NAMD, or
   DMFT inputs; `magnetic-workflow` owns the complete VASP → Wannier90 → TB2J →
   VAMPIRE pipeline.
3. For two or more tasks, maintain the lightweight root [workflow handoff
   record](references/workflow-handoff.md) in `WORKFLOW.md`. It records stage
   relationships, factual handoff status, and evidence; `calc-task.yaml` remains
   the fact source for identity, paths, lifecycle status, and indexes.
   Use [multi-task calculation notes](references/multi-task-notes.md) for the
   concise purpose and task matrix that accompany the workflow record.
4. Receive generated-file and validation evidence from downstream workflows, then
   route confirmed YAML, README, and `NOTE-doing.md` updates to `calc-task`.

## Calculation-note scope guard

Before recommending, creating, or submitting a new task from an existing
campaign, read the authoritative calculation note and identify its recorded
problem, decision criterion, and stopping condition. If the criterion has been
met, state that the problem is complete under the recorded condition and stop.
This notice states that the problem is complete; it does not create a report.
Do not recommend or create a broader mechanism study, validation campaign,
parameter sweep, comparison, report, or replacement next action.

Continue only for a task already required by the note, directly contradictory
new evidence, or a prerequisite strictly necessary to answer the same recorded
problem; label the applicable exception. Any other scope expansion requires
explicit user confirmation.

| Request scope | Owner |
|---|---|
| VASP input, VASPkit, VASP PBS, or bands | `vasp-workflow` |
| solid_dmft input, PBS, or postprocessing | `dmft-workflow` |
| Hefei-NAMD/NAMDwithSOC or VASP snapshot handoff | `namd-workflow` |
| Magnetic VASP → Wannier90 → TB2J → VAMPIRE pipeline | `magnetic-workflow` |
| Wannier90 or other cross-method handoff | `calc-workflows` |

## Boundaries

- `script-management` validates plugin-local and project template assets. Downstream
  workflows, not this skill or `script-management`, write task-local inputs and
  scripts from approved templates.
- When a downstream workflow writes any `*.template` asset into a task, it removes
  the `.template` suffix from the task-copy name.
- On every new template lookup, read the exact declared source from the current
  plugin tree. If it is unavailable or malformed, disable the plugin-template
  option; an independently approved project template remains valid.
- Do not create tasks, alter task YAML, or directly write method inputs or scripts.
- The root `WORKFLOW.md` is human-maintained documentation, not a machine-parsed
  format or a source of global scientific defaults.
- Read [common PBS rules](references/pbs.md) before defining a PBS-stage handoff.
- Do not perform remote synchronization. Do not submit jobs.
