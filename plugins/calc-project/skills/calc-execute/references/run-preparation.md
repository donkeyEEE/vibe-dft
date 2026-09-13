# Run preparation

Read this reference when preparing one selected Run. It owns the common input
layout, materialization rules, and completion criterion for preparation.

## Materialize the Run inputs

Resolve the selected Run, task, current Spec, and declared upstream current Run
before writing. A Run contains `inputs/`, `outputs/`, and `logs/`; `run.sh` and
`run.pbs` live in that Run's `inputs/`. If the selected path already belongs to
another Run, stop rather than clearing, overwriting, or adopting it.

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

For a matching built-in backend, render its assets from their exact owning
paths. Templates supply structure, not scientific choices: values and upstream
identities come from the approved current Spec and its current Runs. Keep
CHGCAR, WAVECAR, and HDF5 on the server. Prepare their declared handoffs there,
as Run inputs without downloading them.

## Complete preparation

Run preparation from the environment that owns the selected Run:

```bash
bash /exact/task/RUN-NNN/inputs/run.sh prepare
```

Preparation is complete when this command succeeds and the declared Run inputs
have been materialized. Validation, review, synchronization, and submission
belong to later workflow steps.
