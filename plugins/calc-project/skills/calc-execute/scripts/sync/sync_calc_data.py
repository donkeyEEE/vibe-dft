#!/usr/bin/env python3
"""Preview or synchronize one calculation task with rsync."""
from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath
import re
import shlex
import subprocess
import sys
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None

CONFIG_FILENAME = "calc-sync.yaml"
CONFIG_KEYS = {"local", "server", "exclude"}
YAML_REQUIRED_ERROR = "PyYAML is required to read calc-sync.yaml"
BUILTIN_EXCLUDES = (
    CONFIG_FILENAME, ".calc-sync/", "__pycache__/", ".pytest_cache/", "*.pyc", "*.pyo", ".DS_Store",
    "[Cc][Hh][Gg][Cc][Aa][Rr]", "[Ww][Aa][Vv][Ee][Cc][Aa][Rr]",
    "*.[Hh]5", "*.[Hh][Dd][Ff]5", "*.[Hh][Dd][Ff]",
)


def _has_control(value: str) -> bool:
    return any(ord(character) < 32 or ord(character) == 127 for character in value)


def _is_relative_safe(value: str) -> bool:
    if not value or value == "." or "\\" in value or _has_control(value):
        return False
    parts = value.split("/")
    return not any(part in ("", ".", "..") for part in parts) and not PurePosixPath(value).is_absolute()


def _symlink_component(path: Path, boundary: Path) -> bool:
    try:
        relative = path.absolute().relative_to(boundary.absolute())
    except ValueError:
        return True
    current = boundary.absolute()
    if current.is_symlink():
        return True
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            return True
    return False


def parse_server_path(value: str) -> tuple[str, str]:
    if not isinstance(value, str) or ":" not in value:
        raise ValueError("server must use host:/absolute/task/path")
    host, root = value.split(":", 1)
    host_pattern = r"(?:[A-Za-z0-9][A-Za-z0-9._-]*@)?[A-Za-z0-9][A-Za-z0-9._-]*"
    root_pattern = r"/(?:[A-Za-z0-9._-]+/)*[A-Za-z0-9._-]+"
    parts = root.split("/")[1:]
    if (not re.fullmatch(host_pattern, host) or host.startswith("-") or root == "/"
            or not re.fullmatch(root_pattern, root) or any(part in ("", ".", "..") for part in parts)
            or _has_control(root) or any(character.isspace() for character in root)):
        raise ValueError("server must use host:/absolute/task/path")
    return host, root.rstrip("/")


def _validate_exclude(exclude: Any) -> list[str]:
    if not isinstance(exclude, list):
        return ["exclude must be a list"]
    return [f"exclude[{index}] must be a safe non-empty relative pattern"
            for index, pattern in enumerate(exclude)
            if not isinstance(pattern, str) or not _is_relative_safe(pattern) or pattern.startswith("-")]


def validate_config(config: dict[str, Any], workspace: Path | None = None) -> list[str]:
    workspace = (workspace or Path.cwd()).resolve()
    if not isinstance(config, dict):
        return ["config root must be a mapping"]
    errors: list[str] = []
    unknown, missing = set(config) - CONFIG_KEYS, CONFIG_KEYS - set(config)
    if unknown:
        errors.append("unknown top-level keys: " + ", ".join(sorted(str(key) for key in unknown)))
    if missing:
        errors.append("missing top-level keys: " + ", ".join(sorted(missing)))
    local = config.get("local")
    if not isinstance(local, str) or not _is_relative_safe(local):
        errors.append("local must name a non-empty relative task root inside the project")
    else:
        try:
            (workspace / local).resolve().relative_to(workspace)
        except (OSError, ValueError):
            errors.append("local must stay inside the project root without a symlink escape")
    try:
        parse_server_path(config.get("server"))
    except ValueError as exc:
        errors.append(str(exc))
    errors.extend(_validate_exclude(config.get("exclude")))
    return errors


