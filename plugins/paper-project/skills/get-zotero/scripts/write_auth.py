"""Codex authorization shared across skill invocations, outside project data."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import tempfile
from pathlib import Path

from runtime_config import config_path


def credential_file(server_id: str) -> Path:
    override = os.environ.get("GET_ZOTERO_AUTH_DIR")
    directory = (
        Path(override)
        if override
        else config_path(platform.system(), os.environ, Path.home()).parent
        / "write-auth"
    )
    # Server IDs are opaque: hash them instead of treating them as filenames.
    return directory / (hashlib.sha256(server_id.encode()).hexdigest() + ".json")


def load(server_id: str, endpoint: str) -> str | None:
    path = credential_file(server_id)
    try:
        if path.is_symlink() or (os.name != "nt" and path.stat().st_mode & 0o077):
            return None
        value = json.loads(path.read_text(encoding="utf-8"))
        if (
            value.get("app_name") == "Codex"
            and value.get("server_id") == server_id
            and value.get("endpoint") == endpoint
        ):
            return value.get("key")
    except (OSError, ValueError):
        pass
    return None


def save(server_id: str, endpoint: str, api_key: str) -> None:
    path = credential_file(server_id)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".auth-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(
                {
                    "app_name": "Codex",
                    "server_id": server_id,
                    "endpoint": endpoint,
                    "key": api_key,
                },
                stream,
            )
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def forget(server_id: str) -> None:
    credential_file(server_id).unlink(missing_ok=True)
