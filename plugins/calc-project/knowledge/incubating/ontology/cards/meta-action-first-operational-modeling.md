---
name: meta-action-first-operational-modeling
type: procedure
tags: [domain/knowledge-engineering, task/ontology-design, task/workflow-design]
updated_at: 2026-08-26
---

# Action 优先的操作型建模

操作型建模应先识别高价值业务 Action 及其决策条件，再反推参与的 Object、Link、Function 和数据需求，以防对象模型膨胀却没有可执行闭环。

## Procedure

列出需要改变业务状态的操作并按价值、频率、风险和可逆性排序；为优先 Action 定义触发条件、输入、前置条件、授权、副作用与完成状态；由这些契约反推必须存在的 Object、Link 和计算 Function；再追溯到数据源、刷新要求和质量门禁；最后用一次完整回写验证最小闭环，稳定后才扩展对象或长尾 Action。

## Caveats

Action 优先适用于运营决策和状态改变系统。以跨域知识整合、术语一致或逻辑推理为目标的项目可能仍需概念与能力问题先行。

## References

- 《本体论紫皮书》v2，第 5.6、5.8 节，PDF 第 93、98 页（ONT-OP-010、ONT-OP-016）。
