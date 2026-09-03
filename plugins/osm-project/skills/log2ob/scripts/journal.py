"""Canonical Markdown project-log operations for the log2ob skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Any


PROJECT_LOG_HEADING = "### 项目日志"
SUMMARY_HEADING = "### Summarize Today"
MANAGEMENT_HEADING = "### 笔记的管理规范"
SUMMARY_FIELDS: tuple[str, ...] = ("任务", "起点", "进展", "结论", "未决", "入口")
FIELD_PATTERN = re.compile(r"^- \*\*(任务|起点|进展|结论|未决|入口)\*\*：(.*)$")
DAILY_RELATIVE_DIR = Path("01-个人/0105-journal/日记")


class JournalError(Exception):
    """Raised when a project-log document cannot be changed safely."""

    def __init__(self, message: str, recovery: str = "Inspect the note and retry."):
        super().__init__(message)
        self.recovery = recovery


class JsonArgumentParser(argparse.ArgumentParser):
    """Report invalid command input through the helper's JSON error boundary."""

    def error(self, message: str) -> None:
        raise JournalError(
            f"Invalid command arguments: {message}",
            "Correct the command options and retry.",
        )


def note_revision(text: str) -> str:
    """Return the SHA-256 digest of the exact UTF-8 note text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def guarded_replace(path: Path, original_text: str, updated_text: str) -> None:
    """Atomically replace a note only if its original text still matches."""
    before = path.stat()
    if _read_note_utf8(path) != original_text:
        raise JournalError(
            f"Note changed before write: {path}",
            "Reload the note, recreate the draft, and reconfirm the write.",
        )

    temporary_path: Path | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
        )
        temporary_path = Path(temporary_name)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(updated_text)
            handle.flush()
            os.fsync(handle.fileno())

        after = path.stat()
        signature_before = (before.st_size, before.st_mtime_ns, before.st_ino)
        signature_after = (after.st_size, after.st_mtime_ns, after.st_ino)
        if signature_after != signature_before or _read_note_utf8(path) != original_text:
            raise JournalError(
                f"Note changed during write: {path}",
                "Reload the note, recreate the draft, and reconfirm the write.",
            )
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def find_unique_section(text: str, heading: str) -> tuple[int, int]:
    """Return the content bounds of one exact Markdown heading."""
    lines = _lines_with_offsets(text)
    matches = [index for index, (_, line, _) in enumerate(lines) if line == heading]

    if not matches:
        raise JournalError(f"Missing heading: {heading}")
    if len(matches) > 1:
        raise JournalError(f"Duplicate heading: {heading}")

    heading_index = matches[0]
    heading_level = len(heading) - len(heading.lstrip("#"))
    heading_offset, _, raw_heading = lines[heading_index]
    start = heading_offset + len(raw_heading)
    end = len(text)
    next_heading = re.compile(rf"^#{{1,{heading_level}}}\s+")
    for line_offset, line, _ in lines[heading_index + 1 :]:
        if next_heading.match(line):
            end = line_offset
            break
    return start, end


def parse_project_fields(block: str) -> dict[str, str]:
    """Extract nonblank canonical project-summary fields from a block."""
    fields: dict[str, str] = {}
    for line in block.splitlines():
        match = FIELD_PATTERN.match(line)
        if match and (value := match.group(2).strip()):
            fields[match.group(1)] = value
    return fields


def render_project_block(project: str, fields: dict[str, str]) -> str:
    """Render one project under its canonical level-four heading."""
    normalized_project = _normalize_project(project)
    unknown_fields = set(fields).difference(SUMMARY_FIELDS)
    if unknown_fields:
        raise JournalError(f"Unknown summary field: {sorted(unknown_fields)[0]}")
    for value in fields.values():
        if "\n" in value or "\r" in value:
            raise JournalError("Invalid field value: newlines are not allowed")

    normalized_fields = {
        name: value.strip() for name, value in fields.items() if value.strip()
    }
    if not normalized_fields:
        raise JournalError("Project fields must contain at least one nonblank value")

    rendered_fields = "".join(
        f"- **{name}**：{normalized_fields[name]}\n"
        for name in SUMMARY_FIELDS
        if name in normalized_fields
    )
    return f"#### {normalized_project}\n\n{rendered_fields}"


def inspect_project(text: str, project: str) -> tuple[bool, dict[str, str]]:
    """Report whether a project exists and return its canonical fields."""
    normalized_project = _normalize_project(project)
    try:
        section_start, section_end = find_unique_section(text, PROJECT_LOG_HEADING)
    except JournalError as error:
        if str(error).startswith("Missing heading:"):
            return False, {}
        raise

    project_heading = f"#### {normalized_project}"
    section = text[section_start:section_end]
    matches = _exact_line_offsets(section, project_heading)
    if len(matches) > 1:
        raise JournalError(f"Duplicate project: {normalized_project}")
    if not matches:
        return False, {}

    block_start = matches[0] + len(project_heading)
    block_end = _following_project_heading(section, block_start)
    return True, parse_project_fields(section[block_start:block_end])


def upsert_project(
    text: str, project: str, fields: dict[str, str]
) -> tuple[str, str]:
    """Add or replace one project with its canonical Markdown block."""
    normalized_project = _normalize_project(project)
    block = render_project_block(normalized_project, fields)
    try:
        section_start, section_end = find_unique_section(text, PROJECT_LOG_HEADING)
    except JournalError as error:
        if not str(error).startswith("Missing heading:"):
            raise
        insertion_point = _section_insertion_point(text)
        section = f"{PROJECT_LOG_HEADING}\n\n{block}"
        return _insert_section(text, insertion_point, section), "added"

    project_heading = f"#### {normalized_project}"
    section = text[section_start:section_end]
    matches = _exact_line_offsets(section, project_heading)
    if len(matches) > 1:
        raise JournalError(f"Duplicate project: {normalized_project}")
    if not matches:
        return _append_project(text, section_end, block), "added"

    block_start = section_start + matches[0]
    raw_block_end = section_start + _following_project_heading(
        section, matches[0] + len(project_heading)
    )
    existing_block = text[block_start:raw_block_end]
    canonical_existing = existing_block.rstrip("\r\n") + "\n"
    if canonical_existing == block:
        return text, "unchanged"
    trailing_whitespace = existing_block[len(existing_block.rstrip("\r\n")) :]
    if trailing_whitespace.startswith("\r\n"):
        trailing_whitespace = trailing_whitespace[2:]
    elif trailing_whitespace:
        trailing_whitespace = trailing_whitespace[1:]
    return (
        text[:block_start] + block + trailing_whitespace + text[raw_block_end:],
        "updated",
    )


def _normalize_project(project: str) -> str:
    normalized = project.strip()
    if not normalized or "\n" in project or "\r" in project or normalized.startswith("#"):
        raise JournalError(f"Invalid project: {project!r}")
    return normalized


def _section_insertion_point(text: str) -> int:
    try:
        _, end = find_unique_section(text, SUMMARY_HEADING)
    except JournalError as error:
        if not str(error).startswith("Missing heading:"):
            raise
    else:
        return end

    management_start = _unique_heading_start(text, MANAGEMENT_HEADING)
    if management_start is not None:
        return management_start
    return len(text)


def _insert_section(text: str, insertion_point: int, section: str) -> str:
    prefix = text[:insertion_point]
    suffix = text[insertion_point:]
    if prefix:
        prefix += "\n" if prefix.endswith("\n") else "\n\n"
    if suffix:
        return prefix + section + "\n" + suffix
    return prefix + section


def _append_project(text: str, section_end: int, block: str) -> str:
    prefix = text[:section_end]
    if not prefix.endswith("\n\n"):
        prefix += "\n" if prefix.endswith("\n") else "\n\n"
    return prefix + block + text[section_end:]


def _following_project_heading(section: str, block_start: int) -> int:
    for offset, line, _ in _lines_with_offsets(section[block_start:]):
        if re.match(r"^#{4,}\s+", line):
            return block_start + offset
    return len(section)


def _unique_heading_start(text: str, heading: str) -> int | None:
    matches = _exact_line_offsets(text, heading)
    if len(matches) > 1:
        raise JournalError(f"Duplicate heading: {heading}")
    return matches[0] if matches else None


def _lines_with_offsets(text: str) -> list[tuple[int, str, str]]:
    """Return each line's offset, content, and exact bytes-as-text spelling."""
    result: list[tuple[int, str, str]] = []
    offset = 0
    for raw_line in text.splitlines(keepends=True):
        line = raw_line
        if line.endswith("\r\n"):
            line = line[:-2]
        elif line.endswith(("\r", "\n")):
            line = line[:-1]
        result.append((offset, line, raw_line))
        offset += len(raw_line)
    return result


