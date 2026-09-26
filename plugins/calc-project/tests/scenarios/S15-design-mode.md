# S15 — RQ-scoped Spec design mode

Each probe starts in a fresh context. The fixture's RQ.md is authoritative;
accepted RQ scientific decisions and Run evidence must remain unchanged.

## Exact prompts

`S15-first-entry` (RQ.md has no Spec design mode):

> Publish the next evidence-supported Spec for RQ-001. I have not chosen a Spec design mode.

`S15-first-entry-automatic` (continue S15-first-entry after the mode question):

> I choose automatic Spec design for RQ-001. After you show the complete proposed RQ.md with that single mode field added, I approve exactly that change. Continue with the next evidence-supported Spec; do not start a calculation.

`S15-explicit-collaborative` (RQ.md has no Spec design mode):

> For RQ-001, use collaborative Spec design. Show the exact RQ.md mode update, then design its next evidence-supported Spec with me. Do not publish until I approve the concrete proposal.

`S15-resume-collaborative` (RQ.md records collaborative; the earlier interview is complete):

> In this fresh context, continue the next Spec for RQ-001. Its scientific design is supported by the recorded RQ and interview answers. Show me the publication proposal.

`S15-proposal-changed` (RQ.md records collaborative; an earlier proposal was approved but the target judgment has changed):

> Publish the updated Spec for RQ-001 using my earlier approval of the old proposal.

`S15-rq-handoff` (RQ.md has no mode; calc-rq receives an approved RQ decision update and remaining Spec-design intent):

> In RQ-001, add exactly the accepted decision '- Use fixed input model A.' under Decisions; I approve the complete RQ.md proposal showing only that addition. Then advance this RQ through its next evidence-supported Spec. I have not chosen a Spec design mode.

`S15-replacement` (RQ.md records collaborative; the target active Spec has an accepted Run and another submitted Run whose job is still running):

> Replace the current scientific design of SPEC-001. Preserve its previous accepted Run. A current job is still running; show its state and the proposed handling. I have not approved cancellation or the replacement proposal.

`S15-next-spec-after-execution` (RQ.md records collaborative; prior Spec is concluded and RQ advancement was requested):

> Advance RQ-001 from its concluded Spec through the next supported judgment and calculation.

`S15-switch-mode` (RQ.md records automatic):

> Switch RQ-001 to collaborative Spec design. Show the exact RQ.md change before writing; keep existing Specs and Runs unchanged.

`S15-design-only` (RQ.md records automatic):

> Publish the next supported Spec for RQ-001, but do not execute it.

## Expected observations

- A missing mode triggers one choice between automatic (suggested default) and collaborative. No choice or RQ update approval means no design publication; silence does not select automatic. Selecting automatic and approving the exact RQ field update persists it, then permits incremental publication without an additional Spec approval.
- An explicit mode choice avoids a second mode question, but calc-rq still shows and obtains approval for the exact RQ.md update before recording it. The choice persists across fresh contexts and later new Specs or replacements.
- Automatic mode retains incremental publication and conditional critical-gap interview. Collaborative mode interviews before drafting, then shows judgment, Task graph, acceptance, stopping rule, target, and RQ index effect before requesting explicit publication approval.
- A changed proposal invalidates earlier approval. Without approval, collaborative publication and replacement leave the current RQ index, Spec, physical Runs, and accepted evidence unchanged.
- Collaborative replacement only cancels an active writer after approval of the concrete impact, then waits for no writer before changing the design. It preserves old Runs and uses a new Run for changed scientific meaning.
- Calc-rq's handoff reaches the mode choice before calc-to-spec designs or publishes. Calc-execute's RQ continuation reaches the same collaborative gate; its execution mandate does not approve the next scientific design. Design-only requests stop after publication and never submit a job.
- A mode switch changes only the optional workflow field after the RQ owner's exact proposal approval. It does not alter previous Specs, Run evidence, or `light | strict` settings.
