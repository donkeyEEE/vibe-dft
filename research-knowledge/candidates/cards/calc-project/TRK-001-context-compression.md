---
name: TRK-001-context-compression
type: calc-experience-candidate
source_plugin: calc-project
status: candidate
updated_at: 2026-08-18
---

# TRK-001: Context compression

## Status

Resolved. First recorded and last verified against plugin version
`0.1.0+codex.20260723022949`; the release cachebuster is refreshed after this
registry merge.

## Targeted evidence

- `skills/calc-task/SKILL.md`: task metadata and routing were separated from
  task-local script deployment.
- `skills/calc-workflows/references/pbs.md` and
  `skills/calc-project-structure/references/project-structure.md`: shared PBS
  runtime rules and project task-layout authority are kept distinct.
- `skills/script-management/SKILL.md`: task-local script deployment and
  provenance are the sole deployment contract.
- `scripts/maintenance/report_context_inventory.py`: post-change inventory is
  reproducible and reports skill/reference totals plus duplicated lines.

## Affected skills and assets

- Skills: `calc-project-structure`, `calc-task`, `calc-workflows`, and
  `script-management`; the method skills retain only their method-specific
  entry contracts.
- Asset: `scripts/maintenance/report_context_inventory.py`.

## Confirmed rule ownership

`calc-task` owns task metadata and routing; `calc-workflows` owns shared
workflow/PBS conventions; `calc-project-structure` owns the project task
layout; and `script-management` owns task-local script deployment and
provenance. This record preserves those approved ownership boundaries; it does
not introduce calculation parameters or a new global default.

## Tests and verification

- `tests/test_context_compression.py`
- `tests/test_calc_project_structure_profile.py`
- `tests/test_calc_plugin_maintenance.py`
- `pytest .codex/plugins/calc-project/tests -v`
- `python3 /home/donk/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .codex/plugins/calc-project`
- `python .codex/plugins/calc-project/scripts/maintenance/report_context_inventory.py --plugin-root .codex/plugins/calc-project`

## Post-change inventory

Run:

```bash
python .codex/plugins/calc-project/scripts/maintenance/report_context_inventory.py --plugin-root .codex/plugins/calc-project
```

The JSON is an approximate context inventory; token counts use character count
divided by four and are not exact model-token counts.
