from __future__ import annotations

from pathlib import Path


BACKEND_FILES = (
    "dmft/common.md",
    "dmft/postprocessing.md",
    "namd/common.md",
    "namd/namdwithsoc.md",
)

EXPECTED_ENVIRONMENT_PROBES = {
    "DMFT": "test -x '/configured/dmft-entrypoint'",
    "Hefei-NAMD": "test -x '/configured/namd'",
    "NAMDwithSOC": "test -x '/configured/namd_soc'",
}

# These are Task 8's concrete inputs for the later S13 candidate-agent run.
# This contract test only preserves the fixture facts and the instructions the
# candidate will receive; Task 11 owns observing and judging candidate behavior.
S13_FIXTURES = (
    {
        "name": "wrong-soctype",
        "reference": "namd/namdwithsoc.md",
        "facts": (
            "NAMDwithSOC 1.5.2",
            "VASP 6.5 noncollinear SOC",
            "OUTCAR effective ISPIN = 1",
            "WAVECAR has spinor coefficients",
            "Spec says SOCTYPE=2",
        ),
        "expected_owner": "$calc-to-spec",
        "contract_tokens": (
            "NAMDwithSOC 1.5.2",
            "SOCTYPE=1",
            "SOCTYPE=2",
            "VASP 6.5",
            "$calc-to-spec",
        ),
    },
    {
        "name": "missing-snapshot-fields",
        "reference": "namd/common.md",
        "facts": (
            "five approved snapshots",
            "snapshot 4 has no NKPTS evidence",
            "other OUTCAR fields are present",
        ),
        "expected_owner": "calc-execute validation",
        "contract_tokens": (
            "effective `ISPIN`",
            "`NKPTS`",
            "`NBANDS`",
            "`LSORBIT`",
            "`LNONCOLLINEAR`",
            "every snapshot",
        ),
    },
    {
        "name": "wrong-band-window",
        "reference": "namd/namdwithsoc.md",
        "facts": (
            "approved SOCTYPE=1 and BMIN=80 BMAX=96",
            "snapshot 3 EIGENVAL contains bands 1 through 64",
            "INICON selects band 88",
        ),
        "expected_owner": "$calc-to-spec",
        "contract_tokens": (
            "`BMIN/BMAX`",
            "`EIGENVAL`",
            "occupations",
            "every frame",
            "$calc-to-spec",
        ),
    },
    {
        "name": "dmft-ambiguous-convergence",
        "reference": "dmft/common.md",
        "facts": (
            "Spec requires both an occupancy plateau and a self-energy criterion",
            "occupancy evidence passes",
            "self-energy evidence conflicts across the decisive interval",
        ),
        "expected_owner": "$calc-to-spec",
        "contract_tokens": (
            "approved Spec",
            "decisive criteria",
            "ambiguous",
            "$calc-to-spec",
        ),
    },
)


def _backend_root(plugin_root: Path) -> Path:
    return plugin_root / "skills/calc-execute/references/backends"


def test_dmft_namd_bundle_files(plugin_root):
    base = _backend_root(plugin_root)
    for relative in BACKEND_FILES:
        assert (base / relative).is_file()
    assert "1.5.2" in (base / "namd/namdwithsoc.md").read_text(encoding="utf-8")


def test_dmft_namd_exact_environment_probe_coverage(plugin_root):
    """Catch a mutable backend check being omitted or replaced by a fallback."""
    text = (plugin_root / "skills/calc-execute/references/pbs.md").read_text(
        encoding="utf-8"
    )
    for label, command in EXPECTED_ENVIRONMENT_PROBES.items():
        assert f"| {label} | `{command}` |" in text


def test_dmft_execution_applies_spec_criteria_without_local_hdf5(plugin_root):
    """Catch execution reverting to the legacy no-interpretation or local-HDF5 path."""
    base = _backend_root(plugin_root)
    common = (base / "dmft/common.md").read_text(encoding="utf-8")
    postprocessing = (base / "dmft/postprocessing.md").read_text(encoding="utf-8")
    combined = common + postprocessing

    for token in (
        "approved Spec",
        "decisive criteria",
        "$calc-to-spec",
        "impurity spectral function",
        "self-energy MaxEnt",
        "self-energy Pade",
        "server",
        "lightweight",
    ):
        assert token in combined
    assert "Do not interpret physical convergence" not in combined


def test_dmft_source_instructions_cannot_override_spec_authority(plugin_root):
    """Catch rendering mechanics being promoted to scientific parameter authority."""
    common = (_backend_root(plugin_root) / "dmft/common.md").read_text(
        encoding="utf-8"
    )
    assert "Spec is the sole scientific parameter authority" in common
    assert "supply rendering mechanics only" in common
    assert "never override or add a missing scientific parameter" in common
    assert "They are parameter authority" not in common


def test_namdwithsoc_preserves_the_verified_interface_contract(plugin_root):
    """Catch loss of a 1.5.2 representation, snapshot, or success-evidence rule."""
    base = _backend_root(plugin_root)
    common = (base / "namd/common.md").read_text(encoding="utf-8")
    soc = (base / "namd/namdwithsoc.md").read_text(encoding="utf-8")
    combined = common + soc

    for token in (
        "olap%ISPIN = inp%SOCTYPE",
        "`SOCTYPE=1`",
        "`SOCTYPE=2`",
        "`BMIN/BMAX`",
        "`BMINU/BMAXU`",
        "`BMIND/BMAXD`",
        "`time_index band`",
        "`time_index band spin`",
        "`I0.<len(NSW)>`",
        "`RUNDIR/1/WAVECAR`",
        "`RUNDIR/5/WAVECAR`",
        "`COUPCAR`",
        "`NATXT`",
        "`EIGTXT`",
        "`SHPROP.*`",
        "`PSICT.*`",
        "No. of spin components does NOT match",
        "read-only by convention",
    ):
        assert token in combined


def test_backend_references_define_run_rendering_integration(plugin_root):
    """Catch a backend inventing a universal template or malformed injected body."""
    base = _backend_root(plugin_root)
    for relative in BACKEND_FILES:
        text = (base / relative).read_text(encoding="utf-8")
        assert "inputs/run.pbs" in text
    for relative in ("dmft/common.md", "namd/common.md"):
        text = (base / relative).read_text(encoding="utf-8")
        for token in (
            "../../../assets/templates/common/run.sh.template",
            "`__FINGERPRINT_SOURCE__`",
            "`__PREPARE_BODY__`",
            "`__VALIDATE_BODY__`",
            "copy_immutable SOURCE DESTINATION",
            "`|| return 1`",
            "approved source instructions",
        ):
            assert token in text


def test_s13_dmft_namd_fixtures_are_concrete_and_covered(plugin_root):
    """Keep the four agreed refusal fixtures available for Task 11 inference."""
    assert {fixture["name"] for fixture in S13_FIXTURES} == {
        "wrong-soctype",
        "missing-snapshot-fields",
        "wrong-band-window",
        "dmft-ambiguous-convergence",
    }
    base = _backend_root(plugin_root)
    for fixture in S13_FIXTURES:
        assert len(fixture["facts"]) >= 3
        assert fixture["expected_owner"]
        text = (base / fixture["reference"]).read_text(encoding="utf-8")
        for token in fixture["contract_tokens"]:
            assert token in text
