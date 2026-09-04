from pathlib import Path


ROOT = Path(__file__).resolve().parents[2] / "knowledge"


def test_calc_knowledge_exposes_formal_entrypoints() -> None:
    assert (ROOT / "CONSUMER_CONTRACT.md").is_file()
    assert (ROOT / "cards/INDEX.md").is_file()
    assert (ROOT / "templates/INDEX.md").is_file()


def test_consumer_contract_excludes_nonformal_content_and_fails_open() -> None:
    contract = (ROOT / "CONSUMER_CONTRACT.md").read_text(encoding="utf-8")
    for phrase in (
        "must not read or search",
        "`candidates/`",
        "`incubating/`",
        "smallest relevant",
        "warn and continue",
    ):
        assert phrase in contract
