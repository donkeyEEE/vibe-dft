# Presentation Skill Incubator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move `paper2ppt` and `ppt-master` from Paper Project into an independently installable `skill-incubator` plugin without breaking their handoff, release integrity, or lifecycle history.

**Architecture:** The two presentation skills, PPT Master maintenance assets, and presentation release builder move together into `plugins/skill-incubator/`. Paper Project keeps its research and writing workflows and a slimmed release contract. Root navigation and marketplace metadata expose four plugins, while `CONTEXT.md` remains unchanged by explicit user decision.

**Tech Stack:** Codex plugin JSON, Markdown/YAML skill metadata, Python release and synchronization scripts, pytest, Git.

**Spec:** `docs/adr/0006-separate-presentation-skills-into-incubator.md`

## Global Constraints

- `paper2ppt` and `ppt-master` remain `published`; relocation cannot reverse lifecycle history.
- `paper2ppt` continues to invoke sibling `$ppt-master` after publishing its material handoff.
- `paper2ppt` continues to use the separately installed `paper-project:liteparse` for source normalization.
- The terminology-ledger input becomes skill-owned inside `paper2ppt`; no runtime path reaches back into Paper Project resources.
- PPT Master attribution, upstream provenance, and integrity checks remain byte-for-byte complete except for required path and owning-plugin metadata changes.
- `CONTEXT.md` is not modified.
- `tests/` and `docs/superpowers/` remain ignored and untracked.

---

### Task 1: Establish the Skill Incubator plugin boundary

**Files:**
- Create: `plugins/skill-incubator/.codex-plugin/plugin.json`
- Create: `plugins/skill-incubator/skill-lifecycle.json`
- Create: `plugins/skill-incubator/README.md`
- Move: `plugins/paper-project/skills/paper2ppt/` → `plugins/skill-incubator/skills/paper2ppt/`
- Move: `plugins/paper-project/skills/ppt-master/` → `plugins/skill-incubator/skills/ppt-master/`
- Modify: `plugins/paper-project/skill-lifecycle.json`
- Test: `plugins/skill-incubator/tests/test_plugin_boundary.py`

**Interfaces:**
- Consumes: the accepted ADR and the two published skill trees.
- Produces: an independently valid plugin named `skill-incubator` with lifecycle roster `{paper2ppt, ppt-master}`.

- [ ] **Step 1: Add a failing boundary test**

  Assert that the new manifest name is `skill-incubator`, both skills exist only under the new plugin, both lifecycle values are `published`, `paper2ppt/manifest.yaml` resolves `consumer_skill`, and Paper Project no longer lists either skill.

- [ ] **Step 2: Run the boundary test and confirm it fails because the new plugin does not exist**

  Run: `PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider plugins/skill-incubator/tests/test_plugin_boundary.py`

- [ ] **Step 3: Move the skill directories and create the plugin manifest, lifecycle registry, and README**

  Use plugin version `0.1.0`, retain both published states, and describe the plugin as the presentation incubator containing the academic adapter and PPT runtime.

- [ ] **Step 4: Remove the two entries from Paper Project lifecycle metadata**

- [ ] **Step 5: Run the boundary test and both plugin validators**

  Run: `PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider plugins/skill-incubator/tests/test_plugin_boundary.py`

  Run: `python3 /home/donk/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/skill-incubator`

  Run: `python3 /home/donk/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/paper-project`

### Task 2: Localize Paper2PPT resources and repair runtime paths

**Files:**
- Create: `plugins/skill-incubator/skills/paper2ppt/references/paper-writing/write-terminology-ledger.md`
- Modify: `plugins/skill-incubator/skills/paper2ppt/manifest.yaml`
- Modify: `plugins/skill-incubator/skills/paper2ppt/README.md`
- Modify: `plugins/skill-incubator/skills/paper2ppt/README_EN.md`
- Modify: `plugins/skill-incubator/skills/paper2ppt/static/core/toolchain.md`
- Modify: `plugins/skill-incubator/skills/paper2ppt/workflows/paper-to-deck.md`
- Modify: `plugins/skill-incubator/skills/paper2ppt/workflows/failure-recovery.md`
- Modify: `plugins/paper-project/resources/paper-writing/README.md`
- Test: `plugins/skill-incubator/tests/test_plugin_boundary.py`

**Interfaces:**
- Consumes: Paper Project's existing terminology-ledger reference and the `paper-project:liteparse` public skill name.
- Produces: a self-contained presentation plugin whose only cross-plugin runtime dependency is the explicitly named `paper-project:liteparse` skill.

