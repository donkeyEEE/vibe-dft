import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from types import SimpleNamespace

import pytest


SCRIPT = "skills/calc-execute/scripts/sync/sync_calc_data.py"


def _config(local="data/TASK-001", server="fake:/calc/TASK-001", exclude=None):
    return {"local": local, "server": server, "exclude": [] if exclude is None else exclude}


def _write_config(project_root: Path, config: dict) -> Path:
    task_root = project_root / config["local"]
    task_root.mkdir(parents=True, exist_ok=True)
    path = task_root / "calc-sync.yaml"
    path.write_text(
        f"local: {config['local']}\nserver: {config['server']}\nexclude: {json.dumps(config['exclude'])}\n",
        encoding="utf-8",
    )
    return path


def _remote_result(kind="MISSING", data=b""):
    if kind == "REGULAR":
        digest = hashlib.sha256(data).hexdigest()
        stdout = f"REGULAR\t{len(data)}\t{digest}\n"
    else:
        stdout = kind + "\n"
    return SimpleNamespace(stdout=stdout, returncode=0)


def test_minimal_sync_config(load_script, tmp_path):
    module = load_script(SCRIPT)
    config = _config()
    assert module.validate_config(config, tmp_path) == []
    assert module.validate_config({**config, "status": "active"}, tmp_path)
    assert module.validate_config({**config, "local": "../escape"}, tmp_path)


@pytest.mark.parametrize(
    "change",
    [
        {"local": 7},
        {"local": ""},
        {"local": "."},
        {"local": "data/./TASK-001"},
        {"server": "-oProxyCommand=x:/calc/task"},
        {"server": "fake:/"},
        {"server": "fake:relative"},
        {"server": "fake:/calc/./TASK-001"},
        {"exclude": "*.tmp"},
        {"exclude": [""]},
        {"exclude": ["../escape"]},
        {"exclude": ["cache/./*"]},
        {"exclude": ["bad\npattern"]},
    ],
)
def test_sync_config_rejects_unsafe_or_malformed_values(load_script, tmp_path, change):
    module = load_script(SCRIPT)
    assert module.validate_config({**_config(), **change}, tmp_path)


def test_sync_config_rejects_local_symlink_escape(load_script, tmp_path):
    module = load_script(SCRIPT)
    outside = tmp_path.parent / f"{tmp_path.name}-outside"
    outside.mkdir()
    (tmp_path / "data").symlink_to(outside, target_is_directory=True)
    assert module.validate_config(_config(), tmp_path)


@pytest.mark.parametrize(
    "server",
    [
        "fake:/calc/*/TASK-001",
        "fake:/calc/$(touch-pwned)/TASK-001",
        "fake:/calc/TASK-001;echo-pwned",
    ],
)
def test_remote_root_rejects_transport_metacharacters_before_remote_call(load_script, tmp_path, monkeypatch, server):
    module = load_script(SCRIPT)
    config = _config(server=server)
    config_path = _write_config(tmp_path, config)
    monkeypatch.chdir(tmp_path)
    calls = []
    monkeypatch.setattr(module.subprocess, "run", lambda *args, **kwargs: calls.append((args, kwargs)))

    assert module.validate_config(config, tmp_path)
    with pytest.raises(SystemExit):
        module.cmd_plan(argparse.Namespace(config=str(config_path), direction="pull"))
    assert calls == []


def test_remote_root_accepts_portable_path_characters(load_script, tmp_path):
    module = load_script(SCRIPT)
    server = "user-1@cluster.example:/calc_1/project-2/TASK-001.run"
    assert module.parse_server_path(server) == (
        "user-1@cluster.example",
        "/calc_1/project-2/TASK-001.run",
    )
    assert module.validate_config(_config(server=server), tmp_path) == []


