# Skill Resource Localization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace both plugin knowledge repositories with explicit skill-owned and demonstrably shared resources while removing knowledge support operations and freezing Cangjie.

**Architecture:** Consumers link exact skill-local or plugin-shared resources; there is no repository descriptor, global runtime index, or formal/candidate/incubating protocol. Paper writing references and calculation templates are moved before the old trees are deleted, and repository tests enforce link, sharing, packaging, and stale-path rules.

**Tech Stack:** Markdown skill instructions, YAML manifests, shell/PBS templates, Python 3/pytest repository tests, Codex plugin validator.

**Spec:** `docs/superpowers/specs/2026-09-04-skill-resource-localization-design.md`

## Global Constraints

- Preserve unrelated user changes and commit only files in this task.
- A resource used by one skill belongs under that skill; plugin `resources/` requires at least two named active consumers.
- Agent-readable guidance uses `references/`; task-copy sources use `assets/templates/` or the shared calculation-template source.
- Active consumers name exact files and do not use generic repository discovery.
- Remove all non-formal knowledge and all unconsumed formal resources.
- Keep Cangjie installed but frozen and non-writing; its legacy material is explicitly non-executable.
- Do not install, publish, modify external repositories, or rewrite external environments.

---

### Task 1: Encode the target repository contract

**Files:**
- Modify: `tests/test_repository_layout.py`

**Interfaces:**
- Consumes: target paths and retirement rules from the approved spec.
- Produces: repository-level assertions used by every later task.

- [ ] **Step 1: Replace knowledge-layout tests with failing resource tests**

Add assertions that both `plugins/*/knowledge` directories are absent; the eight paper shared files, shared common/VASP templates, and magnetic assets exist; `prl-shared` and `calc-skill-distillation` are absent; and Cangjie's `SKILL.md` remains present.

- [ ] **Step 2: Add shared-consumer and stale-active-path tests**

Parse each shared `README.md` table and require at least two existing skill consumers per resource group. Scan active plugin files while excluding `cangjie-skill/references/legacy/` and require no `knowledge-source.yaml`, `/knowledge/`, candidate, incubating, admission, or promotion dependencies.

- [ ] **Step 3: Run the focused tests and verify RED**

Run: `PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider tests/test_repository_layout.py`

Expected: failures report missing target resources and existing knowledge paths.

- [ ] **Step 4: Commit the failing contract tests**

Run:

```bash
git add tests/test_repository_layout.py
git commit -m "test: define localized plugin resource contract"
```

### Task 2: Localize Paper Project resources

**Files:**
- Create: `plugins/paper-project/resources/paper-writing/README.md`
- Create: eight shared Markdown resources under `plugins/paper-project/resources/paper-writing/`
- Create: skill-owned resources under `plugins/paper-project/skills/prl-polishing/references/knowledge/`
- Create: two figure resources under `plugins/paper-project/skills/prl-figure/references/knowledge/`
- Modify: `plugins/paper-project/skills/prl-polishing/SKILL.md`
- Modify: `plugins/paper-project/skills/prl-polishing/manifest.yaml`
- Modify: `plugins/paper-project/skills/prl-figure/SKILL.md`
- Modify: `plugins/paper-project/skills/prl-figure/manifest.yaml`
- Modify: `plugins/paper-project/skills/paper2ppt/SKILL.md`
- Modify: `plugins/paper-project/skills/paper2ppt/manifest.yaml`
- Test: `plugins/paper-project/tests/knowledge/test_card_library.py`

**Interfaces:**
- Consumes: exact retained files named in the spec and current card contents.
- Produces: direct relative resource links and a shared-resource consumer declaration.

- [ ] **Step 1: Rewrite paper resource tests for target paths**

Replace index/frontmatter discovery tests with exact expected-file sets, valid frontmatter checks, relative-link resolution, and assertions that the shared README names `prl-polishing`, `prl-figure`, and `paper2ppt` where applicable.

