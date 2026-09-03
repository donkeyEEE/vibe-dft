from pathlib import Path


ROOT = Path(__file__).parents[1]
CARDS = ROOT / "cards"
EXPECTED_GENERAL_CARD_COUNT = 31


def test_general_card_inventory_and_index_resolution() -> None:
    """Catch a partial migration or an orphaned formal general card."""
    cards = sorted((CARDS / "atoms").glob("*.md"))
    assert len(cards) == EXPECTED_GENERAL_CARD_COUNT
    index = (CARDS / "INDEX.md").read_text(encoding="utf-8")
    for card in cards:
        assert f"`{card.stem}`" in index


def test_physics_index_resolves_every_formal_card() -> None:
    """Catch formal physics cards omitted from their authoritative index."""
    index = (CARDS / "physics/PHYSICS_INDEX.md").read_text(encoding="utf-8")
    cards = [
        card
        for category in ("concepts", "phenomena", "theories-and-models")
        for card in (CARDS / "physics" / category).glob("phys-*.md")
    ]
    assert cards
    for card in cards:
        assert len([line for line in index.splitlines() if card.name in line]) == 1


def test_formal_indexes_never_route_to_candidates() -> None:
    """Catch draft content becoming discoverable through a formal index."""
    for index_path in (CARDS / "INDEX.md", CARDS / "physics/PHYSICS_INDEX.md"):
        assert "candidates/" not in index_path.read_text(encoding="utf-8")
