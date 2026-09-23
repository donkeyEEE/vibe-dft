---
name: ask-lyz
description: 显式辅助 Calc Project 用户选择工作接口、解释项目术语或查看进度。
---

# Ask LYZ

这是由用户显式调用的辅助入口。根据用户请求进入且仅进入以下一个场景。不得自行给出科学建议、
方法选择、参数值、评审结论或授权。

## 推荐 sibling

推荐 sibling，不自动调用它，也不把后续工作拆成多个推荐。

| 用户目标 | 推荐 |
|---|---|
| 缺失或变更了稳定项目、Tracker、数据边界或集群配置 | `$calc-setup` |
| RQ 生命周期、已接受决策、未回答的 RQ 问题，或 concluded Spec 对 RQ 的影响 | `$calc-rq` |
| RQ 当前下一主要判断的 Spec、科学承诺、Task DAG、条件、验收、停止规则或替换一份 Spec | `$calc-to-spec` |
| 推进 ready/active Spec；准备、提交、跟踪、同步、接受、纠正或闭合其 Run 与 Task | `$calc-execute` |
| 围绕主题或选定 RQ/Spec 汇总已有证据，生成阶段汇报或结果汇报 | `$calc-report` |

## 术语解释

用户询问 Calc Project 术语、概念边界或词汇冲突时，调用 `$dev-engineering:domain-modeling`。
将用户的问题和当前项目上下文交给它，由其解释、澄清并在术语真正发生变化时同步领域词汇。

## 进度查询

用户询问项目进展、执行历史或当前 RQ、Spec、Task、Run 状态时，调用 `$show-cot`，并以其
结果回答。
