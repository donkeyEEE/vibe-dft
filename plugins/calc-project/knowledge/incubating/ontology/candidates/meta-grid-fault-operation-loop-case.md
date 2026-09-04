---
name: meta-grid-fault-operation-loop-case
type: evidence
tags: [domain/knowledge-engineering, task/workflow-design, case/energy]
updated_at: 2026-08-26
---

# 配电网故障操作闭环教学案例

配电网故障教学实例展示了如何把拓扑对象、潮流与转供校验、隔离和恢复 Action、风险分级授权及执行审计组合为高风险处置闭环。

## Example

SCADA 异常触发故障区段定位；拓扑对象描述馈线、开关、变压器和负荷连接；专业 Function 校验潮流和转供能力；系统产生隔离、转供和恢复候选；权限策略根据区域、风险和紧急程度决定审批或紧急通道；执行后回读开关与供电状态，并记录告警、授权和操作结果。

## Caveats

该实例只说明架构分工。真实电网操作必须使用经认证的保护、调度和安全规程，不能由通用 Agent 自主替代。

## References

- 《本体论紫皮书》v2，第 5.5b、5.6、5.8 节，PDF 第 89、94、98 页（ONT-OP-008、ONT-OP-012、ONT-OP-015）。
