#!/usr/bin/env python3
"""Core operations for Cangjie knowledge-distillation projects."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import Any, Callable, Literal, NamedTuple
from datetime import datetime, timezone

import yaml


PROJECT_PHASES = frozenset(
    {
        "initialized",
        "parsing",
        "extracting",
        "reviewing",
        "delivering",
        "complete",
        "blocked",
    }
)
REVIEW_ACTIONS = frozenset(
    {"accept", "reject", "revise", "merge", "split", "deliver"}
)


class ProjectError(RuntimeError):
    """Raised when a project operation would violate the workspace contract."""


class ValidationIssue(NamedTuple):
    level: Literal["error", "warning"]
    code: str
    path: str
    message: str


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _validate_identifier(value: str, field: str) -> None:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise ProjectError(f"{field} must use lowercase kebab-case: {value}")


def sha256_file(path: Path) -> str:
    """Return the SHA-256 digest of *path* without loading it all into memory."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_yaml(path: Path) -> dict[str, Any]:
    """Read a mapping-root YAML document."""
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ProjectError(f"YAML root must be a mapping: {path}")
    return value


def write_yaml_atomic(path: Path, value: dict[str, Any]) -> None:
    """Serialize YAML beside its target and atomically replace the target."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    try:
        with temporary.open("w", encoding="utf-8") as stream:
            yaml.safe_dump(value, stream, allow_unicode=True, sort_keys=False)
            stream.flush()
        temporary.replace(path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def _write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    try:
        temporary.write_text(text, encoding="utf-8")
        temporary.replace(path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def resolve_inside(root: Path, relative: str) -> Path:
    """Resolve a relative path and reject paths escaping *root*."""
    resolved_root = root.resolve()
    resolved = (resolved_root / relative).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as error:
        raise ProjectError(f"path is outside project root: {relative}") from error
    return resolved


def current_candidate_states(review_log: dict[str, Any]) -> dict[str, str]:
    """Derive candidate states from the last applicable review decision."""
    decisions = review_log.get("decisions", [])
    if not isinstance(decisions, list):
        raise ProjectError("review log decisions must be a list")
    states: dict[str, str] = {}
    for decision in decisions:
        if not isinstance(decision, dict):
            raise ProjectError("review decision must be a mapping")
        candidate_id = decision.get("candidate_id")
        action = decision.get("action")
        if not isinstance(candidate_id, str) or not candidate_id:
            raise ProjectError("review decision requires candidate_id")
        if action not in REVIEW_ACTIONS:
            raise ProjectError(f"invalid review action: {action}")
        states[candidate_id] = action
    return states


def initialize_project(
    project_root: Path,
    project_id: str,
    topic: str,
    source_id: str,
    source_pdf: Path,
    title: str,
    scope_file: Path | None = None,
) -> Path:
    """Create a complete project skeleton around a copied source PDF."""
    project_root = project_root.resolve()
    source_pdf = source_pdf.resolve()
    if project_root.exists():
        raise ProjectError(f"project already exists: {project_root}")
    if not source_pdf.is_file():
        raise ProjectError(f"source PDF does not exist: {source_pdf}")
    _validate_identifier(project_id, "project_id")
    _validate_identifier(source_id, "source_id")

    if scope_file is None:
        scope: dict[str, Any] = {
            "schema_version": 1,
            "sources": {source_id: {"units": []}},
        }
    else:
        scope = read_yaml(scope_file.resolve())

    source_digest = sha256_file(source_pdf)
    project_root.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(
        tempfile.mkdtemp(prefix=f".{project_root.name}-", dir=project_root.parent)
    )
    try:
        source_root = temporary / "sources" / source_id
        for directory in (
            source_root / "source",
            source_root / "parsed",
            source_root / "screenshots",
            temporary / "extraction",
            temporary / "evidence",
            temporary / "candidates" / "by-source",
            temporary / "candidates" / "consolidated",
            temporary / "decisions",
            temporary / "delivery",
        ):
            directory.mkdir(parents=True, exist_ok=True)

        copied_pdf = source_root / "source" / "original.pdf"
        copy_temporary = copied_pdf.with_suffix(".pdf.tmp")
        shutil.copyfile(source_pdf, copy_temporary)
        if sha256_file(copy_temporary) != source_digest:
            raise ProjectError("copied source PDF failed SHA-256 verification")
        copy_temporary.replace(copied_pdf)

        created_at = _utc_now()
        write_yaml_atomic(
            temporary / "project.yaml",
            {
                "schema_version": 1,
                "project_id": project_id,
                "topic": topic,
                "phase": "initialized",
                "sources": [source_id],
                "units": {},
                "created_at": created_at,
                "updated_at": created_at,
                "last_error": None,
            },
        )
        write_yaml_atomic(temporary / "scope.yaml", scope)
        write_yaml_atomic(
            source_root / "source.yaml",
            {
                "schema_version": 1,
                "source_id": source_id,
                "title": title,
                "source_type": "book",
                "original_location": str(source_pdf),
                "project_copy": f"sources/{source_id}/source/original.pdf",
                "sha256": source_digest,
                "parser": {"engine": "liteparse", "ocr": False},
                "page_mapping": {},
            },
        )
        write_yaml_atomic(temporary / "decisions" / "review-log.yaml", {"decisions": []})
        write_yaml_atomic(temporary / "delivery" / "manifest.yaml", {"deliveries": []})
        for keep in (
            temporary / "candidates" / "by-source" / ".gitkeep",
            temporary / "candidates" / "consolidated" / ".gitkeep",
            source_root / "screenshots" / ".gitkeep",
        ):
            keep.write_text("", encoding="utf-8")
        (temporary / "delivery" / "report.md").write_text(
            "# Delivery report\n\nNo cards have been delivered.\n", encoding="utf-8"
        )
        temporary.replace(project_root)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    return project_root


def _validated_document(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ProjectError(f"invalid LiteParse JSON: {path}") from error
    if not isinstance(value, dict) or not isinstance(value.get("pages"), list):
        raise ProjectError(f"LiteParse JSON requires a pages list: {path}")
    return value


def export_scoped_text(
    document: dict[str, Any], units: list[dict[str, Any]]
) -> dict[str, str]:
    """Create layout-preserved text views for inclusive page ranges."""
    pages = document.get("pages")
    if not isinstance(pages, list):
        raise ProjectError("LiteParse document requires a pages list")
    page_text: dict[int, str] = {}
    for page in pages:
        if not isinstance(page, dict) or not isinstance(page.get("page"), int):
            raise ProjectError("LiteParse page requires an integer page number")
        text = page.get("text", "")
        if not isinstance(text, str):
            raise ProjectError(f"LiteParse page {page['page']} text must be a string")
        page_text[page["page"]] = text

    exports: dict[str, str] = {}
    for unit in units:
        unit_id = unit.get("unit_id")
        if not isinstance(unit_id, str) or not unit_id:
            raise ProjectError("scope unit requires unit_id")
        pdf_pages = unit.get("pdf_pages")
        pdf_page_ranges = unit.get("pdf_page_ranges")
        if pdf_pages is not None and pdf_page_ranges is not None:
            raise ProjectError(
                f"scope unit {unit_id} cannot define both pdf_pages and pdf_page_ranges"
            )
        ranges = [pdf_pages] if pdf_pages is not None else pdf_page_ranges
        if not isinstance(ranges, list) or not ranges:
            raise ProjectError(
                f"scope unit {unit_id} requires pdf_pages or pdf_page_ranges"
            )
        for page_range in ranges:
            if (
                not isinstance(page_range, list)
                or len(page_range) != 2
                or not all(isinstance(page, int) for page in page_range)
                or page_range[0] > page_range[1]
            ):
                raise ProjectError(
                    f"scope unit {unit_id} requires inclusive PDF page ranges"
                )
        chunks: list[str] = []
        for start, end in ranges:
            for number in range(start, end + 1):
                if number not in page_text:
                    raise ProjectError(f"missing PDF page {number} for {unit_id}")
                chunks.append(page_text[number].rstrip())
        exports[unit_id] = "\n\n".join(chunks).rstrip() + "\n"
    return exports


def _set_project_phase(project_root: Path, phase: str, error: str | None) -> None:
    project_path = project_root / "project.yaml"
    project = read_yaml(project_path)
    project["phase"] = phase
    project["updated_at"] = _utc_now()
    project["last_error"] = error
    write_yaml_atomic(project_path, project)


def parse_source(
    project_root: Path,
    source_id: str,
    *,
    force: bool = False,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> Path:
    """Parse a copied source with LiteParse and export all scoped text units."""
    project_root = project_root.resolve()
    source_root = project_root / "sources" / source_id
    source_metadata = read_yaml(source_root / "source.yaml")
    source_pdf = resolve_inside(project_root, str(source_metadata.get("project_copy", "")))
    recorded_hash = source_metadata.get("sha256")
    if not source_pdf.is_file() or sha256_file(source_pdf) != recorded_hash:
        raise ProjectError(f"source PDF SHA-256 mismatch: {source_pdf}")

    scope = read_yaml(project_root / "scope.yaml")
    source_scopes = scope.get("sources")
    if not isinstance(source_scopes, dict) or not isinstance(
        source_scopes.get(source_id), dict
    ):
        raise ProjectError(f"scope is missing source: {source_id}")
    units = source_scopes[source_id].get("units")
    if not isinstance(units, list):
        raise ProjectError(f"scope units must be a list: {source_id}")

    parsed_root = source_root / "parsed"
    document_path = parsed_root / "document.json"
    temporary = document_path.with_suffix(".json.tmp")
    _set_project_phase(project_root, "parsing", None)
    try:
        if document_path.is_file() and not force:
            document = _validated_document(document_path)
        else:
            temporary.unlink(missing_ok=True)
            command = [
                "lit",
                "parse",
                str(source_pdf),
                "--format",
                "json",
                "--no-ocr",
                "-o",
                str(temporary),
            ]
            result = runner(command, check=True, capture_output=True, text=True)
            if result.returncode != 0:
                raise subprocess.CalledProcessError(
                    result.returncode, command, result.stdout, result.stderr
                )
            document = _validated_document(temporary)
            temporary.replace(document_path)

        exports = export_scoped_text(document, units)
        for unit_id, text in exports.items():
            _write_text_atomic(parsed_root / f"{unit_id}.txt", text)

        project = read_yaml(project_root / "project.yaml")
        project_units = project.setdefault("units", {})
        if not isinstance(project_units, dict):
            raise ProjectError("project units must be a mapping")
        for unit in units:
            unit_id = unit["unit_id"]
            unit_record = project_units.setdefault(unit_id, {"status": "pending"})
            if not isinstance(unit_record, dict):
                raise ProjectError(f"project unit must be a mapping: {unit_id}")
            unit_record.setdefault("mode", unit.get("mode", "full"))
            unit_record.setdefault("source_id", source_id)
            extraction_path = project_root / "extraction" / f"{unit_id}.yaml"
            if not extraction_path.exists():
                write_yaml_atomic(
                    extraction_path,
                    {
                        "unit_id": unit_id,
                        "source_id": source_id,
                        "status": "pending",
                        "processed_sections": [],
                        "knowledge_objects": [],
                        "omission_risks": [],
                        "exceptions": [],
                    },
                )
            evidence_path = project_root / "evidence" / f"{unit_id}.yaml"
            if not evidence_path.exists():
                write_yaml_atomic(
                    evidence_path,
                    {"unit_id": unit_id, "source_id": source_id, "evidence": []},
                )
        project["phase"] = "extracting"
        project["updated_at"] = _utc_now()
        project["last_error"] = None
        write_yaml_atomic(project_root / "project.yaml", project)
    except subprocess.CalledProcessError as error:
        temporary.unlink(missing_ok=True)
        message = f"LiteParse failed for {source_id}: {error.stderr or error}"
        _set_project_phase(project_root, "parsing", message)
        raise ProjectError(message) from error
    except Exception as error:
        temporary.unlink(missing_ok=True)
        message = str(error)
        _set_project_phase(project_root, "parsing", message)
        if isinstance(error, ProjectError):
            raise
        raise ProjectError(message) from error
    return document_path


def _candidate_paths(root: Path) -> list[Path]:
    paths = [*root.rglob("*.yaml"), *root.rglob("*.yml")]
    return sorted(set(path.resolve() for path in paths))


def _load_for_validation(
    path: Path, issues: list[ValidationIssue]
) -> dict[str, Any] | None:
    try:
        return read_yaml(path)
    except (OSError, yaml.YAMLError, ProjectError) as error:
        issues.append(ValidationIssue("error", "INVALID_YAML", str(path), str(error)))
        return None


def project_status(project_root: Path) -> dict[str, object]:
    """Return a read-only summary of project progress."""
    project_root = project_root.resolve()
    project = read_yaml(project_root / "project.yaml")
    evidence_count = 0
    for path in sorted((project_root / "evidence").glob("*.yaml")):
        evidence = read_yaml(path).get("evidence", [])
        if isinstance(evidence, list):
            evidence_count += len(evidence)
    by_source = _candidate_paths(project_root / "candidates" / "by-source")
    consolidated = _candidate_paths(project_root / "candidates" / "consolidated")
    states = current_candidate_states(
        read_yaml(project_root / "decisions" / "review-log.yaml")
    )
    sources = project.get("sources", [])
    units = project.get("units", {})
    return {
        "project_id": project.get("project_id"),
        "phase": project.get("phase"),
        "sources": len(sources) if isinstance(sources, list) else 0,
        "units": len(units) if isinstance(units, dict) else 0,
        "evidence": evidence_count,
        "by_source_candidates": len(by_source),
        "consolidated_candidates": len(consolidated),
        "review_states": states,
    }


def validate_project(
    project_root: Path, shared_root: Path | None = None
) -> list[ValidationIssue]:
    """Validate provenance, review, and delivery links without changing the project."""
    project_root = project_root.resolve()
    issues: list[ValidationIssue] = []

    required = [
        "project.yaml",
        "scope.yaml",
        "sources",
        "extraction",
        "evidence",
        "candidates/by-source",
        "candidates/consolidated",
        "decisions/review-log.yaml",
        "delivery/manifest.yaml",
    ]
    for relative in required:
        if not (project_root / relative).exists():
            issues.append(
                ValidationIssue(
                    "error", "MISSING_REQUIRED_PATH", relative, "required path is missing"
                )
            )

    project = _load_for_validation(project_root / "project.yaml", issues)
    if project is None:
        return sorted(issues)
    phase = project.get("phase")
    if phase not in PROJECT_PHASES:
        issues.append(
            ValidationIssue("error", "INVALID_PROJECT_PHASE", "project.yaml", str(phase))
        )

    source_ids = project.get("sources", [])
    if not isinstance(source_ids, list):
        issues.append(
            ValidationIssue("error", "INVALID_SOURCES", "project.yaml", "sources must be a list")
        )
        source_ids = []
    for source_id in source_ids:
        metadata_path = project_root / "sources" / str(source_id) / "source.yaml"
        metadata = _load_for_validation(metadata_path, issues)
        if metadata is None:
            continue
        relative_copy = metadata.get("project_copy")
        try:
            source_pdf = resolve_inside(project_root, str(relative_copy))
        except ProjectError as error:
            issues.append(ValidationIssue("error", "PATH_ESCAPE", str(metadata_path), str(error)))
            continue
        if not source_pdf.is_file() or sha256_file(source_pdf) != metadata.get("sha256"):
            issues.append(
                ValidationIssue(
                    "error",
                    "SOURCE_HASH_MISMATCH",
                    str(source_pdf),
                    "copied source does not match recorded SHA-256",
                )
            )

    evidence_ids: set[str] = set()
    for path in sorted((project_root / "evidence").glob("*.yaml")):
        document = _load_for_validation(path, issues)
        if document is None:
            continue
        entries = document.get("evidence", [])
        if not isinstance(entries, list):
            issues.append(ValidationIssue("error", "INVALID_EVIDENCE", str(path), "evidence must be a list"))
            continue
        for entry in entries:
            if not isinstance(entry, dict) or not isinstance(entry.get("evidence_id"), str):
                issues.append(ValidationIssue("error", "INVALID_EVIDENCE", str(path), "entry requires evidence_id"))
                continue
            evidence_id = entry["evidence_id"]
            if evidence_id in evidence_ids:
                issues.append(ValidationIssue("error", "DUPLICATE_EVIDENCE_ID", str(path), evidence_id))
            evidence_ids.add(evidence_id)
            locator = entry.get("locator", {})
            precise = isinstance(locator, dict) and any(
                locator.get(key) is not None
                for key in ("pdf_page", "book_page", "section", "equation")
            )
            if not precise:
                issues.append(ValidationIssue("warning", "IMPRECISE_LOCATOR", str(path), evidence_id))

    candidates: dict[str, dict[str, Any]] = {}
    for candidate_root in (
        project_root / "candidates" / "by-source",
        project_root / "candidates" / "consolidated",
    ):
        for path in _candidate_paths(candidate_root):
            candidate = _load_for_validation(path, issues)
            if candidate is None:
                continue
            candidate_id = candidate.get("candidate_id")
            if not isinstance(candidate_id, str) or not candidate_id:
                issues.append(ValidationIssue("error", "INVALID_CANDIDATE", str(path), "candidate_id is required"))
                continue
            candidates[candidate_id] = candidate
            references = candidate.get("evidence_ids", [])
            if not isinstance(references, list):
                issues.append(ValidationIssue("error", "INVALID_CANDIDATE", str(path), "evidence_ids must be a list"))
                continue
            for evidence_id in references:
                if evidence_id not in evidence_ids:
                    issues.append(ValidationIssue("error", "MISSING_EVIDENCE", str(path), str(evidence_id)))

    review_path = project_root / "decisions" / "review-log.yaml"
    review = _load_for_validation(review_path, issues) or {"decisions": []}
    decisions = review.get("decisions", [])
    states: dict[str, str] = {}
    if not isinstance(decisions, list):
        issues.append(ValidationIssue("error", "INVALID_REVIEW_LOG", str(review_path), "decisions must be a list"))
    else:
        for decision in decisions:
            if not isinstance(decision, dict):
                issues.append(ValidationIssue("error", "INVALID_REVIEW_LOG", str(review_path), "decision must be a mapping"))
                continue
            candidate_id = decision.get("candidate_id")
            action = decision.get("action")
            if action not in REVIEW_ACTIONS:
                issues.append(ValidationIssue("error", "INVALID_REVIEW_ACTION", str(review_path), str(action)))
                continue
            if isinstance(candidate_id, str):
                states[candidate_id] = action

    consolidated_ids: set[str] = set()
    for path in _candidate_paths(project_root / "candidates" / "consolidated"):
        candidate = _load_for_validation(path, [])
        if candidate and isinstance(candidate.get("candidate_id"), str):
            consolidated_ids.add(candidate["candidate_id"])
    for candidate_id in sorted(consolidated_ids - states.keys()):
        issues.append(ValidationIssue("warning", "UNREVIEWED_CANDIDATE", "candidates/consolidated", candidate_id))

    units = project.get("units", {})
    if isinstance(units, dict):
        for unit_id, unit in units.items():
            if isinstance(unit, dict) and unit.get("mode") == "selective" and unit.get("status") == "pending":
                issues.append(ValidationIssue("warning", "PENDING_SELECTIVE_UNIT", "project.yaml", str(unit_id)))

    manifest_path = project_root / "delivery" / "manifest.yaml"
    manifest = _load_for_validation(manifest_path, issues) or {"deliveries": []}
    deliveries = manifest.get("deliveries", [])
    if isinstance(deliveries, list):
        for delivery in deliveries:
            if not isinstance(delivery, dict):
                continue
            candidate_id = delivery.get("candidate_id")
            if states.get(str(candidate_id)) not in {"accept", "deliver"}:
                issues.append(ValidationIssue("error", "DELIVERY_NOT_ACCEPTED", str(manifest_path), str(candidate_id)))
            card_path = delivery.get("card_path")
            if shared_root is not None:
                try:
                    card = resolve_inside(shared_root.resolve(), str(card_path))
                except ProjectError as error:
                    issues.append(ValidationIssue("error", "PATH_ESCAPE", str(manifest_path), str(error)))
                else:
                    if not card.is_file():
                        issues.append(ValidationIssue("error", "MISSING_DELIVERY_CARD", str(card), str(candidate_id)))
    else:
        issues.append(ValidationIssue("error", "INVALID_DELIVERY_MANIFEST", str(manifest_path), "deliveries must be a list"))

    return sorted(issues, key=lambda issue: (issue.level, issue.code, issue.path, issue.message))
