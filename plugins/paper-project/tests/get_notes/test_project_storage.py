from pathlib import Path
import sys

import pytest


SCRIPTS = (
    Path(__file__).resolve().parents[2] / "skills" / "get-notes" / "scripts"
)
sys.path.insert(0, str(SCRIPTS))

import research_note_storage as note_storage  # noqa: E402
import writing_library_storage as library_storage  # noqa: E402


def test_selected_collection_resolves_note_path_under_existing_research_line(
    tmp_path: Path,
) -> None:
    line = tmp_path / "line"
    line.mkdir()
    mapping = note_storage.load_mapping(tmp_path, "line")
    note_storage.select_collection(mapping, "COLL1234", "磁性材料/Fe3GaTe2")
    note_storage.save_mapping(tmp_path, "line", mapping)

    paths = note_storage.resolve_note_paths(
        tmp_path, "line", "ITEM1234", ["OTHER", "COLL1234"]
    )

    assert paths == [
        line
        / "06-文献笔记"
        / "01-单篇文献"
        / "磁性材料"
        / "Fe3GaTe2"
        / "ITEM1234.md"
    ]


def test_note_path_requires_at_least_one_selected_collection(tmp_path: Path) -> None:
    (tmp_path / "line").mkdir()

    with pytest.raises(note_storage.NoSelectedCollectionError):
        note_storage.resolve_note_paths(tmp_path, "line", "ITEM1234", ["COLL1234"])


def test_material_library_records_success_and_failure_without_deleting_output(
    tmp_path: Path,
) -> None:
    manuscript = tmp_path / "paper.md"
    manuscript.write_text("draft")
    root = library_storage.writing_library_for_manuscript(manuscript)
    library_storage.initialize_writing_library(
        root,
        mode="standalone",
        source_manuscript=manuscript,
        collection_key="COLL1234",
        collection_path="Project/Papers",
    )
    library_storage.register_material_items(
        root, [{"item_key": "ITEM1234", "title": "Paper", "version": 1}]
    )
    output = library_storage.write_material_item(
        root,
        metadata={"item_key": "ITEM1234", "title": "Paper", "version": 1},
        paragraphs=[
            {"tags": ["方法"], "text": "Source paragraph.", "source_location": "p. 2"}
        ],
        evidence_source="zotero-indexed-fulltext",
        indexed_at="2026-09-11T20:00:00+08:00",
    )

    library_storage.mark_material_failed(
        root, "ITEM1234", "temporary read failure", "2026-09-11T20:01:00+08:00"
    )

    assert output.is_file()
    entry = library_storage.load_material_state(root)["items"][0]
    assert entry["status"] == "failed"
    assert entry["output_path"] == "素材库/文献片段/ITEM1234.md"
