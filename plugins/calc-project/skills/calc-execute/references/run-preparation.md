# Run preparation

Read this reference when materializing or preparing one Run. Backend references
provide the stage-specific input list and checks; this reference owns only the
common Run seam.

## Select and materialize the Run

Resolve the Spec, task, Run ID, task path, and declared upstream current Run
before writing. A Run contains `inputs/`, `outputs/`, and `logs/`; `run.sh` and
`run.pbs` live in that Run's `inputs/`. Normally allocate a new stable Run ID.
When [simple correction](simple-correction.md) selects the current Run for an
in-place repair, reuse that exact path and replace only the authorized artifacts
before preparation. Otherwise, if the target path already belongs to another
snapshot, stop rather than clearing, overwriting, or adopting it.

Render
`../assets/templates/common/run.sh.template` from its exact path. Replace these
integration points once each:

- `__FINGERPRINT_SOURCE__`: the exact, server-visible path to the owning
  `../scripts/fingerprint_run.py`. Preparation copies its bytes to
  `inputs/fingerprint_run.py` with `copy_immutable`.
- `__PREPARE_BODY__`: stage-specific server-side handoff and generation. Each
  command propagates failure with `|| return 1`.
- `__VALIDATE_BODY__`: stage-specific prerequisite and input checks. Each
  command propagates failure with `|| return 1`.

`copy_immutable SOURCE DESTINATION` is available only to the rendered prepare
body. It requires a declared regular source and an existing destination
directory below this Run's `inputs/`. It uses server-side `rsync`, preserves the
source, accepts an already identical regular destination, and rejects links or
a differing destination. An authorized in-place correction removes or replaces
the named affected destination before invoking `prepare`; the helper never
decides correction eligibility. Name every copied file; do not use a directory
glob.

Render backend assets from their exact owning paths. Templates supply structure,
not scientific choices: values and upstream identities come from the approved
current Spec and its current Runs. Keep CHGCAR, WAVECAR, and HDF5 on the server.
Prepare their declared handoffs there, before review, without downloading them.

## Prepare, validate, and hand off

Run these from the environment that owns the concrete Run:

```bash
bash /exact/task/RUN-NNN/inputs/run.sh prepare
bash /exact/task/RUN-NNN/inputs/run.sh validate
```

`prepare` may add only the declared files to its own Run's `inputs/` and must
finish before review. `validate` loads the reviewed Run-local
`inputs/cluster-env.sh`, then checks the common layout, scheduler command,
backend prerequisites, and stage-specific consistency before printing the
digest of every file below `inputs/`. Scripts and copied helpers are part of
that snapshot; nothing is excluded.

Pass the prepared Run, task, current Spec, printed digest, and intended
submission environment to `calc-review`. Its transient result is not a file.
Any input or environment change restarts validation and review.

## Recheck immediately before submission

Re-read the current Spec and confirm that each declared upstream Run is still
current. Re-run the exact environment probes from [PBS submission](pbs.md), and
read the scheduler state needed for the intended queue and resources. For a
server-only handoff, recheck the exact source path and the targeted source-file
identity established during preparation. A changed current Run, source byte,
software path, scheduler fact, resource, or submission target invalidates the
review even when the local input digest is unchanged.

Only after those rechecks, a passing review in this same execution chain, and a
submission inside the current authorization scope may `calc-execute` pass the
in-memory reviewed digest to `run.sh submit`. Submission reloads the same
reviewed Run-local `inputs/cluster-env.sh`, then verifies the complete input
digest before invoking `qsub`; an environment-loading side effect therefore
invalidates the snapshot. Environment changes still require validation and a
fresh review. A digest proves byte identity; it does not prove review or
approval.
