---
name: ask-lyz
description: 显式辅助 Calc Project 用户了解插件术语与流程、domain-research 的用途、选择工作接口或查看进度。
---

# Ask LYZ

这是由用户显式调用的辅助入口。识别用户是在了解插件、选择工作接口，还是查询实际进度；
同一问题涉及多个使用说明主题时一并回答。不得自行给出科学建议、方法选择、参数值、
评审结论或授权。

## 插件使用说明

用户询问插件术语、流程或记录职责时，以[领域术语](../../resources/project-context.md)解释。
涉及进度记录的字段与权威时读取[字段契约](../../resources/progress-tracker.md)；
涉及维护或重建时再读[维护契约](../../resources/progress-tracker-maintenance.md)。
具体操作读取 owning skill 的 `SKILL.md`，项目特定问题结合已有配置回答。
说明所问概念的作用、相邻流程和负责技能；科学设计或操作授权遵循对应入口。
需要修改领域词汇时调用 `$dev-engineering:domain-modeling`。

## domain-research 使用说明

`domain-research` 用物理因果链和计算剪枝分析研究机制、证据与计算取舍；
对齐术语含义及适用范围，维护 RQ 的 `RQ-CONTEXT.md`，校准证据措辞并精简科学表达。
它可隐式用于研究讨论、RQ/Spec 设计、结果解释和汇报。
项目 `CONTEXT.md` 由 `$dev-engineering:domain-modeling` 维护，问题、设计和验收决策由对应 Calc 技能记录。
涉及操作时读取同插件 `$domain-research` 的 `SKILL.md`；需要实际研究分析或术语对齐时推荐该技能。

## 推荐工作接口

推荐相应技能，不自动调用它，也不把后续工作拆成多个推荐。

| 用户目标 | 推荐 |
|---|---|
| 缺失或变更了稳定项目、RQ配置、数据边界或集群配置 | `$calc-setup` |
| RQ 生命周期、已接受决策、未回答的 RQ 问题，或 concluded Spec 对 RQ 的影响 | `$calc-rq` |
| RQ 当前研究目标的 Spec、科学承诺、Task DAG、条件、验收或替换一份 Spec | `$calc-to-spec` |
| 推进 ready/active Spec；准备、提交、跟踪、同步、接受、纠正或闭合其 Run 与 Task | `$calc-execute` |
| 按编号查询、记录、关联或合并 Issue，或委托推进其调研 | `$calc-issue` |
| 围绕主题或选定 RQ/Spec 汇总已有证据，生成阶段汇报或结果汇报 | `$calc-report` |
| 科研讨论或汇报中的术语自造、概念偏移、证据表述歧义或RQ 上下文维护 | `$domain-research` |

## 进度查询

用户询问项目进展、执行历史或当前 RQ、Spec、Task、Run 状态时，调用 `$show-cot`，并以其
结果回答。
