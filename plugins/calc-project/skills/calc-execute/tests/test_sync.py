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


def test_sync_validates_paths_and_rejects_invalid_requests_before_remote_calls(
    load_script, tmp_path, monkeypatch, capsys
):
    module = load_script(SCRIPT)
    config = _config()
    assert module.validate_config(config, tmp_path) == []
    for change in (
        {"status": "active"}, {"local": "../escape"}, {"local": 7},
        {"local": ""}, {"local": "."}, {"local": "data/./TASK-001"},
        {"server": "-oProxyCommand=x:/calc/task"}, {"server": "fake:/"},
        {"server": "fake:relative"}, {"server": "fake:/calc/./TASK-001"},
        {"exclude": "*.tmp"}, {"exclude": [""]}, {"exclude": ["../escape"]},
        {"exclude": ["cache/./*"]}, {"exclude": ["bad\npattern"]},
    ):
        assert module.validate_config({**config, **change}, tmp_path), change
    server = "user-1@cluster.example:/calc_1/project-2/TASK-001.run"
    assert module.parse_server_path(server) == (
        "user-1@cluster.example", "/calc_1/project-2/TASK-001.run",
    )
    assert module.validate_config(_config(server=server), tmp_path) == []

    outside = tmp_path.parent / f"{tmp_path.name}-outside"
    outside.mkdir()
    (tmp_path / "data").symlink_to(outside, target_is_directory=True)
    assert module.validate_config(config, tmp_path)
    (tmp_path / "data").unlink()

    monkeypatch.chdir(tmp_path)
    calls = []
    monkeypatch.setattr(module.subprocess, "run", lambda *a, **kw: calls.append((a, kw)))
    for server in (
        "fake:/calc/*/TASK-001", "fake:/calc/$(touch-pwned)/TASK-001",
        "fake:/calc/TASK-001;echo-pwned",
    ):
        invalid = _config(server=server)
        path = _write_config(tmp_path, invalid)
        assert module.validate_config(invalid, tmp_path)
        with pytest.raises(SystemExit):
            module.cmd_plan(argparse.Namespace(config=str(path), direction="pull"))
        assert calls == []

    path.write_text("local: [unterminated\n", encoding="utf-8")
    with pytest.raises(ValueError, match="invalid calc-sync.yaml"):
        module.load_config(path)
    assert module.cmd_validate(argparse.Namespace(config=str(path))) == 1
    for function, arguments in (
        (module.cmd_inspect, argparse.Namespace(config=str(path))),
        (module.cmd_plan, argparse.Namespace(config=str(path), direction="pull")),
        (module.cmd_push, argparse.Namespace(config=str(path), yes=True)),
        (module.cmd_pull, argparse.Namespace(config=str(path), yes=True)),
    ):
        with pytest.raises(SystemExit, match="invalid calc-sync.yaml"):
            function(arguments)
    captured = capsys.readouterr()
    assert "invalid calc-sync.yaml" in captured.err
    assert "Traceback" not in captured.err
    assert calls == []

    path = _write_config(tmp_path, config)
    alias = tmp_path / "other.yaml"
    alias.write_bytes(path.read_bytes())
    assert module.cmd_validate(argparse.Namespace(config=str(alias))) == 1
    assert "init" not in module.build_parser()._subparsers._group_actions[0].choices
    assert module.cmd_pull(argparse.Namespace(config=str(path), yes=False)) == 2
    assert "--yes" in capsys.readouterr().err
    assert calls == []


def test_sync_previews_and_transfers_both_directions_without_deleting_or_saving_state(
    load_script, tmp_path, monkeypatch
):
    module = load_script(SCRIPT)
    config = _config(exclude=["*.tmp", "scratch/*"])
    path = _write_config(tmp_path, config)
    monkeypatch.chdir(tmp_path)
    calls = []
    monkeypatch.setattr(
        module.subprocess, "run",
        lambda command, **kw: calls.append((command, kw)) or SimpleNamespace(returncode=0),
    )
    for direction in ("push", "pull"):
        for dry_run in (True, False):
            calls.clear()
            if dry_run:
                status = module.cmd_plan(argparse.Namespace(config=str(path), direction=direction))
            else:
                transfer = module.cmd_push if direction == "push" else module.cmd_pull
                status = transfer(argparse.Namespace(config=str(path), yes=True))
            assert status == 0
            assert len(calls) == 1
            command, kwargs = calls[0]
            assert command[0] == "rsync"
            assert ("--dry-run" in command) is dry_run
            assert "--no-links" in command
            assert "--delete" not in command
            assert kwargs.get("check") is True
            excludes = {arg for arg in command if arg.startswith("--exclude=")}
            assert {
                "--exclude=*.tmp", "--exclude=scratch/*", "--exclude=calc-sync.yaml",
                "--exclude=.calc-sync/", "--exclude=__pycache__/",
                "--exclude=[Cc][Hh][Gg][Cc][Aa][Rr]", "--exclude=[Ww][Aa][Vv][Ee][Cc][Aa][Rr]",
                "--exclude=*.[Hh]5", "--exclude=*.[Hh][Dd][Ff]5", "--exclude=*.[Hh][Dd][Ff]",
            } <= excludes
            assert not (tmp_path / config["local"] / ".calc-sync").exists()
