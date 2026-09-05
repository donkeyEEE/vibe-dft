# Matt Skills 技能导航

从 Matt Pocock 上游选用并为 Codex 适配的个人技能集合。产品设计与工程交付是导航分组，共用一个插件和 `$matt-skills:<skill>` 调用前缀。

当前保留 22 个技能；个人精选已处理十项，后续继续分批确认和改写流程。状态以 [skill-lifecycle.json](../skill-lifecycle.json) 为准；下表中的显式入口仍为停用状态，仅由用户显式调用。

## 需求设计与协作

### 仅显式调用

Codex does not select these implicitly. Invoke them deliberately as `$skill-name`; each sets `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.

- **[handoff](./handoff/SKILL.md)** — Compact the current conversation into a handoff document so another agent can continue the work.
- **[teach](./teach/SKILL.md)** — Teach the user a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace.
- **[to-questionnaire](./to-questionnaire/SKILL.md)** — Turn a decision you cannot answer alone into a questionnaire for the person who can.
- **[wait-what](./wait-what/SKILL.md)** — Re-pitch a message in plain language using the relevant domain context.

### 已发布，可自动选用

Codex can select these from ordinary task wording; each also remains explicitly invokable.

- **[domain-modeling](./domain-modeling/SKILL.md)** — Sharpen product-domain language and maintain `CONTEXT.md` and durable architectural decisions.
- **[grill-me](./grill-me/SKILL.md)** — Get relentlessly interviewed about a plan or design until every branch of the design tree is resolved.
- **[grill-with-docs](./grill-with-docs/SKILL.md)** — Resolve a design through interview while maintaining its domain glossary and durable decisions.
- **[grilling](./grilling/SKILL.md)** — Interview the user in rounds until every branch of a plan or design is resolved.
- **[prototype](./prototype/SKILL.md)** — Build throwaway logic or UI artifacts that answer a design question.
- **[research](./research/SKILL.md)** — Investigate a design question against primary sources and capture cited findings.
- **[writing-for-agents](./writing-for-agents/SKILL.md)** — Write and review Codex skills, AGENTS.md, plugin metadata, and operational documents agents consume.

## 工程交付

### 仅显式调用

Codex runs these only through deliberate invocation; each sets `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.

- **[ask-matt](./ask-matt/SKILL.md)** — Route work across design, engineering, and collaboration skills in this plugin.
- **[code-review](./code-review/SKILL.md)** — Review a change against repository standards and its originating specification.
- **[tdd](./tdd/SKILL.md)** — Implement behavior through red-green-refactor slices.
- **[implement](./implement/SKILL.md)** — Build a specification or ticket with TDD and code-review gates.
- **[setup-matt-pocock-skills](./setup-matt-pocock-skills/SKILL.md)** — Configure issue tracking, triage labels, and domain-document conventions.
- **[triage](./triage/SKILL.md)** — Classify and technically verify incoming bugs, feature requests, and pull requests.

### 已发布，可自动选用

Codex can select these from ordinary task wording; each also remains explicitly invokable.

- **[improve-codebase-architecture](./improve-codebase-architecture/SKILL.md)** — Find and design codebase-deepening opportunities.
- **[codebase-design](./codebase-design/SKILL.md)** — Design implementation-facing module interfaces, seams, adapters, and test surfaces.
- **[diagnosing-bugs](./diagnosing-bugs/SKILL.md)** — Diagnose hard bugs and performance regressions through a tight feedback loop.
- **[resolving-merge-conflicts](./resolving-merge-conflicts/SKILL.md)** — Resolve an in-progress merge or rebase conflict by intent.
- **[wizard](./wizard/SKILL.md)** — Generate a guided Bash workflow for infrastructure steps only a human can perform.
