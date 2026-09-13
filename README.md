# YZ Skills

面向科研计算、学术写作与个人项目日志的 Codex 插件集合。本仓库集中维护四个插件及其技能、脚本、模板和参考资料，每个 `plugins/<plugin-name>/` 目录都是独立的插件发布单元。

## 插件一览

| 插件 | 功能 | 典型任务 |
| --- | --- | --- |
| [calc-project](plugins/calc-project/) | 科研计算 RQ、Spec、执行与作业监控工作流 | 配置项目、设计 Spec、推进 Run、监控 PBS 作业、瞬时只读评审 |
| [paper-project](plugins/paper-project/) | 文献证据与学术写作 | 整理文献、核查引用、润色论文与制作科学图件 |
| [osm-project](plugins/osm-project/) | 个人项目进展记录 | 将当前会话整理为 Obsidian 项目日志 |
| [skill-incubator](plugins/skill-incubator/) | 通用 skill 试验场 | 物理论文润色、演示文稿和学术评价 |

## 安装

需要安装支持 `codex plugin` 命令的 Codex CLI。仓库自带名为
`yz-skills` 的插件市场，可以从 GitHub 安装，也可以在参与开发时从本地目录安装。

### 从 GitHub 安装

稳定使用建议固定到 `v0.1` 标签：

```bash
codex plugin marketplace add donkeyEEE/yz-skills --ref v0.1
```

若希望使用 `main` 分支的最新开发内容：

```bash
codex plugin marketplace add donkeyEEE/yz-skills --ref main
```

注册插件市场后，按需安装插件：

```bash
codex plugin add calc-project@yz-skills
codex plugin add paper-project@yz-skills
codex plugin add osm-project@yz-skills
codex plugin add skill-incubator@yz-skills
codex plugin list
```

只使用科研计算工作流时安装 `calc-project` 即可。安装完成后新建 Codex 对话，
使新插件和技能进入会话上下文。

### 从本地仓库安装

需要修改或调试本仓库时，克隆后把仓库根目录注册为本地插件市场：

```bash
git clone https://github.com/donkeyEEE/yz-skills.git
cd yz-skills
codex plugin marketplace add "$(pwd)"
codex plugin add calc-project@yz-skills
```

本地插件市场直接读取当前工作树；修改插件后重新执行对应的
`codex plugin add`，再新建对话验证。不要同时把同一仓库的 GitHub 副本和本地副本
注册成重名插件市场。

### 更新 GitHub 安装

```bash
codex plugin marketplace upgrade yz-skills
codex plugin add calc-project@yz-skills
```

第二条命令用于重新安装已更新的插件。更新后同样需要新建对话。可以随时运行
`codex plugin list --marketplace yz-skills` 查看该插件市场中的插件。

## 常用技能

下列名称链接到仓库内的 `SKILL.md`，可查看具体流程、输入要求和依赖。插件的 `skills/*/SKILL.md` 目录集合是其技能清单；标注“仅显式调用”的入口由 `agents/openai.yaml` 禁止 Codex 隐式选用。

### calc-project：科研计算

| 技能 | 功能与适用场景 |
| --- | --- |
| [ask-lyz](plugins/calc-project/skills/ask-lyz/SKILL.md) | 可选的显式路由入口；请求不明确时推荐正确的同级接口，但不代替用户调用。 |
| [calc-setup](plugins/calc-project/skills/calc-setup/SKILL.md) | 初始化或维护项目结构、Tracker 配置、数据边界和集群配置。 |
| [calc-rq](plugins/calc-project/skills/calc-rq/SKILL.md) | 建立和推进研究问题（RQ），管理临时决策记录及已接受决策。 |
| [calc-to-spec](plugins/calc-project/skills/calc-to-spec/SKILL.md) | 把一个 RQ 设计为可执行的科学 Spec，经批准后发布。 |
| [calc-execute](plugins/calc-project/skills/calc-execute/SKILL.md) | 推进整份已就绪或活动中的 Spec，管理任务、Run、提交、同步、接收与闭合。 |
| [calc-review](plugins/calc-project/skills/calc-review/SKILL.md) | 对指定的已准备 Run 快照做瞬时只读预提交评审。 |

所有接口都需要显式调用。已知目标时直接调用对应技能；只有不知道应该进入哪个
接口时才使用 `ask-lyz`。

