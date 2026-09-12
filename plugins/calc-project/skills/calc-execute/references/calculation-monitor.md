# Calculation Monitor

Read this reference only when the current execution chain explicitly requested
post-submission monitoring or continuation after the PBS job leaves `qstat`.
The monitor is a local coordination aid; remote completion evidence and every
Spec decision remain in the ordinary `calc-execute` receipt path.

## Launch gate

Launch only after `qsub` returned the exact job ID and the authoritative Spec
records that Run as `submitted`. Resolve the scheduler host from the selected
project configuration, the exact absolute Spec and current Run paths from the
authorities just updated, and the thread only from the current
`CODEX_THREAD_ID`. Accept one caller-selected continuation message: UTF-8 and
Markdown are allowed, while NUL, credentials, and content above 16 KiB are not.

If any value is missing, report the recorded job ID and leave monitoring
inactive. A monitor failure never changes or repeats the successful submission
and is not written into the Spec.

## Transient service

The owning script is `../scripts/calculation-monitor.py`. Invoke
`systemd-run --user` with an argv array, not an evaluated shell string. Use a
unit name made only from a sanitized host and job ID and include these exact
service controls:

```text
--collect
--setenv=PATH=CURRENT_PATH
--property=StandardOutput=null
--property=StandardError=null
```

Resolve `CURRENT_PATH` in the submitting Codex process and pass it explicitly;
the systemd user manager's default PATH may not contain the active `codex`
executable.

Pass the Python executable, exact owning script path, and these script options
as separate arguments:

```text
--host CONFIGURED_HOST
--job-id QSUB_JOB_ID
--thread-id CODEX_THREAD_ID
--spec ABSOLUTE_SPEC_PATH
--run ABSOLUTE_CURRENT_RUN_PATH
--message CALLER_SELECTED_MESSAGE
--interval 30
```

After launch, report the job ID, resources, immediate scheduler state, and
whether systemd accepted the unit. When systemd or `CODEX_THREAD_ID` is
unavailable, report an exact manual status command for the submitted job.

## Waiting gate

An active monitor owns the wait. On a later invocation, inspect the local unit
before any remote scheduler call. If it is `active/running` and the invocation
contains neither its complete `PBS_JOB_LEFT_QSTAT` envelope nor an explicit
user request for current status, end the execution turn without querying PBS,
restarting the unit, or reporting another synthetic waiting update.

A persistent goal may still generate ordinary continuation turns while the
external job is running. Treat the unchanged active monitor as the same
external-state blocking condition on each such turn. Do no remote work. On the
third consecutive goal turn with that condition, use the goal status mechanism
to mark the goal `blocked`; do not leave it active and emit further waiting
messages. The monitor remains independent of the goal and continues running.
Its queued `PBS_JOB_LEFT_QSTAT` message is new input that can resume the blocked
goal and open the receipt path below.

If the unit is absent or inactive without a matching wake-up envelope, diagnose
the monitor itself and perform at most one current scheduler check before
deciding whether to restore monitoring. Never resubmit the recorded job merely
because observation stopped.

## Wake-up semantics

The monitor executes a fixed SSH query that loads `/etc/profile` before running
`qstat JOB_ID`, so configured Torque commands are available in the
non-interactive remote session. Status zero waits one interval; any nonzero
status immediately triggers one `codex queue` attempt. The monitor does not
distinguish queue disappearance from SSH, scheduler, or authentication failure
and does not query accounting.

The delivered message adds `PBS_JOB_LEFT_QSTAT`, host, job ID, exact Spec, and
exact Run before the caller-selected text. Treat it only as a wake-up signal.
On receipt, re-read the named authorities and apply
[remote completion](remote-completion.md) before synchronization, acceptance,
status change, or downstream execution.

The first version has one queue attempt and no outbox, retry, delivery state,
duplicate suppression, journal output, or closed-Codex recovery.
