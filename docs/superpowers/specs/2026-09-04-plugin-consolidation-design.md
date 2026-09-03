# 插件统一仓库迁移设计

日期：2026-09-04

## 目标

在 `/home/donk/yz-skills` 建立单一 Git 仓库，集中维护当前开发版插件、共享的 `research-knowledge` 知识库和按需加载的项目上下文。首轮迁移只处理插件源码、共享知识库、上下文与仓库级代理说明；其他文档留在原仓库。

## 目标结构

```text
/home/donk/yz-skills/
├── AGENTS.md
├── CONTEXT-MAP.md
├── plugins/
│   ├── calc-project/
│   ├── dev-engineering/
│   ├── dev-incubator/
│   ├── dev-misc/
│   ├── dev-productivity/
│   ├── osm-project/
│   └── paper-project/
├── research-knowledge/
└── docs/
    ├── contexts/
    │   ├── calc-project.md
    │   ├── dev-project.md
    │   ├── osm-project.md
    │   ├── paper-project.md
    │   └── research-knowledge.md
    ├── migrations/
    │   └── 2026-09-04-plugin-consolidation.md
    └── superpowers/
        └── specs/
            └── 2026-09-04-plugin-consolidation-design.md
```

## 迁移范围

| 新路径 | 当前来源 | 类型 |
|---|---|---|
| `plugins/calc-project/` | `/home/donk/plugins/calc-project` 中确认后的插件源码 | 插件 |
| `plugins/dev-engineering/` | `/home/donk/plugins/dev-project/plugins/dev-engineering` | 插件 |
| `plugins/dev-incubator/` | `/home/donk/plugins/dev-project/plugins/dev-incubator` | 插件 |
| `plugins/dev-misc/` | `/home/donk/plugins/dev-project/plugins/dev-misc` | 插件 |
| `plugins/dev-productivity/` | `/home/donk/plugins/dev-project/plugins/dev-productivity` | 插件 |
| `plugins/osm-project/` | `/home/donk/plugins/osm-project-dev/osm-project` | 插件 |
| `plugins/paper-project/` | `/home/donk/plugins/paper-project/paper-project` | 插件 |
| `research-knowledge/` | `/home/donk/plugins/research-knowledge` | 共享知识依赖 |

`tender-master`、`fde-skills`、`knowledge-distillation`、参考仓库及其他项目文档不在首轮范围内。`calc-project` 当前未在仓库根部发现标准 `.codex-plugin/plugin.json`；实施前必须根据现有发布脚本、测试和构建输出确认其源码边界，不能把整个旧仓库不加区分地放入 `plugins/`。

## 内容保留与排除

迁移以源工作区的当前文件状态为准，保留已跟踪修改与未跟踪的有效源码，避免退回 Git HEAD 而丢失开发进度。

每个迁移单元排除：

- `.git/` 与嵌套 worktree 元数据；
- `.pytest_cache/`、`__pycache__/` 等缓存；
- `.worktrees/`、临时目录和明确可重建的构建产物；
- 不属于插件发布边界的旧仓库文档、参考副本和测试素材，除非插件运行或验证直接依赖它们。

原目录保持不变。统一仓库通过验证前，不删除、不重命名源文件。

## Context 架构

根 `AGENTS.md` 使用中文，承担始终适用的仓库规则。它只通过带触发条件的指针引用 `CONTEXT-MAP.md`，不复制各插件背景。

`CONTEXT-MAP.md` 是上下文导航的单一入口。每个条目必须列出：维护单元、目标路径、context 文件、旧路径、关键依赖，以及什么任务需要读取该 context。

旧 context 的迁移映射：

| Context | 来源 |
|---|---|
| `docs/contexts/calc-project.md` | `/home/donk/plugins/calc-project/CONTEXT.md` |
| `docs/contexts/dev-project.md` | `/home/donk/plugins/dev-project/CONTEXT.md` |
| `docs/contexts/osm-project.md` | `/home/donk/plugins/osm-project-dev/CONTEXT.md` |
| `docs/contexts/paper-project.md` | `/home/donk/plugins/paper-project/CONTEXT.md` |
| `docs/contexts/research-knowledge.md` | 从知识库现有契约和索引提炼 |

四个 `dev-*` 插件共用 `dev-project.md`，避免复制相同项目背景。只有出现插件专属且不能由共享 context 清楚表达的规则时，才新增插件级 context。

## 共享知识依赖

`research-knowledge` 是顶层共享数据仓库，不添加插件清单。首批已确认的直接消费者为 `calc-project` 和 `paper-project`。

迁移时检查并更新有效源码、配置、技能说明与测试中硬编码的 `/home/donk/plugins/research-knowledge`，使其解析到 `/home/donk/yz-skills/research-knowledge`。历史规格、归档材料中的旧路径作为历史事实保留，迁移日志说明其不参与运行。

知识库的写入治理、候选区、正式卡片、模板和索引边界保持不变；目录迁移不改变准入语义。

## 迁移日志

`docs/migrations/2026-09-04-plugin-consolidation.md` 记录：

- 每个源路径和目标路径；
- 复制时间及源 Git 分支、revision、dirty 状态；
- 保留的未提交修改和排除类别；
- 所有运行时路径重写；
- 未迁移项目及原因；
- 验证命令和结果。

## 验证与完成条件

迁移完成必须同时满足：

1. 七个插件目标目录均存在，标准插件均能找到并解析 `.codex-plugin/plugin.json`。
2. `calc-project` 的插件源码边界已被明确记录并通过其现有布局测试。
3. `research-knowledge` 的正式索引和模板边界通过现有验证器或等价测试。
4. 有效文件中不再依赖旧的 `/home/donk/plugins/research-knowledge` 运行时路径；历史文档命中已分类。
5. 根 `AGENTS.md`、`CONTEXT-MAP.md` 和五个 context 文件的所有相对路径均可解析。
6. 新仓库不存在嵌套 `.git/`、缓存目录或意外迁入的旧构建产物。
7. 各插件相关测试在统一仓库路径下通过；失败项必须在迁移日志中给出原因和处置状态。
8. 源仓库未被修改或删除。

## 非目标

首轮不导入各源仓库完整 Git 历史，不使用 submodule 或 subtree，不迁移普通 README、旧设计文档、参考仓库和知识蒸馏项目，也不安装或发布插件。
