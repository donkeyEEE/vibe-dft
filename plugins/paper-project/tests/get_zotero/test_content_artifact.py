from pathlib import Path
import sys


SCRIPTS = (
    Path(__file__).resolve().parents[2] / "skills" / "get-zotero" / "scripts"
)
sys.path.insert(0, str(SCRIPTS))

import zotero  # noqa: E402
from attachment_paths import ResolvedAttachment  # noqa: E402
from runtime_config import PathMappingConfig, RuntimeConfig  # noqa: E402


def runtime() -> RuntimeConfig:
    return RuntimeConfig(
        mode="native",
        host=None,
        port=23119,
        timeout_seconds=5.0,
        path_mappings=(),
        sources={
            "mode": "test",
            "host": "test",
            "port": "test",
            "timeout_seconds": "test",
        },
    )


class FakeClient:
    def __init__(self, responses: dict[str, object]) -> None:
        self.responses = responses
        self.config = runtime()

    def request(self, path: str) -> zotero.Response:
        value = self.responses[path]
        if isinstance(value, tuple):
            status, body = value
        else:
            status, body = 200, value
        return zotero.Response(
            status=status,
            headers={"Content-Type": "application/json"},
            text=zotero.json.dumps(body),
        )


PARENT = {
    "key": "ABCD1234",
    "data": {
        "itemType": "journalArticle",
        "title": "Example paper",
        "creators": [{"firstName": "Ada", "lastName": "Lovelace"}],
        "date": "2026-01-02",
        "DOI": "10.0000/example",
        "url": "https://example.test/paper",
        "abstractNote": "Original abstract",
        "publicationTitle": "Example Journal",
        "collections": ["COLL1234"],
    },
}
PDF_CHILD = {
    "key": "EFGH5678",
    "data": {
        "itemType": "attachment",
        "contentType": "application/pdf",
        "title": "Full Text PDF",
    },
}


def base_responses() -> dict[str, object]:
    return {
        "/api/users/0/items/ABCD1234": PARENT,
        "/api/users/0/items/ABCD1234/children": [PDF_CHILD],
    }


def test_indexed_text_is_written_as_artifact_without_inline_body(tmp_path: Path) -> None:
    responses = base_responses()
    responses["/api/users/0/items/EFGH5678/fulltext"] = {
        "content": "Paragraph one.\n\nParagraph two.",
        "indexedPages": 12,
        "totalPages": 15,
    }

    manifest = zotero.build_content_artifact(
        FakeClient(responses), "ABCD1234", "auto", tmp_path
    )

    assert manifest["schema_version"] == 1
    assert manifest["item_key"] == "ABCD1234"
    assert manifest["metadata"]["doi"] == "10.0000/example"
    assert manifest["content"] == {
        "kind": "text-file",
        "path": str((tmp_path / "EFGH5678.txt").resolve()),
        "source": "zotero-indexed-fulltext",
        "attachment_key": "EFGH5678",
        "indexed_pages": 12,
        "total_pages": 15,
    }
    assert (tmp_path / "EFGH5678.txt").read_text() == (
        "Paragraph one.\n\nParagraph two."
    )
    assert "Paragraph one" not in zotero.json.dumps(manifest)


def test_pdf_mode_returns_resolved_read_only_artifact(
    tmp_path: Path, monkeypatch
) -> None:
    responses = base_responses()
    responses["/api/users/0/items/EFGH5678/file/view/url"] = (
        200,
        "file:///papers/Example.pdf",
    )
    pdf = tmp_path / "Example.pdf"
    pdf.write_bytes(b"%PDF-1.4")
    monkeypatch.setattr(
        zotero,
        "resolve_attachment_path",
        lambda raw, mode, mappings: ResolvedAttachment(pdf, "native"),
    )

    manifest = zotero.build_content_artifact(
        FakeClient(responses), "ABCD1234", "pdf", tmp_path / "artifacts"
    )

    assert manifest["content"] == {
        "kind": "pdf-file",
        "path": str(pdf.resolve()),
        "source": "local-pdf",
        "attachment_key": "EFGH5678",
    }


def test_missing_pdf_attachment_degrades_to_metadata_only(tmp_path: Path) -> None:
    responses = base_responses()
    responses["/api/users/0/items/ABCD1234/children"] = []

    manifest = zotero.build_content_artifact(
        FakeClient(responses), "ABCD1234", "auto", tmp_path
    )

    assert manifest["content"] == {
        "kind": "metadata-only",
        "source": "metadata-abstract-only",
    }


def test_required_content_mode_returns_error_without_pdf_attachment(
    tmp_path: Path,
) -> None:
    responses = base_responses()
    responses["/api/users/0/items/ABCD1234/children"] = []

    for mode in ("indexed-text", "pdf"):
        manifest = zotero.build_content_artifact(
            FakeClient(responses), "ABCD1234", mode, tmp_path / mode
        )

        assert manifest["content"]["kind"] == "error"
        assert manifest["content"]["code"] == "pdf-attachment-not-found"
        assert manifest["content"]["next_step"]


def test_parser_exposes_content_modes() -> None:
    args = zotero.build_parser().parse_args(
        ["content", "ABCD1234", "--mode", "indexed-text", "--out-dir", "/tmp/out"]
    )

    assert args.command == "content"
    assert args.content_mode == "indexed-text"
    assert args.out_dir == "/tmp/out"
