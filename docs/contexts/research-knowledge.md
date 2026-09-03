# Research Knowledge 上下文

`research-knowledge/` 是共享内容源，不是可安装插件。`paper-project` 拥有 Cangjie 与 `prl-shared` 的准入和索引治理；`calc-project` 拥有计算模板的语义与可执行验收。

## 边界

- `cards/`：已被正式索引登记的知识卡。
- `templates/`：已被 `templates/INDEX.md` 登记且满足计算验收的模板。
- `candidates/`：尚未完成治理的候选区，消费端不可读取、搜索或作为缺失知识的回退。

## 消费顺序

消费者每次显式查找共享知识时依次读取自身 `references/knowledge-source.yaml`、`research-knowledge/CONSUMER_CONTRACT.md`、相关正式索引，以及完成任务所需的最小正式资源集合。资源必须同时位于正式目录并被索引登记。

仓库、契约、索引或资源缺失或格式错误时，消费者应警告并在不使用共享知识的情况下继续，不回退到插件内旧副本。

正式卡片入口为 `research-knowledge/cards/INDEX.md`；物理卡继续由 `cards/physics/PHYSICS_INDEX.md` 导航；本体与 Agent 治理由 `cards/ontology/INDEX.md` 导航；计算模板入口为 `research-knowledge/templates/INDEX.md`。
