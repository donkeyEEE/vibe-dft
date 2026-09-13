from __future__ import annotations

import hashlib
import os
import shlex
import stat
import subprocess
from pathlib import Path

import pytest


SCRIPT = "skills/calc-execute/scripts/fingerprint_run.py"
TEMPLATE = "skills/calc-execute/assets/templates/common/run.sh.template"
PROBE = "skills/calc-execute/scripts/probe-run-environment.sh"
MONITOR_REFERENCE = "skills/calc-execute/references/calculation-monitor.md"


def test_execute_skill_has_compact_three_part_contract(plugin_root):
    skill = (plugin_root / "skills/calc-execute/SKILL.md").read_text(
        encoding="utf-8"
    )
    body = skill.split("---", 2)[2].strip()
    sections = [line for line in body.splitlines() if line.startswith("#")]

    assert sections == ["# Calc Execute", "## Workflow", "## Principles"]

    overview, remainder = body.split("## Workflow", 1)
    overview_text = " ".join(overview.removeprefix("# Calc Execute").split())
    assert overview_text
    assert len(overview_text) <= 500
    assert "\n\n" not in overview.removeprefix("# Calc Execute").strip()

    workflow, principles = remainder.split("## Principles", 1)
    for reference in (
        "references/task-advancement.md",
        "references/run-preparation.md",
        "references/pbs.md",
        "references/simple-correction.md",
        "references/calculation-monitor.md",
        "references/remote-completion.md",
        "references/sync.md",
    ):
        assert reference in workflow
    for sibling in (
        "`$calc-setup`",
        "`$dev-engineering:research`",
        "`$calc-review`",
        "`$calc-rq`",
    ):
        assert sibling in workflow

    for status in ("`finished`", "`failed`", "`cancelled`"):
        assert status in principles
    assert "`$calc-to-spec`" in principles


def test_calculation_monitor_is_conditional_and_post_submission(plugin_root):
    skill = (plugin_root / "skills/calc-execute/SKILL.md").read_text(encoding="utf-8")
    skill_flat = " ".join(skill.split())
    reference_path = plugin_root / MONITOR_REFERENCE

    assert reference_path.is_file()
    assert "references/calculation-monitor.md" in skill
    assert "explicitly requested" in skill
    assert skill_flat.index("update the Spec Run row to `submitted`") < skill_flat.index(
        "references/calculation-monitor.md"
    )

    reference = reference_path.read_text(encoding="utf-8")
    for contract in (
        "scripts/calculation-monitor.py",
        "CODEX_THREAD_ID",
        "systemd-run --user",
        "--collect",
        "--setenv=PATH=",
        "StandardOutput=null",
        "StandardError=null",
    ):
        assert contract in reference


def _expected_fingerprint(files: dict[str, bytes]) -> str:
    snapshot = hashlib.sha256()
    for relative, content in sorted(files.items()):
        name = relative.encode("utf-8")
        snapshot.update(len(name).to_bytes(8, "big"))
        snapshot.update(name)
        snapshot.update(hashlib.sha256(content).digest())
    return snapshot.hexdigest()


