# Calc Project RQ Tracker Design

**Date:** 2026-09-11
**Status:** Approved design; implementation out of scope

## Purpose

Define a cross-session coordination mechanism for calculation Specs under one research question (RQ). The mechanism exposes which Spec is being coordinated, what its current calculation frontier is, and what a replacement session must know. It does not own scientific results or external execution.

This design depends on the confirmed domain decisions recorded in `/tmp/calc-project-object-responsibilities-handoff.md`. That temporary handoff is context rather than a repository contract; later domain and implementation specifications must incorporate the decisions they consume.

## Decision Summary

- There is no standalone Tracker skill.
- `calc-project-structure` configures the Tracker protocol once for a calculation project.
- Each RQ has one Tracker document covering all Specs owned by that RQ.
- Consumer skills read a repository-local configuration document and perform normalized Tracker operations directly.
- The first backend is local Markdown. The protocol preserves a backend adapter seam without implementing other backends.
- The Tracker is authoritative for Spec coordination claims, leases, and handoffs.
- The calculation frontier and execution summaries are rebuildable views derived from Spec, task, and Run sources.
- The Tracker is not authoritative for the RQ, Spec design, task acceptance, Run results, correction history, or external scheduler state.

## Architecture

```text
calculation project
├─ Agent instruction pointer
├─ Tracker protocol configuration
└─ RQ
   ├─ RQ Tracker
   ├─ Spec A
   │  └─ task DAG → tasks → Runs
   └─ Spec B
      └─ task DAG → tasks → Runs
```

The RQ Tracker is the coordination entry point for all Specs owned by one RQ. Different Specs under the same RQ may be claimed by different sessions. A single Spec may have only one effective claim at a time. The claiming session may still submit multiple calculation-frontier tasks in parallel.

## Authority Boundaries

| Fact | Authority |
|---|---|
| RQ identity, question, boundary, and accepted Spec impact | Upstream RQ document and its managing workflow |
| Task DAG, conditions, Spec revisions, acceptance rules, and closure | Spec document |
| Task identity, task state, inputs, and task acceptance | Task metadata |
| Run input snapshot, outputs, logs, execution state, and current designation | Run metadata and directory |
| Spec claim, lease, release, and session handoff | RQ Tracker |
| Calculation frontier, active-Run summary, and attention summary | Rebuildable RQ Tracker views |

When a rebuildable Tracker view conflicts with an authoritative source, consumers rebuild the view. They must not modify the authoritative source to match the Tracker.

The Tracker does not diagnose computation failures, decide whether a scientific result is valid, alter the task DAG, approve a Spec revision, update the RQ, or control an external scheduler.

## Configuration Seam

`calc-project-structure` configures the mechanism using the same policy/configuration separation used by Matt Skills for issue trackers. It presents the Agent pointer and Tracker protocol configuration for user approval before writing them.

The Agent instruction points consumers to a repository-local configuration document. That document defines:

- the configured backend;
- how to locate the Tracker for an RQ;
- the supported schema version;
- concrete storage and locking rules;
- normalized operation semantics.

The normalized operations are:

```text
create
read
register-spec
claim-spec
renew-claim
release-spec
recompute-frontier
record-handoff
mark-concluded
```

The initial backend is `local-markdown`. A consumer that cannot find or parse the Agent pointer or configuration stops its Tracker mutation and reports the configuration problem. It does not guess a location or initialize an implicit default. Switching backends is a configuration action owned by `calc-project-structure`.

## RQ Tracker Document

The Tracker uses YAML frontmatter for machine-coordination state and fixed Markdown sections for human- and agent-readable views.

Illustrative frontmatter:

```yaml
---
tracker_schema: calc-rq-tracker/v1
rq_id: RQ-001
rq_path: path/to/rq.md
tracker_revision: 12
updated_at: 2026-09-11T15:30:00+08:00

specs:
  - spec_id: SPEC-001
    path: path/to/spec-001.md
    current_revision: 3
    claim:
      session_id: session-abc
      claimed_at: 2026-09-11T14:00:00+08:00
      renewed_at: 2026-09-11T15:00:00+08:00
      expires_at: 2026-09-11T16:00:00+08:00
    view_refreshed_at: 2026-09-11T15:29:00+08:00
---
```

Required Markdown sections:

```markdown
# RQ Tracker

## Spec Overview
## Calculation Frontiers
## Active Runs
## Needs Attention
## Session Handoffs
## Recent Coordination Events
```

