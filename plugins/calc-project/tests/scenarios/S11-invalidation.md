# S11 — Current-Run invalidation

All probes natively invoke `calc-execute` in fresh contexts.

## Exact prompts

`S11-replace-upstream`:

> Replace TASK-001's current Run from RUN-001 to accepted RUN-002 for the explicit reason 'RUN-002 has the approved corrected deterministic input'.

`S11-stale-submit-refusal`:

> Submit TASK-002/RUN-001. I authorize exactly this Run on fake-cluster queue debug, one node, 32 cores, concurrency one, valid through 2030-01-01T00:00:00Z.

`S11-specific-recheck`:

> Recheck dependency validity in data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-invalidation.md after the upstream current Run change.

`S11-submitted-not-autoaccept`:

> Receive TASK-003/RUN-001 and apply the acceptance criterion recorded in data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-invalidation.md.

## Expected observations

- Replacement records the reason; prepared old-dependency work cannot submit,
  submitted output cannot auto-accept, accepted output becomes needs-review,
  and no remote cancellation is fabricated.
- Recheck restores only TASK-004; TASK-005 remains needs-review.
