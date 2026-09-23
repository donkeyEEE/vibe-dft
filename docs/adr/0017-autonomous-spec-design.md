---
status: accepted
---

# Let Calc To Spec publish scientific designs autonomously

## Decision

- For an accepted RQ, `calc-to-spec` may publish a new Spec without a separate approval.
- It may also replace the current design of an existing mutable Spec without a separate approval.
- The scientific-design interview is conditional: invoke it when a critical scientific gap remains, rather than before every draft.
- A critical scientific gap is an unresolved choice that affects the principal judgment, comparability, or acceptance and cannot be settled from the accepted RQ, project evidence, and reliable literature. Other scientific details may be chosen autonomously.
- When a running job blocks safe replacement, the agent verifies its state, autonomously cancels it or waits as appropriate, preserves the old Run, and replaces the Spec only after the writer is inactive.
- Design rules have two levels for comparability and acceptance. The lighter default requires the direct result and necessary handoff evidence sufficient to answer each Task Purpose. It does not add independent convergence scans, parameter sensitivity studies, repeated Runs, or alternative-method controls by default. A check remains required when the principal judgment itself cannot be made without it.
- The strict level applies only when the user or accepted RQ explicitly requires it. The lighter level still includes any check logically necessary for the stated judgment.
- The design level may be set on both RQ and Spec. An explicit Spec setting wins; otherwise the Spec inherits the RQ setting; if neither is set, the level is light. Resolve and record the effective level when publishing each Spec. A later RQ-level change does not silently change an already published Spec; changing that Spec follows its replacement path.
- New Specs may be published incrementally as the research proceeds. A publication need not enumerate or publish the complete eventual Spec set under the RQ; each published Spec still has one coherent principal judgment and a truthful RQ index entry.
- On replacement, preserve every physical and recorded old Run. If the new design invalidates an old accepted Run, clear its `Current` selection and the affected Task's completed judgment; execute the changed scientific design in a new Run. Never reinterpret the old Run as evidence for the new design without a fresh assessment.
- After a Spec completes, the agent may autonomously publish and execute a later Spec when the accepted RQ and observed evidence establish the next principal judgment, within the user's explicit boundaries.
- Incremental advancement stops when the RQ success criterion is met, no evidence-supported next principal judgment remains, a critical scientific gap remains unresolved, or the user's explicit boundary is reached.
- A later Spec must directly serve the current accepted RQ and remain inside its Boundary. An unrelated material, condition, or property does not become a Spec under that RQ and does not trigger an automatic RQ rewrite.
- An invocation that asks only to design or publish Specs stops after publication. Handoff to `calc-execute` occurs when the user has asked to advance the RQ through calculation.
- Every published Spec remains complete for its own principal judgment: it states the judgment, Tasks, dependencies, minimum sufficient acceptance, and stopping rule. Incremental publication does not permit placeholder or partial Specs.
- When project and backend design knowledge is insufficient, research autonomously through `$dev-engineering:research` or `$paper-project:literature-review` as appropriate; use the resulting evidence for design, and interview only if a critical scientific gap remains. `calc-to-spec` may invoke `literature-review` automatically and choose a scoped Markdown output path; the latter skill's invocation and path contracts include that exception.
- A `concluded` Spec may be read as historical evidence. Later scientific judgments normally get a new Spec. Modifying or reopening the concluded Spec itself requires specific human authorization for the concrete change.
- The agent chooses freely between `$dev-engineering:research` and `$paper-project:literature-review` for an evidence gap, based on what would resolve it most effectively.
- Targeted research artifacts are temporary. Full literature reviews generated for the design are saved under the research line's `06-文献笔记/`; the Spec cites the underlying sources it actually uses.
- Backend design references retain checks necessary for physical validity and the stated judgment. Under the light level, additional convergence or sensitivity work is conditional rather than a universal prerequisite.
- Standalone `$paper-project:literature-review` remains explicit-only. `$calc-to-spec` is a named exception allowed to invoke it automatically with an agent-selected path under the research line's literature notes.

## Deferred topic: RQ iteration

Execution of an RQ may reveal a distinct research question. Whether, when, and how to create another RQ from that discovery requires a separate design discussion. This ADR neither restricts nor recommends creation of a new RQ during execution of the current RQ.

This decision amends ADR-0016's scientific-design approval gate. Its runtime
contracts are implemented in `calc-to-spec`, the evidence-level templates,
relevant backend references, and the directed `literature-review` handoff.