#### 主要工作流

```text
可选路由             项目配置          研究问题          科学设计            计算执行
 ask-lyz ───────▶ calc-setup ───────▶ calc-rq ───────▶ calc-to-spec ───────▶ calc-execute
                                                                              │
                                                                              │ 已准备的 Run 快照
                                                                              ▼
                                                                         calc-review
                                                                         瞬时只读评审
```

1. **建立项目配置**：用 `calc-setup` 确定项目根目录、数据根、RQ Tracker、计算模板
   边界和集群配置。这些稳定事实是后续流程的基础。
2. **定义研究问题**：用 `calc-rq` 创建或推进 RQ。尚未解决且必须由用户明确回答的
   问题进入临时决策记录；答案被接受后写回 RQ。
3. **设计科学 Spec**：用 `calc-to-spec` 明确主要科学判断、任务依赖图、每项任务的
   条件、验收规则和停止规则。Spec 只有经过用户批准才发布。
4. **执行整份 Spec**：用 `calc-execute` 从当前权威状态继续，准备并验证 Run 输入、
   请求预提交评审、获得具体提交授权、提交作业、接收结果并推进后续任务。
5. **闭合与反馈**：当 Spec 中的任务满足验收规则后，`calc-execute` 提出闭合；RQ
   是否据此更新由后续 `calc-rq` 流程决定。

`calc-review` 不是主线中的独立状态管理器。正常情况下由 `calc-execute` 在提交前
针对准确的已准备 Run 快照调用；直接调用只会得到当前诊断，不会产生后续提交授权。

#### 常用调用示例

```text
$calc-project:ask-lyz 我想继续这个计算项目，但不确定应进入哪个接口。
$calc-project:calc-setup 为当前目录初始化计算项目配置。
$calc-project:calc-rq 为这个项目建立一个新的研究问题。
$calc-project:calc-to-spec 把 RQ-001 设计为新的科学 Spec。
$calc-project:calc-execute 推进 SPEC-001 中当前可执行的任务。
$calc-project:calc-review 只读评审 TASK-001/RUN-001 的已准备输入快照。
```

#### 权威对象与职责边界

Calc Project 采用六个显式接口和一条单向权威链。`ask-lyz` 只负责推荐入口；
其余接口各自拥有一类变更，避免用平行状态文件复制研究或执行事实。

```text
                         ┌──────────────┐
                         │   ask-lyz    │  路由建议
                         └──────┬───────┘
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
        ┌───────────┐     ┌───────────┐     ┌──────────────┐
        │ calc-setup│ ──▶ │  calc-rq  │ ──▶ │ calc-to-spec │
        └───────────┘     └───────────┘     └──────┬───────┘
                                                   ▼
                                            ┌──────────────┐
                                            │ calc-execute │
                                            └──────┬───────┘
                                                   │ 精确 Run 快照
                                                   ▼
                                            ┌─────────────┐
                                            │ calc-review │  瞬时只读
                                            └─────────────┘
```

| 权威对象 | 唯一事实源 | 负责接口 |
| --- | --- | --- |
| 项目结构、Tracker 适配器、数据边界与集群配置 | 项目稳定配置 | `calc-setup` |
| RQ、决策单与已接受的 RQ 决策 | `RQ.md` 与 `decision-tickets/` | `calc-rq` |
| 科学判断、任务 DAG、条件与验收规则 | 发布后的 Spec | `calc-to-spec` |
| 任务状态、Run 记录、输入快照、输出与执行证据 | Spec 与对应 Run 目录 | `calc-execute` |
| 提交前判断 | 当前已准备 Run 的瞬时审查结果 | `calc-review` |

每个 RQ 的本地 Markdown Tracker 目录包含 `RQ.md`、`decision-tickets/` 和
`specs/`；不使用独立 Tracker 数据库、进度缓存或会话登记表。Spec 是任务依赖图、
Run、执行状态与闭环的协调权威；Run 目录保存实际 `inputs/`、私有 `outputs/` 和
`logs/`。每次验证与评审固定当时的输入快照；符合条件的当前 Run 可原地纠正，任何
输入修改都会使旧验证与评审失效。正常提交链为：

```text
prepare → validate → calc-review → submit unchanged inputs
```

