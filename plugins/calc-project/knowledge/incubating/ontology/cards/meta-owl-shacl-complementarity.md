---
name: meta-owl-shacl-complementarity
type: method-constraint
tags: [domain/knowledge-engineering, task/ontology-design, concern/validation]
updated_at: 2026-08-18
---

# OWL 推理与 SHACL 校验互补

OWL 推理与 SHACL 数据校验应承担不同保障职责：前者在开放世界中处理逻辑蕴含与一致性，后者按 shapes 检查给定数据中的显式值、类型、单位和基数是否合规。

## Explanation

OWL 公理 `Material ⊑ ∃hasStructure.CrystalStructure` 可以在逻辑上保证材料具有某种结构，但缺失显式 `hasStructure` 三元组通常不会因此造成不一致。若交付规范要求每条材料记录明确填写一个结构或每个测量值明确填写单位，应由 SHACL 对 data graph 执行 `minCount`、类型、值域或其他 shape 检查，并生成 validation report。

## Caveats

OWL 与 SHACL 可以协同但不能互相替代。实际结果还取决于 OWL profile、SHACL shapes、entailment regime 和验证器配置。

## References

- 《本体论紫皮书》v2，第 3.2–3.3 节，PDF 第 14–15 页（ONT-SO-004、ONT-SO-005）。
- W3C, [OWL 2 Primer](https://www.w3.org/TR/owl2-primer/) 与 [Direct Semantics](https://www.w3.org/TR/owl2-direct-semantics/)（ONT-STD-001、ONT-STD-002）。
- W3C, [Shapes Constraint Language](https://www.w3.org/TR/shacl/), §3（ONT-STD-003）。
