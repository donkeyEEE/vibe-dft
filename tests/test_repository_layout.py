from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PLUGINS = (
    "calc-project",
    "matt-skills",
    "osm-project",
    "paper-project",
)
FORBIDDEN_DIRS = {".pytest_cache", "__pycache__", ".worktrees", ".scratch", "dist"}
DESIGN_SKILLS = {
    "domain-modeling",
    "grill-with-docs",
    "prototype",
    "research",
}
ENGINEERING_SKILLS = {
    "ask-matt",
    "codebase-design",
    "diagnosing-bugs",
    "improve-codebase-architecture",
    "resolving-merge-conflicts",
    "setup-matt-pocock-skills",
    "triage",
    "wizard",
}
SKILL_STATES = {"development", "published", "explicit-only"}


def load_skill_lifecycle(plugin_root: Path) -> dict[str, str]:
    path = plugin_root / "skill-lifecycle.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["schema_version"] == 1
    skills = data["skills"]
    assert isinstance(skills, dict)
    assert set(skills.values()) <= SKILL_STATES
    return skills


def test_required_repository_layout_exists() -> None:
    assert (ROOT / "AGENTS.md").is_file()
    assert (ROOT / "CONTEXT.md").is_file()
    assert not (ROOT / "CONTEXT-MAP.md").exists()
    assert not (ROOT / "docs" / "contexts").exists()
    paper = ROOT / "plugins" / "paper-project"
    calc = ROOT / "plugins" / "calc-project"
    assert not (paper / "knowledge").exists()
    assert not (calc / "knowledge").exists()
    assert (paper / "resources" / "paper-writing" / "README.md").is_file()
    assert (
        calc / "resources" / "calculation-templates" / "common" / "prepare_run.sh.template"
    ).is_file()
    assert (
        calc
        / "skills"
        / "magnetic-workflow"
        / "assets"
        / "templates"
        / "wannier"
        / "run_wannier90.pbs.template"
    ).is_file()
    assert not (paper / "skills" / "prl-shared").exists()
    assert not (calc / "skills" / "calc-skill-distillation").exists()
    assert (paper / "skills" / "cangjie-skill" / "SKILL.md").is_file()
    assert not (ROOT / "research-knowledge").exists()


def test_each_plugin_has_a_valid_manifest() -> None:
    actual = {path.parent.parent.name for path in (ROOT / "plugins").glob("*/.codex-plugin/plugin.json")}
    assert actual == set(EXPECTED_PLUGINS)
    for plugin in EXPECTED_PLUGINS:
        manifest = ROOT / "plugins" / plugin / ".codex-plugin" / "plugin.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        assert data["name"] == plugin


def test_each_plugin_has_a_complete_skill_lifecycle_registry() -> None:
    for plugin in EXPECTED_PLUGINS:
        plugin_root = ROOT / "plugins" / plugin
        actual_skills = {
            path.parent.name for path in (plugin_root / "skills").glob("*/SKILL.md")
        }
        assert set(load_skill_lifecycle(plugin_root)) == actual_skills


def test_skill_lifecycle_matches_codex_invocation_policy() -> None:
    for plugin in EXPECTED_PLUGINS:
        plugin_root = ROOT / "plugins" / plugin
        for skill_name, state in load_skill_lifecycle(plugin_root).items():
            interface = (
                plugin_root / "skills" / skill_name / "agents" / "openai.yaml"
            )
            is_explicit_only = (
                interface.is_file()
                and re.search(
                    r"(?m)^\s*allow_implicit_invocation:\s*false\s*$",
                    interface.read_text(encoding="utf-8"),
                )
                is not None
            )
            assert is_explicit_only == (state == "explicit-only"), (
                plugin,
                skill_name,
                state,
            )


def test_matt_plugin_matches_the_selected_roster() -> None:
    plugin = ROOT / "plugins" / "matt-skills"
    expected = DESIGN_SKILLS | ENGINEERING_SKILLS | {
        "grill-me", "grilling", "handoff", "teach", "to-questionnaire",
        "wait-what", "writing-for-agents",
    }
    assert set(load_skill_lifecycle(plugin)) == expected
    assert {path.parent.name for path in (plugin / "skills").glob("*/SKILL.md")} == expected
    assert not (ROOT / "plugins" / "dev-engineering").exists()
    assert not (ROOT / "plugins" / "dev-productivity").exists()
    assert "Copyright (c) 2026 Matt Pocock" in (plugin / "LICENSE").read_text()


def test_active_sources_do_not_reference_previous_dev_plugins() -> None:
    stale_reference = re.compile(r"dev-(?:engineering|productivity)|cross-plugin-dependencies\.md")
    offenders: list[Path] = []
    paths = [ROOT / name for name in ("AGENTS.md", "CONTEXT.md", "README.md")]
    paths.extend((ROOT / "plugins").rglob("*"))
    for path in paths:
        if not path.is_file() or path.suffix not in {".md", ".json", ".yaml", ".yml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if stale_reference.search(text):
            offenders.append(path.relative_to(ROOT))
    assert offenders == []


def test_matt_skill_invocations_resolve_within_the_plugin() -> None:
    plugin = ROOT / "plugins" / "matt-skills"
    roster = load_skill_lifecycle(plugin)
    for path in plugin.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".yaml", ".yml"}:
            continue
        for name in re.findall(r"\$matt-skills:([a-z][a-z0-9-]*)", path.read_text()):
            assert name in roster, (path, name)


