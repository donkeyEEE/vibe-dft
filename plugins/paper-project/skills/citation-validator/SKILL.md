---
name: citation-validator
description: >-
  Validate whether citations in a Word-document manuscript paragraph
  appropriately support the claims they are attached to. Parse the DOCX,
  identify every citation marker, look up each cited paper in Zotero,
  retrieve the abstract or full text, and evaluate support level against
  the claim using a five-grade conservative framework. Use this skill when
  the user asks to check citations, verify references, audit citation
  quality, "检查引用", "核对文献", "引用是否合理", "校验引用",
  "引用支撑", "检查这段话的引用", "验证参考文献", or any request to
  examine whether a citation genuinely supports a statement in a paper.
metadata:
  version: "1.0.0"
  author: paper-project
---

# Citation Validator — Router

校验 Word 论文中指定段落的引用是否合理：识别引用标记 → Zotero 查文献 → 获取摘要/全文 → 评估支撑等级 → 输出报告。

This skill is split into two layers:

- A **static layer** under `static/core/` that holds the core principles, the six-step
  workflow, and the five-grade support evaluation framework.
- A **dynamic layer** (this file plus `manifest.yaml`) that loads the core every time
  and reaches for deeper references only when a step needs them.

Do not try to apply the citation-validation logic from memory. Always load fragments
from disk as described below.

## Routing protocol

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). Then read every file listed under `always_load`:

- `static/core/principles.md` — what the skill does, scope, boundaries, and Zotero access rules.
- `static/core/workflow.md` — the six-step workflow from DOCX parsing to final report.
- `static/core/support-grading.md` — the five-grade support evaluation framework with examples.

### 2. Parse the user request

Extract from the user's request:

- **Document path**: the .docx file to check.
- **Paragraph range**: which paragraph(s) to validate (e.g. "第3段", "段落1-5", "paragraph 3").
- **Citation style**: auto-detect from the text; if the user specifies a style, honor it.
- **Evaluation depth**: default is abstract-level; if the user asks for "深度检查" or "全文核对", go to full text for every citation.

If the document path or paragraph range is missing, ask the user once in a concise question — do not guess.

### 3. Run the workflow

Follow the six steps in `static/core/workflow.md`:

1. **Parse DOCX** — use liteparse to extract text, locate the target paragraph(s).
2. **Extract citations** — run `scripts/citation_validator.py extract --text "..." --json` to identify all citation markers.
3. **Look up in Zotero** — for each citation, search Zotero; for numeric citations, first parse the reference list to build number→paper mapping.
4. **Retrieve abstracts** — get abstract from Zotero item metadata; if insufficient, get full text snippet.
5. **Evaluate support** — for each citation, apply the five-grade framework from `static/core/support-grading.md`.
6. **Generate report** — run `scripts/citation_validator.py report --json-file ... --out ...` and present the report.

### 4. Reach for references only when needed

The files under `references/` are deep references, not defaults. Open them on demand per the `references.on_demand` table in the manifest:

- running the script with full flags → `references/script-usage.md`
- identifying complex citation patterns → `references/citation-patterns.md`
- querying Zotero for each citation → `references/zotero-integration.md`
- making final judgment when abstract is ambiguous → `references/judgment-guidelines.md`

## Output format

The final report is a Markdown file with the following structure:

1. **Header**: source file, paragraph range, total citations
2. **Support grade distribution**: summary table
3. **Per-citation detail**: each citation with grade, reasoning, evidence basis
4. **Warnings and gaps**: issues needing attention
5. **Actionable recommendations**: concrete suggestions for improvement

After generating the report, present a 2-4 sentence summary of key findings to the user along with the report path.

## Why this split

- The static layer is versioned and reviewable; the core stays small for a normal run.
- The dynamic layer keeps each invocation cheap: the script flag dump and complex
  pattern reference load only when actually needed.
- The router itself is short on purpose. Update fragments and references, not this
  file, when adding scope or evaluation criteria.
- This structure mirrors `nature-citation`, `nature-figure`, and other nature-* skills.
