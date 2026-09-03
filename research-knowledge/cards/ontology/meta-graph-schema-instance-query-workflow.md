---
name: meta-graph-schema-instance-query-workflow
type: procedure
tags: [domain/knowledge-engineering, task/ontology-implementation, task/workflow-design]
updated_at: 2026-08-26
---

# 图谱 Schema—实例—查询工作流

属性图项目应从目标查询反推关系语义，依次落实 Schema 定义、实例治理与查询消费，并用实际查询结果验证三层是否闭合。

## Procedure

先把业务问题改写成可验收的路径问题，明确起点、关系方向、过滤条件和返回结果；再定义最小节点标签、关系类型、主键约束与索引。随后把来源数据映射为实例，并在写入前完成格式、标识和取值校验。最后用代表性查询对照现有人工结果，检查路径是否回答原问题，并将失败反推到 Schema 或实例治理环节修正。

## Caveats

该流程针对关联遍历型图谱。需要模型论推理时，不能用 Cypher 路径匹配替代 OWL 推理。

## References

- 《本体论紫皮书》v2，第 4.2、4.7 节，PDF 第 32、67 页（ONT-KG-001、ONT-KG-016）。
