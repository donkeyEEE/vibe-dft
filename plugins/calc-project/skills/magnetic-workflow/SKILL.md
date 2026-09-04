---
name: magnetic-workflow
description: Prepare, validate, or document the magnetic VASP-to-Wannier90-to-TB2J-to-VAMPIRE scientific workflow. Use when a spin-polarized magnetic pipeline spans these stages; do not use for unrelated VASP, DMFT, or remote-sync work.
---

# Magnetic Workflow

Own the complete magnetic pipeline after `calc-workflows` routes a confirmed
VASP → Wannier90 → TB2J → VAMPIRE workflow here. `calc-task` creates the stage
tasks as a batch; this skill generates and checks their task-local files.

## Directory convention

Under the confirmed magnetic calculation line, use:

```text
00-structure/                 # structure sources and provenance; no task YAML
01-vasp-scf-<tag>/            # VASP SCF task
02-vasp-band-<tag>/           # VASP bands and VEST task
03-wannier-prerun-<tag>/      # VASP-to-Wannier interface task
04-wannier90-<tag>/           # spin-resolved Wannier90 task
05-tb2j-<tag>/                # exchange-model task
06-vampire-<tag>/             # VAMPIRE task
```

`00-structure/` keeps approved structure sources and provenance. Every `01`–`06`
directory is an independent standard `calc-task` skeleton. Put workflow purpose
and handoff summaries in the relevant task-root `README.md`; YAML remains the
task fact source.

## Stage layout and templates

Read [the magnetic pipeline](references/magnetic-pipeline.md) and [the magnetic
handoff preflight](references/magnetic-handoff-preflight.md) before generation.
Before new task preparation, read [the plugin template-copy preflight](../calc-workflows/references/template-copy-preflight.md).
The magnetic pipeline remains the method-specific parameter authority; do not
infer unconfirmed scientific settings.
When interpreting a calculation note or troubleshooting record whose stopping
condition is met, do not expand the calculation question; route any scope
expansion to `calc-workflows`.
For every stage, read `references/knowledge-source.yaml`, the plugin-local consumer
contract and `templates/INDEX.md`, then use either an accepted formal plugin template or a copied project
`calculation_templates/` baseline, then make only confirmed task changes. The
plugin source is under `templates/computation/`; read the current working tree
on each new lookup, never read or search `candidates/`, and use only the
smallest relevant formal set. If it is unavailable or malformed, warn and
continue without a plugin template; do not fall back to another knowledge location. The
template source is validated by `script-management`; this skill writes task
`inputs/`, removes `.template` from task-copy names, checks them,
and returns source, changes, generated
files, and validation evidence to `calc-workflows`.

Route VASP SCF and band stages to `vasp-workflow`. Read
[the TB2J/VAMPIRE interface](references/tb2j-vampire-interface.md) before the
VAMPIRE stage; read [reference cases](references/reference-cases.md) only when
historical evidence is requested. Apply shared PBS rules to every PBS stage.

For `02-vasp-band-<tag>/`, `vasp-workflow` runs VASPKIT band export; this skill
writes the approved plugin `scripts/wannier/vest2.py` source to `band/vest2.py`
and verifies both spin-range outputs before the Wannier handoff.
Read [energy mapping](references/energy-mapping.md) when that method is
requested. Before selecting or reviewing final spin-resolved Wannier90 windows,
read [Wannier-window selection](references/wannier-window-selection.md).

## Boundaries

- Do not assign material, cluster, moment, projection, Wannier-window, TB2J-grid,
  or VAMPIRE-sampling defaults.
- Do not change task metadata, perform remote synchronization, or submit jobs.
- Do not alter a VAMPIRE source model or treat historical cases as templates.
