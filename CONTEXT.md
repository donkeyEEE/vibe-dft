# YZ Skills 开发上下文

本仓库集中维护五个 Codex 插件。插件发布单元位于 `plugins/`，实验性知识随其所属插件维护；维护单元、旧路径和依赖关系由 `CONTEXT-MAP.md` 导航。

## Calc Project 计算插件术语

`plugins/calc-project` 是可安装计算工作流插件。[领域术语](plugins/calc-project/skills/calc-project-structure/references/project-context.md)。

**计算工具脚本（Calculation Utility Script）**:
计算项目中可复用的可执行工具资产，用于辅助计算工作，但不作为生成任务输入的来源。
_Avoid_: 计算模板，任务专用脚本

以下名称是供仓库导航和跨插件检索使用的关键索引词；完整定义仍以 Calc Project 的领域术语表为准。
- **计算项目（Calculation Project）**：围绕一个研究目标组织的计算工作整体。
- **计算项目结构（Calculation Project Structure）**：由计算笔记结构与计算工作结构共同组成的项目管理层级。
- **数据根（Data Root）**：计算工作结构的项目级边界，容纳任务导航、计算线、计算任务及其执行产物。
- **计算线（Calculation Line）**：按科研关系组织一组计算任务的层级，不等同于工作流。
- **工作流（Workflow）**：连接多个计算任务的阶段顺序、依赖、交接产物和验收关系，不拥有任务身份。
- **计算任务（Calculation Task）**：具有独立科学目的、输入和生命周期状态的最小可独立跟踪单元。
- **运行（Run）**：一个计算任务的一次独立执行尝试；失败、取消或重跑仍是 Run，而非新任务。
- **计算模板（Calculation Template）**：可复用于生成任务输入的来源资产；按维护范围分为项目计算模板与插件计算模板。
- **项目计算模板（Project Calculation Template）**：面向特定项目或材料体系维护的计算模板，不自动成为共享正式资产。
- **插件计算模板（Plugin Calculation Template）**：随 calc-project 发布、通过插件内索引登记并完成验收、可由消费者发现的计算模板。
- **候选经验卡（Candidate Experience Card）**：保存计算实践观察、证据、条件与边界、等待治理的候选记录；它不是正式知识卡，也不是消费输入。

计算模板的语义与可执行验收由 calc-project 负责；候选经验卡经治理后可提炼为正式知识，但候选记录本身始终留在消费边界之外。

## Paper Project

`plugins/paper-project` 面向学术研究与论文工作；可选的论文写作与期刊知识位于插件内 `knowledge/`。Cangjie 暂为开发者专用，其长期写入与治理模型尚未确定。

## Plugin Knowledge

本上下文定义插件所拥有并随其发布的可选知识资产，以及这些资产的正式性、类型和消费边界。

**插件本地知识（Plugin-local Knowledge）**:
归属于单个插件发布边界、供该插件的可选知识能力使用的知识资产集合，当前包括知识卡片、候选卡片和计算模板。
_Avoid_: 插件知识，插件本地知识库，共享知识库

**知识卡片（Knowledge Card）**:
可由插件的知识能力消费、围绕单一知识对象组织的正式知识单元。
_Avoid_: 候选卡片，正式知识卡片，原始资料

**候选卡片（Candidate Card）**:
尚未成为知识卡片的提案，可以承载物理、本体论或论文写作等主题。
_Avoid_: 知识卡片，孵化知识，本体卡片

**知识消费协议（Knowledge Consumption Protocol）**:
约束知识消费者何时选择插件本地知识、选择哪些知识以及如何将其用于当前任务的共同规则。
_Avoid_: 消费方法，读取步骤，知识同步

**物理卡片（Physics Card）**:
记录物理概念、物理现象或物理理论与模型的知识卡片。
_Avoid_: 候选卡片，本体卡片，计算经验卡

## Dev Project 插件组


## OSM Project

`plugins/osm-project` 维护 Obsidian Self-Management（OSM）的项目日志工作流。