- [ ] **Step 1: Extend the test to reject paths into `plugins/paper-project` and require the local terminology-ledger file**

- [ ] **Step 2: Run the new assertions and confirm the old shared-resource path fails**

- [ ] **Step 3: Copy the terminology ledger into Paper2PPT ownership and update its manifest**

- [ ] **Step 4: Update user-facing text to describe `paper-project:liteparse` as an external plugin dependency and PPT Master as the bundled sibling**

- [ ] **Step 5: Remove `paper2ppt` from the Paper Project shared-resource consumer list and run the boundary test**

### Task 3: Move PPT Master maintenance and release ownership

**Files:**
- Move: `plugins/paper-project/scripts/sync_ppt_master_skill.py` → `plugins/skill-incubator/scripts/sync_ppt_master_skill.py`
- Move: `plugins/paper-project/scripts/ppt_master_provenance.json` → `plugins/skill-incubator/scripts/ppt_master_provenance.json`
- Move: `plugins/paper-project/templates/ppt-master-openai.yaml` → `plugins/skill-incubator/templates/ppt-master-openai.yaml`
- Create: `plugins/skill-incubator/scripts/build_marketplace_release.py`
- Modify: `plugins/paper-project/scripts/build_marketplace_release.py`
- Modify: `plugins/paper-project/tests/resources/test_resource_release.py`
- Create: `plugins/skill-incubator/tests/test_release.py`

**Interfaces:**
- Consumes: the current Paper Project release builder and PPT Master synchronization contract.
- Produces: separate Paper Project and Skill Incubator release archives, each containing only its own lifecycle roster and assets.

- [ ] **Step 1: Add release tests requiring presentation assets in the incubator archive and forbidding them in the Paper Project archive**

- [ ] **Step 2: Run the release tests and confirm the ownership assertions fail**

- [ ] **Step 3: Move the sync script, provenance, and overlay; change owning-plugin validation from `paper-project` to `skill-incubator`**

- [ ] **Step 4: Adapt a Skill Incubator release builder with marketplace name `skill-incubator-release`, bundle directory `skill-incubator-marketplace`, and plugin path `./plugins/skill-incubator`**

- [ ] **Step 5: Remove presentation-specific required files and prose from the Paper Project release builder**

- [ ] **Step 6: Run both release-test suites, both attribution guards, and both plugin validators**

### Task 4: Update repository navigation, installation, and lifecycle history

**Files:**
- Modify: `.agents/plugins/marketplace.json`
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `plugins/paper-project/README.md`
- Modify: `docs/migrations/2026-09-04-plugin-consolidation.md`
- Modify locally only: `tests/test_repository_layout.py`

**Interfaces:**
- Consumes: the final four-plugin tree and lifecycle registries.
- Produces: correct installation commands, routing descriptions, and a historical record of both published-skill relocations.

- [ ] **Step 1: Add `skill-incubator` to the root marketplace after Paper Project**

- [ ] **Step 2: Move presentation navigation and installation text from the Paper Project section into a new Skill Incubator section**

- [ ] **Step 3: Add the plugin to `AGENTS.md` navigation without changing `CONTEXT.md`**

- [ ] **Step 4: Record old and new paths, unchanged published states, plugin versions, ownership changes, and validation evidence in the migration log**

- [ ] **Step 5: Update the ignored local repository-layout test so local verification recognizes four manifests while exempting Skill Incubator from the unchanged `CONTEXT.md` coverage assertion**

### Task 5: Verify and commit the completed migration

**Files:**
- Verify: all files changed in Tasks 1–4

**Interfaces:**
- Consumes: the complete migrated source tree.
- Produces: one reviewable commit with no stale old paths and no changes to `CONTEXT.md`.

- [ ] **Step 1: Scan active source for stale presentation paths and unresolved relative references**

  Run: `rg -n 'plugins/paper-project/skills/(paper2ppt|ppt-master)|skills/paper-project/(paper2ppt|ppt-master)' AGENTS.md README.md plugins docs/migrations`

- [ ] **Step 2: Run the complete local test suite without generating caches**

  Run: `PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider`

- [ ] **Step 3: Validate all four plugins and run `git diff --check`**

- [ ] **Step 4: Confirm `git diff -- CONTEXT.md` is empty and ignored directories remain untracked**

- [ ] **Step 5: Review the lifecycle change against commit `5e43eb2` and confirm it contains two relocations with unchanged `published` state, not deletions from active scope**

- [ ] **Step 6: Commit the migration**

  Run: `git commit -m "refactor: move presentation skills to incubator"`
