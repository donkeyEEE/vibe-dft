---
name: calc-to-spec
description: Design and publish the complete calculation Spec set for one accepted RQ, or replace one existing Spec.
---

# Calc to Spec

Own the scientific design of one RQ's complete new Spec set, or one existing
Spec to replace. New-Spec input is exactly one accepted RQ plus the full
intended answer scope; replacement input is exactly one existing Spec. Output
is one concise publication proposal before approval and, only after explicit
approval, the complete proposed set and its aggregate RQ index change. This
skill declares tasks; it creates no task directory or Run and performs no
calculation or submission.

## Flow

1. Resolve exactly one calculation project, then read its `ARCHITECTURE.md`
   `## Calculation Configuration`. Resolve `Data root:`, `Tracker adapter:`,
   and `RQ location:`; require the `local-markdown` adapter. When configuration
   names a `Software profile:`, read that exact profile as the project capability
   record. Resolve exactly one RQ and read its `RQ.md`, relevant accepted
   Decisions, linked evidence, and relevant published Specs. For replacement,
   resolve the existing Spec through that RQ rather than treating its locally
   scoped `SPEC-NNN` as globally unique. Ambiguous or missing authority stops
   the action.
2. Load only the exact scientific design references needed by the proposed
   tasks:

   - VASP physical commitments: [VASP design](references/backends/vasp.md).
   - Directional SOC-MAE, together with VASP design: [VASP MAE design](references/backends/vasp-mae.md).
   - DFT+DMFT: [DMFT design](references/backends/dmft.md).
   - Hefei-NAMD/NAMDwithSOC: [NAMD design](references/backends/namd.md).
   - VASP → Wannier90 → TB2J → VAMPIRE: [magnetic design](references/backends/magnetic.md),
     plus the VASP or Wannier reference above when that stage requires its
     scientific commitments.
   - Exchange-parameter energy mapping: [energy-mapping design](references/backends/energy-mapping.md).
   - Spin-resolved Wannier windows: [Wannier90 design](references/backends/wannier90.md).
   Treat templates as implementation baselines, never as evidence for a
   scientific value. If a required reference, project capability, or evidence
   source is unavailable, stop instead of discovering an alternative backend
   resource at runtime.
3. Before drafting, invoke `$dev-engineering:grill-with-docs` in the current
   conversation to form the scientific design. In new-Spec mode, determine the
   complete set of independent principal judgments needed to answer the accepted
   RQ before drafting any member. Return a genuinely unresolved RQ-level
   question to
   `$calc-rq`; after its accepted resolution, resume complete-set design from
   the authoritative RQ. If the interview dependency is unavailable, pause this
   workflow and report it.
4. Draft the Spec set with [the Spec template](references/spec-template.md),
   using it once for every member, and keep the complete Spec draft internal
   for every member until publication. Each independent
   principal judgment gets one Spec; one judgment stays within one Spec. Include
   the tasks, dependencies, conditions, acceptance criteria, and stopping rule
   needed to answer that judgment. Allocate `SPEC-NNN` only within the resolved
   RQ, `TASK-NNN` only within that Spec, and `RUN-NNN` only within its task.
   Dependencies name only tasks in the same Spec and form an acyclic graph.
   Conditions use only recorded upstream results. State acceptance as the
   minimum sufficient evidence that the task's Purpose was answered. Leave
   execution-owned choices to `$calc-execute`: environment and executable paths,
   launch and parallel mechanics, logging and restart controls, and auxiliary
   parameters with a deterministic backend, software-profile, or
   upstream-evidence default that does not change scientific meaning. An
   explicit Spec value is binding. Return a stable project capability or
   configuration gap to `$calc-setup`.
5. For replacement, read the current Spec, every recorded task and Run,
   the referenced physical Run directories, and current scheduler state. A
   concluded Spec is immutable. Active execution that could be invalidated or
   made inconsistent blocks replacement. The proposal preserves all physical
   Run directories and overwrites only the current Spec design; it creates no
   obsolete-design history or revision counter.
6. Present only the target path, design summary, and exact `RQ.md` index change
   for each proposed member. In new-Spec mode, combine every member and the
   exact aggregate index change into one complete-set proposal. In replacement
   mode, also confirm that physical Run directories are preserved. Obtain one
   explicit approval for the displayed proposal; approval does not require
   displaying the complete Markdown for any member. Silence, historical
   preference, and general
   delegation do not satisfy the approval gate. A change to any target,
   scientific design, index entry, or stated replacement effect invalidates the
   approval.
7. Immediately before writing, re-read `RQ.md`, every target Spec, and every
   authority used for replacement. Preflight the whole approved set: require
   matching RQ ownership, unused or byte-identical new-Spec targets, complete
   designs, unique IDs and links, and safe replacement when applicable. Stop on
   any conflict before writing instead of repairing another owner's authority.
   Otherwise write every approved Spec and the exact aggregate RQ index change,
   then re-read all members and `RQ.md` to confirm them. An interrupted write is
   reconciled by re-reading the whole approved set; publishing identical
   members and links is idempotent, while any difference requires a new
   proposal and approval.
8. Report every published member or the one replaced Spec. Only after every
   member of a new complete Spec set and its aggregate index change are
   confirmed, continue directly with `$calc-execute` when execution intent
   remains; never hand off after only a prefix of the set. A safely replaced
   active Spec may continue as before. Carry the resolved identities, paths,
   approved content, and remaining intent. The handoff adds no submission or
   other external-action authorization; `$calc-execute` applies its own gates.

## Authority

This skill owns the current principal judgments and the scientific commitments,
task DAG, task declarations, conditions, acceptance rules, and stopping rules
in each Spec. `$calc-execute` owns execution-owned choices omitted by a Spec and
records their realized values in the Run inputs and evidence; it cannot
override an explicit Spec value. Each Spec is the sole authority for its task
and Run records. This skill does not materialize those declarations, alter
physical Run data, persist complete-set state or another parallel workflow
record, or formally update RQ conclusions.
