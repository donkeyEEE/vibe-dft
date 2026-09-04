# Project-owned knowledge: frozen design decisions

Status: frozen for later design; not approved for implementation

## Context

This note preserves the decisions reached while evaluating the three long-term
plugin-knowledge arrangements described in
`/tmp/yz-skills-plugin-knowledge-handoff-2026-09-04.md`. The discussion was
paused after recognizing that card selection and plugin access to project
knowledge require a separate, deeper design. Nothing in this note authorizes a
migration or changes the accepted boundary in
[`docs/adr/0001-localize-experimental-plugin-knowledge.md`](../../adr/0001-localize-experimental-plugin-knowledge.md).

## Frozen decisions

1. A future project-owned knowledge design would make the project copy the
   sole runtime authority, including calculation templates. It would not fall
   back silently to knowledge shipped by a plugin.
2. Project knowledge would use one discovery entry point with separate domain
   indexes: **统一入口、分域索引**. The proposed machine-readable entry point is
   `knowledge/INDEX.yaml`; paper, physics, calculation, and other domains would
   retain independent indexes and validation rules.
3. Skill-local `references/` would remain, but only for operational procedure,
   reasoning frameworks, input/output contracts, tool instructions, and safety
   boundaries. Domain facts, journal requirements, physical knowledge,
   calculation templates, cluster configuration, and project experience would
   belong to project knowledge.
4. The base knowledge library would be maintained in this repository and
   copied into a project by `calc-project-structure`. A separate plugin or a
   separate project-knowledge skill would not be introduced at this stage.
5. Creating a new calculation project could initialize the knowledge tree as
   part of normal project creation. Copying into or supplementing an existing
   project would require an explicit user request.
6. Supplementary initialization would be non-overwriting. Existing-name
   conflicts would be reported for a user decision; plugin upgrades would
   never update project knowledge automatically.
7. Initialization would copy the complete base knowledge workspace, including
   formal `cards/` and `templates/` and non-formal `candidates/` and
   `incubating/` areas, together with their indexes, contracts, and guidance.
8. Ordinary consumers would continue to read only resources registered in
   formal domain indexes. Candidate and incubating material would be visible
   and editable in the project but accessible only to an explicitly requested
   maintenance or promotion workflow. Promotion would require updating the
   appropriate formal index.
9. Cangjie is outside this design. Its current behavior and write target remain
   unchanged until a later design explicitly addresses knowledge authoring,
   admission, promotion, and synchronization.

## Unresolved questions

- How plugins reliably discover and consume a project's knowledge entry point.
- The query, selection, evidence-return, context-budget, and no-result contract
  for card consumption.
- Whether card selection is owned by each consuming skill or a shared router.
- How domain indexes represent enough metadata for bounded, explainable
  selection without loading an entire knowledge tree.
- How a repository base library is curated and how selected project knowledge
  might later be contributed back without violating project ownership.
- How the temporary unchanged Cangjie flow relates to a future project-owned
  model.

## Pause condition

Do not implement this model until the unresolved consumption and discovery
design has been completed and explicitly approved. A newer decision may retire
this proposal; preserve this note as the record of the paused alternative.
