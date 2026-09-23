# Calculation Troubleshooting

Read this reference for every selected task with an abnormal preparation,
validation, review, execution, numerical result, resource use, or claimed
completion. It owns the diagnostic loop from locating the anomaly through
verified disposition. The Spec remains the scientific authority, and the Run
and task retain their actual states throughout the loop.

## Locate the anomaly and define the problem

Resolve the selected Spec, task, current Run, declared upstream Runs, target
environment, and applicable backend references. Inspect the smallest relevant
set of Run inputs, validation or review findings, scheduler evidence, logs,
outputs, timestamps, and resource observations. Preserve full failed logs and
other evidence while diagnosis is active.

State the observed anomaly, what it prevents, its known scope, and the concrete
condition that must change. Distinguish an execution symptom from a scientific
result that merely differs from expectation. A request to reinterpret results
without an execution anomaly belongs outside this workflow.

If logs, deterministic checks, or loaded backend rules establish one direct
execution-only root cause, enter [simple correction](simple-correction.md).
That branch may repair an eligible current Run in place without first
presenting a solution choice. Simple correction still preserves any Run with
an active or possible writer, adopted task evidence, required provenance, or
comparison value, and it requalifies every changed snapshot before submission.

## Gather missing evidence

For a problem that is not simple correction, first inspect relevant stable
notes under the selected calculation line's `02-计算规范/`. Treat those notes as
evidence subject to the current Spec and actual Run, not as permission to copy
a past change blindly.

When those notes and the current authorities do not resolve the uncertainty,
invoke `$dev-engineering:research`. Request a `gpt-5.6-luna` background agent
and give it the exact diagnostic question, observed evidence, relevant software
and version, and scientific boundaries it must not decide. Direct its single
cited Markdown artifact to a uniquely scoped directory under `/tmp`, rather
than into the calculation project. The research skill owns source selection,
primary-source tracing, citation, and the background reading process.

Read the returned artifact and synthesize it with the task evidence. Research
can establish software behavior, input meaning, commands, environment facts,
products, or mechanical checks. It is neither a root-cause decision nor a
task-level execution plan, Spec override, scientific judgment, or external
authorization.

## Select and apply a solution

For every viable solution, relate the evidence to the suspected cause and name
the intended changes, affected Run artifacts, material risks, scientific or
cost effects, and targeted checks. When competing technical solutions remain,
choose the one best supported by evidence, then test it against the targeted checks.
Preserve alternatives and the reason for the choice in the troubleshooting record.

Technical solutions proceed within the approved scientific meaning and the
user's explicit constraints. A solution that changes a scientific commitment
or requires a Spec change goes through `$calc-to-spec` for approval. Stable
project configuration changes go through `$calc-setup`. Handle submission,
cancellation, synchronization, resource or cost changes, and cleanup as part of
the selected Spec's execution; inspect the target and impact before acting and
record the result.

Apply the selected solution through the owning execution path. Change the set
of coupled variables the diagnosis requires; calculation troubleshooting does
not impose a single-variable rule. A changed prepared snapshot loses its prior
digest, validation, and review and must pass the normal preparation,
validation, and `$calc-review` path again.

## Verify and conclude the loop

Before applying a solution, name checks that directly respond to the defined
problem. After applying it, inspect those checks and any new failure evidence.
Troubleshooting succeeds only when the original anomaly is absent, the targeted
checks pass, and the task can resume its appropriate execution lifecycle. An
extra repetition solely to establish reproducibility is not a universal
completion requirement.

If a check fails or exposes a new anomaly, preserve the evidence and loop back
to problem definition, stable notes, research, or solution selection as the
new facts require. If no safe path remains, report confirmed facts, excluded
causes, remaining hypotheses, attempted solutions, and available next actions;
leave the authoritative task and Run states truthful.

After success, report the effective solution, evidence, and applicability
boundary. When the finding is reusable and verified, write an independent stable
note under `02-计算规范/`, citing the temporary research evidence and its
applicability boundary. This workflow does not create a
task-specific record under `04-问题排查/`, and an unverified solution is never
promoted as stable calculation knowledge.
