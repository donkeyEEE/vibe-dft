from __future__ import annotations

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


def test_execute_does_not_embed_a_backend_inventory(plugin_root):
    """Keep backend discovery out of the main execution workflow."""
    text = (plugin_root / "skills/calc-execute/SKILL.md").read_text(encoding="utf-8")
    assert "Preferred backend bundles" not in text
    assert "| Branch | Exact bundle |" not in text
    for backend in EXPECTED_BUNDLES:
        assert f"`{backend}`" not in text


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
