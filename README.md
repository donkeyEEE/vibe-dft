# YZ Skills

面向科研计算、学术写作与个人项目日志的 Codex 插件集合。本仓库集中维护四个插件及其 skill、脚本、模板和参考资料，每个 `plugins/<plugin-name>/` 目录都是独立的插件发布单元。

## 插件一览

| 插件 | 功能 | 典型任务 |
| --- | --- | --- |
| [calc-project](plugins/calc-project/) | 科研计算 RQ、Spec 与执行工作流 | 配置项目、设计 Spec、推进 Run、瞬时只读评审 |
| [paper-project](plugins/paper-project/) | 文献证据与学术写作 | 整理文献、核查引用、润色论文与制作科学图件 |
| [osm-project](plugins/osm-project/) | 个人项目进展记录 | 将当前会话整理为 Obsidian 项目日志 |
| [skill-incubator](plugins/skill-incubator/) | 通用 skill 试验场 | 物理论文润色、演示文稿和学术评价 |

## 安装

需要已安装且支持 `codex plugin` 命令的 Codex CLI。克隆仓库后，将仓库根目录注册为本地 marketplace：

```bash
git clone <repository-url> yz-skills
cd yz-skills
git checkout v0.1
codex plugin marketplace add "$(pwd)"
```

按需安装一个或多个插件：

```bash
codex plugin add calc-project@yz-skills
codex plugin add paper-project@yz-skills
codex plugin add osm-project@yz-skills
codex plugin add skill-incubator@yz-skills
codex plugin list
```

安装或更新后新建 Codex 对话，使插件中的 skills 进入新的会话上下文。若从 Git marketplace 安装后需要获取新版，可先运行 `codex plugin marketplace upgrade`，再重新运行相应的 `codex plugin add` 命令。

## 常用 skill

下列名称链接到仓库内的 `SKILL.md`，可查看具体流程、输入要求和依赖。插件的 `skills/*/SKILL.md` 目录集合是其 Skill roster；标注“仅显式调用”的入口由 `agents/openai.yaml` 禁止 Codex 隐式选用。

### calc-project：科研计算

| Skill | 功能与适用场景 |
| --- | --- |
| [ask-dnk](plugins/calc-project/skills/ask-dnk/SKILL.md) | 仅显式调用；只读取足够的项目上下文，将请求路由到正确 sibling。 |
| [calc-setup](plugins/calc-project/skills/calc-setup/SKILL.md) | 仅显式调用；初始化或维护稳定项目结构、Tracker 配置、数据边界与集群 profile。 |
| [calc-rq](plugins/calc-project/skills/calc-rq/SKILL.md) | 仅显式调用；管理一个 RQ 及其 Decision Tickets。 |
| [calc-to-spec](plugins/calc-project/skills/calc-to-spec/SKILL.md) | 仅显式调用；设计、批准并发布一个当前科学 Spec。 |
| [calc-execute](plugins/calc-project/skills/calc-execute/SKILL.md) | 仅显式调用；推进一整份 ready 或 active Spec 的任务、Run、同步、接收和闭合。 |
| [calc-review](plugins/calc-project/skills/calc-review/SKILL.md) | 仅显式调用；对一个准确的 prepared Run 快照做瞬时只读预提交评审。 |

常见分工：不确定入口时显式调用 `ask-dnk`；配置进入 `calc-setup`，RQ 决策进入 `calc-rq`，科学设计进入 `calc-to-spec`，执行进入 `calc-execute`。`calc-execute` 在提交前调用 `calc-review`，而直接评审只产生当前诊断，不形成后续提交授权。

#### 当前架构（WF-001）

Calc Project 采用六个显式接口和一条单向权威链。`ask-dnk` 只负责推荐入口；其余接口各自拥有一类变更，避免用平行状态文件复制研究或执行事实。

