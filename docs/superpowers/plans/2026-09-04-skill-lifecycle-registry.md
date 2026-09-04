# Skill Lifecycle Registry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one machine-readable lifecycle registry to every plugin and enforce the agreed `development`, `published`, and `explicit-only` states in repository and release validation.

**Architecture:** Each plugin owns a root-level `skill-lifecycle.json` whose `skills` object maps every bundled Skill name to exactly one current state. Repository tests enforce complete roster coverage and ensure `explicit-only` agrees with `agents/openai.yaml`; the Paper Project release builder consumes and packages the same registry instead of introducing another roster source.

**Tech Stack:** JSON, Python standard library, pytest, existing Paper Project release builder.

**Spec:** `CONTEXT.md` section “技能生命周期”

## Global Constraints

- A Skill has no independent version number.
- Allowed states are exactly `development`, `published`, and `explicit-only`.
- State transitions are `development -> published <-> explicit-only`.
- `explicit-only` requires `policy.allow_implicit_invocation: false`; explicit invocation remains available.
- Deletion is not a state, and a Skill must be `explicit-only` before deletion.
- Current state belongs in the registry; transition history belongs in `docs/migrations/`.
- Preserve unrelated worktree changes; do not install or publish plugins.

---

### Task 1: Define and validate plugin lifecycle registries

**Files:**
- Create: `plugins/calc-project/skill-lifecycle.json`
- Create: `plugins/dev-engineering/skill-lifecycle.json`
- Create: `plugins/dev-productivity/skill-lifecycle.json`
- Create: `plugins/osm-project/skill-lifecycle.json`
- Create: `plugins/paper-project/skill-lifecycle.json`
- Modify: `tests/test_repository_layout.py`

**Interfaces:**
- Consumes: plugin directories selected by `EXPECTED_PLUGINS`; Skill directories matching `skills/*/SKILL.md`; invocation policy in `skills/<name>/agents/openai.yaml`.
- Produces: schema version `1`; `skills: {"<skill-name>": "<state>"}`; repository-wide roster and policy validation.

- [x] **Step 1: Write the failing registry-presence and schema test**

Add constants and helpers to `tests/test_repository_layout.py`:

```python
SKILL_STATES = {"development", "published", "explicit-only"}


def load_skill_lifecycle(plugin_root: Path) -> dict[str, str]:
    path = plugin_root / "skill-lifecycle.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["schema_version"] == 1
    skills = data["skills"]
    assert isinstance(skills, dict)
    assert set(skills.values()) <= SKILL_STATES
    return skills
```

Add a test which, for every `EXPECTED_PLUGINS` entry, asserts that registry keys exactly equal the directory names under `skills/*/SKILL.md`.

- [x] **Step 2: Run the new test and verify it fails because registries are absent**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider tests/test_repository_layout.py -k lifecycle
```

Expected: FAIL because `skill-lifecycle.json` does not exist.

- [x] **Step 3: Add the five initial registries**

Use this exact shape:

```json
{
  "schema_version": 1,
  "skills": {
    "skill-name": "published"
  }
}
```

Initialize every Skill whose `agents/openai.yaml` contains `allow_implicit_invocation: false` as `explicit-only`; initialize every other existing Skill as `published`. Do not introduce a `development` entry merely to exercise the state.

- [x] **Step 4: Add policy-consistency validation**

For every registry entry:

```python
interface = plugin_root / "skills" / skill_name / "agents" / "openai.yaml"
is_explicit_only = (
    interface.is_file()
    and re.search(
        r"(?m)^\s*allow_implicit_invocation:\s*false\s*$",
        interface.read_text(encoding="utf-8"),
    )
    is not None
)
assert is_explicit_only == (state == "explicit-only")
```

This makes the lifecycle registry authoritative while checking that Codex runtime policy implements the recorded state.

- [x] **Step 5: Run the lifecycle and full repository-layout tests**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider tests/test_repository_layout.py
```

Expected: all tests pass.

### Task 2: Make the Paper release consume and package lifecycle state

