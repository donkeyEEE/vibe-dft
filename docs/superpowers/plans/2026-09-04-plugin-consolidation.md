# 插件统一仓库迁移实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将七个开发版插件及共享 `research-knowledge` 无损汇入 `/home/donk/yz-skills`，建立中文代理导航、上下文地图和可验证的单仓库维护边界。

**Architecture:** 插件发布单元扁平放入 `plugins/`，共享知识库作为顶层兄弟目录。复制当前工作区实态但过滤仓库元数据和缓存；运行时路径统一改到新根目录，历史文档中的旧路径保留并分类。根 `AGENTS.md` 只保存常驻规则，详细背景经 `CONTEXT-MAP.md` 按任务触发加载。

**Tech Stack:** Git、Bash、Python、pytest、Codex 插件 JSON/YAML/Markdown 资源。

**Spec:** `docs/superpowers/specs/2026-09-04-plugin-consolidation-design.md`

## Global Constraints

- 源目录只读：不删除、不重命名、不改写 `/home/donk/plugins` 与 `/home/donk/03FGT/.codex/plugins/calc-project/calc-project`。
- 复制源工作区当前状态，包括有效的未提交和未跟踪源码。
- 排除 `.git/`、`.worktrees/`、`.pytest_cache/`、`__pycache__/`、`.scratch/`、`dist/` 与可重建缓存。
- `research-knowledge` 位于仓库根目录，不添加插件 manifest。
- 首轮不迁移普通项目文档、reference 副本、`tender-master`、`fde-skills` 或 `knowledge-distillation`。
- 每个任务验证通过后单独提交；不得自动安装或发布插件。

---

### Task 1: 建立迁移清单与结构契约

**Files:**
- Create: `tests/test_repository_layout.py`
- Create: `docs/migrations/2026-09-04-plugin-consolidation.md`

**Interfaces:**
- Consumes: 设计规格中的八个迁移单元与排除规则。
- Produces: `EXPECTED_PLUGINS`、仓库结构断言、可持续更新的迁移审计记录。

- [ ] **Step 1: 写结构测试**

创建 `tests/test_repository_layout.py`，断言七个插件目录、每个 `.codex-plugin/plugin.json`、顶层 `research-knowledge/cards/INDEX.md`、`research-knowledge/templates/INDEX.md`、`AGENTS.md`、`CONTEXT-MAP.md` 和五个 context 文件存在；递归断言目标树中除根仓库外没有 `.git`，没有 `.pytest_cache`、`__pycache__`、`.worktrees`、`.scratch` 或 `dist` 目录。

- [ ] **Step 2: 运行测试并确认红灯**

Run: `pytest -q tests/test_repository_layout.py`

Expected: FAIL，至少报告 `plugins/calc-project` 或 `AGENTS.md` 不存在。

- [ ] **Step 3: 写迁移日志骨架**

记录八个源路径、当前分支、revision、dirty 状态和过滤规则。明确 `calc-project` 的有效来源是 `/home/donk/03FGT/.codex/plugins/calc-project/calc-project`，旧仓库中的 `calc-project/calc-project` 仅为绝对符号链接。

- [ ] **Step 4: 提交契约**

```bash
git add tests/test_repository_layout.py docs/migrations/2026-09-04-plugin-consolidation.md
git commit -m "test: define consolidated repository layout"
```

### Task 2: 复制插件与共享知识库

**Files:**
- Create: `plugins/calc-project/**`
- Create: `plugins/dev-engineering/**`
- Create: `plugins/dev-incubator/**`
- Create: `plugins/dev-misc/**`
- Create: `plugins/dev-productivity/**`
- Create: `plugins/osm-project/**`
- Create: `plugins/paper-project/**`
- Create: `research-knowledge/**`
- Modify: `docs/migrations/2026-09-04-plugin-consolidation.md`

**Interfaces:**
- Consumes: Task 1 的固定目标目录和过滤规则。
- Produces: 七个自包含插件目录与一个非插件共享知识库。

- [ ] **Step 1: 复制七个插件**

使用 `rsync -aL` 复制 `calc-project` 链接目标，使用 `rsync -a` 复制其余六个插件。每次复制应用同一排除集：`.git`、`.worktrees`、`.pytest_cache`、`__pycache__`、`.scratch`、`dist`。源与目标映射严格采用规格表，不从外层开发仓库附带 README、docs、reference 或 tests。

- [ ] **Step 2: 复制共享知识库**

使用相同元数据与缓存排除集复制 `/home/donk/plugins/research-knowledge/` 到 `research-knowledge/`；保留其 README、契约、cards、templates、tests 和有效未跟踪内容。

- [ ] **Step 3: 核验清单和符号链接**

Run: `find plugins -path '*/.codex-plugin/plugin.json' -print | sort`

Expected: 精确输出七个 manifest。

Run: `find plugins research-knowledge -xtype l -print`

Expected: 无断裂符号链接；任何有效内部符号链接均在迁移日志逐项说明。

- [ ] **Step 4: 更新迁移日志并提交**

记录复制时间、每个源 revision/dirty 状态、过滤项以及 `calc-project` 链接解引用事实。

```bash
git add plugins research-knowledge docs/migrations/2026-09-04-plugin-consolidation.md
git commit -m "feat: consolidate plugin sources and research knowledge"
```

### Task 3: 建立中文代理导航与 Context Map

