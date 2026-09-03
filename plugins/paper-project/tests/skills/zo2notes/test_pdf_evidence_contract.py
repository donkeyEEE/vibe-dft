#!/usr/bin/env python3
"""Contract tests for Zo2Notes PDF evidence routing."""

from __future__ import annotations

from pathlib import Path


SKILL_ROOT = Path(__file__).parents[3] / "skills" / "zo2notes"


def test_skill_routes_pdf_evidence_through_reference() -> None:
    skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

    assert "references/pdf-evidence-strategy.md" in skill
    assert "Zotero indexed full text" in skill
    assert "显式关闭 OCR" in skill
    assert "扫描件或损坏文本层才启用 OCR" in skill


def test_pdf_strategy_preserves_source_priority_and_project_boundary() -> None:
    strategy = (SKILL_ROOT / "references" / "pdf-evidence-strategy.md").read_text(
        encoding="utf-8"
    )

    assert strategy.index("Zotero highlights") < strategy.index("Zotero indexed full text")
    assert "--format json --no-ocr" in strategy
    assert "OCR is a fallback" in strategy
    assert "do not copy it into the project" in strategy
    assert "Do not scan Zotero storage" in strategy


def test_note_template_declares_pdf_evidence_modes() -> None:
    template = (SKILL_ROOT / "references" / "论文精读模板.md").read_text(
        encoding="utf-8"
    )

    assert 'source_coverage:\n  - "zotero-indexed-fulltext"' in template
    assert "local-pdf-text-layer" in template
    assert "local-pdf-visual-check" in template
    assert "local-pdf-ocr" in template
