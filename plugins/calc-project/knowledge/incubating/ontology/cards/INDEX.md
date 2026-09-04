# Incubating Ontology and Agent Governance Index

本索引只维护孵化区内部清单，不授予正式消费可见性。内容分为本体与推理、Agent
治理及两者的组合边界；所有卡片保留自身 References 与 Caveats。

## Ontology, reasoning, and knowledge engineering

- [meta-semantic-ontology](meta-semantic-ontology.md) — 语义本体的角色与边界
- [meta-description-logic](meta-description-logic.md) — 描述逻辑与 OWL DL 推理基础
- [meta-open-closed-world-assumptions](meta-open-closed-world-assumptions.md) — 开放世界与封闭世界假设
- [meta-separate-tbox-abox](meta-separate-tbox-abox.md) — 分离 TBox 与 ABox
- [meta-owl-shacl-complementarity](meta-owl-shacl-complementarity.md) — OWL 与 SHACL 的互补职责
- [meta-ontology-five-components](meta-ontology-five-components.md) — 本体五件套教学框架
- [meta-semantic-ontology-engineering-loop](meta-semantic-ontology-engineering-loop.md) — 本体工程迭代流程
- [meta-semantic-ontology-architecture-selection](meta-semantic-ontology-architecture-selection.md) — 语义架构选择
- [meta-semantic-ontology-reference-implementation](meta-semantic-ontology-reference-implementation.md) — 参考实现路径
- [meta-airworthiness-semantic-ontology-case](meta-airworthiness-semantic-ontology-case.md) — 适航语义案例

### Knowledge graph engineering

- [meta-graph-schema-instance-query-workflow](meta-graph-schema-instance-query-workflow.md) — Schema、实例与查询三层工作流
- [meta-graph-instance-governance-pipeline](meta-graph-instance-governance-pipeline.md) — 图谱实例治理管线
- [meta-tiered-entity-resolution](meta-tiered-entity-resolution.md) — 分级实体消歧
- [meta-versioned-graph-schema-migration](meta-versioned-graph-schema-migration.md) — 版本化图谱 Schema 迁移
- [meta-use-case-first-graph-mvp](meta-use-case-first-graph-mvp.md) — 用例优先的图谱 MVP
- [meta-financial-hidden-association-graph-case](meta-financial-hidden-association-graph-case.md) — 金融隐藏关联图谱案例
- [meta-drug-repurposing-graph-case](meta-drug-repurposing-graph-case.md) — 药物重定位图谱案例

### Operational ontology

- [meta-operational-ontology](meta-operational-ontology.md) — 操作型 Ontology 的角色与边界
- [meta-action-first-operational-modeling](meta-action-first-operational-modeling.md) — Action 优先的操作型建模
- [meta-operational-action-contract](meta-operational-action-contract.md) — 操作型 Action 契约
- [meta-read-action-writeback-validation](meta-read-action-writeback-validation.md) — Read—Action—Writeback 闭环验证
- [meta-operational-ontology-lifecycle](meta-operational-ontology-lifecycle.md) — 操作型 Ontology 生命周期
- [meta-supply-disruption-decision-loop-case](meta-supply-disruption-decision-loop-case.md) — 供应链断供决策闭环案例
- [meta-flight-rerouting-decision-loop-case](meta-flight-rerouting-decision-loop-case.md) — 航班改航决策闭环案例
- [meta-grid-fault-operation-loop-case](meta-grid-fault-operation-loop-case.md) — 配电网故障操作闭环案例
- [meta-retail-inventory-decision-loop-case](meta-retail-inventory-decision-loop-case.md) — 零售库存决策闭环案例

## Agent ontology and governance

- [meta-agent-ontology](meta-agent-ontology.md) — Agent 本体的建模范围
- [meta-four-layer-agent-harness](meta-four-layer-agent-harness.md) — 四层 Agent harness
- [meta-agent-harness-reference-loop](meta-agent-harness-reference-loop.md) — Agent harness 参考闭环
- [meta-agent-harness-deployment-selection](meta-agent-harness-deployment-selection.md) — 部署形态选择
- [meta-agent-component-responsibility-separation](meta-agent-component-responsibility-separation.md) — 组件职责分离
- [meta-agent-tool-contract](meta-agent-tool-contract.md) — 工具契约
- [meta-agent-sop-externalization](meta-agent-sop-externalization.md) — SOP 外部化
- [meta-agent-traceability](meta-agent-traceability.md) — 可追溯性
- [meta-validate-agent-proposals-before-execution](meta-validate-agent-proposals-before-execution.md) — 执行前适用门禁
- [meta-agent-governance-regression-evaluation](meta-agent-governance-regression-evaluation.md) — 治理回归评估
- [meta-graphrag-evidence-is-not-governance](meta-graphrag-evidence-is-not-governance.md) — GraphRAG 证据与治理的区别
- [meta-refund-agent-governance-case](meta-refund-agent-governance-case.md) — 退款 Agent 案例
- [meta-maintenance-agent-governance-case](meta-maintenance-agent-governance-case.md) — 维护 Agent 案例

## Composition boundary

- [meta-semantic-knowledge-agent-governance-composition](meta-semantic-knowledge-agent-governance-composition.md) — 语义、知识与治理层的有限保证

## Tag navigation

新增工作实例使用以下单层 tags：

- `case/finance` — 金融风控与运营案例
- `case/life-sciences` — 生命科学研发案例
- `case/supply-chain` — 供应链运营案例
- `case/energy` — 能源与电网案例
- `case/retail` — 零售运营案例

`case/aviation` 继续用于民航实例；流程卡沿用 `task/ontology-design`、
`task/ontology-implementation`、`task/workflow-design`、`concern/quality`、
`concern/validation`、`concern/maintainability` 与 `concern/traceability`。
