# PBS submission

Read this reference when validating a Run's target environment or submitting
its exact reviewed input snapshot.

## Exact environment probes

Invoke the owner-local probe with one host and one already reviewed, read-only
remote command:

```bash
bash ../scripts/probe-run-environment.sh HOST 'REMOTE_COMMAND'
```

The probe forwards that command unchanged to `ssh`, leaves stdout visible, and
returns the SSH status. It adds no profile sourcing, executable path, or
fallback. Build each concrete command from the maintained project profile and
the rendered Run. Use these explicit command forms for retained backends,
replacing each quoted operand with the exact configured value before review:

| Target | Exact command form |
|---|---|
| PBS / Torque | `command -v qsub && command -v qstat` after any exact configured initialization included in the reviewed command |
| VASP SCF, band, Wannier pre-run, or MAE | `test -x '/configured/vasp-executable' && test -x '/configured/vaspkit-executable' && command -v mpirun` |
| DMFT | `test -x '/configured/dmft-entrypoint'` |
| Hefei-NAMD | `test -x '/configured/namd'` |
| NAMDwithSOC | `test -x '/configured/namd_soc'` |
| Wannier90 | `test -x '/configured/wannier90.x' && command -v '/configured/mpi-launcher'` |
| TB2J | `conda run -n 'configured-environment' wann2J.py --help` |
| VAMPIRE | `test -x '/configured/vampire'` |

The quoted operands above are slots, not defaults. Use the profile's literal
paths, environment name, initialization, and launcher. A missing entry stops
the Run and returns to `calc-setup`; never infer it from historical mu01 paths.
Run every command required by a multi-backend stage separately so its output
and failure ownership stay visible.

## Submission gate

The sequence is prepare, validate, transient `calc-review`, immediate mutable
environment and upstream-current-Run rechecks, then submit unchanged inputs.
Review applies only to the current execution chain. Do not persist the digest,
a review verdict, or an authorization marker in the Run.

Submit with the digest printed by this chain's successful validation:

```bash
bash /exact/task/RUN-NNN/inputs/run.sh submit "$reviewed_digest"
```

`submit` loads the reviewed Run-local environment, then recomputes the complete
`inputs/` fingerprint and refuses a missing or mismatched digest before `qsub`.
This ordering detects any input side effect from environment loading. It
performs no preparation, validation, copy, or edit of its own. It changes to the
Run directory and submits exactly `inputs/run.pbs`, routing PBS stdout and
stderr to `logs/pbs.stdout` and `logs/pbs.stderr`.

Keep qsub's returned job ID visible and record it concisely in the Spec's Run
row. A checksum is only a byte-identity guard. The selected Spec execution
request authorizes submission of a verified, reviewed Run within the user's
explicit constraints; the agent checks the actual queue, resources, cost, and
concurrency before submitting.
