---
name: calc-rq
description: Create, inspect, revise, or derive one calculation Research Question and resolve its Decision Tickets.
---

# Calc RQ

Own the RQ lifecycle and its temporary Decision Tickets. The configured
Tracker is a storage convention; `RQ.md` remains the accepted RQ authority.

1. Resolve exactly one calculation project. Read its `ARCHITECTURE.md`
   `## Calculation Configuration`, then resolve the configured `Data root:`,
   `Tracker adapter:`, and `RQ location:`. Require the `local-markdown` adapter.
   For creation, resolve exactly one parent main-line; otherwise resolve exactly
   one target RQ by its stable ID or path. Ask the user to select when no target
   or more than one target matches. A missing or invalid configuration stops
   this action and should be handed to `$calc-setup`.
2. For creation, read the sibling RQ directories under the resolved main-line
   to prevent an ID collision. For existing-RQ work, read the selected `RQ.md`,
   its `decision-tickets/*.md`, and the relevant published Spec when the intent
   concerns concluded-Spec impact. Treat those files as authorities, not
   conversational summaries. Derive pending decisions on demand; keep no
   Tracker document, registry, cache, claim, or session state.
3. For creating or deriving an RQ, or changing its Question, Boundary, or
   Success Criterion, invoke `$dev-engineering:grill-with-docs`. If that
   dependency is unavailable, stop only this workflow and report it; inspection,
   Ticket resolution, and already-decided RQ updates remain available when they
   do not require that workflow.
4. Draft an RQ with [the RQ template](references/rq-template.md) when creating
   one. Draft a Ticket with [the Decision Ticket
   template](references/decision-ticket-template.md) when one unresolved RQ
   question needs an explicit answer. IDs are stable and unused within their
   parent: `RQ-NNN` within one main-line and `DT-NNN` within one RQ. Ticket
   files use `decision-tickets/NN-<slug>.md`, where `NN` is the numeric ID value
   rendered with at least two digits: `DT-001` maps to `01-<slug>.md`, `DT-012`
   to `12-<slug>.md`, and `DT-100` to `100-<slug>.md`. Ticket dependencies name
   only `DT-NNN` IDs in that same RQ. Directory location expresses Ticket
   ownership.
5. Present the exact proposed file paths and complete Markdown changes. Wait for
   every approval required by the calling convention: creating or deriving an
   RQ and every formal RQ update require explicit approval. Approval binds only
   the displayed proposal; revise and present it again after any change.
   Closure impact from a concluded Spec remains a proposal until this approval;
   report it as accepted, rejected, or pending. On approved creation, create the
   configured RQ directory with `RQ.md`, `decision-tickets/`, and `specs/`.
6. For one Ticket resolution, present its proposed `Status: resolved` and
   `## Answer` together with the exact corresponding update to `RQ.md`
   `## Decisions`. One explicit approval may accept this displayed pair. Write
   both authorities before advancing another Ticket. If either write fails,
   stop and report which member of the pair was written; reconcile by rereading
   those two files and proposing the remaining or corrective write. Do not
   introduce a transaction or session registry.
7. Re-read `RQ.md` and the same-RQ Tickets after each write. Advance at most the
   currently decidable Ticket frontier and resolve one Ticket at a time.
   Unrelated open Tickets do not block Spec design. When the decisions relevant
   to the intended Spec are sufficient and the user's unfinished request
   includes designing it, continue directly with `$calc-to-spec`, carrying the
   resolved RQ, paths, accepted decisions, and remaining intent. Stop for
   missing approval or an unavailable configured Tracker. Invoke the owning
   business sibling directly for a stable-configuration or Spec-design issue;
   use `$ask-lyz` only when workflow selection itself remains open-ended.

Do not create or change a Spec, task, Run, calculation input, or execution
state within this interface. A sibling handoff needs no separate authorization,
but the receiving skill retains every approval and external-action gate it
owns.
