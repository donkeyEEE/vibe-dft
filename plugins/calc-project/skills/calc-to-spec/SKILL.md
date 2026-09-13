---
name: calc-to-spec
description: Design or replace one calculation Spec from an accepted RQ and a principal scientific judgment.
---

# Calc to Spec

Own one Spec's current scientific design. Input is exactly one RQ plus one
intended principal judgment, or exactly one existing Spec to replace. Output is
one concise publication proposal before approval and, only after explicit
approval, one published Spec and one link in its RQ. This skill declares tasks;
it creates no task directory or Run and performs no calculation or submission.

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
   conversation to form the scientific design. If that dependency is
   unavailable, pause this workflow and report it.
4. Draft the Spec with [the Spec template](references/spec-template.md), and
   keep the complete Spec draft internal until publication. Form one principal
   judgment and propose separate Specs for independent principal judgments.
   Include the tasks, dependencies, conditions, acceptance criteria, and
   stopping rule needed to answer that judgment. Allocate `SPEC-NNN` only within
   the resolved RQ, `TASK-NNN` only within that Spec, and `RUN-NNN` only within
   its task. Dependencies name only tasks in the same Spec and form an acyclic
   graph. Conditions use only recorded upstream results. State acceptance as the
   minimum sufficient evidence that the task's Purpose was answered. Leave
   execution-owned choices to `$calc-execute`: environment and executable paths,
   launch and parallel mechanics, logging and restart controls, and auxiliary
   parameters with a deterministic backend, software-profile, or
   upstream-evidence default that does not change scientific meaning. An
   explicit Spec value is binding. Return RQ-level scientific uncertainty to
   `$calc-rq`; return a stable project capability or configuration gap to
   `$calc-setup`.
5. For replacement, read the current Spec, every recorded task and Run,
   the referenced physical Run directories, and current scheduler state. A
   concluded Spec is immutable. Active execution that could be invalidated or
   made inconsistent blocks replacement. The proposal preserves all physical
   Run directories and overwrites only the current Spec design; it creates no
   obsolete-design history or revision counter.
6. Present only the target path, design summary, exact `RQ.md` index change,
   and, for replacement, confirmation that physical Run directories are
   preserved. Obtain explicit approval for that concise proposal; approval does
   not require displaying the complete Markdown. Silence, historical
   preference, and general delegation do not satisfy the approval gate. A
   change to the target, scientific design, index entry, or stated replacement
   effects invalidates the approval.
7. Immediately before writing, re-read `RQ.md`, the target Spec, and every
   authority used for replacement. Require matching RQ ownership and confirm
   that the approved design remains complete and the replacement remains safe.
   Stop on a conflict instead of repairing another owner's authority. Otherwise
   write the Spec and exactly one RQ index link, then re-read both to confirm
   them. Publishing the same target, design, and index entry is idempotent.
8. Report the published or replaced Spec. When the user's unfinished request
   includes execution, continue directly with `$calc-execute` for a ready or
   safely replaced active Spec, carrying the resolved identities, paths,
   approved content, and remaining intent. The handoff adds no submission or
   other external-action authorization; `$calc-execute` applies its own gates.

## Authority

This skill owns the current principal judgment, scientific commitments, task
DAG, task declarations, conditions, acceptance rules, and stopping rules in one
Spec. `$calc-execute` owns execution-owned choices omitted by the Spec and
records their realized values in the Run inputs and evidence; it cannot
override an explicit Spec value. The Spec is the sole authority for its task
and Run records. This skill does not materialize those declarations, alter
physical Run data, persist a parallel workflow record, or formally update RQ
conclusions.
