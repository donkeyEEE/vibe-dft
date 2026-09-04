---
name: meta-agent-component-responsibility-separation
type: concept
tags: [domain/agent-governance, task/architecture-selection, concern/ai-boundaries]
updated_at: 2026-08-18
---

# Agent 组件职责分离

知识图谱、OWL 推理机、LLM Agent、结构验证器、策略授权引擎、工作流、受控执行器和 Trace 应承担可独立检查的职责；Agent 负责生成候选方案，不应同时充当自身的授权者与执行者。

## Explanation

知识图谱保存实体、关系、事实和来源；OWL 推理机处理蕴含、一致性、分类和实例判定；LLM Agent 理解目标并生成候选计划或工具提案；验证器检查显式结构；策略引擎判断主体能否对资源执行动作；工作流控制状态、顺序、重试和恢复；执行器只执行获批动作；Trace 记录完整决策和执行链。职责分离使每个环节能够独立测试，并避免让概率模型自行决定其提案是否安全。

## Caveats

职责必须可区分和独立验证，但不要求部署为八个独立服务。低风险只读路径可以按风险采用较轻门禁。

## References

- 《本体论紫皮书》v2，第 3.2、6.1、6.3 节（ONT-SO-004、ONT-AO-002、ONT-AO-005、ONT-AO-011）。
- W3C, [OWL 2 Direct Semantics](https://www.w3.org/TR/owl2-direct-semantics/) 与 [SHACL](https://www.w3.org/TR/shacl/)（ONT-STD-002、ONT-STD-003）。
- [MCP Tool Safety](https://modelcontextprotocol.io/specification/2024-11-05/index)、[OPA](https://www.openpolicyagent.org/docs/)、[OPA Decision Logs](https://www.openpolicyagent.org/docs/management-decision-logs)、[Cedar](https://github.com/cedar-policy/cedar)、[OpenTelemetry GenAI Agent spans](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md)（ONT-AG-001–005）。
