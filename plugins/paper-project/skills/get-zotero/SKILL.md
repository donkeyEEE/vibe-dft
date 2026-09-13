---
name: get-zotero
description: Use when retrieving bibliographic metadata, annotations, Zotero indexed full text, or an original PDF from Zotero Desktop. Provides read-only content artifacts for other skills; does not create research notes or project libraries.
---

# Get Zotero

从 Zotero Desktop 只读取得一篇文献的题录与原始内容。输出供用户或其他 skill 使用，不生成研究笔记、论文素材库或项目目录。

## 调用边界

- 只处理用户指定或确认的文献、collection 与附件。
- Zotero 始终只读；不修改条目、批注、附件、设置或 profile。
- metadata 可直接返回 JSON；正文与 PDF 作为文件 artifact 传递，不嵌入 JSON。
- 本地附件路径只供内部工具调用，不写入普通回复或持久文档。
- 连接失败时读取 [故障排查](references/troubleshooting.md)；需要非默认连接或附件映射时读取 [配置说明](references/configuration.md)。

## 访问与诊断

Zotero Desktop 必须运行且启用本地 API。先运行：

```bash
python3 <plugin-root>/skills/get-zotero/scripts/zotero.py doctor --json
```

支持 Windows 原生、macOS/Linux 原生，以及 Windows Zotero + WSL Codex。具体只读路由见 [本地 API 路由](references/local-api-routes.md)。

## 获取模式

统一内容入口为：

```bash
python3 <plugin-root>/skills/get-zotero/scripts/zotero.py content \
  <item-key> --mode {auto,indexed-text,pdf} --out-dir <temporary-directory>
```

- `auto`：优先 Zotero indexed full text；不可用时返回所属 PDF；两者都不存在时返回 metadata-only。
- `indexed-text`：要求索引正文并写入 UTF-8 TXT artifact；不可用时返回结构化错误。
- `pdf`：返回所属 PDF 的只读本地路径；不可访问时返回结构化错误。

需要先定位文献时使用 `search`；需要检查附件、批注或 child notes 时使用 `children`；需要用户当前选择的 collection 时使用 `selected-target`。PDF 的读取和 OCR 边界见 [PDF 证据策略](references/pdf-evidence-strategy.md)。

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

调用方必须先验证 `schema_version`、`item_key`、`content.kind` 和 artifact 是否存在，再消费内容。
