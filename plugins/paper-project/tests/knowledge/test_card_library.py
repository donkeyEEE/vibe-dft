from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[2]
SHARED = PLUGIN / "resources" / "paper-writing"
POLISHING = PLUGIN / "skills" / "prl-polishing" / "references" / "paper-writing"
FIGURE = PLUGIN / "skills" / "prl-figure" / "references" / "paper-writing"

EXPECTED_SHARED = {
    "write-terminology-ledger.md",
    "write-prl-model-to-validation-pairing.md",
    "write-prl-figure-prerequisite-signature-consequence.md",
    "write-prl-quantitative-claim-with-criterion.md",
    "write-prl-main-text-supplement-evidence-allocation.md",
    "write-prl-prediction-condition-observable-bridge.md",
    "write-prl-mechanism-control-comparator.md",
    "write-prl-computational-sensitivity-as-result.md",
}

EXPECTED_POLISHING = {
    "journal-physical-review-data-availability.md",
    "journal-physical-review-reference-obligations.md",
    "journal-prl-abstract.md",
    "journal-prl-letter-length.md",
    "journal-prl-run-in-headings.md",
    "journal-prl-title-style.md",
    "meta-ai-writing-boundaries.md",
    "write-attribute-intellectual-debt.md",
    "write-citation-scope.md",
    "write-cite-primary-source.md",
    "write-paper-type-taxonomy.md",
    "write-prl-claim-evidence-consequence-sequence.md",
    "write-prl-effective-model-assumption-boundary.md",
    "write-reader-question-sequence.md",
}

EXPECTED_FIGURE = {
    "journal-physical-review-figure-preparation.md",
    "journal-physical-review-supplemental-material.md",
}


def markdown_files(root: Path) -> set[str]:
    return {path.name for path in root.glob("*.md") if path.name != "README.md"}


def test_active_paper_resources_have_one_declared_owner() -> None:
    """Catch missing, duplicated, or accidentally retained paper resources."""
    assert markdown_files(SHARED) == EXPECTED_SHARED
    assert markdown_files(POLISHING) == EXPECTED_POLISHING
    assert markdown_files(FIGURE) == EXPECTED_FIGURE


def test_shared_paper_resources_declare_real_consumers() -> None:
    """Catch a plugin-shared source becoming an ownerless resource dump."""
    declaration = (SHARED / "README.md").read_text(encoding="utf-8")
    assert "prl-polishing" in declaration
    assert "prl-figure" in declaration
    assert "paper2ppt" in declaration


def test_retained_paper_resources_keep_card_metadata() -> None:
    """Catch a move that strips the evidence-card identity and provenance."""
    for root in (SHARED, POLISHING, FIGURE):
        for resource in root.glob("*.md"):
            if resource.name == "README.md":
                continue
            text = resource.read_text(encoding="utf-8")
            assert text.startswith("---\n")
            assert "\nname:" in text
            assert "\ntype:" in text