def _exact_line_offsets(text: str, expected: str) -> list[int]:
    return [offset for offset, line, _ in _lines_with_offsets(text) if line == expected]


def _read_utf8(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def _read_note_utf8(path: Path) -> str:
    try:
        return _read_utf8(path)
    except UnicodeDecodeError as error:
        raise JournalError(
            f"Daily Note is not valid UTF-8: {path}",
            "Open the Daily Note, save it as valid UTF-8, and retry.",
        ) from error


def _require_daily_note(path: Path) -> str:
    if not path.is_file():
        raise JournalError(
            f"Missing Daily Note: {path}",
            "Open Obsidian and initialize the Daily Note for this date, then retry.",
        )
    try:
        return _read_note_utf8(path)
    except PermissionError as error:
        raise JournalError(
            f"Cannot read Daily Note: {path}",
            "Grant Codex access to the Obsidian vault and retry.",
        ) from error


def _parse_day(value: str) -> date:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise JournalError("date must use YYYY-MM-DD") from error
    if parsed.isoformat() != value:
        raise JournalError("date must use YYYY-MM-DD")
    return parsed


def _daily_path(vault: Path, day: date) -> Path:
    return vault / DAILY_RELATIVE_DIR / f"{day.isoformat()}.md"


def _parse_fields(value: object) -> dict[str, str]:
    if not isinstance(value, dict):
        raise JournalError("Invalid request: fields must be an object")

    fields: dict[str, str] = {}
    for key, field_value in value.items():
        if not isinstance(key, str) or not isinstance(field_value, str):
            raise JournalError("Invalid request: field names and values must be strings")
        if "\n" in field_value or "\r" in field_value:
            raise JournalError("Invalid field value: newlines are not allowed")
        if key not in SUMMARY_FIELDS:
            raise JournalError(f"Unknown summary field: {key}")
        fields[key] = field_value
    if not any(value.strip() for value in fields.values()):
        raise JournalError("Project fields must contain at least one nonblank value")
    return fields


def _reject_duplicate_json_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise JournalError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _load_request(path: Path) -> dict[str, object]:
    try:
        request_text = _read_utf8(path)
    except UnicodeDecodeError as error:
        raise JournalError(
            f"Request file is not valid UTF-8: {path}",
            "Recreate the temporary JSON request as UTF-8 and retry.",
        ) from error
    except OSError as error:
        raise JournalError(
            f"Cannot read request file: {path}",
            "Recreate the temporary JSON request and retry.",
        ) from error

    try:
        payload = json.loads(request_text, object_pairs_hook=_reject_duplicate_json_keys)
    except json.JSONDecodeError as error:
        raise JournalError(
            f"Invalid request JSON: {error.msg}",
            "Correct the temporary JSON request and retry.",
        ) from error
    if not isinstance(payload, dict):
        raise JournalError("Invalid request: root must be an object")
    return payload


def _require_string(payload: dict[str, object], key: str) -> str:
    value = payload[key]
    if not isinstance(value, str) or not value:
        raise JournalError(f"Invalid request: {key} must be a nonempty string")
    return value


def _validate_request_keys(
    payload: dict[str, object], expected_keys: set[str]
) -> None:
    missing = expected_keys.difference(payload)
    if missing:
        raise JournalError(f"Missing request key: {sorted(missing)[0]}")
    unknown = set(payload).difference(expected_keys)
    if unknown:
        raise JournalError(f"Unknown request key: {sorted(unknown)[0]}")


def _parse_request(
    path: Path, command: str
) -> tuple[Path, date, str, str | None, dict[str, str] | None]:
    payload = _load_request(path)
    common_keys = {"vault", "date", "project"}
    if command == "inspect":
        _validate_request_keys(payload, common_keys)
        expected_revision = None
        fields = None
    else:
        _validate_request_keys(
            payload, common_keys | {"expected_revision", "fields"}
        )
        expected_revision = _require_string(payload, "expected_revision")
        if not re.fullmatch(r"[0-9a-f]{64}", expected_revision):
            raise JournalError(
                "Invalid request: expected_revision must be a SHA-256 digest"
            )
        fields = _parse_fields(payload["fields"])

    vault = Path(_require_string(payload, "vault"))
    day = _parse_day(_require_string(payload, "date"))
    project = _normalize_project(_require_string(payload, "project"))
    return vault, day, project, expected_revision, fields


def _result(payload: dict[str, Any]) -> int:
    print(json.dumps(payload, ensure_ascii=False))
    return 0


def _inspect(vault: Path, day: date, project: str) -> int:
    path = _daily_path(vault, day)
    text = _require_daily_note(path)
    try:
        find_unique_section(text, PROJECT_LOG_HEADING)
    except JournalError as error:
        if not str(error).startswith("Missing heading:"):
            raise
        section_exists = False
    else:
        section_exists = True
    if section_exists:
        project_exists, fields = inspect_project(text, project)
    else:
        project_exists, fields = False, {}
    return _result(
        {
            "status": "ok",
            "path": str(path),
            "revision": note_revision(text),
            "section_exists": section_exists,
            "project_exists": project_exists,
            "fields": fields,
        }
    )


def _upsert(
    vault: Path, day: date, project: str, expected_revision: str, fields: dict[str, str]
) -> int:
    path = _daily_path(vault, day)
    original = _require_daily_note(path)
    if note_revision(original) != expected_revision:
        raise JournalError(
            f"Note changed since inspection: {path}",
            "Inspect the note again, recreate the draft, and reconfirm the write.",
        )

    normalized_project = _normalize_project(project)
    updated, operation = upsert_project(original, normalized_project, fields)
    if updated != original:
        try:
            guarded_replace(path, original, updated)
        except PermissionError as error:
            raise JournalError(
                f"Cannot write Daily Note: {path}",
                "Grant Codex write access to the Obsidian vault and retry.",
            ) from error
    return _result(
        {
            "status": "ok",
            "path": str(path),
            "revision": note_revision(updated),
            "operation": operation,
            "project": normalized_project,
        }
    )


def _build_parser() -> JsonArgumentParser:
    parser = JsonArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    inspect = subparsers.add_parser("inspect")
    inspect.add_argument("--request", type=Path, required=True)
    upsert = subparsers.add_parser("upsert")
    upsert.add_argument("--request", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        arguments = _build_parser().parse_args(argv)
        vault, day, project, expected_revision, fields = _parse_request(
            arguments.request, arguments.command
        )
        if arguments.command == "inspect":
            return _inspect(vault, day, project)
        if expected_revision is None or fields is None:
            raise AssertionError("validated upsert request is incomplete")
        return _upsert(
            vault,
            day,
            project,
            expected_revision,
            fields,
        )
    except (JournalError, OSError) as error:
        recovery = getattr(error, "recovery", "Check vault access and retry.")
        print(
            json.dumps(
                {"status": "error", "error": str(error), "recovery": recovery},
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
