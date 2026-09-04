from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PLUGINS = (
    "calc-project",
    "dev-engineering",
    "dev-productivity",
    "osm-project",
    "paper-project",
)
FORBIDDEN_DIRS = {".pytest_cache", "__pycache__", ".worktrees", ".scratch", "dist"}


def test_required_repository_layout_exists() -> None:
    assert (ROOT / "AGENTS.md").is_file()
    assert (ROOT / "CONTEXT.md").is_file()
    assert not (ROOT / "CONTEXT-MAP.md").exists()
    assert not (ROOT / "docs" / "contexts").exists()
    paper_knowledge = ROOT / "plugins" / "paper-project" / "knowledge"
    calc_knowledge = ROOT / "plugins" / "calc-project" / "knowledge"
    assert (paper_knowledge / "CONSUMER_CONTRACT.md").is_file()
    assert (paper_knowledge / "cards" / "INDEX.md").is_file()
    assert (calc_knowledge / "CONSUMER_CONTRACT.md").is_file()
    assert (calc_knowledge / "cards" / "physics" / "PHYSICS_INDEX.md").is_file()
    assert (calc_knowledge / "templates" / "INDEX.md").is_file()
    assert (calc_knowledge / "incubating" / "ontology" / "cards" / "INDEX.md").is_file()
    assert not (ROOT / "research-knowledge").exists()


def test_each_plugin_has_a_valid_manifest() -> None:
    actual = {path.parent.parent.name for path in (ROOT / "plugins").glob("*/.codex-plugin/plugin.json")}
    assert actual == set(EXPECTED_PLUGINS)
    for plugin in EXPECTED_PLUGINS:
        manifest = ROOT / "plugins" / plugin / ".codex-plugin" / "plugin.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        assert data["name"] == plugin


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
    assert "plugins/calc-project/knowledge" in context
    assert "plugins/paper-project/knowledge" in context


def test_agents_routes_context_reads_in_chinese() -> None:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "CONTEXT.md" in agents
    for trigger in ("插件", "插件知识", "迁移路径"):
        assert trigger in agents


def test_root_context_indexes_calc_project_boundary_terms() -> None:
    context = (ROOT / "CONTEXT.md").read_text(encoding="utf-8")
    calc_context = (
        ROOT
        / "plugins"
        / "calc-project"
        / "skills"
        / "calc-project-structure"
        / "references"
        / "project-context.md"
    ).read_text(encoding="utf-8")
    for term in (
        "计算项目（Calculation Project）",
        "数据根（Data Root）",
        "计算任务（Calculation Task）",
        "运行（Run）",
        "项目计算模板（Project Calculation Template）",
        "插件计算模板（Plugin Calculation Template）",
        "候选经验卡（Candidate Experience Card）",
    ):
        assert term in context
        assert term in calc_context


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


def test_plugin_knowledge_sources_resolve_from_their_descriptor() -> None:
    descriptors = sorted(
        path
        for plugin in ("calc-project", "paper-project")
        for path in (ROOT / "plugins" / plugin / "skills").glob(
            "*/references/knowledge-source.yaml"
        )
    )
    assert descriptors
    for descriptor in descriptors:
        fields = dict(
            line.strip().split(":", 1)
            for line in descriptor.read_text(encoding="utf-8").splitlines()
            if line.strip() and ":" in line
        )
        assert fields.get("relative_to", "").strip() == "this_file"
        knowledge = (descriptor.parent / fields["path"].strip()).resolve()
        assert knowledge.parent == descriptor.parents[3]
        assert (knowledge / "CONSUMER_CONTRACT.md").is_file()
        assert (knowledge / "cards" / "INDEX.md").is_file()
