# PR Intro Interaction and PRL Polishing Incubation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add controlled paragraph review to `pr-intro`, move `prl-polishing` to Skill Incubator, and eliminate `plugins/paper-project/resources/` by localizing every paper-writing reference.

**Architecture:** `pr-intro` receives a small, skill-owned interaction protocol while retaining its Introduction-specific evidence logic. `prl-polishing` moves intact to Skill Incubator and becomes self-contained. The former shared cards are copied into each surviving consumer's `references/paper-writing/` tree, and every manifest resolves only skill-local paths.

**Tech Stack:** Markdown skill contracts, YAML manifests, Python/pytest repository and release tests, Codex plugin JSON manifests.

**Spec:** `docs/superpowers/specs/2026-09-10-pr-intro-interaction-and-polishing-incubation-design.md`

## Global Constraints

- Scope is limited to `paper-project` and `skill-incubator`; Calc Project resources remain unchanged.
- No `plugins/paper-project/resources/` directory may remain.
- No runtime path may cross from one plugin into another.
- `pr-intro` retains its six-move logic, available-facts view, and source boundaries.
- `prl-polishing` retains its existing user-visible behavior after migration.
- Do not install, publish, reinstall, or update plugin cachebusters.

---

### Task 1: Lock the Desired Repository and Skill Contracts

**Files:**
- Modify: `plugins/paper-project/tests/pr_intro/test_skill_contract.py`
- Modify: `plugins/paper-project/tests/resources/test_card_library.py`
- Modify: `plugins/paper-project/tests/resources/test_resource_release.py`
- Modify: `plugins/skill-incubator/tests/test_plugin_boundary.py`
- Modify: `plugins/skill-incubator/tests/test_release.py`
- Modify: `tests/test_repository_layout.py`

**Interfaces:**
- Consumes: current filesystem layout, skill entrypoints, YAML manifests, release archives.
- Produces: executable assertions for the new ownership and interaction contracts.

- [ ] **Step 1: Add a failing PR Intro interaction contract test**

Assert that `SKILL.md` points to an existing interaction protocol and that the
protocol defines stable `P<n>` paragraph IDs, a revision map, one-paragraph
review, complete original text, selectable `C<n>` changes with `Before`,
`After`, and `Why`, paragraph decisions, delayed consolidation,
and single-paragraph and explicit one-shot routes.

- [ ] **Step 2: Add failing ownership and migration tests**

Assert that Paper Project has no `resources/` directory or `prl-polishing`
skill; Skill Incubator contains `prl-polishing`; both migrated/localized
manifests point to existing local files and contain no `../../resources/`
paths; the seven former shared cards exist in both owning reference trees.

- [ ] **Step 3: Update release assertions to describe the target packages**

Paper Project archives must contain `pr-intro` and localized `prl-figure`
cards but not `prl-polishing` or `resources/`. Skill Incubator archives must
contain `prl-polishing`, its manifest, static protocol, script, and localized
cards.

- [ ] **Step 4: Run the focused tests and verify RED**

Run:

```bash
pytest plugins/paper-project/tests/pr_intro/test_skill_contract.py plugins/paper-project/tests/resources/test_card_library.py plugins/paper-project/tests/resources/test_resource_release.py plugins/skill-incubator/tests/test_plugin_boundary.py plugins/skill-incubator/tests/test_release.py tests/test_repository_layout.py -q
```

Expected: failures specifically report the missing PR Intro protocol, old
`prl-polishing` location, and retained Paper Project resources.

### Task 2: Add the PR Intro Interactive Review Protocol

**Files:**
- Create: `plugins/paper-project/skills/pr-intro/references/writing/interaction-protocol.md`
- Modify: `plugins/paper-project/skills/pr-intro/SKILL.md`
- Modify: `plugins/paper-project/skills/pr-intro/README.md`

**Interfaces:**
- Consumes: `pr-introduction-logic.md`, `source-boundaries.md`, user draft and decisions.
- Produces: stable paragraph/change identifiers and a confirmed consolidated Introduction.

- [ ] **Step 1: Write the skill-owned protocol**

Adapt the existing polishing protocol to Introduction work. Define paragraph
segmentation, Phase A revision map, Phase B located selectable changes,
sentence and change locators, decision locking, delayed paragraph assembly,
final consolidation, single-paragraph review, and explicit direct mode. Omit
`prl-polishing`-specific material-library and style-habit requirements.

- [ ] **Step 2: Route ordinary PR Intro work through the protocol**

Add the exact local reference path to `SKILL.md`; require the protocol after
building the available-facts view and paragraph argument map. Preserve the
maintenance-only route and anti-fabrication constraints.

- [ ] **Step 3: Document the user-visible interaction**

Update the skill README to describe the numbered map, selectable changes,
per-paragraph decisions, and one-shot override.

- [ ] **Step 4: Run the PR Intro contract tests and verify GREEN**

Run:

```bash
pytest plugins/paper-project/tests/pr_intro/test_skill_contract.py -q
```

