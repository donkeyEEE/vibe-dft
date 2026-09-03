# 仓库协作说明

本仓库集中维护 Codex 插件及其共享研究知识。开始工作时，先按任务类型查阅 [CONTEXT-MAP.md](CONTEXT-MAP.md)，只加载命中的 context。

## 工作入口

- 修改任一插件、插件清单、skill 或发布资源时，读取地图中该插件对应的 context。
- 修改共享知识库、知识卡片、计算模板、索引或其消费路径时，读取 `docs/contexts/research-knowledge.md`，并同时读取受影响消费者的 context。
- 核对迁移路径、旧目录、排除项或迁移状态时，读取 `docs/migrations/2026-09-04-plugin-consolidation.md`；迁移映射只在 `CONTEXT-MAP.md` 和该日志维护。

## 仓库规则

- 插件发布单元位于 `plugins/<plugin-name>/`；共享知识库位于 `research-knowledge/`，不是可安装插件。
- `research-knowledge/candidates/` 是候选区；消费端只通过正式索引读取 `cards/` 或 `templates/`。
- 修改共享依赖时，联动验证 `calc-project`、`paper-project` 和知识库契约。
- 保留用户已有改动；提交只包含当前任务范围。
- 变更完成前运行与范围相称的测试，并在迁移日志记录跨目录迁移或运行时路径变更。
- 安装、发布、删除源仓库或改写外部环境需要用户明确授权。