- [ ] **Step 2: Run the paper tests and verify RED**

Run: `PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider plugins/paper-project/tests/knowledge/test_card_library.py`

Expected: failures identify missing `resources/paper-writing` and skill-local files.

- [ ] **Step 3: Move the retained resources without editing their evidence content**

Use `apply_patch` moves. Put the eight shared files at the shared path, all currently loaded polishing-only cards at `prl-polishing/references/knowledge/`, and the two figure-only cards at `prl-figure/references/knowledge/`. Do not move Nature Communications cards.

- [ ] **Step 4: Replace dynamic selection with exact load lists**

Update the three consumer skills and manifests so their load instructions link exact files. Preserve the current warn-and-continue behavior for optional shared writing resources. Remove all knowledge descriptor and index instructions.

- [ ] **Step 5: Run the paper tests and verify GREEN**

Run: `PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider plugins/paper-project/tests/knowledge/test_card_library.py`

Expected: PASS.

- [ ] **Step 6: Commit Paper Project resource localization**

Run:

```bash
git add plugins/paper-project/resources plugins/paper-project/skills/prl-polishing plugins/paper-project/skills/prl-figure plugins/paper-project/skills/paper2ppt plugins/paper-project/tests/knowledge/test_card_library.py
git commit -m "refactor(paper): localize active writing resources"
```

### Task 3: Localize Calc Project templates

**Files:**
- Create: `plugins/calc-project/resources/calculation-templates/README.md`
- Create: common and VASP template sources under `plugins/calc-project/resources/calculation-templates/`
- Create: Wannier90, TB2J, and VAMPIRE sources under `plugins/calc-project/skills/magnetic-workflow/assets/templates/`
- Modify: `plugins/calc-project/skills/calc-workflows/SKILL.md`
- Modify: `plugins/calc-project/skills/calc-workflows/references/template-copy-preflight.md`
- Modify: `plugins/calc-project/skills/vasp-workflow/SKILL.md`
- Modify: `plugins/calc-project/skills/magnetic-workflow/SKILL.md`
- Modify: `plugins/calc-project/skills/script-management/SKILL.md`
- Modify: `plugins/calc-project/skills/script-management/references/templating-from-completed-workflow.md`
- Modify: any affected references under those skills containing old template paths
- Test: `plugins/calc-project/tests/knowledge/test_calculation_templates.py`

**Interfaces:**
- Consumes: current accepted template bytes and copy-name convention that removes `.template`.
- Produces: explicit shared and magnetic-owned template paths maintained by `script-management`.

- [ ] **Step 1: Rewrite calculation-template tests for the new ownership model**

Assert exact target rosters, retained bytes/shebangs, shared consumer declarations, magnetic ownership, and absence of a global formal template index.

- [ ] **Step 2: Run the template tests and verify RED**

Run: `PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider plugins/calc-project/tests/knowledge/test_calculation_templates.py`

Expected: failures identify missing shared and magnetic-owned paths.

- [ ] **Step 3: Move accepted template sources**

Use `apply_patch` moves: common and VASP to plugin resources; Wannier90, TB2J, and VAMPIRE to magnetic assets. Move `ACCEPTANCE.md` into the shared calculation-template source and rewrite it as the validation contract for both shared and magnetic-owned locations.

- [ ] **Step 4: Update routing, copying, and maintenance instructions**

Use exact relative paths. `calc-workflows` routes only; `vasp-workflow` reads shared VASP files; `magnetic-workflow` reads shared common/VASP plus its own assets; `script-management` validates all explicit sources without candidate or promotion behavior.

- [ ] **Step 5: Run the template tests and verify GREEN**

Run: `PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider plugins/calc-project/tests/knowledge/test_calculation_templates.py`

Expected: PASS.

- [ ] **Step 6: Commit Calc Project template localization**

Run:

