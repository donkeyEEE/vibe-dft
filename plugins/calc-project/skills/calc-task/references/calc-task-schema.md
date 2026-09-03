# calc-task.yaml Schema

One task directory contains one `calc-task.yaml`.

After `calc-task` has created the task directory, README, and `inputs/`, resolve
`<calc-project-plugin-root>` from the active installed skill
and run this command from the project root. Do not assume the project contains a
`.codex/plugins/` source checkout.

```bash
python <calc-project-plugin-root>/scripts/sync/sync_calc_data.py init <task-dir>
```

`calc-task` then fills in confirmed server-path and task details. This command is
an implementation asset of `calc-task`, not a `calc-sync` workflow command.

For a new task, `inputs/` stores confirmed calculation inputs together with the
submission, PBS, and environment scripts. Each task-local `<run-tag>/` directory
stores one execution attempt's outputs and log. Do not create a new task-level
`scripts/` directory; preserve any one found in an older task as provenance.
The initializer drafts `material`, `line`, and `name` from the final three local
path segments, so project-defined calculation-line prefixes are allowed but may
require the user to correct the draft fields.

```yaml
schema_version: 1
task:
  project: <project-id>
  material: <material-id>
  line: <calculation-line>
  name: <task-id>
  description: <purpose>
paths:
  local: <workspace-relative-task-path>
  server: <host:/absolute/task/path>
status: prepared
files:
  inputs: []
  outputs: []
sync:
  exclude: ["*.h5", "*.hdf5", "*.hdf", "WAVECAR", "CHGCAR", "stdout", "stderr"]
```

Required fields are every field shown above. `paths.local` stays inside the
workspace; `paths.server` uses `host:/absolute/path` form. Index important
lightweight inputs and outputs only. Exclusions are a negative list; HDF5 is
always excluded. Do not create the legacy sync YAML.

Allowed statuses: `prepared`, `pushed`, `submitted_by_user`, `running`,
`finished`, `pulled`, and `archived`. Update a status only from confirmed or
verified evidence. Record a failed run in the task README and running note.
