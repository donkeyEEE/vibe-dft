# Card-to-skill proposal contract

Use one proposal for one exact target file. Proposals are presented in the
conversation and are not plugin assets until the user accepts them.

## PRP-NNN: concise-slug

- Source card: exact formal-card or calc-candidate-card path
- Target: one exact plugin-relative file
- Action: add | modify | deprecate
- Ownership rationale: why this owner and layer is correct
- Evidence and boundary: applicable conditions, support, and known exclusions
- Verification: exact test or validation command
- Decision: pending | accepted | rejected | implemented

### Proposed diff

```diff
...
```

Assign stable sequential `PRP-NNN` identifiers within the current request. A
proposal never combines target files: split each affected destination into its
own proposal and obtain an explicit decision for each. Implement only accepted
proposals. Never mutate a source card; Cangjie owns knowledge changes and
formal admission.

Prefer an existing reference over a new skill. Create a workflow skill only
when its independent triggering, input/output contract, and validation justify
that boundary.

## Destination routing

| Experience nature | Destination |
|---|---|
| Trigger condition, responsibility, core routing, or safety boundary | Owning `SKILL.md` |
| Detailed operation, failure mode, compatibility, parameter explanation, case, or workflow branch | Owning `references/` file |
| Reusable, deterministic, verifiable input or script | Propose it to `script-management`; route formal-template admission through Cangjie and Calc Project acceptance |
| Cross-method flow with independent trigger, input/output contract, and validation | New workflow skill |
| Project-specific or unsupported conclusion | No plugin change; route stronger evidence or a knowledge correction to Cangjie |

For a deprecation or replacement, include the migration or deprecation note in
the proposal. Never remove knowledge without its own explicit proposal and
accepted decision.
