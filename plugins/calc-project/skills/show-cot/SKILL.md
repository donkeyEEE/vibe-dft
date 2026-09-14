---
name: show-cot
description: Display a calculation project's full Calculation Ownership Tree (COT) to inspect RQ, Spec, Task, and Run history.
---

# Show COT

Present a read-only Calculation Ownership Tree for one configured calculation
project. Use a project root already resolved by the caller; for a direct
invocation, locate the unique configured project from the current directory.
Ask for a project location when that is ambiguous.

Read the project's calculation configuration, then its RQ Tracker authorities:
each `RQ.md`, the Specs it publishes, and each Spec's declared Tasks and Runs.
Render the entire project as a stable tree:

```text
RQ-NNN <title> [<status>]
└── SPEC-NNN <title> [<status>]
    └── TASK-NNN <title> [<status>]
        └── RUN-NNN [<status>]
```

Task dependencies remain in the
Spec and are not drawn as COT edges.

When `calc-execute` supplies the Task and Run at which it is returning control,
precede the tree with one concise line naming that Task and Run and its recorded
Run status. A direct COT request is only the tree.
