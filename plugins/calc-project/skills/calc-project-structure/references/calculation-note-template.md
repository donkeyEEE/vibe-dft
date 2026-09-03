# Multi-Task Calculation Note

Use a task matrix only when one note section covers two or more related tasks.
Start with 2–4 sentences stating the section's purpose, baseline, varied
parameter family, and next research step; do not state conclusions there.

| 问题 | 判据 | 停止条件 |
|---|---|---|
| `<bounded question>` | `<decision criterion>` | `<when to stop>` |

This optional block records the scope of a bounded diagnostic or campaign.

| Task | Parameter(s) vs baseline | Purpose | Decision criterion | Status |
|---|---|---|---|---|
| `<task-id>` | `<change>` | `<purpose>` | `<criterion>` | `<status>` |

| Matrix status | `calc-task.yaml` status | Meaning |
|---|---|---|
| `queued` | `prepared` or `submitted_by_user` | Not started or queued |
| `running` | `running` | Active on cluster |
| `finished` | `finished` or `pulled` | Program completed; convergence unassessed |
| `converged` | `pulled` | Physical convergence verified |
| `failed` | any, with note | Unusable output or failed job |

- One row represents one task; a single run is not a statistical repeat.
- `calc-task.yaml` is authoritative for paths, lifecycle status, and indexed files.
- Keep physical interpretation in per-task details, not the matrix.
- Keep parameter choices scoped to their material and calculation line.

Follow the matrix with per-task inputs, targeted results, interpretation, and next
action, then a short cross-task summary.
