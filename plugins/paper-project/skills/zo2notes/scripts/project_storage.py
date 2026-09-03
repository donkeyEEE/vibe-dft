#!/usr/bin/env python3
"""Project-local storage helpers for Zotero literature notes.

Only collections explicitly placed in ``selected_collections`` are eligible
for note placement.  An item receives one note path for each selected
collection it belongs to, allowing deliberately duplicated category notes.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "Zo2Notes project_storage requires PyYAML. Install it with: pip install pyyaml"
    ) from exc


MAP_FILE = "zotero-project-map.yaml"
MAP_VERSION = 1
LITERATURE_DIR = "06-文献笔记"
SINGLE_NOTE_DIR = "01-单篇文献"
WRITING_LIBRARY_DIR = "07-论文写作库"
STANDALONE_WRITING_LIBRARY_DIR = "论文写作库"
MATERIALS_DIR = "素材库"
MATERIAL_ITEMS_DIR = "文献片段"
STYLE_DIR = "风格笔记"
DRAFTS_DIR = "草稿"
WRITING_PROJECT_FILE = "writing-project.yaml"
MATERIAL_STATE_FILE = "zotero-library.yaml"
MATERIAL_INDEX_FILE = "文献索引.md"
EMPTY_STYLE_NOTE = """# 写作风格笔记

## 已确认习惯

## 已废止或替换的习惯

## 术语与表达选择

## 变更记录
"""


class NoSelectedCollectionError(ValueError):
    """Raised when an item belongs to none of the project's selected collections."""


class InvalidCollectionMappingError(ValueError):
    """Raised when a persisted mapping does not mirror its Zotero path."""


class ProjectStoragePathError(ValueError):
    """Raised when the project root or research line is not a valid directory."""


def sanitize_path_component(name: str) -> str:
    """Return a filesystem-safe component while preserving readable Unicode."""
    sanitized = re.sub(r'[\\/:*?"<>|]+', "_", name or "")
    sanitized = sanitized.strip(". ")
    return sanitized or "untitled"


def _safe_relative_path(path: str) -> Path:
    """Convert a mapped Zotero path into safe, non-traversing components."""
    raw_parts = path.replace("\\", "/").split("/")
    parts = [sanitize_path_component(part) for part in raw_parts if part.strip(". ")]
    if not parts:
        raise ValueError("A selected collection must have a non-empty project path")
    return Path(*parts)


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


def literature_root(project_root: Path, research_line: str) -> Path:
    """Return the project-local root for one existing research line's notes."""
    return research_line_root(project_root, research_line) / LITERATURE_DIR


def writing_library_for_research_line(project_root: Path, research_line: str) -> Path:
    """Return the managed writing-library path for an existing research line."""
    return research_line_root(project_root, research_line) / WRITING_LIBRARY_DIR


def writing_library_for_manuscript(manuscript: Path) -> Path:
    """Return the standalone writing-library path beside an existing manuscript."""
    manuscript = manuscript.resolve()
    if not manuscript.is_file():
        raise ProjectStoragePathError(
            f"Manuscript must already exist as a file: {manuscript}"
        )
    return manuscript.parent / STANDALONE_WRITING_LIBRARY_DIR


