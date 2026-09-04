---
name: meta-drug-repurposing-graph-case
type: evidence
tags: [domain/knowledge-engineering, task/ontology-implementation, case/life-sciences]
updated_at: 2026-08-26
---

# 药物重定位图谱教学案例

药物重定位教学实例展示了如何沿药物—靶点—疾病—通路路径生成可解释候选，并用既有适应症和在研关系排除已覆盖路径，随后交给实验验证。

## Example

案例以靶点连接药物与疾病，再把通路和基因作为机制背景。查询寻找已上市药物作用的靶点所关联、但尚无已批准或在研药物覆盖的疾病，并返回相关通路作为候选解释。图谱在这里承担候选生成、排除和证据组织，而不是替代药理、毒理或临床验证。

## Caveats

图路径表示关联和机制线索，不证明疗效、安全性或因果机制。数据库覆盖偏差、关系方向、证据强度与时间有效性都会改变候选排序。

## References

- 《本体论紫皮书》v2，第 4.5c 节，PDF 第 59–60 页（ONT-KG-012、ONT-KG-013）。
