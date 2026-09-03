#!/usr/bin/env python3
"""Tests for resumable manuscript material libraries."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parents[3] / "skills" / "zo2notes" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import project_storage


@pytest.fixture
def writing_library(tmp_path: Path) -> Path:
    manuscript = tmp_path / "paper.md"
    manuscript.write_text("draft", encoding="utf-8")
    root = project_storage.writing_library_for_manuscript(manuscript)
    project_storage.initialize_writing_library(
        root,
        mode="standalone",
        source_manuscript=manuscript,
        collection_key="COLL1",
        collection_path="论文素材",
    )
    return root


def test_register_material_items_is_resumable(writing_library: Path) -> None:
    first = project_storage.register_material_items(
        writing_library,
        [
            {"item_key": "A", "title": "One", "version": 1},
            {"item_key": "B", "title": "Two", "version": 2},
        ],
    )
    assert [item["status"] for item in first["items"]] == ["pending", "pending"]

    project_storage.write_material_item(
        writing_library,
        metadata={"item_key": "A", "title": "One", "version": 1},
        paragraphs=[
            {
                "tags": ["交换作用"],
                "text": "Source paragraph.",
                "source_location": "indexed full text",
            }
        ],
        evidence_source="zotero-indexed-fulltext",
        indexed_at="2026-08-10T12:00:00+08:00",
    )
    second = project_storage.register_material_items(
        writing_library,
        [
            {"item_key": "A", "title": "One", "version": 1},
            {"item_key": "B", "title": "Two", "version": 2},
        ],
    )
    assert {item["item_key"]: item["status"] for item in second["items"]} == {
        "A": "indexed",
        "B": "pending",
    }


def test_write_material_item_uses_tag_line_and_preserves_source(
    writing_library: Path,
) -> None:
    path = project_storage.write_material_item(
        writing_library,
        metadata={"item_key": "AB/CD", "title": "Example"},
        paragraphs=[
            {
                "tags": ["交换作用", "层间耦合"],
                "text": "Exact source paragraph.",
                "source_location": "第 6 页",
            }
        ],
        evidence_source="pdf-text-layer",
        indexed_at="2026-08-10T12:00:00+08:00",
    )
    text = path.read_text(encoding="utf-8")
    assert path.name == "AB_CD.md"
    assert "#交换作用 #层间耦合\nExact source paragraph." in text
    assert "来源位置：第 6 页" in text
    assert "[Example](文献片段/AB_CD.md)" in (
        writing_library / "素材库" / "文献索引.md"
    ).read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "tags", [[], ["a", "b", "c", "d"], ["#bad"], ["two words"]]
)
def test_write_material_item_rejects_invalid_tags(
    writing_library: Path, tags: list[str]
) -> None:
    with pytest.raises(ValueError):
        project_storage.write_material_item(
            writing_library,
            metadata={"item_key": "A", "title": "Example"},
            paragraphs=[
                {"tags": tags, "text": "Source", "source_location": "unknown"}
            ],
            evidence_source="zotero-indexed-fulltext",
            indexed_at="2026-08-10T12:00:00+08:00",
        )


def test_abstract_only_and_failed_states_are_persisted(writing_library: Path) -> None:
    project_storage.write_material_item(
        writing_library,
        metadata={"item_key": "A", "title": "Abstract paper", "abstract": "Original."},
        paragraphs=[],
        evidence_source="abstract-only",
        indexed_at="2026-08-10T12:00:00+08:00",
    )
    project_storage.register_material_items(
        writing_library, [{"item_key": "B", "title": "Failed", "version": 1}]
    )
    project_storage.mark_material_failed(
        writing_library, "B", "no full text", "2026-08-10T13:00:00+08:00"
    )

    state = project_storage.load_material_state(writing_library)
    statuses = {item["item_key"]: item["status"] for item in state["items"]}
    assert statuses == {"A": "abstract_only", "B": "failed"}
    assert "未据此推断正文结论" in (
        writing_library / "素材库" / "文献片段" / "A.md"
    ).read_text(encoding="utf-8")


def test_material_item_refuses_overwrite_without_reindex(writing_library: Path) -> None:
    kwargs = {
        "metadata": {"item_key": "A", "title": "One", "version": 1},
        "paragraphs": [
            {"tags": ["主题"], "text": "First.", "source_location": "p. 1"}
        ],
        "evidence_source": "zotero-indexed-fulltext",
        "indexed_at": "2026-08-10T12:00:00+08:00",
    }
    project_storage.write_material_item(writing_library, **kwargs)
    with pytest.raises(FileExistsError):
        project_storage.write_material_item(writing_library, **kwargs)

    kwargs["paragraphs"] = [
        {"tags": ["主题"], "text": "Updated.", "source_location": "p. 1"}
    ]
    project_storage.write_material_item(writing_library, reindex=True, **kwargs)
    assert "Updated." in (
        writing_library / "素材库" / "文献片段" / "A.md"
    ).read_text(encoding="utf-8")
