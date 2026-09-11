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


def test_review_owns_only_the_exact_instruction_bundle(plugin_root):
    review_root = plugin_root / "skills" / "calc-review"

    assert (review_root / "SKILL.md").is_file()
    assert (review_root / "agents" / "openai.yaml").is_file()
    assert {
        path.relative_to(review_root / "references").as_posix()
        for path in (review_root / "references").rglob("*.md")
    } == REVIEW_REFERENCES
    assert not (review_root / "assets").exists()
    assert not (review_root / "scripts").exists()
