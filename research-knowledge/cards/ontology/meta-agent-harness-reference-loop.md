---
name: meta-agent-harness-reference-loop
type: procedure
tags: [domain/agent-governance, task/agent-implementation, artifact/code-example]
updated_at: 2026-08-18
---

# 最小 Agent Harness 执行循环

最小 Harness 执行循环应把声明式约束加载、proposal 生成、适用门禁校验、违规反馈、受控工具执行和 Trace 写入拆成可测试阶段。

## Caveats

示例中的简化规则求值不可直接用于生产；生产实现必须采用可审计策略判断和真实权限边界。

## References

- 《本体论紫皮书》v2，第 6.3 节（ONT-AO-009、ONT-AO-010、ONT-AO-011）。
