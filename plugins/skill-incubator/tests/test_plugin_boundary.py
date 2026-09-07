from __future__ import annotations

import json
from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[1]
ROOT = PLUGIN.parents[1]
PAPER = ROOT / "plugins" / "paper-project"


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def check_skill_incubator_owns_expected_skills() -> None:
    manifest = load_json(PLUGIN / ".codex-plugin" / "plugin.json")
    assert manifest["name"] == "skill-incubator"

    skill_names = {
        path.parent.name for path in (PLUGIN / "skills").glob("*/SKILL.md")
    }
    assert skill_names == {
        "cangjie-skill",
        "nature-response",
        "paper2ppt",
        "ppt-master",
        "scholar-evaluation",
        "scientific-critical-thinking",
    }
    for skill_name in skill_names:
        assert (PLUGIN / "skills" / skill_name / "SKILL.md").is_file()
        assert not (PAPER / "skills" / skill_name).exists()


def check_paper_project_no_longer_owns_incubator_skills() -> None:
    for skill_name in (
        "cangjie-skill",
        "nature-response",
        "paper2ppt",
        "ppt-master",
        "scholar-evaluation",
        "scientific-critical-thinking",
    ):
        assert not (PAPER / "skills" / skill_name).exists()


def check_paper2ppt_consumer_path_resolves_to_bundled_ppt_master() -> None:
    manifest = (PLUGIN / "skills" / "paper2ppt" / "manifest.yaml").read_text(
        encoding="utf-8"
    )
    assert "consumer_skill: ../ppt-master/SKILL.md" in manifest
    assert (PLUGIN / "skills" / "ppt-master" / "SKILL.md").is_file()


def check_paper2ppt_owns_its_terminology_resource() -> None:
    paper2ppt = PLUGIN / "skills" / "paper2ppt"
    manifest = (paper2ppt / "manifest.yaml").read_text(encoding="utf-8")
    local_resource = (
        paper2ppt
        / "references"
        / "paper-writing"
        / "write-terminology-ledger.md"
    )

    assert local_resource.is_file()
    assert (
        "references/paper-writing/write-terminology-ledger.md" in manifest
    )
    assert "../../resources/paper-writing" not in manifest


def check_paper2ppt_names_only_its_public_cross_plugin_dependency() -> None:
    paper2ppt = PLUGIN / "skills" / "paper2ppt"
    runtime_docs = [
        paper2ppt / "README.md",
        paper2ppt / "README_EN.md",
        paper2ppt / "static" / "core" / "toolchain.md",
        paper2ppt / "workflows" / "paper-to-deck.md",
        paper2ppt / "workflows" / "failure-recovery.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in runtime_docs)

    assert "paper-project:liteparse" in combined
    assert "plugins/paper-project/skills" not in combined
    assert "plugins/paper-project/resources" not in combined


def check_terminology_ledger_is_owned_by_each_remaining_consumer() -> None:
    relative = Path("references/paper-writing/write-terminology-ledger.md")
    assert (PLUGIN / "skills" / "paper2ppt" / relative).is_file()
    assert (PAPER / "skills" / "prl-polishing" / relative).is_file()
    assert not (
        PAPER / "resources" / "paper-writing" / "write-terminology-ledger.md"
    ).exists()


def check_repository_navigation_exposes_skill_incubator() -> None:
    marketplace = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    entries = {entry["name"]: entry for entry in marketplace["plugins"]}
    assert entries["skill-incubator"]["source"]["path"] == (
        "./plugins/skill-incubator"
    )

    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    paper_readme = (PAPER / "README.md").read_text(encoding="utf-8")
    assert "plugins/skill-incubator/" in agents
    assert "skill-incubator@yz-skills" in readme
    assert "plugins/skill-incubator/skills/paper2ppt/SKILL.md" in readme
    assert "plugins/skill-incubator/skills/ppt-master/SKILL.md" in readme
    assert "`paper2ppt`" not in paper_readme
    assert "`ppt-master`" not in paper_readme


def test_skill_incubator_boundary() -> None:
    check_skill_incubator_owns_expected_skills()
    check_paper_project_no_longer_owns_incubator_skills()
    check_paper2ppt_consumer_path_resolves_to_bundled_ppt_master()
    check_paper2ppt_owns_its_terminology_resource()
    check_paper2ppt_names_only_its_public_cross_plugin_dependency()
    check_terminology_ledger_is_owned_by_each_remaining_consumer()
    check_repository_navigation_exposes_skill_incubator()
