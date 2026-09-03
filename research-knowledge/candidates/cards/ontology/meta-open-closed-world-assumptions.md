---
name: meta-open-closed-world-assumptions
type: concept
tags: [domain/knowledge-engineering, task/ontology-design]
updated_at: 2026-08-18
---

# 开放世界与封闭世界假设

开放世界假设把缺失事实解释为未知，而封闭世界式校验可以把未记录的必要事实视为不满足要求；选择错误会直接改变缺失检测和完整性约束的语义。

## Explanation

在 OWL 的开放世界语义中，没有记录 `P(a)` 通常既不能推出 `P(a)`，也不能推出 `¬P(a)`。`a : ∃R.C` 可以保证逻辑上存在某个 R 后继，却不要求 RDF 数据中已有一个命名实体或显式三元组。需要检查提交数据是否显式给出属性值时，应使用具有相应闭口校验语义的数据验证机制，例如 SHACL shape。

## Caveats

开放世界与封闭世界是语义选择，不应简化为“所有本体都开放、所有数据库都封闭”。具体行为取决于采用的语言、查询、规则和验证配置。

## References

- 《本体论紫皮书》v2，第 3.1、3.3 节，PDF 第 12、15 页（ONT-SO-002、ONT-SO-005）。
- W3C, [OWL 2 Web Ontology Language Primer](https://www.w3.org/TR/owl2-primer/), §5.2（ONT-STD-001）。
- W3C, [Shapes Constraint Language](https://www.w3.org/TR/shacl/), §3（ONT-STD-003）。
