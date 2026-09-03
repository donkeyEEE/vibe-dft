---
name: TRK-003-incar-parameter-preflight
type: calc-experience-candidate
source_plugin: calc-project
status: candidate
updated_at: 2026-08-18
---

# TRK-003: Upstream/downstream INCAR parameter preflight

## Problem

New PBS-backed tasks could prepare a downstream input snapshot whose material
and runtime-control parameters diverged from its declared upstream calculation
without detecting the divergence before submission.

## Targeted evidence

- `scripts/common/validate_run.sh.template`
- `scripts/common/compare_incar_parameters.sh`
- `tests/test_pbs_input_layout.py`

## Affected skills and assets

- `calc-workflows`: shared validation contract.
- `vasp-workflow`: VASP INCAR compatibility contract.
- `script-management`: generated script deployment and substitution rules.
- `scripts/common/compare_incar_parameters.sh`: common preflight helper.

## Confirmed rule

Generated validation scripts must declare an upstream `INCAR` path and compare
it with `<run-tag>/inputs/INCAR` before submission. The check covers `ISPIN`,
`ISYM`, `LDAU*`, `MAGMOM`, `ENCUT`, `NBANDS`, smearing, and convergence tags.
Only explicit per-key exceptions in `__INCAR_EXCEPTIONS__` suppress a mismatch.
Historical task copies and remote jobs are not changed.

## Tests

- `test_incar_preflight_rejects_mismatched_isym_and_ispin`
- `test_incar_preflight_allows_declared_per_key_exception`
- `test_generated_validation_declares_upstream_incar_and_exceptions`
- `test_generated_validation_stages_helper_and_blocks_incar_mismatch`

## Status

Resolved in plugin version `0.1.0+codex.20260724054635`; cachebuster refresh is
deferred to the reliability plan's release task.
