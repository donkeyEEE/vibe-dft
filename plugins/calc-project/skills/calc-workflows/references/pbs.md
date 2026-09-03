# PBS Runtime Rules for This Project

Read this reference only when creating or modifying a PBS script. Task layout,
environment probing, and submission-wrapper requirements belong to the
contributing project's `AGENTS.md` task-layout contract.

## Two-script handoff contract

The submission script validates the task-level immutable `inputs/` sources and
prepares the named `<run-tag>/` output directory. Before calling `qsub`, it
performs direct, task-specific checks that the upstream handoff files declared
for its stage are present and usable. It does not infer physical parameters or
submit a downstream stage.

The PBS calculation script reads from task-level `inputs/`, runs in
`<task-root>/<run-tag>/`, and checks the stage's required output artifacts before
it succeeds. A passing output check prints a concise handoff-complete message; a
missing or empty required artifact results in a non-zero exit. PBS scripts never
alter task-level `inputs/`.
Method workflows own the stage-specific artifacts and acceptance decisions.

- New or modified PBS scripts default to `#PBS -q manycores`, `#PBS -l nodes=1:ppn=32`, and `#PBS -l walltime=144:00:00`.
- Resolve the task root from the PBS script, require one run tag, and execute only in `<task-root>/<run-tag>/`. Refuse an existing run-tag directory by default; `reuse` or `overwrite` requires explicit user selection, and overwrite requires immediate explicit approval.
- Keep `<task-root>/<run-tag>/output` as the sole job log; truncate it deliberately and append program stdout and stderr with `>> "$OUTPUT_FILE" 2>&1`.
- Do not use `#PBS -o`, `#PBS -e`, or `#PBS -j` scheduler redirection.
- Source task-local `inputs/cluster-env.sh` before checking or invoking software; do not rely on an implicit `~/.bashrc`.
- PBS reads only task-level `inputs/`, copies files into its run directory, and never deletes or modifies that input snapshot. Server-side preparation scripts, not PBS, read explicit upstream paths.
- Keep pre-launch checks limited to the immediate inputs and executables required by the invoked program. Do not add broad recovery or no-overwrite guards that prevent an intended rerun.
- Do not use `set -euo pipefail`; use explicit prerequisite checks and `command || exit 1` for deterministic failures.
- Formal jobs are submitted manually by the user by default. The agent may submit a new job only after explicit approval and must never cancel or alter an existing scheduler job without explicit approval.
