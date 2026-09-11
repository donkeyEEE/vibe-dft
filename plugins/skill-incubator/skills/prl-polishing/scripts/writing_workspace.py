#!/usr/bin/env python3
"""Deterministic storage helpers for managed manuscript revision workspaces."""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise ImportError("writing_workspace requires PyYAML") from exc


PROJECT_FILE = "writing-project.yaml"
STYLE_FILE = Path("风格笔记/writing-style.md")
MATERIAL_DIR = Path("素材库/文献片段")
TAG_LINE = re.compile(r"^(#[^\s#]+)(\s+#[^\s#]+){0,2}$")
YAML_RECORD = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)


class WritingWorkspaceError(ValueError):
    """Raised when a managed writing workspace is unsafe or malformed."""


def _root(path: Path) -> Path:
    resolved = path.resolve()
    if resolved.name not in {"论文写作库", "07-论文写作库"}:
        raise WritingWorkspaceError(f"Unexpected writing workspace: {resolved}")
    if not (resolved / PROJECT_FILE).is_file():
        raise WritingWorkspaceError(f"Missing {PROJECT_FILE}: {resolved}")
    return resolved


def load_project(root: Path) -> dict[str, Any]:
    """Load the writing-project state."""
    with (_root(root) / PROJECT_FILE).open("r", encoding="utf-8") as stream:
        return yaml.safe_load(stream) or {}


