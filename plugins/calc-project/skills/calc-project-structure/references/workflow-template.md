# WORKFLOW.md template

Copy this file to the project root as `WORKFLOW.md` when an approved workflow
spans stages. Edit it manually as a lightweight handoff record; do not parse it
as task metadata. `calc-task.yaml` remains authoritative for task paths and
lifecycle state.

## Stage handoffs

| Stage | Upstream artifacts | Downstream use | Required outputs | Acceptance condition | Status | Evidence |
|---|---|---|---|---|---|---|
| `<stage-label>` | `<upstream-artifact-label>` | `<downstream-use-label>` | `<required-output-label>` | `<acceptance-condition-label>` | `<status-label>` | `<evidence-path-or-note-label>` |

## Notes

Record unresolved handoff details, assumptions, or decisions here.
