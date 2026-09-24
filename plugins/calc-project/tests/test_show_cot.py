from __future__ import annotations


def test_show_cot_keeps_authority_read_only_and_scopes_report_choice(plugin_root):
    text = (plugin_root / "skills/show-cot/SKILL.md").read_text(encoding="utf-8")

    assert "在对话中展示完整 COT 后" in text
    assert "询问用户是否需要 HTML" in text
    assert "由 `$calc-execute` 在交还控制前调用时" in text
    assert "无需再次询问" in text
    assert "对 RQ、Spec、Task、Run 及其他权威记录保持只读" in text
    assert "不拥有计算事实或进度状态" in text


def test_show_cot_report_contract_is_narrow_and_reproducible(plugin_root):
    text = (plugin_root / "skills/show-cot/SKILL.md").read_text(encoding="utf-8")

    assert "调用 `$show-me`" in text
    assert ".calc-project/progress-report-YYYY-MM-DD.html" in text
    assert "progress-report-*.html" in text
    assert "删除范围只包括" in text
    assert "不依赖 CDN、远程字体或" in text
    assert "返回新报告的可点击路径" in text


def test_calc_setup_ignores_generated_project_reports(plugin_root):
    skill = (plugin_root / "skills/calc-setup/SKILL.md").read_text(encoding="utf-8")
    structure = (
        plugin_root / "skills/calc-setup/references/project-structure.md"
    ).read_text(encoding="utf-8")

    assert "根 `.gitignore` 包含 `/.calc-project/`" in skill
    assert "`.gitignore` 包含 `/.calc-project/`" in structure
    assert "不属于计算项目结构或进度权威" in structure


def test_progress_tracker_consumers_use_shared_contract(plugin_root):
    for name in ("calc-setup", "calc-rq", "calc-to-spec", "calc-execute", "show-cot"):
        skill = plugin_root / "skills" / name / "SKILL.md"
        text = skill.read_text(encoding="utf-8")
        assert "(../../resources/progress-tracker.md)" in text
        assert "../calc-setup/references/project-structure.md" not in text


def test_legacy_query_delegates_project_rules_to_setup(plugin_root):
    query = (plugin_root / "skills/show-cot/SKILL.md").read_text(encoding="utf-8")
    contract = (plugin_root / "resources/progress-tracker.md").read_text(encoding="utf-8")

    assert "规则补齐交由 `$calc-setup` 按其授权规则处理" in query
    assert "本次查询可继续，不自行修改项目 `AGENTS.md`" in query
    assert "`calc-setup` 拥有项目 AGENTS 维护约定的写入和迁移" in contract
    assert "由智能体直接编辑 JSON，无需统一更新脚本" in contract


def test_progress_trackers_are_scoped_to_rq_and_aggregated_without_omissions(plugin_root):
    contract = (plugin_root / "resources/progress-tracker.md").read_text(encoding="utf-8")
    query = (plugin_root / "skills/show-cot/SKILL.md").read_text(encoding="utf-8")
    assert "每个 RQ 在 `RQ.md` 同级保存一份 `tracker.json`" in contract
    assert "单个 `rq` 对象" in contract
    assert "空项目不创建跟踪表" in contract
    assert "跨 RQ 移动对象时更新源和目标两份表" in contract
    assert "按 `RQ location:` 枚举配置范围内实际 RQ 目录" in query
    assert "不能因缺少 tracker 而跳过该 RQ" in query
    assert "不保存项目级跟踪表" in query
    for name in ("calc-rq", "calc-to-spec", "calc-execute"):
        writer = (plugin_root / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        assert "所属 RQ 目录下的 `tracker.json`" in writer
        assert ".calc-project/tracker.json" not in writer


def test_project_tracker_migration_preserves_authorities_and_other_reports(plugin_root):
    contract = (plugin_root / "resources/progress-tracker.md").read_text(encoding="utf-8")
    assert "从各 RQ 权威记录" in contract
    assert "全部完成后删除旧项目级派生表" in contract
    assert "迁移未完成时保留旧文件" in contract
    assert "不回退到旧项目表" in contract
    assert "保留 `.calc-project/` 内的其他文件" in contract