```bash
git add plugins/calc-project/resources plugins/calc-project/skills/calc-workflows plugins/calc-project/skills/vasp-workflow plugins/calc-project/skills/magnetic-workflow plugins/calc-project/skills/script-management plugins/calc-project/tests/knowledge/test_calculation_templates.py
git commit -m "refactor(calc): localize calculation templates"
```

### Task 4: Freeze Cangjie and retire knowledge support skills

**Files:**
- Modify: `plugins/paper-project/skills/cangjie-skill/SKILL.md`
- Modify: `plugins/paper-project/skills/cangjie-skill/agents/openai.yaml`
- Create: `plugins/paper-project/skills/cangjie-skill/references/legacy/README.md`
- Move: existing `methodology/`, `extractors/`, templates, scripts, and explanatory READMEs needed only by the old behavior under `references/legacy/`
- Delete: `plugins/paper-project/skills/prl-shared/`
- Delete: `plugins/calc-project/skills/calc-skill-distillation/`
- Modify: plugin READMEs or rosters that list the retired skills
- Test: `tests/test_repository_layout.py`

**Interfaces:**
- Consumes: approved frozen behavior.
- Produces: an installed Cangjie entry point that reports suspension and performs no writes.

- [ ] **Step 1: Add assertions for frozen Cangjie behavior**

Require active `SKILL.md` to state that resource writes are suspended, forbid executable path references outside `references/legacy/`, and require the legacy notice to say its contents are historical and non-executable.

- [ ] **Step 2: Run the focused Cangjie/roster tests and verify RED**

Run: `PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider tests/test_repository_layout.py -k 'resource or cangjie or skill'`

Expected: failures identify active legacy instructions and retired skill directories.

- [ ] **Step 3: Freeze Cangjie and archive old behavior**

Replace active instructions with a concise non-writing suspension response. Move old implementation material under `references/legacy/`, add the warning README, and update its user interface metadata consistently.

- [ ] **Step 4: Delete the two retired support skills and update rosters**

Remove `prl-shared` and `calc-skill-distillation`, then update Paper marketplace expected/public skill sets and plugin documentation that enumerate them.

- [ ] **Step 5: Run focused tests and verify GREEN**

Run: `PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider tests/test_repository_layout.py -k 'resource or cangjie or skill'`

Expected: PASS.

- [ ] **Step 6: Commit the frozen/retired workflows**

Run:

```bash
git add plugins/paper-project/skills/cangjie-skill plugins/paper-project/skills/prl-shared plugins/calc-project/skills/calc-skill-distillation plugins/paper-project/scripts/build_marketplace_release.py plugins/paper-project/README.md plugins/calc-project/README.md tests/test_repository_layout.py
git commit -m "refactor: retire knowledge support workflows"
```

### Task 5: Remove the old repositories and update packaging tests

**Files:**
- Delete: `plugins/paper-project/knowledge/`
- Delete: `plugins/calc-project/knowledge/`
- Delete: obsolete knowledge contract/card/ontology tests
- Rename or modify: retained resource tests under both plugin test suites
- Modify: `plugins/paper-project/scripts/build_marketplace_release.py`
- Modify: marketplace release tests that assert bundle contents
- Modify: `tests/test_repository_layout.py`

**Interfaces:**
- Consumes: migrated target files from Tasks 2-4.
- Produces: packages and tests with no knowledge-repository compatibility path.

- [ ] **Step 1: Add release and absence assertions before deletion**

Require the Paper bundle to include shared and skill-owned resources, frozen Cangjie, and no `knowledge/` or `prl-shared`. Require Calc's source tree to contain only the new template paths.

- [ ] **Step 2: Run package/layout tests and verify RED**

Run: `PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider tests/test_repository_layout.py plugins/paper-project/tests`

Expected: failures report old directories or old release requirements.

- [ ] **Step 3: Remove old repositories, descriptors, and obsolete tests**