Document rules:

- `tracker_revision` increments on every successful mutation.
- Stable IDs and paths are both stored: IDs preserve identity, while paths locate sources.
- The document does not copy complete DAGs, task inputs, logs, correction diagnoses, or scientific conclusions.
- Frontiers are grouped by Spec and identify tasks by stable ID and path.
- `Needs Attention` is a rebuildable coordination summary. Details remain in the owning Spec, task, or Run source.
- Coordination events are limited to registration, claim, renewal, release, takeover, handoff, frontier rebuild, and Spec closure.
- Times use timezone-qualified ISO 8601 values.

The final filename and path rule are configured rather than hard-coded here because the upstream RQ storage design remains separate.

## Spec Lifecycle and Coordination Claims

The Spec document owns its lifecycle:

```text
draft → ready → active → concluded
```

The Tracker owns coordination claim state:

```text
unclaimed ↔ claimed
             ↓
           expired
```

The Tracker derives a human-facing display from the two sources:

| Spec lifecycle | Claim | Display |
|---|---|---|
| draft | none | not-ready |
| ready | none | available |
| ready or active | effective | claimed |
| ready or active | expired | takeover-needed |
| active | deliberately released | paused |
| concluded | none | concluded |

Claim protocol:

1. Re-read the Tracker and target Spec before claiming.
2. Claim only a ready or active Spec with no effective claim.
3. Permit at most one effective claim per Spec.
4. Renew the lease while coordinating the Spec.
5. Do not cancel an external job or alter a Run merely because a lease expires.
6. Before takeover, the new consumer checks existing Runs and scheduler state as part of its own execution responsibility.
7. On release, record a minimal handoff: completed coordination work, referenced active Runs, outstanding attention, and the next intended action.
8. On Spec closure, release the claim and retain the last handoff and closure coordination event.

Different Specs under the same RQ may hold claims concurrently. The RQ is not an execution lock.

## Concurrency Control

`tracker_revision` detects stale edits but does not prevent two writers from producing the same next revision. The local Markdown backend therefore uses a short-lived write lock for each Tracker mutation:

```text
acquire Tracker write lock
→ re-read tracker_revision
→ validate operation preconditions
→ write and validate a temporary document
→ atomically replace the Tracker
→ release lock
```

The write lock protects one file mutation; it is not the long-lived Spec claim. Lock records identify their holder and creation time. The backend configuration defines the stale-lock threshold and recovery procedure. Recovering a stale write lock records a coordination event.

On revision conflict, the consumer discards its proposed document, reads the latest state, and reapplies the semantic operation. It never resolves the conflict by blindly overwriting the newer Tracker.

## Calculation Frontier

The calculation frontier is the set of tasks that are scientifically and technically ready to execute at a given moment. A task is in the frontier only when all of the following hold:

- its Spec is ready or active;
- the task is not cancelled, paused, or superseded;
- every upstream task has a valid current Run outcome;
- the task activation condition evaluates to true;
- the task has no valid current Run satisfying its current definition;
- no active Run is already expected to satisfy that task.

Condition states are:

- `true`: the task may enter the frontier;
- `false`: the task is currently skipped by condition;
- `undecidable`: more upstream outcomes are required.

The frontier may contain multiple tasks. Resource quotas, queue capacity, and user priority decide which frontier tasks are submitted; they do not change frontier membership.

Consumers recompute the frontier after:

- a Spec revision takes effect;
- a task is accepted, cancelled, paused, or superseded;
- a Run starts, ends, loses validity, or becomes current;
- an activation condition changes;
- a Spec claim is taken over;
- an explicit frontier refresh is requested.

Recomputing the frontier modifies only the Tracker view. It does not validate scientific results or alter source states.

## Relationship to Correction

Correction is deliberately outside Tracker authority.

- Run metadata and logs own execution errors and observations.
- Task metadata owns suspect, needs-review, acceptance invalidation, recomputation reason, and current-Run changes.
- Spec revisions own approved changes to scientific commitments, replacement tasks, and DAG structure.
- The Tracker may show a derived `Needs Attention` summary when those facts affect coordination or frontier membership.
- Detailed diagnosis, root cause, repair steps, and recomputation history are not Tracker events.

The task DAG remains acyclic. Correcting an upstream task does not create a back edge. When a task's scientific commitment remains unchanged, correction creates a new Run under the same task. When the commitment changes, an approved Spec revision creates a replacement task and adjusts current DAG dependencies. Iterative scientific algorithms are encapsulated inside one task and use Runs as their smallest execution units.

