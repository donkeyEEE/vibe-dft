#!/usr/bin/env python3
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


DEFAULT_EXCLUDE = ["*.h5", "*.hdf5", "*.hdf", "WAVECAR", "CHGCAR", "stdout", "stderr"]
HARD_EXCLUDE = ["*.h5", "*.hdf5", "*.hdf", "*.H5", "*.HDF5", "*.HDF"]
DEFAULT_LARGE_FILE_THRESHOLD_MB = 50
YAML_REQUIRED_ERROR = "PyYAML is required to read and write calc-task.yaml"
LOCAL_METADATA_FILES = {"calc-task.yaml"}
# Keep legacy metadata out of public docs/searches while still skipping it on upload.
LEGACY_SYNC_METADATA_BASENAME = "calc-" "sync.yaml"
LEGACY_METADATA_FILES = {LEGACY_SYNC_METADATA_BASENAME}
LOCAL_CACHE_PATTERNS = [
    "__pycache__/*",
    "*/__pycache__/*",
    ".pytest_cache/*",
    "*/.pytest_cache/*",
    "*.pyc",
    "*.pyo",
    ".DS_Store",
]
REVIEWED_PLAN_DIRECTORY = ".calc-sync"
REVIEWED_PLAN_FILENAME = "reviewed-plan.json"
REVIEWED_PLAN_SCHEMA_VERSION = 2
# A reviewed plan is intentionally short-lived: it is for one human review session.
REVIEWED_PLAN_TTL_SECONDS = 30 * 60
ALLOWED_STATUS = {
    "prepared",
    "pushed",
    "submitted_by_user",
    "running",
    "finished",
    "pulled",
    "archived",
}


def _relpath(path: Path, workspace: Path) -> str:
    return path.resolve().relative_to(workspace.resolve()).as_posix()


def build_draft_config(run_dir: Path, workspace: Path | None = None) -> dict[str, Any]:
    workspace = (workspace or Path.cwd()).resolve()
    run_dir = run_dir.resolve()
    parts = run_dir.relative_to(workspace).parts
    name = run_dir.name
    line = parts[-2] if len(parts) >= 2 else ""
    material = parts[-3] if len(parts) >= 3 else ""
    return {
        "schema_version": 1,
        "task": {
            "project": workspace.name,
            "material": material,
            "line": line,
            "name": name,
            "description": "",
        },
        "paths": {
            "local": _relpath(run_dir, workspace),
            "server": "",
        },
        "status": "prepared",
        "files": {"inputs": [], "outputs": []},
        "sync": {"exclude": DEFAULT_EXCLUDE},
    }


def _is_relative_safe(path: str) -> bool:
    pure = PurePosixPath(path)
    return not pure.is_absolute() and ".." not in pure.parts


def parse_server_path(value: str) -> tuple[str, str]:
    if ":" not in value:
        raise ValueError("paths.server must use host:/absolute/path")
    host, root = value.split(":", 1)
    host_pattern = r"(?:[A-Za-z0-9][A-Za-z0-9._-]*@)?[A-Za-z0-9][A-Za-z0-9._-]*"
    root_path = PurePosixPath(root)
    if (
        not re.fullmatch(host_pattern, host)
        or not root.startswith("/")
        or ".." in root_path.parts
        or any(ord(character) < 32 or character.isspace() for character in root)
    ):
        raise ValueError("paths.server must use host:/absolute/path")
    return host, root


def _status_error() -> str:
    return "status must be one of " + ", ".join(sorted(ALLOWED_STATUS))


def validate_config(config: dict[str, Any], workspace: Path | None = None) -> list[str]:
    workspace = (workspace or Path.cwd()).resolve()
    errors: list[str] = []
    if config.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    task = config.get("task")
    if not isinstance(task, dict):
        errors.append("task must be a mapping")
        task = {}
    for key in ("project", "material", "line", "name"):
        if not task.get(key):
            errors.append(f"task.{key} is required")

    paths = config.get("paths")
    if not isinstance(paths, dict):
        errors.append("paths must be a mapping")
        paths = {}

    local = paths.get("local")
    if not local:
        errors.append("paths.local is required")
    elif not _is_relative_safe(str(local)):
        errors.append("paths.local must stay inside the workspace")
    else:
        local_path = (workspace / str(local)).resolve()
        try:
            local_path.relative_to(workspace)
        except ValueError:
            errors.append("paths.local must stay inside the workspace")

    server = paths.get("server")
    if not server:
        errors.append("paths.server is required")
    else:
        try:
            parse_server_path(str(server))
        except ValueError as exc:
            errors.append(str(exc))

    status = config.get("status")
    if status not in ALLOWED_STATUS:
        errors.append(_status_error())

    files = config.get("files")
    if not isinstance(files, dict):
        errors.append("files must be a mapping")
        files = {}
    for key in ("inputs", "outputs"):
        if key not in files:
            errors.append(f"files.{key} is required")
        elif not isinstance(files[key], list):
            errors.append(f"files.{key} must be a list")

    sync = config.get("sync")
    if not isinstance(sync, dict):
        errors.append("sync must be a mapping")
        sync = {}
    exclude = sync.get("exclude")
    if not isinstance(exclude, list):
        errors.append("sync.exclude must be a list")

    return errors


