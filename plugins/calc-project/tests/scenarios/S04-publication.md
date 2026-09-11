# S04 — Spec publication

Each probe natively invokes `calc-project:calc-to-spec` in a fresh fixture.

## Exact prompts

`S04-approved-publication`:

> Publish the approved Spec to data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-stability.md. I approve exactly this complete content: '# Stability Spec\n\nID: SPEC-001\nStatus: ready\nRQ: ../RQ.md\n\n## Judgment\nSynthetic stability.\n\n## Tasks\n\n### TASK-001: Synthetic SCF\n\nStatus: pending\nPath: TASK-001\nBlocked by:\nCondition: always\n\nPurpose: Test the recorded synthetic stability judgment.\n\nAcceptance: outputs/result.txt equals PASS.\n\n#### Runs\n\n| Run | Status | Current | Path | Result |\n|---|---|---|---|---|\n\n## Stopping rule\n\nStop after TASK-001 meets its acceptance rule.\n' and exactly one RQ.md ## Specs entry '- [SPEC-001: Stability](specs/SPEC-001-stability.md)'.

`S04-malformed-approved-publication`:

> Publish SPEC-002 to data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-002-check.md. I approve exactly this content: '# Check Spec\n\nID: SPEC-002\nStatus: ready\nRQ: ../RQ.md\n\n## Judgment\nCheck the recorded synthetic result.\n\n## Tasks\n\n### TASK-001: Check\n\nStatus: pending\nPath: TASK-001\nBlocked by:\nCondition: always\nPurpose: Check the recorded synthetic result.\n\n#### Runs\n\n| Run | Status | Current | Path | Result |\n|---|---|---|---|---|\n' and exactly one RQ.md ## Specs entry '- [SPEC-002: Check](specs/SPEC-002-check.md)'.

`S04-draft-unapproved`:

> Inspect drafts/SPEC-002-draft.md for RQ-001 and tell me what concrete publication proposal requires approval.

`S04-repeat-idempotent`:

> Repeat publication of the already identical SPEC-001 at data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-stability.md with the already present index link. I approve exactly the identical file and identical single link; do not add a duplicate.

`S04-owner-conflict`:

> Publish SPEC-001 for RQ-001 at data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-stability.md, but first inspect the existing target. I approve only a matching-owner publication, not mutation of another RQ's Spec.

## Expected observations

- Publication writes only the approved Spec and one exact RQ link; it does not
  adopt unapproved drafts.
- Repeating identical publication leaves one link.
- A different owner at the target stops all writes.
- An approved proposal missing its task `Acceptance` field leaves both the Spec
  target and RQ index unchanged and identifies `calc-to-spec` as the owner.
