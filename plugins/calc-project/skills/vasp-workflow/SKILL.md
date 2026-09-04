---
name: vasp-workflow
description: Prepare, modify, or validate VASP inputs, VASPkit-dependent calculations, and plain VASP band results. Use when a task requires VASP-specific settings or PBS preparation; do not use for task metadata, remote synchronization, or non-VASP method workflows.
---

# VASP Workflow

Own VASP-specific task inputs, scripts, and checks after `calc-workflows` routes
an existing task here. Read [the VASP input checklist](references/vasp-parameters.md)
for every calculation type; read [the VASPKIT reference](references/vaspkit.md)
before a VASPKIT operation.
For directional SOC magnetocrystalline-anisotropy-energy (MAE) tasks, read [the
MAE workflow](references/mae-workflow.md).

Before new task preparation, read [the plugin template-copy preflight](../calc-workflows/references/template-copy-preflight.md).
The VASP checklist remains the method-specific parameter authority; do not infer
material or physical settings that the user has not confirmed.
When interpreting a calculation note or troubleshooting record whose stopping
condition is met, do not expand the calculation question; route any scope
expansion to `calc-workflows`.

## Template modes

- **Plugin template:** read `references/knowledge-source.yaml`, the plugin-local
  consumer contract and `templates/INDEX.md`, then select an accepted VASP or
  PBS source from `templates/computation/`,
  then write the task copy in `inputs/` with confirmed substitutions.
- **Project template:** copy an approved VASP baseline from
  `calculation_templates/`, then make only confirmed task-specific changes.

On every new lookup read the current plugin-local working tree, never read or
search `candidates/`, and load only the smallest relevant formal template set.
If optional plugin knowledge is unavailable or malformed, warn and continue without a
  plugin template; do not fall back to another knowledge location. `script-management`
validates both template layers; this skill creates the task
copies and removes `.template` from their task-copy names. Record the source,
task-level changes, generated files, and checks for
`calc-workflows` to hand back to `calc-task`.

## Method checks

1. Identify relaxation, SCF, non-self-consistent bands, SOC, directional
   SOC-MAE, DFT+U, or Wannier pre-run, then apply the approved material
   settings.
2. Check `ENCUT`, KPOINTS, `ISPIN`/`MAGMOM`, smearing, `LORBIT`, `LWAVE`, and
   `LCHARG`. For SOC check non-collinear settings; for DFT+U check species order
   and all species-indexed arrays.
3. Run VASPKIT only beside the intended `POSCAR`. Task 102 requires explicit
   `GENERATE_KPOINTS=1`; task 103 preserves prepared KPOINTS and is required for
   band calculations and Wannier pre-runs.
4. Check generated files remain in the task `inputs/`; apply common
   PBS rules and run `bash -n` for generated PBS or shell scripts.

Use `scripts/vasp/plot_vasp_band.py` only for unprojected, blank-separated
VASPKIT `BAND.dat`. Do not change task metadata, perform remote synchronization,
or submit jobs.
