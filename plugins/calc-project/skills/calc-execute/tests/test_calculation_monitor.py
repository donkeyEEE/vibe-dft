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


def test_builds_fixed_context_envelope(load_script, tmp_path):
    monitor = load_script(SCRIPT)
    config = monitor.parse_args(valid_argv(tmp_path))

    assert monitor.build_delivery(config) == (
        "PBS_JOB_LEFT_QSTAT\n"
        "host=mu01\n"
        "job_id=123.mu01\n"
        f"spec={tmp_path / 'spec.md'}\n"
        f"run={tmp_path / 'TASK-001' / 'RUN-001'}\n"
        "instruction=continue **carefully**"
    )


@pytest.mark.parametrize(
    ("option", "value", "error"),
    [
        ("--host", "mu01; reboot", "host"),
        ("--job-id", "123.mu01; reboot", "job ID"),
        ("--thread-id", "old-thread", "thread ID"),
        ("--message", "bad\0message", "NUL"),
        ("--message", "界" * 5462, "16 KiB"),
        ("--interval", "0", "interval"),
        ("--interval", "nan", "interval"),
    ],
)
def test_rejects_invalid_values(load_script, tmp_path, option, value, error):
    monitor = load_script(SCRIPT)
    argv = valid_argv(tmp_path)
    if option in argv:
        argv[argv.index(option) + 1] = value
    else:
        argv.extend([option, value])

    with pytest.raises(ValueError, match=error):
        monitor.parse_args(argv)


def test_requires_existing_absolute_spec_and_run(load_script, tmp_path):
    monitor = load_script(SCRIPT)
    argv = valid_argv(tmp_path)
    argv[argv.index("--spec") + 1] = "relative-spec.md"

    with pytest.raises(ValueError, match="Spec"):
        monitor.parse_args(argv)


def test_qstat_loads_remote_profile_and_zero_waits(load_script, tmp_path):
    monitor = load_script(SCRIPT)
    config = monitor.parse_args(valid_argv(tmp_path))
    calls = []
    statuses = iter([0, 7])

    def runner(argv):
        calls.append(argv)
        return SimpleNamespace(returncode=next(statuses))

    sleeps = []
    status = monitor.wait_until_left_qstat(config, runner=runner, sleep=sleeps.append)

    assert status == 7
    assert calls == [
        [
            "ssh",
            "mu01",
            "source /etc/profile >/dev/null 2>&1 && exec qstat 123.mu01",
        ],
        [
            "ssh",
            "mu01",
            "source /etc/profile >/dev/null 2>&1 && exec qstat 123.mu01",
        ],
    ]
    assert sleeps == [30.0]


def test_nonzero_qstat_causes_exactly_one_queue_attempt(load_script, tmp_path):
    monitor = load_script(SCRIPT)
    config = monitor.parse_args(valid_argv(tmp_path, message="next\nstep"))
    calls = []

    def runner(argv):
        calls.append(argv)
        return SimpleNamespace(returncode=0)

    assert monitor.deliver(config, runner=runner) == 0
    assert calls == [
        [
            "codex",
            "queue",
            "--thread",
            THREAD_ID,
            "--message",
            monitor.build_delivery(config),
        ]
    ]


def test_queue_failure_is_returned_without_retry(load_script, tmp_path):
    monitor = load_script(SCRIPT)
    config = monitor.parse_args(valid_argv(tmp_path))
    calls = []

    def runner(argv):
        calls.append(argv)
        return SimpleNamespace(returncode=19)

    assert monitor.deliver(config, runner=runner) == 19
    assert len(calls) == 1
