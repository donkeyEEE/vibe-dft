---
name: meta-validate-agent-proposals-before-execution
type: constraint
tags: [domain/agent-governance, task/tool-use, concern/ai-boundaries]
updated_at: 2026-08-18
---

# Agent 提案必须先验证再执行

LLM 生成的 proposal 不应直接触达有副作用的工具；它必须经过结构验证、知识事实与语义前置条件检查、独立策略授权及必要的人工审批，成功后才交给受控执行器。

## Explanation

结构验证检查类型、必填字段和值域；知识图谱与 OWL 检查实体身份、类型和语义前置条件；策略引擎根据主体、动作、资源和上下文决定允许或拒绝；高成本、高风险或不可逆操作还需人工批准。执行器只接收获批提案，并把真实参数与结果写入 trace。失败提案应被拦截、修正或升级审批，而不是由 LLM 自行宣布安全。

## Caveats

Agent 只生成 proposal，不能为自己的提案提供确定性安全保证。只读、低风险工具可以采用较轻门禁，但风险等级和审批规则必须由实际系统定义。

## References

- 《本体论紫皮书》v2，第 6.1、6.3 节，PDF 第 101、112、114 页（ONT-AO-002、ONT-AO-010、ONT-AO-011）。
- [Model Context Protocol Specification: Tool Safety](https://modelcontextprotocol.io/specification/2024-11-05/index)（ONT-AG-001）。
- [Open Policy Agent](https://www.openpolicyagent.org/docs/)（ONT-AG-002）。
- [Cedar Policy Language](https://github.com/cedar-policy/cedar)（ONT-AG-004）。
