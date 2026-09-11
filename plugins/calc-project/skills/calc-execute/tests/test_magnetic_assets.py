from __future__ import annotations

import hashlib
import os
import stat
import subprocess
from pathlib import Path


TEMPLATE_ROOT = Path("skills/calc-execute/assets/templates")
SCRIPT_ROOT = Path("skills/calc-execute/scripts")
VEST2_SHA256 = "8b428964bd23dc869a24b5b19fa5978c367ea3ce95378f127cf8005ec39174bb"


def _write_executable(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


def _run_pbs(template: Path, run: Path, env: dict[str, str] | None = None):
    return subprocess.run(
        ["bash", str(template)], cwd=run.parent,
        env={**os.environ, **(env or {}), "PBS_O_WORKDIR": str(run), "MPLBACKEND": "Agg"},
        capture_output=True, text=True,
    )


def _make_run(tmp_path: Path, name: str) -> Path:
    run = tmp_path / name
    (run / "inputs").mkdir(parents=True)
    (run / "outputs").mkdir()
    (run / "logs").mkdir()
    return run


def _prepare_vampire_run(plugin_root: Path, tmp_path: Path, executable: Path, name: str) -> Path:
    run = _make_run(tmp_path, name)
    inputs = run / "inputs"
    (inputs / "cluster-env.sh").write_text(f'export VAMPIRE_EXE="{executable}"\n')
    (inputs / "input").write_text("output:temperature\noutput:mean-magnetisation-length\n")
    (inputs / "vampire.UCF").write_text("ucf\n")
    (inputs / "vampire.mat").write_text("material\n")
    (inputs / "plot.py").write_bytes(
        (plugin_root / SCRIPT_ROOT / "vampire/plot.py").read_bytes()
    )
    manifest = "".join(
        f"{hashlib.sha256((inputs / model).read_bytes()).hexdigest()}  {model}\n"
        for model in ("vampire.UCF", "vampire.mat")
    )
    (inputs / "model-source.sha256").write_text(manifest)
    return run


def test_vest2_is_byte_identical_and_runs_noninteractively(plugin_root, tmp_path):
    script = plugin_root / SCRIPT_ROOT / "wannier90/vest2.py"
    assert hashlib.sha256(script.read_bytes()).hexdigest() == VEST2_SHA256
    (tmp_path / "DOSCAR").write_text("1\n2\n3\n4\n5\n0 0 0 0.5\n")
    (tmp_path / "BAND.dat").write_text(
        "# header\n# a b c 2 1\n# columns\n0 1.0 2.0\n1 1.5 2.5\n"
    )
    result = subprocess.run(
        ["python3", str(script)], cwd=tmp_path, input="5\ny\n8\n",
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "bandrange_spin0.dat").stat().st_size > 0
    assert (tmp_path / "bandrange_spin1.dat").stat().st_size > 0


def test_migrated_assets_match_accepted_hashes(plugin_root):
    # Helper hashes are the byte-preserved DT005 sources. The environment
    # template hash includes its accepted Run-local filename comment rewrite.
    expected = {
        "skills/calc-execute/scripts/vasp/compare_incar_parameters.sh": "fcbff4b79759e677bd886918004b62e6e3d02aa48cb7f614152934f8ad9f4141",
        "skills/calc-execute/scripts/vasp/plot_vasp_band.py": "16a814d3b4aaf7148994461fd87959b3eaf2729b8b206b4a45d4751e428517ff",
        "skills/calc-execute/scripts/wannier90/vest2.py": VEST2_SHA256,
        "skills/calc-execute/scripts/wannier90/plot_wannier_fit_up.py": "8c8cd6435fe79107a34b7d7b24b0938c65ef4fd2ff105e2184fdf588bbb3d332",
        "skills/calc-execute/scripts/wannier90/plot_wannier_fit_dn.py": "f8943842e5c49d51ce069e0d7c3c9b7545ea31d58d7e3d8c08812ce16beebbc4",
        "skills/calc-execute/scripts/vampire/plot.py": "eec9ac3fa6cb8445f8958c01382f89d934e37e55bed860088000f9888e83d8f5",
        "skills/calc-execute/scripts/vampire/pack_magnetic_results.sh": "5e31889219ebeae18aa6390aa154a46cf3f60810332d7933af022fa9912f510e",
        "skills/calc-execute/assets/templates/wannier90/wannier-run.env.template": "2c7e6fae9d91f6933558fd9b3bfdbc19b31852aa03043d1f1fa28bacf9389a8b",
    }
    for target, digest in expected.items():
        assert hashlib.sha256((plugin_root / target).read_bytes()).hexdigest() == digest


def test_wannier_window_template_names_the_run_local_pbs(plugin_root):
    template = plugin_root / TEMPLATE_ROOT / "wannier90/wannier-run.env.template"
    first_line = template.read_text(encoding="utf-8").splitlines()[0]
    assert first_line == "# Fill all eight values before submitting inputs/run.pbs."


def test_all_plot_helpers_run_on_synthetic_data(plugin_root, tmp_path):
    env = {**os.environ, "MPLBACKEND": "Agg"}
    band = tmp_path / "BAND.dat"
    band.write_text("0 0\n1 1\n\n0 0.5\n1 1.5\n")
    vasp_png = tmp_path / "vasp.png"
    subprocess.run([
        "python3", str(plugin_root / SCRIPT_ROOT / "vasp/plot_vasp_band.py"),
        "--input", str(band), "--output", str(vasp_png),
    ], check=True, env=env)
    assert vasp_png.stat().st_size > 0

    (tmp_path / "DOSCAR").write_text("1\n2\n3\n4\n5\n0 0 0 0.5\n")
    (tmp_path / "REFORMATTED_BAND_UP.dat").write_text("0 0\n1 0.5\n")
    (tmp_path / "REFORMATTED_BAND_DW.dat").write_text("0 0.2\n1 0.7\n")
    for spin, index, vest in (("up", 1, "REFORMATTED_BAND_UP.dat"), ("dn", 2, "REFORMATTED_BAND_DW.dat")):
        (tmp_path / f"wannier90.{index}_band.dat").write_text("0 0.5\n1 1.0\n  \n")
        output = tmp_path / f"fit-{spin}.png"
        subprocess.run([
            "python3", str(plugin_root / SCRIPT_ROOT / f"wannier90/plot_wannier_fit_{spin}.py"),
            "--emin", "-1", "--emax", "1", "--doscar", "DOSCAR",
            "--vest-band", vest, "--output", str(output),
        ], cwd=tmp_path, check=True, env=env)
        assert output.stat().st_size > 0

    vampire_data = tmp_path / "output"
    vampire_data.write_text(
        "#output:temperature output:mean-magnetisation-length\n100 0.9\n200 0.5\n"
    )
    vampire_png = tmp_path / "vampire.png"
    subprocess.run([
        "python3", str(plugin_root / SCRIPT_ROOT / "vampire/plot.py"),
        "--input", str(vampire_data), "--output", str(vampire_png),
    ], check=True, env=env)
    assert vampire_png.stat().st_size > 0


def test_wannier90_pbs_preserves_per_spin_windows_and_outputs(plugin_root, tmp_path):
    run = _make_run(tmp_path, "RUN-wannier")
    inputs = run / "inputs"
    commands = tmp_path / "commands"
    commands.mkdir()
    _write_executable(commands / "mpirun", '#!/bin/bash\nexec "$@"\n')
    _write_executable(commands / "wannier90", """#!/bin/bash
seed=$1
printf 'hr\n' > "${seed}_hr.dat"
printf '2\nX\nX 0 0 0\n' > "${seed}_centres.xyz"
printf '0 0.5\n1 1.0\n  \n' > "${seed}_band.dat"
printf 'converged\n' > "${seed}.wout"
""")
    (inputs / "cluster-env.sh").write_text(
        f'export WANNIER90_EXE="{commands / "wannier90"}"\nexport WANNIER90_MPI_LAUNCHER=mpirun\n'
    )
    (inputs / "wannier-run.env").write_text(
        "export UP_DIS_WIN_MIN=-2\nexport UP_DIS_WIN_MAX=2\nexport UP_DIS_FROZ_MIN=-1\nexport UP_DIS_FROZ_MAX=1\n"
        "export DN_DIS_WIN_MIN=-3\nexport DN_DIS_WIN_MAX=3\nexport DN_DIS_FROZ_MIN=-1.5\nexport DN_DIS_FROZ_MAX=1.5\n"
    )
    for name in ("plot_wannier_fit_up.py", "plot_wannier_fit_dn.py"):
        (inputs / name).write_bytes((plugin_root / SCRIPT_ROOT / "wannier90" / name).read_bytes())
    for spin in (1, 2):
        (inputs / f"wannier90.{spin}.win").write_text("num_wann = 2\n")
        for suffix in ("amn", "mmn", "eig"):
            (inputs / f"wannier90.{spin}.{suffix}").write_text(f"{suffix}\n")
    (inputs / "bandrange_spin0.dat").write_text("range up\n")
    (inputs / "bandrange_spin1.dat").write_text("range dn\n")
    (inputs / "REFORMATTED_BAND_UP.dat").write_text("0 0\n1 .5\n")
    (inputs / "REFORMATTED_BAND_DW.dat").write_text("0 .2\n1 .7\n")
    (inputs / "DOSCAR").write_text("1\n2\n3\n4\n5\n0 0 0 .5\n")
    before = {p.name: p.read_bytes() for p in inputs.iterdir()}
    env = {"PATH": f"{commands}{os.pathsep}{os.environ['PATH']}", "PLOT_EMIN": "-2", "PLOT_EMAX": "2"}

    result = _run_pbs(plugin_root / TEMPLATE_ROOT / "wannier90/run.pbs.template", run, env)

    assert result.returncode == 0, result.stderr
    assert "dis_win_min = -2" in (run / "outputs/wannier90.1.win").read_text()
    assert "dis_win_min = -3" in (run / "outputs/wannier90.2.win").read_text()
    for name in ("wannier90.1.wout", "wannier90.2.wout", "wannier90.1_hr.dat", "wannier90.2_hr.dat", "wannier90.1_centres.xyz", "wannier90.2_centres.xyz", "band_structure-up.png", "band_structure-dn.png"):
        assert (run / "outputs" / name).stat().st_size > 0
    assert {p.name: p.read_bytes() for p in inputs.iterdir()} == before
    template_text = (plugin_root / TEMPLATE_ROOT / "wannier90/run.pbs.template").read_text()
    assert "test -s wannier90.1.wout" in template_text
    assert "test -s wannier90.2.wout" in template_text


def test_wannier90_pbs_rejects_an_incomplete_window_set(plugin_root, tmp_path):
    run = _make_run(tmp_path, "RUN-wannier-missing")
    inputs = run / "inputs"
    (inputs / "cluster-env.sh").write_text("export WANNIER90_EXE=/bin/true\n")
    (inputs / "wannier-run.env").write_text("export UP_DIS_WIN_MIN=-2\n")
    result = _run_pbs(plugin_root / TEMPLATE_ROOT / "wannier90/run.pbs.template", run)
    assert result.returncode != 0


def test_tb2j_pbs_uses_declared_fermi_and_kmesh_and_requires_handoff(plugin_root, tmp_path):
    run = _make_run(tmp_path, "RUN-tb2j")
    inputs = run / "inputs"
    commands = tmp_path / "commands-tb2j"
    commands.mkdir()
    calls = tmp_path / "tb2j.calls"
    _write_executable(commands / "conda", """#!/bin/bash
printf '%s\n' "$*" > "$FAKE_TB2J_CALLS"
mkdir -p TB2J_results/Vampire
printf 'exchange\n' > TB2J_results/exchange.out
printf 'ucf\n' > TB2J_results/Vampire/vampire.UCF
printf 'material\n' > TB2J_results/Vampire/vampire.mat
printf 'output:material-magnetisation\n' > TB2J_results/Vampire/input
""")
    (inputs / "cluster-env.sh").write_text("export TB2J_CONDA_ENV=tb2j\n")
    (inputs / "POSCAR").write_text("structure\n")
    (inputs / "OUTCAR").write_text(" E-fermi : 4.250 other\n")
    for name in ("wannier90.1_hr.dat", "wannier90.2_hr.dat", "wannier90.1_centres.xyz", "wannier90.2_centres.xyz"):
        (inputs / name).write_text("handoff\n")
    before = {path.name: path.read_bytes() for path in inputs.iterdir()}
    template_text = (plugin_root / TEMPLATE_ROOT / "tb2j/run.pbs.template").read_text()
    template_text = template_text.replace("__TB2J_RCUT__", "8.0").replace("__TB2J_KMESH__", "4 4 1").replace("__TB2J_ELEMENTS__", "Fe").replace("__TB2J_EMIN__", "-5").replace("__TB2J_EMAX__", "5")
    rendered = tmp_path / "tb2j.pbs"
    rendered.write_text(template_text)
    env = {"PATH": f"{commands}{os.pathsep}{os.environ['PATH']}", "FAKE_TB2J_CALLS": str(calls)}
    result = _run_pbs(rendered, run, env)
    assert result.returncode == 0, result.stderr
    call = calls.read_text()
    assert "--efermi 4.250" in call
    assert "--kmesh 4 4 1" in call
    assert (run / "outputs/TB2J_results/Vampire/vampire.UCF").stat().st_size > 0
    assert {path.name: path.read_bytes() for path in inputs.iterdir()} == before

    missing = _make_run(tmp_path, "RUN-tb2j-missing")
    for name in ("cluster-env.sh", "POSCAR", "OUTCAR", "wannier90.1_hr.dat", "wannier90.2_hr.dat", "wannier90.1_centres.xyz"):
        (missing / "inputs" / name).write_bytes((inputs / name).read_bytes())
    assert _run_pbs(rendered, missing, env).returncode != 0


def test_vampire_pbs_checks_model_bytes_and_named_columns(plugin_root, tmp_path):
    commands = tmp_path / "commands-vampire"
    commands.mkdir()
    _write_executable(commands / "vampire", """#!/bin/bash
test -z "${FAKE_VAMPIRE_CALLS:-}" || printf 'called\n' >> "$FAKE_VAMPIRE_CALLS"
if test "${MALFORMED_VAMPIRE:-0}" = 1; then
  printf '#temperature magnetisation\n100 .9\n' > output
else
  printf '#output:temperature output:mean-magnetisation-length\n100 .9\n200 .5\n' > output
fi
""")

    env = {"PATH": f"{commands}{os.pathsep}{os.environ['PATH']}"}
    template = plugin_root / TEMPLATE_ROOT / "vampire/run.pbs.template"
    run = _prepare_vampire_run(plugin_root, tmp_path, commands / "vampire", "RUN-vampire")
    before = {path.name: path.read_bytes() for path in (run / "inputs").iterdir()}
    result = _run_pbs(template, run, env)
    assert result.returncode == 0, result.stderr
    assert (run / "outputs/M_vs_T.png").stat().st_size > 0
    assert (run / "logs/model-source.sha256").read_text() == (run / "outputs/model-copy.sha256").read_text()
    assert {path.name: path.read_bytes() for path in (run / "inputs").iterdir()} == before

    changed = _prepare_vampire_run(plugin_root, tmp_path, commands / "vampire", "RUN-vampire-changed")
    (changed / "inputs/vampire.mat").write_text("altered model\n")
    assert _run_pbs(template, changed, env).returncode != 0

    malformed = _prepare_vampire_run(plugin_root, tmp_path, commands / "vampire", "RUN-vampire-malformed")
    assert _run_pbs(template, malformed, {**env, "MALFORMED_VAMPIRE": "1"}).returncode != 0


def test_vampire_rejects_an_omitted_manifest_entry_before_execution(plugin_root, tmp_path):
    commands = tmp_path / "commands-vampire-omitted"
    commands.mkdir()
    calls = tmp_path / "omitted.calls"
    _write_executable(
        commands / "vampire",
        '#!/bin/bash\nprintf "called\\n" >> "$FAKE_VAMPIRE_CALLS"\nprintf "#output:temperature output:mean-magnetisation-length\\n100 .9\\n" > output\n',
    )
    run = _prepare_vampire_run(plugin_root, tmp_path, commands / "vampire", "RUN-vampire-omitted")
    manifest = (run / "inputs/model-source.sha256").read_text().splitlines()
    (run / "inputs/model-source.sha256").write_text(manifest[0] + "\n")

    result = _run_pbs(
        plugin_root / TEMPLATE_ROOT / "vampire/run.pbs.template",
        run,
        {"PATH": f"{commands}{os.pathsep}{os.environ['PATH']}", "FAKE_VAMPIRE_CALLS": str(calls)},
    )

    assert result.returncode != 0
    assert not calls.exists()


def test_vampire_rejects_an_absolute_manifest_entry_before_execution(plugin_root, tmp_path):
    commands = tmp_path / "commands-vampire-absolute"
    commands.mkdir()
    calls = tmp_path / "absolute.calls"
    _write_executable(
        commands / "vampire",
        '#!/bin/bash\nprintf "called\\n" >> "$FAKE_VAMPIRE_CALLS"\nprintf "#output:temperature output:mean-magnetisation-length\\n100 .9\\n" > output\n',
    )
    run = _prepare_vampire_run(plugin_root, tmp_path, commands / "vampire", "RUN-vampire-absolute")
    inputs = run / "inputs"
    ucf_digest = hashlib.sha256((inputs / "vampire.UCF").read_bytes()).hexdigest()
    mat_digest = hashlib.sha256((inputs / "vampire.mat").read_bytes()).hexdigest()
    (inputs / "model-source.sha256").write_text(
        f"{ucf_digest}  {inputs / 'vampire.UCF'}\n{mat_digest}  vampire.mat\n"
    )

    result = _run_pbs(
        plugin_root / TEMPLATE_ROOT / "vampire/run.pbs.template",
        run,
        {"PATH": f"{commands}{os.pathsep}{os.environ['PATH']}", "FAKE_VAMPIRE_CALLS": str(calls)},
    )

    assert result.returncode != 0
    assert not calls.exists()


def test_pack_helper_excludes_models_and_large_files(plugin_root, tmp_path):
    source = tmp_path / "source"
    destination = tmp_path / "packed"
    source.mkdir()
    for name in ("exchange.out", "M_vs_T.png", "vampire.UCF", "WAVECAR", "model_hr.dat"):
        (source / name).write_text(name)
    result = subprocess.run([
        "bash", str(plugin_root / SCRIPT_ROOT / "vampire/pack_magnetic_results.sh"),
        str(source), str(destination),
    ], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert {p.name for p in destination.iterdir()} == {"exchange.out", "M_vs_T.png", "manifest.included", "manifest.skipped"}


def test_scientific_changes_have_an_explicit_stop_owner(plugin_root):
    backend = plugin_root / "skills/calc-execute/references/backends"
    magnetic = (backend / "vasp/common.md").read_text()
    mae = (backend / "vasp/mae.md").read_text()
    windows = (backend / "wannier90/common.md").read_text()
    assert "MAGMOM" in magnetic and "blocks" in magnetic and "$calc-to-spec" in magnetic
    assert "unapproved direction blocks" in mae and "$calc-to-spec" in mae
    assert "Changed, shared, missing, or reordered values block" in windows and "$calc-to-spec" in windows
