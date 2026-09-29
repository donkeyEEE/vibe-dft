"""Opt-in behavior checks for Calc research writing guidance."""

import json
import os
import subprocess
import tempfile
from pathlib import Path

import pytest


pytestmark = pytest.mark.skipif(
    os.environ.get("CALC_SKILL_EVAL") != "1",
    reason="requires a live Codex model; set CALC_SKILL_EVAL=1",
)


def rewrite_acceptance(plugin_root: Path, source: str) -> str:
    repository = plugin_root.parents[1]
    schema = {
        "type": "object",
        "properties": {"acceptance": {"type": "string"}},
        "required": ["acceptance"],
        "additionalProperties": False,
    }
    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory) / "answer.json"
        schema_file = Path(directory) / "schema.json"
        schema_file.write_text(json.dumps(schema), encoding="utf-8")
        prompt = (
            "只读写作测试。先读取本仓库的 calc-to-spec/SKILL.md、"
            "domain-research/SKILL.md 和 domain-research/references/research-writing.md，"
            "然后以 Spec 设计者身份修改下面的 Acceptance。只输出 JSON 中的 acceptance；"
            "保留当前任务必需的科学条件，不修改项目文件。\n\n"
            f"背景和原文：{source}"
        )
        command = [
            "codex", "exec", "--ephemeral", "--sandbox", "read-only",
            "-C", str(repository), "--output-schema", str(schema_file),
            "-o", str(output), "-",
        ]
        completed = subprocess.run(
            command, input=prompt, text=True, capture_output=True, timeout=120
        )
        assert completed.returncode == 0, completed.stderr
        return json.loads(output.read_text(encoding="utf-8"))["acceptance"]


def test_spec_drops_untriggered_future_remeasurement_rule(plugin_root):
    actual = rewrite_acceptance(
        plugin_root,
        "当前 Task 已固定 300 K、1 fs、3×3×1 k 点及 32 核设置；没有更改设置的计划或迹象。"
        "Acceptance：记录这些设置下稳定段单步耗时，估算 10 ps 轨迹所需机时；"
        "若以后改变温度、时间步、k 点或核数，应根据变更重新检查本估算的适用性。",
    )
    assert "稳定段" in actual and "单步耗时" in actual
    assert "10 ps" in actual
    assert all(term not in actual for term in ("若以后改变", "设置变更", "重新检查", "适用性"))


def test_spec_keeps_condition_that_decides_scientific_validity(plugin_root):
    actual = rewrite_acceptance(
        plugin_root,
        "当前 Task 要确认 SOC 后的 AF 磁序能否作为后续计算基线。"
        "Acceptance：检查 SOC 后 AF 层间关系；若该关系丧失，判定该磁序基线不可用。",
    )
    assert "SOC" in actual
    assert "AF" in actual and "层间" in actual
    assert any(term in actual for term in ("不可用", "不成立", "无效", "不能作为"))
    assert all(term not in actual for term in ("若保持", "则接受", "接受该磁序", "可以作为"))
