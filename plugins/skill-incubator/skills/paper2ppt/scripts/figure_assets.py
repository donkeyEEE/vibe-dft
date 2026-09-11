"""Render selected PDF evidence crops and record manual crop confirmation."""

from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib
import json
from pathlib import Path
import re
from typing import Sequence

import fitz


_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")


class CropVerificationError(ValueError):
    """Raised when a crop cannot safely be confirmed as evidence."""


class CropValidationError(ValueError):
    """Raised when a crop request or output path is unsafe or invalid."""


@dataclass(frozen=True)
class CropRequest:
    source_pdf: Path
    page_index: int
    rect: tuple[float, float, float, float]
    output_name: str
    source_label: str
    slide_id: str
    preserved: tuple[str, ...]


@dataclass(frozen=True)
class AssetRecord:
    path: Path
    output_path: Path
    asset_root: Path
    source_pdf: Path
    page_index: int
    rect: tuple[float, float, float, float]
    source_label: str
    slide_id: str
    crop_qa: str
    preserved: tuple[str, ...]
    width_px: int
    height_px: int
    output_sha256: str
    verified_elements: tuple[str, ...] = ()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _clip_for(request: CropRequest, page: fitz.Page) -> fitz.Rect:
    if request.page_index < 0:
        raise CropValidationError("page_index must be zero-based and non-negative")
    if len(request.rect) != 4:
        raise CropValidationError("rect must have four coordinates")
    clip = fitz.Rect(*request.rect)
    if clip.is_empty or clip.is_infinite or not page.rect.contains(clip):
        raise CropValidationError("crop rectangle must be non-empty and contained by the page")
    return clip


def _contained_images_dir(project_root: Path) -> tuple[Path, Path]:
    canonical_root = project_root.resolve()
    canonical_root.mkdir(parents=True, exist_ok=True)
    images_path = canonical_root / "images"
    if images_path.is_symlink():
        raise CropValidationError("images must be a real directory inside project_root")
    images_path.mkdir(parents=True, exist_ok=True)
    canonical_images = images_path.resolve(strict=True)
    if not canonical_images.is_relative_to(canonical_root):
        raise CropValidationError("images resolves outside project_root")
    return canonical_root, canonical_images


def render_crop(request: CropRequest, project_root: Path, dpi: int = 300) -> AssetRecord:
    """Render only the requested page rectangle; semantic QA remains manual."""
    if dpi <= 0:
        raise CropValidationError("dpi must be positive")
    output_name = Path(request.output_name)
    if output_name.name != request.output_name or output_name.suffix.lower() != ".png":
        raise CropValidationError("output_name must be a PNG filename")
    source_pdf = request.source_pdf.resolve()
    if not source_pdf.is_file():
        raise CropValidationError(f"source PDF does not exist: {request.source_pdf}")
    _, images_dir = _contained_images_dir(project_root)
    output_path = (images_dir / output_name).resolve()
    if not output_path.is_relative_to(images_dir):
        raise CropValidationError("crop output must remain inside project_root/images")
    document = fitz.open(source_pdf)
    try:
        if request.page_index >= document.page_count:
            raise CropValidationError("page_index is outside the source PDF")
        page = document.load_page(request.page_index)
        clip = _clip_for(request, page)
        pixmap = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72), clip=clip, alpha=False)
        pixmap.save(output_path)
    finally:
        document.close()
    if pixmap.width <= 0 or pixmap.height <= 0:
        raise CropValidationError("rendered crop has zero dimensions")
    return AssetRecord(
        path=output_path,
        output_path=Path("images") / output_name,
        asset_root=images_dir,
        source_pdf=source_pdf,
        page_index=request.page_index,
        rect=tuple(float(value) for value in request.rect),
        source_label=request.source_label,
        slide_id=request.slide_id,
        crop_qa="pending",
        preserved=request.preserved,
        width_px=pixmap.width,
        height_px=pixmap.height,
        output_sha256=_sha256(output_path),
    )


