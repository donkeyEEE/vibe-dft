from pathlib import Path

import yaml


PLUGIN = Path(__file__).resolve().parents[2]
SKILLS = PLUGIN / "skills"
GET_ZOTERO = SKILLS / "get-zotero"
GET_NOTES = SKILLS / "get-notes"


def policy(skill: Path) -> bool:
    document = yaml.safe_load((skill / "agents/openai.yaml").read_text())
    return document["policy"]["allow_implicit_invocation"]


def test_split_skills_exist_without_zo2notes_compatibility_entrypoint() -> None:
    assert (GET_ZOTERO / "SKILL.md").is_file()
    assert (GET_NOTES / "SKILL.md").is_file()
    assert not (SKILLS / "zo2notes").exists()
    assert policy(GET_ZOTERO) is True
    assert policy(GET_NOTES) is True


def test_get_zotero_owns_only_acquisition_resources() -> None:
    expected = {
        "scripts/zotero.py",
        "scripts/runtime_config.py",
        "scripts/attachment_paths.py",
        "references/configuration.md",
        "references/local-api-routes.md",
        "references/troubleshooting.md",
        "references/pdf-evidence-strategy.md",
    }
    for relative in expected:
        assert (GET_ZOTERO / relative).is_file(), relative
    assert not (GET_ZOTERO / "scripts/project_storage.py").exists()
    assert not (GET_ZOTERO / "references/论文精读模板.md").exists()


def test_get_notes_owns_storage_and_note_resources() -> None:
    expected = {
        "scripts/research_note_storage.py",
        "scripts/writing_library_storage.py",
        "scripts/_storage_support.py",
        "references/writing-material-library.md",
        "references/研究问题卡片模板.md",
        "references/论文精读模板.md",
    }
    for relative in expected:
        assert (GET_NOTES / relative).is_file(), relative
    assert not (GET_NOTES / "scripts/zotero.py").exists()
    assert not (GET_NOTES / "scripts/project_storage.py").exists()
    assert not (GET_NOTES / "references/configuration.md").exists()


def test_get_notes_consumes_content_artifacts_without_direct_zotero_access() -> None:
    text = (GET_NOTES / "SKILL.md").read_text()
    assert "skills/get-zotero/scripts/zotero.py content" in text
    for kind in ("text-file", "pdf-file", "metadata-only", "error"):
        assert kind in text
    assert "scripts/runtime_config.py" not in text
    assert "scripts/attachment_paths.py" not in text
    assert "/api/users/0" not in text


def test_get_zotero_documents_the_versioned_artifact_contract() -> None:
    text = (GET_ZOTERO / "SKILL.md").read_text()
    assert "schema_version" in text
    assert "--mode {auto,indexed-text,pdf}" in text
    assert "不生成研究笔记" in text
    for kind in ("text-file", "pdf-file", "metadata-only", "error"):
        assert kind in text
