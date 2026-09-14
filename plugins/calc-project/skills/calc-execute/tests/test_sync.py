import argparse
import json
from pathlib import Path
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


def test_minimal_sync_config(load_script, tmp_path):
    module = load_script(SCRIPT)
    config = _config()
    assert module.validate_config(config, tmp_path) == []
    assert module.validate_config({**config, "status": "active"}, tmp_path)
    assert module.validate_config({**config, "local": "../escape"}, tmp_path)


@pytest.mark.parametrize("change", [
    {"local": 7}, {"local": ""}, {"local": "."}, {"local": "data/./TASK-001"},
    {"server": "-oProxyCommand=x:/calc/task"}, {"server": "fake:/"},
    {"server": "fake:relative"}, {"server": "fake:/calc/./TASK-001"},
    {"exclude": "*.tmp"}, {"exclude": [""]}, {"exclude": ["../escape"]},
    {"exclude": ["cache/./*"]}, {"exclude": ["bad\npattern"]},
])
def test_sync_config_rejects_unsafe_or_malformed_values(load_script, tmp_path, change):
    module = load_script(SCRIPT)
    assert module.validate_config({**_config(), **change}, tmp_path)


def test_sync_config_rejects_local_symlink_escape(load_script, tmp_path):
    module = load_script(SCRIPT)
    outside = tmp_path.parent / f"{tmp_path.name}-outside"
    outside.mkdir()
    (tmp_path / "data").symlink_to(outside, target_is_directory=True)
    assert module.validate_config(_config(), tmp_path)


@pytest.mark.parametrize("server", [
    "fake:/calc/*/TASK-001", "fake:/calc/$(touch-pwned)/TASK-001",
    "fake:/calc/TASK-001;echo-pwned",
])
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
    assert module.parse_server_path(server) == ("user-1@cluster.example", "/calc_1/project-2/TASK-001.run")
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


@pytest.mark.parametrize("direction", ["push", "pull"])
def test_plan_is_one_rsync_dry_run_and_saves_no_state(load_script, tmp_path, monkeypatch, direction):
    module = load_script(SCRIPT)
    config = _config(exclude=["*.tmp"])
    config_path = _write_config(tmp_path, config)
    monkeypatch.chdir(tmp_path)
    calls = []
    monkeypatch.setattr(module.subprocess, "run", lambda command, **kwargs: calls.append((command, kwargs)) or SimpleNamespace(returncode=0))
    assert module.cmd_plan(argparse.Namespace(config=str(config_path), direction=direction)) == 0
    assert len(calls) == 1
    command, kwargs = calls[0]
    assert command[0] == "rsync"
    assert "--dry-run" in command
    assert "--no-links" in command
    assert "--delete" not in command
    assert "--exclude=*.tmp" in command
    assert kwargs.get("check") is True
    assert not (tmp_path / config["local"] / ".calc-sync").exists()


@pytest.mark.parametrize("direction", ["push", "pull"])
def test_transfer_is_one_rsync_without_remote_probes_or_saved_plan(load_script, tmp_path, monkeypatch, direction):
    module = load_script(SCRIPT)
    config_path = _write_config(tmp_path, _config())
    monkeypatch.chdir(tmp_path)
    calls = []
    monkeypatch.setattr(module.subprocess, "run", lambda command, **kwargs: calls.append((command, kwargs)) or SimpleNamespace(returncode=0))
    function = module.cmd_push if direction == "push" else module.cmd_pull
    assert function(argparse.Namespace(config=str(config_path), yes=True)) == 0
    assert len(calls) == 1
    command, kwargs = calls[0]
    assert command[0] == "rsync"
    assert "--dry-run" not in command
    assert "--no-links" in command
    assert "--delete" not in command
    assert kwargs.get("check") is True


def test_rsync_excludes_large_scientific_files_local_state_and_caches(load_script):
    module = load_script(SCRIPT)
    command = module.build_rsync_command(_config(exclude=["scratch/*"]), "push", dry_run=False)
    excludes = {argument for argument in command if argument.startswith("--exclude=")}
    for expected in (
        "--exclude=scratch/*", "--exclude=calc-sync.yaml", "--exclude=.calc-sync/",
        "--exclude=__pycache__/", "--exclude=[Cc][Hh][Gg][Cc][Aa][Rr]",
        "--exclude=[Ww][Aa][Vv][Ee][Cc][Aa][Rr]", "--exclude=*.[Hh]5",
        "--exclude=*.[Hh][Dd][Ff]5", "--exclude=*.[Hh][Dd][Ff]",
    ):
        assert expected in excludes


def test_transfer_requires_yes_before_rsync(load_script, tmp_path, monkeypatch, capsys):
    module = load_script(SCRIPT)
    config_path = _write_config(tmp_path, _config())
    monkeypatch.chdir(tmp_path)
    calls = []
    monkeypatch.setattr(module.subprocess, "run", lambda *args, **kwargs: calls.append((args, kwargs)))
    assert module.cmd_pull(argparse.Namespace(config=str(config_path), yes=False)) == 2
    assert calls == []
    assert "--yes" in capsys.readouterr().err


def test_cli_requires_exact_task_root_calc_sync_path_and_has_no_init(load_script, tmp_path, monkeypatch):
    module = load_script(SCRIPT)
    config = _config()
    actual = _write_config(tmp_path, config)
    alias = tmp_path / "other.yaml"
    alias.write_bytes(actual.read_bytes())
    monkeypatch.chdir(tmp_path)
    assert module.cmd_validate(argparse.Namespace(config=str(alias))) == 1
    assert "init" not in module.build_parser()._subparsers._group_actions[0].choices
