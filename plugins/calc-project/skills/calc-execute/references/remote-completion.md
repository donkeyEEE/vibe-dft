# Remote Completion

Read this reference after a Run is recorded as `submitted`. It owns optional
monitoring, resumption, completion assessment, and the handoff to result
synchronization.

## Start the Calculation Monitor

Start monitoring only when the current execution chain explicitly requested
post-submission monitoring or continuation. The monitor is a local coordination
aid; `calc-execute` remains responsible for Run status, acceptance, and Spec
updates.

Start only after `qsub` returned the job ID and the Spec records the Run as
`submitted`. Resolve the scheduler host from project configuration, the exact
Spec and current Run paths from the current authorities, and the thread from
`CODEX_THREAD_ID`. If a required value is missing, leave monitoring inactive
and report the job ID and a manual status command.

Invoke `../scripts/calculation-monitor.py` through `systemd-run --user` with an
argv array. Use a unit name made from the sanitized host and job ID and include:

```text
--collect
--setenv=PATH=CURRENT_PATH
--property=StandardOutput=null
--property=StandardError=null
```

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

Resolve `CURRENT_PATH` in the submitting Codex process. The local Run path must
exist on the monitor machine. After launch, report whether systemd accepted the
unit. A monitor failure does not change or repeat the submission.

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

Keep HDF5, `CHGCAR`, and `WAVECAR` on the server. When results are ready to
transfer, read [previewed synchronization](sync.md) and follow its reviewed
transfer process.
