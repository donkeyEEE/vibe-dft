# YZ Skills 开发上下文

本仓库集中维护五个 Codex 插件。插件发布单元位于 `plugins/`；资源优先与 owning skill 共置，只有多 skill 实际消费的资源进入插件级 `resources/`。旧路径与迁移状态记录在 `docs/migrations/2026-09-04-plugin-consolidation.md`。

## 插件导航

**[calc-project](plugins/calc-project)**:
面向科研计算项目及其可执行工作流，管理项目结构、任务事实、受限同步、[共享计算模板](plugins/calc-project/resources/)和方法专属计算流程。

**[paper-project](plugins/paper-project)**:
面向研究论文与学位论文生产，组织文献证据、[共享写作资源](plugins/paper-project/resources/)、学术写作、引用核验、科学图件和汇报材料。Cangjie 保留为显式调用的停用入口，等待未来重新设计。

**[dev-productivity](plugins/dev-productivity)**:
面向软件产品定义、需求与方案设计，提供访谈澄清、领域建模、规格与任务分解、设计调研和原型验证等协作能力。

**[dev-engineering](plugins/dev-engineering)**:
面向已定义软件工作的工程交付，负责代码与架构实现、测试、调试、审查、请求分流和代码库维护。

**[osm-project](plugins/osm-project)**:
面向个人项目状态沉淀，将当前对话提炼为经确认的项目日志并写入 Obsidian Daily Note。

## 技能生命周期

Skill 本身是生命周期主体，不设置独立版本号；每个 Skill 在任一时刻只处于开发中、已发布或停用三种状态之一。状态沿“开发中 → 已发布 ⇄ 停用”转换。

**Skill 生命周期清单（Skill Lifecycle Registry）**:
所属插件维护的机器可读当前状态事实源，逐一标记 Skill 为开发中、已发布或停用。

**Skill 状态转换（Skill State Transition）**:
Skill 生命周期状态的改变；每次转换都在迁移日志记录原因、生效插件版本及适用的替代 Skill 或验证结果。

**开发中（In Development）**:
尚未进入过正式插件发布包的 Skill。

**已发布（Published）**:
已经进入正式插件发布包且允许 Codex 隐式调用的 Skill；后续维护不改变其已发布状态。

**停用（Explicit-only）**:
仍保留在所属插件中并允许用户显式调用，但 Codex 不得隐式调用的 Skill。
_Avoid_: 冻结

删除不是 Skill 的生命周期状态。Skill 只能从停用状态删除；删除后不再属于当前 Skill 集合，其旧路径和删除原因只保留在迁移日志中。

## Calc Project 计算插件术语

`plugins/calc-project` 是可安装计算工作流插件。

**计算工具脚本（Calculation Utility Script）**:
计算项目中可复用的可执行工具资产，用于辅助计算工作，但不作为生成任务输入的来源。
_Avoid_: 计算模板，任务专用脚本

关键索引词，完整定义仍以[领域术语](plugins/calc-project/skills/calc-project-structure/references/project-context.md)。为准：计算项目、计算项目结构、数据根、计算线、工作流、计算任务、运行、计算模板、项目计算模板、插件计算模板。

## Paper Project

`plugins/paper-project` 面向学术研究与论文工作；多个活动 skill 共用的写作资源位于插件内 `resources/`。Cangjie 当前停用且仅允许显式调用，未来另行设计。

## Plugin Resources

**skill 所属资源（skill-owned resource）**只服务一个 skill 并与其共置。agent 阅读的说明进入 `references/`；会复制到任务中的文件进入 `assets/`。其接口是 consuming skill 声明的精确相对路径。

**插件共享资源（plugin-shared resource）**由同一插件内至少两个活动 skill 实际消费，位于 `plugins/<plugin>/resources/`。共享目录 README 记录消费者，但不提供运行时发现索引。

当前没有 formal、candidate 或 incubating 资源状态，也没有通用知识消费协议或项目初始化机制。历史材料只可留在历史文档或 Cangjie 明确标记为非执行的 `references/legacy/`。


## Dev Project 插件组


## OSM Project

`plugins/osm-project` 维护 Obsidian Self-Management（OSM）的项目日志工作流。
