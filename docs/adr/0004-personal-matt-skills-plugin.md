---
status: accepted
---

# Maintain a personal Matt Skills plugin

Supersedes: ADR 0002.

The user wants one personally selected Codex adaptation of Matt Pocock's skills, with workflows that can evolve for personal needs and selective upstream updates. `plugins/matt-skills/` is the publication unit. Product design, engineering delivery and collaboration remain navigation categories within that plugin.

The initial consolidation retains all 25 skills and their current lifecycle states and invocation policies. Qualified calls use `$matt-skills:<skill>`. Workflows reach sibling skills directly, so separate-plugin installation checks no longer apply. Skill selection and workflow redesign are later changes governed by the existing lifecycle rules.

The plugin retains upstream provenance and the MIT license. This source change does not install, publish or modify an external marketplace. Historical path mappings and baseline verification are recorded only in the migration log.
