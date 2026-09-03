# citation_validator.py 脚本用法

## 子命令概览

| 命令 | 用途 |
|------|------|
| `extract` | 从文本中提取引用标记 |
| `report` | 从 JSON 生成 Markdown 报告 |
| `grade` | 评估单条引用支撑等级 |

## extract — 提取引用标记

```bash
python3 scripts/citation_validator.py extract \
  --text "段落文本..." \
  --json
```

### 参数

| 参数 | 说明 |
|------|------|
| `--text TEXT` | 直接传入文本 |
| `--text-file PATH` | 从 UTF-8 文件读取 |
| `--json` | 输出 JSON（供后续步骤使用） |

### JSON 输出格式

```json
{
  "text": "原始段落文本",
  "total_citations": 3,
  "segments": [
    {
      "id": "S001",
      "text": "句子文本...",
      "claim_summary": "前200字...",
      "citations": [
        {
          "id": "C001",
          "raw_text": "[1,2]",
          "pattern_type": "numeric",
          "zotero_query": "NUMERIC:[1,2]"
        }
      ]
    }
  ]
}
```

## report — 生成报告

```bash
python3 scripts/citation_validator.py report \
  --json-file /tmp/citation_validation.json \
  --out /tmp/citation_report.md
```

### JSON 输入格式

在 extract 输出的基础上，补充每条引用的 Zotero 信息和评估结果：

```json
{
  "source_file": "paper.docx",
  "paragraphs": "3-5",
  "segments": [
    {
      "id": "S001",
      "text": "...",
      "claim_summary": "...",
      "citations": [
        {
          "id": "C001",
          "raw_text": "[1]",
          "pattern_type": "numeric",
          "zotero_query": "Smith 2020",
          "zotero_key": "ABC123",
          "zotero_title": "Title of paper",
          "zotero_authors": "Smith et al., 2020",
          "zotero_doi": "10.1234/example",
          "abstract": "Abstract text...",
          "fulltext_snippet": "Relevant snippet...",
          "support_grade": "strong_support",
          "support_reasoning": "论文直接验证了...",
          "evidence_basis": "abstract"
        }
      ]
    }
  ],
  "warnings": ["引用 [3] 在 Zotero 中未找到"]
}
```

## grade — 单条评估

```bash
python3 scripts/citation_validator.py grade \
  --claim "Fe₃GeTe₂ 的居里温度随 Fe 空位浓度增加而降低" \
  --abstract "We studied the effect of Fe vacancies..." \
  --title "Effect of Fe vacancies on Curie temperature in Fe₃GeTe₂"
```

输出 JSON 包含 grade、grade_label、reasoning、evidence_basis。

## 批量处理

当需要校验多个段落时：

1. 对每个段落运行 `extract`，合并 JSON
2. 批量查询 Zotero（注意不要重复查询同一篇文献）
3. 逐条评估支撑等级
4. 运行 `report` 生成统一报告