def test_malformed_yaml_is_a_controlled_cli_error_before_remote_call(load_script, tmp_path, monkeypatch, capsys):
    module = load_script(SCRIPT)
    config_path = tmp_path / "data" / "TASK-001" / "calc-sync.yaml"
    config_path.parent.mkdir(parents=True)
    config_path.write_text("local: [unterminated\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    calls = []
    monkeypatch.setattr(module.subprocess, "run", lambda *args, **kwargs: calls.append((args, kwargs)))

    with pytest.raises(ValueError, match="invalid calc-sync.yaml"):
        module.load_config(config_path)
    assert module.cmd_validate(argparse.Namespace(config=str(config_path))) == 1
    for function, arguments in (
        (module.cmd_inspect, argparse.Namespace(config=str(config_path))),
        (module.cmd_plan, argparse.Namespace(config=str(config_path), direction="pull")),
        (module.cmd_push, argparse.Namespace(config=str(config_path), yes=True)),
        (module.cmd_pull, argparse.Namespace(config=str(config_path), yes=True)),
    ):
        with pytest.raises(SystemExit, match="invalid calc-sync.yaml"):
            function(arguments)

    captured = capsys.readouterr()
    assert "invalid calc-sync.yaml" in captured.err
    assert "Traceback" not in captured.err
    assert calls == []


def test_review_plan_expiry(load_script, tmp_path):
    module = load_script(SCRIPT)
    config = _config()
    plan = {"upload": [], "skipped": []}
    module.write_reviewed_plan(config, "push", plan, tmp_path, now=100)
    assert module.load_reviewed_plan(config, "push", tmp_path, now=101) == plan
    with pytest.raises(ValueError):
        module.load_reviewed_plan(config, "push", tmp_path, now=1901)


@pytest.mark.parametrize("stamp", [float("nan"), float("inf"), float("-inf")])
def test_review_plan_rejects_nonfinite_timestamps(load_script, tmp_path, stamp):
    module = load_script(SCRIPT)
    with pytest.raises(ValueError):
        module.write_reviewed_plan(_config(), "push", {"upload": [], "skipped": []}, tmp_path, now=stamp)


def test_review_plan_binds_flat_config_direction_and_exact_list(load_script, tmp_path):
    module = load_script(SCRIPT)
    config = _config()
    plan = {"upload": [{"source": "safe.dat", "target": "safe.dat", "size": 1}], "skipped": []}
    artifact = module.write_reviewed_plan(config, "push", plan, tmp_path, now=100)

    with pytest.raises(ValueError):
        module.load_reviewed_plan(config, "pull", tmp_path, now=101)
    with pytest.raises(ValueError):
        module.load_reviewed_plan({**config, "exclude": ["*.dat"]}, "push", tmp_path, now=101)

    payload = json.loads(artifact.read_text(encoding="utf-8"))
    payload["plan"]["upload"][0]["source"] = "other.dat"
    artifact.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError):
        module.load_reviewed_plan(config, "push", tmp_path, now=101)


def test_review_plan_refuses_symlinked_state_directory(load_script, tmp_path):
    module = load_script(SCRIPT)
    outside = tmp_path / "outside"
    outside.mkdir()
    task_root = tmp_path / "task"
    task_root.mkdir()
    plan = {"upload": [], "skipped": []}
    artifact = module.write_reviewed_plan(_config(local="task"), "push", plan, task_root, now=100)
    reviewed_bytes = artifact.read_bytes()
    artifact.unlink()
    artifact.parent.rmdir()
    (outside / "reviewed-plan.json").write_bytes(reviewed_bytes)
    (task_root / ".calc-sync").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match="path"):
        module.write_reviewed_plan(_config(local="task"), "push", plan, task_root, now=100)
    with pytest.raises(ValueError, match="path"):
        module.load_reviewed_plan(_config(local="task"), "push", task_root, now=101)


def test_planners_hard_exclude_large_scientific_files_and_local_state(load_script, tmp_path):
    module = load_script(SCRIPT)
    task_root = tmp_path / "data" / "TASK-001"
    for relative in (
        "RUN-001/outputs/result.HdF5",
        "RUN-001/inputs/CHGCAR",
        "RUN-001/inputs/wavecar",
        "calc-sync.yaml",
        ".calc-sync/reviewed-plan.json",
        "__pycache__/helper.pyc",
        "RUN-001/outputs/value.dat",
    ):
        path = task_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"x")

    push = module.build_push_plan(_config(), task_root)
    assert [item["source"] for item in push["upload"]] == ["RUN-001/outputs/value.dat"]

    pull = module.build_pull_plan(
        _config(),
        [
            {"path": "RUN-001/outputs/data.H5", "size": 1},
            {"path": "RUN-001/outputs/WAVECAR", "size": 1},
            {"path": "RUN-001/logs/job.log", "size": 1},
        ],
    )
    assert [item["source"] for item in pull["download"]] == ["RUN-001/logs/job.log"]


