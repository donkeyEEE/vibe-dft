---
name: TRK-005-wannier-run-staging
type: calc-experience-candidate
source_plugin: calc-project
status: candidate
updated_at: 2026-08-18
---

# TRK-005: MPI-capable Wannier run staging

## Problem

The spin-resolved Wannier PBS template invoked the executable directly, did not
explicitly guard its staged plotting helpers, and accepted a run without
confirming the two generated Wannier band files and fitting plots were nonempty.

## Targeted evidence

- `scripts/wannier/run_wannier90.pbs.template`
- `scripts/common/cluster-env.sh.template`
- `scripts/common/probe-cluster-env.sh`
- `skills/calc-project-structure/references/cluster-software-profiles.md`
- `skills/magnetic-workflow/references/magnetic-pipeline.md`
- `tests/test_pbs_input_layout.py`
- `tests/test_calc_project_structure_profile.py`
- `tests/test_magnetic_workflow.py`

## Affected skills and assets

- `calc-project-structure`: documents the project-local launcher variable.
- `calc-workflows`: uses the selected launcher for each Wannier spin seed.
- `magnetic-workflow`: records helper staging and two-spin acceptance rules.
- `script-management`: retains helper staging from the immutable input snapshot.

## Confirmed rule

`WANNIER90_MPI_LAUNCHER` is a task-local profile variable that defaults to
`mpirun`. The Wannier PBS validates the launcher, invokes it for `wannier90.1`
and `wannier90.2`, verifies both staged plot helpers, and succeeds only when
both spin Hamiltonian, centre-coordinate, and band files, plus both fitting
PNGs, are nonempty. It leaves all eight user-owned Wannier window values in
`wannier-run.env`; it does not submit jobs.

## Tests

- `test_generated_wannier_template_uses_mpi_and_validates_both_spin_outputs`
- `test_generated_wannier_template_rejects_empty_two_spin_handoff_artifacts`
- `test_spin_wannier_template_preserves_handoff_artifacts_and_plots_both_spins`
- `test_cluster_environment_template_exposes_configurable_wannier_mpi_launcher`
- `test_pipeline_requires_mpi_wannier_launch_and_both_spin_fit_validation`

## Status

Resolved in plugin version `0.1.0+codex.20260724054635`; cachebuster refresh
and external reinstall are deferred to the reliability plan's release task.
