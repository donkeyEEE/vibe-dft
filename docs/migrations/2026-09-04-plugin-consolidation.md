# 插件统一仓库迁移记录

日期：2026-09-04

## 迁移范围

| 维护单元 | 源路径 | 源分支 | 源 revision | 初始状态 | 目标路径 |
|---|---|---|---|---|---|
| calc-project | `/home/donk/03FGT/.codex/plugins/calc-project/calc-project` | 由外层 `calc-project` 仓库维护 | `38ecb7d` | 外层仓库 dirty | `plugins/calc-project/` |
| dev-engineering | `/home/donk/plugins/dev-project/plugins/dev-engineering` | `main` | `f8faf0c` | dirty | `plugins/dev-engineering/` |
| dev-incubator | `/home/donk/plugins/dev-project/plugins/dev-incubator` | `main` | `f8faf0c` | dirty | `plugins/dev-incubator/` |
| dev-misc | `/home/donk/plugins/dev-project/plugins/dev-misc` | `main` | `f8faf0c` | dirty | `plugins/dev-misc/` |
| dev-productivity | `/home/donk/plugins/dev-project/plugins/dev-productivity` | `main` | `f8faf0c` | dirty | `plugins/dev-productivity/` |
| osm-project | `/home/donk/plugins/osm-project-dev/osm-project` | `feat/log2ob` | `978ba49` | clean | `plugins/osm-project/` |
| paper-project | `/home/donk/plugins/paper-project/paper-project` | `main` | `36db45c` | dirty | `plugins/paper-project/` |
| research-knowledge | `/home/donk/plugins/research-knowledge` | `main` | `c8a8b73` | clean | `research-knowledge/` |

`calc-project` 外层仓库中的 `calc-project/calc-project` 是指向上述源路径的绝对符号链接。迁移必须复制链接目标内容，目标仓库不保留该机器相关链接。

## 复制规则

迁移读取各源工作区的当前状态，包括有效的已跟踪修改和未跟踪源码。统一排除 `.git/`、`.worktrees/`、`.pytest_cache/`、`__pycache__/`、`.scratch/`、`dist/` 与其他可重建缓存。源目录保持不变。

复制于 2026-09-04（Asia/Shanghai）执行。七个 manifest 均已复制并与目标目录同名；目标树没有断裂符号链接或被排除的目录。`calc-project` 使用解引用复制，目标中保存实际文件而非旧绝对符号链接。

## 暂不迁移

- `tender-master`：当前是独立 skill，不是本轮已确认插件。
- `fde-skills`：未发现本轮需要迁移的插件发布单元。
- `knowledge-distillation`：属于项目数据，不是插件或共享正式知识库。
- 各外层开发仓库的普通 README、旧设计文档、reference 副本及测试素材：首轮仅迁移插件发布边界所需内容。

## 路径重写

实施阶段将运行时依赖 `/home/donk/plugins/research-knowledge` 改为 `/home/donk/yz-skills/research-knowledge`。历史规格、计划和归档中的旧路径保留为历史事实，并从运行时扫描中显式排除。

已更新 27 个 `calc-project` 与 `paper-project` 的有效技能、配置、脚本索引、方法说明和配套 README。全仓剩余旧路径只出现在本迁移日志、迁移规格、实施计划及用于防止回归的测试常量中；这些命中均承担迁移追溯或测试用途，不参与运行时解析。

## Context 后续调整

2026-09-04 根据维护规模将五份 `docs/contexts/*.md` 合并为根目录 `CONTEXT.md`。`AGENTS.md` 直接指向合并正文；维护单元和当前依赖收敛到 `CONTEXT.md`，历史迁移来源由本日志维护。原迁移规格与实施计划保留当时的拆分设计，作为历史决策记录。

## 验证记录

- 路径迁移阶段 `pytest -q tests/test_repository_layout.py`：6 passed；加入缓存防护后最终为 7 passed。
- `pytest -q research-knowledge/tests`：14 passed。
- `python plugins/paper-project/skills/prl-shared/scripts/validate_knowledge_repository.py research-knowledge`：退出码 0，解析到 `/home/donk/yz-skills/research-knowledge`。

最终验证（均使用禁用 pytest 缓存和字节码写入的方式执行）：

