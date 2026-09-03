---
name: meta-tiered-entity-resolution
type: procedure
tags: [domain/knowledge-engineering, task/ontology-implementation, concern/validation]
updated_at: 2026-08-26
---

# 分级实体消歧

多源实体对齐应把稳定业务主键、属性相似度和图拓扑证据分级组合，自动合并仅限强证据，模糊区间进入人工审核并保留不合并决定。

## Procedure

先以统一社会信用代码、标准编码等稳定主键处理确定性匹配；主键缺失时再组合规范化名称、地址、时间和其他领域属性；图谱已有足够上下文时，可用共同邻居等拓扑证据辅助判断。规则应区分自动合并、人工审核和明确拒绝三类结果，并记录规则版本、置信依据以及人工决定，防止同一错误在后续批次反复出现。

## Caveats

相似度阈值必须用领域标注集校准。名称相似或共同邻居本身不能证明实体同一。

## References

- 《本体论紫皮书》v2，第 4.2.5.3 节，PDF 第 39 页（ONT-KG-005）。
