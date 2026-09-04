# Engineering Delivery

Implementation, verification, and maintenance workflows for defined software work.

## Explicit-only

Codex runs these only through deliberate invocation; each sets `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.

- **[ask-matt](./ask-matt/SKILL.md)** — Route work across the engineering flow and into the independently installable design plugin when needed.
- **[implement](./implement/SKILL.md)** — Build a specification or ticket with TDD and code-review gates.
- **[improve-codebase-architecture](./improve-codebase-architecture/SKILL.md)** — Find and design codebase-deepening opportunities.
- **[setup-matt-pocock-skills](./setup-matt-pocock-skills/SKILL.md)** — Configure issue tracking, triage labels, and domain-document conventions.
- **[triage](./triage/SKILL.md)** — Classify and technically verify incoming bugs, feature requests, and pull requests.

## Model-invoked

Codex can select these from ordinary task wording; each also remains explicitly invokable.

- **[code-review](./code-review/SKILL.md)** — Review a change against repository standards and its originating specification.
- **[codebase-design](./codebase-design/SKILL.md)** — Design implementation-facing module interfaces, seams, adapters, and test surfaces.
- **[diagnosing-bugs](./diagnosing-bugs/SKILL.md)** — Diagnose hard bugs and performance regressions through a tight feedback loop.
- **[resolving-merge-conflicts](./resolving-merge-conflicts/SKILL.md)** — Resolve an in-progress merge or rebase conflict by intent.
- **[tdd](./tdd/SKILL.md)** — Implement behavior through red-green-refactor slices.
- **[wizard](./wizard/SKILL.md)** — Generate a guided Bash workflow for infrastructure steps only a human can perform.
