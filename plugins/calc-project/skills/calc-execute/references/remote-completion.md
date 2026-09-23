# Remote Completion

Read this reference after a Run is recorded as `submitted`. It owns optional
monitoring, resumption, completion assessment, and the handoff to result
synchronization.

## Start the Calculation Monitor

Start monitoring when the selected Spec's execution needs to wait for an
asynchronous job and resume afterward. The monitor is a local coordination
aid; `calc-execute` remains responsible for Run status, acceptance, and Spec
updates.

Start only after `qsub` returned the job ID and the Spec records the Run as
`submitted`. Resolve the scheduler host from project configuration, the exact
Spec and current Run paths from the current authorities, and the thread from
`CODEX_THREAD_ID`. If a required value is missing, leave monitoring inactive
and report the job ID and a manual status command.

Start `../scripts/calculation-monitor.py` as a detached local process using the
current platform's available supervisor. Prefer `systemd-run --user` when it is
available; on other platforms, select an equivalent local background mechanism.
Use an argv array, preserve the submitting process's `PATH`, discard monitor
stdout and stderr, and report the launcher that was accepted. A missing suitable
launcher leaves monitoring inactive; it does not affect the submitted job.

Pass the Python executable, owning script path, and these script arguments
separately:

```text
--host CONFIGURED_HOST
--job-id QSUB_JOB_ID
--thread-id CODEX_THREAD_ID
--spec ABSOLUTE_SPEC_PATH
--run LOCAL_AUTHORITATIVE_RUN_PATH
--message CALLER_SELECTED_MESSAGE
--interval 30
```

The local Run path must exist on the monitor machine. A monitor failure does
not change or repeat the submission.

## Wait and resume

An active monitor owns the wait. On a later invocation, inspect its local unit
before querying the remote scheduler. If it is active and the invocation has
neither its complete `PBS_JOB_LEFT_QSTAT` message nor an explicit user status
request, leave the Run waiting.

The monitor checks whether the recorded job remains visible to `qstat`. Its
`PBS_JOB_LEFT_QSTAT` message is only a wake-up signal; it does not prove that
the Run succeeded. If the monitor stops without that message, diagnose it and
check the scheduler before deciding whether to restart monitoring. Observation
failure never causes job resubmission.

## Assess completion

For the selected Run, inspect the available scheduler or accounting state,
expected products, output and log timestamps, and targeted completion or
failure excerpts. Use the actual situation to choose the Run status. Queue
disappearance alone does not establish successful completion.

Update the Spec row with the actual result and whether the task may advance.
Add a concise failure cause when failed and the material difference when a
previous Run exists. Keep scheduler transcripts, raw excerpts, and detailed
diagnosis in the Run logs or troubleshooting record, referenced by path rather
than copied into `Result`.

Keep HDF5, `CHGCAR`, and `WAVECAR` on the server. When results are ready to
transfer, read [previewed synchronization](sync.md) and follow its reviewed
transfer process.
