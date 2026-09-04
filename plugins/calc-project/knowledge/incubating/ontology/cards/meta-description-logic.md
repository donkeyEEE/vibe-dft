---
name: meta-description-logic
type: concept
tags: [domain/knowledge-engineering, task/ontology-design]
updated_at: 2026-08-18
---

# 描述逻辑

描述逻辑（Description Logic, DL）是一族可判定的知识表示逻辑，以概念、角色、个体和组合构造子表达领域知识，并支持类包含、实例判定、本体一致性和类可满足性等推理任务；OWL 2 DL 的直接语义建立在 SROIQ 描述逻辑之上。

## Explanation

常用记号包括：`C ⊑ D` 表示每个 C 实例也是 D 实例；`C ⊓ D` 与 `C ⊔ D` 分别表示交集和并集；`¬C` 表示否定；`∃R.C` 要求至少存在一个经 R 连接的 C 实例；`∀R.C` 要求所有已有 R 后继均为 C 实例；`C(a)` 与 `R(a,b)` 分别是概念和角色断言。

存在限制可以由逻辑模型中的匿名见证者满足，不要求把命名实体写回 RDF。全称限制只约束关系后继，本身不保证后继存在；没有后继时可以空真。本体蕴含一个结论，要求该结论在本体的全部模型中都成立；本体一致则只要求至少存在一个模型。

## Caveats

本卡只提供常用记号和推理任务的入门语义，不替代特定描述逻辑的完整语法、模型论定义或复杂度分析。

## References

- 《本体论紫皮书》v2，第 3.1 节，PDF 第 12 页（ONT-SO-001）。
- W3C, [OWL 2 Web Ontology Language Primer](https://www.w3.org/TR/owl2-primer/), §§3, 5.2（ONT-STD-001）。
- W3C, [OWL 2 Web Ontology Language Direct Semantics](https://www.w3.org/TR/owl2-direct-semantics/), §§2.2, 3（ONT-STD-002）。
