from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SKILL = ROOT / "plugins/paper-project/skills/pr-intro/SKILL.md"


def test_router_keeps_maintenance_explicit():
    text = SKILL.read_text(encoding="utf-8")
    assert "explicit request to optimize `pr-intro`" in text
    assert "references/maintenance/optimization-protocol.md" in text
    assert "Do not load maintenance" in text


def test_runtime_contract_names_grounding_and_argument_map():
    text = SKILL.read_text(encoding="utf-8")
    assert "available-facts" in text
    assert "argument map" in text
    assert "do not invent" in text.lower()


def test_repository_navigation_lists_pr_intro():
    description = "Draft or restructure evidence-grounded Physical Review Introductions."
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    plugin_readme = (ROOT / "plugins/paper-project/README.md").read_text(
        encoding="utf-8"
    )

    assert "[pr-intro](plugins/paper-project/skills/pr-intro/SKILL.md)" in root_readme
    assert description in root_readme
    assert "[pr-intro](skills/pr-intro/SKILL.md)" in plugin_readme
    assert description in plugin_readme
