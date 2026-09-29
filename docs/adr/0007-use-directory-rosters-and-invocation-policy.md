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

This decision replaces earlier lifecycle registry, state-transition,
deletion-gate, and migration-log requirements while preserving the resource
ownership, plugin boundary, and upstream engineering-skill decisions.