- 七个 `.codex-plugin/plugin.json` 均通过 `python -m json.tool`。
- 结构与知识库联合测试：21 passed。
- 七个插件逐一通过官方 `validate_plugin.py`。
- `plugins/paper-project/tests`：28 passed。
- 知识库验证器再次返回退出码 0。
- 全仓旧路径扫描仅命中本迁移日志、迁移规格、实施计划和回归测试，均为追溯或测试用途。
- 旧开发仓库的分支、revision 和 dirty 条目数与迁移前一致：calc-project `main@38ecb7d`（4）、dev-project `main@f8faf0c`（1）、osm-project-dev `feat/log2ob@978ba49`（0）、paper-project `main@36db45c`（111）、research-knowledge `main@c8a8b73`（0）。复制过程未修改源仓库。

外层开发仓库中的历史测试、发布测试和参考素材测试未迁入统一仓库；它们依赖旧外层目录或明确属于首轮边界外。统一仓库使用根结构测试、插件 validator、知识库测试与插件内自带测试覆盖迁移后的发布边界。

## 后续移除

2026-09-04，应维护请求从统一仓库移除 `dev-incubator` 与 `dev-misc` 两个插件发布单元。迁移范围表和历史规格、计划继续保留其最初迁入事实；当前维护单元以根 `CONTEXT.md` 和结构测试为准。

## Context Map 移除

2026-09-04，根目录只保留一份 `CONTEXT.md` 后，`CONTEXT-MAP.md` 不再提供有效的分层导航，因此予以删除。当前维护单元与依赖在 `CONTEXT.md` 维护；旧路径和迁移状态只在本日志维护。历史规格与计划中的 `CONTEXT-MAP.md` 引用保留为当时设计记录。

## 插件知识本地化

2026-09-04，根据 [ADR 0001](../adr/0001-localize-experimental-plugin-knowledge.md) 将尚处测试阶段、没有实际跨插件正式消费者的顶层 `research-knowledge/` 拆回插件发布边界：

- `cards/atoms/` 与空的 paper 候选入口迁入 `plugins/paper-project/knowledge/`；
- `templates/`、`cards/physics/`、calc-project 候选卡和模板候选迁入 `plugins/calc-project/knowledge/`；
- ontology 正式卡与候选卡迁入 `plugins/calc-project/knowledge/incubating/ontology/`，不进入 calc 正式索引；
- 原知识库测试按内容所有者迁入两个插件的 `tests/knowledge/`；
- 消费端 `knowledge-source.yaml` 改为相对描述符自身解析 `../../../knowledge`，不再依赖宿主机绝对路径；
- 顶层 `research-knowledge/` 在迁移完成后删除，不保留副本或运行时回退。

Cangjie 暂为开发者专用流程；本次迁移只更新其开发路径，不决定未来的写入、准入、晋升或治理模型。

本地化验证结果：

- 根结构与两个插件知识测试：`24 passed`；
- paper-project 本地知识验证器：退出码 0；
- calc-project 与 paper-project 官方插件验证器：均通过；
- paper-project marketplace 发布构建通过，归档包含本地消费契约、卡片索引与卡片正文；
- 迁移清点为 paper atoms 31、physics 39、ontology 正式卡 40、ontology 候选 24、计算模板 14、calc 候选卡 12；
- 顶层 `research-knowledge/` 不再存在，两个插件的活动文件均无旧绝对路径命中。

## Dev 插件职责重划分

2026-09-04，根据 [ADR 0002](../adr/0002-separate-software-design-from-engineering-delivery.md) 将 Dev Project 插件按“软件产品定义与设计 / 工程交付”重划分：

- `domain-modeling`、`grill-with-docs`、`prototype`、`research`、`to-spec`、`to-tickets` 和 `wayfinder` 从 `dev-engineering` 迁入 `dev-productivity`；
- `triage`、`ask-matt`、`setup-matt-pocock-skills`、实现、测试、调试、审查与代码库维护 skills 保留在 `dev-engineering`，没有新增拆分或兼容 skill；
- 两插件继续独立安装；保留的 engineering 工作流通过延迟检查调用 `$dev-productivity:*`，迁入 productivity 的规格、工单和 wayfinding 工作流通过对称规则调用 `$dev-engineering:setup-matt-pocock-skills`；
- 两个 manifest 与 skills README 已按新的发布边界更新，活动文件中不再引用迁移前的七个 `$dev-engineering:*` 名称或旧目录。

验证记录：

- 七个迁移后的 skills 分别通过 `quick_validate.py`；
- `dev-engineering` 与 `dev-productivity` 分别通过官方 `validate_plugin.py`；
- 新增的 Dev skill 所有权和命名空间测试：`2 passed`；
- 删除已经失效、要求根 `CONTEXT.md` 重复 Calc Project 中英双语术语正文的测试后，全仓结构测试：`10 passed`。
