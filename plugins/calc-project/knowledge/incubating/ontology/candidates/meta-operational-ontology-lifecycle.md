---
name: meta-operational-ontology-lifecycle
type: procedure
tags: [domain/knowledge-engineering, task/ontology-implementation, concern/quality]
updated_at: 2026-08-26
---

# 操作型 Ontology 生命周期

操作型 Ontology 应按领域与 Action 选择、数据接入、对象和规则实现、闭环验证、上线监控、权限审计与演化迭代推进，并在既有闭环不稳时优先修补而非继续扩张。

## Procedure

先确定业务对象与 Action 候选并按价值和风险排序；接入具有血统与质量门禁的数据；实现 Object、Link、Function、Action 与授权；用端到端回写验证闭环；上线后监测成功率、延迟、数据漂移、审批和审计完整性；定期清理权限、复查规则和依赖；只有核心闭环稳定且新增 Action 的边际收益仍高于治理成本时才扩展范围。

## Caveats

成熟度与目标值必须结合场景风险解释。没有 Action 执行的展示系统不能用空执行集合制造虚高审计率；强监管场景保留人在环并不表示成熟度倒退。

## References

- 《本体论紫皮书》v2，第 5.8 节，PDF 第 95–98 页（ONT-OP-013、ONT-OP-014、ONT-OP-016）。