@pytest.mark.parametrize(
    ("direction", "plan"),
    [
        ("push", {"upload": [{"source": "../escape", "target": "../escape", "size": 1}], "skipped": []}),
        ("pull", {"download": [{"source": "RUN-001/outputs/A.HDF", "target": "RUN-001/outputs/A.HDF", "size": 1}], "review_needed": [], "skipped": []}),
    ],
)
def test_transfer_revalidates_traversal_and_protected_entries(load_script, tmp_path, monkeypatch, direction, plan):
    module = load_script(SCRIPT)
    calls = []
    monkeypatch.setattr(module.subprocess, "run", lambda *args, **kwargs: calls.append((args, kwargs)))
    function = module.sync_uploads if direction == "push" else module.sync_downloads
    with pytest.raises(ValueError):
        function(_config(), plan, tmp_path)
    assert calls == []


def test_push_consumes_exact_reviewed_list_without_planning(load_script, tmp_path, monkeypatch):
    module = load_script(SCRIPT)
    project_root = tmp_path
    config = _config()
    config_path = _write_config(project_root, config)
    task_root = project_root / config["local"]
    source = task_root / "RUN-001" / "outputs" / "energy result.dat"
    source.parent.mkdir(parents=True)
    source.write_bytes(b"ok")
    plan = {"upload": [{"source": "RUN-001/outputs/energy result.dat", "target": "RUN-001/outputs/energy result.dat", "size": 2}], "skipped": []}
    module.write_reviewed_plan(config, "push", plan, task_root)
    monkeypatch.chdir(project_root)
    monkeypatch.setattr(module, "build_push_plan", lambda *args: pytest.fail("push replanned"))
    monkeypatch.setattr(module, "list_remote_files", lambda *args: pytest.fail("push listed remote files"))
    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        if command[0] == "ssh":
            return _remote_result()
        assert command[0] == "rsync"
        file_list = Path(command[command.index("--files-from") + 1])
        assert file_list.read_bytes() == b"RUN-001/outputs/energy result.dat\n"
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(module.subprocess, "run", fake_run)
    assert module.cmd_push(argparse.Namespace(config=str(config_path), yes=True)) == 0
    rsync = [command for command in calls if command[0] == "rsync"]
    assert len(rsync) == 1
    assert not any(
        argument.startswith("--delete") or argument in {"--remove-source-files", "--copy-links", "--inplace"}
        for argument in rsync[0]
    )


def test_pull_consumes_exact_reviewed_list_without_planning(load_script, tmp_path, monkeypatch):
    module = load_script(SCRIPT)
    project_root = tmp_path
    config = _config()
    config_path = _write_config(project_root, config)
    task_root = project_root / config["local"]
    plan = {
        "download": [{"source": "RUN-001/logs/job output.log", "target": "RUN-001/logs/job output.log", "size": 3}],
        "review_needed": [],
        "skipped": [],
    }
    module.write_reviewed_plan(config, "pull", plan, task_root)
    monkeypatch.chdir(project_root)
    monkeypatch.setattr(module, "build_pull_plan", lambda *args: pytest.fail("pull replanned"))
    monkeypatch.setattr(module, "list_remote_files", lambda *args: pytest.fail("pull listed remote files"))
    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        if command[0] == "ssh":
            return _remote_result("REGULAR", b"log")
        assert command[0] == "rsync"
        file_list = Path(command[command.index("--files-from") + 1])
        assert file_list.read_bytes() == b"RUN-001/logs/job output.log\n"
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(module.subprocess, "run", fake_run)
    assert module.cmd_pull(argparse.Namespace(config=str(config_path), yes=True)) == 0
    rsync = [command for command in calls if command[0] == "rsync"]
    assert len(rsync) == 1
    assert not any(
        argument.startswith("--delete") or argument in {"--remove-source-files", "--copy-links", "--inplace"}
        for argument in rsync[0]
    )