def _frontmatter_and_body(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        return {}, text
    return yaml.safe_load(parts[1]) or {}, parts[2].lstrip("\n")


def _material_fragments(path: Path) -> list[dict[str, str]]:
    metadata, body = _frontmatter_and_body(path.read_text(encoding="utf-8"))
    lines = body.splitlines()
    fragments: list[dict[str, str]] = []
    index = 0
    while index < len(lines):
        if not TAG_LINE.fullmatch(lines[index]):
            index += 1
            continue
        tags = [token[1:] for token in lines[index].split()]
        index += 1
        content: list[str] = []
        location = "未知"
        while index < len(lines) and not TAG_LINE.fullmatch(lines[index]):
            line = lines[index]
            if line.startswith("来源位置："):
                location = line.removeprefix("来源位置：").strip() or "未知"
            elif line.strip():
                content.append(line)
            index += 1
        if content:
            fragments.append(
                {
                    "item_key": str(metadata.get("item_key") or path.stem),
                    "title": str(metadata.get("title") or path.stem),
                    "tags": " ".join(tags),
                    "text": "\n".join(content),
                    "source_location": location,
                }
            )
    return fragments


def search_materials(
    root: Path, topics: list[str], *, limit: int = 8
) -> list[dict[str, str]]:
    """Find material fragments, ranking tag matches before title and text."""
    root = _root(root)
    clean_topics = [topic.strip().lstrip("#") for topic in topics if topic.strip()]
    if not clean_topics or limit < 1:
        return []
    ranked: list[tuple[int, str, int, dict[str, str]]] = []
    for path in sorted((root / MATERIAL_DIR).glob("*.md")):
        for order, fragment in enumerate(_material_fragments(path)):
            tags = fragment["tags"].split()
            if any(topic in tags for topic in clean_topics):
                rank, kind = 0, "tag"
            elif any(topic.casefold() in fragment["title"].casefold() for topic in clean_topics):
                rank, kind = 1, "title"
            elif any(topic.casefold() in fragment["text"].casefold() for topic in clean_topics):
                rank, kind = 2, "text"
            else:
                continue
            result = dict(fragment)
            result["match_kind"] = kind
            ranked.append((rank, path.name, order, result))
    ranked.sort(key=lambda item: item[:3])
    return [item[3] for item in ranked[:limit]]


def _habit_records(root: Path) -> list[dict[str, Any]]:
    text = (_root(root) / STYLE_FILE).read_text(encoding="utf-8")
    records = []
    for match in YAML_RECORD.finditer(text):
        value = yaml.safe_load(match.group(1)) or {}
        if isinstance(value, dict) and value.get("id"):
            records.append(value)
    return records


def load_active_habits(
    root: Path, *, section: str | None = None, language: str | None = None
) -> list[dict[str, str]]:
    """Return confirmed active habits applicable to a section and language."""
    active = []
    for record in _habit_records(root):
        if record.get("status") != "active":
            continue
        if section and record.get("scope", "all") not in {"all", section}:
            continue
        if language and record.get("language", "any") not in {"any", language}:
            continue
        active.append({key: str(value) for key, value in record.items()})
    return active


def _render_style_note(records: list[dict[str, Any]], changes: list[str]) -> str:
    active = [record for record in records if record.get("status") == "active"]
    superseded = [record for record in records if record.get("status") == "superseded"]

    def blocks(values: list[dict[str, Any]]) -> str:
        return "\n\n".join(
            "```yaml\n"
            + yaml.safe_dump(value, sort_keys=False, allow_unicode=True).rstrip()
            + "\n```"
            for value in values
        )

    return (
        "# 写作风格笔记\n\n"
        "## 已确认习惯\n\n"
        f"{blocks(active)}\n\n"
        "## 已废止或替换的习惯\n\n"
        f"{blocks(superseded)}\n\n"
        "## 术语与表达选择\n\n"
        "## 变更记录\n\n"
        + "\n".join(changes)
        + "\n"
    )


def confirm_habit(
    root: Path,
    habit: dict[str, str],
    *,
    confirmed_at: str,
    supersedes: str | None = None,
) -> str:
    """Persist one already user-confirmed habit and optionally supersede another."""
    root = _root(root)
    required = {"scope", "preference", "source_paragraph"}
    if any(not str(habit.get(field, "")).strip() for field in required):
        raise ValueError("Confirmed habit requires scope, preference, and source_paragraph")
    records = _habit_records(root)
    if supersedes:
        old = next((record for record in records if record.get("id") == supersedes), None)
        if old is None or old.get("status") != "active":
            raise ValueError(f"Cannot supersede inactive or missing habit: {supersedes}")
        old["status"] = "superseded"
    numbers = [int(match.group(1)) for record in records if (match := re.fullmatch(r"habit-(\d+)", str(record.get("id"))))]
    habit_id = f"habit-{max(numbers, default=0) + 1:04d}"
    record = {
        "id": habit_id,
        "scope": habit["scope"],
        "language": habit.get("language", "any"),
        "preference": habit["preference"],
        "avoid": habit.get("avoid", ""),
        "source_paragraph": habit["source_paragraph"],
        "confirmed_at": confirmed_at,
        "status": "active",
    }
    records.append(record)
    note_path = root / STYLE_FILE
    old_text = note_path.read_text(encoding="utf-8")
    change_lines = [line for line in old_text.splitlines() if line.startswith("- ")]
    action = f"confirmed {habit_id}"
    if supersedes:
        action += f"; superseded {supersedes}"
    change_lines.append(f"- {confirmed_at}: {action}")
    temporary = note_path.with_suffix(".md.tmp")
    temporary.write_text(_render_style_note(records, change_lines), encoding="utf-8")
    temporary.replace(note_path)
    return habit_id


def _managed_path(root: Path, relative: str) -> Path:
    root = _root(root)
    target = (root / relative).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise WritingWorkspaceError("Managed path escapes the writing workspace") from exc
    return target


def update_working_draft(root: Path, source: Path) -> Path:
    """Replace only the managed work draft from an explicit revision file."""
    if not source.is_file():
        raise FileNotFoundError(source)
    project = load_project(root)
    target = _managed_path(root, str(project["current_working_draft"]))
    temporary = target.with_suffix(target.suffix + ".tmp")
    shutil.copy2(source, temporary)
    temporary.replace(target)
    return target


def snapshot_working_draft(
    root: Path, *, timestamp: str, partial: bool = False
) -> Path:
    """Create a non-overwriting confirmed or explicitly partial snapshot."""
    project = load_project(root)
    source = _managed_path(root, str(project["current_working_draft"]))
    label = "_partial" if partial else ""
    target = _root(root) / "草稿" / "02-已确认版本" / (
        f"{source.stem}_{timestamp}{label}{source.suffix}"
    )
    if target.exists():
        raise FileExistsError(target)
    shutil.copy2(source, target)
    return target
