from pathlib import Path


ROOT = Path(__file__).parents[2] / "knowledge"


def test_paper_knowledge_exposes_formal_entrypoints() -> None:
    """Catch dropping plugin-local paper knowledge entrypoints."""
    assert (ROOT / "CONSUMER_CONTRACT.md").is_file()
    assert (ROOT / "cards/INDEX.md").is_file()


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
