import yaml


EXPECTED = {
    "ask-lyz",
    "calc-setup",
    "calc-rq",
    "calc-to-spec",
    "calc-execute",
    "calc-issue",
    "calc-report",
    "calc-review",
    "show-cot",
}


def test_exact_roster(plugin_root):
    assert {
        path.name for path in (plugin_root / "skills").iterdir() if path.is_dir()
    } == EXPECTED
    assert {
        path.parent.name for path in (plugin_root / "skills").glob("*/SKILL.md")
    } == EXPECTED


def test_model_invoked_metadata(plugin_root):
    for name in sorted(EXPECTED - {"ask-lyz", "show-cot"}):
        metadata = plugin_root / "skills" / name / "agents" / "openai.yaml"
        data = yaml.safe_load(metadata.read_text(encoding="utf-8"))

        assert "policy" not in data
        assert f"${name}" in data["interface"]["default_prompt"]
        assert data["interface"]["display_name"]
        assert data["interface"]["short_description"]


def test_user_invoked_entries_are_explicit_only(plugin_root):
    for name in ("ask-lyz", "show-cot"):
        metadata = plugin_root / "skills" / name / "agents" / "openai.yaml"
        data = yaml.safe_load(metadata.read_text(encoding="utf-8"))

        assert data["policy"]["allow_implicit_invocation"] is False
        assert f"${name}" in data["interface"]["default_prompt"]


def test_ask_lyz_explains_plugin_usage_and_routes_other_requests(plugin_root):
    router = (plugin_root / "skills/ask-lyz/SKILL.md").read_text(encoding="utf-8")

    assert all(
        f"## {scenario}" in router
        for scenario in ("插件使用说明", "推荐 sibling", "进度查询")
    )
    assert "[领域术语](../../resources/project-context.md)" in router
    assert "[进度跟踪表契约](../../resources/progress-tracker.md)" in router
    assert "直接解释" in router
    assert "调用 `$dev-engineering:domain-modeling`" in router
    assert "调用 `$show-cot`" in router
