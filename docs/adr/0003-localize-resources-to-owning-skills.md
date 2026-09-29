---
status: accepted
---

# Localize resources to owning skills

Plugin-level knowledge repositories introduced descriptors, dynamic indexes,
formal states, governance operations, and dormant content that current skills
did not need. The repository removes that model. A resource used by one skill
is co-located with its owner; only resources with at least two active consumers
live under the plugin's `resources/` source area. Consumers name exact relative
paths rather than discovering resources through a generic contract.

Unconsumed resources and the old knowledge-state machinery were removed.
`prl-shared` and `calc-skill-distillation` were retired. Cangjie remains an
explicit-only entry point whose legacy material is non-executable historical
input.
