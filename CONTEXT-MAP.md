# Context Map

上下文正文统一位于根目录 `CONTEXT.md`。本文件只维护插件路径、迁移来源、依赖关系和任务定位；旧路径用于迁移追溯，不再作为维护入口。

| 维护单元 | 当前路径 | Context | 迁移来源 | 关键依赖 | 读取触发条件 |
|---|---|---|---|---|---|
| calc-project | `plugins/calc-project` | `CONTEXT.md#calc-project` | `/home/donk/03FGT/.codex/plugins/calc-project/calc-project` | 插件内 `knowledge/` 的模板、物理卡、候选卡与孵化内容 | 修改计算项目结构、VASP/DMFT/NAMD/Wannier/TB2J/VAMPIRE 工作流、同步、知识、模板或清单时 |
| dev-engineering | `plugins/dev-engineering` | `CONTEXT.md#dev-project-插件组` | `/home/donk/plugins/dev-project/plugins/dev-engineering` | dev 插件共享术语 | 修改软件工程、评审、诊断、TDD、研究或向导 skill 时 |
| dev-productivity | `plugins/dev-productivity` | `CONTEXT.md#dev-project-插件组` | `/home/donk/plugins/dev-project/plugins/dev-productivity` | dev 插件共享术语 | 修改构思、沟通、教学或 agent 文档 skill 时 |
| osm-project | `plugins/osm-project` | `CONTEXT.md#osm-project` | `/home/donk/plugins/osm-project-dev/osm-project` | Obsidian 本地连接 | 修改日志写入、项目身份、状态合并或恢复点语义时 |
| paper-project | `plugins/paper-project` | `CONTEXT.md#paper-project` | `/home/donk/plugins/paper-project/paper-project` | 插件内 `knowledge/` 的论文写作与期刊卡片 | 修改论文、图表、引文、PPT、Cangjie、PRL 或插件知识时 |

## 已迁移内容源

- `/home/donk/plugins/research-knowledge` 曾迁入顶层 `research-knowledge/`；其内容现按 ADR 0001 分别位于 `plugins/paper-project/knowledge/` 与 `plugins/calc-project/knowledge/`，顶层目录不再是维护单元。

## 跨单元读取

- `calc-project` 或 `paper-project` 涉及知识目录、模板、卡片或消费路径时，同时参考 `CONTEXT.md` 的 Plugin Knowledge 章节。
- `plugins/calc-project/knowledge/templates/` 变更同时参考 Calc Project 章节；Cangjie 或 paper 卡片变更同时参考 Paper Project 章节。
- 迁移来源、dirty 状态、过滤规则和验证证据见 `docs/migrations/2026-09-04-plugin-consolidation.md`。
