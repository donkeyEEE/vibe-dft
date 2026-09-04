# Dev Plugin Responsibility Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Realign `dev-productivity` around software product definition and design, and `dev-engineering` around implementation, verification and maintenance, without adding new skills or breaking cross-plugin workflow references.

**Architecture:** Move the seven design-discovery skills as intact publication units, then rewrite their fully qualified invocations and the workflows that consume them. Keep implementation-facing architecture, triage, routing and repository setup in `dev-engineering`; make dependency checks bidirectional wherever a retained engineering workflow invokes a migrated productivity skill.

**Tech Stack:** Codex plugin manifests, Markdown skills and references, YAML agent metadata, Python/pytest repository tests, official Codex plugin validator.

**Spec:** `docs/adr/0002-separate-software-design-from-engineering-delivery.md`

## Global Constraints

- Move exactly these skills from `plugins/dev-engineering/skills/` to `plugins/dev-productivity/skills/`: `domain-modeling`, `grill-with-docs`, `to-spec`, `to-tickets`, `wayfinder`, `prototype`, and `research`.
- Keep `ask-matt`, `setup-matt-pocock-skills`, `triage`, `implement`, `tdd`, `diagnosing-bugs`, `code-review`, `codebase-design`, `improve-codebase-architecture`, `resolving-merge-conflicts`, and `wizard` in `dev-engineering`.
- Do not create an additional triage, router, setup or compatibility-wrapper skill.
- Preserve skill names and invocation policy unless a namespace must change from `$dev-engineering:*` to `$dev-productivity:*`.
- Keep `CONTEXT.md` limited to plugin-domain definitions; implementation details belong in this plan and migration history.
- Preserve unrelated user changes and do not install or publish either plugin.
- Perform moves with `git mv` so file history remains traceable.

---

### Task 1: Add a repository contract for the new ownership boundary

**Files:**
- Modify: `tests/test_repository_layout.py`

**Interfaces:**
- Consumes: the accepted ownership decision in ADR 0002 and the exact move/retain lists in Global Constraints.
- Produces: `DESIGN_SKILLS`, `ENGINEERING_SKILLS`, and assertions that prevent moved skills from returning to the wrong plugin.

- [ ] **Step 1: Add the ownership sets and failing assertions**

Add these constants near the existing repository-layout constants:

```python
DESIGN_SKILLS = {
    "domain-modeling",
    "grill-with-docs",
    "prototype",
    "research",
    "to-spec",
    "to-tickets",
    "wayfinder",
}

ENGINEERING_SKILLS = {
    "ask-matt",
    "code-review",
    "codebase-design",
    "diagnosing-bugs",
    "implement",
    "improve-codebase-architecture",
    "resolving-merge-conflicts",
    "setup-matt-pocock-skills",
    "tdd",
    "triage",
    "wizard",
}
```

Add a test that asserts every name in `DESIGN_SKILLS` exists only below `plugins/dev-productivity/skills/`, and every name in `ENGINEERING_SKILLS` exists below `plugins/dev-engineering/skills/`.

- [ ] **Step 2: Add stale-namespace assertions**

Scan active `SKILL.md`, `*.md`, and `agents/openai.yaml` files under both Dev Project plugins. Assert that the seven migrated names never appear as `$dev-engineering:<name>` or as absolute links rooted at `plugins/dev-engineering/skills/<name>`; exclude `docs/migrations/` and `docs/superpowers/` because they preserve history and plans.

- [ ] **Step 3: Run the focused test and verify that it fails**

Run: `pytest -q tests/test_repository_layout.py -k 'dev_skill_ownership or dev_skill_namespaces'`

Expected: FAIL because the seven design skills still reside in `dev-engineering` and active files still use their old namespace.

- [ ] **Step 4: Commit the red contract**

```bash
git add tests/test_repository_layout.py
git commit -m "test: define dev plugin responsibility boundary"
```

### Task 2: Move the seven design skill publication units

