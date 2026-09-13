#!/usr/bin/env python3
"""Project-local storage helpers for Zotero literature notes.

Only collections explicitly placed in ``selected_collections`` are eligible
for note placement.  An item receives one note path for each selected
collection it belongs to, allowing deliberately duplicated category notes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from _storage_support import (
    research_line_root,
    sanitize_path_component,
)

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "get-notes research-note storage requires PyYAML. Install it with: pip install pyyaml"
    ) from exc


MAP_FILE = "zotero-project-map.yaml"
MAP_VERSION = 1
LITERATURE_DIR = "06-文献笔记"
SINGLE_NOTE_DIR = "01-单篇文献"


class NoSelectedCollectionError(ValueError):
    """Raised when an item belongs to none of the project's selected collections."""


class InvalidCollectionMappingError(ValueError):
    """Raised when a persisted mapping does not mirror its Zotero path."""


def _safe_relative_path(path: str) -> Path:
    """Convert a mapped Zotero path into safe, non-traversing components."""
    raw_parts = path.replace("\\", "/").split("/")
    parts = [sanitize_path_component(part) for part in raw_parts if part.strip(". ")]
    if not parts:
        raise ValueError("A selected collection must have a non-empty project path")
    return Path(*parts)


def literature_root(project_root: Path, research_line: str) -> Path:
    """Return the project-local root for one existing research line's notes."""
    return research_line_root(project_root, research_line) / LITERATURE_DIR


def mapping_path(project_root: Path, research_line: str) -> Path:
    """Return the mapping file location for a research line."""
    return literature_root(project_root, research_line) / MAP_FILE


def load_mapping(project_root: Path, research_line: str) -> dict[str, Any]:
    """Load explicit collection mappings, without discovering Zotero collections."""
    path = mapping_path(project_root, research_line)
    if not path.exists():
        return {"version": MAP_VERSION, "selected_collections": []}
    with path.open("r", encoding="utf-8") as fh:
        mapping = yaml.safe_load(fh) or {}
    mapping.setdefault("version", MAP_VERSION)
    mapping.setdefault("selected_collections", [])
    return mapping


def save_mapping(project_root: Path, research_line: str, mapping: dict[str, Any]) -> None:
    """Persist the explicit project-relevant collection mapping."""
    path = mapping_path(project_root, research_line)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(mapping, fh, sort_keys=False, allow_unicode=True)


def find_selected_collection(
    mapping: dict[str, Any], collection_key: str
) -> dict[str, Any] | None:
    """Find an explicitly selected collection by Zotero collection key."""
    for entry in mapping.get("selected_collections", []):
        if entry.get("zotero_collection_key") == collection_key:
            return entry
    return None


def select_collection(
    mapping: dict[str, Any], collection_key: str, zotero_path: str
) -> None:
    """Add or update one user-selected Zotero collection and its mirrored path."""
    project_path = _safe_relative_path(zotero_path).as_posix()
    entry = find_selected_collection(mapping, collection_key)
    if entry is None:
        mapping.setdefault("selected_collections", []).append(
            {
                "zotero_collection_key": collection_key,
                "zotero_path": zotero_path,
                "project_path": project_path,
            }
        )
        return
    entry.update({"zotero_path": zotero_path, "project_path": project_path})


def resolve_note_paths(
    project_root: Path,
    research_line: str,
    item_key: str,
    item_collection_keys: Iterable[str],
) -> list[Path]:
    """Resolve note paths for the item's explicitly selected collection memberships.

    Paths follow the persisted selected-collection mapping order. Item memberships
    outside that mapping are ignored.
    """
    item_collection_key_set = set(item_collection_keys)
    mapping = load_mapping(project_root, research_line)
    selected_entries = [
        entry
        for entry in mapping.get("selected_collections", [])
        if entry.get("zotero_collection_key") in item_collection_key_set
    ]
    if not selected_entries:
        raise NoSelectedCollectionError(
            "The item belongs to no Zotero collection selected for this project"
        )

    note_paths: list[Path] = []
    for entry in selected_entries:
        collection_key = entry.get("zotero_collection_key")
        zotero_path = entry.get("zotero_path")
        if not isinstance(zotero_path, str):
            raise InvalidCollectionMappingError(
                f"Selected Zotero collection {collection_key!r} has no Zotero path"
            )
        canonical_path = _safe_relative_path(zotero_path)
        project_path = entry.get("project_path")
        if project_path is not None and (
            not isinstance(project_path, str)
            or _safe_relative_path(project_path) != canonical_path
        ):
            raise InvalidCollectionMappingError(
                f"Selected Zotero collection {collection_key!r} has a non-canonical project path"
            )

        notes_dir = literature_root(project_root, research_line) / SINGLE_NOTE_DIR / canonical_path
        notes_dir.mkdir(parents=True, exist_ok=True)
        note_paths.append(notes_dir / f"{sanitize_path_component(item_key)}.md")
    return note_paths
