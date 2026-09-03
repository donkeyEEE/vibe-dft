#!/usr/bin/env python3
"""
citation-validator — parse citations from manuscript text, query Zotero for each
cited paper, retrieve abstracts, and evaluate whether each citation supports the
claim it is attached to.

This script handles the text-processing and evaluation logic. DOCX extraction
and Zotero interaction are orchestrated by the SKILL.md workflow through
liteparse and the zotero plugin respectively.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# ── citation pattern recognition ──────────────────────────────────────────

# Numeric: [1], [1,2], [1-3], [1,2,5-7]
NUMERIC_RE = re.compile(
    r"\[(?P<nums>\d+(?:\s*[-,]\s*\d+)*)\]",
)

# Author-year: (Smith et al., 2020), (Smith and Jones, 2019), (Zhang, 2021)
AUTHOR_YEAR_RE = re.compile(
    r"\((?P<auth>[A-Z][a-zA-Záéíóúàèìòùäëïöüñç\-']+(?:\s+(?:et\s+al\.|and\s+[A-Z][a-zA-Záéíóúàèìòùäëïöüñç\-']+))?),\s*(?P<year>\d{4}[a-z]?)\)",
)

# Inline author-year: Smith et al. (2020), Zhang (2021)
INLINE_AUTHOR_RE = re.compile(
    r"(?P<auth>[A-Z][a-zA-Záéíóúàèìòùäëïöüñç\-']+(?:\s+(?:et\s+al\.|and\s+[A-Z][a-zA-Záéíóúàèìòùäëïöüñç\-']+))?)\s+\((?P<year>\d{4}[a-z]?)\)",
)

# Superscript numbers (common in Nature/Science): text¹² or text¹,²
SUPERSCRIPT_RE = re.compile(
    r"[\u00B9\u00B2\u00B3\u2070\u2071\u2074\u2075\u2076\u2077\u2078\u2079]+",
)

# Combined: detect all citation markers with their positions
CITATION_PATTERNS = [
    ("numeric", NUMERIC_RE),
    ("author_year_paren", AUTHOR_YEAR_RE),
    ("inline_author_year", INLINE_AUTHOR_RE),
    ("superscript", SUPERSCRIPT_RE),
]


# ── support grading ────────────────────────────────────────────────────────

SUPPORT_GRADES = OrderedDict(
    [
        ("strong_support", "强支撑 — 论文直接验证了同一核心关系/机制/方法，结果支持该声明"),
        ("partial_support", "部分支撑 — 论文支撑声明的一部分、更窄的条件或相关模型"),
        ("background_support", "背景支撑 — 论文仅支撑领域背景或先验观察，不直接支撑该具体声明"),
        ("contradictory", "矛盾/限制 — 论文结果与该声明冲突或缩小了声明范围"),
        ("metadata_only", "仅元数据匹配 — 标题/元数据表明相关，但摘要/全文未核实，不可作为引用依据"),
        ("no_evidence", "无证据 — 检索到的摘要/全文内容与该声明无实质关联"),
    ]
)

SUPPORT_GRADE_SHORT = {
    "strong_support": "strong",
    "partial_support": "partial",
    "background_support": "background",
    "contradictory": "contradictory",
    "metadata_only": "metadata-only",
    "no_evidence": "no-evidence",
}


# ── data classes ───────────────────────────────────────────────────────────

@dataclass
class CitationRef:
    """A single citation marker found in the text."""
    id: str                          # e.g. C001
    raw_text: str                    # the raw citation text, e.g. "[1,2]" or "(Smith, 2020)"
    pattern_type: str                # numeric, author_year_paren, inline_author_year, superscript
    position: int                    # character position in paragraph
    zotero_query: str = ""           # search query for Zotero
    zotero_key: str = ""             # Zotero item key if found
    zotero_title: str = ""           # title from Zotero
    zotero_authors: str = ""         # first author + year from Zotero
    zotero_doi: str = ""             # DOI from Zotero
    abstract: str = ""               # retrieved abstract
    fulltext_snippet: str = ""       # relevant snippet from full text
    support_grade: str = ""          # one of SUPPORT_GRADE_SHORT keys
    support_reasoning: str = ""      # why this grade
    evidence_basis: str = ""         # abstract / fulltext / publisher-page / metadata-only


@dataclass
class ClaimSegment:
    """A segment of text with a claim and its citations."""
    id: str
    text: str
    claim_summary: str = ""
    citations: list[CitationRef] = field(default_factory=list)


@dataclass
class ValidationReport:
    """Complete validation report."""
    source_file: str = ""
    paragraphs: str = ""
    segments: list[ClaimSegment] = field(default_factory=list)
    total_citations: int = 0
    strong: int = 0
    partial: int = 0
    background: int = 0
    contradictory: int = 0
    metadata_only: int = 0
    no_evidence: int = 0
    not_found: int = 0
    warnings: list[str] = field(default_factory=list)


# ── citation extraction ────────────────────────────────────────────────────

def extract_citations(text: str) -> list[CitationRef]:
    """Extract all citation markers from text and return them with positions."""
    citations: list[CitationRef] = []
    seen_positions: set[int] = set()

    for pattern_type, pattern in CITATION_PATTERNS:
        for match in pattern.finditer(text):
            pos = match.start()
            if pos in seen_positions:
                continue
            seen_positions.add(pos)
            citations.append(CitationRef(
                id=f"C{len(citations) + 1:03d}",
                raw_text=match.group(0),
                pattern_type=pattern_type,
                position=pos,
            ))

    citations.sort(key=lambda c: c.position)
    for i, c in enumerate(citations):
        c.id = f"C{i + 1:03d}"
    return citations


def split_into_claim_segments(text: str, citations: list[CitationRef]) -> list[ClaimSegment]:
    """
    Split text into claim segments, each associated with its nearest citations.
    Uses a simple proximity-based approach: a citation belongs to the sentence
    or clause it appears in.
    """
    if not citations:
        return [ClaimSegment(id="S001", text=text)]

    # Protect common abbreviations from being treated as sentence boundaries.
    abbreviations = re.compile(r"(?:et al|i\.e|e\.g|vs|cf|Dr|Mr|Mrs|Ms|Prof|St|Ave|Blvd|Rd|Inc|Ltd|Jr|Sr|No)\.")
    protected = abbreviations.sub(lambda m: m.group(0).replace(".", "\x00"), text)

    # Split by sentence boundaries
    sentences = re.split(r"(?<=[.!?。！？])\s+", protected)
    sentences = [s.replace("\x00", ".") for s in sentences]
    # Drop empty fragments and artifacts from abbreviation protection.
    sentences = [s.strip() for s in sentences if s.strip()]
    # Collapse isolated abbreviations such as "et al." back into their neighbors.
    merged: list[str] = []
    for s in sentences:
        if merged and re.fullmatch(r"(?:et al|i\.e|e\.g|vs|cf)\.", s, re.IGNORECASE):
            merged[-1] = merged[-1] + " " + s
        elif s.lower() in {"et al.", "i.e.", "e.g.", "vs.", "cf."}:
            continue
        else:
            merged.append(s)
    sentences = merged
    
    # Build sentence boundary map: list of (start, end) positions in original text.
    boundaries: list[tuple[int, int]] = []
    cursor = 0
    for s in sentences:
        start = text.find(s, cursor)
        if start == -1:
            start = cursor
        end = start + len(s)
        boundaries.append((start, end))
        cursor = end

    segments: list[ClaimSegment] = []
    seg_id = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        seg_id += 1
        seg = ClaimSegment(id=f"S{seg_id:03d}", text=sentence)

        # Find citations whose position falls within this sentence's boundaries.
        seg_start, seg_end = boundaries[seg_id - 1]
        for c in citations:
            if seg_start <= c.position < seg_end:
                seg.citations.append(c)

        # Extract a claim summary
        seg.claim_summary = sentence[:200] + ("..." if len(sentence) > 200 else "")
        segments.append(seg)

    return segments


# ── Zotero query generation ────────────────────────────────────────────────

def generate_zotero_queries(citations: list[CitationRef]) -> list[CitationRef]:
    """
    Generate Zotero search queries for each citation based on pattern type.
    Numeric citations need to be mapped via a reference list (provided separately).
    Author-year citations can be searched directly.
    """
    for c in citations:
        if c.pattern_type == "author_year_paren":
            m = AUTHOR_YEAR_RE.match(c.raw_text)
            if m:
                auth = m.group("auth").replace(" et al.", "").replace(" and ", " ")
                year = m.group("year")
                c.zotero_query = f"{auth} {year}"
        elif c.pattern_type == "inline_author_year":
            m = INLINE_AUTHOR_RE.match(c.raw_text)
            if m:
                auth = m.group("auth").replace(" et al.", "").replace(" and ", " ")
                year = m.group("year")
                c.zotero_query = f"{auth} {year}"
        elif c.pattern_type == "numeric":
            c.zotero_query = f"NUMERIC:{c.raw_text}"
        elif c.pattern_type == "superscript":
            c.zotero_query = f"SUPERSCRIPT:{c.raw_text}"

    return citations


# ── support evaluation ─────────────────────────────────────────────────────

def evaluate_support(
    claim: str,
    abstract: str,
    fulltext_snippet: str = "",
    title: str = "",
) -> tuple[str, str, str]:
    """
    Evaluate whether a cited paper supports a claim.

    Returns (grade, reasoning, evidence_basis).

    This function provides a structured framework for evaluation. The actual
    evaluation is performed by the LLM agent following the SKILL.md workflow,
    which calls this function with pre-retrieved abstract/fulltext and then
    applies the grading criteria.

    When called with empty abstract/fulltext, returns metadata_only.
    """
    if not abstract and not fulltext_snippet:
        return (
            "metadata_only",
            "摘要与全文均未检索，无法判断支撑关系。请通过 Zotero 获取摘要后重新评估。",
            "metadata-only",
        )

    # Evidence basis determination
    if fulltext_snippet:
        evidence = "fulltext"
    elif abstract:
        evidence = "abstract"
    else:
        evidence = "metadata-only"

    # This is a structured template for the LLM agent to fill in.
    # The actual grade determination happens in the agent's reasoning
    # following the criteria in static/core/support-grading.md.
    return (
        "metadata_only",
        f"待评估：摘要长度={len(abstract)}字符，全文片段长度={len(fulltext_snippet)}字符。"
        f"请按 static/core/support-grading.md 的评估框架判断支撑等级。",
        evidence,
    )


def grade_to_label(grade: str) -> str:
    """Convert short grade to full Chinese label."""
    labels = {
        "strong_support": "强支撑",
        "partial_support": "部分支撑",
        "background_support": "背景支撑",
        "contradictory": "矛盾/限制",
        "metadata_only": "仅元数据",
        "no_evidence": "无证据",
    }
    return labels.get(grade, grade)


# ── report generation ──────────────────────────────────────────────────────

def generate_report(report: ValidationReport) -> str:
    """Generate a structured markdown report."""
    lines: list[str] = []
    lines.append("# 引用校验报告")
    lines.append("")
    lines.append(f"**源文件**: {report.source_file}")
    lines.append(f"**校验段落**: {report.paragraphs}")
    lines.append(f"**引用总数**: {report.total_citations}")
    lines.append("")

    # Summary statistics
    lines.append("## 支撑等级分布")
    lines.append("")
    lines.append(f"| 等级 | 数量 |")
    lines.append(f"|------|------|")
    if report.strong:
        lines.append(f"| 🟢 强支撑 | {report.strong} |")
    if report.partial:
        lines.append(f"| 🟡 部分支撑 | {report.partial} |")
    if report.background:
        lines.append(f"| 🔵 背景支撑 | {report.background} |")
    if report.contradictory:
        lines.append(f"| 🔴 矛盾/限制 | {report.contradictory} |")
    if report.metadata_only:
        lines.append(f"| ⚪ 仅元数据 | {report.metadata_only} |")
    if report.no_evidence:
        lines.append(f"| ⚫ 无证据 | {report.no_evidence} |")
    if report.not_found:
        lines.append(f"| ❓ 未找到 | {report.not_found} |")
    lines.append("")

    # Per-segment details
    for seg in report.segments:
        lines.append(f"## {seg.id}: {seg.claim_summary}")
        lines.append("")
        if not seg.citations:
            lines.append("  ⚠️ 该段未检测到引用标记。")
            lines.append("")
            continue

        for c in seg.citations:
            grade_label = grade_to_label(c.support_grade) if c.support_grade else "未评估"
            lines.append(f"### 引用 {c.id}: `{c.raw_text}`")
            lines.append("")
            lines.append(f"- **引用格式**: {c.pattern_type}")
            if c.zotero_title:
                lines.append(f"- **文献标题**: {c.zotero_title}")
            if c.zotero_authors:
                lines.append(f"- **作者/年份**: {c.zotero_authors}")
            if c.zotero_doi:
                lines.append(f"- **DOI**: [{c.zotero_doi}](https://doi.org/{c.zotero_doi})")
            if c.zotero_key:
                lines.append(f"- **Zotero Key**: `{c.zotero_key}`")
            lines.append(f"- **支撑等级**: **{grade_label}**")
            if c.support_reasoning:
                lines.append(f"- **评估依据**: {c.evidence_basis}")
                lines.append(f"- **推理**: {c.support_reasoning}")
            lines.append("")

    # Warnings
    if report.warnings:
        lines.append("## ⚠️ 风险与缺口")
        lines.append("")
        for w in report.warnings:
            lines.append(f"- {w}")
        lines.append("")

    # Recommendations
    lines.append("## 建议操作")
    lines.append("")
    if report.metadata_only > 0:
        lines.append(f"- {report.metadata_only} 条引用仅基于元数据，建议通过 Zotero 获取摘要后重新评估")
    if report.no_evidence > 0:
        lines.append(f"- {report.no_evidence} 条引用与声明无实质关联，建议删除或替换")
    if report.contradictory > 0:
        lines.append(f"- {report.contradictory} 条引用与声明矛盾，需立即核实或替换")
    if report.not_found > 0:
        lines.append(f"- {report.not_found} 条引用在 Zotero 中未找到，请检查引用列表")
    if report.partial > 0:
        lines.append(f"- {report.partial} 条引用仅部分支撑，可考虑补充更直接的文献或在文中限定声明范围")
    if report.strong == 0 and report.total_citations > 0:
        lines.append("- ⚠️ 没有引用达到强支撑等级，该段落的引用支撑可能不足")
    if report.strong == report.total_citations and report.total_citations > 0:
        lines.append("- ✅ 所有引用均达到强支撑等级，引用质量良好")
    lines.append("")

    return "\n".join(lines)


def build_report(
    source_file: str,
    paragraphs: str,
    segments: list[ClaimSegment],
) -> ValidationReport:
    """Build a ValidationReport from segments."""
    report = ValidationReport(
        source_file=source_file,
        paragraphs=paragraphs,
        segments=segments,
    )

    for seg in segments:
        for c in seg.citations:
            report.total_citations += 1
            grade = c.support_grade
            if grade == "strong_support":
                report.strong += 1
            elif grade == "partial_support":
                report.partial += 1
            elif grade == "background_support":
                report.background += 1
            elif grade == "contradictory":
                report.contradictory += 1
            elif grade == "metadata_only":
                report.metadata_only += 1
            elif grade == "no_evidence":
                report.no_evidence += 1
            else:
                report.not_found += 1

    return report


# ── CLI ────────────────────────────────────────────────────────────────────

def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="citation-validator — parse citations and evaluate support",
    )
    sub = parser.add_subparsers(dest="command")

    # extract: extract citations from text
    extract_parser = sub.add_parser("extract", help="Extract citations from text")
    extract_parser.add_argument("--text", help="Text to parse")
    extract_parser.add_argument("--text-file", help="UTF-8 text file to parse")
    extract_parser.add_argument("--json", action="store_true", help="Output JSON")

    # report: generate report from JSON mapping
    report_parser = sub.add_parser("report", help="Generate report from validation JSON")
    report_parser.add_argument("--json-file", required=True, help="Validation JSON file")
    report_parser.add_argument("--out", help="Output markdown report path")

    # grade: evaluate support for a single citation
    grade_parser = sub.add_parser("grade", help="Evaluate support for a citation")
    grade_parser.add_argument("--claim", required=True, help="Claim text")
    grade_parser.add_argument("--abstract", help="Paper abstract")
    grade_parser.add_argument("--abstract-file", help="File with paper abstract")
    grade_parser.add_argument("--title", help="Paper title")

    return parser.parse_args(argv)


def cmd_extract(args: argparse.Namespace) -> int:
    text = ""
    if args.text:
        text = args.text
    elif args.text_file:
        text = Path(args.text_file).read_text(encoding="utf-8")
    else:
        # Read from stdin
        text = sys.stdin.read()

    if not text.strip():
        print("No text provided.", file=sys.stderr)
        return 2

    citations = extract_citations(text)
    citations = generate_zotero_queries(citations)
    segments = split_into_claim_segments(text, citations)

    if args.json:
        output = {
            "text": text,
            "total_citations": len(citations),
            "segments": [
                {
                    "id": seg.id,
                    "text": seg.text,
                    "claim_summary": seg.claim_summary,
                    "citations": [
                        {
                            "id": c.id,
                            "raw_text": c.raw_text,
                            "pattern_type": c.pattern_type,
                            "zotero_query": c.zotero_query,
                        }
                        for c in seg.citations
                    ],
                }
                for seg in segments
            ],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"Text length: {len(text)} chars")
        print(f"Citations found: {len(citations)}")
        print(f"Segments: {len(segments)}")
        for seg in segments:
            print(f"\n--- {seg.id} ---")
            print(f"  Text: {seg.text[:120]}...")
            for c in seg.citations:
                print(f"  [{c.id}] {c.raw_text} ({c.pattern_type}) -> query: {c.zotero_query}")

    return 0


def cmd_report(args: argparse.Namespace) -> int:
    data = json.loads(Path(args.json_file).read_text(encoding="utf-8"))

    segments = []
    for seg_data in data.get("segments", []):
        citations = []
        for c_data in seg_data.get("citations", []):
            citations.append(CitationRef(
                id=c_data.get("id", ""),
                raw_text=c_data.get("raw_text", ""),
                pattern_type=c_data.get("pattern_type", ""),
                position=c_data.get("position", 0),
                zotero_query=c_data.get("zotero_query", ""),
                zotero_key=c_data.get("zotero_key", ""),
                zotero_title=c_data.get("zotero_title", ""),
                zotero_authors=c_data.get("zotero_authors", ""),
                zotero_doi=c_data.get("zotero_doi", ""),
                abstract=c_data.get("abstract", ""),
                fulltext_snippet=c_data.get("fulltext_snippet", ""),
                support_grade=c_data.get("support_grade", ""),
                support_reasoning=c_data.get("support_reasoning", ""),
                evidence_basis=c_data.get("evidence_basis", ""),
            ))
        segments.append(ClaimSegment(
            id=seg_data.get("id", ""),
            text=seg_data.get("text", ""),
            claim_summary=seg_data.get("claim_summary", ""),
            citations=citations,
        ))

    report = build_report(
        source_file=data.get("source_file", ""),
        paragraphs=data.get("paragraphs", ""),
        segments=segments,
    )
    report.warnings = data.get("warnings", [])

    md = generate_report(report)
    if args.out:
        Path(args.out).write_text(md, encoding="utf-8")
        print(f"Report written to {args.out}")
    else:
        print(md)

    return 0


def cmd_grade(args: argparse.Namespace) -> int:
    abstract = args.abstract or ""
    if args.abstract_file:
        abstract = Path(args.abstract_file).read_text(encoding="utf-8")

    grade, reasoning, evidence = evaluate_support(
        claim=args.claim,
        abstract=abstract,
        title=args.title or "",
    )

    result = {
        "claim": args.claim,
        "title": args.title or "",
        "abstract_length": len(abstract),
        "grade": grade,
        "grade_label": grade_to_label(grade),
        "reasoning": reasoning,
        "evidence_basis": evidence,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.command == "extract":
        return cmd_extract(args)
    elif args.command == "report":
        return cmd_report(args)
    elif args.command == "grade":
        return cmd_grade(args)
    else:
        print("Use: extract | report | grade", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
