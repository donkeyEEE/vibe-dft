#!/usr/bin/env python3
"""Review and synchronize one calculation task's exact file list."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import shlex
import subprocess
import sys
import tempfile
import time
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None


CONFIG_FILENAME = "calc-sync.yaml"
CONFIG_KEYS = {"local", "server", "exclude"}
DEFAULT_LARGE_FILE_THRESHOLD_MB = 50
LOCAL_CACHE_PATTERNS = (
    "__pycache__/*",
    "*/__pycache__/*",
    ".pytest_cache/*",
    "*/.pytest_cache/*",
    "*.pyc",
    "*.pyo",
    ".DS_Store",
)
REVIEWED_PLAN_DIRECTORY = ".calc-sync"
REVIEWED_PLAN_FILENAME = "reviewed-plan.json"
REVIEWED_PLAN_SCHEMA_VERSION = 3
REVIEWED_PLAN_TTL_SECONDS = 30 * 60
YAML_REQUIRED_ERROR = "PyYAML is required to read calc-sync.yaml"


def _has_control(value: str) -> bool:
    return any(ord(character) < 32 or ord(character) == 127 for character in value)


def _is_relative_safe(value: str) -> bool:
    if not value or value == "." or "\\" in value or _has_control(value):
        return False
    raw_parts = value.split("/")
    if any(part in ("", ".", "..") for part in raw_parts):
        return False
    pure = PurePosixPath(value)
    return not pure.is_absolute()


def _symlink_component(path: Path, boundary: Path) -> bool:
    """Return whether an existing component from boundary through path is a link."""
    try:
        relative = path.absolute().relative_to(boundary.absolute())
    except ValueError:
        return True
    current = boundary.absolute()
    if current.is_symlink():
        return True
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            return True
    return False


def parse_server_path(value: str) -> tuple[str, str]:
    if not isinstance(value, str) or ":" not in value:
        raise ValueError("server must use host:/absolute/task/path")
    host, root = value.split(":", 1)
    host_pattern = r"(?:[A-Za-z0-9][A-Za-z0-9._-]*@)?[A-Za-z0-9][A-Za-z0-9._-]*"
    root_pattern = r"/(?:[A-Za-z0-9._-]+/)*[A-Za-z0-9._-]+"
    root_path = PurePosixPath(root)
    raw_root_parts = root.split("/")[1:]
    if (
        not re.fullmatch(host_pattern, host)
        or host.startswith("-")
        or not root.startswith("/")
        or root == "/"
        or not re.fullmatch(root_pattern, root)
        or ".." in root_path.parts
        or any(part in ("", ".", "..") for part in raw_root_parts)
        or _has_control(root)
        or any(character.isspace() for character in root)
    ):
        raise ValueError("server must use host:/absolute/task/path")
    return host, root.rstrip("/")


def _validate_exclude(exclude: Any) -> list[str]:
    if not isinstance(exclude, list):
        return ["exclude must be a list"]
    errors = []
    for index, pattern in enumerate(exclude):
        if (
            not isinstance(pattern, str)
            or not _is_relative_safe(pattern)
            or pattern.startswith("-")
        ):
            errors.append(f"exclude[{index}] must be a safe non-empty relative pattern")
    return errors


def validate_config(config: dict[str, Any], workspace: Path | None = None) -> list[str]:
    workspace = (workspace or Path.cwd()).resolve()
    if not isinstance(config, dict):
        return ["config root must be a mapping"]
    errors: list[str] = []
    unknown = set(config) - CONFIG_KEYS
    missing = CONFIG_KEYS - set(config)
    if unknown:
        errors.append("unknown top-level keys: " + ", ".join(sorted(str(key) for key in unknown)))
    if missing:
        errors.append("missing top-level keys: " + ", ".join(sorted(missing)))

    local = config.get("local")
    if not isinstance(local, str) or not _is_relative_safe(local):
        errors.append("local must name a non-empty relative task root inside the project")
    else:
        local_path = workspace / local
        try:
            local_path.resolve().relative_to(workspace)
        except (OSError, ValueError):
            errors.append("local must stay inside the project root without a symlink escape")

    server = config.get("server")
    try:
        parse_server_path(server)
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


def _matches(path: str, pattern: str) -> bool:
    return fnmatch.fnmatchcase(path, pattern) or fnmatch.fnmatchcase(PurePosixPath(path).name, pattern)


def _hard_excluded(path: str) -> bool:
    name = PurePosixPath(path).name.lower()
    return name in {"chgcar", "wavecar"} or PurePosixPath(name).suffix in {".h5", ".hdf5", ".hdf"}


def _excluded(config: dict[str, Any], path: str) -> bool:
    return _hard_excluded(path) or any(_matches(path, pattern) for pattern in config["exclude"])


def _local_state(path: str) -> bool:
    return (
        path == CONFIG_FILENAME
        or path == REVIEWED_PLAN_DIRECTORY
        or path.startswith(REVIEWED_PLAN_DIRECTORY + "/")
        or any(_matches(path, pattern) for pattern in LOCAL_CACHE_PATTERNS)
    )


def build_pull_plan(config: dict[str, Any], remote_files: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    threshold = DEFAULT_LARGE_FILE_THRESHOLD_MB * 1024 * 1024
    plan: dict[str, list[dict[str, Any]]] = {"download": [], "review_needed": [], "skipped": []}
    for item in remote_files:
        path = item.get("path") if isinstance(item, dict) else None
        size = item.get("size", 0) if isinstance(item, dict) else None
        if not isinstance(path, str) or not _is_relative_safe(path) or isinstance(size, bool) or not isinstance(size, int) or size < 0:
            raise ValueError("remote listing contains an unsafe file entry")
        if _excluded(config, path):
            plan["skipped"].append({"source": path, "reason": "excluded_by_policy", "size": size})
        elif size > threshold:
            plan["review_needed"].append({"source": path, "reason": "large_file", "size": size})
        else:
            plan["download"].append({"source": path, "target": path, "size": size})
    return plan


def build_push_plan(config: dict[str, Any], task_root: Path) -> dict[str, list[dict[str, Any]]]:
    upload: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    if task_root.is_symlink() or not task_root.is_dir():
        raise ValueError("local task root must be an existing non-symlink directory")
    for path in sorted(task_root.rglob("*")):
        rel = path.relative_to(task_root).as_posix()
        if _symlink_component(path, task_root):
            skipped.append({"source": rel, "reason": "local_symlink"})
        elif not path.is_file():
            continue
        elif _local_state(rel):
            skipped.append({"source": rel, "reason": "local_sync_state"})
        elif _excluded(config, rel):
            skipped.append({"source": rel, "reason": "excluded_by_policy"})
        else:
            upload.append({"source": rel, "target": rel, "size": path.stat().st_size})
    return {"upload": upload, "skipped": skipped}


def remote_identity(config: dict[str, Any]) -> str:
    host, _ = parse_server_path(config["server"])
    return host


def remote_root(config: dict[str, Any]) -> str:
    _, root = parse_server_path(config["server"])
    return root


def list_remote_files(config: dict[str, Any]) -> list[dict[str, Any]]:
    root = remote_root(config)
    command = "find -- " + shlex.quote(root) + " -type f -printf '%P\\t%s\\t%TY-%Tm-%TdT%TH:%TM:%TS\\n'"
    result = subprocess.run(
        ["ssh", "--", remote_identity(config), command],
        check=True,
        text=True,
        capture_output=True,
    )
    files = []
    for line in result.stdout.splitlines():
        fields = line.split("\t", 2)
        if len(fields) != 3:
            raise ValueError("remote listing returned a malformed entry")
        path, size, mtime = fields
        try:
            parsed_size = int(size)
        except ValueError as exc:
            raise ValueError("remote listing returned a malformed size") from exc
        files.append({"path": path, "size": parsed_size, "mtime": mtime})
    return files


def render_plan(config: dict[str, Any], plan: dict[str, list[dict[str, Any]]]) -> str:
    lines = [f"Server: {config['server']}", f"Local: {config['local']}", "", "Will download:"]
    lines.extend(f"  {item['source']} -> {item['target']} ({item['size']} bytes)" for item in plan["download"])
    lines.extend(["", "Review needed:"])
    lines.extend(f"  {item['source']} ({item['reason']}, {item['size']} bytes)" for item in plan["review_needed"])
    lines.extend(["", "Skipped:"])
    lines.extend(f"  {item['source']} ({item['reason']}, {item['size']} bytes)" for item in plan["skipped"])
    return "\n".join(lines) + "\n"


def render_push_plan(config: dict[str, Any], plan: dict[str, list[dict[str, Any]]]) -> str:
    lines = [f"Local: {config['local']}", f"Server: {config['server']}", "", "Will upload:"]
    lines.extend(f"  {item['source']} -> {item['target']} ({item['size']} bytes)" for item in plan["upload"])
    lines.extend(["", "Skipped:"])
    lines.extend(f"  {item['source']} ({item['reason']})" for item in plan["skipped"])
    return "\n".join(lines) + "\n"


def _task_root(config: dict[str, Any]) -> Path:
    return Path.cwd() / config["local"]


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


def reviewed_plan_path(task_root: Path) -> Path:
    return task_root / REVIEWED_PLAN_DIRECTORY / REVIEWED_PLAN_FILENAME


def _fingerprint(value: Any) -> str:
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _config_fingerprint(config: dict[str, Any]) -> str:
    return _fingerprint(config)


def _plan_fingerprint(plan: dict[str, list[dict[str, Any]]]) -> str:
    return _fingerprint(plan)


def _plan_keys(direction: str) -> set[str]:
    if direction == "push":
        return {"upload", "skipped"}
    if direction == "pull":
        return {"download", "review_needed", "skipped"}
    raise ValueError("reviewed plan direction must be push or pull")


def _validate_plan(direction: str, plan: Any) -> dict[str, list[dict[str, Any]]]:
    required = _plan_keys(direction)
    if not isinstance(plan, dict) or set(plan) != required or any(not isinstance(plan[key], list) for key in required):
        raise ValueError("reviewed plan has an invalid file list")
    transfer_key = "upload" if direction == "push" else "download"
    seen = set()
    for item in plan[transfer_key]:
        if not isinstance(item, dict):
            raise ValueError("reviewed plan has an invalid transfer item")
        source, target, size = item.get("source"), item.get("target"), item.get("size")
        if (
            not isinstance(source, str)
            or not _is_relative_safe(source)
            or target != source
            or isinstance(size, bool)
            or not isinstance(size, int)
            or size < 0
            or source in seen
        ):
            raise ValueError("reviewed plan has an unsafe transfer item")
        seen.add(source)
    return plan


def _finite_time(value: Any) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value) and value >= 0


def write_reviewed_plan(
    config: dict[str, Any],
    direction: str,
    plan: dict[str, list[dict[str, Any]]],
    task_root: Path,
    now: float | None = None,
) -> Path:
    """Save one short-lived, exact-list review artifact."""
    plan = _validate_plan(direction, plan)
    created_at = time.time() if now is None else now
    if not _finite_time(created_at):
        raise ValueError("reviewed plan timestamp must be finite")
    artifact = reviewed_plan_path(task_root)
    if (
        task_root.is_symlink()
        or not task_root.is_dir()
        or artifact.parent.is_symlink()
        or artifact.is_symlink()
    ):
        raise ValueError("reviewed plan path must stay in a non-symlink task root")
    artifact.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": REVIEWED_PLAN_SCHEMA_VERSION,
        "direction": direction,
        "created_at": created_at,
        "configuration": {key: config[key] for key in sorted(CONFIG_KEYS)},
        "config_fingerprint": _config_fingerprint(config),
        "plan": plan,
        "plan_fingerprint": _plan_fingerprint(plan),
    }
    artifact.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return artifact


def load_reviewed_plan(
    config: dict[str, Any],
    direction: str,
    task_root: Path,
    now: float | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """Load a valid reviewed plan without listing or rebuilding its files."""
    artifact = reviewed_plan_path(task_root)
    if task_root.is_symlink() or artifact.parent.is_symlink() or artifact.is_symlink():
        raise ValueError("reviewed plan path must stay in a non-symlink task root")
    if not artifact.is_file():
        raise ValueError("reviewed plan is missing; run plan and review it before transfer")
    try:
        payload = json.loads(artifact.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("reviewed plan is unreadable; run plan again") from exc
    if not isinstance(payload, dict) or payload.get("schema_version") != REVIEWED_PLAN_SCHEMA_VERSION:
        raise ValueError("reviewed plan is invalid; run plan again")
    if payload.get("direction") != direction:
        raise ValueError("reviewed plan direction does not match this command; run plan again")
    configuration = {key: config[key] for key in sorted(CONFIG_KEYS)}
    if payload.get("configuration") != configuration or payload.get("config_fingerprint") != _config_fingerprint(config):
        raise ValueError("reviewed plan configuration changed; run plan again")
    created_at = payload.get("created_at")
    current_time = time.time() if now is None else now
    if not _finite_time(created_at) or not _finite_time(current_time) or created_at > current_time:
        raise ValueError("reviewed plan timestamp is invalid; run plan again")
    if current_time - created_at > REVIEWED_PLAN_TTL_SECONDS:
        raise ValueError("reviewed plan expired; run plan again")
    plan = _validate_plan(direction, payload.get("plan"))
    if payload.get("plan_fingerprint") != _plan_fingerprint(plan):
        raise ValueError("reviewed plan file list changed; run plan again")
    return plan


def _write_rsync_file_list(path: Path, items: list[dict[str, Any]]) -> None:
    path.write_bytes(b"".join(item["source"].encode("utf-8") + b"\n" for item in items))


def _is_run_input(relative: str) -> bool:
    parts = PurePosixPath(relative).parts
    return len(parts) >= 3 and parts[0].startswith("RUN-") and parts[1] == "inputs"


def _local_transfer_path(task_root: Path, relative: str, source: bool) -> Path:
    path = task_root / PurePosixPath(relative)
    if task_root.is_symlink() or _symlink_component(path, task_root):
        raise ValueError(f"unsafe local symlink path: {relative}")
    if source and (not path.is_file() or path.is_symlink()):
        raise ValueError(f"approved local source is no longer a regular file: {relative}")
    if not source and path.exists() and not path.is_file():
        raise ValueError(f"local destination has an unsafe type: {relative}")
    return path


def _remote_probe_command(root: str, relative: str) -> str:
    full = PurePosixPath(root) / PurePosixPath(relative)
    current = PurePosixPath("/")
    prefixes = []
    for part in full.parts[1:]:
        current /= part
        prefixes.append(str(current))
    link_test = " || ".join(f"[ -L {shlex.quote(prefix)} ]" for prefix in prefixes)
    quoted = shlex.quote(str(full))
    return (
        f"if {link_test}; then printf 'SYMLINK\\n'; "
        f"elif [ ! -e {quoted} ]; then printf 'MISSING\\n'; "
        f"elif [ ! -f {quoted} ]; then printf 'OTHER\\n'; "
        f"else size=$(wc -c < {quoted}); digest=$(sha256sum -- {quoted}); "
        "digest=${digest%% *}; printf 'REGULAR\\t%s\\t%s\\n' \"$size\" \"$digest\"; fi"
    )


def _probe_remote(config: dict[str, Any], relative: str) -> tuple[str, int | None, str | None]:
    result = subprocess.run(
        ["ssh", "--", remote_identity(config), _remote_probe_command(remote_root(config), relative)],
        check=True,
        text=True,
        capture_output=True,
    )
    line = result.stdout.strip()
    if line in {"MISSING", "SYMLINK", "OTHER"}:
        return line, None, None
    fields = line.split("\t")
    if len(fields) != 3 or fields[0] != "REGULAR" or not fields[1].isdigit() or not re.fullmatch(r"[0-9a-f]{64}", fields[2]):
        raise ValueError("remote safety probe returned malformed evidence")
    return "REGULAR", int(fields[1]), fields[2]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_transfer_entries(config: dict[str, Any], direction: str, plan: dict[str, list[dict[str, Any]]], task_root: Path) -> list[dict[str, Any]]:
    plan = _validate_plan(direction, plan)
    key = "upload" if direction == "push" else "download"
    items = plan[key]
    for item in items:
        relative = item["source"]
        if _local_state(relative) or _excluded(config, relative):
            raise ValueError(f"reviewed plan contains a protected or excluded file: {relative}")
        local_path = _local_transfer_path(task_root, relative, source=direction == "push")
        if direction == "push" and local_path.stat().st_size != item["size"]:
            raise ValueError(f"approved local source size changed: {relative}")

        kind, remote_size, remote_digest = _probe_remote(config, relative)
        if kind in {"SYMLINK", "OTHER"}:
            raise ValueError(f"unsafe remote path or type: {relative}")
        if direction == "pull" and (kind != "REGULAR" or remote_size != item["size"]):
            raise ValueError(f"approved remote source changed or disappeared: {relative}")
        if _is_run_input(relative):
            destination_exists = kind == "REGULAR" if direction == "push" else local_path.exists()
            if destination_exists:
                local_size = local_path.stat().st_size
                local_digest = _sha256(local_path)
                if remote_size != local_size or remote_digest != local_digest:
                    raise ValueError(f"refusing to replace differing immutable Run input: {relative}")
    return items


def sync_downloads(config: dict[str, Any], plan: dict[str, list[dict[str, Any]]], task_root: Path) -> None:
    downloads = _validate_transfer_entries(config, "pull", plan, task_root)
    if not downloads:
        return
    with tempfile.TemporaryDirectory(prefix="calc-sync-") as temporary:
        file_list = Path(temporary) / "files-from.txt"
        _write_rsync_file_list(file_list, downloads)
        subprocess.run(
            ["rsync", "-a", "--files-from", str(file_list), "--", f"{remote_identity(config)}:{remote_root(config)}/", str(task_root)],
            check=True,
        )


def sync_uploads(config: dict[str, Any], plan: dict[str, list[dict[str, Any]]], task_root: Path) -> None:
    uploads = _validate_transfer_entries(config, "push", plan, task_root)
    if not uploads:
        return
    with tempfile.TemporaryDirectory(prefix="calc-sync-") as temporary:
        file_list = Path(temporary) / "files-from.txt"
        _write_rsync_file_list(file_list, uploads)
        subprocess.run(
            ["rsync", "-a", "--files-from", str(file_list), "--", f"{task_root}/", f"{remote_identity(config)}:{remote_root(config)}/"],
            check=True,
        )


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
    config = _validated_config(Path(args.config))
    task_root = _task_root(config)
    if args.direction == "push":
        plan = build_push_plan(config, task_root)
        rendered = render_push_plan(config, plan)
    else:
        plan = build_pull_plan(config, list_remote_files(config))
        rendered = render_plan(config, plan)
    artifact = write_reviewed_plan(config, args.direction, plan, task_root)
    print(rendered, end="")
    print(f"Reviewed plan saved to {artifact}; it expires in {REVIEWED_PLAN_TTL_SECONDS // 60} minutes.")
    return 0


def _cmd_transfer(args: argparse.Namespace, direction: str) -> int:
    config = _validated_config(Path(args.config))
    if not args.yes:
        print(f"Refusing to {direction} without --yes; review a fresh {direction} plan first.", file=sys.stderr)
        return 2
    task_root = _task_root(config)
    try:
        plan = load_reviewed_plan(config, direction, task_root)
        if direction == "push":
            sync_uploads(config, plan, task_root)
        else:
            sync_downloads(config, plan, task_root)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


def cmd_push(args: argparse.Namespace) -> int:
    return _cmd_transfer(args, "push")


def cmd_pull(args: argparse.Namespace) -> int:
    return _cmd_transfer(args, "pull")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Synchronize reviewed calculation files using calc-sync.yaml.")
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("config")
    validate.set_defaults(func=cmd_validate)
    inspect = commands.add_parser("inspect")
    inspect.add_argument("config")
    inspect.set_defaults(func=cmd_inspect)
    plan = commands.add_parser("plan")
    plan.add_argument("config")
    plan.add_argument("--direction", choices=("pull", "push"), default="pull")
    plan.set_defaults(func=cmd_plan)
    push = commands.add_parser("push")
    push.add_argument("config")
    push.add_argument("--yes", action="store_true")
    push.set_defaults(func=cmd_push)
    pull = commands.add_parser("pull")
    pull.add_argument("config")
    pull.add_argument("--yes", action="store_true")
    pull.set_defaults(func=cmd_pull)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
