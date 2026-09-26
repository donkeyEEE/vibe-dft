---
status: accepted
---

# Choose the Spec design mode per RQ

An RQ records an optional `Spec design mode: automatic | collaborative` workflow
preference. At its first Spec design entry, if no mode is recorded and the user
has not already chosen one, present both modes and wait for a choice. Automatic
is the suggested default, not consent inferred from silence. `calc-rq` owns the
RQ.md update and applies its existing exact-proposal approval rule. The mode
persists for subsequent new Specs and replacements under that RQ, including
design reached through `calc-execute`; an explicit user switch follows the same
RQ update path. A missing field means automatic for legacy interpretation, but
does not bypass the first-entry choice before a new design action.

Automatic mode retains ADR-0017's evidence-led, incremental publication and
safe replacement without a separate publication approval. Its scientific
interview remains conditional on an unresolved critical scientific gap.
Collaborative mode calls the design interview before drafting, skips questions
already settled by the accepted RQ or reliable evidence, and shows a concrete
proposal before writing. The proposal includes judgment, Tasks and dependencies,
acceptance and stopping rules, target, RQ index effect, and replacement impact
when applicable. Publication or replacement requires explicit approval of that
proposal; a material change invalidates the approval.
For a collaborative replacement, cancellation of an active writer is part of
the proposed impact and occurs only after approval, before the design is changed.

The mode is independent of `light | strict` evidence level and does not require
prepublishing the RQ's entire eventual Spec set. It does not authorize execution,
alter RQ scientific decisions, revise concluded Specs, or change accepted Run
evidence. The existing authorization and safety boundaries remain in force.

This amends ADR-0017's unconditional no-approval publication rule and its
interview-only-for-critical-gaps rule. The latter remains true in automatic mode.
