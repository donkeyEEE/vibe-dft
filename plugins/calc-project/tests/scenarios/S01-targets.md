# S01 — Targets and explicit invocation

Each probe uses a fresh ephemeral `gpt-5.6-sol` thread and a byte-identical,
read-only candidate copy. `S01-ordinary-control` supplies no native skill input;
the other probes supply `calc-project:calc-execute` with its exact candidate path.

## Exact prompts

`S01-ambiguous`:

> Execute SPEC-001 now.

`S01-exact-path`:

> Inspect and resolve exactly data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-alpha.md, then report its parent and status. Do not advance beyond inspection in this request.

`S01-ordinary-control`:

> Please advance the ready calculation Spec at data/01line-a/01-rqs/RQ-001-alpha/specs/SPEC-001-alpha.md.

## Expected observations

- The bare ID finds two legal RQ-local `SPEC-001` objects, asks for the parent,
  and writes nothing.
- The exact path resolves only the Alpha Spec and writes nothing because the
  request is inspection-only.
- The ordinary-text control has no `type: skill` input, does not read or invoke
  any candidate Calc skill, and changes no file. Path-level thread overrides
  disable installed legacy Calc skills without disabling the candidate copy.
