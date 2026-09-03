from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PLUGINS = (
    "calc-project",
    "dev-engineering",
    "dev-incubator",
    "dev-misc",
    "dev-productivity",
    "osm-project",
    "paper-project",
)
FORBIDDEN_DIRS = {".pytest_cache", "__pycache__", ".worktrees", ".scratch", "dist"}


def test_required_repository_layout_exists() -> None:
    assert (ROOT / "AGENTS.md").is_file()
    assert (ROOT / "CONTEXT.md").is_file()
    assert (ROOT / "CONTEXT-MAP.md").is_file()
    assert not (ROOT / "docs" / "contexts").exists()
    assert (ROOT / "research-knowledge" / "cards" / "INDEX.md").is_file()
    assert (ROOT / "research-knowledge" / "templates" / "INDEX.md").is_file()


def test_each_plugin_has_a_valid_manifest() -> None:
    actual = {path.parent.parent.name for path in (ROOT / "plugins").glob("*/.codex-plugin/plugin.json")}
    assert actual == set(EXPECTED_PLUGINS)
    for plugin in EXPECTED_PLUGINS:
        manifest = ROOT / "plugins" / plugin / ".codex-plugin" / "plugin.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        assert data["name"] == plugin


def test_migrated_tree_excludes_repository_metadata_and_caches() -> None:
    for tree in (ROOT / "plugins", ROOT / "research-knowledge"):
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


def test_context_map_covers_units_sources_and_dependencies() -> None:
    context_map = (ROOT / "CONTEXT-MAP.md").read_text(encoding="utf-8")
    for plugin in EXPECTED_PLUGINS:
        assert f"plugins/{plugin}" in context_map
    assert "CONTEXT.md" in context_map
    assert "docs/contexts/" not in context_map
    for source in (
        "/home/donk/03FGT/.codex/plugins/calc-project/calc-project",
        "/home/donk/plugins/dev-project/plugins/dev-engineering",
        "/home/donk/plugins/dev-project/plugins/dev-incubator",
        "/home/donk/plugins/dev-project/plugins/dev-misc",
        "/home/donk/plugins/dev-project/plugins/dev-productivity",
        "/home/donk/plugins/osm-project-dev/osm-project",
        "/home/donk/plugins/paper-project/paper-project",
        "/home/donk/plugins/research-knowledge",
    ):
        assert source in context_map
    assert "calc-project" in context_map and "research-knowledge" in context_map
    assert "paper-project" in context_map and "research-knowledge" in context_map


def test_agents_routes_context_reads_in_chinese() -> None:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "CONTEXT-MAP.md" in agents
    assert "CONTEXT.md" in agents
    for trigger in ("插件", "共享知识库", "迁移路径"):
        assert trigger in agents


def test_active_files_do_not_use_legacy_research_knowledge_path() -> None:
    legacy = "/home/donk/plugins/research-knowledge"
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
            if legacy in path.read_text(encoding="utf-8", errors="ignore"):
                offenders.append(path.relative_to(ROOT))
    assert offenders == []
