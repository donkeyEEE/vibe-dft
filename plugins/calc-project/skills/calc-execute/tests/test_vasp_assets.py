from __future__ import annotations

import os
import shlex
import stat
import subprocess
from pathlib import Path

import pytest


TEMPLATE_ROOT = Path("skills/calc-execute/assets/templates")
SCRIPT_ROOT = Path("skills/calc-execute/scripts")


def _write_executable(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


def _run_pbs(template: Path, run: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(template)],
        cwd=run.parent,
        env={**os.environ, **env, "PBS_O_WORKDIR": str(run)},
        capture_output=True,
        text=True,
    )


def _render_scf_template(plugin_root: Path, tmp_path: Path, handoff: str) -> Path:
    source = plugin_root / TEMPLATE_ROOT / "vasp/scf/run.pbs.template"
    rendered = tmp_path / f"vasp-{handoff.lower()}.pbs"
    rendered.write_text(
        source.read_text(encoding="utf-8").replace("__VASP_CHARGE_HANDOFF__", handoff),
        encoding="utf-8",
    )
    return rendered


@pytest.fixture
def vasp_commands(tmp_path):
    commands = tmp_path / "commands"
    commands.mkdir()
    _write_executable(
        commands / "mpirun",
        """#!/bin/bash
while test "$#" -gt 0; do
    case "$1" in -machinefile|-np) shift 2 ;; *) break ;; esac
done
exec "$@"
""",
    )
    _write_executable(
        commands / "vasp",
        """#!/bin/bash
printf 'completed\n' > OUTCAR
printf '1\n2\n3\n4\n5\n0 0 0 0.5\n' > DOSCAR
""",
    )
    _write_executable(
        commands / "vaspkit",
        """#!/bin/bash
payload=$(tr '\n' ' ')
printf '%s\n' "$payload" >> "$FAKE_VASPKIT_CALLS"
if test "$payload" = '21 211 1 '; then
    printf '# header\n# a b c 2 1\n# columns\n0 1.0 2.0\n1 1.5 2.5\n' > BAND.dat
    printf '0 0.0 0.1\n1 0.5 0.6\n' > REFORMATTED_BAND_UP.dat
    printf '0 0.2 0.3\n1 0.7 0.8\n' > REFORMATTED_BAND_DW.dat
fi
""",
    )
    nodefile = tmp_path / "nodes"
    nodefile.write_text("localhost\n", encoding="utf-8")
    calls = tmp_path / "vaspkit.calls"
    return commands, nodefile, calls


def _vasp_run(tmp_path: Path, plugin_root: Path, vasp_commands, stage: str) -> tuple[Path, dict[str, str]]:
    commands, nodefile, calls = vasp_commands
    run = tmp_path / f"RUN-{stage}"
    inputs = run / "inputs"
    outputs = run / "outputs"
    logs = run / "logs"
    inputs.mkdir(parents=True)
    outputs.mkdir()
    logs.mkdir()
    for name, content in {
        "INCAR": "ENCUT = 520\nISPIN = 2\n",
        "POSCAR": "synthetic\n",
        "KPOINTS": "synthetic\n",
        "POTCAR": "synthetic\n",
    }.items():
        (inputs / name).write_text(content, encoding="utf-8")
    if stage == "band":
        (inputs / "CHGCAR").write_text("charge\n", encoding="utf-8")
        (inputs / "vest2.py").write_bytes(
            (plugin_root / SCRIPT_ROOT / "wannier90/vest2.py").read_bytes()
        )
    cluster_env = inputs / "cluster-env.sh"
    cluster_env.write_text(
        f'export VASP_EXE="{commands / "vasp"}"\n'
        f'export VASPKIT_EXE="{commands / "vaspkit"}"\n',
        encoding="utf-8",
    )
    return run, {
        "PATH": f"{commands}{os.pathsep}{os.environ['PATH']}",
        "PBS_NODEFILE": str(nodefile),
        "FAKE_VASPKIT_CALLS": str(calls),
    }


def test_incar_mismatch_blocks(plugin_root, tmp_path):
    upstream, prepared = tmp_path / "up", tmp_path / "new"
    upstream.write_text("ENCUT = 520\nISPIN = 2\n")
    script = plugin_root / SCRIPT_ROOT / "vasp/compare_incar_parameters.sh"
    assert script.is_file()
    prepared.write_text(upstream.read_text())
    valid = subprocess.run(["bash", str(script), str(upstream), str(prepared), ""], capture_output=True)
    assert valid.returncode == 0
    prepared.write_text("ENCUT = 400\nISPIN = 2\n")
    result = subprocess.run(["bash", str(script), str(upstream), str(prepared), ""], capture_output=True)
    assert result.returncode != 0


