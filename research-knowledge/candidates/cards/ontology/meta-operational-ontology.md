---
name: meta-operational-ontology
type: concept
tags: [domain/knowledge-engineering, task/ontology-design, task/architecture-selection]
updated_at: 2026-08-26
---

# 操作型 Ontology

操作型 Ontology 是把业务对象与受控 Action、计算 Function 和外部 Writeback 连接起来的决策运行模型，其验收终点是可审计的状态改变而非对象展示。

## Definition and distinction

Object 与 Link 表达当前业务状态；Function 封装可复用计算；Action 声明允许发生的状态改变、条件、授权和副作用；Writeback 把结果提交给记录系统；界面、Workflow 或 Agent 只是这些能力的消费者。它不同于以逻辑蕴含为核心的语义本体，也不同于只有对象页面和查询能力的只读数据层。

## Caveats

Palantir Ontology 是来源中的主要实现。通用职责可以迁移，但 SDK、部署和平台能力必须按当前官方文档重新核对。

## References

- 《本体论紫皮书》v2，第 5.1–5.2.5 节，PDF 第 68–79 页（ONT-OP-001、ONT-OP-002、ONT-OP-005）。
