---
name: meta-use-case-first-graph-mvp
type: procedure
tags: [domain/knowledge-engineering, task/ontology-design, concern/maintainability]
updated_at: 2026-08-26
---

# 用例优先的图谱 MVP

知识图谱 MVP 应先限定少量高价值业务用例和可回答的能力问题，再据此确定最小节点、关系、数据源与验收查询，并用真实业务采用决定是否扩展。

## Procedure

选择结果可核对且已有明确使用者的核心用例；为每个用例写出输入、查询路径、预期输出和接受标准；只纳入这些路径必需的实体、关系和来源；用真实数据运行查询并与现有人工过程对照；记录缺失数据、误关联和查询失败；当现有用例稳定且实际被采用后，再以新的能力问题扩展 Schema。

## Caveats

来源中的用例数量和结果一致率只是经验示例，不是所有项目的固定门槛。业务采用也不能替代安全、隐私和数据质量验收。

## References

- 《本体论紫皮书》v2，第 4.7 节，PDF 第 66–67 页（ONT-KG-015、ONT-KG-016）。