def test_scf_pbs_uses_run_local_immutable_inputs(plugin_root, tmp_path, vasp_commands):
    run, env = _vasp_run(tmp_path, plugin_root, vasp_commands, "scf")
    before = {path.name: path.read_bytes() for path in (run / "inputs").iterdir()}

    result = _run_pbs(_render_scf_template(plugin_root, tmp_path, "none"), run, env)

    assert result.returncode == 0, result.stderr
    assert (run / "outputs/OUTCAR").read_text() == "completed\n"
    assert (run / "logs/vasp.log").is_file()
    assert {path.name: path.read_bytes() for path in (run / "inputs").iterdir()} == before


def test_scf_pbs_refuses_missing_input_and_prior_outputs(plugin_root, tmp_path, vasp_commands):
    template = _render_scf_template(plugin_root, tmp_path, "none")
    run, env = _vasp_run(tmp_path, plugin_root, vasp_commands, "scf")
    (run / "inputs/POTCAR").unlink()
    assert _run_pbs(template, run, env).returncode != 0
    (run / "inputs/POTCAR").write_text("synthetic\n")
    (run / "outputs/prior").write_text("preserve\n")
    result = _run_pbs(template, run, env)
    assert result.returncode != 0
    assert (run / "outputs/prior").read_text() == "preserve\n"


def test_mae_rendering_copies_the_approved_charge_handoff(plugin_root, tmp_path, vasp_commands):
    commands, _, _ = vasp_commands
    called = tmp_path / "mae.called"
    _write_executable(
        commands / "vasp-mae",
        """#!/bin/bash
printf 'called\n' >> "$FAKE_MAE_CALLED"
test "$(cat CHGCAR)" = 'approved charge bytes' || exit 9
printf 'completed from charge\n' > OUTCAR
""",
    )
    run, env = _vasp_run(tmp_path, plugin_root, vasp_commands, "mae")
    (run / "inputs/CHGCAR").write_text("approved charge bytes\n")
    (run / "inputs/cluster-env.sh").write_text(f'export VASP_EXE="{commands / "vasp-mae"}"\n')
    before = {path.name: path.read_bytes() for path in (run / "inputs").iterdir()}
    env["FAKE_MAE_CALLED"] = str(called)

    result = _run_pbs(_render_scf_template(plugin_root, tmp_path, "CHGCAR"), run, env)

    assert result.returncode == 0, result.stderr
    assert (run / "outputs/CHGCAR").read_bytes() == b"approved charge bytes\n"
    assert (run / "outputs/OUTCAR").read_text() == "completed from charge\n"
    assert called.read_text().splitlines() == ["called"]
    assert {path.name: path.read_bytes() for path in (run / "inputs").iterdir()} == before


def test_mae_rendering_blocks_before_execution_when_charge_handoff_is_missing(
    plugin_root, tmp_path, vasp_commands
):
    commands, _, _ = vasp_commands
    called = tmp_path / "missing-mae.called"
    _write_executable(
        commands / "vasp-mae-missing",
        '#!/bin/bash\nprintf "called\\n" >> "$FAKE_MAE_CALLED"\nprintf "completed\\n" > OUTCAR\n',
    )
    run, env = _vasp_run(tmp_path, plugin_root, vasp_commands, "mae-missing")
    (run / "inputs/cluster-env.sh").write_text(f'export VASP_EXE="{commands / "vasp-mae-missing"}"\n')
    env["FAKE_MAE_CALLED"] = str(called)

    result = _run_pbs(_render_scf_template(plugin_root, tmp_path, "CHGCAR"), run, env)

    assert result.returncode != 0
    assert not called.exists()


def test_band_pbs_runs_exact_vaspkit_and_vest_path(plugin_root, tmp_path, vasp_commands):
    run, env = _vasp_run(tmp_path, plugin_root, vasp_commands, "band")
    inputs_before = {path.name: path.read_bytes() for path in (run / "inputs").iterdir()}

    result = _run_pbs(plugin_root / TEMPLATE_ROOT / "vasp/band/run.pbs.template", run, env)

    assert result.returncode == 0, result.stderr
    assert (run / "outputs/bandrange_spin0.dat").stat().st_size > 0
    assert (run / "outputs/bandrange_spin1.dat").stat().st_size > 0
    assert (run / "outputs/REFORMATTED_BAND_UP.dat").stat().st_size > 0
    assert (run / "outputs/REFORMATTED_BAND_DW.dat").stat().st_size > 0
    assert (run / "outputs/DOSCAR").stat().st_size > 0
    assert vasp_commands[2].read_text().splitlines() == ["21 211 1 "]
    assert {path.name: path.read_bytes() for path in (run / "inputs").iterdir()} == inputs_before


