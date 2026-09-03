---
name: meta-agent-governance-regression-evaluation
type: procedure
tags: [domain/agent-governance, task/evaluation, concern/maintainability]
updated_at: 2026-08-18
---

# Agent 治理回归评估

每次规则、模型、提示、工具契约或检索源变更后，都应使用固定风险与正常任务集重新评估漏拦、误拦、任务成功、追溯完整性和延迟。

## Caveats

固定回归集需要持续补充线上新型失败，但不得用未经脱敏的生产敏感数据随意扩充。

## References

- 《本体论紫皮书》v2，第 6.6–6.7 节（ONT-AO-020、ONT-AO-021、ONT-AO-022）。
