---
name: meta-semantic-ontology-engineering-loop
type: procedure
tags: [domain/knowledge-engineering, task/ontology-design, concern/quality]
updated_at: 2026-08-18
---

# 语义本体工程闭环

语义本体工程应形成能力问题与范围、概念化、形式化、RDF 数据与 provenance、SHACL 校验、OWL 推理、能力问题回归、版本化发布、监测和演化的闭环，而不是一次性编写类与属性。

## Explanation

能力问题先限定本体必须支持的真实任务。形式化阶段建立类、属性和必要公理；数据阶段把事实映射为 RDF，并把重要断言连接到来源、生成活动和责任主体。交付前分别运行 SHACL 数据校验和 OWL 一致性、分类或实例判定，再用能力问题查询及预期答案执行回归验收。每次公理、映射、数据约束或依赖变更后重新运行这些检查，并通过版本和变更记录保留演化历史。

## Caveats

三元组数量、类数量、SHACL 通过或推理一致中的任一单项，都不能替代来源可靠性、科学正确性和用途适用性验证。

## References

- 《本体论紫皮书》v2，第 3.6–3.7 节，PDF 第 26–28 页（ONT-SO-012、ONT-SO-013、ONT-SO-014）。
- W3C, [Shapes Constraint Language](https://www.w3.org/TR/shacl/), §3（ONT-STD-003）。
- W3C, [PROV-O](https://www.w3.org/TR/prov-o/), §2.2（ONT-STD-004）。