def load_config(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError(YAML_REQUIRED_ERROR)
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError("invalid calc-sync.yaml syntax") from exc
    if not isinstance(data, dict):
        raise ValueError("config root must be a mapping")
    return data


def remote_identity(config: dict[str, Any]) -> str:
    return parse_server_path(config["server"])[0]


def remote_root(config: dict[str, Any]) -> str:
    return parse_server_path(config["server"])[1]


def list_remote_files(config: dict[str, Any]) -> list[dict[str, Any]]:
    command = "find -- " + shlex.quote(remote_root(config)) + " -type f -printf '%P\\t%s\\t%TY-%Tm-%TdT%TH:%TM:%TS\\n'"
    result = subprocess.run(["ssh", "--", remote_identity(config), command], check=True, text=True, capture_output=True)
    files = []
    for line in result.stdout.splitlines():
        fields = line.split("\t", 2)
        if len(fields) != 3:
            raise ValueError("remote listing returned a malformed entry")
        path, size, mtime = fields
        try:
            size = int(size)
        except ValueError as exc:
            raise ValueError("remote listing returned a malformed size") from exc
        files.append({"path": path, "size": size, "mtime": mtime})
    return files


def _load_cli_config(path: Path) -> dict[str, Any]:
    config = load_config(path)
    errors = validate_config(config, Path.cwd())
    if not errors:
        expected = (Path.cwd() / config["local"] / CONFIG_FILENAME).absolute()
        supplied = (Path.cwd() / path).absolute() if not path.is_absolute() else path.absolute()
        if supplied != expected or supplied.is_symlink() or _symlink_component(supplied, Path.cwd()):
            errors.append(f"config must be exactly {config['local']}/{CONFIG_FILENAME} under the project root")
    if errors:
        raise ValueError("\n".join(errors))
    return config


def _validated_config(path: Path) -> dict[str, Any]:
    try:
        return _load_cli_config(path)
    except (OSError, RuntimeError, ValueError) as exc:
        raise SystemExit("\n".join(f"ERROR: {line}" for line in str(exc).splitlines())) from exc


def build_rsync_command(config: dict[str, Any], direction: str, dry_run: bool) -> list[str]:
    host, root = parse_server_path(config["server"])
    local, remote = str(Path.cwd() / config["local"]) + "/", f"{host}:{root}/"
    source, target = (local, remote) if direction == "push" else (remote, local)
    command = ["rsync", "-a", "--no-links", "--itemize-changes", "--human-readable"]
    if dry_run:
        command.append("--dry-run")
    command.extend(f"--exclude={pattern}" for pattern in (*BUILTIN_EXCLUDES, *config["exclude"]))
    command.extend(["--", source, target])
    return command


def run_rsync(config: dict[str, Any], direction: str, dry_run: bool) -> None:
    subprocess.run(build_rsync_command(config, direction, dry_run), check=True)


def cmd_validate(args: argparse.Namespace) -> int:
    try:
        _load_cli_config(Path(args.config))
    except (OSError, RuntimeError, ValueError) as exc:
        for line in str(exc).splitlines():
            print(f"ERROR: {line}", file=sys.stderr)
        return 1
    print("valid")
    return 0


def cmd_inspect(args: argparse.Namespace) -> int:
    config = _validated_config(Path(args.config))
    for item in list_remote_files(config):
        print(f"{item['path']}\t{item['size']}\t{item['mtime']}")
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    run_rsync(_validated_config(Path(args.config)), args.direction, dry_run=True)
    return 0


def _cmd_transfer(args: argparse.Namespace, direction: str) -> int:
    config = _validated_config(Path(args.config))
    if not args.yes:
        print(f"Refusing to {direction} without --yes; review a {direction} dry-run report first.", file=sys.stderr)
        return 2
    run_rsync(config, direction, dry_run=False)
    return 0


def cmd_push(args: argparse.Namespace) -> int:
    return _cmd_transfer(args, "push")


def cmd_pull(args: argparse.Namespace) -> int:
    return _cmd_transfer(args, "pull")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Preview or synchronize calculation files using calc-sync.yaml.")
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate"); validate.add_argument("config"); validate.set_defaults(func=cmd_validate)
    inspect = commands.add_parser("inspect"); inspect.add_argument("config"); inspect.set_defaults(func=cmd_inspect)
    plan = commands.add_parser("plan"); plan.add_argument("config"); plan.add_argument("--direction", choices=("pull", "push"), default="pull"); plan.set_defaults(func=cmd_plan)
    push = commands.add_parser("push"); push.add_argument("config"); push.add_argument("--yes", action="store_true"); push.set_defaults(func=cmd_push)
    pull = commands.add_parser("pull"); pull.add_argument("config"); pull.add_argument("--yes", action="store_true"); pull.set_defaults(func=cmd_pull)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
