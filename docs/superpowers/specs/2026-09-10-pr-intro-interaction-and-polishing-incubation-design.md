# PR Intro Interaction and PRL Polishing Incubation Design

## Goal

Restore a controlled paragraph-by-paragraph revision workflow for Physical
Review Introductions, move the broader `prl-polishing` skill into the Skill
Incubator, and remove plugin-level resources from Paper Project.

## Scope

This change affects only `paper-project` and `skill-incubator`. Calc Project's
calculation-template resources remain unchanged.

The completed repository must have no `plugins/paper-project/resources/`
directory. Every former Paper Project shared resource must live under the
`references/` tree of each skill that consumes it. When two skills need the
same content, each owns a local copy; there is no runtime cross-plugin file
dependency.

## PR Intro Interaction

`pr-intro` keeps its existing six-move Introduction logic, available-facts
view, source precedence, and claim boundaries. Its restructuring and drafting
workflow gains an interactive review protocol adapted from `prl-polishing`.

For input with two or more paragraphs or a complete Introduction, the default
flow is:

1. Segment the source by paragraph or, when paragraph boundaries are
   unreliable, by inferential job. Assign stable `P1`, `P2`, ... identifiers.
2. Present a revision map containing each paragraph's current role, problem,
   scope of change, intended action, and evidence risk. Do not rewrite the
   paragraphs in this phase.
3. After the map is confirmed, review one unresolved paragraph per turn unless
   the user explicitly requests a batch.
4. Preserve the complete original paragraph with stable sentence locators.
   Present independently selectable `C1`, `C2`, ... changes, each with complete
   `Before`, `After`, `Why`, and explicit decision choices.
5. Assemble a proposed paragraph only after its sentence-level changes are
   resolved. Let the user accept it, revise it, keep the original verbatim, or
   skip it.
6. Consolidate the Introduction only after paragraph decisions are resolved;
   report remaining evidence needs and material structural changes.

A single-paragraph request starts directly at paragraph review. An explicit
one-shot request may return a complete revision without intermediate approval.
The protocol must never invent content to fill a rhetorical move or evidence
gap.

The protocol will be a `pr-intro`-owned reference reached from `SKILL.md`.
Tests will assert the behavioral contract rather than exact prose formatting.

## PRL Polishing Migration

Move the complete `plugins/paper-project/skills/prl-polishing/` tree to
`plugins/skill-incubator/skills/prl-polishing/`. Preserve its name, invocation
policy, scripts, static fragments, documentation, and non-shared references.

Update repository and plugin documentation so `prl-polishing` appears only in
the Skill Incubator roster. Remove Paper Project release-builder assumptions
that require the old path. Add or update repository-layout and release tests to
prove that the source path is absent and the incubator path is valid.

The migration changes ownership, not the skill's user-visible polishing
behavior.

## Paper Project Resource Removal

The seven cards currently under `plugins/paper-project/resources/paper-writing/`
are consumed by `prl-figure` and `prl-polishing`.

- Place one copy under
  `plugins/paper-project/skills/prl-figure/references/paper-writing/` and change
  the `prl-figure` manifest to local paths.
- Place one copy under
  `plugins/skill-incubator/skills/prl-polishing/references/paper-writing/` and
  change the migrated manifest to local paths.
- Remove `plugins/paper-project/resources/`, its README, and all documentation
  or tests that describe those files as plugin-shared resources.

Existing skill-local Paper Project resources remain where they are. The
repository-level description of Paper Project will state that writing
references are skill-owned. General repository governance may continue to
permit plugin resources for other plugins; this change does not redesign Calc
Project.

## Validation

Implementation follows a red-green sequence:

1. Add contract tests that fail because `pr-intro` lacks the interactive
   protocol, `prl-polishing` remains in Paper Project, and Paper Project still
   owns plugin-level resources.
2. Add the protocol and migrate the skill and references until those tests
   pass.
3. Run the focused PR Intro contract tests, Paper Project resource/release
   tests, repository-layout tests, and any Skill Incubator tests.
4. Run the full repository test suite and validate both affected plugin
   manifests/skill trees with the repository's existing validators.
5. Inspect `git diff --check`, the final file inventory, and all remaining
   references to the old paths.

No plugin installation, marketplace publication, cachebuster update, or
external-environment modification is included.
