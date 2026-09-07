---
status: accepted
---

# Use directory rosters and invocation policy

The repository does not assign lifecycle states to skills. Each plugin's
`skills/*/SKILL.md` directories are its roster and all included skills may ship
in that plugin's release; an `agents/openai.yaml` entry with
`allow_implicit_invocation: false` is a runtime invocation policy, not a
lifecycle state. Skill Incubator is an installable, publishable general
experimentation boundary, and the maintainer decides case by case whether a
skill stays there or becomes an independent plugin. Adding and removing skills
uses ordinary code review without a lifecycle transition, baseline audit, or
migration log.

This decision supersedes lifecycle registry, state-transition, deletion-gate,
and migration-log requirements in ADRs 0003–0006 while preserving their other
architectural decisions and historical wording.