Expected: all PR Intro contract tests pass.

### Task 3: Move PRL Polishing and Localize Paper-Writing Cards

**Files:**
- Move: `plugins/paper-project/skills/prl-polishing/` to `plugins/skill-incubator/skills/prl-polishing/`
- Move/copy: `plugins/paper-project/resources/paper-writing/write-prl-*.md`
- Modify: `plugins/skill-incubator/skills/prl-polishing/manifest.yaml`
- Modify: `plugins/paper-project/skills/prl-figure/manifest.yaml`
- Delete: `plugins/paper-project/resources/paper-writing/README.md`
- Delete: `plugins/paper-project/resources/`

**Interfaces:**
- Consumes: seven existing shared evidence cards and both consumer manifests.
- Produces: two self-contained skills whose manifest paths resolve within their own plugin trees.

- [ ] **Step 1: Move the complete PRL Polishing tree**

Use a filesystem move so Git records the existing files as renames. Preserve
all files and metadata under the skill directory.

- [ ] **Step 2: Localize each former shared card to both consumers**

Place byte-equivalent copies of all seven cards under both
`prl-figure/references/paper-writing/` and migrated
`prl-polishing/references/paper-writing/`, then remove Paper Project's shared
resource tree.

- [ ] **Step 3: Replace shared manifest paths with local paths**

Change every `../../resources/paper-writing/<name>.md` entry in both manifests
to `references/paper-writing/<name>.md`. Confirm all declared paths exist when
resolved relative to the skill root.

- [ ] **Step 4: Run ownership tests and verify GREEN**

Run:

```bash
pytest plugins/paper-project/tests/resources/test_card_library.py plugins/skill-incubator/tests/test_plugin_boundary.py -q
```

Expected: localized inventories and path-resolution assertions pass.

### Task 4: Repair Documentation, Governance, and Release Boundaries

**Files:**
- Modify: `AGENTS.md`
- Modify: `CONTEXT.md`
- Modify: `README.md`
- Modify: `plugins/paper-project/README.md`
- Modify: `plugins/skill-incubator/README.md`
- Modify: `plugins/paper-project/scripts/build_marketplace_release.py`
- Modify: `plugins/paper-project/tests/resources/test_resource_release.py`
- Modify: `plugins/skill-incubator/tests/test_release.py`
- Modify: `tests/test_repository_layout.py`
- Inspect: `docs/adr/0003-localize-resources-to-owning-skills.md`

**Interfaces:**
- Consumes: final skill roster and localized resource layout.
- Produces: accurate navigation, governance, and independently buildable release archives.

- [ ] **Step 1: Update navigation and plugin descriptions**

Remove `prl-polishing` from Paper Project and add it to Skill Incubator. Update
root links and invocation examples to the new namespace/path.

- [ ] **Step 2: Update Paper Project resource governance**

State that Paper Project writing resources are skill-owned and remove active
references to `plugins/paper-project/resources`. Preserve the repository's
general rule and Calc Project resource design.

- [ ] **Step 3: Update release validation logic**

Remove Paper Project builder requirements for the old polishing and resource
paths. Ensure the existing generic Skill Incubator builder packages the moved
skill without special exclusions.

- [ ] **Step 4: Run release and repository tests and verify GREEN**

Run:

```bash
pytest plugins/paper-project/tests/resources/test_resource_release.py plugins/skill-incubator/tests/test_release.py tests/test_repository_layout.py -q
```

Expected: both archives and repository layout match the new boundaries.

### Task 5: Full Verification and Completion Audit

**Files:**
- Inspect: all modified files and generated temporary release archives.

**Interfaces:**
- Consumes: completed implementation.
- Produces: fresh evidence for every design requirement.

- [ ] **Step 1: Run all affected plugin tests**

```bash
pytest plugins/paper-project/tests plugins/skill-incubator/tests tests/test_repository_layout.py -q
```

- [ ] **Step 2: Run the full repository suite**

```bash
pytest -q
```

- [ ] **Step 3: Validate all changed skill and plugin entrypoints**

Run `quick_validate.py` for `pr-intro`, migrated `prl-polishing`, and
`prl-figure`, then run `validate_plugin.py` for `plugins/paper-project` and
`plugins/skill-incubator`.

- [ ] **Step 4: Audit paths and diffs**

```bash
test ! -e plugins/paper-project/resources
test ! -e plugins/paper-project/skills/prl-polishing
test -e plugins/skill-incubator/skills/prl-polishing/SKILL.md
rg -n 'plugins/paper-project/resources|\.\./\.\./resources|paper-project:prl-polishing' AGENTS.md CONTEXT.md README.md plugins tests
git diff --check
git status --short
```

Expected: the existence checks pass; the search returns no active stale
references; the diff has no whitespace errors; only task-scoped changes remain.

- [ ] **Step 5: Review requirements against current-state evidence**

Confirm every design section has direct filesystem, manifest, documentation,
and test evidence. Do not install or publish either plugin.
