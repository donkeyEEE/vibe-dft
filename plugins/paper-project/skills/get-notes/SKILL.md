---
name: get-notes
description: Use when turning user-selected Zotero literature into evidence-grounded Chinese research notes saved in a project directory. Retrieves source content through get-zotero.
---

# Get Notes

将用户选定的 Zotero 父级文献条目转成项目内中文研究笔记。题录、摘要、索引正文和 PDF 全部通过 `paper-project:get-zotero` 只读获取；本 skill 只负责理解文献并写笔记。

## 输入与输出

- 文献可以由题名、item key 或用户指定的 collection 范围确定；匹配不唯一时先让用户确认。
- 目标是用户指定的项目内目录。请求或当前项目已明确目标时直接使用，否则在写入前只询问一次目标目录。
- 阅读问题是可选项；用户未提供时，生成覆盖研究问题、方法、主要证据、适用条件和局限的通用精读笔记。
- 每个父级条目写成 `<target-directory>/<item-key>.md`。已有同名文件时保留，除非用户明确要求更新。

Attachment、annotation 和独立 note 只作为父级条目的证据来源，不单独生成笔记。

## 获取内容

先用 `get-zotero` 定位父级条目，再调用其版本化内容接口：

```bash
python3 <plugin-root>/skills/get-zotero/scripts/zotero.py content \
  <item-key> --mode auto --out-dir <temporary-directory>
```

验证 manifest 的 `schema_version == 1`、`item_key` 与目标一致、artifact 存在，并按 `content.kind` 处理：

- `text-file`：读取索引正文并提取与阅读问题或研究价值直接相关的证据。
- `pdf-file`：仅在图、表、公式、页码或版面信息对结论必要时，使用 LiteParse 定向解析相关页面。
- `metadata-only`：只使用题录和原始摘要，明确标记没有可用全文。
- `error`：报告 `code` 与 `next_step`，不生成未经证据支持的笔记。

不直接访问 Zotero HTTP API，不解析 Zotero 连接或附件路径，也不导入 `get-zotero` 的 Python 模块。

## 生成笔记

按 [研究笔记模板](references/研究笔记模板.md) 组织内容。每篇笔记必须：

1. 区分作者主张、正文证据和自己的项目判断。
2. 写明证据成立的材料、方法、参数、温度、模型假设或其他适用条件。
3. 对用户的阅读问题给出直接回答；没有指定问题时概括论文解决的问题、方法、主要发现与局限。
4. 标明实际使用的证据来源，不把摘要扩写成正文结论。
5. 给出对当前项目的相关性与可执行的后续核验事项；没有直接相关性时明确说明。

没有全文时写明：

```text
无可用全文：仅记录元数据与摘要，未据此推断正文结论。
```

批量处理时逐篇写入；单篇失败不删除已有文件，也不阻断其他文献。Zotero、PDF 和目标目录中的无关文件始终保持不变。
