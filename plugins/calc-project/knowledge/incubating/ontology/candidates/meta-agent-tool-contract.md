---
name: meta-agent-tool-contract
type: method-constraint
tags: [domain/agent-governance, task/tool-use, concern/ai-boundaries]
updated_at: 2026-08-18
---

# Agent 工具契约

Agent 工具应以显式契约声明输入输出 Schema、前置条件、副作用、超时和失败行为，并把工具存在、Agent 可见性与当前主体在当前上下文中的调用授权作为三个独立判断。

## Explanation

工具注册或 MCP discovery 只说明系统具有某项能力；工具被提供给 Agent 只说明它在当前工具集合中可见；真正调用还必须根据用户身份、动作、资源、环境和风险等级做授权。Schema 校验能够阻止缺失字段、类型错误和越界参数，但不能回答调用者是否有权执行或副作用是否已获批准。

## Caveats

MCP、Function Calling 或 JSON Schema 只是能力发现与契约载体，不能替代主体—动作—资源授权、策略判定、用户同意和运行时隔离。

## References

- 《本体论紫皮书》v2，第 6.2、6.3.5 节，PDF 第 109、117 页（ONT-AO-008、ONT-AO-013）。
- [Model Context Protocol Specification: Tool Safety](https://modelcontextprotocol.io/specification/2024-11-05/index)（ONT-AG-001）。
- [Open Policy Agent](https://www.openpolicyagent.org/docs/)（ONT-AG-002）。
- [Cedar Policy Language](https://github.com/cedar-policy/cedar)（ONT-AG-004）。