```text
                         ┌──────────────┐
                         │   ask-dnk    │  路由建议
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
| 项目结构、Tracker adapter、数据边界与集群 profile | 项目稳定配置 | `calc-setup` |
| RQ、Decision Ticket 与已接受的 RQ 决策 | `RQ.md` 与 `decision-tickets/` | `calc-rq` |
| 科学判断、任务 DAG、条件与验收规则 | 发布后的 Spec | `calc-to-spec` |
| 任务状态、Run 记录、输入快照、输出与执行证据 | Spec 与对应 Run 目录 | `calc-execute` |
| 提交前判断 | 当前 prepared Run 的瞬时审查结果 | `calc-review` |

每个 RQ 的本地 Markdown Tracker 目录包含 `RQ.md`、`decision-tickets/` 和 `specs/`；不存在独立 Tracker 数据库、进度缓存或 session registry。Spec 是任务、DAG、Run、执行状态与闭环的协调权威，Run 目录保存不可变 `inputs/`、私有 `outputs/` 和 `logs/`。正常提交链为：

```text
prepare → validate → calc-review → submit unchanged inputs
```

运行时采用渐进披露：六个 `SKILL.md` 保留公共步骤，具体后端、PBS、同步与修复规则位于 owning skill 的 `references/`，模板和确定性脚本与唯一消费者共置。一次任务只读取命中分支所需的资料，不把完整发布包自动注入上下文。

详细约束见 [RQ Tracker 设计](docs/superpowers/specs/2026-09-11-calc-rq-tracker-design.md)；完整替换的实施与验收方案见 [WF-001 实施计划](docs/superpowers/plans/2026-09-11-calc-roster-replacement.md)。当前实现已通过源码、解压包与隔离行为验收，但尚未作为新的版本标签发布。

### paper-project：文献、论文与汇报

| Skill | 功能与适用场景 |
| --- | --- |
| [zo2notes](plugins/paper-project/skills/zo2notes/SKILL.md) | 将选定的 Zotero 文献整理为项目内中文研究笔记或稿件材料库。 |
| [literature-review](plugins/paper-project/skills/literature-review/SKILL.md) | 跨学术数据库开展系统文献检索、综述与证据综合。 |
| [liteparse](plugins/paper-project/skills/liteparse/SKILL.md) | 提取 PDF、Office 文档和图片中的文字、版面坐标，支持 OCR 与页面渲染。 |
| [citation-validator](plugins/paper-project/skills/citation-validator/SKILL.md) | 检查 Word 稿件中的引用是否支持对应论断，结合 Zotero 文献评估支持程度。 |
| [pr-intro](plugins/paper-project/skills/pr-intro/SKILL.md) | Draft or restructure evidence-grounded Physical Review Introductions. |
| [big-paper-helper](plugins/paper-project/skills/big-paper-helper/SKILL.md) | 规划、撰写、整合或审查计算材料领域的中文学位论文。 |
| [prl-figure](plugins/paper-project/skills/prl-figure/SKILL.md) | 制作、审查和导出面向投稿的科学图件，组织多面板证据与验证结果。 |
| [yuanzhuo-skill](plugins/paper-project/skills/yuanzhuo-skill/SKILL.md) | 组织人物视角的独立分析、交叉提问与主持式圆桌讨论。 |

### osm-project：项目日志

[log2ob](plugins/osm-project/skills/log2ob/SKILL.md) 将当前会话中的任务、进展、结论、未决事项和恢复入口整理成项目状态草稿，经用户确认后写入 Obsidian Daily Note。适合完成一段工作后记录进展，或为下一次继续工作保留入口。

### skill-incubator：试验中通用工作流

| Skill | 功能与适用场景 |
| --- | --- |
| [prl-polishing](plugins/skill-incubator/skills/prl-polishing/SKILL.md) | 按论断、证据、适用边界与物理意义组织科研文字，支持润色、重构和中英翻译。 |
| [paper2ppt](plugins/skill-incubator/skills/paper2ppt/SKILL.md) | 将科研论文组织为可交付给 PPT Master 的演示素材。 |
| [ppt-master](plugins/skill-incubator/skills/ppt-master/SKILL.md) | 创建、填充和验证可编辑演示文稿。 |

## 使用与维护入口

在已加载相应插件的会话中，可以显式指定 skill 并描述任务，例如：

```text
$calc-project:calc-execute 推进这份已批准 Spec 的 ready 任务。
$skill-incubator:prl-polishing 润色下面的论文段落，保留论断的适用条件。
$osm-project:log2ob 记录本次项目进展。
```

插件目录包含可维护的源文件；实际使用还取决于插件是否已加载，以及对应 skill 所需的工具、账号或计算环境是否就绪。

- 参与维护前读取 [AGENTS.md](AGENTS.md)，按任务进入对应插件。
- 领域约定、skill 收录、调用策略与资源归属规则见 [CONTEXT.md](CONTEXT.md)。
