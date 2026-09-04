---
name: TRK-006-runtime-reliability-final-gaps
type: calc-experience-candidate
source_plugin: calc-project
status: candidate
updated_at: 2026-08-18
---

# TRK-006: Runtime reliability final gaps

## Problem

The generic VASP template overwrote a prepared `KPOINTS` snapshot, the retained
legacy submission helper omitted the `RUN_TAG` Torque environment contract,
preflight coverage did not execute a materialized validation script, and a band
rerun could accept stale VEST spin-range files.

## Targeted evidence

- `scripts/vasp/run_vasp.pbs.template`
- `scripts/common/prepare_and_submit.sh.template`
- `scripts/common/validate_run.sh.template`
- `scripts/vasp/run_vasp_band.pbs.template`
- `tests/test_pbs_input_layout.py`

## Affected skills and assets

- `vasp-workflow`: explicit generated-KPOINTS selection only.
- `calc-workflows` and `script-management`: retained helper submits with
  `qsub -v RUN_TAG=<tag>` from task root.
- `scripts/common/validate_run.sh.template`: generated helper staging and
  substituted INCAR preflight execution.
- `scripts/vasp/run_vasp_band.pbs.template`: remove the two VEST range outputs
  before each VEST invocation, then require both current outputs to be nonempty.

## Confirmed rule

Prepared `inputs/KPOINTS` is the generic VASP default. VASPKIT task 102 runs
only when `GENERATE_KPOINTS=1` is explicitly configured. The retained
`prepare_and_submit.sh` requires a tag and exports it through Torque's `-v`
mechanism. Generated validation must fail on an undeclared INCAR mismatch.
Each band VEST invocation removes only `bandrange_spin0.dat` and
`bandrange_spin1.dat` before generating and validating fresh ranges.

## Tests

- `test_generated_generic_vasp_preserves_prepared_kpoints_by_default_and_can_generate_explicitly`
- `test_prepare_and_submit_template_runs_preparation_before_manual_qsub`
- `test_generated_validation_stages_helper_and_blocks_incar_mismatch`
- `test_generated_band_layout_rejects_stale_vest_ranges`

## Status

Resolved in the post-review plugin source; verification and cachebuster update
remain release steps.
