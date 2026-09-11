# <decision question title>

ID: DT-001
Status: open
Blocked by:

## Question

Ticket status is `open | resolved`. `Blocked by` lists IDs in the same RQ and
may be empty. For example, a Ticket depending on two earlier Tickets in its
parent RQ uses:

```markdown
Blocked by: DT-001, DT-002
```

Resolution uses the same file and adds the accepted answer:

```markdown
# <decision question title>

ID: DT-003
Status: resolved
Blocked by: DT-001, DT-002

## Question

## Answer
```

The accepted answer is also reflected in `RQ.md`. Directory location expresses
RQ ownership.
