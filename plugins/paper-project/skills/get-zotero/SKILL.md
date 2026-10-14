---
name: get-zotero
description: Use when reading Zotero literature and all its attachments, or making user-authorized changes to metadata, tags, collections, items, notes, relations, attachments, saved searches, or full-text indexes. Provides compatible read-only artifacts to other skills.
---

# Zotero 文献读取与管理

从 Zotero Desktop 获取文献及全部直接附件，或执行用户授权的文献库修改。读取仍提供只读 artifact；研究笔记生成由 get-notes 负责，用户明确要求写入 Zotero 笔记时使用本 skill。

## 调用边界

- 只处理用户指定或确认的文献、collection 与附件。
- 读取命令不修改 Zotero。每次写入须获用户对具体变更的授权；明确指令本身算授权，宽泛请求先展示方案。删除与文件覆盖单独授权。
- 应用技术授权统一给 Codex，首次 Always Allow 后跨调用复用；技术授权不替代具体变更授权。执行写入前读取 [写入方案与授权](references/write-operations.md)。
- metadata 可直接返回 JSON；正文与 PDF 作为文件 artifact 传递，不嵌入 JSON。
- 本地附件路径只供内部工具调用，不写入普通回复或持久文档。
- 连接失败时读取 [故障排查](references/troubleshooting.md)；正常流程使用本机默认端点，不要求或创建用户配置文件。

## 访问与诊断

Zotero Desktop 必须运行且启用本地 API。先运行：

```bash
python3 <plugin-root>/skills/get-zotero/scripts/zotero.py doctor --json
```

Windows、macOS、Linux 和 WSL 均默认访问 `127.0.0.1:23119`；WSL 的附件路径仍按运行环境解析。版本能力与路由见 [本地 API 路由](references/local-api-routes.md)。

## 获取模式

统一内容入口为：

```bash
python3 <plugin-root>/skills/get-zotero/scripts/zotero.py content \
  <item-key> --mode {auto,indexed-text,pdf} --out-dir <temporary-directory>
```

- `auto`：枚举全部直接附件，各自优先索引文本，不可用时返回本地文件；没有附件时返回 metadata-only。
- `indexed-text`：逐附件要求索引文本并写入 UTF-8 TXT artifact；不可用的附件单独返回错误。
- `pdf`：逐附件返回只读本地文件；PDF 标明 pdf-file，其他格式在附件清单中标明 local-file；不可访问时返回结构化错误。

需要先定位文献时使用 `search`；需要列出某个用户指定分类中的父条目时使用 `inventory --collection-key <collection-key> --json`；需要检查附件、批注或 child notes 时使用 `children`；需要用户当前选择的 collection 时使用 `selected-target`。PDF 的读取和 OCR 边界见 [PDF 证据策略](references/pdf-evidence-strategy.md)。

## Content artifact contract

stdout 返回小型 JSON manifest，`schema_version` 固定为 `1`：

```json
{
  "schema_version": 1,
  "item_key": "ABCD1234",
  "metadata": {},
  "content": {
    "kind": "text-file",
    "path": "/tmp/get-zotero/run/EFGH5678.txt",
    "source": "zotero-indexed-fulltext",
    "attachment_key": "EFGH5678",
    "indexed_pages": 12,
    "total_pages": 15
  }
}
```

`content.kind` 只有四种：

- `text-file`：从 `path` 读取 UTF-8 正文。
- `pdf-file`：从 `path` 读取只读 PDF，必要时定向解析页面。
- `metadata-only`：只能使用题录与原始摘要，不推断正文结论。
- `error`：检查 `code` 与 `next_step`，不得把失败伪装成无全文结论。

`attachments` 是逐附件结果清单，包含 key、标题、MIME、角色提示、artifact 或错误；`coverage` 记录范围、获取完整性及遗漏。标签只是正文/SI 角色的线索，需根据标题页和内容核实；普通 PDF 标签不证明正文身份。默认读取清单中所有附件，包括 SI、图片与表格，使用对应工具；外部链接不自动追踪下载。

多附件的 `content` 是 text-file 汇总 artifact，包含各附件的文本及需要进一步打开的文件提示；它不是一份独立正文。调用方必须逐项检查 `attachments`；打开 PDF、图片等所需文件，报告不可读或缺失附件。`coverage.complete` 只表示获取是否完整，不证明科学阅读完成；索引页数/字符数不足须读取原文件补齐。仅有 SI 时明确正文缺失，不能宣称已读完整论文。单附件保留原有 content 输出形式，schema_version 仍为 1。

调用方必须先验证 `schema_version`、`item_key`、`content.kind` 和 artifact 是否存在，再消费内容。
