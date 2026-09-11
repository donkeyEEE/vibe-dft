# S03 — RQ interviews and Decision Tickets

The success interview uses a native input only for the real staged copy of
`calc-rq`. Byte-identical copies of `grill-with-docs`, `grilling`, and
`domain-modeling`, plus their cross-plugin dependency reference, are registered
as available dependencies so the trace must show `calc-rq` reaching them. The
missing dependency probe stages only the candidate. Ticket adoption is a
separate fresh context.

## Exact prompts

`S03-interview-required`:

> Create RQ-003 under data/01line-a/01-rqs for the question 'Does synthetic phase A remain stable under strain?'.

`S03-missing-dependency`:

> Create RQ-003 under data/01line-a/01-rqs for the question 'Does synthetic phase A remain stable under strain?'.

`S03-approved-creation`:

> Create RQ-003 after inspecting interview.md and existing sibling RQs. The structured interview is complete and its accepted answers are recorded there. I approve exactly this proposal: create data/01line-a/01-rqs/RQ-003-strain-stability/RQ.md with complete content '# Strain stability\n\nID: RQ-003\nStatus: active\n\n## Question\nDoes synthetic phase A remain stable under strain?\n\n## Boundary\nSynthetic phase A at strains -1%, 0%, and +1%; fixed input model A.\n\n## Success Criterion\nAll three strain points record result PASS under the published Spec criterion.\n\n## Decisions\n- Use fixed input model A and strains -1%, 0%, +1%.\n\n## Specs\n'; also create its empty decision-tickets and specs directories. No other RQ update is approved.

`S03-first-ticket-only`:

> Resolve the two currently decidable Tickets in data/01line-a/01-rqs/RQ-001-alpha. I approve exactly this displayed pair for DT-001 only: set decision-tickets/01-strain.md to Status: resolved with Answer 'Use strains -1%, 0%, +1%'; add exactly '- DT-001: Use strains -1%, 0%, +1%.' under RQ.md ## Decisions. I do not approve the proposed DT-002 answer or any DT-002/RQ update.

## Expected observations

- The natively loaded `calc-rq` reaches and reads the real external dependency
  chain, which asks the current interview frontier; no RQ is written before
  approval.
- With the dependency absent, RQ creation stops without a local substitute.
- The approved Ticket/RQ pair is written together; DT-002 is untouched and no
  pending/session cache appears.
