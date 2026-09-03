# Sync CLI

Read this reference when invoking the bundled synchronization script.

Resolve `<calc-project-plugin-root>` from the active installed skill; do not
assume that the research project contains a `.codex/plugins/` source checkout.

```bash
python <calc-project-plugin-root>/scripts/sync/sync_calc_data.py validate <task-dir>/calc-task.yaml
python <calc-project-plugin-root>/scripts/sync/sync_calc_data.py inspect <task-dir>/calc-task.yaml
python <calc-project-plugin-root>/scripts/sync/sync_calc_data.py plan <task-dir>/calc-task.yaml
python <calc-project-plugin-root>/scripts/sync/sync_calc_data.py plan <task-dir>/calc-task.yaml --direction push
python <calc-project-plugin-root>/scripts/sync/sync_calc_data.py push <task-dir>/calc-task.yaml --yes
python <calc-project-plugin-root>/scripts/sync/sync_calc_data.py pull <task-dir>/calc-task.yaml --yes
```

Every remote command validates `calc-task.yaml` internally. Use standalone
`validate` for diagnosis; use `inspect` only when a remote-state listing is
needed. `plan` defaults to a pull plan; use `--direction push` for a push plan.
It saves the validated file list under `<task-dir>/.calc-sync/reviewed-plan.json`.
That local runtime artifact is excluded from uploads and expires after 30 minutes.

Use `--yes` only after the user has approved the displayed plan. Confirmed
`push` and `pull` consume the saved reviewed plan exactly: they reject a missing,
expired, configuration-changed, or wrong-direction artifact before invoking
`rsync`, and do not independently inspect or rebuild a list. The script reports
transfer evidence but does not update task metadata.
