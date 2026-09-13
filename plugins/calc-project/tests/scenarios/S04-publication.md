# S04 — Spec publication

Each probe natively invokes `calc-project:calc-to-spec` in a fresh fixture.

## Exact prompts

`S04-approved-publication`:

> Run the required scientific-design interview, then publish the resulting Spec to data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-stability.md. I approve this design summary: judge synthetic stability with one unconditional SCF task; accept when outputs/result.txt records the completed stability result; stop when that task is accepted. I also approve exactly one RQ.md ## Specs entry '- [SPEC-001: Stability](specs/SPEC-001-stability.md)'.

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
  Spec represented by the approved target, design summary, and exact RQ link;
  the approval proposal displays those concise fields rather than the complete
  Markdown draft, and publication does not adopt unapproved drafts.
- Repeating identical publication leaves one link.
- A different owner at the target stops all writes.
- An incomplete scientific design leaves both the Spec target and RQ index
  unchanged and identifies `calc-to-spec` as the owner.
