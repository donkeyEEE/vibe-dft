# Calc Project 共享资源

`progress-tracker.md` 定义每个 RQ 独立跟踪表的维护、字段、项目汇总和旧项目迁移契约。
活动消费者为 `calc-setup`、`calc-rq`、`calc-to-spec`、`calc-execute` 和 `show-cot`。

`project-context.md` 定义 Calc Project 的共享领域术语，是 RQ 上下文的基础组成。
`calc-rq`、`calc-to-spec`、`calc-execute` 在涉及稳定术语时读取它；
`calc-setup` 将它作为 `domain-modeling` 维护项目上下文的参考，`ask-lyz` 用它解释插件用法。
同插件的 `domain-research` 仅在首次创建 `RQ-CONTEXT.md` 时读取本资源；后续直接使用 RQ 上下文。
其余活动 skill 在涉及稳定术语或对象边界时按需读取。

各消费者直接声明资源的精确相对路径；本文件仅记录资源归属。
