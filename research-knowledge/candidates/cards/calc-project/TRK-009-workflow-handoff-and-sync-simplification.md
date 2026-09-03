---
name: TRK-009-workflow-handoff-and-sync-simplification
type: calc-experience-candidate
source_plugin: calc-project
status: candidate
updated_at: 2026-08-18
---

# TRK-009: Workflow handoff and sync simplification

## Problem

Multi-stage calculation lines needed a concise, human-maintained record of
stage handoffs and explicit submission/PBS responsibility boundaries. Sync
transfers also needed to consume the reviewed plan rather than independently
rebuilding it after confirmation.

## Final proposal

- Proposal ID: `PRP-009-workflow-handoff-and-sync-simplification`
- Decision: implemented after focused verification.

## Affected skills and assets

- `skills/calc-workflows/SKILL.md`,
  `skills/calc-workflows/references/workflow-handoff.md`, and
  `skills/calc-workflows/references/pbs.md`: root `WORKFLOW.md` routing and
  the shared two-script handoff boundary.
- `skills/calc-project-structure/references/project-structure.md` and
  `skills/calc-project-structure/references/workflow-template.md`: copyable
  root workflow-record guidance.
- `scripts/common/submit_run.sh.template` and the VASP, Wannier, TB2J, and
  VAMPIRE PBS templates: task-specific upstream preflight and output
  acceptance checks.
- `scripts/sync/sync_calc_data.py`, `skills/calc-sync/SKILL.md`, and
  `skills/calc-sync/references/cli.md`: persisted reviewed plans consumed by
  confirmed directional transfers.
- `tests/test_workflow_handoff.py`, `tests/test_pbs_input_layout.py`,
  `tests/test_magnetic_workflow.py`, `tests/test_sync_calc_data.py`, and
  `tests/test_plugin_layout.py`: regression coverage.

## Confirmed rules

`WORKFLOW.md` is descriptive, human-maintained handoff documentation;
`calc-task.yaml` remains authoritative for task paths and lifecycle state.
Submission scripts prepare immutable input snapshots and perform task-specific
upstream checks; PBS scripts validate required outputs and fail when acceptance
is not met. A confirmed sync transfer consumes a compatible, unexpired reviewed
plan and retains the existing non-destructive, no-HDF5 restrictions.

## Verification

Completed successfully:

```text
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -q tests/test_workflow_handoff.py tests/test_sync_calc_data.py tests/test_pbs_input_layout.py tests/test_magnetic_workflow.py tests/test_plugin_layout.py
# 17 passed in 0.15s

python3 /home/donk/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py calc-project
# Plugin validation passed: calc-project
```

## Status

Resolved in the plugin source. This record does not change remote jobs or task
data, and it makes no cachebuster, marketplace-installation, or reinstall claim.