**Files:**
- Move: `plugins/dev-engineering/skills/domain-modeling/` → `plugins/dev-productivity/skills/domain-modeling/`
- Move: `plugins/dev-engineering/skills/grill-with-docs/` → `plugins/dev-productivity/skills/grill-with-docs/`
- Move: `plugins/dev-engineering/skills/to-spec/` → `plugins/dev-productivity/skills/to-spec/`
- Move: `plugins/dev-engineering/skills/to-tickets/` → `plugins/dev-productivity/skills/to-tickets/`
- Move: `plugins/dev-engineering/skills/wayfinder/` → `plugins/dev-productivity/skills/wayfinder/`
- Move: `plugins/dev-engineering/skills/prototype/` → `plugins/dev-productivity/skills/prototype/`
- Move: `plugins/dev-engineering/skills/research/` → `plugins/dev-productivity/skills/research/`

**Interfaces:**
- Consumes: complete skill directories, including each skill's `agents/`, references, templates and scripts.
- Produces: unchanged skill-local relative layouts under the new plugin owner.

- [ ] **Step 1: Move each complete directory with Git**

Run:

```bash
git mv plugins/dev-engineering/skills/domain-modeling plugins/dev-productivity/skills/domain-modeling
git mv plugins/dev-engineering/skills/grill-with-docs plugins/dev-productivity/skills/grill-with-docs
git mv plugins/dev-engineering/skills/to-spec plugins/dev-productivity/skills/to-spec
git mv plugins/dev-engineering/skills/to-tickets plugins/dev-productivity/skills/to-tickets
git mv plugins/dev-engineering/skills/wayfinder plugins/dev-productivity/skills/wayfinder
git mv plugins/dev-engineering/skills/prototype plugins/dev-productivity/skills/prototype
git mv plugins/dev-engineering/skills/research plugins/dev-productivity/skills/research
```

- [ ] **Step 2: Verify directory completeness**

Run: `find plugins/dev-productivity/skills/{domain-modeling,grill-with-docs,to-spec,to-tickets,wayfinder,prototype,research} -type f -print | sort`

Expected: every formerly tracked file appears at the corresponding new path, including nested references and `agents/openai.yaml` files; none of the seven old directories remains.

- [ ] **Step 3: Check skill frontmatter names**

Run: `for skill in domain-modeling grill-with-docs to-spec to-tickets wayfinder prototype research; do sed -n '1,6p' "plugins/dev-productivity/skills/$skill/SKILL.md"; done`

Expected: each `name:` remains the unqualified skill name matching its directory.

- [ ] **Step 4: Commit the physical ownership change**

```bash
git add plugins/dev-engineering/skills plugins/dev-productivity/skills
git commit -m "refactor: move software design skills to productivity plugin"
```

### Task 3: Repair migrated workflows and cross-plugin dependency rules

**Files:**
- Modify: `plugins/dev-productivity/skills/grill-with-docs/SKILL.md`
- Modify: `plugins/dev-productivity/skills/wayfinder/SKILL.md`
- Modify: `plugins/dev-productivity/skills/to-spec/SKILL.md`
- Modify: `plugins/dev-productivity/skills/to-tickets/SKILL.md`
- Modify: `plugins/dev-productivity/skills/prototype/SKILL.md`
- Modify: `plugins/dev-productivity/skills/prototype/UI.md`
- Modify: `plugins/dev-productivity/skills/research/SKILL.md`
- Create: `plugins/dev-productivity/references/cross-plugin-dependencies.md`
- Modify: `plugins/dev-engineering/references/cross-plugin-dependencies.md`

**Interfaces:**
- Consumes: migrated skill locations from Task 2 and the fully qualified invocation convention.
- Produces: valid intra-plugin `$dev-productivity:*` calls and explicit, independently installable cross-plugin transitions.

- [ ] **Step 1: Rewrite migrated design namespaces**

Within the seven migrated directories, replace invocations of the moved skills as follows while preserving all invocations of retained engineering skills:

```text
$dev-engineering:domain-modeling  -> $dev-productivity:domain-modeling
$dev-engineering:grill-with-docs  -> $dev-productivity:grill-with-docs
$dev-engineering:prototype        -> $dev-productivity:prototype
$dev-engineering:research         -> $dev-productivity:research
$dev-engineering:to-spec          -> $dev-productivity:to-spec
$dev-engineering:to-tickets       -> $dev-productivity:to-tickets
$dev-engineering:wayfinder        -> $dev-productivity:wayfinder
```

Do not replace `$dev-engineering:implement`, `$dev-engineering:tdd`, `$dev-engineering:code-review`, `$dev-engineering:triage`, `$dev-engineering:codebase-design`, or other retained engineering invocations.

