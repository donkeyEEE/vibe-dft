# Productivity

General workflow tools, not code-specific.

## Explicit-only

Codex does not select these implicitly. Invoke them deliberately as `$skill-name`; each sets `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.

- **[grill-me](./grill-me/SKILL.md)** — Get relentlessly interviewed about a plan or design until every branch of the design tree is resolved.
- **[handoff](./handoff/SKILL.md)** — Compact the current conversation into a handoff document so another agent can continue the work.
- **[teach](./teach/SKILL.md)** — Teach the user a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace.
- **[to-questionnaire](./to-questionnaire/SKILL.md)** — Turn a decision you can't answer alone into a Markdown questionnaire for the one person who can — filled in async, or together over a meeting.
- **[wait-what](./wait-what/SKILL.md)** — Fire this the moment a message doesn't land. The agent re-pitches it in plain English using the relevant `CONTEXT.md`, resolved through `CONTEXT-MAP.md` when needed.

## Model-invoked

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[grilling](./grilling/SKILL.md)** — Interview the user in clearly separated question rounds until every branch of a plan, decision, or idea is resolved.
- **[writing-for-agents](./writing-for-agents/SKILL.md)** — Write and review Codex skills, AGENTS.md, plugin metadata, and any operational document an agent reaches by a pointer.
