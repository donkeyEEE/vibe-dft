---
name: literature-review
description: Produce an evidence-grounded literature review from Web sources or a user-specified Zotero collection and save the result as Markdown. Standalone use requires explicit invocation; calc-to-spec may call it for design research.
---

# Literature Review

围绕用户的研究主题检索、阅读并综合文献，最终只交付一份 Markdown 文档。默认使用 Web；用户指定 Zotero 分类时，改用该分类及其全部子分类。
独立使用时仅接受用户显式调用。`$calc-project:calc-to-spec` 为已解析 RQ 的科学设计
补证据时，可明确调用本 skill；这不是面向普通请求的隐式调用入口。

## 启动门槛

开始检索前确认以下两项：

1. 研究主题或问题。
2. Markdown 保存路径。

独立调用缺少任一项时，先向用户询问。由 `$calc-project:calc-to-spec` 调用时，
研究问题由其当前 Spec 设计缺口给定，保存路径由其在已解析研究主线的 `06-文献笔记/`
中选择唯一 `.md` 文件；仅在该范围内可自行创建缺失的父目录。目标文件已存在时
另选唯一文件名，不覆盖或续写。其他调用中，路径必须先由用户确认；已有文件或
缺失父目录也按用户确认处理。

时间范围、语言、综述侧重点和引用格式都是可选约束；用户未指定时，根据研究问题作合理选择。

## 来源模式

每次运行只采用一种已确认的来源模式：

- **Web 模式**：默认模式。使用可用的 Web 检索能力查找论文，优先原始论文、出版社页面及可信学术索引。
- **Zotero 模式**：当用户指定 Zotero 分类时采用。递归纳入该分类及全部子分类中的条目；通过 `get-zotero` 的只读接口获取题录、摘要、索引正文或 PDF。
- **混合模式**：仅在用户明确要求同时使用 Web 和 Zotero 时采用。

Zotero 分类不明确或无法唯一定位时，先让用户确认具体分类。Zotero 始终只读。

### Zotero 只读获取契约

先运行 `doctor --json`。调用 `collections --json` 得到分类 key 与 `parentCollection`，从用户确认的根 key 递归计算后代 key；对每个 key 调用：

```bash
python3 <plugin-root>/skills/get-zotero/scripts/zotero.py inventory \
  --collection-key <collection-key> --json
```

合并并按父条目 key 去重后，再为候选条目调用：

```bash
python3 <plugin-root>/skills/get-zotero/scripts/zotero.py content \
  <item-key> --mode auto --out-dir <temporary-directory>
```

验证 stdout manifest 的 `schema_version == 1`、`item_key` 与请求一致、`content.kind` 有效且文件 artifact 存在后才读取。`text-file` 可作为正文证据；`pdf-file` 在任何需要支撑具体结果、数值、方法比较或局限性的全文主张时定向解析，图、表、公式或页内位置同样如此；`metadata-only` 只能用于题录和原始摘要；`error` 按 `code` 与 `next_step` 处理且不写成无全文。不得直接调用 Zotero HTTP API、导入 `get-zotero` Python 模块或访问 Zotero 配置/附件路径。

## 证据门槛

- 至少读到摘要，文献才可进入正文综合。
- 涉及具体结果、数值、方法比较或研究局限时，读取可获得的正文证据。
- 只有标题或题录、且内容不足以核对的文献可作为候选，但不能支撑正文结论。
- 核对作者、题名、年份、期刊以及 DOI 或稳定链接；无法核验的字段明确标注，不猜测补全。
- 区分同行评议论文与预印本，并在结论力度上反映证据差异。

本 skill 不要求保存检索式、每轮结果数、筛选流水、PRISMA 图或其他可复现检索记录。用户明确要求正式系统综述或 PRISMA 流程时，先说明当前轻量工作流不覆盖该方法学承诺，再确认是否仍按本流程完成普通文献综述。

## 综合与写作

根据主题选择足够覆盖问题的文献，兼顾奠基性工作、当前进展、相互冲突的结果和重要限制。正文按研究问题或主题综合，不写成逐篇摘要清单，也不以引用量、期刊名或作者声望替代证据判断。

文档结构随问题调整，但必须包含：

- 清楚界定的主题与范围；
- 按主题组织的证据综合；
- 共识、分歧、局限和仍未解决的问题；
- 正文引用与完整参考文献表。

默认使用作者—年份引用格式，并尽量为每条参考文献提供 DOI 或稳定链接；用户指定目标格式时遵从用户要求。图件不是必需交付物，不生成 PDF。

## 写入与完成标准

将最终内容写入按启动门槛确定的 Markdown 路径。完成前检查：

- 文件存在且为可读的 Markdown；
- 正文中的每项实质性文献主张都有已读取证据支撑；
- 正文引用与参考文献表逐一对应；
- 来源限制、全文不可得或证据不足等重要边界已在文中说明；
- 除用户明确要求外，没有创建其他交付文件。

最后向用户返回 Markdown 文件路径，并用几句话概括覆盖范围与主要证据限制。