- [ ] **Step 2: Make `grill-with-docs` internally composed**

Update its first operational step to invoke `$dev-productivity:grilling` alongside `$dev-productivity:domain-modeling`. Remove the obsolete cross-plugin check from this step because both dependencies now share one plugin.

- [ ] **Step 3: Add productivity-to-engineering dependency guidance**

Create `plugins/dev-productivity/references/cross-plugin-dependencies.md` with the same deferred-check contract used by engineering: local steps run without probing the other plugin; only a step that explicitly invokes `$dev-engineering:<skill>` checks availability; unavailable dependencies pause only that step and report that `dev-engineering` must be installed or enabled in a new session.

- [ ] **Step 4: Repair relative dependency links**

For each migrated workflow that invokes a retained engineering skill, link to `../../references/cross-plugin-dependencies.md` at the invocation point. Check every `../../references/` link after the move and preserve skill-local links such as `./CONTEXT-FORMAT.md` unchanged.

- [ ] **Step 5: Generalize the engineering dependency reference**

Keep `plugins/dev-engineering/references/cross-plugin-dependencies.md` focused on deferred calls into `dev-productivity`, but update examples so migrated skill names use their new fully qualified invocations.

- [ ] **Step 6: Run link and namespace checks**

Run: `rg -n '\$dev-engineering:(domain-modeling|grill-with-docs|prototype|research|to-spec|to-tickets|wayfinder)' plugins/dev-engineering plugins/dev-productivity`

Expected: no matches.

Run: `find plugins/dev-engineering plugins/dev-productivity -type l -xtype l -print`

Expected: no broken symbolic links.

- [ ] **Step 7: Commit the repaired design workflows**

```bash
git add plugins/dev-engineering/references plugins/dev-productivity
git commit -m "fix: repair cross-plugin design workflow references"
```

### Task 4: Rewire retained engineering orchestration

**Files:**
- Modify: `plugins/dev-engineering/skills/ask-matt/SKILL.md`
- Modify: `plugins/dev-engineering/skills/ask-matt/PHASE-BOUNDARIES.md`
- Modify: `plugins/dev-engineering/skills/improve-codebase-architecture/SKILL.md`
- Modify: `plugins/dev-engineering/skills/triage/SKILL.md`
- Modify: `plugins/dev-engineering/skills/setup-matt-pocock-skills/domain.md`
- Modify: `plugins/dev-engineering/skills/setup-matt-pocock-skills/issue-tracker-github.md`
- Modify: `plugins/dev-engineering/skills/setup-matt-pocock-skills/issue-tracker-gitlab.md`
- Modify: `plugins/dev-engineering/skills/setup-matt-pocock-skills/issue-tracker-local.md`

**Interfaces:**
- Consumes: the new `$dev-productivity:*` design invocations and both cross-plugin dependency contracts.
- Produces: an engineering-owned end-to-end router and setup flow that defer safely when the independently installable design plugin is unavailable.

- [ ] **Step 1: Update the `ask-matt` routing graph**

Route domain modeling, documented grilling, research, prototypes, specifications, tickets and wayfinding to their `$dev-productivity:*` names. Keep implementation, TDD, review, debugging, codebase design, architecture improvement, triage, merge-conflict resolution and wizard routes under `$dev-engineering:*`.

- [ ] **Step 2: Mark each newly cross-plugin transition**

At the first design transition in each `ask-matt`, architecture-improvement, triage or setup branch, apply `plugins/dev-engineering/references/cross-plugin-dependencies.md`: preserve completed local artifacts, check only when the invocation is reached, and pause only the dependent step if `dev-productivity` is unavailable.

- [ ] **Step 3: Update setup documentation and tracker templates**

Change `/domain-modeling`, `/grill-with-docs`, `/to-spec`, `/to-tickets`, `/wayfinder`, `/prototype`, and `/research` references to fully qualified `$dev-productivity:*` invocations. Keep `/triage` and engineering execution references under `$dev-engineering:*`.

- [ ] **Step 4: Run the ownership and namespace contract**

Run: `pytest -q tests/test_repository_layout.py -k 'dev_skill_ownership or dev_skill_namespaces'`

Expected: PASS.

- [ ] **Step 5: Commit orchestration updates**

