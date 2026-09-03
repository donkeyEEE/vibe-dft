# Skill mechanics

The skill-specific branch of [`writing-for-agents`](SKILL.md): what changes when the document is a skill — frontmatter, the invocation choice, and router skills. Everything else about writing it is the universal reference in `SKILL.md`.

## Invocation

Codex supports explicit and implicit skill activation:

- A **model-invoked** skill uses the default `policy.allow_implicit_invocation: true`. Omit the `policy` field, and write a concise `description` carrying the trigger branches so Codex can match it to a task. It also remains explicitly reachable as `$skill-name`.
- An **explicit-only** skill sets `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. Codex does not select it from description matching, but explicit `$skill-name` invocation still works. Its required `description` stays concise and useful in the skill selector without promising automatic activation.

Pick model-invocation when Codex should recognize the workflow from ordinary task wording. Pick explicit-only when starting the workflow must be a deliberate invocation, such as a destructive release cutover or a user-controlled mode switch.

Every `SKILL.md` keeps only the required `name` and `description` frontmatter. Put Codex-specific metadata beside it in `agents/openai.yaml`:

```yaml
interface:
  display_name: "Release Cutover"
  short_description: "Run a deliberate release cutover"
  default_prompt: "$release-cutover Prepare and execute this release cutover."

policy:
  allow_implicit_invocation: false
```

The same file may declare required MCP tools under `dependencies.tools`. Keep workflow steps in `SKILL.md`; a dependency makes a tool available but does not explain how to use it.

## Splitting by invocation

The invocation cut of splitting (the sequence cut lives in `SKILL.md`): split off a model-invoked skill when a distinct task branch should trigger it on its own and can be expressed as a focused description. Split off an explicit-only skill when the branch needs a deliberate `$skill-name` boundary. Each extra skill adds discovery and maintenance load, so the independent entry point must earn the split.

## Router skills

When explicit-only skills multiply past what a user can remember, a **router skill** can name the available workflows and recommend the exact `$skill-name` for each branch. A router does not claim that Codex will implicitly activate an explicit-only skill; it presents the explicit next invocation to the user.