def load_config(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError(YAML_REQUIRED_ERROR)
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError("config root must be a mapping")
    return data


def dump_config(config: dict[str, Any]) -> str:
    if yaml is None:
        raise RuntimeError(YAML_REQUIRED_ERROR)
    return yaml.safe_dump(config, allow_unicode=True, sort_keys=False)


def _matches(path: str, pattern: str) -> bool:
    return fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(PurePosixPath(path).name, pattern)


def _effective_exclude(config: dict[str, Any]) -> list[str]:
    sync = config.get("sync") if isinstance(config.get("sync"), dict) else {}
    configured = sync.get("exclude") if isinstance(sync.get("exclude"), list) else []
    return [str(pattern) for pattern in configured] + HARD_EXCLUDE


def build_pull_plan(config: dict[str, Any], remote_files: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    exclude = _effective_exclude(config)
    threshold = DEFAULT_LARGE_FILE_THRESHOLD_MB * 1024 * 1024
    plan: dict[str, list[dict[str, Any]]] = {"download": [], "review_needed": [], "skipped": []}

    for item in remote_files:
        path = str(item["path"])
        size = int(item.get("size", 0))
        if any(_matches(path, pattern) for pattern in exclude):
            plan["skipped"].append({"source": path, "reason": "excluded_by_policy", "size": size})
            continue
        if size > threshold:
            plan["review_needed"].append({"source": path, "reason": "large_file", "size": size})
            continue
        plan["download"].append({"source": path, "target": path, "size": size})
    return plan


def remote_identity(config: dict[str, Any]) -> str:
    host, _root = parse_server_path(str(config["paths"]["server"]))
    return host


def remote_root(config: dict[str, Any]) -> str:
    _host, root = parse_server_path(str(config["paths"]["server"]))
    return root


def list_remote_files(config: dict[str, Any]) -> list[dict[str, Any]]:
    root = remote_root(config)
    remote = remote_identity(config)
    script = "find " + shlex.quote(root) + " -type f -printf '%P\\t%s\\t%TY-%Tm-%TdT%TH:%TM:%TS\\n'"
    result = subprocess.run(
        ["ssh", remote, script],
        check=True,
        text=True,
        capture_output=True,
    )
    files = []
    for line in result.stdout.splitlines():
        path, size, mtime = line.split("\t", 2)
        files.append({"path": path, "size": int(size), "mtime": mtime})
    return files


def render_plan(config: dict[str, Any], plan: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        f"Server: {config['paths']['server']}",
        f"Local: {config['paths']['local']}",
        "",
        "Will download:",
    ]
    lines.extend(f"  {item['source']} -> {item['target']} ({item['size']} bytes)" for item in plan["download"])
    lines.append("")
    lines.append("Review needed:")
    lines.extend(f"  {item['source']} ({item['reason']}, {item['size']} bytes)" for item in plan["review_needed"])
    lines.append("")
    lines.append("Skipped:")
    lines.extend(f"  {item['source']} ({item['reason']}, {item['size']} bytes)" for item in plan["skipped"])
    return "\n".join(lines) + "\n"


def render_push_plan(config: dict[str, Any], plan: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        f"Local: {config['paths']['local']}",
        f"Server: {config['paths']['server']}",
        "",
        "Will upload:",
    ]
    lines.extend(f"  {item['source']} -> {item['target']} ({item['size']} bytes)" for item in plan["upload"])
    lines.append("")
    lines.append("Skipped:")
    lines.extend(f"  {item['source']} ({item['reason']})" for item in plan["skipped"])
    return "\n".join(lines) + "\n"


def _validated_config(path: Path) -> dict[str, Any]:
    config = load_config(path)
    errors = validate_config(config)
    if errors:
        raise SystemExit("\n".join(f"ERROR: {error}" for error in errors))
    return config


def _task_root(config: dict[str, Any]) -> Path:
    local_root = Path(config["paths"]["local"])
    return local_root if local_root.is_absolute() else Path.cwd() / local_root


def reviewed_plan_path(task_root: Path) -> Path:
    return task_root / REVIEWED_PLAN_DIRECTORY / REVIEWED_PLAN_FILENAME


def _config_fingerprint(config: dict[str, Any]) -> str:
    canonical = json.dumps(config, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _plan_fingerprint(plan: dict[str, list[dict[str, Any]]]) -> str:
    canonical = json.dumps(plan, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


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
    for item in plan[transfer_key]:
        if not isinstance(item, dict):
            raise ValueError("reviewed plan has an invalid transfer item")
        source = item.get("source")
        target = item.get("target")
        size = item.get("size")
        if (
            not isinstance(source, str)
            or not source
            or not _is_relative_safe(source)
            or any(ord(character) < 32 for character in source)
            or target != source
            or isinstance(size, bool)
            or not isinstance(size, int)
            or size < 0
        ):
            raise ValueError("reviewed plan has an unsafe transfer item")
    return plan


def write_reviewed_plan(
    config: dict[str, Any], direction: str, plan: dict[str, list[dict[str, Any]]], task_root: Path, now: float | None = None
) -> Path:
    """Persist exactly the reviewed file lists for one short-lived transfer session."""
    _validate_plan(direction, plan)
    artifact = reviewed_plan_path(task_root)
    artifact.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": REVIEWED_PLAN_SCHEMA_VERSION,
        "direction": direction,
        "created_at": time.time() if now is None else now,
        "config_fingerprint": _config_fingerprint(config),
        "paths": {"local": config["paths"]["local"], "server": config["paths"]["server"]},
        "plan": plan,
        "plan_fingerprint": _plan_fingerprint(plan),
    }
    artifact.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return artifact


def load_reviewed_plan(
    config: dict[str, Any], direction: str, task_root: Path, now: float | None = None
) -> dict[str, list[dict[str, Any]]]:
    """Load a still-valid reviewed plan without inspecting or rebuilding its file list."""
    artifact = reviewed_plan_path(task_root)
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
    expected_paths = {"local": config["paths"]["local"], "server": config["paths"]["server"]}
    if payload.get("config_fingerprint") != _config_fingerprint(config) or payload.get("paths") != expected_paths:
        raise ValueError("reviewed plan configuration changed; run plan again")
    created_at = payload.get("created_at")
    current_time = time.time() if now is None else now
    if isinstance(created_at, bool) or not isinstance(created_at, (int, float)) or not math.isfinite(created_at) or created_at > current_time:
        raise ValueError("reviewed plan timestamp is invalid; run plan again")
    if current_time - created_at > REVIEWED_PLAN_TTL_SECONDS:
        raise ValueError("reviewed plan expired; run plan again")
    plan = _validate_plan(direction, payload.get("plan"))
    if payload.get("plan_fingerprint") != _plan_fingerprint(plan):
        raise ValueError("reviewed plan file list changed; run plan again")
    return plan


def _write_rsync_file_list(path: Path, items: list[dict[str, Any]]) -> None:
    lines = [str(item["source"]) for item in items]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def sync_downloads(config: dict[str, Any], plan: dict[str, list[dict[str, Any]]], task_root: Path) -> None:
    downloads = plan["download"]
    if not downloads:
        return

    remote = remote_identity(config)
    server_root = remote_root(config).rstrip("/") + "/"
    with tempfile.TemporaryDirectory(prefix="calc-sync-") as tmp:
        file_list = Path(tmp) / "files-from.txt"
        _write_rsync_file_list(file_list, downloads)
        subprocess.run(
            ["rsync", "-a", "--files-from", str(file_list), f"{remote}:{server_root}", str(task_root)],
            check=True,
        )


def build_push_plan(config: dict[str, Any], task_root: Path) -> dict[str, list[dict[str, Any]]]:
    exclude = _effective_exclude(config)
    upload: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for path in sorted(task_root.rglob("*")):
        rel = path.relative_to(task_root).as_posix()
        if path.is_symlink():
            skipped.append({"source": rel, "reason": "local_symlink"})
            continue
        if not path.is_file():
            continue
        if rel in LOCAL_METADATA_FILES:
            skipped.append({"source": rel, "reason": "local_metadata"})
            continue
        if rel in LEGACY_METADATA_FILES:
            skipped.append({"source": rel, "reason": "legacy_metadata"})
            continue
        if rel.startswith(REVIEWED_PLAN_DIRECTORY + "/") or any(_matches(rel, pattern) for pattern in LOCAL_CACHE_PATTERNS):
            skipped.append({"source": rel, "reason": "local_cache"})
            continue
        if any(_matches(rel, pattern) for pattern in exclude):
            skipped.append({"source": rel, "reason": "excluded_by_policy"})
            continue
        upload.append({"source": rel, "target": rel, "size": path.stat().st_size})
    return {"upload": upload, "skipped": skipped}


def sync_uploads(config: dict[str, Any], plan: dict[str, list[dict[str, Any]]], task_root: Path) -> None:
    uploads = plan["upload"]
    if not uploads:
        return

    remote = remote_identity(config)
    server_root = remote_root(config).rstrip("/") + "/"
    with tempfile.TemporaryDirectory(prefix="calc-sync-") as tmp:
        file_list = Path(tmp) / "files-from.txt"
        _write_rsync_file_list(file_list, uploads)
        subprocess.run(["rsync", "-a", "--files-from", str(file_list), f"{task_root}/", f"{remote}:{server_root}"], check=True)


def cmd_init(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    out = run_dir / "calc-task.yaml"
    if out.is_symlink():
        print(f"{out} is a symlink; refusing to overwrite", file=sys.stderr)
        return 2
    if out.exists() and not args.force:
        print(f"{out} already exists; use --force to overwrite", file=sys.stderr)
        return 2
    config = build_draft_config(run_dir)
    out.write_text(dump_config(config), encoding="utf-8")
    print(f"wrote {out}")
    print("fill paths.server before remote operations")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    config = load_config(Path(args.config))
    errors = validate_config(config)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("valid")
    return 0


def cmd_inspect(args: argparse.Namespace) -> int:
    config = _validated_config(Path(args.config))
    files = list_remote_files(config)
    for item in files:
        print(f"{item['path']}\t{item['size']}\t{item.get('mtime', '')}")
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    config = _validated_config(Path(args.config))
    task_root = _task_root(config)
    if args.direction == "push":
        plan = build_push_plan(config, task_root)
        rendered = render_push_plan(config, plan)
    else:
        files = list_remote_files(config)
        plan = build_pull_plan(config, files)
        rendered = render_plan(config, plan)
    artifact = write_reviewed_plan(config, args.direction, plan, task_root)
    print(rendered, end="")
    print(f"Reviewed plan saved to {artifact}; it expires in {REVIEWED_PLAN_TTL_SECONDS // 60} minutes.")
    return 0


def cmd_push(args: argparse.Namespace) -> int:
    config = _validated_config(Path(args.config))
    task_root = _task_root(config)
    if not args.yes:
        print("Refusing to upload without --yes; run plan --direction push, review it, then confirm.", file=sys.stderr)
        return 2
    try:
        plan = load_reviewed_plan(config, "push", task_root)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    sync_uploads(config, plan, task_root)
    return 0


def cmd_pull(args: argparse.Namespace) -> int:
    config = _validated_config(Path(args.config))
    if not args.yes:
        print("Refusing to download without --yes; run plan, review it, then confirm.", file=sys.stderr)
        return 2
    task_root = _task_root(config)
    try:
        plan = load_reviewed_plan(config, "pull", task_root)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    sync_downloads(config, plan, task_root)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Synchronize calculation task files using calc-task.yaml.")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("run_dir")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=cmd_init)
    validate = sub.add_parser("validate")
    validate.add_argument("config")
    validate.set_defaults(func=cmd_validate)
    inspect = sub.add_parser("inspect")
    inspect.add_argument("config")
    inspect.set_defaults(func=cmd_inspect)
    plan = sub.add_parser("plan")
    plan.add_argument("config")
    plan.add_argument("--direction", choices=("pull", "push"), default="pull", help="transfer direction to review (default: pull)")
    plan.set_defaults(func=cmd_plan)
    push = sub.add_parser("push")
    push.add_argument("config")
    push.add_argument("--yes", action="store_true", help="confirm the displayed plan and upload approved files")
    push.set_defaults(func=cmd_push)
    pull = sub.add_parser("pull")
    pull.add_argument("config")
    pull.add_argument("--yes", action="store_true", help="confirm the displayed plan and download approved files")
    pull.set_defaults(func=cmd_pull)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