@pytest.mark.parametrize("failure", ["missing", "expired", "wrong_direction", "changed_config", "changed_list"])
def test_push_refuses_invalid_reviewed_plan_before_subprocess(load_script, tmp_path, monkeypatch, failure):
    module = load_script(SCRIPT)
    config = _config()
    config_path = _write_config(tmp_path, config)
    task_root = tmp_path / config["local"]
    plan = {"upload": [], "skipped": []}
    if failure != "missing":
        artifact = module.write_reviewed_plan(config, "pull" if failure == "wrong_direction" else "push", plan if failure != "wrong_direction" else {"download": [], "review_needed": [], "skipped": []}, task_root, now=100)
        if failure == "changed_list":
            payload = json.loads(artifact.read_text(encoding="utf-8"))
            payload["plan"]["upload"].append({"source": "new", "target": "new", "size": 0})
            artifact.write_text(json.dumps(payload), encoding="utf-8")
        if failure == "changed_config":
            config["exclude"] = ["*.tmp"]
            config_path = _write_config(tmp_path, config)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(module.time, "time", lambda: 1901 if failure == "expired" else 101)
    calls = []
    monkeypatch.setattr(module.subprocess, "run", lambda *args, **kwargs: calls.append((args, kwargs)))
    assert module.cmd_push(argparse.Namespace(config=str(config_path), yes=True)) == 2
    assert calls == []


@pytest.mark.parametrize("failure", ["missing", "expired", "wrong_direction", "changed_config", "changed_list"])
def test_pull_refuses_invalid_reviewed_plan_before_subprocess(load_script, tmp_path, monkeypatch, failure):
    module = load_script(SCRIPT)
    config = _config()
    config_path = _write_config(tmp_path, config)
    task_root = tmp_path / config["local"]
    plan = {"download": [], "review_needed": [], "skipped": []}
    if failure != "missing":
        artifact = module.write_reviewed_plan(config, "push" if failure == "wrong_direction" else "pull", plan if failure != "wrong_direction" else {"upload": [], "skipped": []}, task_root, now=100)
        if failure == "changed_list":
            payload = json.loads(artifact.read_text(encoding="utf-8"))
            payload["plan"]["download"].append({"source": "new", "target": "new", "size": 0})
            artifact.write_text(json.dumps(payload), encoding="utf-8")
        if failure == "changed_config":
            config["exclude"] = ["*.tmp"]
            config_path = _write_config(tmp_path, config)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(module.time, "time", lambda: 1901 if failure == "expired" else 101)
    calls = []
    monkeypatch.setattr(module.subprocess, "run", lambda *args, **kwargs: calls.append((args, kwargs)))
    assert module.cmd_pull(argparse.Namespace(config=str(config_path), yes=True)) == 2
    assert calls == []


def test_pull_refuses_symlink_ancestor_before_rsync(load_script, tmp_path, monkeypatch):
    module = load_script(SCRIPT)
    outside = tmp_path / "outside"
    outside.mkdir()
    task_root = tmp_path / "task"
    task_root.mkdir()
    (task_root / "RUN-001").symlink_to(outside, target_is_directory=True)
    plan = {
        "download": [{"source": "RUN-001/logs/job.log", "target": "RUN-001/logs/job.log", "size": 3}],
        "review_needed": [],
        "skipped": [],
    }
    calls = []
    monkeypatch.setattr(module.subprocess, "run", lambda *args, **kwargs: calls.append((args, kwargs)))
    with pytest.raises(ValueError):
        module.sync_downloads(_config(local="task"), plan, task_root)
    assert not any(args[0][0] == "rsync" for args in calls)


