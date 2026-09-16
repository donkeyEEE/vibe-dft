# YZ Skills 开发上下文

本仓库集中维护四个 Codex 插件。插件发布单元位于 `plugins/`；资源优先与 owning skill 共置，只有多 skill 实际消费的资源进入插件级 `resources/`。

## 插件导航

定位任务所属插件时，读取 [AGENTS.md 的插件导航](AGENTS.md#插件导航)；了解常用 skill 的功能时，读取 [README.md](README.md)。

## Skill 收录与调用

**Skill roster**:
一个插件当前收录的 skill 集合，以该插件下实际存在的 `skills/*/SKILL.md` 为唯一事实源。

**调用策略（Invocation Policy）**:
Skill 是否允许 Codex 隐式选择的运行时策略；默认允许隐式调用，仅限用户主动调用的入口在 `agents/openai.yaml` 声明 `allow_implicit_invocation: false`。

**Skill Incubator**:
可安装、可发布并允许正常调用的通用 skill 试验场。Skill 是否继续留在其中或形成独立插件，由维护者根据领域边界、依赖与发布需要逐项决定。

## Calc Project 计算插件术语

`plugins/calc-project` 是可安装计算工作流插件。运行时计算模板和确定性辅助脚本属于唯一消费者 `calc-execute`，不属于插件共享资源。

**RQ Tracker**:
每个 RQ 用于存放 `RQ.md` 与已发布 Spec 的配置化存储约定；RQ 属于一条计算研究主线，本地 Markdown adapter 下对应 `<project-root>/01<main-line-slug>/01-rqs/<rq-id>-<slug>/`，不是独立状态文档。
_Avoid_: Tracker 数据库，进度缓存，session registry

**计算工具脚本（Calculation Utility Script）**:
计算项目中可复用的可执行工具资产，用于辅助计算工作，但不作为生成任务输入的来源。
_Avoid_: 计算模板，任务专用脚本

**计算监控器（Calculation Monitor）**:
由一次已记录的调度器提交启动、在本地独立等待该 Run 的作业离开活动队列并请求恢复原 Codex 线程的临时协调进程。它不判断 Run 成功，也不保存 Spec、Run 或科学验收状态。
_Avoid_: watcher，完成判定器，Run 状态数据库

**执行研究（Execution Research）**:
`calc-execute` 在任务执行中遇到不确定性时，为补充软件用法、输入格式、命令、环境要求、产物与机械校验规则而开展的临时研究。其结果先作为临时证据，只有经用户接受后才沉淀为计算规范；它不是任务级执行方案，也不取代 Spec 的科学权威。
_Avoid_: 通用 Run，任务级后端方案，搜索授权

**计算排障（Calculation Troubleshooting）**:
`calc-execute` 对异常计算任务定位问题、补充证据、提出方案并验证处置结果的执行流程；根因明确且满足原地纠正条件的异常进入简单纠错分支。
_Avoid_: 简单纠错，结果解释，Spec 修改

**Ask LYZ (`ask-lyz`)**:
Calc Project 面向用户的显式辅助入口，用于推荐工作接口、解释领域术语或查询进度；原名
`ask-dnk`，自 2026-09-13 起使用现名。过去文档中的旧名称保留为历史记录。
_Avoid_: ask-dnk（当前名称）

关键索引词，完整定义以 [calc-setup 领域术语](plugins/calc-project/skills/calc-setup/references/project-context.md) 为准：计算项目、计算项目结构、数据根、计算线、RQ、Spec、计算任务、运行、计算归属树（COT）、进展报告、计算汇报、汇报源数据、Run-local inputs、计算模板、项目计算模板、插件计算模板。

## Paper Project

`plugins/paper-project` 面向学术研究与论文工作；写作资源全部下放到实际消费它们的 skill 的 `references/`，不保留插件级 `resources/`。

**遮蔽续写测试（Masked Continuation Evaluation）**:
向受测 agent 只提供 Introduction 的可见前文与候选 skill，由其生成被遮蔽的后续论证；评估以修辞功能、科学内容兼容性、信息密度和无虚构为主，不要求逐字复现原文。
_Avoid_: 原文复现测试、字面续写测试

**开发集（Development Set）**:
在 skill 优化循环中可反复评估并用于定位规则缺陷的遮蔽续写样例集。
_Avoid_: 训练集

**验收集（Acceptance Set）**:
由 Introduction 数据快照固定，不向迭代循环暴露逐例反馈，只用于判定候选 skill 相对 baseline 是否真正改善的遮蔽续写样例集。只有显式重建数据快照才会重新抽取验收集。
_Avoid_: 测试集、开发集

**结构续写样例（Structural Continuation Case, SCC）**:
不提供未知研究结果，用于评估 skill 能否根据可见前文合理推进 Introduction 论证结构的遮蔽续写样例。
_Avoid_: 普通样本、无条件样本

**事实落地样例（Fact-Grounded Continuation Case, FGCC）**:
向受测 agent 额外提供去除原文措辞和修辞顺序的原子事实包，用于评估 skill 能否在不虚构的前提下将研究事实放入正确论证位置的遮蔽续写样例。
_Avoid_: 事实样本、有条件样本

**Introduction 数据快照（Introduction Dataset Snapshot）**:
由独立构建流程从用户指定的 Zotero 分类及子分类生成、供后续 skill 优化运行反复使用的本地 SCC 与 FGCC 集合。快照包含的论文原文与派生文本不进入 Git 或插件发布包，只有显式重建才更新。
_Avoid_: 训练数据集、临时样本集

## Plugin Resources

**skill 所属资源（skill-owned resource）**只服务一个 skill 并与其共置。agent 阅读的说明进入 `references/`；会复制到任务中的文件进入 `assets/`。其接口是 consuming skill 声明的精确相对路径。

**插件共享资源（plugin-shared resource）**由同一插件内至少两个活动 skill 实际消费，位于 `plugins/<plugin>/resources/`。共享目录 README 记录消费者，但不提供运行时发现索引。

Paper Project 不采用插件共享资源：即使另一插件中的 skill 使用相同内容，各插件也各自维护 skill-owned 副本，运行时不跨插件读取文件。Calc Project 当前也没有插件共享计算模板；所有运行时模板都与唯一消费者 `calc-execute` 共置。

**Skill 可执行接口（Skill Executable Interface）**：由 owning skill 提供、其他 skill 通过命令行调用的版本化行为 seam。实现及辅助资源仍归 owning skill；消费者只依赖命令、输入、输出与错误契约，不导入 sibling skill 的实现模块。Paper Project 的 `get-zotero content` 是此类接口，`get-notes` 与 `citation-validator` 通过它消费只读 Zotero artifact，因此不构成插件共享资源。
_Avoid_: sibling 共享脚本、插件共享资源、跨 skill Python 导入

当前没有 formal、candidate 或 incubating 资源状态，也没有通用知识消费协议或项目初始化机制。历史材料只可留在历史文档或 Cangjie 明确标记为非执行的 `references/legacy/`。

## OSM Project

`plugins/osm-project` 维护 Obsidian Self-Management（OSM）的项目日志工作流。

## Skill Incubator

`plugins/skill-incubator` 是可安装的通用 skill 试验场，收纳尚未形成独立插件边界的工作流。`prl-polishing` 在此继续提供通用物理论文逐段润色；Physical Review Introduction 的专用写作与重构由 Paper Project 的 `pr-intro` 负责。
