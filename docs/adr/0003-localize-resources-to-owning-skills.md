---
status: accepted
supersedes: ADR 0001
---

# Localize resources to owning skills

Supersedes: ADR 0001

Plugin-level knowledge repositories introduced descriptors, dynamic indexes,
formal states, governance operations, and dormant content that current skills
did not need. The repository removes that model. A resource used by one skill
is co-located with its owner; only resources with at least two active consumers
live under the plugin's `resources/` source area. Consumers name exact relative
paths rather than discovering resources through a generic contract.

All candidate and incubating material and all unconsumed formal resources are
removed. `prl-shared` and `calc-skill-distillation` are retired. Cangjie remains
as an explicit-only frozen entry point whose legacy material is non-executable
historical input for a future redesign.
