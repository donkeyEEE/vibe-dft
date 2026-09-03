---
name: TRK-002-flat-prepared-run-layout
type: calc-experience-candidate
source_plugin: calc-project
status: candidate
updated_at: 2026-08-18
---

# TRK-002: Flat prepared-run layout

## State

Resolved. The flat prepared-run layout is the current reusable task-layout
contract for new or explicitly migrated PBS-backed tasks.

## Evidence

- `scripts/common/prepare_run.sh.template`, `validate_run.sh.template`, and
  `submit_run.sh.template` define tag-aware preparation, validation, and one
  submission boundary.
- VASP, Wannier, WannierTools, TB2J, and VAMPIRE PBS templates resolve a
  direct `<task-root>/<run-tag>/` directory and read its `inputs/` snapshot.
- `skills/calc-project-structure/references/project-structure.md` records the
  generated-project contract.

## Confirmed rule

The user prepares key small inputs locally in `<run-tag>/inputs/`, uploads
them, then runs a server-side `prepare_run_<tag>.sh` that copies declared
large/upstream files from an explicit confirmed path without overwriting key
inputs. PBS executes only in `<run-tag>/`, removes only declared outputs and
expanded input copies, never mutates `<run-tag>/inputs/`, and writes all logs
and results into that run directory. There is no `runs/`, `temp/`, or
`manifest.yaml` layer.

## Affected skills and assets

- `calc-project-structure`, `calc-workflows`, `script-management`,
  `vasp-workflow`, `magnetic-workflow`, `dmft-workflow`, and `namd-workflow`.
- `scripts/common/`, `scripts/vasp/`, `scripts/wannier/`, `scripts/tb2j/`,
  and `scripts/vampire/`.

## Tests

- `tests/test_flat_prepared_run_layout.py`
- `tests/test_pbs_input_layout.py`
- `tests/test_magnetic_workflow.py`
- `tests/test_calc_project_structure_profile.py`

## Versions

First recorded: `0.1.0+codex.20260724014932`. Last verified: current plugin
release after the flat prepared-run template and documentation test suite.
