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

## 验证记录

尚未执行迁移验证。
