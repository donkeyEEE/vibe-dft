---
name: dmft-workflow
description: Prepare, modify, or validate solid_dmft/DFT+DMFT inputs, correlated subspaces, and DMFT postprocessing. Use when a task needs DMFT-specific physical settings or postprocessing; do not use for task metadata, remote synchronization, or generic VASP inputs.
---

# DMFT Workflow

Use this skill for solid_dmft-specific physical settings, correlated-subspace
integrity, and DMFT postprocessing. Use `calc-task` for metadata/routing.
`script-management` provides and validates approved template sources; this
workflow creates and validates confirmed task-local DMFT copies.

Read [the DMFT workflow reference](references/dmft-workflow.md) before changing a workflow. The current stage plan plus the project DMFT-parameter, PLO/local-orbital, and troubleshooting records are the parameter authority; do not infer settings from a generic template. Apply [shared PBS rules](../calc-workflows/references/pbs.md) if a PBS script is needed.

Before new task preparation, read [the shared template-copy preflight](../calc-workflows/references/template-copy-preflight.md).
The current stage plan and project records remain the method-specific parameter
authority; do not infer unconfirmed scientific settings.
When interpreting a calculation note or troubleshooting record whose stopping
condition is met, do not expand the calculation question; route any scope
expansion to `calc-workflows`.

## Method rules

- Establish PM/no-spin versus magnetic/spin, one-shot versus CSC scope, correlated subspace, and requested observables before editing inputs.
- Preserve the approved PLO/local-orbital basis, orbital order, projection window, double counting, interaction convention, and U/J unless the user explicitly requests a documented change.
- Use `calculation_templates/dmft-postprocessing/` for impurity spectral-function, self-energy MaxEnt, or self-energy Pade work as appropriate.
- Keep HDF5 files outside the local project, Git, and synchronization; the postprocessing template copies `../vasp.h5` only within the server work directory.
- Do not claim physical comparability across different PLO/local bases, double counting, U/J, or interaction forms without a documented rationale.

## Convergence Diagnostic

When `calc-sync` routes a post-pull convergence diagnostic request here, prepare the
task-local convergence plotting setup. The diagnostic operates on already-pulled
`conv_imp*.dat` and `observables_imp*.dat` files; HDF5 stays on the server.

Responsibilities:

1. Advise on which convergence observables to plot for the task's scope (e.g., DMFT
   iterations, impurity occupancy, double occupancy, self-energy moments).
2. Identify the project-approved convergence plotting script or template from
   `calculation_templates/dmft-postprocessing/` when available.
3. Obtain an approved source from `script-management`, then create and validate
   the confirmed task-local plotting-script copy in this workflow.
4. After plotting, verify that only lightweight outputs (PNG/SVG plots, text
   summaries) are produced and that no HDF5 was read locally.
5. Do not interpret physical convergence; present the plots and note which
   observables are shown. Physical interpretation is the user's responsibility.
