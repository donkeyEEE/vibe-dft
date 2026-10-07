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
REMOTE_COMPLETION_REFERENCE = "skills/calc-execute/references/remote-completion.md"
TROUBLESHOOTING_REFERENCE = "skills/calc-execute/references/calculation-troubleshooting.md"


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


def _fake_commands(tmp_path, monkeypatch):
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



def test_execution_workflow_delegation_and_result_contract(plugin_root):
    skill = (plugin_root / "skills/calc-execute/SKILL.md").read_text(
        encoding="utf-8"
    )
    body = skill.split("---", 2)[2].strip()
    sections = [line for line in body.splitlines() if line.startswith("#")]

    assert sections == ["# Calc Execute", "## 工作流", "## 原则"]

    overview, remainder = body.split("## 工作流", 1)
    overview_text = " ".join(overview.removeprefix("# Calc Execute").split())
    assert overview_text
    assert len(overview_text) <= 500
    assert "\n\n" not in overview.removeprefix("# Calc Execute").strip()

    workflow, principles = remainder.split("## 原则", 1)
    workflow_steps = [
        line for line in workflow.splitlines() if line[:1].isdigit() and ". " in line
    ]
    assert [line.split(".", 1)[0] for line in workflow_steps] == [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
    ]
    for reference in (
        "references/task-advancement.md",
        "references/run-preparation.md",
        "references/pbs.md",
        "references/simple-correction.md",
        "references/calculation-troubleshooting.md",
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

    skill = (plugin_root / "skills/calc-execute/SKILL.md").read_text(encoding="utf-8")
    advancement = (
        plugin_root / "skills/calc-execute/references/task-advancement.md"
    ).read_text(encoding="utf-8")

    workflow = skill.split("## 工作流", 1)[1].split("## 原则", 1)[0]
    first_step = " ".join(workflow.split("2.", 1)[0].split())

    for contract in (
        "选定 Spec",
        "已记录 Run",
        "权威资料格式错误",
        "不足以调和",
        "可运行 Task",
        "`submitted` Run",
        "不得直接另行分配 Run",
        "确定为假的条件",
        "`failed`",
        "`$calc-to-spec`",
        "持久化每项确定的状态变更",
    ):
        assert contract in first_step
    assert "## Derive the frontier" not in advancement
    assert "## 验收并选择 current Run" in advancement
    assert "## 闭合" in advancement

    references = plugin_root / "skills/calc-execute/references"
    advancement = (references / "task-advancement.md").read_text(encoding="utf-8")
    pbs = (references / "pbs.md").read_text(encoding="utf-8")
    completion = (references / "remote-completion.md").read_text(encoding="utf-8")
    correction = (references / "simple-correction.md").read_text(encoding="utf-8")

    assert "简短表格条目" in advancement
    assert "依次写结果、简短失败原因" in advancement
    assert "qsub 作业 ID" in pbs
    assert "Task 推进判断" in completion
    assert "与上次尝试的实质差异" in correction
    for text in (advancement, completion, correction):
        assert "Run 日志" in text
        assert "排查记录" in text

    reference_path = plugin_root / TROUBLESHOOTING_REFERENCE

    assert reference_path.is_file()
    reference = reference_path.read_text(encoding="utf-8")
    normalized = reference.lower()
    for contract in (
        "定位异常",
        "简单纠错",
        "02-计算规范/",
        "`$dev-engineering:research`",
        "luna",
        "`/tmp`",
        "竞争技术方案",
        "针对性检查",
        "独立稳定笔记",
    ):
        assert contract in normalized

    skill = (plugin_root / "skills/calc-execute/SKILL.md").read_text(encoding="utf-8")
    skill_flat = " ".join(skill.split())
    reference_path = plugin_root / REMOTE_COMPLETION_REFERENCE

    assert reference_path.is_file()
    assert not (
        plugin_root / "skills/calc-execute/references/calculation-monitor.md"
    ).exists()
    assert "references/remote-completion.md" in skill
    assert "需要等待异步作业并恢复本次执行" in skill
    assert skill_flat.index("将 Spec 的 Run 行更新为 `submitted`") < skill_flat.index(
        "references/remote-completion.md"
    )

    reference = reference_path.read_text(encoding="utf-8")
    reference_flat = " ".join(reference.split())
    for contract in (
        "scripts/calculation-monitor.py",
        "CODEX_THREAD_ID",
        "当前平台可用的监督器",
        "优先 `systemd-run --user`",
        "等价后台机制",
        "argv 数组",
        "提交进程的 `PATH`",
        "丢弃监控器 stdout 和 stderr",
        "没有适用启动器时报告监控未启用",
    ):
        assert contract in reference_flat



def test_run_fingerprint_identity_read_only_behavior_and_errors(load_script, plugin_root, tmp_path, monkeypatch):
    module = load_script(SCRIPT)
    inputs = tmp_path / "inputs"
    (inputs / "nested").mkdir(parents=True)
    files = {"INCAR": b"ENCUT=520\n", "nested/run.pbs": b"#PBS -N test\n"}
    for relative, content in reversed(tuple(files.items())):
        (inputs / relative).write_bytes(content)
    before = {path.relative_to(inputs): path.read_bytes() for path in inputs.rglob("*") if path.is_file()}
    first = module.fingerprint_inputs(inputs)
    assert first == _expected_fingerprint(files)
    assert {path.relative_to(inputs): path.read_bytes() for path in inputs.rglob("*") if path.is_file()} == before
    (inputs / "INCAR").write_text("ENCUT=600\n")
    assert module.fingerprint_inputs(inputs) != first
    (inputs / "linked").symlink_to(inputs / "INCAR")
    with pytest.raises(ValueError):
        module.fingerprint_inputs(inputs)
    with pytest.raises(ValueError):
        module.fingerprint_inputs(tmp_path / "absent")

    def denied_walk(_path, *, followlinks, onerror):
        assert followlinks is False
        onerror(PermissionError("denied by fixture"))
        return iter(())

    with monkeypatch.context() as patch:
        patch.setattr(module.os, "walk", denied_walk)
        with pytest.raises(ValueError, match="cannot inspect inputs"):
            module.fingerprint_inputs(inputs)

    cli_inputs = tmp_path / "cli-inputs"
    cli_inputs.mkdir()
    (cli_inputs / "run.sh").write_bytes(b"run\n")
    result = subprocess.run(
        ["python", str(plugin_root / SCRIPT), str(cli_inputs)], capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert result.stderr == ""
    assert result.stdout == _expected_fingerprint({"run.sh": b"run\n"}) + "\n"


def test_run_preparation_preserves_sources_and_validation_covers_complete_inputs(plugin_root, tmp_path, monkeypatch):
    for stage in ("scf", "band"):
        case = tmp_path / stage
        case.mkdir()
        with monkeypatch.context() as patch:
            commands = _fake_commands(case, patch)
            run, source = _render_run(plugin_root, case, stage)
            old = run.parent / "RUN-001/inputs/preserved"
            old.parent.mkdir(parents=True)
            old.write_bytes(b"old run bytes\n")
            before = source.read_bytes()
            prepared = _run_action(run, "prepare")
            assert prepared.returncode == 0, prepared.stderr
            assert (run / "inputs" / f"{stage.upper()}-HANDOFF").read_bytes() == before
            assert (run / "inputs/fingerprint_run.py").read_bytes() == (plugin_root / SCRIPT).read_bytes()
            assert source.read_bytes() == before
            assert old.read_bytes() == b"old run bytes\n"
            assert len(commands["rsync"].read_text().splitlines()) == 2
            validation = _run_action(run, "validate")
            assert validation.returncode == 0, validation.stderr
            digest = validation.stdout.strip()
            assert len(digest) == 64
            assert digest == subprocess.run(
                ["python3", str(run / "inputs/fingerprint_run.py"), str(run / "inputs")],
                check=True, capture_output=True, text=True,
            ).stdout.strip()

    case = tmp_path / "different-destination"
    case.mkdir()
    with monkeypatch.context() as patch:
        _fake_commands(case, patch)
        run, source = _render_run(plugin_root, case, "band")
        destination = run / "inputs/BAND-HANDOFF"
        destination.write_bytes(b"different prior snapshot\n")
        before = source.read_bytes()
        rejected = _run_action(run, "prepare")
        assert rejected.returncode != 0
        assert "existing destination differs" in rejected.stderr
        assert destination.read_bytes() == b"different prior snapshot\n"
        assert source.read_bytes() == before


def test_run_submission_digest_environment_and_exact_remote_probe(plugin_root, tmp_path, monkeypatch):
    # The digest checks byte identity; this fixture does not authenticate approval.
    for scenario in ("local-environment", "environment-mutation", "missing-or-stale-digest", "unchanged"):
        case = tmp_path / scenario
        case.mkdir()
        with monkeypatch.context() as patch:
            commands = _fake_commands(case, patch)
            stage = "band" if scenario == "missing-or-stale-digest" else "scf"
            run, _ = _render_run(plugin_root, case, stage)
            assert _run_action(run, "prepare").returncode == 0
            if scenario == "local-environment":
                scheduler = case / "scheduler-commands"
                scheduler.mkdir()
                (case / "commands/qsub").rename(scheduler / "qsub")
                (run / "inputs/cluster-env.sh").write_text(
                    f'export PATH={shlex.quote(str(scheduler))}:"$PATH"\n',
                )
            elif scenario == "environment-mutation":
                counter = case / "cluster-env-source.count"
                (run / "inputs/cluster-env.sh").write_text(
                    f'count_file={shlex.quote(str(counter))}\n'
                    'count="$(cat "$count_file" 2>/dev/null || printf 0)"\n'
                    'if test "$count" -gt 0; then\n'
                    '    printf "# changed after review\\n" >> "$INPUTS_DIR/run.pbs"\n'
                    'fi\n'
                    'printf "%s\\n" "$((count + 1))" > "$count_file"\n',
                )
            validation = _run_action(run, "validate")
            assert validation.returncode == 0, validation.stderr
            digest = validation.stdout.strip()
            commands["rsync"].write_text("")
            if scenario == "missing-or-stale-digest":
                (run / "logs/band.prepared").unlink()
                assert _run_action(run, "submit").returncode != 0
                assert not commands["qsub"].exists()
                (run / "inputs/BAND-HANDOFF").write_bytes(b"mutated\n")
            submission = _run_action(run, "submit", digest)
            if scenario in {"environment-mutation", "missing-or-stale-digest"}:
                assert submission.returncode != 0
                assert "input snapshot changed" in submission.stderr
                assert not commands["qsub"].exists()
            else:
                assert submission.returncode == 0, submission.stderr
                assert submission.stdout == "731.server\n"
                assert commands["qsub"].read_text().splitlines() == [
                    f"cwd={run}|-o|{run / 'logs/pbs.stdout'}|-e|{run / 'logs/pbs.stderr'}|{run / 'inputs/run.pbs'}",
                ]
            assert commands["rsync"].read_text() == ""
            if scenario == "missing-or-stale-digest":
                assert not (run / "logs/band.prepared").exists()

            if scenario == "unchanged":
                command = "source /reviewed/profile && test -x '/path with spaces/vasp'"
                for status in (0, 23):
                    patch.setenv("FAKE_SSH_STATUS", str(status))
                    probe = subprocess.run(
                        ["bash", str(plugin_root / PROBE), "cluster.example", command],
                        capture_output=True, text=True,
                    )
                    assert probe.returncode == status
                    assert probe.stdout == "remote probe output\n"
                    assert commands["ssh"].read_text().splitlines() == ["--", "cluster.example", command]