**Files:**
- Create: `AGENTS.md`
- Create: `CONTEXT-MAP.md`
- Create: `docs/contexts/calc-project.md`
- Create: `docs/contexts/dev-project.md`
- Create: `docs/contexts/osm-project.md`
- Create: `docs/contexts/paper-project.md`
- Create: `docs/contexts/research-knowledge.md`
- Modify: `tests/test_repository_layout.py`

**Interfaces:**
- Consumes: 四个旧 `CONTEXT.md` 与 `research-knowledge` 的 README、`CONSUMER_CONTRACT.md`、cards/templates 索引。
- Produces: 代理常驻规则、任务触发式 context 指针、旧路径到新路径的单一导航表。

- [ ] **Step 1: 扩充导航测试**

断言 `CONTEXT-MAP.md` 包含七个插件目标路径、八个源路径、五个 context 相对链接，以及 `calc-project`、`paper-project` 到 `research-knowledge` 的依赖关系。断言 `AGENTS.md` 链接 `CONTEXT-MAP.md`，并用中文说明修改插件、共享知识库和迁移路径时的读取触发条件。

- [ ] **Step 2: 运行测试并确认仍为红灯**

Run: `pytest -q tests/test_repository_layout.py`

Expected: FAIL，报告代理导航文件缺失。

- [ ] **Step 3: 创建五个 context 文件**

四个项目 context 保留现有有效语义并改写为新路径；四个 `dev-*` 插件共用 `dev-project.md`。`research-knowledge.md` 提炼所有权、候选/正式边界、消费者、写入治理和索引入口，不复制完整契约内容，而是链接其单一来源。

- [ ] **Step 4: 创建 CONTEXT-MAP 与中文 AGENTS**

`CONTEXT-MAP.md` 用表格给出维护单元、目标路径、context、旧路径、依赖和读取触发条件。`AGENTS.md` 只写全仓规则：先查地图、保护共享知识边界、修改依赖时联动验证、记录迁移路径、不自动发布。

- [ ] **Step 5: 运行导航测试并提交**

Run: `pytest -q tests/test_repository_layout.py`

Expected: PASS。

```bash
git add AGENTS.md CONTEXT-MAP.md docs/contexts tests/test_repository_layout.py
git commit -m "docs: add Chinese agent context navigation"
```

### Task 4: 重写共享知识库运行时路径

**Files:**
- Modify: `plugins/calc-project/**`
- Modify: `plugins/paper-project/**`
- Modify: `research-knowledge/**` only where an active configuration requires it
- Modify: `tests/test_repository_layout.py`
- Modify: `docs/migrations/2026-09-04-plugin-consolidation.md`

**Interfaces:**
- Consumes: 新固定路径 `/home/donk/yz-skills/research-knowledge`。
- Produces: 在统一仓库中可运行的知识库消费者；旧绝对路径只允许存在于已分类的历史材料中。

- [ ] **Step 1: 写旧路径扫描测试**

扫描插件的 `SKILL.md`、YAML、JSON、Python、Shell 和测试文件，断言不含 `/home/donk/plugins/research-knowledge`。Markdown 只扫描插件运行说明；设计规格、迁移日志和归档文件列入显式历史白名单。

- [ ] **Step 2: 运行扫描并确认红灯**

Run: `pytest -q tests/test_repository_layout.py -k research_knowledge_path`

Expected: FAIL，并列出 `calc-project` 或 `paper-project` 中的旧运行时路径。

- [ ] **Step 3: 更新有效路径**

将有效源码、技能说明、配置和测试中的旧根路径替换为 `/home/donk/yz-skills/research-knowledge`。不批量改写历史规格或归档内容；将剩余命中逐项分类写入迁移日志。

- [ ] **Step 4: 验证知识库及消费者**

Run: `pytest -q tests/test_repository_layout.py`

Run: `pytest -q research-knowledge/tests`

Run: `python plugins/paper-project/skills/prl-shared/scripts/validate_knowledge_repository.py research-knowledge`

Expected: 全部 PASS，验证器退出码为 0。

- [ ] **Step 5: 提交路径迁移**

```bash
git add plugins research-knowledge tests docs/migrations/2026-09-04-plugin-consolidation.md
git commit -m "fix: point plugins at consolidated research knowledge"
```

### Task 5: 全仓验证与迁移收尾

**Files:**
- Modify: `docs/migrations/2026-09-04-plugin-consolidation.md`

**Interfaces:**
- Consumes: Tasks 1–4 的完整迁移结果。
- Produces: 可审计的最终验证记录和干净的统一仓库工作树。

- [ ] **Step 1: 验证 manifest 与 JSON**

Run: `find plugins -path '*/.codex-plugin/plugin.json' -print0 | xargs -0 -n1 python -m json.tool`

Expected: 七个文件全部解析成功。

- [ ] **Step 2: 运行仓库与知识库测试**

Run: `pytest -q tests/test_repository_layout.py research-knowledge/tests`

Expected: 全部 PASS。

- [ ] **Step 3: 运行可迁移的插件原有测试**

从原开发仓库测试中选择只依赖插件发布边界的布局、清单和技能清单测试，在新目录结构下运行。逐项记录命令、通过数和失败原因；因旧仓库外层工具或测试素材未迁移而不能运行的测试标记为“边界外”，不能伪报通过。

- [ ] **Step 4: 完成迁移审计**

更新迁移日志：确认源仓库未改动；列出所有旧路径剩余命中及历史分类；列出验证命令、结果和任何开放事项。

- [ ] **Step 5: 最终提交并检查工作树**

```bash
git add docs/migrations/2026-09-04-plugin-consolidation.md
git commit -m "docs: record plugin consolidation verification"
git status --short --branch
```

Expected: `## main`，无未提交文件。
