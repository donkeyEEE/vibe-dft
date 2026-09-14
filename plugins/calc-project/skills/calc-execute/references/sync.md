# Previewed synchronization

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

`inspect` is an optional remote listing for diagnosis. `plan` defaults to pull and runs one `rsync --dry-run`; it prints the report and saves no synchronization state. Present that report for review. After the user or agent accepts it, run the matching `push` or `pull` with `--yes`. Execution reads the current configuration and filesystem directly; it does not bind itself to the earlier report or account for changes since review.

HDF5 files in every extension case, `CHGCAR`, and `WAVECAR` remain server-side. Both directions exclude `calc-sync.yaml`, `.calc-sync/`, local caches, configured patterns, and symbolic links. Transfers use no deletion mode. The helper validates the configuration and task-root location, but performs no per-file remote probes, saved-plan checks, fingerprints, expiry checks, or immutable-input comparisons.
