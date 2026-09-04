# Skill Resource Localization Design

Status: approved in conversation; pending written-spec review

## Purpose

Remove the plugin-level project-knowledge runtime and maintenance model from
`paper-project` and `calc-project`. Retain only resources consumed by current
workflows, place single-skill resources with their owning skill, and keep only
demonstrably shared resources in a small plugin-level source area.

This design supersedes the current ownership and runtime-path decision in ADR
0001. It does not implement the frozen project-owned knowledge alternative.

## Design principles

1. A resource used by one skill belongs under that skill.
2. A resource used by two or more skills may live under plugin-level
   `resources/`; the consumers must be named and tested.
3. Agent-readable explanatory material belongs under `references/`. Files
   copied into calculation tasks belong under `assets/` or the shared
   calculation-template source.
4. Consumers name exact files. There is no generic repository descriptor,
   formal index discovery, or repository-wide selection protocol.
5. Unconsumed resources and all non-formal knowledge are removed rather than
   retained as dormant compatibility data.
6. Historical records may describe retired paths, but active source and tests
   must not depend on them.

## Target modules and interfaces

### Skill-owned resources

A skill-owned resource is internal to that skill's module. Its interface is an
explicit relative link from the skill's active instructions or manifest. A
missing skill-owned resource is a packaging defect.

Explanatory Markdown moves under the owner's `references/`. Task-copy template
files move under the owner's `assets/templates/`.

### Plugin-shared resources

Shared resources live under `plugins/<plugin>/resources/<resource-kind>/`.
There is no generic consumer contract. Each consumer links the exact resources
it needs, while a maintenance-only `README.md` records each resource's purpose
and its two or more consumers.

The shared module earns its seam only where duplication would otherwise return
to multiple callers. Tests reject shared resources without two declared active
consumers.

Optional shared writing resources warn and allow the workflow to continue when
unavailable. A missing calculation template disables that plugin-template
choice; it does not prevent use of an independently approved project template.

## Paper Project disposition

### Shared paper-writing resources

Move these eight cards to `plugins/paper-project/resources/paper-writing/`:

- `write-terminology-ledger`
- `write-prl-model-to-validation-pairing`
- `write-prl-figure-prerequisite-signature-consequence`
- `write-prl-quantitative-claim-with-criterion`
- `write-prl-main-text-supplement-evidence-allocation`
- `write-prl-prediction-condition-observable-bridge`
- `write-prl-mechanism-control-comparator`
- `write-prl-computational-sensitivity-as-result`

Their consumers are the applicable combination of `prl-polishing`,
`prl-figure`, and `paper2ppt` already demonstrated by current instructions.

### Skill-owned paper resources

Move cards loaded only by `prl-polishing` to that skill's `references/` and
move the two figure-only Physical Review preparation resources to
`prl-figure/references/`. Preserve resource content and update the consuming
instructions to exact relative links.

Delete the seven Nature Communications cards because no active skill consumes
them. Do not add implicit consumption to `nature-response` as part of this
migration.

### Cangjie

Retain `cangjie-skill` as a named future design entry point, but freeze its
current behavior. Its active `SKILL.md` must state that writing and governance
are suspended and must not modify resources. Move useful current methodology
to `references/legacy/` with an explicit non-executable historical notice.
Remove active dependencies on knowledge indexes, candidates, cross-plugin
writes, admission, promotion, and knowledge-repository validation.

Delete `prl-shared`; it exists only to support the retired knowledge governance
model.

## Calc Project disposition

Move the common calculation templates to
`plugins/calc-project/resources/calculation-templates/common/`.

Move VASP templates to
`plugins/calc-project/resources/calculation-templates/vasp/` because both
`vasp-workflow` and the complete magnetic workflow use them.

Move Wannier90, TB2J, and VAMPIRE templates to
`plugins/calc-project/skills/magnetic-workflow/assets/templates/`. They are
owned by the complete magnetic pipeline.

Retain `script-management`, but change it to maintain and validate these
explicit resource locations. It no longer manages formal status, candidates,
promotion, or a knowledge repository. Change `calc-workflows` to route work
without loading a global template index.

Delete `calc-skill-distillation`, whose interface depends entirely on formal
and candidate knowledge cards.

Delete all 39 formal physics cards because no current calculation workflow
consumes them. Cangjie's index reference is governance behavior, not runtime
physics consumption.

## Removed support operations

Delete both plugin `knowledge/` trees, including:

- all `candidates/` and `incubating/` content, indexes, and placeholders;
- unconsumed formal resources;
- formal card and template indexes;
- `CONSUMER_CONTRACT.md` and knowledge README files;
- every `knowledge-source.yaml` descriptor;
- admission, promotion, and formal/candidate/incubating state rules;
- knowledge-repository validation scripts and knowledge-specific tests;
- release assertions that require a knowledge repository.

The ontology incubator contains 40 cards and 24 candidates. All 24 candidate
files duplicate same-named card files byte for byte. The entire incubator is
removed as unconsumed and outside Calc Project's domain.

## Migration sequence

1. Add tests for the target resource paths and explicit-reference rules.
2. Copy retained resources to their target locations without changing content.
3. Update consuming skills, manifests, template-copy rules, validation, and
   release packaging.
4. Freeze Cangjie and preserve only clearly marked historical methodology.
5. Remove retired skills, descriptors, contracts, indexes, tests, and both
   knowledge trees.
6. Update repository guidance, context, ADRs, and migration history.
7. Run path scans, repository tests, plugin tests, package validation, and
   release-content validation.

Deletion happens only after new locations and consumers pass their targeted
tests.

## Documentation changes

- Add a new ADR that supersedes ADR 0001 without rewriting that historical
  decision.
- Update `AGENTS.md` and `CONTEXT.md` to describe skill-owned resources and the
  narrowly admitted plugin-shared resource source.
- Append exact moves and deletions to
  `docs/migrations/2026-09-04-plugin-consolidation.md`.
- Preserve frozen and historical specifications as records; exclude them from
  active-path regression scans.

## Verification

Tests must establish that:

- every active skill and manifest resource link resolves;
- every plugin-shared resource declares at least two active consumers;
- consumers reference only their declared shared resources;
- calculation templates retain expected content, copy names, and executable
  behavior;
- both plugin release packages include all referenced resources;
- active files contain no `knowledge/`, `knowledge-source.yaml`, candidate,
  incubating, admission, or promotion protocol dependencies;
- historical repository documents and Cangjie's explicitly non-executable
  `references/legacy/` material are the only allowed old-path matches;
- both official plugin validators and scope-appropriate plugin/repository test
  suites pass.

## Out of scope

- Redesigning or reactivating Cangjie.
- Creating a project-owned knowledge system.
- Adding new resource consumers based only on topical relevance.
- Installing or publishing plugins, changing external repositories, or
  rewriting external environments.
- Unrelated Dev Project plugin changes.
