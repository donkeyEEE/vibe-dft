# Paper Project 开发上下文

`plugins/paper-project` 面向学术研究与论文工作，并通过 Cangjie 与 `prl-shared` 治理顶层 `research-knowledge`。

## 共享知识术语

**物理卡片**：有可追溯来源支持的原子物理知识记录，分为概念、现象、理论与模型三类。

**核心陈述**：由现有来源共同支持、可独立成立的最小知识陈述；来源特有解释单独保存。

**已确立 / 有争议**：分别表示核心陈述目前无实质冲突，或来源在定义、解释、适用范围上存在实质分歧。

**总索引**：`research-knowledge/cards/INDEX.md`，只提供一级导航。

**物理索引**：`research-knowledge/cards/physics/PHYSICS_INDEX.md`，是物理卡片类型、状态和主题的唯一导航。

**准入接口**：候选成为正式共享知识前必须满足的输入、门禁、人工确认、写入动作和完成条件。

**消费协议**：消费端定位并只读使用正式卡片时遵循的共同读取顺序和异常处理规则。

修改 Cangjie、`prl-shared`、PRL、paper2ppt 或其他知识消费者时，同时读取 `docs/contexts/research-knowledge.md`。写入治理属于 paper-project；计算模板的语义和可执行验收属于 calc-project。
