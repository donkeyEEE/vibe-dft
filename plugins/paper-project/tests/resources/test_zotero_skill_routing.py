from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_raw_evidence_consumers_route_to_get_zotero() -> None:
    for relative in (
        "plugins/paper-project/skills/citation-validator/references/zotero-integration.md",
        "plugins/paper-project/skills/citation-validator/static/core/principles.md",
        "plugins/paper-project/skills/citation-validator/static/core/workflow.md",
    ):
        text = read(relative)
        assert "get-zotero" in text, relative
        assert "zo2notes" not in text.lower(), relative
        assert "skills/zotero/scripts/zotero.py" not in text, relative
        assert "/api/users/0" not in text, relative


def test_citation_validator_validates_content_artifact_contract() -> None:
    text = read(
        "plugins/paper-project/skills/citation-validator/references/zotero-integration.md"
    )
    for field in ("schema_version", "item_key", "content.kind"):
        assert field in text
    for kind in ("text-file", "pdf-file", "metadata-only", "error"):
        assert kind in text


def test_get_notes_routes_acquisition_to_get_zotero() -> None:
    relative = "plugins/paper-project/skills/get-notes/SKILL.md"
    text = read(relative)
    assert "get-zotero" in text
    assert "zo2notes" not in text.lower()


def test_public_navigation_has_no_retired_zo2notes_entrypoint() -> None:
    for relative in (
        "plugins/paper-project/README.md",
        "plugins/paper-project/.codex-plugin/plugin.json",
    ):
        assert "zo2notes" not in read(relative).lower(), relative
