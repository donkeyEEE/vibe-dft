# Workflow

每轮引用校验执行以下六步。

## 1. 解析文档，定位段落

使用 liteparse 提取 DOCX 文本：

```bash
lit parse paper.docx --format json -o /tmp/paper_parsed.json
```

从 JSON 输出中按段落边界定位用户指定的段落。如果 liteparse 不可用，回退到 `python3 -c "import docx; ..."` 读取 python-docx（若已安装）。

提取目标段落的纯文本，保留段落编号。

## 2. 提取引用标记

运行 `scripts/citation_validator.py extract` 识别段落中所有引用标记：

```bash
python3 <plugin-root>/skills/citation-validator/scripts/citation_validator.py extract \
  --text "段落文本..." \
  --json
```

输出 JSON 包含每个引用标记的 ID、原始文本、模式类型和 Zotero 搜索查询。

引用模式识别覆盖：
- 数字编号: `[1]`, `[1,2]`, `[1-3]`, `[1,2,5-7]`
- 作者-年份: `(Smith et al., 2020)`, `(Zhang and Li, 2019)`
- 内联作者: `Smith et al. (2020)`
- 上标: `text¹²³`

如果段落中引用模式复杂（混合样式、引文嵌套），打开 `references/citation-patterns.md`。

## 3. 在 Zotero 中定位每一篇文献

对每条引用，通过 Zotero 搜索定位文献：

**数字编号引用**：需要从论文末尾的参考文献列表中解析对应关系。先查找文档中的参考文献列表，建立编号到文献信息的映射。如果 Word 文档中参考文献列表不可解析，请用户提供。

**作者-年份引用**：直接使用生成的查询搜索 Zotero：

```bash
python3 <plugin-root>/skills/get-zotero/scripts/zotero.py search "Author 2020" --json
```

只使用 `get-zotero` 的只读 CLI seam。如果 Zotero 未运行，提示用户启动 Zotero Desktop。

搜索后，匹配最可能的结果。如果多个结果匹配，优先选择标题或领域与段落主题最相关的。如果找不到，标记为"未找到"。

详细的 Zotero 查询策略见 `references/zotero-integration.md`。

## 4. 获取摘要和（按需）全文

对每条找到的文献，获取摘要：

```bash
python3 <plugin-root>/skills/get-zotero/scripts/zotero.py content \
  <itemKey> --mode auto --out-dir <temporary-directory>
```

先按 `references/zotero-integration.md` 验证 manifest；摘要位于 metadata，正文由
`content.kind` 指向的 artifact 提供。

**何时获取全文**：
- 摘要信息不足以判断支撑关系（例如摘要只描述了方法未提结论）
- 摘要与声明看起来相关但需要确认具体数据或结论
- 评估等级为 `partial_support` 或 `contradictory` 时需确认细节

获取全文时继续消费同一个 content artifact，不绕过 `get-zotero` 直接访问附件。

仅读取与声明相关的部分（500-1000 字），不要将整篇论文加载到上下文。

## 5. 评估支撑等级

对每条引用，按 `static/core/support-grading.md` 中的框架判断支撑等级。

评估流程：
1. 精读段落声明，提取核心主张（研究对象、关系、方法、结论）
2. 阅读文献摘要，判断论文实际研究了什么、发现了什么
3. 对比声明和论文实际内容，按五级标准分级
4. 写出评估推理（50-150 字），说明为什么给出此等级
5. 如果评估依据来自摘要，注明 `evidence_basis: abstract`；如果来自全文，注明 `evidence_basis: fulltext`

可用脚本辅助：

```bash
python3 <plugin-root>/skills/citation-validator/scripts/citation_validator.py grade \
  --claim "声明文本" \
  --abstract "摘要文本" \
  --title "论文标题"
```

**关键规则**：
- 绝不因为标题相关就判定为强支撑或部分支撑
- 如果摘要和声明讨论的是不同机制/材料/方法/物种，即使主题相关也是 `no_evidence`
- 综述文章用于背景支撑是合理的，用于实验性声明则需降级
- 矛盾文献必须明确指出矛盾点，不可淡化

## 6. 生成报告

将评估结果汇总为 JSON，然后生成 Markdown 报告：

```bash
python3 <plugin-root>/skills/citation-validator/scripts/citation_validator.py report \
  --json-file /tmp/citation_validation.json \
  --out /tmp/citation_report.md
```

报告结构：
1. **引用校验报告** — 源文件、校验段落、引用总数
2. **支撑等级分布** — 统计表
3. **逐条详情** — 每个引用段落的评估
4. **风险与缺口** — 需要关注的问题
5. **建议操作** — 可执行的改进建议

返回报告路径，并总结关键发现（2-4 句话）。