## Consumer Contracts

### `calc-project-structure`

- Detects existing Agent instructions and Tracker configuration.
- Presents the proposed pointer and configuration for approval.
- Writes or updates the configuration without duplicating instruction blocks.
- Does not act as the runtime Tracker coordinator.

### Upstream RQ management workflow

- Creates the RQ Tracker when it creates an approved RQ.
- Reads concluded Spec impact through links from the Tracker.
- Updates the RQ only after user approval.
- Does not change Spec DAGs, tasks, or Runs.

### `to-spec`

- Reads the RQ and its Tracker.
- Creates a Spec draft and stable task declarations.
- Registers the Spec after user approval makes it ready.
- Does not create task directories, implement inputs, create Runs, or claim the Spec.

### `implement`

- Reads configuration, Tracker, Spec, tasks, and Runs.
- Atomically claims the whole Spec.
- Recomputes the frontier and may submit multiple frontier tasks in parallel.
- Updates task and Run authorities before refreshing the Tracker view.
- Renews the claim and records a handoff on release.
- Does not approve a design revision or an overwrite-style recomputation.

### Future correction capability

Its final skill boundary remains intentionally undesigned. Any future consumer follows the same Tracker configuration and only refreshes Tracker views when correction facts affect coordination. It records correction facts in their owning task, Run, or Spec source.

### Spec closure

The executing workflow first writes the Spec's single immutable closure record and changes the Spec lifecycle to concluded. It then releases the Tracker claim, refreshes views, and records `spec-concluded`. The Tracker links to the closure but does not copy the primary judgment. The upstream RQ workflow separately handles the proposed impact on the RQ.

## Tracker Failure Semantics

Tracker failure behavior is limited to coordination:

- Missing or unparseable configuration: stop the Tracker operation and report it.
- Missing RQ Tracker: do not infer or rebuild it; defer to the upstream RQ creation workflow.
- Write-lock conflict: do not write; retry from the newest document or report the conflict.
- Changed `tracker_revision`: discard the stale proposal and reapply the semantic operation.
- Syntactically damaged Tracker: stop writes and report the damage; do not modify other domain sources.
- Expired lease: display the expired claim; external-state checks belong to the session attempting takeover.
- Stale frontier view: a consumer may recompute it from authoritative sources.

There is no general Tracker audit operation. Domain validation, path repair, DAG validation, correction diagnosis, and scheduler reconciliation belong to their corresponding workflows.

## Acceptance Criteria

### Configuration

- Consumers locate the protocol through the Agent instruction pointer.
- Missing or invalid configuration prevents mutation.
- The initial implementation accepts only the local Markdown backend.

### Creation and registration

- An RQ has at most one Tracker.
- Re-registering the same Spec is idempotent.
- A Spec owned by another RQ cannot be registered.
- A draft may be displayed but cannot be claimed; a ready Spec is available.

### Claims and leases

- Concurrent claims for one Spec yield at most one success.
- Different Specs can be claimed by different sessions.
- Only the holder renews a claim.
- Lease expiry changes coordination state only.
- Release clears the claim and preserves a minimal handoff.

### Concurrent mutation

- Locking plus revision checks prevent silent overwrite.
- Conflicts are reapplied against the latest document.
- Interrupted writes do not leave a partially written Tracker.

### Frontier view

- Independent ready tasks can appear together.
- Changes in upstream current Runs can refresh the view.
- The view is rebuildable from authoritative sources.
- Refreshing it does not alter Spec, task, or Run facts.

### Handoff and closure

- A replacement session can identify the claim state, frontier, active-Run references, attention summary, and next coordination action.
- A concluded Spec has no effective claim.
- Closure is linked rather than copied.
- The Tracker does not formally update the RQ.

### Explicit exclusions

Tracker tests do not assert scientific input quality, Run-result correctness, DAG scientific validity, scheduler execution, correction diagnosis, or whether an RQ should change.

## Non-Goals

- Implementing a standalone Tracker skill.
- Supporting GitHub, GitLab, Jira, or another remote backend in the first version.
- Replacing Spec, task, or Run authorities with one database-like document.
- Managing correction details or scientific evidence.
- Controlling or reconciling external jobs.
- Designing the future correction skill.
- Finalizing RQ storage paths or the complete Calc Project skill roster.
