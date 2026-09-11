# PBS Snapshot Checks

Read the rendered `inputs/run.sh`, `inputs/run.pbs`, cluster environment, and
current profile/probe evidence without modifying or executing them.

- PBS must receive `PBS_O_WORKDIR` equal to the exact Run directory, require
  that directory, name its immutable `inputs/`, private `outputs/`, and `logs/`,
  refuse nonempty outputs, source the prepared cluster environment, then work
  only in `outputs/`.
- It must copy only named prepared inputs, never guess an upstream Run or read
  task-level inputs, and write command evidence beneath `logs/`. The job must
  leave `inputs/` unchanged and require the task's declared output products
  before success.
- Queue, nodes, processors, walltime, executable, environment, and any backend
  resource values must match the current Spec, project profile, intended
  submission environment, and authorization scope. A generic historical
  default is not evidence.
- `run.sh submit` must verify the unchanged reviewed snapshot and submit the
  exact `inputs/run.pbs` from the Run directory. Preparation or validation
  during submit, destructive flags, cancellation, or output reuse blocks.

If a resource choice, environment repair, script edit, or authorization is
needed, return `block` to its owner. Review never performs the action.
