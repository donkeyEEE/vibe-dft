from pathlib import Path
import re


ROOT = Path(__file__).parents[1]
CANDIDATES = ROOT / "candidates/cards/calc-project"


def _frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    assert match, f"missing candidate frontmatter: {path}"
    return match.group(1)


def test_calc_track_migration_creates_twelve_indexed_candidate_cards() -> None:
    """Catch losing a historical track or exposing it without candidate indexing."""
    cards = sorted(CANDIDATES.glob("TRK-*.md"))
    assert len(cards) == 12
    index = (CANDIDATES / "INDEX.md").read_text(encoding="utf-8")
    for card in cards:
        assert card.name in index


def test_calc_candidate_cards_keep_identity_evidence_and_candidate_status() -> None:
    """Catch migrated tracks being mistaken for formally admitted cards."""
    cards = tuple(CANDIDATES.glob("TRK-*.md"))
    assert cards
    for card in cards:
        frontmatter = _frontmatter(card)
        assert f"name: {card.stem}" in frontmatter
        assert "type: calc-experience-candidate" in frontmatter
        assert "source_plugin: calc-project" in frontmatter
        assert "status: candidate" in frontmatter
        assert "updated_at: 2026-08-18" in frontmatter
        body = card.read_text(encoding="utf-8")
        assert any(heading in body for heading in ("## Problem", "## Status", "## State"))
        assert len(re.findall(r"^## ", body, flags=re.MULTILINE)) >= 2


def test_formal_indexes_do_not_expose_calc_candidates() -> None:
    """Catch candidate track IDs leaking into formal discovery paths."""
    formal = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (
            ROOT / "cards/INDEX.md",
            ROOT / "cards/physics/PHYSICS_INDEX.md",
            ROOT / "templates/INDEX.md",
        )
    )
    assert "candidates/cards/calc-project" not in formal
