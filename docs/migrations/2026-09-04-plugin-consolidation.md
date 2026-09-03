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

已更新 27 个 `calc-project` 与 `paper-project` 的有效技能、配置、脚本索引、方法说明和配套 README。全仓剩余旧路径只出现在 `CONTEXT-MAP.md`、本迁移日志、迁移规格、实施计划及用于防止回归的测试常量中；这些命中均承担迁移追溯或测试用途，不参与运行时解析。

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
- 全仓旧路径扫描仅命中 `CONTEXT-MAP.md`、本迁移日志、迁移规格、实施计划和回归测试，均为追溯或测试用途。
- 旧开发仓库的分支、revision 和 dirty 条目数与迁移前一致：calc-project `main@38ecb7d`（4）、dev-project `main@f8faf0c`（1）、osm-project-dev `feat/log2ob@978ba49`（0）、paper-project `main@36db45c`（111）、research-knowledge `main@c8a8b73`（0）。复制过程未修改源仓库。

外层开发仓库中的历史测试、发布测试和参考素材测试未迁入统一仓库；它们依赖旧外层目录或明确属于首轮边界外。统一仓库使用根结构测试、插件 validator、知识库测试与插件内自带测试覆盖迁移后的发布边界。
