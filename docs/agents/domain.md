# Domain Docs

Before exploring the codebase, engineering skills should read:

- `CONTEXT.md` at the repository root
- Relevant ADRs under `docs/adr/`

Missing files should not block work or trigger suggestions to create them prematurely.

## File structure

This repository uses a single-context layout:

```text
/
├── CONTEXT.md
└── docs/adr/
```

Use terminology defined in `CONTEXT.md`, including its explicitly preferred and avoided terms. If work contradicts an existing ADR, surface that conflict explicitly rather than silently overriding the decision.
