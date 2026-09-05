# 仓库协作说明

本仓库集中维护 Codex 插件及其 skill 所属资源和插件共享资源。开始相关维护前读取根目录 [CONTEXT.md](CONTEXT.md)。

## 插件导航

- [calc-project](plugins/calc-project/)：科研计算项目结构、任务元数据、数据同步与 VASP、DMFT、NAMD、磁性计算工作流。计算输入与计算模板维护进入此插件。
- [paper-project](plugins/paper-project/)：文献整理、论文与学位论文写作、引用核验、科学图件和演示文稿。研究证据与学术表达任务进入此插件。
- [osm-project](plugins/osm-project/)：将当前对话中的项目进展整理为草稿，经确认后写入 Obsidian Daily Note。用户要求记录项目日志时进入此插件。

上游来源和常用 skill 功能见 [README.md](README.md)。选择具体 skill 时，核对所属插件的 `skill-lifecycle.json` 与该 skill 的 `SKILL.md`；停用入口仅在用户显式调用时使用。

## 工作入口

- 修改任一插件、插件清单、skill 或发布资源时，读取 `CONTEXT.md` 中对应章节。
- 修改 skill 生命周期状态时，读取 `CONTEXT.md` 的技能生命周期章节，更新所属插件的 `skill-lifecycle.json`，同步 `agents/openai.yaml` 调用策略，并在迁移日志记录转换。
- 审查 skill 生命周期变更时，将清单与基线 revision 对比，只接受“开发中 → 已发布 ⇄ 停用”；删除项的基线状态必须为停用。当前快照测试不替代这项历史审查。
- 修改 skill 所属资源、插件共享资源、计算模板或其消费路径时，读取 `CONTEXT.md` 的 Paper Project、Calc Project 和 Plugin Resources 章节。
- 核对迁移路径、旧目录、排除项或迁移状态时，读取 `docs/migrations/2026-09-04-plugin-consolidation.md`；历史迁移映射只在该日志维护。

## 仓库规则

- 插件发布单元位于 `plugins/<plugin-name>/`；单一 skill 使用的资源与该 skill 共置。
- 只有至少两个活动 skill 实际消费的资源才进入所属插件的 `resources/`；消费者直接声明精确相对路径。
- 修改资源消费 seam 时，联动验证 consuming skills、相对路径和插件发布包。
- 保留用户已有改动；提交只包含当前任务范围。
- 变更完成前运行与范围相称的测试，并在迁移日志记录跨目录迁移或运行时路径变更。
- 安装、发布、删除源仓库或改写外部环境需要用户明确授权。
