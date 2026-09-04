# Localize Plugin Knowledge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the top-level experimental `research-knowledge` dependency with optional knowledge assets owned and shipped by `paper-project` and `calc-project`.

**Architecture:** Paper writing and journal cards move to `plugins/paper-project/knowledge`; calculation templates and physics cards move to `plugins/calc-project/knowledge`; ontology material moves to `plugins/calc-project/knowledge/incubating` and stays outside formal consumer indexes. Consumers resolve paths relative to their own `knowledge-source.yaml`, and the top-level source is removed after all references and tests move.

**Tech Stack:** Markdown skill contracts, YAML source descriptors, Python/pytest repository tests.

**Spec:** `docs/adr/0001-localize-experimental-plugin-knowledge.md`

## Global Constraints

- Shared knowledge remains an optional, fail-open enhancement for consuming skills.
- Cangjie remains developer-only; this migration does not define its future write, admission, promotion, or governance model.
- Ontology is incubating content and must not appear in a formal consumer index.
- No compatibility copy or fallback remains at top-level `research-knowledge/`.
- Preserve unrelated user worktree changes; do not commit, install, or publish.

---

### Task 1: Lock the target repository boundary

**Files:**
- Modify: `tests/test_repository_layout.py`
- Test: `tests/test_repository_layout.py`

**Interfaces:**
- Consumes: ADR 0001 migration mapping.
- Produces: repository-level assertions for the two plugin-local roots and removal of the top-level root.

- [x] Add a test asserting both plugin-local knowledge entry points exist, ontology is under calc `incubating`, and top-level `research-knowledge` is absent.
- [x] Run the new test and verify it fails because the old layout still exists.
- [x] Continue to Task 2; its content relocation is the minimal implementation that turns this test green.

### Task 2: Relocate content and preserve formal/incubating visibility

**Files:**
- Create: `plugins/paper-project/knowledge/CONSUMER_CONTRACT.md`
- Create: `plugins/paper-project/knowledge/cards/INDEX.md`
- Move: `research-knowledge/cards/atoms/` to `plugins/paper-project/knowledge/cards/atoms/`
- Create: `plugins/calc-project/knowledge/CONSUMER_CONTRACT.md`
- Create: `plugins/calc-project/knowledge/cards/INDEX.md`
- Move: `research-knowledge/cards/physics/` to `plugins/calc-project/knowledge/cards/physics/`
- Move: `research-knowledge/templates/` to `plugins/calc-project/knowledge/templates/`
- Move: `research-knowledge/candidates/cards/calc-project/` to `plugins/calc-project/knowledge/candidates/cards/calc-project/`
- Move: `research-knowledge/candidates/templates/` to `plugins/calc-project/knowledge/candidates/templates/`
- Move: `research-knowledge/cards/ontology/` and `research-knowledge/candidates/cards/ontology/` to `plugins/calc-project/knowledge/incubating/ontology/`

**Interfaces:**
- Consumes: current formal indexes and consumer contract.
- Produces: independent plugin-local knowledge trees; formal calc index exposes physics but not ontology.

- [x] Move the assets without changing card or template bodies.
- [x] Split the primary index so paper exposes only writing/journal atoms and calc exposes physics.
- [x] Retain the fail-open and candidate exclusion contract in each plugin-local root.
- [x] Run the Task 1 test and verify the target layout is green.

### Task 3: Repoint every runtime consumer

**Files:**
- Modify: all `plugins/{paper-project,calc-project}/skills/*/references/knowledge-source.yaml`
- Modify: active `SKILL.md`, references, READMEs, script indexes, and Cangjie developer documentation that names the old root.
- Modify: `plugins/paper-project/scripts/build_marketplace_release.py`
- Modify: `plugins/paper-project/skills/prl-shared/scripts/validate_knowledge_repository.py`

**Interfaces:**
- Consumes: `path` relative to each source descriptor with `relative_to: this_file`.
- Produces: portable plugin-local lookup with no active absolute or top-level shared path.

- [x] Add a repository test that resolves every source descriptor from its own directory and verifies its local contract/index exists.
- [x] Run it and verify failure against the absolute descriptors.
- [x] Rewrite descriptors and active instructions to plugin-local paths; keep Cangjie explicitly developer-only and avoid specifying future governance.
- [x] Narrow the paper validator to the paper knowledge schema and update release-bundle checks to include paper knowledge.
- [x] Run the source-resolution and paper validator tests until green.

### Task 4: Move knowledge tests to their owners

**Files:**
- Move/adapt: `research-knowledge/tests/*` to `plugins/paper-project/tests/knowledge/` and `plugins/calc-project/tests/knowledge/`

**Interfaces:**
- Consumes: plugin-local formal and incubating trees.
- Produces: owner-local tests for card inventories, template inventories, index resolution, contract behavior, and ontology incubation.

- [x] Move the existing tests to owner-local suites and run them; resolve the observed duplicate-module collection failure before evaluating assertions.
- [x] Adapt the existing repository tests without weakening inventory, frontmatter, index, candidate, or acceptance assertions.
- [x] Verify paper and calc knowledge suites pass independently.

### Task 5: Remove the obsolete boundary and update operational documentation

**Files:**
- Remove: `research-knowledge/`
- Modify: `CONTEXT.md`
- Modify: `CONTEXT-MAP.md`
- Modify: `docs/migrations/2026-09-04-plugin-consolidation.md`
- Modify: `docs/adr/0001-localize-experimental-plugin-knowledge.md` only if implementation details reveal a contradiction.

**Interfaces:**
- Consumes: completed local trees and green owner-local tests.
- Produces: one authoritative description of the implemented dependency direction and a migration audit trail.

- [x] Remove the empty old tree after confirming every tracked resource has a destination.
- [x] Update context and dependency mapping to describe plugin-local optional knowledge and ontology incubation.
- [x] Record exact migration mapping and verification commands in the migration log without rewriting its historical record.
- [x] Scan active files for the old absolute paths and top-level runtime references; allow only migration history and explicit regression-test constants.

### Task 6: Full verification

**Files:**
- Verify all files changed by Tasks 1–5.

**Interfaces:**
- Consumes: completed migration.
- Produces: fresh evidence for repository structure, both knowledge libraries, validators, manifests, and absence of obsolete runtime dependencies.

- [x] Run `git diff --check`.
- [x] Run repository layout plus both plugin knowledge test suites with pytest caches and bytecode disabled.
- [x] Run the paper knowledge validator against `plugins/paper-project/knowledge`.
- [x] Run official plugin validation for `calc-project` and `paper-project`.
- [x] Inspect `git status`, old-path scans, and source/destination inventories; confirm unrelated dirty changes remain untouched.
