from __future__ import annotations


REVIEW_REFERENCES = {
    "pre-submit.md",
    "pbs.md",
    "backends/vasp.md",
    "backends/vasp-magnetic.md",
    "backends/dmft.md",
    "backends/namd.md",
    "backends/wannier90.md",
    "backends/tb2j.md",
    "backends/vampire.md",
}


def test_exact_read_only_review_contract(plugin_root):
    # Review owns only the exact instruction bundle.
    review_root = plugin_root / "skills" / "calc-review"

    assert (review_root / "SKILL.md").is_file()
    assert (review_root / "agents" / "openai.yaml").is_file()
    assert {
        path.relative_to(review_root / "references").as_posix()
        for path in (review_root / "references").rglob("*.md")
    } == REVIEW_REFERENCES
    assert not (review_root / "assets").exists()
    assert not (review_root / "scripts").exists()

    # Review references do not repeat main routing policy.
    review_root = plugin_root / "skills" / "calc-review"
    references = [
        review_root / "references/pre-submit.md",
        review_root / "references/pbs.md",
        *(review_root / "references/backends").glob("*.md"),
    ]

    for path in references:
        text = path.read_text(encoding="utf-8")
        assert "stops for user judgment" not in text, path
        assert "stop for user judgment" not in text, path
        assert "return to the active execution flow" not in text, path
        assert "returns to the active execution flow" not in text, path
        assert "Repair safe Run-local defects automatically" not in text, path
        assert "停止并等待用户判断" not in text, path
        assert "交回活跃执行流" not in text, path
        assert "自动修复安全的 Run-local 缺陷" not in text, path
