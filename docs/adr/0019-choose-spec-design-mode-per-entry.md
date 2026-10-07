---
status: accepted
---

# Choose the Spec design mode at each design entry

相关研究推理职责、Spec 目标与证据档位规则已由 [ADR-0021](0021-guide-spec-reasoning-with-domain-research.md) 修订；以下保留原决策记录。

At a Spec design entry, `calc-to-spec` uses an explicit user choice of automatic
or collaborative mode. If the current request does not specify one, it presents
both and waits for an answer. Automatic is the suggested default, not consent
inferred from silence. The choice applies to the current new Spec or replacement.
The next Spec is a new design entry unless the user explicitly scoped the same
choice to the whole continuous request. No mode selection is written to RQ.md,
Spec, a preference file, or another persistent record. RQ handoff, direct
invocation, replacement, and design reached through `calc-execute` all use this
entry rule.

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

The choice is independent of `light | strict` evidence level and does not require
prepublishing the RQ's entire eventual Spec set. It does not authorize execution,
alter RQ scientific decisions, revise concluded Specs, or change accepted Run
evidence. The existing authorization and safety boundaries remain in force.

This amends ADR-0017's unconditional no-approval publication rule and its
interview-only-for-critical-gaps rule. The latter remains true in automatic mode.
