# Context Map

上下文正文统一位于根目录 `CONTEXT.md`。本文件只维护插件路径、迁移来源、依赖关系和任务定位；旧路径用于迁移追溯，不再作为维护入口。

| 维护单元 | 当前路径 | Context | 迁移来源 | 关键依赖 | 读取触发条件 |
|---|---|---|---|---|---|
| calc-project | `plugins/calc-project` | `CONTEXT.md#calc-project` | `/home/donk/03FGT/.codex/plugins/calc-project/calc-project` | `research-knowledge` 计算模板与候选卡 | 修改计算项目结构、VASP/DMFT/NAMD/Wannier/TB2J/VAMPIRE 工作流、同步、模板或清单时 |
| dev-engineering | `plugins/dev-engineering` | `CONTEXT.md#dev-project-插件组` | `/home/donk/plugins/dev-project/plugins/dev-engineering` | dev 插件共享术语 | 修改软件工程、评审、诊断、TDD、研究或向导 skill 时 |
| dev-incubator | `plugins/dev-incubator` | `CONTEXT.md#dev-project-插件组` | `/home/donk/plugins/dev-project/plugins/dev-incubator` | dev 插件共享术语 | 修改孵化中的实验性开发 skill 时 |
| dev-misc | `plugins/dev-misc` | `CONTEXT.md#dev-project-插件组` | `/home/donk/plugins/dev-project/plugins/dev-misc` | dev 插件共享术语 | 修改 Git 防护、迁移、脚手架或 pre-commit skill 时 |
| dev-productivity | `plugins/dev-productivity` | `CONTEXT.md#dev-project-插件组` | `/home/donk/plugins/dev-project/plugins/dev-productivity` | dev 插件共享术语 | 修改构思、沟通、教学或 agent 文档 skill 时 |
| osm-project | `plugins/osm-project` | `CONTEXT.md#osm-project` | `/home/donk/plugins/osm-project-dev/osm-project` | Obsidian 本地连接 | 修改日志写入、项目身份、状态合并或恢复点语义时 |
| paper-project | `plugins/paper-project` | `CONTEXT.md#paper-project` | `/home/donk/plugins/paper-project/paper-project` | `research-knowledge` 正式卡片与治理 | 修改论文、图表、引文、PPT、Cangjie、PRL 或共享知识治理 skill 时 |
| research-knowledge | `research-knowledge` | `CONTEXT.md#research-knowledge` | `/home/donk/plugins/research-knowledge` | 由 calc-project 与 paper-project 消费 | 修改卡片、模板、候选区、正式索引、消费协议或知识库路径时 |

## 跨单元读取

- `calc-project` 或 `paper-project` 涉及知识库读写、模板或路径时，同时参考 `CONTEXT.md` 的 Research Knowledge 章节。
- `research-knowledge/templates/` 变更同时参考 Calc Project 章节；卡片准入或治理变更同时参考 Paper Project 章节。
- 迁移来源、dirty 状态、过滤规则和验证证据见 `docs/migrations/2026-09-04-plugin-consolidation.md`。
