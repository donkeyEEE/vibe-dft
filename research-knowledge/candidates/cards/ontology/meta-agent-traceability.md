---
name: meta-agent-traceability
type: constraint
tags: [domain/agent-governance, task/agent-governance, concern/traceability]
updated_at: 2026-08-18
---

# Agent 行为可追溯性

可执行 Agent 必须把目标与身份上下文、原始 proposal、知识事实与来源、策略和规则版本、授权结果、步骤状态、工具参数与返回值以及审批事件关联为结构化 trace，使行为能够复盘、归因和回归验证。

## Explanation

仅记录“调用过某工具”无法解释为什么调用、依据什么事实或哪条规则放行。有效 trace 应连接提案、证据、策略决策和实际副作用，并为一次决策提供稳定标识。它支持事故定位、离线调试、漏拦与误拦分析，以及规则、模型或工具变更后的回归评估。

## Caveats

Trace 必须遵守隐私、最小化、脱敏和保留期限要求。OpenTelemetry GenAI Agent 语义约定仍处于 Development，生产 trace schema 应独立版本化，不能无限记录敏感提示、凭据或原始数据。

## References

- 《本体论紫皮书》v2，第 6.1.5、6.3.5、6.7 节，PDF 第 103、118、130 页（ONT-AO-005、ONT-AO-014、ONT-AO-022）。
- [OPA Decision Logs](https://www.openpolicyagent.org/docs/management-decision-logs)（ONT-AG-003）。
- [OpenTelemetry GenAI Agent spans](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md)（ONT-AG-005）。