def test_band_pbs_blocks_incomplete_spin_outputs(plugin_root, tmp_path, vasp_commands):
    run, env = _vasp_run(tmp_path, plugin_root, vasp_commands, "band")
    incomplete = run / "inputs/vest2.py"
    _write_executable(incomplete, "from pathlib import Path\nPath('bandrange_spin0.dat').write_text('up')\n")

    result = _run_pbs(plugin_root / TEMPLATE_ROOT / "vasp/band/run.pbs.template", run, env)

    assert result.returncode != 0
    assert not (run / "outputs/bandrange_spin1.dat").exists()


def test_wannier_prerun_requires_both_spin_interfaces(plugin_root, tmp_path, vasp_commands):
    commands, nodefile, _ = vasp_commands
    _write_executable(
        commands / "vasp-wannier",
        """#!/bin/bash
for spin in 1 2; do
  for suffix in amn mmn eig win; do printf '%s.%s\n' "$spin" "$suffix" > "wannier90.$spin.$suffix"; done
done
""",
    )
    run = tmp_path / "RUN-prerun"
    inputs = run / "inputs"
    inputs.mkdir(parents=True)
    (run / "outputs").mkdir()
    (run / "logs").mkdir()
    for name in ("INCAR", "POSCAR", "KPOINTS", "POTCAR", "CHGCAR", "WAVECAR"):
        (inputs / name).write_text(f"{name}\n")
    (inputs / "cluster-env.sh").write_text(f'export VASP_EXE="{commands / "vasp-wannier"}"\n')
    before = {path.name: path.read_bytes() for path in inputs.iterdir()}
    env = {"PATH": f"{commands}{os.pathsep}{os.environ['PATH']}", "PBS_NODEFILE": str(nodefile)}

    result = _run_pbs(plugin_root / TEMPLATE_ROOT / "vasp/wannier-prerun/run.pbs.template", run, env)

    assert result.returncode == 0, result.stderr
    for spin in (1, 2):
        for suffix in ("amn", "mmn", "eig", "win"):
            assert (run / "outputs" / f"wannier90.{spin}.{suffix}").stat().st_size > 0
    assert {path.name: path.read_bytes() for path in inputs.iterdir()} == before


def test_every_backend_pbs_uses_the_exact_run_local_prologue(plugin_root):
    expected = """RUN_DIR="${PBS_O_WORKDIR:?missing PBS work directory}"
INPUTS_DIR="$RUN_DIR/inputs"
OUTPUTS_DIR="$RUN_DIR/outputs"
LOGS_DIR="$RUN_DIR/logs"
test -d "$INPUTS_DIR" && test -d "$OUTPUTS_DIR" && test -d "$LOGS_DIR" || exit 1
source "$INPUTS_DIR/cluster-env.sh" || exit 1
cd "$OUTPUTS_DIR" || exit 1"""
    relatives = (
        "vasp/scf/run.pbs.template",
        "vasp/band/run.pbs.template",
        "vasp/wannier-prerun/run.pbs.template",
        "wannier90/run.pbs.template",
        "tb2j/run.pbs.template",
        "vampire/run.pbs.template",
    )
    for relative in relatives:
        text = (plugin_root / TEMPLATE_ROOT / relative).read_text()
        assert expected in text
        assert "rm -f" not in text
        assert "cp -f" not in text


def test_common_prepare_stages_the_named_server_handoff_before_review(plugin_root, tmp_path):
    run = tmp_path / "TASK-band/RUN-002"
    inputs = run / "inputs"
    inputs.mkdir(parents=True)
    (run / "outputs").mkdir()
    (run / "logs").mkdir()
    (inputs / "run.pbs").write_text("#!/bin/bash\n")
    upstream = tmp_path / "TASK-scf/RUN-001/outputs/CHGCAR"
    upstream.parent.mkdir(parents=True)
    upstream.write_bytes(b"server-side charge density\n")
    commands = tmp_path / "handoff-commands"
    commands.mkdir()
    _write_executable(
        commands / "rsync",
        '#!/bin/bash\nwhile test "$#" -gt 2; do shift; done\ntest ! -e "$2" && cp -- "$1" "$2"\n',
    )
    template = (plugin_root / TEMPLATE_ROOT / "common/run.sh.template").read_text()
    rendered = template.replace(
        "__FINGERPRINT_SOURCE__",
        str(plugin_root / SCRIPT_ROOT / "fingerprint_run.py"),
    ).replace(
        "__PREPARE_BODY__",
        f'copy_immutable {shlex.quote(str(upstream))} "$INPUTS_DIR/CHGCAR" || return 1',
    ).replace("__VALIDATE_BODY__", ": || return 1")
    (inputs / "run.sh").write_text(rendered)
    before = upstream.read_bytes()

    result = subprocess.run(
        ["bash", str(inputs / "run.sh"), "prepare"],
        env={**os.environ, "PATH": f"{commands}{os.pathsep}{os.environ['PATH']}"},
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert (inputs / "CHGCAR").read_bytes() == before
    assert upstream.read_bytes() == before
    assert not (run.parent / "inputs").exists()
