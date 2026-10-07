from pathlib import Path
from types import SimpleNamespace

import pytest


SCRIPT = "skills/calc-execute/scripts/calculation-monitor.py"
THREAD_ID = "01a095d3-ba82-71f1-8f39-ce44e2943002"


def valid_argv(tmp_path: Path, message: str = "continue **carefully**") -> list[str]:
    spec = tmp_path / "spec.md"
    run = tmp_path / "TASK-001" / "RUN-001"
    spec.write_text("spec\n", encoding="utf-8")
    run.mkdir(parents=True)
    return [
        "--host",
        "mu01",
        "--job-id",
        "123.mu01",
        "--thread-id",
        THREAD_ID,
        "--spec",
        str(spec),
        "--run",
        str(run),
        "--message",
        message,
    ]


def test_monitor_validates_inputs_and_builds_wake_envelope(load_script, tmp_path):
    monitor = load_script(SCRIPT)
    argv = valid_argv(tmp_path)
    config = monitor.parse_args(argv)
    assert monitor.build_delivery(config) == (
        "PBS_JOB_LEFT_QSTAT\n"
        "host=mu01\n"
        "job_id=123.mu01\n"
        f"spec={tmp_path / 'spec.md'}\n"
        f"run={tmp_path / 'TASK-001' / 'RUN-001'}\n"
        "instruction=continue **carefully**"
    )
    for option, value, error in (
        ("--host", "mu01; reboot", "host"),
        ("--job-id", "123.mu01; reboot", "job ID"),
        ("--thread-id", "old-thread", "thread ID"),
        ("--message", "bad\0message", "NUL"),
        ("--message", "界" * 5462, "16 KiB"),
        ("--interval", "0", "interval"),
        ("--interval", "nan", "interval"),
        ("--spec", "relative-spec.md", "Spec"),
    ):
        invalid = argv.copy()
        if option in invalid:
            invalid[invalid.index(option) + 1] = value
        else:
            invalid.extend([option, value])
        with pytest.raises(ValueError, match=error):
            monitor.parse_args(invalid)


def test_monitor_waits_then_delivers_once_even_when_queue_fails(load_script, tmp_path):
    monitor = load_script(SCRIPT)
    config = monitor.parse_args(valid_argv(tmp_path, message="next\nstep"))
    calls, sleeps = [], []
    statuses = iter([0, 7])

    def query(argv):
        calls.append(argv)
        return SimpleNamespace(returncode=next(statuses))

    assert monitor.wait_until_left_qstat(config, runner=query, sleep=sleeps.append) == 7
    assert calls == [[
        "ssh", "mu01", "source /etc/profile >/dev/null 2>&1 && exec qstat 123.mu01",
    ]] * 2
    assert sleeps == [30.0]

    for status in (0, 19):
        calls.clear()

        def deliver(argv):
            calls.append(argv)
            return SimpleNamespace(returncode=status)

        assert monitor.deliver(config, runner=deliver) == status
        assert calls == [[
            "codex", "queue", "--thread", THREAD_ID,
            "--message", monitor.build_delivery(config),
        ]]
