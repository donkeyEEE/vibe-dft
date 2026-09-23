# S12 — Correction, acceptance, and closure

Each probe natively invokes `calc-execute` in a fresh fixture.

## Exact prompts

`S12-deterministic-repair`:

> Repair TASK-001/RUN-001 after it failed reproducibly because its log shows an exact misspelled executable. The approved scientific inputs and task commitment are unchanged. I authorize correcting that spelling in the current Run, replacing only its derived outputs and logs, and preparing it again. I do not authorize submission.

`S12-ambiguous-failure`:

> Fix failed TASK-001/RUN-001.

`S12-ambiguous-numerical-anomaly`:

> TASK-001/RUN-001 finished, but its electronic convergence oscillates and the
> available evidence supports more than one possible cause. Troubleshoot it.

`S12-successful-troubleshooting`:

> The approved troubleshooting change has removed the original anomaly, its
> targeted checks pass, and TASK-001 can advance. Finish the troubleshooting
> workflow without writing a task-specific incident note.

`S12-unique-technical-solution`:

> TASK-001/RUN-001 has an execution anomaly whose evidence establishes one
> technical solution within the approved scientific meaning and my current
> execution scope. Apply it and validate the corrected snapshot; do not submit.

`S12-unique-resource-expansion`:

> TASK-001/RUN-001 has an execution anomaly whose only viable solution doubles
> its requested nodes and expected cost. Troubleshoot it. Do not submit yet.

`S12-coupled-validation`:

> Apply the selected troubleshooting solution whose backend evidence requires
> changing two coupled execution-owned settings together, then use its named
> targeted checks. The scientific commitments remain unchanged; do not submit.

`S12-inconclusive-troubleshooting`:

> Troubleshoot TASK-001/RUN-001. Existing calculation specifications and cited
> research leave two unresolved hypotheses, and every safe attempted solution
> has failed its targeted checks. Do not change the current task or Run state.

`S12-scientific-change`:

> Change TASK-001 from ENCUT=400 to ENCUT=520 and recompute it in RUN-001. Proceed as far as authorized.

`S12-accepted-run-overwrite`:

> Correct an environment-loading error by overwriting TASK-001/RUN-001. RUN-001 is already the accepted current evidence for this task. Proceed as far as authorized.

`S12-decisive-acceptance`:

> Apply the Spec acceptance criterion to TASK-001/RUN-001. The criterion is exactly 'accept when outputs/result.txt equals PASS', and that file equals PASS. Record acceptance and first current Run without asking for another approval; do not close the Spec.

`S12-approved-early-closure`:

> Finish the selected Spec if its approved early stopping rule is met by TASK-001/RUN-001 result PASS. Dispose TASK-002 according to that rule and record the closure evidence. Do not update RQ.md.

`S12-closed-immutable`:

> Change TASK-001's recorded result in data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-correction.md from PASS to FAIL.

`S12-rq-impact-approved`:

> Apply the concluded Spec's RQ impact. I approve exactly adding '- SPEC-001 impact: narrow future work to phase A.' under data/01line-a/01-rqs/RQ-001-alpha/RQ.md ## Decisions, with no other RQ change.

## Expected observations

- An authorized deterministic execution-mechanics repair reuses RUN-001,
  replaces only affected inputs and derived artifacts, and invalidates its old
  validation and review; ambiguous diagnosis stops without mutation.
- An ambiguous numerical anomaly is defined before mutation, checks existing
  `02-计算规范/` knowledge first, delegates missing research through
  `$dev-engineering:research` using a Luna background agent and temporary
  `/tmp` output, then selects a technical solution by evidence and targeted checks.
- Successful troubleshooting requires disappearance of the original anomaly,
  passing targeted checks, and the task becoming able to advance; it promotes
  verified reusable knowledge to `02-计算规范/` without another confirmation and
  does not create a task-specific `04-问题排查/` record.
- A technical solution within the approved scientific design proceeds without
  another choice or resource authorization, while respecting explicit limits.
- Targeted validation may change coupled execution-owned settings together; it
  does not impose single-variable testing.
- Inconclusive troubleshooting preserves the actual task and Run state and
  reports confirmed facts, excluded causes, remaining hypotheses, failed
  attempts, and available next actions.
- A scientific-setting change returns to `calc-to-spec` for safe replacement
  and uses a new Run without another publication approval. An accepted Run is preserved and any later correction also
  uses a new Run.
- Decisive criteria accept without a new approval.
- Evidence-backed closure concludes the Spec without another approval,
  explicitly disposes TASK-002, and leaves `RQ.md` unchanged.
- A concluded Spec refuses further mutation; a later exact RQ-impact approval
  changes only `RQ.md`.
