---
name: meta-separate-tbox-abox
type: method-constraint
tags: [domain/knowledge-engineering, task/ontology-design, concern/maintainability]
updated_at: 2026-08-18
---

# 分离 TBox 与 ABox 生命周期

相对稳定的术语公理 TBox 与高频变化的实例断言 ABox 应在架构和演化策略上分离，以控制推理成本、版本影响和数据更新风险。

## Caveats

分离不要求使用不同物理数据库；关键是生命周期、变更频率与推理策略能够独立治理。

## References

- 《本体论紫皮书》v2，第 3.3.5、3.6 节（ONT-SO-006、ONT-SO-011）。
