def test_spec_template(plugin_root):
    text = (
        plugin_root / "skills/calc-to-spec/references/spec-template.md"
    ).read_text()
    for field in (
        "ID: SPEC-001",
        "Status: ready",
        "RQ: ../RQ.md",
        "## 判断",
        "## 任务",
        "### TASK-001:",
        "Blocked by:",
        "Condition:",
        "Acceptance:",
        "#### 运行（Run）",
        "| Run | Status | Current | Path | Result |",
        "## 上下文",
    ):
        assert field in text

    assert "`Context` 是最后一节。" in text
    assert "将 `Closure` 紧接在 `Context` 前插入" in text


def test_spec_template_uses_reduced_task_statuses(plugin_root):
    text = (
        plugin_root / "skills/calc-to-spec/references/spec-template.md"
    ).read_text()

    assert "Task 状态为 `pending | completed\n| failed | needs-review`" in text
    assert "条件被明确判定为假或\nTask 被取消时，该 Task 的状态为 `failed`" in text


def test_run_result_is_a_compact_advancement_summary(plugin_root):
    text = (
        plugin_root / "skills/calc-to-spec/references/spec-template.md"
    ).read_text(encoding="utf-8")
    flat = " ".join(text.split())

    assert "`Result` 是可扫描的执行摘要" in flat
    assert "最好按“结果 → 失败原因 → 与上一 Run 的区别 → 推进” 组织" in flat
    assert "必须包含“结果”和“推进”" not in flat
    assert "允许|不允许|待定" not in flat
    assert "不粘贴原始日志、排障过程或详细诊断" in flat


def test_design_flow_keeps_full_draft_internal_until_summary_approval(plugin_root):
    text = " ".join(
        (plugin_root / "skills/calc-to-spec/SKILL.md")
        .read_text(encoding="utf-8")
        .split()
    )

    assert "$dev-engineering:grill-with-docs" in text
    assert text.index("$dev-engineering:grill-with-docs") < text.index(
        "用 [Spec 模板]"
    )
    assert "完整 Spec 草案为内部内容" in text
    assert "只展示目标路径、设计摘要" in text
    assert "不要求展示任一成员的完整 Markdown" in text
    assert "一份可审阅草案" not in text
    assert "完整 Markdown 草案" not in text
    assert "完整被覆盖 Spec" not in text
    assert "每条记录的 Run 行" not in text


def test_spec_separates_scientific_commitments_from_execution_discretion(plugin_root):
    spec = (plugin_root / "skills/calc-to-spec/SKILL.md").read_text(encoding="utf-8")
    template = (
        plugin_root / "skills/calc-to-spec/references/spec-template.md"
    ).read_text(encoding="utf-8")

    spec_flat = " ".join(spec.split())
    template_flat = " ".join(template.split())
    assert "execution-owned" in spec_flat
    assert "最低充分证据" in spec_flat
    assert "由执行负责" in template_flat
    assert "有利的科学结果" in template_flat
