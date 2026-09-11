from __future__ import annotations

import re


EXPECTED_BUNDLES = {
    "vasp-scf": ("vasp/common.md", "vasp/scf.md"),
    "vasp-band": ("vasp/common.md", "vasp/band.md", "vasp/handoff.md"),
    "vasp-wannier-prerun": (
        "vasp/common.md",
        "vasp/wannier-prerun.md",
        "vasp/handoff.md",
    ),
    "vasp-mae": ("vasp/common.md", "vasp/mae.md", "vasp/handoff.md"),
    "dmft": ("dmft/common.md",),
    "dmft-postprocessing": ("dmft/common.md", "dmft/postprocessing.md"),
    "namd": ("namd/common.md",),
    "namdwithsoc": ("namd/common.md", "namd/namdwithsoc.md"),
    "wannier90": ("wannier90/common.md",),
    "tb2j": ("tb2j/common.md",),
    "vampire": ("vampire/common.md", "vampire/handoff.md"),
}


def _declared_bundles(skill_text: str) -> dict[str, tuple[str, ...]]:
    bundles: dict[str, tuple[str, ...]] = {}
    for line in skill_text.splitlines():
        match = re.fullmatch(r"\| `([^`]+)` \| (.+) \|", line)
        if match:
            bundles[match.group(1)] = tuple(re.findall(r"`([^`]+\.md)`", match.group(2)))
    return bundles


def test_execute_declares_the_exact_backend_bundles(plugin_root):
    """Catch a branch loading an unrelated backend file or omitting an owner."""
    text = (plugin_root / "skills/calc-execute/SKILL.md").read_text(encoding="utf-8")
    assert _declared_bundles(text) == EXPECTED_BUNDLES


def test_every_declared_backend_file_exists(plugin_root):
    """Catch a declared execution branch continuing after a required file is absent."""
    backend_root = plugin_root / "skills/calc-execute/references/backends"
    missing = [
        relative
        for bundle in EXPECTED_BUNDLES.values()
        for relative in bundle
        if not (backend_root / relative).is_file()
    ]
    assert missing == []


def test_task7_vasp_and_magnetic_bundles_exist(plugin_root):
    """Catch loss of a VASP or magnetic reference without depending on Task 8."""
    backend_root = plugin_root / "skills/calc-execute/references/backends"
    task7 = ("vasp-scf", "vasp-band", "vasp-wannier-prerun", "vasp-mae", "wannier90", "tb2j", "vampire")
    for branch in task7:
        assert tuple(relative for relative in EXPECTED_BUNDLES[branch] if (backend_root / relative).is_file()) == EXPECTED_BUNDLES[branch]