```bash
git add plugins/dev-engineering tests/test_repository_layout.py
git commit -m "refactor: route design work through productivity plugin"
```

### Task 5: Align plugin metadata and skill navigation

**Files:**
- Modify: `plugins/dev-engineering/.codex-plugin/plugin.json`
- Modify: `plugins/dev-productivity/.codex-plugin/plugin.json`
- Modify: `plugins/dev-engineering/skills/README.md`
- Modify: `plugins/dev-productivity/skills/README.md`

**Interfaces:**
- Consumes: the final physical ownership and routing graph from Tasks 2–4.
- Produces: discovery metadata and human navigation that describe the same boundary as `CONTEXT.md`.

- [ ] **Step 1: Rewrite `dev-productivity` metadata**

Set its manifest description, short description, long description, keywords and default prompt around software product definition, requirements and solution design, including interview, domain modeling, research, prototyping, specification and work decomposition. Retain collaboration-support capabilities such as handoff, teaching, questionnaires, clarification and agent-facing documentation without calling the plugin “general productivity.”

- [ ] **Step 2: Rewrite `dev-engineering` metadata**

Set its manifest description, short description, long description, keywords and default prompt around implementation, testing, debugging, review, request triage, code architecture and maintenance. Mention that it can route into the independently installable design plugin, but do not claim ownership of the migrated skills.

- [ ] **Step 3: Rebuild both skill indexes**

List only physically present skills in each `skills/README.md`. Describe `codebase-design` as implementation-facing module/interface design and `triage` as engineering verification of incoming work; describe the seven moved skills as product-definition and design-discovery workflows.

- [ ] **Step 4: Check JSON and index parity**

Run: `python -m json.tool plugins/dev-engineering/.codex-plugin/plugin.json`

Run: `python -m json.tool plugins/dev-productivity/.codex-plugin/plugin.json`

Run: `for plugin in dev-engineering dev-productivity; do comm -3 <(find "plugins/$plugin/skills" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort) <(rg -o '\./[^/)]+/SKILL\.md' "plugins/$plugin/skills/README.md" | sed -E 's#\./([^/]+)/SKILL\.md#\1#' | sort); done`

Expected: both JSON commands exit 0 and both `comm` comparisons produce no output.

- [ ] **Step 5: Commit metadata and navigation**

```bash
git add plugins/dev-engineering plugins/dev-productivity
git commit -m "docs: align dev plugin metadata with responsibilities"
```

### Task 6: Validate both independently installable plugins and record migration

**Files:**
- Modify: `docs/migrations/2026-09-04-plugin-consolidation.md`
- Modify: `tests/test_repository_layout.py` only if validation exposes an incomplete contract

**Interfaces:**
- Consumes: the completed directory moves, namespace rewrites and metadata updates.
- Produces: independently valid plugin packages and an auditable record of the runtime-path change.

- [ ] **Step 1: Run the full repository structure suite**

Run: `PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider tests/test_repository_layout.py`

Expected: PASS with zero failures.

- [ ] **Step 2: Validate each plugin package**

Run: `python3 /home/donk/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/dev-engineering`

Run: `python3 /home/donk/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/dev-productivity`

Expected: both validators exit 0.

- [ ] **Step 3: Audit stale paths and invocations**

Run: `rg -n 'plugins/dev-engineering/skills/(domain-modeling|grill-with-docs|prototype|research|to-spec|to-tickets|wayfinder)|\$dev-engineering:(domain-modeling|grill-with-docs|prototype|research|to-spec|to-tickets|wayfinder)' --glob '!docs/migrations/**' --glob '!docs/superpowers/**' .`

Expected: no active-path matches.

- [ ] **Step 4: Record the completed runtime-path migration**

Append a dated section to `docs/migrations/2026-09-04-plugin-consolidation.md` listing the seven moves, the retained engineering skills, the cross-plugin reference changes, validation commands and exact results. Do this only after Steps 1–3 pass; describe failures as open work rather than completed migration.

- [ ] **Step 5: Review the scoped diff and commit**

Run: `git diff --check`

Run: `git status --short`

Expected: no whitespace errors; only the files named in this plan and the pre-existing user changes appear.

```bash
git add docs/migrations/2026-09-04-plugin-consolidation.md tests/test_repository_layout.py
git commit -m "docs: record dev plugin responsibility migration"
```
