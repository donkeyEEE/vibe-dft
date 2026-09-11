# Reviewed synchronization

Read this reference only for remote inspection, transfer planning, or transfer of one selected task. Run every command from the calculation project root and resolve the bundled script from this skill's installed directory.

The selected task root owns `calc-sync.yaml`:

```yaml
local: 02原始数据/example/TASK-001
server: cluster:/absolute/calculation/path/TASK-001
exclude:
  - "*.tmp"
```

The mapping has exactly `local`, `server`, and `exclude`. `local` is relative to the project root, and `exclude` is a list of safe relative glob patterns. `server` combines an explicit SSH host with an absolute task root whose path components use only portable letters, digits, `.`, `_`, and `-`; shell operators, substitutions, wildcard characters, whitespace, `.` components, and `..` components are invalid. This file configures the sync tool; the Spec remains the authority for task and Run state.

Use the exact task-root configuration path:

```bash
python <calc-execute-skill-root>/scripts/sync/sync_calc_data.py validate <task-root>/calc-sync.yaml
python <calc-execute-skill-root>/scripts/sync/sync_calc_data.py inspect <task-root>/calc-sync.yaml
python <calc-execute-skill-root>/scripts/sync/sync_calc_data.py plan <task-root>/calc-sync.yaml
python <calc-execute-skill-root>/scripts/sync/sync_calc_data.py plan <task-root>/calc-sync.yaml --direction push
python <calc-execute-skill-root>/scripts/sync/sync_calc_data.py push <task-root>/calc-sync.yaml --yes
python <calc-execute-skill-root>/scripts/sync/sync_calc_data.py pull <task-root>/calc-sync.yaml --yes
```

`inspect` is an explicit remote listing for diagnosis. `plan` defaults to pull and writes `.calc-sync/reviewed-plan.json` below the task root. Present the rendered plan for review. Use `--yes` only for the direction and exact list the user approved.

The reviewed plan expires after 30 minutes and binds the flat configuration, direction, and complete file list by fingerprint. Push and pull consume that saved list directly: a missing, expired, edited, wrong-direction, or configuration-mismatched plan requires a new plan and review. Transfer-time checks may read only the exact listed paths to confirm safety and immutable Run inputs; they do not list, rebuild, or enlarge the plan.

HDF5 files in every extension case, `CHGCAR`, and `WAVECAR` remain server-side. Push also excludes `calc-sync.yaml`, `.calc-sync/`, and local caches. Transfers preserve the exact relative names, use no deletion mode, and reject traversal or symlink paths. If an approved path targets an existing file under `RUN-…/inputs/`, transfer proceeds only when the existing destination is a regular file with identical bytes. A differing input requires a new Run and a newly reviewed plan.