@pytest.mark.parametrize("direction", ["push", "pull"])
def test_remote_symlink_path_is_refused_before_rsync(load_script, tmp_path, monkeypatch, direction):
    module = load_script(SCRIPT)
    task_root = tmp_path / "task"
    relative = "RUN-001/logs/job.log"
    source = task_root / relative
    source.parent.mkdir(parents=True)
    source.write_bytes(b"log")
    transfer = {"source": relative, "target": relative, "size": 3}
    plan = {"upload": [transfer], "skipped": []} if direction == "push" else {"download": [transfer], "review_needed": [], "skipped": []}
    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        return _remote_result("SYMLINK")

    monkeypatch.setattr(module.subprocess, "run", fake_run)
    function = module.sync_uploads if direction == "push" else module.sync_downloads
    with pytest.raises(ValueError, match="remote path"):
        function(_config(local="task"), plan, task_root)
    assert not any(command[0] == "rsync" for command in calls)


def test_remote_safety_probe_shell_checks_exact_path_and_symlink_ancestors(load_script, tmp_path):
    module = load_script(SCRIPT)
    remote_root = tmp_path / "remote"
    regular = remote_root / "RUN-001" / "logs" / "job output.log"
    regular.parent.mkdir(parents=True)
    regular.write_bytes(b"log")
    result = subprocess.run(
        ["sh", "-c", module._remote_probe_command(str(remote_root), "RUN-001/logs/job output.log")],
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout == f"REGULAR\t3\t{hashlib.sha256(b'log').hexdigest()}\n"

    linked_root = tmp_path / "linked"
    linked_root.mkdir()
    (linked_root / "RUN-001").symlink_to(remote_root / "RUN-001", target_is_directory=True)
    result = subprocess.run(
        ["sh", "-c", module._remote_probe_command(str(linked_root), "RUN-001/logs/job output.log")],
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stdout == "SYMLINK\n"


@pytest.mark.parametrize("direction", ["push", "pull"])
def test_existing_run_input_destination_must_be_byte_identical(load_script, tmp_path, monkeypatch, direction):
    module = load_script(SCRIPT)
    task_root = tmp_path / "task"
    relative = "RUN-001/inputs/run.pbs"
    local = task_root / relative
    local.parent.mkdir(parents=True)
    local.write_bytes(b"local")
    transfer = {"source": relative, "target": relative, "size": 5 if direction == "push" else 6}
    plan = {"upload": [transfer], "skipped": []} if direction == "push" else {"download": [transfer], "review_needed": [], "skipped": []}
    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        assert command[0] == "ssh"
        return _remote_result("REGULAR", b"remote")

    monkeypatch.setattr(module.subprocess, "run", fake_run)
    function = module.sync_uploads if direction == "push" else module.sync_downloads
    with pytest.raises(ValueError, match="immutable Run input"):
        function(_config(local="task"), plan, task_root)
    assert not any(command[0] == "rsync" for command in calls)


@pytest.mark.parametrize("direction", ["push", "pull"])
def test_existing_identical_run_input_is_idempotent(load_script, tmp_path, monkeypatch, direction):
    module = load_script(SCRIPT)
    task_root = tmp_path / "task"
    relative = "RUN-001/inputs/run.pbs"
    local = task_root / relative
    local.parent.mkdir(parents=True)
    local.write_bytes(b"same")
    transfer = {"source": relative, "target": relative, "size": 4}
    plan = {"upload": [transfer], "skipped": []} if direction == "push" else {"download": [transfer], "review_needed": [], "skipped": []}
    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        return _remote_result("REGULAR", b"same") if command[0] == "ssh" else SimpleNamespace(returncode=0)

    monkeypatch.setattr(module.subprocess, "run", fake_run)
    function = module.sync_uploads if direction == "push" else module.sync_downloads
    function(_config(local="task"), plan, task_root)
    assert len([command for command in calls if command[0] == "rsync"]) == 1


def test_cli_requires_exact_task_root_calc_sync_path_and_has_no_init(load_script, tmp_path, monkeypatch):
    module = load_script(SCRIPT)
    config = _config()
    actual = _write_config(tmp_path, config)
    alias = tmp_path / "other.yaml"
    alias.write_bytes(actual.read_bytes())
    monkeypatch.chdir(tmp_path)
    assert module.cmd_validate(argparse.Namespace(config=str(alias))) == 1
    assert "init" not in module.build_parser()._subparsers._group_actions[0].choices
