"""Private path primitives shared by get-notes storage modules."""

from __future__ import annotations

import re
from pathlib import Path


class ProjectStoragePathError(ValueError):
    """Raised when a project, research line, or manuscript path is invalid."""


def sanitize_path_component(name: str) -> str:
    """Return a filesystem-safe component while preserving readable Unicode."""
    sanitized = re.sub(r'[\\/:*?"<>|]+', "_", name or "")
    sanitized = sanitized.strip(". ")
    return sanitized or "untitled"


def research_line_root(project_root: Path, research_line: str) -> Path:
    """Validate and return an existing research-line directory under a project."""
    if not project_root.is_dir():
        raise ProjectStoragePathError(
            f"Project root must already exist as a directory: {project_root}"
        )
    if not research_line or not research_line.strip():
        raise ProjectStoragePathError("Research line must not be blank")

    research_path = Path(research_line)
    if research_path == Path("."):
        raise ProjectStoragePathError("Research line must not target the project root")
    if research_path.is_absolute():
        raise ProjectStoragePathError("Research line must be a relative path")

    resolved_project_root = project_root.resolve()
    resolved_research_line = (resolved_project_root / research_path).resolve()
    try:
        resolved_research_line.relative_to(resolved_project_root)
    except ValueError as exc:
        raise ProjectStoragePathError(
            "Research line must not traverse outside the project root"
        ) from exc
    if not resolved_research_line.is_dir():
        raise ProjectStoragePathError(
            "Research line must already exist as a directory: "
            f"{resolved_research_line}"
        )
    return resolved_research_line
