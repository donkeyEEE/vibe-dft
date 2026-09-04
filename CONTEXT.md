# YZ Skills 开发上下文

本仓库集中维护五个 Codex 插件。插件发布单元位于 `plugins/`，实验性知识随其所属插件维护；旧路径与迁移状态记录在 `docs/migrations/2026-09-04-plugin-consolidation.md`。

## 插件导航

**[calc-project](plugins/calc-project)**:
面向科研计算项目及其可执行工作流，管理项目结构、任务事实、受限同步、[插件本地计算知识](plugins/calc-project/knowledge/)和方法专属计算流程。

**[paper-project](plugins/paper-project)**:
面向研究论文与学位论文生产，组织文献证据、[插件本地论文知识](plugins/paper-project/knowledge/)、学术写作、引用核验、科学图件和汇报材料。

**[dev-productivity](plugins/dev-productivity)**:
面向软件产品定义、需求与方案设计，提供访谈澄清、领域建模、规格与任务分解、设计调研和原型验证等协作能力。

**[dev-engineering](plugins/dev-engineering)**:
面向已定义软件工作的工程交付，负责代码与架构实现、测试、调试、审查、请求分流和代码库维护。

**[osm-project](plugins/osm-project)**:
面向个人项目状态沉淀，将当前对话提炼为经确认的项目日志并写入 Obsidian Daily Note。


## Calc Project 计算插件术语

`plugins/calc-project` 是可安装计算工作流插件。

**计算工具脚本（Calculation Utility Script）**:
计算项目中可复用的可执行工具资产，用于辅助计算工作，但不作为生成任务输入的来源。
_Avoid_: 计算模板，任务专用脚本

关键索引词，完整定义仍以[领域术语](plugins/calc-project/skills/calc-project-structure/references/project-context.md)。为准：计算项目、计算项目结构、数据根、计算线、工作流、计算任务、运行、计算模板、项目计算模板、插件计算模板、候选经验卡。

## Paper Project

`plugins/paper-project` 面向学术研究与论文工作；可选的论文写作与期刊知识位于插件内 `knowledge/`。Cangjie 暂为开发者专用，其长期写入与治理模型尚未确定。


## Dev Project 插件组


## OSM Project

`plugins/osm-project` 维护 Obsidian Self-Management（OSM）的项目日志工作流。
