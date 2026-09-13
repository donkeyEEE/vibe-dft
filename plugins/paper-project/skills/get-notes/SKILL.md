---
name: get-notes
description: Use when turning selected Zotero literature into Chinese project-local research notes, or creating and maintaining a manuscript material library from one user-selected Zotero collection. Retrieves source content through get-zotero.
---

# Get Notes

将已选 Zotero 文献转成项目本地中文研究笔记或论文写作素材库。所有 Zotero 题录、索引正文和 PDF 通过 `paper-project:get-zotero` 获取；本 skill 只负责交互、理解、组织和项目写入。

## 两条互斥路线

- **研究笔记**：为既有研究线生成问题导向的单篇阅读笔记，写入 `06-文献笔记/01-单篇文献/`。
- **论文素材库**：修改论文前，让用户明确选择 exactly one Zotero collection，然后完整读取并执行 [论文素材库契约](references/writing-material-library.md)。不得同时创建或更新 `06-文献笔记/`。

研究笔记路线不得顺带创建论文素材库。

## 前置条件

研究笔记要求用户提供已存在的 `project-root`、已存在的 `research-line`、明确的阅读问题，以及相关 Zotero collection 的显式选择。项目或研究线不存在时停止，不替用户创建。

只处理父级文献条目；attachment、annotation 和独立 note 只作为证据来源。Zotero 与 PDF 始终只读。

## 内部获取接口

先通过 `get-zotero` 定位条目，再调用：

```bash
python3 <plugin-root>/skills/get-zotero/scripts/zotero.py content \
  <item-key> --mode auto --out-dir <temporary-directory>
```

验证 manifest 的 `schema_version == 1`、`item_key` 与目标一致，并按 `content.kind` 分派：

- `text-file`：读取 TXT artifact，按阅读问题筛选证据。
- `pdf-file`：只有问题依赖图、表、公式、页内位置或索引异常时，使用 LiteParse 定向解析必要页面；不复制 PDF 到项目。
- `metadata-only`：只使用题录和原始摘要，并明确标记没有可用全文。
- `error`：按 `code` 和 `next_step` 处理；不写入未验证笔记。

`get-notes` 不直接访问 Zotero HTTP API，不解析 Zotero 连接配置或 Windows/WSL 附件路径，也不导入 `get-zotero` 的 Python 模块。

## 研究笔记流程

1. 对新专题，在 `02-专题综合/<主题>-研究问题卡片.md` 使用 [研究问题卡片模板](references/研究问题卡片模板.md)；已有卡片时确认本条目的阅读问题。
2. 记录既有项目根与研究线，通过 `get-zotero` 展示条目所属 collections，让用户确认项目相关分类；没有已选分类时不写入。
3. 取得父条目的 item key、题录、摘要、collection memberships、attachment key 和 content artifact。
4. 使用 `scripts/research_note_storage.py` 解析每个已选分类的目标路径，并只更新用户确认的 collection 映射。
5. 按 [论文精读模板](references/论文精读模板.md) 回答阅读问题，区分作者主张、索引正文、PDF 文本层、页面视觉核验与 OCR 证据。
6. 检查 YAML、证据来源、适用条件、附件 key、页码、数学分隔符和目标路径后，写入每个已选分类目录。

笔记路径：

```text
<project-root>/<research-line>/06-文献笔记/01-单篇文献/<selected-collection-path>/<item-key>.md
```

映射文件：

```text
<project-root>/<research-line>/06-文献笔记/zotero-project-map.yaml
```

## 内容要求

笔记必须包含直接回答、证据与适用条件、对项目的影响、冲突与局限、后续验证。不得把摘要扩写为正文主张。

无全文时在 YAML 和正文标记：

```text
无可用全文：仅记录元数据与摘要，未据此推断正文结论。
```

## 写入边界

- 研究笔记路线只可新建 `06-文献笔记/` 下必要目录和映射。
- 专题综合与证据矩阵由研究者手工维护，单篇导入不得自动更新。
- 素材库的增量状态、失败恢复、原稿保护和片段格式以 [论文素材库契约](references/writing-material-library.md) 为准；文件生命周期由 `scripts/writing_library_storage.py` 管理。
- 单篇失败不得删除已有文件，也不得阻断 collection 中其他条目。
- 不扫描全部 Zotero collections，不创建全局索引，不修改 Zotero、PDF 或用户已有项目数据。
