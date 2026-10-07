import yaml


EXPECTED = {
    "ask-lyz",
    "calc-setup",
    "calc-rq",
    "domain-research",
    "calc-to-spec",
    "calc-execute",
    "calc-issue",
    "calc-report",
    "calc-review",
    "show-cot",
}


def test_roster_and_invocation_policy(plugin_root):
    # Exact roster.
    assert {
        path.name for path in (plugin_root / "skills").iterdir() if path.is_dir()
    } == EXPECTED
    assert {
        path.parent.name for path in (plugin_root / "skills").glob("*/SKILL.md")
    } == EXPECTED

    # Model invoked metadata.
    for name in sorted(EXPECTED - {"ask-lyz", "show-cot"}):
        metadata = plugin_root / "skills" / name / "agents" / "openai.yaml"
        data = yaml.safe_load(metadata.read_text(encoding="utf-8"))

        assert "policy" not in data
        assert f"${name}" in data["interface"]["default_prompt"]
        assert data["interface"]["display_name"]
        assert data["interface"]["short_description"]

    # User invoked entries are explicit only.
    for name in ("ask-lyz", "show-cot"):
        metadata = plugin_root / "skills" / name / "agents" / "openai.yaml"
        data = yaml.safe_load(metadata.read_text(encoding="utf-8"))

        assert data["policy"]["allow_implicit_invocation"] is False
        assert f"${name}" in data["interface"]["default_prompt"]

    # Ask lyz explains plugin usage and routes other requests.
    router = (plugin_root / "skills/ask-lyz/SKILL.md").read_text(encoding="utf-8")

    assert all(
        f"## {scenario}" in router
        for scenario in ("插件使用说明", "推荐工作接口", "进度查询")
    )
    assert "[领域术语](../../resources/project-context.md)" in router
    assert "[字段契约](../../resources/progress-tracker.md)" in router
    assert "解释" in router
    assert "具体操作读取 owning skill" in router
    for duty in ("物理因果链", "计算剪枝", "RQ-CONTEXT.md", "校准证据措辞", "精简科学表达"):
        assert duty in router
    assert "调用 `$dev-engineering:domain-modeling`" in router
    assert "调用 `$show-cot`" in router
