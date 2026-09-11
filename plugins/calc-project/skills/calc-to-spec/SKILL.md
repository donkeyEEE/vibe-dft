---
name: calc-to-spec
description: Design or replace one calculation Spec from an accepted RQ and a principal scientific judgment.
---

# Calc to Spec

Own one Spec's current scientific design. Input is exactly one RQ plus one
intended principal judgment, or exactly one existing Spec to replace. Output is
one reviewable draft and, only after explicit approval, one published Spec and
one link in its RQ. This skill declares tasks; it creates no task directory or
Run and performs no calculation or submission.

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
3. Form one principal judgment for the Spec. Propose separate Specs for
   independent principal judgments. Settle every decision that would change the
   scientific commitment, task DAG, dependency or condition, acceptance
   criterion, or stopping rule. Return RQ-level scientific uncertainty to
   `$calc-rq`; return a stable project capability or configuration gap to
   `$calc-setup`.
4. Draft the complete Spec with [the Spec template](references/spec-template.md).
   Allocate `SPEC-NNN` only within the resolved RQ, `TASK-NNN` only within that
   Spec, and `RUN-NNN` only within its task. Record task paths relative to the
   configured data root and Run paths relative to their task. Dependencies name
   only tasks in the same Spec and form an acyclic graph. Conditions use only
   recorded upstream results. State decisive acceptance and stopping criteria;
   ambiguity is an unresolved design decision, not an execution default.
5. For replacement, first read the current Spec, every recorded task and Run,
   the referenced physical Run directories, and current scheduler state. A
   concluded Spec is immutable. Active execution that could be invalidated or
   made inconsistent blocks replacement. The proposal preserves all physical
   Run directories and overwrites only the current Spec design; it creates no
   obsolete-design history or revision counter.
6. Present one concrete publication proposal: the full Markdown draft, its
   exact `specs/SPEC-NNN-<slug>.md` target, and the exact single ID/title/link
   entry for `RQ.md` `## Specs`. For replacement, show the complete overwritten
   Spec and any index correction. Obtain explicit approval for this exact
   proposal. Silence, historical preference, and general delegation do not
   satisfy an approval gate. A changed proposal invalidates that approval.
7. Immediately before writing, re-read `RQ.md`, the exact target Spec path, and
   every authority used for replacement. Before any write, require the complete
   proposed Spec, the current RQ, and, for replacement, the current Spec to have
   the needed document shape. The RQ has `ID`, `Status: active | concluded`, and
   `Question`, `Boundary`, `Success Criterion`, `Decisions`, and `Specs`. The
   proposed and current Spec have `ID`, `Status`, `RQ`, `Judgment`, and `Tasks`;
   each task has `Status`, `Path`, `Blocked by`, `Condition`, `Purpose`,
   `Acceptance`, and `Runs`; each recorded Run row has Run ID, `Status`,
   `Current`, `Path`, and `Result`. Apply the permitted values, same-Spec
   dependency and acyclic-DAG rule, relative-path rules, and at-most-one-current
   Run convention stated by the Spec template. Also require unique references,
   unchanged approved content, and matching RQ ownership. This is a direct check
   of the documents being used, not a general schema validator.

   Approval of malformed content does not waive this contract and does not
   authorize filling or changing the approved proposal. Stop all writes, name
   the specific missing or conflicting field and its document, and identify its
   owner: RQ shape returns to `$calc-rq`; a proposed Spec is corrected here and
   presented again in full for new approval; current Spec design or task
   declarations belong here, while current execution status and Run records
   belong to `$calc-execute`. Identity, path, ownership, or newly unsafe active
   execution conflicts stop in the same way. Publishing an identical complete
   ID/path/content/link is idempotent. Otherwise write the approved Spec and
   exactly one RQ index link, then re-read both authorities to confirm them.
8. Report the published or replaced Spec and recommend `$calc-execute` for a
   ready or safely replaced active Spec. The recommendation carries resolved
   paths and unfinished intent; it does not invoke the sibling automatically.

## Authority

This skill owns the current principal judgment, scientific commitments, task
DAG, task declarations, conditions, acceptance rules, and stopping rules in one
Spec. The Spec is the sole authority for its task and Run records. This skill
does not materialize those declarations, alter physical Run data, persist a
parallel workflow record, or formally update RQ conclusions.
