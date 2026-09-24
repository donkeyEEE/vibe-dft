---
name: ask-lyz
description: 显式辅助 Calc Project 用户了解插件术语与流程、选择工作接口或查看进度。
---

# Ask LYZ

这是由用户显式调用的辅助入口。识别用户是在了解插件、选择工作接口，还是查询实际进度；
同一问题涉及多个使用说明主题时一并回答。不得自行给出科学建议、方法选择、参数值、
评审结论或授权。

## 插件使用说明

用户询问术语含义、核心流程、各记录及 skill 的职责、Tracker 在流程中的位置等插件用法时，
直接解释。以 [领域术语](../../resources/project-context.md) 为概念依据；涉及进度跟踪表的
存储、维护、重建或权威边界时，读取 [进度跟踪表契约](../../resources/progress-tracker.md)；
涉及某阶段的具体操作时，读取该阶段 owning skill 的 `SKILL.md`。结合已配置项目的约定回答
项目特定问题，并说明通用设计与项目实际配置的区别。

回答应交代用户所问概念的作用及其与相邻记录或流程的关系。例如解释 Tracker 时，说明每个
RQ 的 `tracker.json` 是 RQ、Spec、Task、Run 状态的派生摘要，由状态写入者同步维护，
`show-cot` 汇总查询；RQ.md 和 Spec 保持权威。解释核心流程时，串起项目配置、RQ 决策、
Spec 设计、Task/Run 执行与汇报或进度查询，并指出各阶段的 owning skill。仅在用户要
解决术语冲突、重新定义概念或修改领域词汇时调用 `$dev-engineering:domain-modeling`。

## 推荐 sibling

推荐 sibling，不自动调用它，也不把后续工作拆成多个推荐。

| 用户目标 | 推荐 |
|---|---|
| 缺失或变更了稳定项目、RQ 存储配置、数据边界或集群配置 | `$calc-setup` |
| RQ 生命周期、已接受决策、未回答的 RQ 问题，或 concluded Spec 对 RQ 的影响 | `$calc-rq` |
| RQ 当前下一主要判断的 Spec、科学承诺、Task DAG、条件、验收、停止规则或替换一份 Spec | `$calc-to-spec` |
| 推进 ready/active Spec；准备、提交、跟踪、同步、接受、纠正或闭合其 Run 与 Task | `$calc-execute` |
| 按编号查询、记录、关联或合并 Issue，或委托推进其调研 | `$calc-issue` |
| 围绕主题或选定 RQ/Spec 汇总已有证据，生成阶段汇报或结果汇报 | `$calc-report` |

## 进度查询

用户询问项目进展、执行历史或当前 RQ、Spec、Task、Run 状态时，调用 `$show-cot`，并以其
结果回答。