def confirm_crop(record: AssetRecord, verified_elements: Sequence[str]) -> AssetRecord:
    """Mark a crop passing only after manual review confirms every required item."""
    checked = tuple(verified_elements)
    if not record.path.is_file():
        raise CropVerificationError("rendered crop path must be a regular file")
    try:
        resolved_path = record.path.resolve(strict=True)
        resolved_root = record.asset_root.resolve(strict=True)
    except OSError as exc:
        raise CropVerificationError(f"rendered crop path cannot be resolved: {exc}") from exc
    if record.path != resolved_path or record.asset_root != resolved_root:
        raise CropVerificationError("rendered crop path and asset root must be canonical")
    if resolved_root.name != "images" or not resolved_path.is_relative_to(resolved_root):
        raise CropVerificationError("rendered crop path must remain inside canonical images root")
    if record.width_px <= 0 or record.height_px <= 0:
        raise CropVerificationError("rendered crop must have nonzero dimensions")
    try:
        image = fitz.Pixmap(str(resolved_path))
    except Exception as exc:
        raise CropVerificationError(f"rendered crop is not a readable image: {exc}") from exc
    if image.width != record.width_px or image.height != record.height_px:
        raise CropVerificationError("rendered crop pixel dimensions do not match the asset record")
    if _SHA256_PATTERN.fullmatch(record.output_sha256) is None:
        raise CropVerificationError("asset record must contain a valid lowercase SHA-256 digest")
    if _sha256(resolved_path) != record.output_sha256:
        raise CropVerificationError("rendered crop SHA-256 does not match the asset record")
    if set(checked) != set(record.preserved) or len(checked) != len(set(checked)):
        raise CropVerificationError("verified elements must exactly cover preserved elements")
    return replace(record, crop_qa="pass", verified_elements=checked)


def write_asset_manifest(records: Sequence[AssetRecord], path: Path) -> None:
    """Write a deterministic manifest that records manual crop confirmation."""
    payload = [
        {
            "path": str(record.output_path),
            "source_pdf": str(record.source_pdf),
            "page_index": record.page_index,
            "rect": record.rect,
            "source_label": record.source_label,
            "slide_id": record.slide_id,
            "crop_qa": record.crop_qa,
            "preserved": record.preserved,
            "width_px": record.width_px,
            "height_px": record.height_px,
            "output_sha256": record.output_sha256,
            "verified_elements": record.verified_elements,
        }
        for record in records
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def load_asset_manifest(path: Path) -> tuple[AssetRecord, ...]:
    """Load a JSON asset manifest without losing path, tuple, or float types."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    project_root = path.parent.resolve()
    asset_root = project_root / "images"
    if asset_root.is_symlink():
        raise CropValidationError("images must be a real directory inside project_root")
    asset_root = asset_root.resolve()

    def load_record(item: dict[str, object]) -> AssetRecord:
        output_path = Path(str(item["path"]))
        if output_path.is_absolute():
            raise CropValidationError("manifest asset path must be project-relative")
        asset_path = (project_root / output_path).resolve()
        if not asset_path.is_relative_to(asset_root):
            raise CropValidationError("manifest asset path must remain inside project_root/images")
        output_sha256 = item.get("output_sha256")
        if not isinstance(output_sha256, str) or _SHA256_PATTERN.fullmatch(output_sha256) is None:
            raise CropValidationError(
                "manifest output_sha256 must be exactly 64 lowercase hexadecimal characters"
            )
        return AssetRecord(
            path=asset_path,
            output_path=output_path,
            asset_root=asset_root,
            source_pdf=Path(str(item["source_pdf"])),
            page_index=int(item["page_index"]),
            rect=tuple(float(value) for value in item["rect"]),
            source_label=str(item["source_label"]),
            slide_id=str(item["slide_id"]),
            crop_qa=str(item["crop_qa"]),
            preserved=tuple(str(value) for value in item["preserved"]),
            width_px=int(item["width_px"]),
            height_px=int(item["height_px"]),
            output_sha256=output_sha256,
            verified_elements=tuple(str(value) for value in item["verified_elements"]),
        )

    return tuple(
        load_record(item)
        for item in payload
    )
