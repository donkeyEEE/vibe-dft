# 仓库协作说明

本仓库集中维护 Codex 插件及其插件本地实验知识。开始相关维护前读取根目录 [CONTEXT.md](CONTEXT.md)。

## 工作入口

- 修改任一插件、插件清单、skill 或发布资源时，读取 `CONTEXT.md` 中对应章节。
- 修改插件知识、知识卡片、计算模板、索引或其消费路径时，读取 `CONTEXT.md` 的 Paper Project、Calc Project 和 Plugin Knowledge 章节。
- 核对迁移路径、旧目录、排除项或迁移状态时，读取 `docs/migrations/2026-09-04-plugin-consolidation.md`；历史迁移映射只在该日志维护。

## 仓库规则

- 插件发布单元位于 `plugins/<plugin-name>/`；可选知识位于所属插件的 `knowledge/`，随插件发布。
- `knowledge/candidates/` 和 `knowledge/incubating/` 是非正式区；消费端只通过插件内正式索引读取 `cards/` 或 `templates/`。
- 修改知识消费边界时，联动验证对应插件、相对路径描述符和知识契约。
- 保留用户已有改动；提交只包含当前任务范围。
- 变更完成前运行与范围相称的测试，并在迁移日志记录跨目录迁移或运行时路径变更。
- 安装、发布、删除源仓库或改写外部环境需要用户明确授权。
