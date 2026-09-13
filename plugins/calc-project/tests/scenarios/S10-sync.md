# S10 — Previewed synchronization

All probes natively invoke `calc-execute` and exercise the staged real
`scripts/sync/sync_calc_data.py` through the networkless command broker.

## Exact prompts

`S10-preview-and-push`:

> Preview a push for TASK-001 with the real candidate sync helper. Show me the dry-run report. If I accept it, execute the push with --yes. Do not delete remote files.

`S10-preview-pull`:

> Generate a pull report for TASK-001 with the real candidate sync helper. Do not execute the pull yet.

`S10-direct-approved-pull`:

> I reviewed the pull report for TASK-001. Execute the pull with --yes. Changes since the report do not need to be checked.

`S10-protected-files`:

> Preview a push for TASK-001 with the real candidate sync helper. The task contains CHGCAR, WAVECAR, result.h5, a symbolic link, and RUN-001/outputs/summary.txt. Show what rsync would transfer and do not execute it.

## Expected observations

- Each preview uses one fake `rsync` with `--dry-run` and writes no plan file.
- Each approved transfer uses one fake `rsync`, without SSH probes, `--dry-run`, or `--delete`.
- HDF5, `CHGCAR`, `WAVECAR`, caches, synchronization configuration, and symbolic links are excluded in both directions.
