# YZ Skills 开发上下文

本仓库集中维护七个 Codex 插件和一个共享研究知识库。插件发布单元位于 `plugins/`，共享内容源位于 `research-knowledge/`。维护单元、旧路径和依赖关系由 `CONTEXT-MAP.md` 导航。

## Calc Project

`plugins/calc-project` 是可安装计算工作流插件。领域术语由 `plugins/calc-project/skills/calc-project-structure/references/project-context.md` 统一定义，本节不维护第二份术语表。

计算模板的正式内容位于 `research-knowledge/templates/computation/`，候选经验卡位于 `research-knowledge/candidates/cards/calc-project/`。插件负责计算模板的语义和可执行验收；候选卡不能直接作为消费输入。

## Dev Project 插件组

本组包含 `dev-engineering`、`dev-incubator`、`dev-misc` 和 `dev-productivity`，共享以下术语但各自保有独立 manifest 和发布边界：

- **Engineering plugin**：`dev-engineering`，维护软件开发与维护工作流，中文称“工程插件”。
- **Productivity plugin**：`dev-productivity`，维护构思、决策、沟通和 agent-facing 文档工作流，中文称“设计插件”。
- **Issue tracker**：承载项目 issue 的工具，例如 GitHub Issues、Linear 或项目本地约定。
- **Issue**：Issue tracker 中单个可追踪工作单元。
- **Decision ticket**：`wayfinder` 使用的特殊子 Issue，承载需要形成决策的问题，不是实现切片。
- **Triage role**：triage 状态机施加到 Issue 的规范角色标签。

跨插件引用必须通过实际路径或明确依赖表达，不能依赖旧 `/home/donk/plugins/dev-project` 外层仓库结构。

## OSM Project

`plugins/osm-project` 维护 Obsidian Self-Management（OSM）的项目日志工作流。

- **Work Conversation**：仅在用户调用 `$log2ob` 或明确要求记录当前项目工作时才被总结的当前 Codex 对话。
- **Summary Draft**：等待用户确认的工作会话摘要；确认前不是日志。
- **Work Session Summary**：用户批准的极简项目状态，保留起点、进展、证据结论、关键未决事项和可执行恢复点。
- **Resume Point**：重新进入任务的第一个具体动作，包含动作、对象和完成条件。
- **Project Log**：上海时区某日 Daily Note 的 `### 项目日志` 下，以项目身份为四级标题保存的当前状态；重复写入执行状态合并而非追加历史。
- **Project Identity**：在同一 Daily Note 内可区分项目的最短人类可读名称。
- **State Merge**：新摘要用已确认变化替换旧状态，保留尚未解决且仍重要的信息。
- **Recordable Progress**：能降低恢复成本的有证据项目状态，排除秘密、个人数据、原始诊断转储和空活动报告。

Daily Summary、对话转录和自动推断内容不属于 Project Log。

## Paper Project

`plugins/paper-project` 面向学术研究与论文工作，并通过 Cangjie 与 `prl-shared` 治理顶层 `research-knowledge`。

- **物理卡片**：有可追溯来源支持的原子物理知识记录，分为概念、现象、理论与模型三类。
- **核心陈述**：由现有来源共同支持、可独立成立的最小知识陈述；来源特有解释单独保存。
- **已确立 / 有争议**：分别表示核心陈述目前无实质冲突，或来源在定义、解释、适用范围上存在实质分歧。
- **总索引**：`research-knowledge/cards/INDEX.md`，只提供一级导航。
- **物理索引**：`research-knowledge/cards/physics/PHYSICS_INDEX.md`，是物理卡片类型、状态和主题的唯一导航。
- **准入接口**：候选成为正式共享知识前必须满足的输入、门禁、人工确认、写入动作和完成条件。
- **消费协议**：消费端定位并只读使用正式卡片时遵循的共同读取顺序和异常处理规则。

共享卡片准入与索引治理属于 paper-project；计算模板的语义和可执行验收属于 calc-project。

## Research Knowledge

`research-knowledge/` 是共享内容源，不是可安装插件。`paper-project` 拥有 Cangjie 与 `prl-shared` 的准入和索引治理；`calc-project` 拥有计算模板的语义与可执行验收。

- `cards/`：已被正式索引登记的知识卡。
- `templates/`：已被 `templates/INDEX.md` 登记且满足计算验收的模板。
- `candidates/`：尚未完成治理的候选区，消费端不可读取、搜索或作为缺失知识的回退。

消费者每次显式查找共享知识时依次读取自身 `references/knowledge-source.yaml`、`research-knowledge/CONSUMER_CONTRACT.md`、相关正式索引，以及完成任务所需的最小正式资源集合。资源必须同时位于正式目录并被索引登记。

仓库、契约、索引或资源缺失或格式错误时，消费者应警告并在不使用共享知识的情况下继续，不回退到插件内旧副本。

正式卡片入口为 `research-knowledge/cards/INDEX.md`；物理卡由 `cards/physics/PHYSICS_INDEX.md` 导航；本体与 Agent 治理由 `cards/ontology/INDEX.md` 导航；计算模板入口为 `research-knowledge/templates/INDEX.md`。
