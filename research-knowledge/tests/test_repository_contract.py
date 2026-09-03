from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_repository_is_content_only_and_exposes_formal_entrypoints() -> None:
    """Catch packaging this content store as a plugin or dropping entrypoints."""
    assert not (ROOT / ".codex-plugin").exists()
    assert (ROOT / "CONSUMER_CONTRACT.md").is_file()
    assert (ROOT / "cards/INDEX.md").is_file()
    assert (ROOT / "templates/INDEX.md").is_file()


def test_consumer_contract_excludes_candidates_and_requires_index_discovery() -> None:
    """Catch consumers being allowed to bypass formal indexes or read drafts."""
    contract = (ROOT / "CONSUMER_CONTRACT.md").read_text(encoding="utf-8")
    for phrase in (
        "must not read or search `candidates/`",
        "formal index",
        "smallest relevant",
        "warn and continue",
        "working tree",
    ):
        assert phrase in contract
