from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "cards" / "ontology"
EXPECTED_COUNT = 40
FRONTMATTER_KEYS = {"name", "type", "tags", "updated_at"}


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"missing frontmatter: {path}"
    block = text.split("---\n", 2)[1]
    fields = {}
    for line in block.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


def test_ontology_cards_are_indexed_and_well_formed():
    cards = sorted(ONTOLOGY.glob("*.md"))
    index = ONTOLOGY / "INDEX.md"
    cards.remove(index)
    assert len(cards) == EXPECTED_COUNT
    index_text = index.read_text(encoding="utf-8")

    for card in cards:
        fields = parse_frontmatter(card)
        assert set(fields) == FRONTMATTER_KEYS
        assert fields["name"] == card.stem
        assert len(re.findall(rf"\({re.escape(card.name)}\)", index_text)) == 1


def test_primary_index_links_ontology_index():
    primary = (ROOT / "cards" / "INDEX.md").read_text(encoding="utf-8")
    assert "[ontology/INDEX.md](ontology/INDEX.md)" in primary
