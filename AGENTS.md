# 仓库协作说明

本仓库集中维护 Codex 插件及其 skill 所属资源和插件共享资源。开始相关维护前读取根目录 [CONTEXT.md](CONTEXT.md)。

## 插件导航

- [calc-project](plugins/calc-project/)：管理科研计算项目配置、RQ、Spec、整份 Spec 执行、prepared Run 瞬时评审、Issue 调研和计算汇报；`ask-lyz` 提供显式插件使用说明与路由辅助，`show-cot` 提供从既有权威记录派生的显式只读执行总览。稳定术语见[插件共享领域词汇](plugins/calc-project/resources/project-context.md)，Run 输入、执行模板和同步工具由 `calc-execute` 所有。
- [paper-project](plugins/paper-project/)：文献整理、论文与学位论文写作、引用核验和科学图件。研究证据与学术表达任务进入此插件。
- [osm-project](plugins/osm-project/)：将当前对话中的项目进展整理为草稿，经确认后写入 Obsidian Daily Note。用户要求记录项目日志时进入此插件。
- [skill-incubator](plugins/skill-incubator/)：维护尚未形成独立插件边界的可安装 skill，包括通用物理论文润色与演示文稿工作流。

上游来源和常用 skill 功能见 [README.md](README.md)。插件的 `skills/*/SKILL.md` 目录集合是 Skill roster；选择具体 skill 时读取其 `SKILL.md`。调用策略以该 skill 的 `agents/openai.yaml` 为准。

## 版本安装边界

原版与汉化版是互斥的整套发行版本；任一 Codex 环境同一时刻只能安装其中一版。
`calc-project`、`paper-project`、`osm-project` 和 `skill-incubator` 必须全部来自同一版本，
不得混用原版与汉化版插件。切换版本时，切换整套 marketplace 来源并重新安装所需插件，
然后新建对话。

## 工作入口

- 修改任一插件、插件清单、skill 或发布资源时，读取 `CONTEXT.md` 中对应章节。
- 修改 skill 的隐式调用能力时，更新其 `agents/openai.yaml`；默认允许隐式调用，只有仅限用户显式调用的入口才声明 `allow_implicit_invocation: false`。
- 新增或删除 skill 时，直接修改所属插件的 `skills/` 目录并按普通代码审查验证；仓库不维护 skill 生命周期状态或独立 roster 清单。
- 修改 skill 所属资源、插件共享资源、计算模板或其消费路径时，读取 `CONTEXT.md` 的 Paper Project、Calc Project 和 Plugin Resources 章节。
- Paper Project 的写作资源全部与 consuming skill 共置于 `references/`，不使用插件级 `resources/`。

## 仓库规则

- 设计插件或 skill 时，相信智能体的判断与执行能力：明确目标、接口和完成标准，并为实现保留自主空间；只为安全、权限、不可逆操作或已验证的稳定性要求增加行为限制。
- 插件发布单元位于 `plugins/<plugin-name>/`；单一 skill 使用的资源与该 skill 共置。
- 只有至少两个活动 skill 实际消费的资源才进入所属插件的 `resources/`；消费者直接声明精确相对路径。
- 修改资源消费 seam 时，联动验证 consuming skills、相对路径和插件发布包。
- 明确产生新版本号时，在根目录 `CHANGELOG.md` 顶部记录版本号、日期和修改内容。
- 保留用户已有改动；提交只包含当前任务范围。
- 变更完成前运行与范围相称的测试。
- 安装、发布或删除源仓库需要用户明确授权。
- 外部环境中的提交、同步、取消、扩大资源或成本、删除，以及超出当前工作范围的覆盖操作通常需要用户明确授权。用户请求推进一份选定 Spec 或已接受 RQ 时，`calc-execute` 与 `calc-to-spec` 可在该目标和用户明确约束内自主处理执行及渐进式 Spec 发布、替换；已 `concluded` Spec 的修改或重开仍需针对具体变更的人工授权。其他工作流沿用各自的授权规则。

## Agent skills

### Issue tracker

Issues and specs are tracked as local Markdown files under `.scratch/`. See `docs/agents/issue-tracker.md`.

### Domain docs

This repository uses a single-context domain documentation layout. See `docs/agents/domain.md`.
