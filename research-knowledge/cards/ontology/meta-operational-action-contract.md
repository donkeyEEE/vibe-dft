---
name: meta-operational-action-contract
type: constraint
tags: [domain/knowledge-engineering, task/workflow-design, concern/traceability]
updated_at: 2026-08-26
---

# 操作型 Action 契约

会产生真实副作用的 Action 必须显式声明输入、前置条件、授权、预期副作用、幂等与失败处理，并为每次执行留下可追溯审计记录。

## Explanation

输入契约限定参数和值域；前置条件检查对象状态和必要数据新鲜度；授权结合角色、对象属性、风险等级与审批要求；副作用列出将修改的系统和记录；幂等键阻止重复执行；重试、补偿和人工接管处理部分失败。审计至少记录执行者、时间、对象、理由、规则版本、审批、请求与结果，使一次状态改变可以复盘。

## Caveats

审批级别、补偿策略和紧急通道必须按法规、风险与底层系统能力配置。通过 Action 契约不等于业务决定必然正确。

## References

- 《本体论紫皮书》v2，第 5.2、5.6 节，PDF 第 69、79、93–94 页（ONT-OP-003、ONT-OP-005、ONT-OP-011、ONT-OP-012）。
