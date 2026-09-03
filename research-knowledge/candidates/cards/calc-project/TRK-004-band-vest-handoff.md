---
name: TRK-004-band-vest-handoff
type: calc-experience-candidate
source_plugin: calc-project
status: candidate
updated_at: 2026-08-18
---

# TRK-004: Automated spin-resolved VEST handoff

## Problem

The VASP band PBS template ended after VASPkit export.  It neither staged the
bundled VEST utility nor produced the two spin-resolved range files required by
the later explicit Wannier preparation step.

## Targeted evidence

- `scripts/vasp/run_vasp_band.pbs.template`
- `scripts/wannier/vest2.py`
- `scripts/wannier/run_wannier90.pbs.template`
- `skills/magnetic-workflow/references/magnetic-pipeline.md`
- `tests/test_pbs_input_layout.py`
- `tests/test_magnetic_workflow.py`

## Affected skills and assets

- `vasp-workflow`: band PBS runtime behavior.
- `calc-workflows`: preserved VASPkit-to-Wannier handoff ordering.
- `magnetic-workflow`: documented automated VEST handoff.
- `scripts/vasp/run_vasp_band.pbs.template`: stages and invokes VEST.

## Confirmed rule

After the existing VASPkit `21 -> 211 -> 1` band export, the band PBS requires
`band/vest2.py`, copies it into the tagged run directory, invokes VEST's
spin-range mode noninteractively, and stops unless both
`bandrange_spin0.dat` and `bandrange_spin1.dat` are nonempty.  This does not
select or modify any user-owned Wannier windows; the later explicit Wannier
preparation step remains responsible for copying the indexed VEST and band
artifacts.

## Tests

- `test_vasp_band_template_stages_and_runs_vest_for_nonempty_spin_ranges`
- `test_generated_band_layout_runs_vest_from_band_asset`
- `test_pipeline_requires_user_owned_wannier_windows`

## Status

Resolved in plugin version `0.1.0+codex.20260724054635`; cachebuster refresh is
deferred to the reliability plan's release task.
