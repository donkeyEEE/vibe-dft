# S03 — RQ interviews and accepted decisions

The success interview uses a native input only for the real staged copy of
`calc-rq`. Byte-identical copies of `grill-with-docs`, `grilling`, and
`domain-modeling`, plus their cross-plugin dependency reference, are registered
as available dependencies so the trace must show `calc-rq` reaching them. The
missing dependency probe stages only the candidate. A direct decision update is
a separate fresh context.

## Exact prompts

`S03-interview-required`:

> Create RQ-003 under data/01line-a/01-rqs for the question 'Does synthetic phase A remain stable under strain?'.

`S03-missing-dependency`:

> Create RQ-003 under data/01line-a/01-rqs for the question 'Does synthetic phase A remain stable under strain?'.

`S03-approved-creation`:

> Create RQ-003 after inspecting interview.md and existing sibling RQs. The structured interview is complete and its accepted answers are recorded there. I approve exactly this proposal: create data/01line-a/01-rqs/RQ-003-strain-stability/RQ.md with complete content '# Strain stability\n\nID: RQ-003\nStatus: active\n\n## Question\nDoes synthetic phase A remain stable under strain?\n\nBoundary: Synthetic phase A at strains -1%, 0%, and +1%; fixed input model A.\n\n## Success Criterion\nAll three strain points record result PASS under the published Spec criterion.\n\n## Specs\n\n## Decisions\n- Use fixed input model A and strains -1%, 0%, +1%.\n\n## Context\n'; also create its empty specs directory. No other RQ update is approved.

`S03-approved-decision-update`:

> For data/01line-a/01-rqs/RQ-001-alpha, I answer the unresolved strain question with 'Use strains -1%, 0%, +1%'. Propose the exact RQ.md ## Decisions update. I approve adding exactly '- Use strains -1%, 0%, +1%.' and no other RQ change.

`S03-unanswered-question`:

> For data/01line-a/01-rqs/RQ-001-alpha, determine the strain range, but I have not answered which range to use.

## Expected observations

- The natively loaded `calc-rq` reaches and reads the real external dependency
  chain, which asks the current interview frontier; no RQ is written before
  approval.
- With the dependency absent, RQ creation stops without a local substitute.
- An answered question produces one exact proposed `RQ.md` `## Decisions`
  update; after approval that RQ write is the only decision authority.
- An unanswered question remains in the conversation and produces no separate
  question file, ID, dependency graph, pending cache, or RQ mutation.
