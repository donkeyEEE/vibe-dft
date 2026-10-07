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
            "生效的 `ISPIN`",
            "`NKPTS`",
            "`NBANDS`",
            "`LSORBIT`",
            "`LNONCOLLINEAR`",
            "每一个快照",
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
            "占据数",
            "每一帧",
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
            "已批准 Spec",
            "决定性判据",
            "含糊",
            "$calc-to-spec",
        ),
    },
)


def _backend_root(plugin_root: Path) -> Path:
    return plugin_root / "skills/calc-execute/references/backends"


def test_dmft_namd_backend_contract(plugin_root):
    # Dmft namd bundle files.
    base = _backend_root(plugin_root)
    for relative in BACKEND_FILES:
        assert (base / relative).is_file()
    assert "1.5.2" in (base / "namd/namdwithsoc.md").read_text(encoding="utf-8")

    # Dmft namd exact environment probe coverage.
    text = (plugin_root / "skills/calc-execute/references/pbs.md").read_text(
        encoding="utf-8"
    )
    for label, command in EXPECTED_ENVIRONMENT_PROBES.items():
        assert f"| {label} | `{command}` |" in text

    # Dmft execution applies spec criteria without local hdf5.
    base = _backend_root(plugin_root)
    common = (base / "dmft/common.md").read_text(encoding="utf-8")
    postprocessing = (base / "dmft/postprocessing.md").read_text(encoding="utf-8")
    combined = common + postprocessing

    for token in (
        "已批准 Spec",
        "决定性判据",
        "$calc-to-spec",
        "杂质谱函数",
        "自能 MaxEnt",
        "自能 Pade",
        "服务器",
        "轻量",
    ):
        assert token in combined
    assert "结果明确时，可判定满足或未满足判据" in common

    # Dmft source instructions cannot override spec authority.
    common = (_backend_root(plugin_root) / "dmft/common.md").read_text(
        encoding="utf-8"
    )
    assert "Spec 是唯一的科学参数依据" in common
    assert "来源说明只提供渲染方法" in common
    assert "不能覆盖或补入缺失的科学参数" in common
    assert "来源说明可覆盖 Spec" not in common

    # Namdwithsoc preserves the verified interface contract.
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
        "按约定将其文件视为只读",
    ):
        assert token in combined

    # Backend references define run rendering integration.
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
            "已批准来源说明",
        ):
            assert token in text

    # S13 dmft namd fixtures are concrete and covered.
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
