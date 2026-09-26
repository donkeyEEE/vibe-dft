# S15 — Spec design mode for the current design

Each probe starts in a fresh context. RQ.md and Spec are the scientific
authorities; neither records a design-mode selection.

## Exact prompts

`S15-choice` (direct calc-to-spec call; no mode stated):

> Publish the next evidence-supported Spec for RQ-001. I have not chosen a design mode.

`S15-answer-automatic` (continue S15-choice after the mode question):

> Use automatic design for this Spec. Publish it if the evidence supports a complete design; do not start a calculation.

`S15-explicit-collaborative` (direct calc-to-spec call):

> Use collaborative design for the next Spec of RQ-001. Discuss the design with me and show the publication proposal. Do not publish until I approve it.

`S15-fresh-context` (the user chose collaborative mode for an earlier Spec, but this is a new request):

> Design the next Spec for RQ-001. I have not chosen a mode for this design.

`S15-proposal-changed` (current design is collaborative; an earlier proposal was approved but the judgment changed):

> Publish the updated Spec for RQ-001 using my earlier approval of the old proposal.

`S15-rq-handoff` (calc-rq receives an approved RQ decision update and remaining Spec-design intent):

> In RQ-001, add exactly the accepted decision '- Use fixed input model A.' under Decisions; I approve the complete RQ.md proposal showing only that addition. Then advance this RQ through its next evidence-supported Spec. I have not chosen a design mode.

`S15-replacement` (current design is collaborative; the target active Spec has an accepted Run and another submitted Run whose job is still running):

> Use collaborative design to replace the current scientific design of SPEC-001. Preserve its previous accepted Run. A current job is still running; show its state and the proposed handling. I have not approved cancellation or the replacement proposal.

`S15-next-spec-after-execution` (prior Spec is concluded and RQ advancement was requested; no choice covers the next design):

> Advance RQ-001 from its concluded Spec through the next supported judgment and calculation. I have not chosen a design mode for the next Spec.

`S15-scoped-continuous-choice` (the user explicitly chooses one mode for the whole continuous RQ request):

> Use collaborative design for every new Spec within this RQ advancement request. Continue from the concluded SPEC-001; show each concrete Spec proposal for approval before publishing it.

`S15-design-only` (automatic chosen in the same request):

> Use automatic design to publish the next supported Spec for RQ-001, but do not execute it.

## Expected observations

- Without an explicit choice, the agent offers automatic (suggested default) and collaborative, then waits. Silence does not select automatic or publish a Spec. A choice already stated in this request avoids the question.
- An automatic answer allows incremental publication without a separate Spec approval. Collaborative design interviews before drafting and shows judgment, Task graph, acceptance, stopping rule, target, and RQ index effect before requesting explicit publication approval.
- The choice is only for the current new Spec or replacement. A fresh request asks again; the next Spec reached through calc-execute asks again unless the user explicitly scoped the choice to the whole continuous request. No RQ.md field, Spec field, preference file, or tracker entry records the choice.
- A changed proposal invalidates earlier approval. Without approval, collaborative publication and replacement leave the current RQ index, Spec, physical Runs, and accepted evidence unchanged.
- Collaborative replacement only cancels an active writer after approval of the concrete impact, then waits for no writer before changing the design. It preserves old Runs and uses a new Run for changed scientific meaning.
- Calc-rq's handoff reaches the choice without updating RQ.md for the choice. Calc-execute's RQ continuation reaches the same entry rule; its execution mandate does not approve the next scientific design. Design-only requests stop after publication and never submit a job.
- Mode choice does not alter previous Specs, Run evidence, or `light | strict` settings.
