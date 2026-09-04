---
name: script-management
description: Maintain and validate approved calculation template assets in plugin resource, owning-skill asset, and project calculation_templates directories. Use when adding, changing, cataloging, or checking reusable input or script templates; do not use to generate task-local files or make method-specific input decisions.
---

# Calculation Template Management

Own reusable template assets, including extracting approved templates from
completed calculation workflows; do not generate task-local files.
Read `../../resources/calculation-templates/README.md` and `ACCEPTANCE.md`
before selecting, adding, or changing a plugin asset. Read the exact source from
the current working tree on every lookup. If a required source is unavailable
or malformed, report that the corresponding plugin-template option is
unavailable.

## Template assets

| Layer | Location | Scope |
|---|---|---|
| Shared plugin templates | `calc-project/resources/calculation-templates/` | Common and VASP sources with multiple workflow consumers |
| Magnetic workflow assets | `calc-project/skills/magnetic-workflow/assets/templates/` | Wannier90, TB2J, and VAMPIRE sources owned by the complete magnetic pipeline |
| Project templates | `<project>/calculation_templates/` | Project- or material-specific input and script baselines |

## Flow

1. Identify the asset layer, intended downstream workflow, scope, source path,
   and compatibility constraints.
2. Obtain explicit user confirmation before proposing, modifying, replacing,
   or removing a template.
3. Present the exact target path, method semantics, cluster assumptions, and
   executable validation, then wait for explicit user approval before changing
   a reusable plugin source.
4. Provide the approved formal source and constraints to the downstream workflow that
   will create task-local `inputs/` files.

When converting a completed workflow into a template, first read [templating from
a completed workflow](references/templating-from-completed-workflow.md). The
upstream workflow and method owner define the reusable boundary; this skill
extracts, sanitizes, records, and validates the approved asset.

## Boundaries

- Downstream software and complete workflows choose a plugin-template or
  project-template mode, create the task copy, make task-specific edits, and run
  method checks.
- Do not write task-local files, alter `calc-task.yaml`, deploy scripts, or submit
  jobs.
- Existing task copies are provenance records; never change a template to rewrite
  them.
