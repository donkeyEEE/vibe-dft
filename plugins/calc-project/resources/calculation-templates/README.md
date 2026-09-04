# Shared calculation templates

These task-copy sources have multiple active workflow consumers. Consumers use
the exact paths declared in their skill instructions; this directory is not a
runtime discovery index.

| Resource group | Active consumers |
|---|---|
| `common/` | `calc-workflows`, `vasp-workflow`, `magnetic-workflow` |
| `vasp/` | `vasp-workflow`, `magnetic-workflow` |

`script-management` maintains and validates both groups. If a required plugin
template is missing, the plugin-template option is unavailable; an independently
approved project template remains a valid source.
