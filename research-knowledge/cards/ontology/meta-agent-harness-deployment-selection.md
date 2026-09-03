---
name: meta-agent-harness-deployment-selection
type: procedure
tags: [domain/agent-governance, task/architecture-selection, task/agent-implementation]
updated_at: 2026-08-18
---

# Agent Harness 部署选型

Harness 的进程内、网关 Sidecar 或 SDK 内嵌部署应依据隔离性、跨语言复用、延迟、故障边界、策略一致性和运维复杂度选择，并配套策略引擎、Trace、评测与工具契约。

## Caveats

不存在脱离组织技术栈和风险等级的唯一最佳放置方式；高风险工具仍需独立授权与执行隔离。

## References

- 《本体论紫皮书》v2，第 6.3.5 节（ONT-AO-012、ONT-AO-023、ONT-AO-024、ONT-AO-025）。
