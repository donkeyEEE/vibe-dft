---
name: scientific-critical-thinking
description: Use when critically evaluating materials-physics claims, DFT or first-principles calculations, magnetism, spectroscopy, synthesis, characterization, or theory–experiment agreement. Use for evidence-based assessment of rigor, limitations, and alternative explanations.
---

# Materials Critical Thinking

评估材料物理论文、计算、实验或研究主张的证据强度与推理边界。输出中文批判性分析，严格区分来源事实、推断和未证实假设。

## 先取得足够证据

先判断用户提供的论文、数据或计算输入是否足够。若不足，自动选择补充路径：

1. 需要题录、批注、方法细节、图表语境、数值结果或原始结论时，调用 `zo2notes/scripts/zotero.py` 的只读命令：先 `search`，再按需 `children`，最后只读取所需 PDF 附件的 `fulltext`。
2. 仍缺关键材料时，明确列出缺口并只给出条件性判断；不要补造细节。

`zo2notes` 是项目内的 Zotero 接口；本技能只做评估，不修改 Zotero、PDF 或条目。

## 按任务选择检查项

先读取 `references/computational-research-and-reasoning.md`，核对模型、收敛、对照、可复现性和主张强度；再读取 `references/materials-physics-checklist.md` 中与任务对应的部分：

- DFT、DFT+U、SOC、vdW、声子、交换映射或居里温度：使用“第一性原理”检查项。
- 磁性、输运、XMCD、ARPES、散射、显微或衍射：使用“磁性与谱学”检查项。
- 合成、掺杂、相纯度、成分或结构表征：使用“合成与表征”检查项。
- 计算与实验结论相互解释：使用“理论—实验对照”检查项。

不要机械套用医学研究的随机化、盲法、GRADE 或 Cochrane 框架；仅在问题本身确实涉及这些概念时采用。

## 输出格式

按以下结构给出中文评估：

1. **评估对象与已用证据**：列出 Vault 笔记、Zotero 文献、用户材料及其用途。
2. **研究优势**：仅陈述证据能支持的优势。
3. **关键问题**：按“影响主结论 / 影响定量解释 / 次要问题”排序，并说明每项影响。
4. **主张与证据匹配度**：区分直接支持、间接支持和未支持的主张。
5. **不确定性与缺失信息**：明确缺少的参数、对照、原始数据或复现证据。
6. **下一步核验**：给出可执行的计算、实验或资料核验步骤；不把建议表述为既成事实。

## 硬性边界

- 没有直接证据时，不宣称计算已收敛、结构/相已稳定或机制已确立。
- 明确理论结果与实验结果是否在材料成分、厚度、缺陷、温度、磁场和测量几何上可比。
- 将“趋势一致”与“绝对数值一致”分开评价。
- 对方法或数据未披露的情况使用条件句，并说明需要什么信息才能确认。
