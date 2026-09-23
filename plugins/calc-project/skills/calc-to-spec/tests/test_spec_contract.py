def test_spec_template(plugin_root):
    text = (
        plugin_root / "skills/calc-to-spec/references/spec-template.md"
    ).read_text()
    for field in (
        "ID: SPEC-001",
        "Status: ready",
        "RQ: ../RQ.md",
        "Evidence level: light",
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
    assert "不粘贴原始日志、排障过程或 详细诊断" in flat


def test_design_flow_is_incremental_and_only_interviews_for_critical_gaps(plugin_root):
    text = " ".join(
        (plugin_root / "skills/calc-to-spec/SKILL.md")
        .read_text(encoding="utf-8")
        .split()
    )

    assert "$dev-engineering:grill-with-docs" in text
    assert "无需预先穷尽该 RQ 的全部 Spec" in text
    assert "只有影响主要判断、必要 可比性或验收" in text
    assert "没有关键缺口时自主完成设计" in text
    assert "新建与安全替换不另设发布批准" in text
    assert "`concluded` Spec 可只读引用" in text
    assert "直接进入 `$calc-execute`" in text


def test_evidence_level_inheritance_and_research_handoff(plugin_root):
    spec = (plugin_root / "skills/calc-to-spec/SKILL.md").read_text(encoding="utf-8")
    template = (plugin_root / "skills/calc-to-spec/references/spec-template.md").read_text(encoding="utf-8")
    rq_template = (plugin_root / "skills/calc-rq/references/rq-template.md").read_text(encoding="utf-8")

    assert "Spec 的明确设置优先" in spec
    assert "两者都未设置时为 `light`" in spec
    assert "证据档位" in template
    assert "Evidence level:" in rq_template
    assert "$dev-engineering:research" in spec
    assert "$paper-project:literature-review" in spec


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