**Files:**
- Modify: `plugins/paper-project/scripts/build_marketplace_release.py`
- Modify: `plugins/paper-project/tests/resources/test_resource_release.py`

**Interfaces:**
- Consumes: `plugins/paper-project/skill-lifecycle.json` from Task 1.
- Produces: release validation whose expected Skill roster comes from the lifecycle registry, rejects development or policy-inconsistent Skills, and emits an archive containing that registry.

- [x] **Step 1: Write failing release tests**

Add assertions that:

```python
assert "paper-project-marketplace/plugins/paper-project/skill-lifecycle.json" in names
```

and that changing the registry roster in a temporary plugin fixture makes release validation fail with an `Unexpected skill roster` error.

- [x] **Step 2: Run the targeted test and verify it fails**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider plugins/paper-project/tests/resources/test_resource_release.py
```

Expected: FAIL because the builder does not yet require or consume the registry.

- [x] **Step 3: Load the lifecycle registry in the release builder**

Add:

```python
def load_skill_lifecycle(plugin_root: Path) -> dict[str, str]:
    path = plugin_root / "skill-lifecycle.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("skills"), dict):
        raise SystemExit(f"Invalid skill lifecycle registry: {path}")
    return data["skills"]
```

Change `assert_skill_contract` to compare actual Skill directories with `set(load_skill_lifecycle(plugin_root))`. Keep the existing UI-file contract separate because UI metadata and lifecycle state are different concerns.

- [x] **Step 4: Require the registry in the built bundle**

Add `bundled_plugin / "skill-lifecycle.json"` to `assert_bundle_contract`'s required paths. The existing copy operation should include it without a new copying branch.

- [x] **Step 5: Run release tests and a disposable release build**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider plugins/paper-project/tests/resources/test_resource_release.py
```

Then build into a temporary directory without publishing:

```bash
release_dir=$(mktemp -d)
python plugins/paper-project/scripts/build_marketplace_release.py --output-dir "$release_dir"
tar -tzf "$release_dir"/*.tar.gz | rg 'plugins/paper-project/skill-lifecycle.json'
```

Expected: tests pass, build exits zero, and the archive lists the lifecycle registry.

### Task 3: Document lifecycle governance and transition history

**Files:**
- Modify: `AGENTS.md`
- Modify: `docs/migrations/2026-09-04-plugin-consolidation.md`
- Modify: `CONTEXT.md` only if implementation reveals a terminology mismatch

**Interfaces:**
- Consumes: lifecycle model in `CONTEXT.md` and registries from Task 1.
- Produces: an agent-facing maintenance pointer and the initial lifecycle-registry migration record.

- [x] **Step 1: Add the maintenance pointer to `AGENTS.md`**

Extend the existing maintenance entry so changing a Skill state requires reading the lifecycle section in `CONTEXT.md`, updating the owning plugin's `skill-lifecycle.json`, aligning `agents/openai.yaml`, and recording the transition in the migration log.

- [x] **Step 2: Record the registry introduction**

Append a dated “Skill 生命周期登记” subsection to `docs/migrations/2026-09-04-plugin-consolidation.md` recording:

- the three-state model and allowed transitions;
- the five registry paths;
- the initial classification rule (`allow_implicit_invocation: false` maps to `explicit-only`, all other existing Skills map to `published`);
- the validation and Paper release integration introduced by this change.

- [x] **Step 3: Run documentation and complete regression checks**

Run:

```bash
git diff --check
PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider tests/test_repository_layout.py plugins/paper-project/tests
```

Expected: no whitespace errors and all selected tests pass.

- [x] **Step 4: Review the final diff without publishing or installing**

Run:

```bash
git status --short
git diff --stat
git diff -- CONTEXT.md AGENTS.md docs/migrations/2026-09-04-plugin-consolidation.md tests/test_repository_layout.py plugins/*/skill-lifecycle.json plugins/paper-project/scripts/build_marketplace_release.py plugins/paper-project/tests/resources/test_resource_release.py
```

Expected: only lifecycle-governance files and the pre-existing user change are present; no release archive, cache, installation, or publication change is included.
