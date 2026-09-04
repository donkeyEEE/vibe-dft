from pathlib import Path


ROOT = Path(__file__).parents[2] / "knowledge"
CARDS = ROOT / "cards"
EXPECTED_GENERAL_CARD_COUNT = 31


def test_general_card_inventory_and_index_resolution() -> None:
    """Catch a partial migration or an orphaned formal general card."""
    cards = sorted((CARDS / "atoms").glob("*.md"))
    assert len(cards) == EXPECTED_GENERAL_CARD_COUNT
    index = (CARDS / "INDEX.md").read_text(encoding="utf-8")
    for card in cards:
        assert f"`{card.stem}`" in index


def test_formal_indexes_never_route_to_candidates() -> None:
    """Catch draft content becoming discoverable through a formal index."""
    assert "candidates/" not in (CARDS / "INDEX.md").read_text(encoding="utf-8")
