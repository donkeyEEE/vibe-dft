---
name: meta-read-action-writeback-validation
type: procedure
tags: [domain/knowledge-engineering, task/ontology-implementation, concern/validation]
updated_at: 2026-08-26
---

# Read—Action—Writeback 闭环验证

操作型 Ontology 上线前必须端到端验证 Read、决策、Action、Writeback、回读确认与审计链，只有只读展示或从未成功回写不能证明闭环成立。

## Procedure

在隔离环境准备可识别的测试对象；读取对象并记录数据版本；产生包含明确参数和理由的决策；执行前置条件与授权检查；调用 Action 并以幂等键写回记录系统；重新读取源系统和 Ontology，确认最终状态一致；核对审计中是否包含请求、规则、审批、结果和错误。再分别测试重复请求、超时、部分失败、补偿与人工接管。

## Caveats

闭环测试必须隔离真实副作用。一次成功的 happy path 不能替代失败路径、并发、回滚和权限测试。

## References

- 《本体论紫皮书》v2，第 5.2.5、5.8 节，PDF 第 70、79、95、97 页（ONT-OP-004、ONT-OP-005、ONT-OP-013、ONT-OP-014）。
