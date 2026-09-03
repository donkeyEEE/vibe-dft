---
name: script-management
description: Maintain and validate approved calculation template assets in external research-knowledge and project calculation_templates directories. Use when adding, changing, cataloging, or checking reusable input or script templates; do not use to generate task-local files or make method-specific input decisions.
---

# Calculation Template Management

Own reusable template assets, including extracting approved templates from
completed calculation workflows; do not generate task-local files.
Read `references/knowledge-source.yaml`, then the configured repository's
`CONSUMER_CONTRACT.md` and `/home/donk/yz-skills/research-knowledge/templates/INDEX.md`
before selecting, adding, or changing a shared asset. Read the current working
tree on every new lookup and never read or search `candidates/` as a consumer.
If the repository or formal template is unavailable or malformed, warn and
continue without a shared template; do not use a bundled legacy copy.

## Template assets

| Layer | Location | Scope |
|---|---|---|
| Shared templates | external `research-knowledge/templates/computation/` | Reusable script and PBS template sources accepted by calc-project |
| Project templates | `<project>/calculation_templates/` | Project- or material-specific input and script baselines |

## Flow

1. Identify the asset layer, intended downstream workflow, scope, source path,
   and compatibility constraints.
2. Obtain explicit user confirmation before proposing, modifying, replacing,
   or removing a template.
3. Write proposed shared assets only to `candidates/templates/`; record method
   semantics, cluster assumptions, and executable validation for Cangjie.
4. Cangjie alone promotes an accepted candidate into the formal template tree
   and index. This skill validates without creating task copies.
4. Provide the approved source and constraints to the downstream workflow that
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