def _write_executable(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


@pytest.fixture
def fake_commands(tmp_path, monkeypatch):
    commands = tmp_path / "commands"
    commands.mkdir()
    qsub_calls = tmp_path / "qsub.calls"
    ssh_calls = tmp_path / "ssh.calls"
    rsync_calls = tmp_path / "rsync.calls"

    _write_executable(
        commands / "qsub",
        """#!/bin/bash
printf 'cwd=%s' "$PWD" >> "$FAKE_QSUB_CALLS"
printf '|%s' "$@" >> "$FAKE_QSUB_CALLS"
printf '\n' >> "$FAKE_QSUB_CALLS"
printf '731.server\n'
""",
    )
    _write_executable(
        commands / "ssh",
        """#!/bin/bash
printf '%s\n' "$@" > "$FAKE_SSH_CALLS"
printf 'remote probe output\n'
exit "${FAKE_SSH_STATUS:-0}"
""",
    )
    _write_executable(
        commands / "rsync",
        """#!/bin/bash
printf '%s' "$1" >> "$FAKE_RSYNC_CALLS"
printf '|%s' "${@:2}" >> "$FAKE_RSYNC_CALLS"
printf '\n' >> "$FAKE_RSYNC_CALLS"
while [ "$#" -gt 2 ]; do shift; done
test ! -e "$2" && cp -- "$1" "$2"
""",
    )
    _write_executable(commands / "vasp-stage", "#!/bin/bash\nexit 0\n")
    _write_executable(commands / "band-stage", "#!/bin/bash\nexit 0\n")

    monkeypatch.setenv("PATH", f"{commands}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("FAKE_QSUB_CALLS", str(qsub_calls))
    monkeypatch.setenv("FAKE_SSH_CALLS", str(ssh_calls))
    monkeypatch.setenv("FAKE_RSYNC_CALLS", str(rsync_calls))
    return {
        "qsub": qsub_calls,
        "ssh": ssh_calls,
        "rsync": rsync_calls,
    }


def _render_run(plugin_root: Path, tmp_path: Path, stage: str) -> tuple[Path, Path]:
    task = tmp_path / f"TASK-{stage.upper()}"
    run = task / "RUN-002"
    inputs = run / "inputs"
    inputs.mkdir(parents=True)
    (run / "outputs").mkdir()
    (run / "logs").mkdir()
    (inputs / "run.pbs").write_text("#!/bin/bash\n", encoding="utf-8")
    (inputs / "cluster-env.sh").write_text(":\n", encoding="utf-8")

    source = tmp_path / f"{stage}-source"
    source.write_bytes(f"{stage} handoff\n".encode())
    fingerprint_source = plugin_root / SCRIPT
    command = "vasp-stage" if stage == "scf" else "band-stage"
    prepare_body = (
        f"copy_immutable {shlex.quote(str(source))} "
        f'"$INPUTS_DIR/{stage.upper()}-HANDOFF" || return 1\n'
        f'touch "$LOGS_DIR/{stage}.prepared"'
    )
    validate_body = f"command -v {command} >/dev/null 2>&1 || exit 1"
    rendered = (plugin_root / TEMPLATE).read_text(encoding="utf-8")
    rendered = rendered.replace("__FINGERPRINT_SOURCE__", str(fingerprint_source))
    rendered = rendered.replace("__PREPARE_BODY__", prepare_body)
    rendered = rendered.replace("__VALIDATE_BODY__", validate_body)
    (inputs / "run.sh").write_text(rendered, encoding="utf-8")
    return run, source


def _run_action(run: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(run / "inputs" / "run.sh"), *args],
        cwd=run.parent.parent,
        capture_output=True,
        text=True,
    )


def test_snapshot_changes_and_rejects_links(load_script, tmp_path):
    module = load_script(SCRIPT)
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    (inputs / "INCAR").write_text("ENCUT=520\n")
    first = module.fingerprint_inputs(inputs)
    (inputs / "INCAR").write_text("ENCUT=600\n")
    assert module.fingerprint_inputs(inputs) != first
    (inputs / "linked").symlink_to(inputs / "INCAR")
    with pytest.raises(ValueError):
        module.fingerprint_inputs(inputs)


def test_fingerprint_is_length_delimited_sorted_and_read_only(load_script, tmp_path):
    module = load_script(SCRIPT)
    inputs = tmp_path / "inputs"
    (inputs / "nested").mkdir(parents=True)
    files = {"INCAR": b"ENCUT=520\n", "nested/run.pbs": b"#PBS -N test\n"}
    for relative, content in reversed(tuple(files.items())):
        (inputs / relative).write_bytes(content)
    before = {path.relative_to(inputs): path.read_bytes() for path in inputs.rglob("*") if path.is_file()}

    assert module.fingerprint_inputs(inputs) == _expected_fingerprint(files)
    assert {path.relative_to(inputs): path.read_bytes() for path in inputs.rglob("*") if path.is_file()} == before
    with pytest.raises(ValueError):
        module.fingerprint_inputs(tmp_path / "absent")


def test_fingerprint_reports_an_unreadable_directory(load_script, tmp_path, monkeypatch):
    module = load_script(SCRIPT)
    inputs = tmp_path / "inputs"
    inputs.mkdir()

    def denied_walk(_path, *, followlinks, onerror):
        assert followlinks is False
        onerror(PermissionError("denied by fixture"))
        return iter(())

    monkeypatch.setattr(module.os, "walk", denied_walk)
    with pytest.raises(ValueError, match="cannot inspect inputs"):
        module.fingerprint_inputs(inputs)


def test_fingerprint_cli_prints_one_digest(plugin_root, tmp_path):
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    (inputs / "run.sh").write_bytes(b"run\n")
    result = subprocess.run(
        ["python", str(plugin_root / SCRIPT), str(inputs)], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert result.stderr == ""
    assert result.stdout == _expected_fingerprint({"run.sh": b"run\n"}) + "\n"


@pytest.mark.parametrize("stage", ["scf", "band"])
def test_prepare_copies_declared_bytes_without_changing_source_or_old_run(
    plugin_root, tmp_path, fake_commands, stage
):
    run, source = _render_run(plugin_root, tmp_path, stage)
    old_run_file = run.parent / "RUN-001" / "inputs" / "preserved"
    old_run_file.parent.mkdir(parents=True)
    old_run_file.write_bytes(b"old run bytes\n")
    source_before = source.read_bytes()
    old_before = old_run_file.read_bytes()

    result = _run_action(run, "prepare")

    assert result.returncode == 0, result.stderr
    assert (run / "inputs" / f"{stage.upper()}-HANDOFF").read_bytes() == source_before
    assert (run / "inputs" / "fingerprint_run.py").read_bytes() == (plugin_root / SCRIPT).read_bytes()
    assert source.read_bytes() == source_before
    assert old_run_file.read_bytes() == old_before
    assert len(fake_commands["rsync"].read_text().splitlines()) == 2


def test_prepare_refuses_a_different_existing_destination(plugin_root, tmp_path, fake_commands):
    run, source = _render_run(plugin_root, tmp_path, "band")
    destination = run / "inputs" / "BAND-HANDOFF"
    destination.write_bytes(b"different prior snapshot\n")
    source_before = source.read_bytes()

    result = _run_action(run, "prepare")

    assert result.returncode != 0
    assert "existing destination differs" in result.stderr
    assert destination.read_bytes() == b"different prior snapshot\n"
    assert source.read_bytes() == source_before


def test_validate_reports_the_complete_run_fingerprint(plugin_root, tmp_path, fake_commands):
    run, _ = _render_run(plugin_root, tmp_path, "scf")
    assert _run_action(run, "prepare").returncode == 0

    result = _run_action(run, "validate")

    assert result.returncode == 0, result.stderr
    digest = result.stdout.strip()
    assert len(digest) == 64
    assert digest == subprocess.run(
        ["python3", str(run / "inputs" / "fingerprint_run.py"), str(run / "inputs")],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def test_validate_and_submit_load_the_run_local_scheduler_environment(
    plugin_root, tmp_path, fake_commands
):
    run, _ = _render_run(plugin_root, tmp_path, "scf")
    assert _run_action(run, "prepare").returncode == 0

    scheduler_commands = tmp_path / "scheduler-commands"
    scheduler_commands.mkdir()
    (tmp_path / "commands" / "qsub").rename(scheduler_commands / "qsub")
    (run / "inputs" / "cluster-env.sh").write_text(
        f"export PATH={shlex.quote(str(scheduler_commands))}:\"$PATH\"\n",
        encoding="utf-8",
    )

    validation = _run_action(run, "validate")

    assert validation.returncode == 0, validation.stderr
    digest = validation.stdout.strip()
    submission = _run_action(run, "submit", digest)
    assert submission.returncode == 0, submission.stderr
    assert submission.stdout == "731.server\n"


def test_submit_rejects_inputs_changed_while_loading_environment(
    plugin_root, tmp_path, fake_commands
):
    run, _ = _render_run(plugin_root, tmp_path, "scf")
    assert _run_action(run, "prepare").returncode == 0
    source_count = tmp_path / "cluster-env-source.count"
    (run / "inputs" / "cluster-env.sh").write_text(
        f'count_file={shlex.quote(str(source_count))}\n'
        'count="$(cat "$count_file" 2>/dev/null || printf 0)"\n'
        'if test "$count" -gt 0; then\n'
        '    printf "# changed after review\\n" >> "$INPUTS_DIR/run.pbs"\n'
        'fi\n'
        'printf "%s\\n" "$((count + 1))" > "$count_file"\n',
        encoding="utf-8",
    )
    digest = _run_action(run, "validate").stdout.strip()

    submission = _run_action(run, "submit", digest)

    assert submission.returncode != 0
    assert "input snapshot changed" in submission.stderr
    assert not fake_commands["qsub"].exists()


def test_submit_requires_current_digest_and_never_prepares(plugin_root, tmp_path, fake_commands):
    run, _ = _render_run(plugin_root, tmp_path, "band")
    assert _run_action(run, "prepare").returncode == 0
    digest = _run_action(run, "validate").stdout.strip()
    fake_commands["rsync"].write_text("")
    (run / "logs" / "band.prepared").unlink()

    missing = _run_action(run, "submit")
    assert missing.returncode != 0
    assert not fake_commands["qsub"].exists()

    (run / "inputs" / "BAND-HANDOFF").write_bytes(b"mutated\n")
    mutated = _run_action(run, "submit", digest)
    assert mutated.returncode != 0
    assert "input snapshot changed" in mutated.stderr
    assert not fake_commands["qsub"].exists()
    assert fake_commands["rsync"].read_text() == ""
    assert not (run / "logs" / "band.prepared").exists()


def test_unchanged_reviewed_test_chain_submits_once(plugin_root, tmp_path, fake_commands):
    """The digest models byte identity; this fixture does not authenticate approval."""
    run, _ = _render_run(plugin_root, tmp_path, "scf")
    assert _run_action(run, "prepare").returncode == 0
    digest = _run_action(run, "validate").stdout.strip()
    fake_commands["rsync"].write_text("")

    result = _run_action(run, "submit", digest)

    assert result.returncode == 0, result.stderr
    assert result.stdout == "731.server\n"
    calls = fake_commands["qsub"].read_text().splitlines()
    assert calls == [
        f"cwd={run}|-o|{run / 'logs' / 'pbs.stdout'}|-e|{run / 'logs' / 'pbs.stderr'}|{run / 'inputs' / 'run.pbs'}"
    ]
    assert fake_commands["rsync"].read_text() == ""


def test_probe_forwards_exact_reviewed_command_and_status(plugin_root, fake_commands, monkeypatch):
    command = "source /reviewed/profile && test -x '/path with spaces/vasp'"
    success = subprocess.run(
        ["bash", str(plugin_root / PROBE), "cluster.example", command],
        capture_output=True,
        text=True,
    )
    assert success.returncode == 0
    assert success.stdout == "remote probe output\n"
    assert fake_commands["ssh"].read_text().splitlines() == ["--", "cluster.example", command]

    monkeypatch.setenv("FAKE_SSH_STATUS", "23")
    failure = subprocess.run(
        ["bash", str(plugin_root / PROBE), "cluster.example", command],
        capture_output=True,
        text=True,
    )
    assert failure.returncode == 23
    assert failure.stdout == "remote probe output\n"