Delete both knowledge trees only after confirming all retained target files exist. Remove every remaining `knowledge-source.yaml` and knowledge-only validator/test. Preserve historical documentation and Cangjie legacy files.

- [ ] **Step 4: Update the Paper release contract**

Replace required knowledge files with the exact shared resources, skill-local references, and frozen Cangjie entry point. Keep skill-roster and checksum validation intact.

- [ ] **Step 5: Run package/layout tests and verify GREEN**

Run: `PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider tests/test_repository_layout.py plugins/paper-project/tests`

Expected: PASS.

- [ ] **Step 6: Commit repository removal and packaging changes**

Run:

```bash
git add plugins/paper-project plugins/calc-project tests/test_repository_layout.py
git commit -m "refactor: remove plugin knowledge repositories"
```

### Task 6: Update ownership documentation and migration history

**Files:**
- Modify: `AGENTS.md`
- Modify: `CONTEXT.md`
- Create: `docs/adr/0003-localize-resources-to-owning-skills.md`
- Modify: `docs/migrations/2026-09-04-plugin-consolidation.md`

**Interfaces:**
- Consumes: final implemented paths and deletion counts.
- Produces: current ownership guidance plus an immutable historical migration record.

- [ ] **Step 1: Add failing documentation assertions**

Update repository tests to require `skill-owned resources`, plugin `resources/`, ADR 0003, the migration-log entry, and no current-context links to plugin `knowledge/`.

- [ ] **Step 2: Run documentation tests and verify RED**

Run: `PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider tests/test_repository_layout.py -k 'context or agents or resource'`

Expected: failures identify the old ownership wording and missing ADR.

- [ ] **Step 3: Update current guidance and ADR**

Define skill-owned and plugin-shared resources in `CONTEXT.md`; update `AGENTS.md` routing and rules; write ADR 0003 with status accepted and an explicit `Supersedes: ADR 0001` relation.

- [ ] **Step 4: Append the exact migration record**

Record resource moves, retired skills/contracts/tests, Cangjie freeze, deleted formal/non-formal counts, branch, and validation results without rewriting earlier history.

- [ ] **Step 5: Run documentation tests and verify GREEN**

Run: `PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider tests/test_repository_layout.py -k 'context or agents or resource'`

Expected: PASS.

- [ ] **Step 6: Commit documentation**

Run:

```bash
git add AGENTS.md CONTEXT.md docs/adr/0003-localize-resources-to-owning-skills.md docs/migrations/2026-09-04-plugin-consolidation.md tests/test_repository_layout.py
git commit -m "docs: record skill resource ownership"
```

### Task 7: Verify both plugin releases and the repository

**Files:**
- Modify only files needed to fix failures within the approved scope.

**Interfaces:**
- Consumes: all prior task outputs.
- Produces: final evidence that source, packages, links, and tests agree.

- [ ] **Step 1: Scan active paths**

Run targeted `rg` scans over active plugin source for `knowledge-source.yaml`, `/knowledge/`, `candidates/`, `incubating/`, admission, and promotion terms. Manually classify only historical documents and Cangjie legacy matches as permitted.

- [ ] **Step 2: Run repository and plugin test suites**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider tests/test_repository_layout.py plugins/paper-project/tests plugins/calc-project/tests
```

Expected: PASS.

- [ ] **Step 3: Run official plugin validators**

Run the official `validate_plugin.py` separately for `plugins/paper-project` and `plugins/calc-project`.

Expected: both pass.

- [ ] **Step 4: Build and inspect the Paper marketplace release**

Build into a fresh `/tmp` directory using the existing release script, run its bundle contract, and verify the archive contains every referenced resource and no retired knowledge/support path.

- [ ] **Step 5: Review the final diff and commit fixes**

Run `git diff --check`, `git status --short`, and `git diff --stat` against the design commit. Commit only necessary in-scope fixes with message `fix: complete resource localization verification` when any exist.
