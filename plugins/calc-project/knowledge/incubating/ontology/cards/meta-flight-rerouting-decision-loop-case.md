---
name: meta-flight-rerouting-decision-loop-case
type: evidence
tags: [domain/knowledge-engineering, task/workflow-design, case/aviation]
updated_at: 2026-08-26
---

# 航班改航决策闭环教学案例

航班改航教学实例展示了天气事件触发受影响航班筛选，Function 校验机型、燃油、跑道和容量约束，再由调度审批并回写运行系统的决策链。

## Example

机场状态变化触发 Workflow，并筛选计划或已起飞且目的地受影响的航班。Function 根据飞机当前位置、机型适配、剩余燃油、跑道长度和机位容量形成可行备降集合；Agent 生成逐航班提案；运行控制人员审查后执行改航 Action，并把新目的地和通知状态写回运行系统。

## Caveats

本案例不是运行控制规程。真实改航必须服从当前航空法规、公司手册、空管指令和授权人员判断。

## References

- 《本体论紫皮书》v2，第 5.5 节，PDF 第 88 页（ONT-OP-007）。
