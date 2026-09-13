---
name: calc-rq
description: Create, inspect, revise, or derive one calculation Research Question and record its accepted decisions.
---

# Calc RQ

Own the RQ lifecycle and its accepted decisions. The configured Tracker is a
storage convention; `RQ.md` is the sole RQ authority.

1. Resolve exactly one calculation project. Read its `ARCHITECTURE.md`
   `## Calculation Configuration`, then resolve the configured `Data root:`,
   `Tracker adapter:`, and `RQ location:`. Require the `local-markdown` adapter.
   For creation, resolve exactly one parent main-line; otherwise resolve exactly
   one target RQ by its stable ID or path. Ask the user to select when no target
   or more than one target matches. A missing or invalid configuration stops
   this action and should be handed to `$calc-setup`.
2. For creation, read the sibling RQ directories under the resolved main-line
   to prevent an ID collision. For existing-RQ work, read the selected `RQ.md`,
   plus the relevant published Spec when the intent concerns concluded-Spec
   impact. Treat those files as authorities, not conversational summaries. Keep
   no separate question record, Tracker document, registry, cache, claim, or
   session state.
3. For creating or deriving an RQ, or changing its Question, the `Boundary:`
   field under Question, or Success Criterion, invoke `$dev-engineering:grill-with-docs`. If that
   dependency is unavailable, stop only this workflow and report it; inspection
   and already-decided RQ updates remain available when they do not require that
   workflow. Record RQ-scoped terminology and framing produced by the interview
   under `RQ.md` `## Context`; reserve the repository's root `CONTEXT.md` for
   stable project-wide domain terms. Resolve an unanswered question in the
   current conversation. After the user answers it, propose the exact addition
   or replacement under `RQ.md` `## Decisions`; do not persist the unanswered
   question separately.
4. Draft an RQ with [the RQ template](references/rq-template.md) when creating
   one. `RQ-NNN` IDs are stable and unused within their parent main-line.
5. Present the exact proposed file paths and complete Markdown changes. Wait for
   every approval required by the calling convention: creating or deriving an
   RQ and every formal RQ update require explicit approval. Approval binds only
   the displayed proposal; revise and present it again after any change.
   Closure impact from a concluded Spec remains a proposal until this approval;
   report it as accepted, rejected, or pending. On approved creation, create the
   configured RQ directory with `RQ.md` and `specs/`.
6. Re-read `RQ.md` after each write. When its accepted decisions are sufficient
   for the intended answer scope and the user's unfinished request includes Spec
   design, continue directly with `$calc-to-spec`, carrying the resolved RQ,
   paths, accepted decisions, and complete remaining intent so it can design
   every required Spec before any default execution handoff. Stop for missing
   approval or an unavailable configured Tracker. Invoke the owning
   business sibling directly for a stable-configuration or Spec-design issue;
   use `$ask-lyz` only when workflow selection itself remains open-ended.

Do not create or change a Spec, task, Run, calculation input, or execution
state within this interface. A sibling handoff needs no separate authorization,
but the receiving skill retains every approval and external-action gate it
owns.
