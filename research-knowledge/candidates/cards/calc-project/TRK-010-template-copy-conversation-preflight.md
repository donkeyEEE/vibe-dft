---
name: TRK-010-template-copy-conversation-preflight
type: calc-experience-candidate
source_plugin: calc-project
status: candidate
updated_at: 2026-08-18
---

# TRK-010: Template copy and conversation preflight

## Problem

New calculation-task inputs need a reusable, approved template source boundary
and a clear pre-submit review without treating prior task directories or their
runtime artefacts as templates. The review must keep scientific choices under
explicit user control and must not create task-local provenance metadata.

## Targeted evidence

- `skills/calc-workflows/references/template-copy-preflight.md`: authoritative
  permitted-source boundary and conversation checklist.
- `skills/calc-workflows/SKILL.md`: cross-method routing before a new task
  copy.
- `skills/vasp-workflow/SKILL.md`, `skills/dmft-workflow/SKILL.md`,
  `skills/magnetic-workflow/SKILL.md`, and `skills/namd-workflow/SKILL.md`:
  method-specific preparation routing and parameter authority.
- `tests/test_template_copy_preflight.py` and `tests/test_plugin_layout.py`:
  contract and installable-plugin-layout coverage.

## Affected skills and assets

- `calc-workflows` owns the shared copy-and-conversation preflight contract and
  the cross-stage handoff checklist items.
- `vasp-workflow`, `dmft-workflow`, `magnetic-workflow`, and `namd-workflow`
  apply the contract before new task preparation while retaining their own
  method-specific parameter authority.
- `script-management` remains the owner of reusable template-library
  maintenance; this record does not transfer that ownership.
- `calc-task` remains the source of truth for task identity, paths, and
  lifecycle metadata.

## Confirmed rule

Template files may be copied only from plugin `scripts/` and project
`calculation_templates/`; existing task directories, historical reference
cases, completed-run outputs, logs, job identifiers, caches, and remote paths
are excluded as template sources. HDF5 files, `CHGCAR`, and `WAVECAR` are a
single large-upstream-file class: a user may confirm an existing task or remote
result as the source, and the submission script copies it only on the server.
Large upstream files never enter Git, the local project, `calc-sync`, or a
template library. Only parameters explicitly confirmed by the user may change;
unconfirmed physical settings remain at the selected template value and are
shown as unchanged in the conversation-only pre-submit checklist.

Before a submission script is run or recommended, Codex presents the selected
template layer and copied files, purpose and method, confirmed changes,
unchanged physical settings, task path/run tag/input snapshot, upstream
handoff-artifact availability (including each required large file's source,
purpose, target, and presence check), scheduler/PBS pairing, and expected-output
acceptance condition, then obtains explicit user confirmation. The checklist is
not written into a task directory and creates no provenance file, manifest,
task-YAML field, or task-local source record.

## Verification

Completed successfully:

```text
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -q tests/test_template_copy_preflight.py tests/test_plugin_layout.py
# 4 passed in 0.07s

python3 /home/donk/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py calc-project
# Plugin validation passed: calc-project
```

## Status

Resolved in the plugin source. No cachebuster update or plugin reinstall
occurred. This record does not modify remote tasks, task data, or task-local
provenance.

## Versions

- First recorded: `0.1.0+codex.20260803010142`
- Last verified: implemented in dev (not yet released)
