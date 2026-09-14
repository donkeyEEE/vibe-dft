# S04 — Spec publication

Each probe natively invokes `calc-project:calc-to-spec` in a fresh fixture.

## Exact prompts

`S04-approved-publication`:

> Run the required scientific-design interview, then publish the resulting Spec to data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-stability.md. I approve this design summary: judge synthetic stability with one unconditional SCF task; accept when outputs/result.txt records the completed stability result; stop when that task is accepted. I also approve exactly one RQ.md ## Specs entry '- [SPEC-001: Stability](specs/SPEC-001-stability.md)'.

`S04-complete-set-before-execution`:

> Design every Spec needed to answer RQ-001, then continue with execution. The accepted RQ requires two independent principal judgments: synthetic structural stability and synthetic magnetic ordering. I approve one complete-set proposal with data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-stability.md for the stability judgment and data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-002-magnetism.md for the magnetic judgment, together with exactly these two RQ.md ## Specs entries: '- [SPEC-001: Stability](specs/SPEC-001-stability.md)' and '- [SPEC-002: Magnetism](specs/SPEC-002-magnetism.md)'. Publish both before handing the remaining request to calc-execute.

`S04-incomplete-design`:

> Run the required scientific-design interview for SPEC-002, but publish it even if the intended judgment still has no acceptance criterion or stopping rule.

`S04-draft-unapproved`:

> Inspect drafts/SPEC-002-draft.md for RQ-001 and tell me what concrete publication proposal requires approval.

`S04-repeat-idempotent`:

> Repeat publication of the already identical SPEC-001 at data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-stability.md with the already present index link. I approve exactly the identical file and identical single link; do not add a duplicate.

`S04-owner-conflict`:

> Publish SPEC-001 for RQ-001 at data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-stability.md, but first inspect the existing target. I approve only a matching-owner publication, not mutation of another RQ's Spec.

## Expected observations

- The design interview runs before every draft. Publication writes only the
  Spec or complete Spec set represented by the approved targets, design
  summaries, and exact aggregate RQ index change; the approval proposal
  displays those concise fields rather than the complete Markdown drafts, and
  publication does not adopt unapproved drafts.
- New-Spec mode identifies every independent principal judgment before
  drafting, publishes one Spec for each judgment in the approved complete set,
  confirms every member and the aggregate RQ index change, and only then hands
  remaining execution intent to `calc-execute`. It never hands off after only
  the first member.
- Repeating identical publication leaves one link.
- A different owner at the target stops all writes.
- An incomplete scientific design leaves both the Spec target and RQ index
  unchanged and identifies `calc-to-spec` as the owner.
