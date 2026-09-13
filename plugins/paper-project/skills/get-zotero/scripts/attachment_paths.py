#!/usr/bin/env python3
"""Resolve Zotero attachment locations without scanning local storage."""

from __future__ import annotations

import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import unquote, urlsplit

from runtime_config import PathMappingConfig


WINDOWS_DRIVE = re.compile(r"^/?([A-Za-z]):[\\/](.*)$")


class AttachmentPathError(ValueError):
    """Raised when a Zotero attachment cannot be resolved safely."""


@dataclass(frozen=True)
class ResolvedAttachment:
    path: Path
    strategy: str


def _decoded_local_path(raw: str) -> str:
    if "\x00" in raw:
        raise AttachmentPathError("Attachment path contains an invalid NUL byte")
    if WINDOWS_DRIVE.match(raw):
        decoded = unquote(raw)
    else:
        parsed = urlsplit(raw)
        if parsed.scheme and parsed.scheme.lower() != "file":
            raise AttachmentPathError("Attachment location is not a local file")
        if parsed.scheme.lower() == "file":
            decoded = unquote(parsed.path)
            if parsed.netloc and parsed.netloc.lower() != "localhost":
                decoded = f"//{parsed.netloc}{decoded}"
        else:
            decoded = unquote(raw)
    if "\x00" in decoded:
        raise AttachmentPathError("Attachment path contains an invalid NUL byte")

    windows = bool(WINDOWS_DRIVE.match(decoded)) or decoded.startswith(("\\\\", "//"))
    pure = PureWindowsPath(decoded) if windows else PurePosixPath(decoded)
    if ".." in pure.parts:
        raise AttachmentPathError("Attachment path must not contain parent traversal")
    if not windows and not pure.is_absolute():
        raise AttachmentPathError("Attachment path must be absolute")
    return decoded


def _windows_text(value: str) -> str:
    return value.replace("/", "\\").rstrip("\\")


def _mapping_suffix(path: str, prefix: str) -> str | None:
    normalized_path = _windows_text(path)
    normalized_prefix = _windows_text(prefix)
    folded_path = normalized_path.casefold()
    folded_prefix = normalized_prefix.casefold()
    if folded_path == folded_prefix:
        return ""
    boundary = folded_prefix + "\\"
    if not folded_path.startswith(boundary):
        return None
    return normalized_path[len(normalized_prefix) + 1 :]


def redact_attachment_path(raw: str) -> str:
    decoded = unquote(raw)
    windows = bool(WINDOWS_DRIVE.match(decoded)) or decoded.startswith(("\\\\", "//"))
    name = PureWindowsPath(decoded).name if windows else PurePosixPath(decoded).name
    kind = "Windows" if windows else "local"
    return f"{kind} attachment '{name or 'unknown'}'"


def _require_exists(
    path: Path,
    strategy: str,
    raw: str,
    exists: Callable[[Path], bool],
) -> ResolvedAttachment:
    if not exists(path):
        raise AttachmentPathError(f"Resolved {redact_attachment_path(raw)} does not exist")
    return ResolvedAttachment(path=path, strategy=strategy)


def resolve_attachment_path(
    raw_url: str,
    mode: str,
    mappings: Sequence[PathMappingConfig],
    exists: Callable[[Path], bool] = Path.exists,
) -> ResolvedAttachment:
    decoded = _decoded_local_path(raw_url)

    if mode != "wsl":
        return _require_exists(Path(decoded), "native", raw_url, exists)

    windows_path = _windows_text(decoded.lstrip("/") if WINDOWS_DRIVE.match(decoded) else decoded)
    for mapping in mappings:
        suffix = _mapping_suffix(windows_path, mapping.windows_prefix)
        if suffix is None:
            continue
        relative_parts = [part for part in suffix.split("\\") if part]
        target = Path(mapping.local_prefix).joinpath(*relative_parts)
        return _require_exists(target, "configured-mapping", raw_url, exists)

    if windows_path.startswith("\\\\"):
        raise AttachmentPathError(
            f"A configured mapping is required for network or UNC {redact_attachment_path(raw_url)}"
        )

    drive_match = WINDOWS_DRIVE.match(decoded)
    if drive_match:
        drive, suffix = drive_match.groups()
        target = Path("/mnt") / drive.lower()
        if suffix:
            target = target.joinpath(*[part for part in re.split(r"[\\/]", suffix) if part])
        return _require_exists(target, "wsl-drive", raw_url, exists)

    if decoded.startswith("/"):
        return _require_exists(Path(decoded), "native", raw_url, exists)
    raise AttachmentPathError(
        f"No WSL path rule matches {redact_attachment_path(raw_url)}"
    )