def test_root_and_matt_navigation_links_resolve() -> None:
    docs = [ROOT / name for name in ("AGENTS.md", "CONTEXT.md", "README.md")]
    docs.extend(ROOT / "plugins" / "matt-skills" / name for name in ("README.md", "skills/README.md"))
    for doc in docs:
        for target in re.findall(r"\]\(([^)]+)\)", doc.read_text()):
            if target.startswith(("https://", "http://", "#")):
                continue
            assert (doc.parent / target.split("#")[0]).exists(), (doc, target)


def test_migrated_tree_excludes_repository_metadata_and_caches() -> None:
    for tree in (ROOT / "plugins",):
        assert tree.is_dir()
        offenders = [
            path.relative_to(ROOT)
            for path in tree.rglob("*")
            if path.is_dir() and (path.name == ".git" or path.name in FORBIDDEN_DIRS)
        ]
        assert offenders == []


def test_repository_does_not_track_generated_caches() -> None:
    tracked = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.splitlines()
    forbidden = {".pytest_cache", "__pycache__", ".worktrees", ".scratch"}
    offenders = [path for path in tracked if forbidden.intersection(Path(path).parts)]
    assert offenders == []


def test_root_context_covers_units_and_dependencies() -> None:
    context = (ROOT / "CONTEXT.md").read_text(encoding="utf-8")
    for plugin in EXPECTED_PLUGINS:
        assert f"plugins/{plugin}" in context
    assert "docs/migrations/2026-09-04-plugin-consolidation.md" in context
    assert "skill-owned resource" in context
    assert "plugin-shared resource" in context
    assert "plugins/calc-project/resources" in context
    assert "plugins/paper-project/resources" in context
    assert "plugins/calc-project/knowledge" not in context
    assert "plugins/paper-project/knowledge" not in context


def test_agents_routes_context_reads_in_chinese() -> None:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "CONTEXT.md" in agents
    for trigger in ("插件", "skill 所属资源", "插件共享资源", "迁移路径"):
        assert trigger in agents


def test_resource_ownership_decision_and_migration_are_recorded() -> None:
    """Catch current resource paths changing without ownership history."""
    adr = ROOT / "docs" / "adr" / "0003-localize-resources-to-owning-skills.md"
    assert adr.is_file()
    text = adr.read_text(encoding="utf-8")
    assert "Supersedes: ADR 0001" in text
    migration = (
        ROOT / "docs" / "migrations" / "2026-09-04-plugin-consolidation.md"
    ).read_text(encoding="utf-8")
    assert "Skill 资源本地化" in migration
    assert "refactor/localize-skill-resources" in migration


def test_active_files_do_not_use_legacy_research_knowledge_path() -> None:
    obsolete = (
        "/home/donk/plugins/research-knowledge",
        "/home/donk/yz-skills/research-knowledge",
    )
    suffixes = {".py", ".sh", ".json", ".yaml", ".yml"}
    offenders: list[Path] = []
    for plugin in ("calc-project", "paper-project"):
        root = ROOT / "plugins" / plugin
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            is_runtime_markdown = path.name == "SKILL.md" or "references" in path.parts
            if path.suffix not in suffixes and not is_runtime_markdown:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(path_text in text for path_text in obsolete):
                offenders.append(path.relative_to(ROOT))
    assert offenders == []


def test_active_plugin_sources_do_not_depend_on_retired_knowledge_protocol() -> None:
    forbidden_names = {"knowledge-source.yaml", "knowledge-source.yml"}
    forbidden_fragments = (
        "plugins/paper-project/knowledge/",
        "plugins/calc-project/knowledge/",
        "CONSUMER_CONTRACT.md",
        "knowledge/candidates/",
        "knowledge/incubating/",
    )
    offenders: list[Path] = []
    for plugin in ("calc-project", "paper-project"):
        plugin_root = ROOT / "plugins" / plugin
        for path in plugin_root.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(plugin_root)
            if relative.parts[0] == "tests":
                continue
            if relative.parts[:3] == (
                "skills",
                "cangjie-skill",
                "references",
            ) and "legacy" in relative.parts:
                continue
            if path.name in forbidden_names:
                offenders.append(path.relative_to(ROOT))
                continue
            if path.suffix not in {".md", ".yaml", ".yml", ".py"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(fragment in text for fragment in forbidden_fragments):
                offenders.append(path.relative_to(ROOT))
    assert offenders == []


def test_cangjie_is_an_explicit_frozen_entry_point() -> None:
    """Catch the suspended skill becoming implicitly runnable or retaining tools."""
    skill = ROOT / "plugins" / "paper-project" / "skills" / "cangjie-skill"
    interface = (skill / "agents" / "openai.yaml").read_text(encoding="utf-8")
    assert "allow_implicit_invocation: false" in interface
    assert (skill / "references" / "legacy" / "README.md").is_file()
    active_executables = [
        path.relative_to(skill)
        for path in skill.rglob("*")
        if path.is_file()
        and "legacy" not in path.parts
        and (path.suffix in {".py", ".sh"} or path.name.startswith("run_"))
    ]
    assert active_executables == []
