---
name: ask-lyz
description: Route an explicit Calc Project request to one of the setup, RQ, Spec-design, or execution interfaces.
---

# Ask LYZ

Read only enough stable project context and authoritative pointers to identify
one target and one sibling. Return the sibling's exact invocation, resolved
project/domain identity and path, the unfinished user action, and any missing
information. If zero or multiple targets remain, ask the user to choose rather
than guessing.

| Request branch | Route |
|---|---|
| Missing or changed stable project, Tracker, data-boundary, or cluster-profile configuration | `$calc-setup` |
| RQ lifecycle, accepted decision, unanswered RQ question, or concluded-Spec RQ impact | `$calc-rq` |
| Complete Spec set for one RQ, principal judgment, scientific commitment, task DAG, condition, acceptance, stopping rule, or one Spec replacement | `$calc-to-spec` |
| Advance a ready/active Spec; prepare, submit, track, synchronize, accept, correct, or close its Runs and tasks | `$calc-execute` |

This is a routing-only interface. Give no scientific advice, method selection,
parameter value, review verdict, authorization, or domain mutation.

Recommend the resolved sibling rather than invoking it automatically.
