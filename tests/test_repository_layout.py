from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PLUGINS = (
    "calc-project",
    "osm-project",
    "paper-project",
    "skill-incubator",
)
EXPECTED_CALC_SKILLS = (
    "ask-dnk",
    "calc-setup",
    "calc-rq",
    "calc-to-spec",
    "calc-execute",
    "calc-review",
)
FORBIDDEN_DIRS = {".pytest_cache", "__pycache__", ".worktrees", ".scratch", "dist"}
def check_required_repository_layout_exists() -> None:
    assert (ROOT / "AGENTS.md").is_file()
    assert (ROOT / "CONTEXT.md").is_file()
    assert not (ROOT / "CONTEXT-MAP.md").exists()
    assert not (ROOT / "docs" / "contexts").exists()
    paper = ROOT / "plugins" / "paper-project"
    calc = ROOT / "plugins" / "calc-project"
    assert not (paper / "knowledge").exists()
    assert not (calc / "knowledge").exists()
    assert not (paper / "resources").exists()
    assert not (paper / "skills" / "prl-polishing").exists()
    assert (
        ROOT / "plugins" / "skill-incubator" / "skills" / "prl-polishing" / "SKILL.md"
    ).is_file()
    assert (
        calc
        / "skills"
        / "calc-execute"
        / "assets"
        / "templates"
        / "common"
        / "run.sh.template"
    ).is_file()
    assert (
        calc
        / "skills"
        / "calc-execute"
        / "assets"
        / "templates"
        / "wannier90"
        / "run.pbs.template"
    ).is_file()
    assert not (paper / "skills" / "prl-shared").exists()
    assert not (calc / "skills" / "calc-skill-distillation").exists()
    assert not (ROOT / "research-knowledge").exists()


def check_each_plugin_has_a_valid_manifest() -> None:
    tracked_manifests = subprocess.run(
        ["git", "ls-files", "plugins/*/.codex-plugin/plugin.json"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    actual = {Path(path).parts[1] for path in tracked_manifests}
    assert actual == set(EXPECTED_PLUGINS)
    for plugin in EXPECTED_PLUGINS:
        manifest = ROOT / "plugins" / plugin / ".codex-plugin" / "plugin.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        assert data["name"] == plugin

        if plugin == "calc-project":
            assert data["version"] == "0.1.0+codex.20260912155550"
            prompts = data["interface"]["defaultPrompt"]
            assert len(prompts) == len(EXPECTED_CALC_SKILLS)
            for name, prompt in zip(EXPECTED_CALC_SKILLS, prompts, strict=True):
                assert f"${name}" in prompt

    marketplace = json.loads(
        (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(
            encoding="utf-8"
        )
    )
    calc_entry = next(
        entry for entry in marketplace["plugins"] if entry["name"] == "calc-project"
    )
    assert calc_entry["source"] == {
        "source": "local",
        "path": "./plugins/calc-project",
    }


def check_each_plugin_has_skills() -> None:
    for plugin in EXPECTED_PLUGINS:
        plugin_root = ROOT / "plugins" / plugin
        actual_skills = {
            path.parent.name for path in (plugin_root / "skills").glob("*/SKILL.md")
        }
        assert actual_skills


def check_removed_engineering_plugins_are_absent() -> None:
    for name in ("matt-skills", "dev-engineering", "dev-productivity"):
        assert not (ROOT / "plugins" / name).exists()


def check_root_navigation_links_resolve() -> None:
    docs = [ROOT / name for name in ("AGENTS.md", "CONTEXT.md", "README.md")]
    for doc in docs:
        for target in re.findall(r"\]\(([^)]+)\)", doc.read_text()):
            if target.startswith(("https://", "http://", "#")):
                continue
            assert (doc.parent / target.split("#")[0]).exists(), (doc, target)


def check_migrated_tree_excludes_repository_metadata_and_caches() -> None:
    for tree in (ROOT / "plugins",):
        assert tree.is_dir()
        offenders = [
            path.relative_to(ROOT)
            for path in tree.rglob("*")
            if path.is_dir() and path.name == ".git"
        ]
        assert offenders == []


def check_repository_does_not_track_generated_caches() -> None:
    tracked = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.splitlines()
    forbidden = {".pytest_cache", "__pycache__", ".worktrees", ".scratch"}
    offenders = [path for path in tracked if forbidden.intersection(Path(path).parts)]
    assert offenders == []


def check_root_context_covers_units_and_dependencies() -> None:
    context = (ROOT / "CONTEXT.md").read_text(encoding="utf-8")
    for plugin in ("calc-project", "osm-project", "paper-project", "skill-incubator"):
        assert f"plugins/{plugin}" in context
    assert "Skill roster" in context
    assert "skill-owned resource" in context
    assert "plugin-shared resource" in context
    assert "plugins/paper-project/resources" not in context
    assert "plugins/calc-project/knowledge" not in context
    assert "plugins/paper-project/knowledge" not in context


def check_agents_routes_context_reads_in_chinese() -> None:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "CONTEXT.md" in agents
    for trigger in ("插件", "skill 所属资源", "插件共享资源", "调用策略"):
        assert trigger in agents


def check_resource_ownership_decision_is_recorded() -> None:
    adr = ROOT / "docs" / "adr" / "0003-localize-resources-to-owning-skills.md"
    assert adr.is_file()
    text = adr.read_text(encoding="utf-8")
    assert "Supersedes: ADR 0001" in text


def check_active_files_do_not_use_legacy_research_knowledge_path() -> None:
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


def check_active_plugin_sources_do_not_depend_on_retired_knowledge_protocol() -> None:
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


def test_repository_contract() -> None:
    check_required_repository_layout_exists()
    check_each_plugin_has_a_valid_manifest()
    check_each_plugin_has_skills()
    check_removed_engineering_plugins_are_absent()
    check_root_navigation_links_resolve()
    check_migrated_tree_excludes_repository_metadata_and_caches()
    check_repository_does_not_track_generated_caches()
    check_root_context_covers_units_and_dependencies()
    check_agents_routes_context_reads_in_chinese()
    check_resource_ownership_decision_is_recorded()
    check_active_files_do_not_use_legacy_research_knowledge_path()
    check_active_plugin_sources_do_not_depend_on_retired_knowledge_protocol()
