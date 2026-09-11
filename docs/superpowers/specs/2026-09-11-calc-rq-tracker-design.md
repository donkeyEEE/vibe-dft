# Calc Project RQ Tracker Design

**Date:** 2026-09-11
**Status:** Approved design; implementation out of scope

## Purpose

Define how one RQ contains multiple published Specs without introducing a
separate Tracker database or state document.

## Model

The Tracker is the configured storage convention for one RQ. With the initial
`local-markdown` adapter, each Tracker is
`<project-root>/01<main-line-slug>/01-rqs/<rq-id>-<slug>/`, containing `RQ.md`,
published Specs under `specs/`, and Decision Tickets under
`decision-tickets/`.

```text
<project-root>/01<main-line-slug>/01-rqs/<rq-id>-<slug>/
├─ RQ.md
├─ specs/
│  └─ <spec-id>-<slug>.md
└─ decision-tickets/
   └─ <NN>-<slug>.md
```

There is no independent `tracker.md`, `specs.md`, registry, progress cache, or
session-state file.

## Configuration

`calc-setup` configures the project Tracker adapter and location convention.
Consumer skills read that repository-local configuration; they do not guess an
unconfigured location. The initial adapter is `local-markdown`.

## Spec Publication

The Tracker contains only:

- a Spec published by `calc-to-spec` after user approval; or
- an existing Spec the user explicitly asks to place in the current RQ.

Publication writes the Spec into the configured RQ storage and adds its ID,
title, and relative link to `RQ.md`. It does not scan the repository or adopt
README files, ADRs, research notes, or ordinary design documents. Repeating
publication of the same Spec is idempotent; an identity or RQ-ownership conflict
stops the write.

The Spec document owns its current lifecycle, task graph, work, and closure. It
keeps no revision history. To resume work, an agent opens the Spec and follows its task and Run
references. The Tracker stores no claim, lease, handoff, takeover, active-Run
summary, completion percentage, or current-task cache.

## Decision Tickets

A Decision Ticket is a temporary record for one unresolved question in the RQ
decision process. Once its answer is accepted and written into the RQ, the
Ticket is complete and does not participate in Spec or execution coordination.

The pending-decisions view is produced on demand by reading the RQ and its
Decision Tickets. It is not persisted as Tracker state. One user confirmation
may accept the proposed Ticket answer and its exact corresponding RQ update.

## Consumer Responsibilities

- `calc-rq` creates the RQ storage and manages its Decision Tickets.
- `calc-to-spec` publishes an approved Spec to the current RQ storage.
- `calc-execute` reads a selected Spec, the referenced Run directories, and
  current external state before advancing work.
- `calc-review` remains a transient review of one prepared Run.

The Tracker does not own scientific facts, execution facts, session state, or
concurrency control for Spec, task, Run, or scheduler mutations.

## Failure Semantics

- Missing or invalid Tracker configuration stops publication or lookup.
- A missing RQ storage location is handled by `calc-rq`, not inferred by a
  consumer.
- A malformed or conflicting Spec stops publication without changing another
  domain document.
- Missing or conflicting task and Run records in the Spec stop execution; they
  are not repaired through the Tracker.

## Acceptance Criteria

- Each RQ resolves to one configured Tracker location.
- Only explicitly published Specs appear in that location.
- A new session can open a published Spec and reconstruct current work from its
  task and Run records plus the referenced calculation directories.
- Pending decisions can be presented without persisted Ticket coordination
  state.
- No independent Tracker document or duplicated progress state is required.

## Non-Goals

- Repository scanning or automatic Spec adoption.
- Spec claims, leases, handoffs, or session recovery records.
- Cached task frontier, current-task, active-Run, or attention views.
- Scientific validation, scheduler control, or correction diagnosis.

## Markdown File Conventions

Domain artifacts use plain Markdown with a title, `ID`, `Status`, and only the
headings needed by that artifact. There is no frontmatter, shared base schema,
format version, general validator, or error-code taxonomy.

The target layout is:

```text
<project-root>/01<main-line-slug>/01-rqs/RQ-001-<slug>/
├── RQ.md
├── decision-tickets/01-<slug>.md
└── specs/SPEC-001-<slug>.md

<data-root>/<project-defined-line>/TASK-001-<slug>/
├── calc-sync.yaml
└── RUN-001-<slug>/
    ├── inputs/
    │   ├── run.sh
    │   ├── run.pbs
    │   └── <scientific inputs>
    ├── outputs/
    └── logs/
```

The target structure removes required `PROJECT_PLAN.md`, `01-研究计划/`, and
`NOTE-doing.md`. Existing-project migration is out of scope.

IDs are scoped to their parent: `RQ-NNN` within a main-line, `DT-NNN` and
`SPEC-NNN` within an RQ, `TASK-NNN` within a Spec, and `RUN-NNN` within a task.
They are stable and not reused. Same-parent references use IDs; cross-level
references use relative paths. Names may append a slug.

### RQ.md

```markdown
# <RQ title>

ID: RQ-001
Status: active

## Question
## Boundary
## Success Criterion
## Decisions
## Specs

- [SPEC-001: <title>](specs/SPEC-001-<slug>.md)
```

RQ status is `active | concluded`. `Specs` contains only each explicitly
published Spec's ID, title, and relative link.

### Decision Ticket

```markdown
# <decision question title>

ID: DT-001
Status: open
Blocked by:

## Question
```

Status is `open | resolved`. `Blocked by` lists IDs in the same RQ and may be
empty. Resolution adds `## Answer`, whose accepted answer is also reflected in
`RQ.md`. Directory location expresses RQ ownership.

### Spec

```markdown
# <Spec title>

ID: SPEC-001
Status: ready
RQ: ../RQ.md

## Judgment

## Tasks

### TASK-001: <title>

Status: pending
Path: <data-root-relative-task-path>
Blocked by:
Condition: always

Purpose: <task purpose>

Acceptance: <acceptance condition>

#### Runs

| Run | Status | Current | Path | Result |
|---|---|---|---|---|
| RUN-001 | prepared | no | <relative path> | — |
```

Spec status is `ready | active | concluded`. Task status is `pending | current
| completed | skipped | cancelled | needs-review`; independent tasks may be
current together. A task has at most one current Run.

Run status is `prepared | submitted | finished | failed | cancelled`;
`submitted` covers queueing and execution. Full inputs, outputs, and logs remain
in the Run directory.

Dependency and condition rules are limited to three:

1. `Blocked by` lists task IDs from the same Spec; dependencies are acyclic.
2. `Condition` is `always` or one natural-language sentence based on recorded
   upstream results.
3. A task stays pending until dependencies and condition permit it; false makes
   it skipped, while ambiguity returns to `calc-to-spec`.

The Spec owns task purpose, DAG position, high-level status, Runs,
current-Run designation, and concise execution record. There is no `TASK.md`,
`RUN.md`, or task-domain YAML.

An approved Spec change overwrites the same file; the Spec keeps no revision
history. After closure approval, set it to `concluded` and add:

```markdown
## Closure

Judgment: <final judgment>
Evidence: <accepted tasks and Runs>
RQ impact: <proposed RQ update>
```

`RQ impact` remains a proposal until `calc-rq` updates the RQ.

### Run Inputs and Synchronization

Every Run owns its input snapshot; there is no task-level `inputs/`. `run.sh`
provides `prepare`, `validate`, and `submit` actions. The sequence is:

```text
prepare → validate → calc-review → submit unchanged inputs
```

`calc-sync.yaml` is the only structured exception and is tool configuration,
not a domain artifact:

```yaml
local: <project-relative-task-path>
server: <host:/absolute/task/path>
exclude:
  - "*.h5"
  - WAVECAR
  - CHGCAR
```

### Action Checks

Before a write, the responsible skill checks only that the needed headings and
`ID`/`Status` exist, references resolve uniquely, and the current state permits
the action. Failure stops that action and is reported in plain language.
