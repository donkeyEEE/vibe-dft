---
name: meta-supply-disruption-decision-loop-case
type: evidence
tags: [domain/knowledge-engineering, task/workflow-design, case/supply-chain]
updated_at: 2026-08-26
---

# 供应链断供决策闭环教学案例

供应链断供教学实例展示了事件更新供应商状态、函数筛选备选方案、Agent 生成结构化提案、人员审批 Action、ERP 回写与审计的完整工作闭环。

## Example

断供事件先改变供应商对象状态并触发 Workflow；系统读取受影响采购订单、零件和物料清单；Function 按产能、交期和成本筛选备选供应商；Agent 把候选转换为带 Action 参数和依据的提案；授权人员审批后执行订单变更并回写 ERP；执行结果、审批与理由进入审计记录。

## Caveats

实例中的订单数量、成本与损失是来源叙事，不是通用绩效证据。替代供应决策还需质量认证、合同、物流和监管检查。

## References

- 《本体论紫皮书》v2，第 5.4 节，PDF 第 87 页（ONT-OP-006）。