def _atomic_yaml(path: Path, value: dict[str, Any]) -> None:
    """Write YAML through a sibling temporary file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        yaml.safe_dump(value, stream, sort_keys=False, allow_unicode=True)
    temporary.replace(path)


def initialize_writing_library(
    root: Path,
    *,
    mode: str,
    source_manuscript: Path,
    collection_key: str,
    collection_path: str,
) -> dict[str, Any]:
    """Create one non-overwriting managed writing workspace."""
    source_manuscript = source_manuscript.resolve()
    if not source_manuscript.is_file():
        raise ProjectStoragePathError(
            f"Manuscript must already exist as a file: {source_manuscript}"
        )
    if mode not in {"standalone", "research-line"}:
        raise ProjectStoragePathError(f"Unsupported writing-library mode: {mode}")
    if not collection_key.strip() or not collection_path.strip():
        raise ValueError("A confirmed Zotero collection key and path are required")

    root = root.resolve()
    if mode == "standalone":
        expected_root = writing_library_for_manuscript(source_manuscript)
        if root != expected_root:
            raise ProjectStoragePathError(
                f"Standalone writing library must be beside the manuscript: {expected_root}"
            )
    elif root.name != WRITING_LIBRARY_DIR or not root.parent.is_dir():
        raise ProjectStoragePathError(
            "Research-line writing library must be named 07-论文写作库 under an existing directory"
        )

    state_path = root / WRITING_PROJECT_FILE
    managed_original = root / DRAFTS_DIR / "00-原稿" / source_manuscript.name
    working_draft = root / DRAFTS_DIR / "01-工作稿" / source_manuscript.name
    if state_path.exists() or managed_original.exists() or working_draft.exists():
        raise FileExistsError(f"Writing library is already initialized: {root}")

    for directory in (
        root / MATERIALS_DIR / MATERIAL_ITEMS_DIR,
        root / STYLE_DIR,
        root / DRAFTS_DIR / "00-原稿",
        root / DRAFTS_DIR / "01-工作稿",
        root / DRAFTS_DIR / "02-已确认版本",
    ):
        directory.mkdir(parents=True, exist_ok=True)

    shutil.copy2(source_manuscript, managed_original)
    shutil.copy2(source_manuscript, working_draft)
    (root / STYLE_DIR / "writing-style.md").write_text(
        EMPTY_STYLE_NOTE, encoding="utf-8"
    )
    (root / MATERIALS_DIR / MATERIAL_INDEX_FILE).write_text(
        "# 文献索引\n", encoding="utf-8"
    )

    selected_collection = {"key": collection_key, "path": collection_path}
    state = {
        "version": 1,
        "mode": mode,
        "source_manuscript": str(source_manuscript),
        "managed_original": managed_original.relative_to(root).as_posix(),
        "current_working_draft": working_draft.relative_to(root).as_posix(),
        "selected_collection": selected_collection,
        "workflow_state": "materials_pending",
    }
    material_state = {
        "version": 1,
        "selected_collection": selected_collection,
        "items": [],
    }
    _atomic_yaml(root / MATERIALS_DIR / MATERIAL_STATE_FILE, material_state)
    _atomic_yaml(state_path, state)
    return state


def _validated_writing_root(root: Path) -> Path:
    """Return an initialized writing root without allowing path indirection."""
    root = root.resolve()
    if not (root / WRITING_PROJECT_FILE).is_file():
        raise ProjectStoragePathError(f"Not an initialized writing library: {root}")
    if root.name not in {WRITING_LIBRARY_DIR, STANDALONE_WRITING_LIBRARY_DIR}:
        raise ProjectStoragePathError(f"Unexpected writing-library directory: {root}")
    return root


def load_material_state(root: Path) -> dict[str, Any]:
    """Load the resumable Zotero material-library state."""
    root = _validated_writing_root(root)
    path = root / MATERIALS_DIR / MATERIAL_STATE_FILE
    with path.open("r", encoding="utf-8") as stream:
        state = yaml.safe_load(stream) or {}
    state.setdefault("version", 1)
    state.setdefault("items", [])
    return state


def _save_material_state(root: Path, state: dict[str, Any]) -> None:
    _atomic_yaml(root / MATERIALS_DIR / MATERIAL_STATE_FILE, state)
    _write_material_index(root, state)


def _write_material_index(root: Path, state: dict[str, Any]) -> None:
    lines = ["# 文献索引", ""]
    for item in state.get("items", []):
        title = str(item.get("title") or item.get("item_key") or "Untitled")
        output_path = item.get("output_path")
        status = item.get("status", "pending")
        if output_path:
            relative = Path(output_path).relative_to(MATERIALS_DIR).as_posix()
            lines.append(f"- [{title}]({relative}) — `{status}`")
        else:
            lines.append(f"- {title} — `{status}`")
    (root / MATERIALS_DIR / MATERIAL_INDEX_FILE).write_text(
        "\n".join(lines).rstrip() + "\n", encoding="utf-8"
    )


def register_material_items(
    root: Path, items: Iterable[dict[str, Any]]
) -> dict[str, Any]:
    """Register collection items while preserving completed unchanged entries."""
    root = _validated_writing_root(root)
    state = load_material_state(root)
    existing = {item.get("item_key"): item for item in state.get("items", [])}
    ordered_keys = [item.get("item_key") for item in state.get("items", [])]
    for metadata in items:
        item_key = str(metadata.get("item_key") or "").strip()
        if not item_key:
            raise ValueError("Every Zotero material item requires an item_key")
        current = existing.get(item_key)
        if current is None:
            current = dict(metadata)
            current["item_key"] = item_key
            current["status"] = "pending"
            existing[item_key] = current
            ordered_keys.append(item_key)
            continue
        old_version = current.get("version")
        current.update(metadata)
        if old_version != metadata.get("version") and current.get("status") in {
            "indexed",
            "abstract_only",
        }:
            current["status"] = "pending"
    state["items"] = [existing[key] for key in ordered_keys]
    _save_material_state(root, state)
    return state


def _valid_material_tags(tags: Any) -> bool:
    return (
        isinstance(tags, list)
        and 1 <= len(tags) <= 3
        and all(
            isinstance(tag, str)
            and tag.strip() == tag
            and tag
            and not tag.startswith("#")
            and not any(character.isspace() for character in tag)
            for tag in tags
        )
    )


def write_material_item(
    root: Path,
    *,
    metadata: dict[str, Any],
    paragraphs: list[dict[str, Any]],
    evidence_source: str,
    indexed_at: str,
    reindex: bool = False,
) -> Path:
    """Write one source-faithful tagged literature item and update its state."""
    root = _validated_writing_root(root)
    item_key = str(metadata.get("item_key") or "").strip()
    if not item_key:
        raise ValueError("Material metadata requires item_key")
    if evidence_source != "abstract-only" and not paragraphs:
        raise ValueError("Indexed material requires at least one tagged paragraph")
    for paragraph in paragraphs:
        if not _valid_material_tags(paragraph.get("tags")):
            raise ValueError("Each material paragraph requires one to three valid tags")
        if not isinstance(paragraph.get("text"), str) or not paragraph["text"]:
            raise ValueError("Each material paragraph requires source text")

    output = root / MATERIALS_DIR / MATERIAL_ITEMS_DIR / (
        sanitize_path_component(item_key) + ".md"
    )
    if output.exists() and not reindex:
        raise FileExistsError(f"Material item already exists: {output}")

    frontmatter = dict(metadata)
    frontmatter.update(
        {
            "item_key": item_key,
            "zotero_collection_key": load_material_state(root)
            .get("selected_collection", {})
            .get("key"),
            "indexed_at": indexed_at,
            "evidence_source": evidence_source,
        }
    )
    yaml_text = yaml.safe_dump(
        frontmatter, sort_keys=False, allow_unicode=True
    ).rstrip()
    sections = ["---", yaml_text, "---", ""]
    if evidence_source == "abstract-only":
        sections.extend(
            [
                "# 仅摘要材料",
                "",
                str(metadata.get("abstract") or ""),
                "",
                "无可用全文：仅记录元数据与摘要，未据此推断正文结论。",
            ]
        )
        status = "abstract_only"
    else:
        for paragraph in paragraphs:
            tag_line = " ".join(f"#{tag}" for tag in paragraph["tags"])
            sections.extend(
                [
                    tag_line,
                    paragraph["text"],
                    "",
                    f"来源位置：{paragraph.get('source_location') or '未知'}",
                    "",
                ]
            )
        status = "indexed"
    temporary = output.with_suffix(".md.tmp")
    temporary.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")
    temporary.replace(output)

    state = load_material_state(root)
    entry = next(
        (item for item in state["items"] if item.get("item_key") == item_key), None
    )
    if entry is None:
        entry = {"item_key": item_key}
        state["items"].append(entry)
    entry.update(metadata)
    entry.update(
        {
            "item_key": item_key,
            "status": status,
            "output_path": output.relative_to(root).as_posix(),
            "evidence_source": evidence_source,
            "indexed_at": indexed_at,
        }
    )
    _save_material_state(root, state)
    return output


def mark_material_failed(
    root: Path, item_key: str, error: str, attempted_at: str
) -> None:
    """Record an item failure without removing any older item file."""
    root = _validated_writing_root(root)
    state = load_material_state(root)
    entry = next(
        (item for item in state["items"] if item.get("item_key") == item_key), None
    )
    if entry is None:
        entry = {"item_key": item_key, "title": item_key}
        state["items"].append(entry)
    entry.update({"status": "failed", "error": error, "attempted_at": attempted_at})
    _save_material_state(root, state)


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
