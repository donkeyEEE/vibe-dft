---
name: ask-lyz
description: 将明确的 Calc Project 请求路由至配置、RQ、Spec 设计或执行接口之一。
---

# Ask LYZ

仅读取足以确定一个目标及其 sibling 所需的稳定项目上下文和权威指针。返回该 sibling 的
准确调用方式、已解析的项目/领域身份与路径、尚待用户完成的动作，以及任何缺失信息。若没有
或存在多个目标，请用户选择而非猜测。明确请求项目进展时，调用只读 `$show-cot` 视图，
而不是选择工作流 sibling。

| 请求分支 | 路由 |
|---|---|
| 缺失或变更了稳定项目、Tracker、数据边界或集群配置 | `$calc-setup` |
| RQ 生命周期、已接受决策、未回答的 RQ 问题，或 concluded Spec 对 RQ 的影响 | `$calc-rq` |
| 一份 RQ 的完整 Spec 集、主要判断、科学承诺、Task DAG、条件、验收、停止规则或替换一份 Spec | `$calc-to-spec` |
| 推进 ready/active Spec；准备、提交、跟踪、同步、接受、纠正或闭合其 Run 与 Task | `$calc-execute` |
| 项目进展、执行历史或当前 RQ / Spec / Task / Run 总览 | `$show-cot` |

除只读 COT 视图外，这是纯路由接口。不得给出科学建议、方法选择、参数值、评审结论、
授权或领域变更。

推荐已解析的工作流 sibling，不自动调用它；进展分支仅调用其只读 COT 视图。
