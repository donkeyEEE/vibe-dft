# PBS Snapshot Checks

Read the rendered `inputs/run.sh`, `inputs/run.pbs`, cluster environment, and
current profile/probe evidence without modifying or executing them.

- Establish that the job is anchored to the exact Run, reads the reviewed
  immutable inputs, isolates mutable outputs and logs, refuses unsafe output
  reuse, and cannot escape into another task or Run. Equivalent script layouts
  are acceptable when they prove these properties.
- Establish that upstream inputs come only from approved named sources, command
  evidence remains attributable to the Run, reviewed inputs stay unchanged,
  and declared products are checked before success.
- Queue, nodes, processors, walltime, executable, environment, and any backend
  resource values must match the current Spec, project profile, intended
  submission environment, and the user's explicit constraints. A generic historical
  default is not evidence.
- `run.sh submit` must verify the unchanged reviewed snapshot and submit the
  exact `inputs/run.pbs` from the Run directory. Preparation or validation
  during submit, destructive flags, cancellation, or output reuse prevents
  submission.
