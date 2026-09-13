```markdown
# <RQ title>

ID: RQ-001
Status: active

## Question

Boundary: <scope, applicable conditions, and exclusions>

## Success Criterion
## Specs

- [SPEC-001: <title>](specs/SPEC-001-<slug>.md)

## Decisions
## Context
```

RQ status is `active | concluded`. `Specs` contains only each explicitly
published Spec's ID, title, and relative link. `Decisions` contains accepted
RQ decisions. `Boundary` is a required field under `Question`. `Context`
records RQ-scoped terminology and framing needed to interpret the Question,
Boundary, Success Criterion, Decisions, and Specs.
