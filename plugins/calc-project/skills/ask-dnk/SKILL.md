---
name: ask-dnk
description: Route an explicit Calc Project request to one of the setup, RQ, Spec-design, or execution interfaces.
---

# Ask DNK

Read only enough stable project context and authoritative pointers to identify
one target and one sibling. Return the sibling's exact invocation, resolved
project/domain identity and path, the unfinished user action, and any missing
information. If zero or multiple targets remain, ask the user to choose rather
than guessing.

| Request branch | Route |
|---|---|
| Missing or changed stable project, Tracker, data-boundary, or cluster-profile configuration | `$calc-setup` |
| RQ lifecycle, Decision Ticket, accepted decision, or concluded-Spec RQ impact | `$calc-rq` |
| Principal judgment, scientific commitment, task DAG, condition, acceptance, stopping rule, or Spec replacement | `$calc-to-spec` |
| Advance a ready/active Spec; prepare, submit, track, synchronize, accept, correct, or close its Runs and tasks | `$calc-execute` |

This is a routing-only interface. Give no scientific advice, method selection,
parameter value, review verdict, authorization, or domain mutation. Do not
route ordinary requests directly to `$calc-review`; its normal caller is
`$calc-execute`, while a user may explicitly invoke it for immediate diagnosis.

Recommend the resolved sibling rather than invoking it automatically unless
the user authorized that concrete chain. A request that already names the
correct sibling uses it directly; this router is not a mandatory front door.
