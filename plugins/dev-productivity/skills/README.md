# Product Definition and Design

Software discovery, definition, solution-design, and supporting collaboration workflows.

## Explicit-only

Codex does not select these implicitly. Invoke them deliberately as `$skill-name`; each sets `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.

- **[grill-me](./grill-me/SKILL.md)** — Get relentlessly interviewed about a plan or design until every branch of the design tree is resolved.
- **[grill-with-docs](./grill-with-docs/SKILL.md)** — Resolve a design through interview while maintaining its domain glossary and durable decisions.
- **[handoff](./handoff/SKILL.md)** — Compact the current conversation into a handoff document so another agent can continue the work.
- **[teach](./teach/SKILL.md)** — Teach the user a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace.
- **[to-questionnaire](./to-questionnaire/SKILL.md)** — Turn a decision you cannot answer alone into a questionnaire for the person who can.
- **[to-spec](./to-spec/SKILL.md)** — Synthesize resolved product and solution decisions into a specification.
- **[to-tickets](./to-tickets/SKILL.md)** — Decompose an approved design into tracer-bullet tickets with explicit blocking edges.
- **[wait-what](./wait-what/SKILL.md)** — Re-pitch a message in plain language using the relevant domain context.
- **[wayfinder](./wayfinder/SKILL.md)** — Resolve the decision map for work too large or uncertain for one session.

## Model-invoked

Codex can select these from ordinary task wording; each also remains explicitly invokable.

- **[domain-modeling](./domain-modeling/SKILL.md)** — Sharpen product-domain language and maintain `CONTEXT.md` and durable architectural decisions.
- **[grilling](./grilling/SKILL.md)** — Interview the user in rounds until every branch of a plan or design is resolved.
- **[prototype](./prototype/SKILL.md)** — Build throwaway logic or UI artifacts that answer a design question.
- **[research](./research/SKILL.md)** — Investigate a design question against primary sources and capture cited findings.
- **[writing-for-agents](./writing-for-agents/SKILL.md)** — Write and review Codex skills, AGENTS.md, plugin metadata, and operational documents agents consume.
