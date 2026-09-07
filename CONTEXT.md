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

`plugins/calc-project` 是可安装计算工作流插件，共享计算模板位于 [resources/](plugins/calc-project/resources/)。

**计算工具脚本（Calculation Utility Script）**:
计算项目中可复用的可执行工具资产，用于辅助计算工作，但不作为生成任务输入的来源。
_Avoid_: 计算模板，任务专用脚本

关键索引词，完整定义仍以[领域术语](plugins/calc-project/skills/calc-project-structure/references/project-context.md)。为准：计算项目、计算项目结构、数据根、计算线、工作流、计算任务、运行、计算模板、项目计算模板、插件计算模板。

## Paper Project

`plugins/paper-project` 面向学术研究与论文工作；多个活动 skill 共用的写作资源位于插件内 [resources/](plugins/paper-project/resources/)。

## Plugin Resources

**skill 所属资源（skill-owned resource）**只服务一个 skill 并与其共置。agent 阅读的说明进入 `references/`；会复制到任务中的文件进入 `assets/`。其接口是 consuming skill 声明的精确相对路径。

**插件共享资源（plugin-shared resource）**由同一插件内至少两个活动 skill 实际消费，位于 `plugins/<plugin>/resources/`。共享目录 README 记录消费者，但不提供运行时发现索引。

当前没有 formal、candidate 或 incubating 资源状态，也没有通用知识消费协议或项目初始化机制。历史材料只可留在历史文档或 Cangjie 明确标记为非执行的 `references/legacy/`。

## OSM Project

`plugins/osm-project` 维护 Obsidian Self-Management（OSM）的项目日志工作流。
