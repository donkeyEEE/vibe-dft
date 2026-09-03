#!/usr/bin/env python3
"""Tests for project-local Zo2Notes note storage."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parents[3] / "skills" / "zo2notes" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import project_storage


def _existing_project_root(tmp_path: Path, research_line: str = "Fe3GaTe2") -> Path:
    (tmp_path / research_line).mkdir(parents=True)
    return tmp_path


def test_sanitize_path_component() -> None:
    assert project_storage.sanitize_path_component("Fe3GeTe2") == "Fe3GeTe2"
    assert project_storage.sanitize_path_component("a/b:c?d") == "a_b_c_d"
    assert project_storage.sanitize_path_component("  .  ") == "untitled"
    assert project_storage.sanitize_path_component("..") == "untitled"
    assert project_storage.sanitize_path_component("DMFT 方法") == "DMFT 方法"


def test_save_and_load_mapping_at_project_research_line_path(tmp_path: Path) -> None:
    project_root = _existing_project_root(tmp_path)
    mapping = {"version": 1, "selected_collections": []}
    project_storage.select_collection(mapping, "CHILD", "磁性材料/Fe3GeTe2")

    project_storage.save_mapping(project_root, "Fe3GaTe2", mapping)

    assert project_storage.load_mapping(project_root, "Fe3GaTe2") == mapping
    assert mapping["selected_collections"] == [
        {
            "zotero_collection_key": "CHILD",
            "zotero_path": "磁性材料/Fe3GeTe2",
            "project_path": "磁性材料/Fe3GeTe2",
        }
    ]
    assert project_storage.mapping_path(project_root, "Fe3GaTe2") == (
        project_root / "Fe3GaTe2" / "06-文献笔记" / "zotero-project-map.yaml"
    )


def test_resolve_note_paths_creates_one_path_for_each_selected_membership(
    tmp_path: Path,
) -> None:
    project_root = _existing_project_root(tmp_path)
    project_storage.save_mapping(
        project_root,
        "Fe3GaTe2",
        {
            "version": 1,
            "selected_collections": [
                {
                    "zotero_collection_key": "MAGNETISM",
                    "zotero_path": "磁性材料/Fe3GaTe2",
                    "project_path": "磁性材料/Fe3GaTe2",
                },
                {
                    "zotero_collection_key": "DMFT",
                    "zotero_path": "强关联/DMFT",
                    "project_path": "强关联/DMFT",
                },
            ],
        },
    )

    paths = project_storage.resolve_note_paths(
        project_root, "Fe3GaTe2", "ABCD1234", ["DMFT", "MAGNETISM"]
    )

    assert paths == [
        project_root
        / "Fe3GaTe2"
        / "06-文献笔记"
        / "01-单篇文献"
        / "磁性材料"
        / "Fe3GaTe2"
        / "ABCD1234.md",
        project_root
        / "Fe3GaTe2"
        / "06-文献笔记"
        / "01-单篇文献"
        / "强关联"
        / "DMFT"
        / "ABCD1234.md",
    ]
    assert all(path.parent.exists() for path in paths)


def test_resolve_note_paths_rejects_divergent_persisted_project_path(tmp_path: Path) -> None:
    project_root = _existing_project_root(tmp_path)
    project_storage.save_mapping(
        project_root,
        "Fe3GaTe2",
        {
            "version": 1,
            "selected_collections": [
                {
                    "zotero_collection_key": "PRIMARY",
                    "zotero_path": "磁性材料/Fe3GaTe2",
                    "project_path": "DMFT",
                }
            ],
        },
    )

    with pytest.raises(project_storage.InvalidCollectionMappingError):
        project_storage.resolve_note_paths(project_root, "Fe3GaTe2", "ABCD1234", ["PRIMARY"])


def test_resolve_note_paths_ignores_unselected_memberships(tmp_path: Path) -> None:
    project_root = _existing_project_root(tmp_path)
    project_storage.save_mapping(
        project_root,
        "Fe3GaTe2",
        {
            "version": 1,
            "selected_collections": [
                {
                    "zotero_collection_key": "PRIMARY",
                    "zotero_path": "磁性材料",
                    "project_path": "磁性材料",
                }
            ],
        },
    )

    paths = project_storage.resolve_note_paths(
        project_root, "Fe3GaTe2", "ABCD1234", ["NOT_SELECTED", "PRIMARY"]
    )

    assert paths == [
        project_root / "Fe3GaTe2" / "06-文献笔记" / "01-单篇文献" / "磁性材料" / "ABCD1234.md"
    ]


def test_resolve_note_paths_rejects_items_without_selected_memberships(tmp_path: Path) -> None:
    project_root = _existing_project_root(tmp_path)
    project_storage.save_mapping(
        project_root,
        "Fe3GaTe2",
        {
            "version": 1,
            "selected_collections": [
                {
                    "zotero_collection_key": "PRIMARY",
                    "zotero_path": "磁性材料",
                    "project_path": "磁性材料",
                },
                {
                    "zotero_collection_key": "SECONDARY",
                    "zotero_path": "DMFT",
                    "project_path": "DMFT",
                },
            ],
        },
    )

    with pytest.raises(project_storage.NoSelectedCollectionError):
        project_storage.resolve_note_paths(
            project_root, "Fe3GaTe2", "ABCD1234", ["NOT_SELECTED"]
        )

    assert not (
        project_root / "Fe3GaTe2" / "06-文献笔记" / "01-单篇文献" / "磁性材料" / "ABCD1234.md"
    ).exists()
    assert not (
        project_root / "Fe3GaTe2" / "06-文献笔记" / "01-单篇文献" / "DMFT" / "ABCD1234.md"
    ).exists()


def test_save_mapping_rejects_missing_project_root_without_creating_it(tmp_path: Path) -> None:
    project_root = tmp_path / "missing-project"

    with pytest.raises(project_storage.ProjectStoragePathError):
        project_storage.save_mapping(
            project_root, "Fe3GaTe2", {"version": 1, "selected_collections": []}
        )

    assert not project_root.exists()


def test_resolve_note_paths_rejects_missing_nested_research_line_without_creating_it(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()

    with pytest.raises(project_storage.ProjectStoragePathError):
        project_storage.resolve_note_paths(
            project_root, "current/Fe3GaTe2", "ABCD1234", ["PRIMARY"]
        )

    assert not (project_root / "current").exists()


@pytest.mark.parametrize("research_line", ["", "   ", ".", "/tmp/outside", "../outside"])
def test_rejects_unsafe_research_line_without_creating_literature_directories(
    tmp_path: Path, research_line: str
) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()

    with pytest.raises(project_storage.ProjectStoragePathError):
        project_storage.save_mapping(
            project_root, research_line, {"version": 1, "selected_collections": []}
        )

    assert not (project_root / "06-文献笔记").exists()
    assert not (tmp_path / "outside").exists()


def test_existing_nested_research_line_hosts_literature_paths(tmp_path: Path) -> None:
    project_root = _existing_project_root(tmp_path, "current/Fe3GaTe2")
    project_storage.save_mapping(
        project_root,
        "current/Fe3GaTe2",
        {
            "version": 1,
            "selected_collections": [
                {"zotero_collection_key": "PRIMARY", "zotero_path": "磁性材料"}
            ],
        },
    )

    paths = project_storage.resolve_note_paths(
        project_root, "current/Fe3GaTe2", "ABCD1234", ["PRIMARY"]
    )

    assert paths == [
        project_root
        / "current"
        / "Fe3GaTe2"
        / "06-文献笔记"
        / "01-单篇文献"
        / "磁性材料"
        / "ABCD1234.md"
    ]


def test_initialize_standalone_writing_library_beside_manuscript(
    tmp_path: Path,
) -> None:
    manuscript = tmp_path / "paper.docx"
    manuscript.write_bytes(b"original")

    root = project_storage.writing_library_for_manuscript(manuscript)
    state = project_storage.initialize_writing_library(
        root,
        mode="standalone",
        source_manuscript=manuscript,
        collection_key="COLL1",
        collection_path="论文素材",
    )

    assert root == tmp_path / "论文写作库"
    assert (root / "素材库" / "文献片段").is_dir()
    assert (root / "风格笔记" / "writing-style.md").read_text(
        encoding="utf-8"
    ) == project_storage.EMPTY_STYLE_NOTE
    assert (root / "草稿" / "00-原稿" / "paper.docx").read_bytes() == b"original"
    assert (root / "草稿" / "01-工作稿" / "paper.docx").read_bytes() == b"original"
    assert state["mode"] == "standalone"
    assert state["selected_collection"]["key"] == "COLL1"


def test_research_line_writing_library_requires_existing_line(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()

    with pytest.raises(project_storage.ProjectStoragePathError):
        project_storage.writing_library_for_research_line(project, "missing")


def test_reinitialization_preserves_managed_original(tmp_path: Path) -> None:
    manuscript = tmp_path / "paper.md"
    manuscript.write_text("v1", encoding="utf-8")
    root = project_storage.writing_library_for_manuscript(manuscript)
    project_storage.initialize_writing_library(
        root,
        mode="standalone",
        source_manuscript=manuscript,
        collection_key="C",
        collection_path="素材",
    )

    manuscript.write_text("v2", encoding="utf-8")
    with pytest.raises(FileExistsError):
        project_storage.initialize_writing_library(
            root,
            mode="standalone",
            source_manuscript=manuscript,
            collection_key="C",
            collection_path="素材",
        )

    assert (root / "草稿" / "00-原稿" / "paper.md").read_text(
        encoding="utf-8"
    ) == "v1"
