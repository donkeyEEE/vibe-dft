# Multi-Task Workflow Note

Read this reference for a workflow with two or more tasks. State its purpose and
baseline, then record each handoff:

| Source task | Target task | Asset | Target path | Acceptance check |
|---|---|---|---|---|
| `<task-id>` | `<task-id>` | `<file or directory>` | `inputs/<path>` | `<check>` |

The note records workflow relationships, not task facts. `calc-task.yaml` remains
authoritative for paths, lifecycle status, and file indexes. Keep physical
interpretation in the contributing project note.