也就是“准备 → 验证 → 只读评审 → 原样提交”。如果评审后输入、资源或目标环境发生
变化，必须重新验证和评审。

提交 PBS 作业并记录作业编号后，`calc-execute` 可以按用户要求启动本地计算监控器。
监控器只等待作业离开 `qstat` 并请求恢复原 Codex 线程；恢复后仍由
`calc-execute` 核验调度器记录、日志和输出。离开队列不等于计算成功，监控器也不
保存 Spec、Run 或科学验收状态。

运行时采用渐进披露：六个 `SKILL.md` 保留公共步骤，具体后端、PBS、同步与修复规则
位于所属技能的 `references/`，模板和确定性脚本与唯一消费者共置。一次任务只读取
当前分支需要的资料。

详细约束见 [RQ Tracker 设计](docs/superpowers/specs/2026-09-11-calc-rq-tracker-design.md)；完整替换的实施与验收方案见 [WF-001 实施计划](docs/superpowers/plans/2026-09-11-calc-roster-replacement.md)。当前实现已通过源码、解压包与隔离行为验收，但尚未作为新的版本标签发布。

### paper-project：文献、论文与汇报

| 技能 | 功能与适用场景 |
| --- | --- |
| [zo2notes](plugins/paper-project/skills/zo2notes/SKILL.md) | 将选定的 Zotero 文献整理为项目内中文研究笔记或稿件材料库。 |
| [literature-review](plugins/paper-project/skills/literature-review/SKILL.md) | 跨学术数据库开展系统文献检索、综述与证据综合。 |
| [liteparse](plugins/paper-project/skills/liteparse/SKILL.md) | 提取 PDF、Office 文档和图片中的文字、版面坐标，支持 OCR 与页面渲染。 |
| [citation-validator](plugins/paper-project/skills/citation-validator/SKILL.md) | 检查 Word 稿件中的引用是否支持对应论断，结合 Zotero 文献评估支持程度。 |
| [pr-intro](plugins/paper-project/skills/pr-intro/SKILL.md) | 撰写或重构以证据为基础的 Physical Review 论文引言。 |
| [big-paper-helper](plugins/paper-project/skills/big-paper-helper/SKILL.md) | 规划、撰写、整合或审查计算材料领域的中文学位论文。 |
| [prl-figure](plugins/paper-project/skills/prl-figure/SKILL.md) | 制作、审查和导出面向投稿的科学图件，组织多面板证据与验证结果。 |
| [yuanzhuo-skill](plugins/paper-project/skills/yuanzhuo-skill/SKILL.md) | 组织人物视角的独立分析、交叉提问与主持式圆桌讨论。 |

### osm-project：项目日志

[log2ob](plugins/osm-project/skills/log2ob/SKILL.md) 将当前会话中的任务、进展、结论、未决事项和恢复入口整理成项目状态草稿，经用户确认后写入 Obsidian Daily Note。适合完成一段工作后记录进展，或为下一次继续工作保留入口。

### skill-incubator：试验中通用工作流

| 技能 | 功能与适用场景 |
| --- | --- |
| [prl-polishing](plugins/skill-incubator/skills/prl-polishing/SKILL.md) | 按论断、证据、适用边界与物理意义组织科研文字，支持润色、重构和中英翻译。 |
| [paper2ppt](plugins/skill-incubator/skills/paper2ppt/SKILL.md) | 将科研论文组织为可交付给 PPT Master 的演示素材。 |
| [ppt-master](plugins/skill-incubator/skills/ppt-master/SKILL.md) | 创建、填充和验证可编辑演示文稿。 |

## 使用与维护入口

在已加载相应插件的会话中，可以显式指定技能并描述任务，例如：

```text
$calc-project:calc-execute 推进这份已批准 Spec 中当前可执行的任务。
$skill-incubator:prl-polishing 润色下面的论文段落，保留论断的适用条件。
$osm-project:log2ob 记录本次项目进展。
```

插件目录包含可维护的源文件；实际使用还取决于插件是否已加载，以及对应技能所需的工具、账号或计算环境是否就绪。

- 参与维护前读取 [AGENTS.md](AGENTS.md)，按任务进入对应插件。
- 领域约定、技能收录、调用策略与资源归属规则见 [CONTEXT.md](CONTEXT.md)。
