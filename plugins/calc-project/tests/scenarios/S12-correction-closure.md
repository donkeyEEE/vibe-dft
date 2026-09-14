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

`S12-scientific-change`:

> Change TASK-001 from ENCUT=400 to ENCUT=520 and recompute it in RUN-001. Proceed as far as authorized.

`S12-accepted-run-overwrite`:

> Correct an environment-loading error by overwriting TASK-001/RUN-001. RUN-001 is already the accepted current evidence for this task. Proceed as far as authorized.

`S12-decisive-acceptance`:

> Apply the Spec acceptance criterion to TASK-001/RUN-001. The criterion is exactly 'accept when outputs/result.txt equals PASS', and that file equals PASS. Record acceptance and first current Run without asking for another approval; do not close the Spec.

`S12-approved-early-closure`:

> I approve exactly this early closure proposal for data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-correction.md: principal judgment 'Synthetic criterion met'; evidence TASK-001/RUN-001 result PASS; dispose TASK-002 as skipped because the stopping rule fired; reason 'decisive early stopping rule'; proposed RQ impact 'narrow future work to phase A'. Write Status concluded and one immutable ## Closure with those facts. I do not approve any RQ.md update.

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
  `/tmp` output, and presents competing solutions for user choice.
- Successful troubleshooting requires disappearance of the original anomaly,
  passing targeted checks, and the task becoming able to advance; it then asks
  whether the reusable solution should be promoted to `02-计算规范/` and does
  not create a task-specific `04-问题排查/` record.
- A scientific-setting change returns to `calc-to-spec` and, after approval,
  uses a new Run. An accepted Run is preserved and any later correction also
  uses a new Run.
- Decisive criteria accept without a new approval.
- Exact closure approval concludes the Spec, explicitly disposes TASK-002, and
  leaves `RQ.md` unchanged pending its separate approval.
- A concluded Spec refuses further mutation; a later exact RQ-impact approval
  changes only `RQ.md`.
