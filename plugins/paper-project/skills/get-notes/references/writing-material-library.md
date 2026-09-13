# 论文素材库契约

## 入口与位置

开始前让用户明确指定 exactly one Zotero collection。展示 collection 的名称、路径和 key，得到确认后才创建文件或枚举条目。Zotero 始终只读。

- 已有计算研究线：`<project-root>/<research-line>/07-论文写作库/`
- 只有论文文件：`<manuscript-parent>/论文写作库/`

调用 `scripts/writing_library_storage.py` 中的定位和初始化函数创建统一结构：

```text
<writing-library>/
├── writing-project.yaml
├── 素材库/
│   ├── zotero-library.yaml
│   ├── 文献索引.md
│   └── 文献片段/<item-key>.md
├── 风格笔记/writing-style.md
└── 草稿/
    ├── 00-原稿/
    ├── 01-工作稿/
    └── 02-已确认版本/
```

外部论文文件不移动、不覆盖。`00-原稿` 的首次副本不可覆盖，`01-工作稿` 是后续修改对象。

## Collection 处理

只处理所选 collection 返回的父级文献条目，不把 attachment、annotation 或独立 note 当成文献。先把所有父条目登记到 `zotero-library.yaml`，再逐一处理，以便中断后恢复。

状态含义：

- `pending`：尚未完成，或 Zotero version 已变化；
- `indexed`：已有可用全文段落索引；
- `abstract_only`：没有可用全文，只保存题录与原始摘要；
- `failed`：本轮读取失败，保留错误与尝试时间，之后可重试。

后续运行只处理新增、变化、`pending`、`failed` 或用户明确要求重新索引的条目。不要覆盖未变化的 `indexed` 文件。显式重新索引使用 `reindex=True`，并只在新文件成功写入后更新状态。

## 取证顺序

取得题名、作者、年份、刊物、DOI、URL、摘要、children 和 indexed full text。正文证据按以下顺序：

1. Zotero indexed full text；
2. annotations/highlights 作为补充；
3. 只有文本不可用或必须核验页码、图、表、公式时，才定向解析必要 PDF 页面。

PDF、OCR、截图和全文临时文件留在临时目录，不复制进论文写作库。

## 每篇文献的 Markdown

每篇文献写入 `素材库/文献片段/<item-key>.md`。保留原文自然段，不改写、不翻译。每个保留段落前必须有单独一行的 1–3 个主题标签：

```markdown
---
item_key: ABCD1234
title: Example
indexed_at: 2026-08-10T12:00:00+08:00
evidence_source: zotero-indexed-fulltext
---

#段落主题 #第二主题
原文段落保持不变。

来源位置：第 6 页
```

标签使用紧凑的 `#段落主题` 格式，不含空格；一段最多三个。标签只描述该段主题，不得写入段落没有表达的结论。

没有可用全文时，保存题录和原始摘要，标记 `abstract_only`，并写明：`无可用全文：仅记录元数据与摘要，未据此推断正文结论。` 不得把摘要扩写为正文主张。

每篇成功后更新 `文献索引.md` 的相对链接。单篇失败不得删除已完成文件，也不得阻断其他文献处理；完成 collection 后报告各状态数量和失败条目。
