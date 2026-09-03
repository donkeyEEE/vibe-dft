# Remote Completion Verification

Read this reference before pulling a task that is expected to be complete.

Confirm completion from several signals: scheduler state when available, expected output files, file modification times, and targeted `tail` or `rg` excerpts. Never infer completion from one weak signal.

If scheduler inspection is unavailable or broken, state that limitation and cross-check at least expected outputs plus targeted completion or error excerpts. Do not read long logs in full.
