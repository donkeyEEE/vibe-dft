---
name: meta-financial-hidden-association-graph-case
type: evidence
tags: [domain/knowledge-engineering, task/ontology-implementation, case/finance]
updated_at: 2026-08-26
---

# 金融隐藏关联图谱教学案例

金融风控教学实例展示了如何把贷款、人、企业、账户、电话和地址统一建模，再用共享标识与多跳路径发现表面独立申请之间的隐藏关联。

## Example

案例先把申请、持股、担保、账户、电话和地址变成显式节点与关系，再查询不同贷款申请人之间是否经过共享联系方式、地址或法人实体形成路径。路径把原本分散在不同系统的线索组合成可审查的风险候选，使分析人员能够继续核对控制关系、交易与业务记录。

## Caveats

关系路径只生成调查线索，不构成欺诈认定。共享电话、地址或企业关联都可能存在合法解释；来源也未提供可独立复核的项目数据与效果评估。

## References

- 《本体论紫皮书》v2，第 4.4 节，PDF 第 53 页（ONT-KG-009）。
