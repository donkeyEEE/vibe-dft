def test_spec_schema_design_and_publication_contract(plugin_root):
    # Spec template.
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

    # Spec template uses reduced task statuses.
    text = (
        plugin_root / "skills/calc-to-spec/references/spec-template.md"
    ).read_text()

    assert "Task 状态为 `pending | completed\n| failed | needs-review`" in text
    assert "条件被明确判定为假或\nTask 被取消时，该 Task 的状态为 `failed`" in text

    # Run result is a compact advancement summary.
    text = (
        plugin_root / "skills/calc-to-spec/references/spec-template.md"
    ).read_text(encoding="utf-8")
    flat = " ".join(text.split())

    assert "`Result` 是可扫描的执行摘要" in flat
    assert "最好按“结果 → 失败原因 → 与上一 Run 的区别 → 推进” 组织" in flat
    assert "必须包含“结果”和“推进”" not in flat
    assert "允许|不允许|待定" not in flat
    assert "不粘贴原始日志、排障过程或 详细诊断" in flat

    # Design flow is incremental and mode dependent.
    text = " ".join(
        (plugin_root / "skills/calc-to-spec/SKILL.md")
        .read_text(encoding="utf-8")
        .split()
    )

    assert "$dev-engineering:grill-with-docs" in text
    assert "无需预先穷尽该 RQ 的全部 Spec" in text
    assert "自动设计只在现有证据仍无法决定的关键科学缺口" in text
    assert "自动设计" in text
    assert "协作设计" in text
    assert "明确批准" in text
    assert "`concluded` Spec 可只读引用" in text
    assert "直接进入 `$calc-execute`" in text

    # Domain research is called during spec design.
    text = " ".join(
        (plugin_root / "skills/calc-to-spec/SKILL.md")
        .read_text(encoding="utf-8")
        .split()
    )

    assert text.index("开始工作时先加载 `$domain-research`") < text.index("定位目标")
    assert "由它指导物理因果链、证据设计与计算剪枝" in text
    assert "术语的收录、确认和更新遵循 `$domain-research`" in text
    assert "检查完整 Spec，清理冗余表达并核对原意" in text
    assert text.index("草稿完成后按 `$domain-research`") < text.index("取得发布批准")
    assert "修订后重复此检查" in text

    # Mode gate covers direct and continued design.
    spec = " ".join(
        (plugin_root / "skills/calc-to-spec/SKILL.md")
        .read_text(encoding="utf-8")
        .split()
    )

    assert "本次设计" in spec
    assert "不写入 `RQ.md`" in spec
    assert "等待" in spec
    assert "新建" in spec and "替换" in spec
    assert "下一份" in spec
    assert "方案变化" in spec

    # Design has no evidence level and keeps research handoff.
    spec = (plugin_root / "skills/calc-to-spec/SKILL.md").read_text(encoding="utf-8")
    template = (plugin_root / "skills/calc-to-spec/references/spec-template.md").read_text(encoding="utf-8")
    rq_template = (plugin_root / "skills/calc-rq/references/rq-template.md").read_text(encoding="utf-8")

    assert "证据档位？" not in spec
    assert "Evidence level:" not in template
    assert "Evidence level:" not in rq_template
    assert "旧 Spec 保留原样" in spec
    assert "$dev-engineering:research" in spec
    assert "$paper-project:literature-review" in spec

    # Spec separates scientific commitments from execution discretion.
    spec = (plugin_root / "skills/calc-to-spec/SKILL.md").read_text(encoding="utf-8")
    template = (
        plugin_root / "skills/calc-to-spec/references/spec-template.md"
    ).read_text(encoding="utf-8")

    spec_flat = " ".join(spec.split())
    template_flat = " ".join(template.split())
    assert "execution-owned" in spec_flat
    assert "探索任务可以用于取得尚缺的科学证据" in spec_flat
    assert "由执行负责" in template_flat
    assert "有利的科学结果" in template_flat
