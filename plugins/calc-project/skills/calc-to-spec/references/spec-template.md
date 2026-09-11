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
| RUN-001 | prepared | no | <task-relative-run-path> | — |
```

Spec status is `ready | active | concluded`. Task status is `pending | current
| completed | skipped | cancelled | needs-review`; independent tasks may be
current together. Run status is `prepared | submitted | finished | failed |
cancelled`; `submitted` covers queueing and execution. `Current` is `yes | no`,
and a task has at most one current Run.

Task paths are relative to the configured data root. Run paths are relative to
their task. `Blocked by` lists only `TASK-NNN` IDs in this Spec and the graph is
acyclic. `Condition` is `always` or one natural-language sentence based on
recorded upstream results. A task stays pending until its dependencies and
condition permit it; a false condition makes it skipped, while ambiguity
returns to Spec design.

Each Spec has one principal Judgment. Purpose, Acceptance, and any stopping
rule state the approved scientific decision without selecting values from a
generic template. A concluded Spec adds this section to the same file:

```markdown
## Closure

Judgment: <final judgment>
Evidence: <accepted tasks and Runs>
RQ impact: <proposed RQ update>
```

`RQ impact` remains a proposal until `calc-rq` updates the RQ.
