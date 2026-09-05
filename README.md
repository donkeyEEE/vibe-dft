# YZ Skills

面向科研计算、学术写作、软件开发与个人项目日志的 Codex 插件集合。本仓库集中维护四个插件及其 skill、脚本、模板和参考资料，每个 `plugins/<plugin-name>/` 目录都是独立的插件发布单元。

## 插件一览

| 插件 | 功能 | 典型任务 |
| --- | --- | --- |
| [calc-project](plugins/calc-project/) | 科研计算项目与方法工作流 | 建立计算任务、准备输入、同步数据、维护模板 |
| [paper-project](plugins/paper-project/) | 文献证据、学术写作与研究展示 | 整理文献、核查引用、润色论文、绘图与制作 PPT |
| [matt-skills](plugins/matt-skills/) | 基于 Matt Pocock skills 的个人精选 Codex 插件 | 需求设计、编码测试、调试审查、协作与 agent 文档 |
| [osm-project](plugins/osm-project/) | 个人项目进展记录 | 将当前会话整理为 Obsidian 项目日志 |

**来源说明：`matt-skills` 基于 [Matt Pocock 的 skills](https://github.com/mattpocock/skills) 进行 Codex 原生插件适配，并按个人习惯持续精选和改写流程，选择性吸收上游更新。** 它是本仓库维护的个人版本；上游来源、适配说明和许可证见 [插件说明](plugins/matt-skills/README.md)。

## 常用 skill

下列名称链接到仓库内的 `SKILL.md`，可查看具体流程、输入要求和依赖。表中标注“仅显式调用”的入口按仓库术语处于停用状态：保留给用户主动调用，Codex 不会自动选用。完整状态以各插件的 `skill-lifecycle.json` 为准。

### calc-project：科研计算

| Skill | 功能与适用场景 |
| --- | --- |
| [calc-project-structure](plugins/calc-project/skills/calc-project-structure/SKILL.md) | 初始化或整理计算项目目录、顶层文档和数据边界。 |
| [calc-task](plugins/calc-project/skills/calc-task/SKILL.md) | 创建或维护具体计算任务的 `calc-task.yaml`，记录身份、路径、状态和索引。 |
| [vasp-workflow](plugins/calc-project/skills/vasp-workflow/SKILL.md) | 准备和检查 VASP 输入、VASPkit 相关计算、PBS 脚本及普通能带结果。 |
| [dmft-workflow](plugins/calc-project/skills/dmft-workflow/SKILL.md) | 准备 DFT+DMFT / solid_dmft 输入、关联子空间和后处理。 |
| [magnetic-workflow](plugins/calc-project/skills/magnetic-workflow/SKILL.md) | 衔接 VASP → Wannier90 → TB2J → VAMPIRE 磁性计算流程。 |
| [namd-workflow](plugins/calc-project/skills/namd-workflow/SKILL.md) | 准备或诊断 VASP 与 Hefei-NAMD / NAMDwithSOC 的快照、耦合和自旋接口。 |
| [calc-workflows](plugins/calc-project/skills/calc-workflows/SKILL.md) | 组织跨方法工作流，准备 Wannier90、共享 PBS 和结果打包资源。 |
| [calc-sync](plugins/calc-project/skills/calc-sync/SKILL.md) | 检查任务元数据与远端状态，对已确认的任务路径规划或执行非破坏性数据同步。 |
| [script-management](plugins/calc-project/skills/script-management/SKILL.md) | 维护和验证可复用计算模板资产及其目录索引。 |

常见分工：先用 `calc-project-structure` 建立项目，再用 `calc-task` 登记任务，交给对应方法 skill 准备计算输入；需要同步任务数据时使用 `calc-sync`。

### paper-project：文献、论文与汇报

| Skill | 功能与适用场景 |
| --- | --- |
| [zo2notes](plugins/paper-project/skills/zo2notes/SKILL.md) | 将选定的 Zotero 文献整理为项目内中文研究笔记或稿件材料库。 |
| [literature-review](plugins/paper-project/skills/literature-review/SKILL.md) | 跨学术数据库开展系统文献检索、综述与证据综合。 |
| [liteparse](plugins/paper-project/skills/liteparse/SKILL.md) | 提取 PDF、Office 文档和图片中的文字、版面坐标，支持 OCR 与页面渲染。 |
| [citation-validator](plugins/paper-project/skills/citation-validator/SKILL.md) | 检查 Word 稿件中的引用是否支持对应论断，结合 Zotero 文献评估支持程度。 |
| [prl-polishing](plugins/paper-project/skills/prl-polishing/SKILL.md) | 按论断、证据、适用边界与物理意义组织科研文字，支持润色、重构和中英翻译。 |
| [big-paper-helper](plugins/paper-project/skills/big-paper-helper/SKILL.md) | 规划、撰写、整合或审查计算材料领域的中文学位论文。 |
| [nature-response](plugins/paper-project/skills/nature-response/SKILL.md) | 起草或修订逐条审稿回复、修回信、投稿附信和修改稿摘录。 |
| [prl-figure](plugins/paper-project/skills/prl-figure/SKILL.md) | 制作、审查和导出面向投稿的科学图件，组织多面板证据与验证结果。 |
| [paper2ppt](plugins/paper-project/skills/paper2ppt/SKILL.md) | 将论文、预印本或阅读笔记转为以证据组织的中文汇报，调用同插件的 PPT Master。 |
| [ppt-master](plugins/paper-project/skills/ppt-master/SKILL.md) | 创建可编辑 PPTX、建立演示模板工作区、填充模板或改进现有演示文稿。 |
| [scientific-critical-thinking](plugins/paper-project/skills/scientific-critical-thinking/SKILL.md) | 评估材料物理论断、计算与实验结果的证据、局限和替代解释。 |
| [scholar-evaluation](plugins/paper-project/skills/scholar-evaluation/SKILL.md) | 从问题、方法、分析与写作等维度评价学术工作，给出评分和改进建议。 |
| [yuanzhuo-skill](plugins/paper-project/skills/yuanzhuo-skill/SKILL.md) | 组织人物视角的独立分析、交叉提问与主持式圆桌讨论。 |

[cangjie-skill](plugins/paper-project/skills/cangjie-skill/SKILL.md) 当前停用，仅保留显式入口，原资源蒸馏工作流等待重新设计。

### matt-skills：需求设计与协作

| Skill | 功能与适用场景 |
| --- | --- |
| [grilling](plugins/matt-skills/skills/grilling/SKILL.md) | 通过持续追问检验计划或设计，澄清假设、选择与未决问题。 |
| [domain-modeling](plugins/matt-skills/skills/domain-modeling/SKILL.md) | 统一领域术语，维护 `CONTEXT.md` 和架构决策记录。 |
| [research](plugins/matt-skills/skills/research/SKILL.md) | 基于一手资料调查设计或技术问题，在仓库中保存带来源的研究结论。 |
| [prototype](plugins/matt-skills/skills/prototype/SKILL.md) | 构建用于回答设计问题的临时逻辑或界面原型。 |
| [writing-for-agents](plugins/matt-skills/skills/writing-for-agents/SKILL.md) | 编写和审查 skill、AGENTS.md、插件元数据等 agent 文档，明确触发条件、信息层次和完成标准。 |
| [handoff](plugins/matt-skills/skills/handoff/SKILL.md) | 将当前会话压缩为供后续 agent 接手的交接文档；仅显式调用。 |

其余访谈、问卷及教学入口见 [完整 skill 导航](plugins/matt-skills/skills/README.md)。

### matt-skills：实现与验证

| Skill | 功能与适用场景 |
| --- | --- |
| [codebase-design](plugins/matt-skills/skills/codebase-design/SKILL.md) | 设计深模块、接口和可替换位置，改善复杂性封装与可测试性。 |
| [tdd](plugins/matt-skills/skills/tdd/SKILL.md) | 通过“测试失败 → 实现通过 → 重构”的循环逐步交付行为。 |
| [diagnosing-bugs](plugins/matt-skills/skills/diagnosing-bugs/SKILL.md) | 围绕复现、假设和验证诊断疑难故障或性能回退。 |
| [code-review](plugins/matt-skills/skills/code-review/SKILL.md) | 从仓库规范与原始需求两个维度审查指定基线之后的代码变更。 |
| [resolving-merge-conflicts](plugins/matt-skills/skills/resolving-merge-conflicts/SKILL.md) | 根据双方修改意图处理正在进行的 merge 或 rebase 冲突。 |
| [wizard](plugins/matt-skills/skills/wizard/SKILL.md) | 为凭据配置、基础设施等必须由人完成的步骤生成交互式 Bash 向导。 |
| [implement](plugins/matt-skills/skills/implement/SKILL.md) | 根据规格或任务实现软件工作，结合 TDD 与代码审查；仅显式调用。 |
| [improve-codebase-architecture](plugins/matt-skills/skills/improve-codebase-architecture/SKILL.md) | 扫描模块深化机会，生成可视化报告并进一步讨论选定方案；仅显式调用。 |
| [ask-matt](plugins/matt-skills/skills/ask-matt/SKILL.md) | 根据当前任务推荐合适的 skill 或工作流程；仅显式调用。 |

配置与请求分流入口见 [完整 skill 导航](plugins/matt-skills/skills/README.md)。

### osm-project：项目日志

[log2ob](plugins/osm-project/skills/log2ob/SKILL.md) 将当前会话中的任务、进展、结论、未决事项和恢复入口整理成项目状态草稿，经用户确认后写入 Obsidian Daily Note。适合完成一段工作后记录进展，或为下一次继续工作保留入口。

## 使用与维护入口

在已加载相应插件的会话中，可以显式指定 skill 并描述任务，例如：

```text
$calc-project:calc-task 为这次 VASP 计算登记任务元数据。
$paper-project:prl-polishing 润色下面的论文段落，保留论断的适用条件。
$matt-skills:writing-for-agents 精简这个项目的 AGENTS.md。
$matt-skills:code-review 审查当前分支相对 main 的变更。
$osm-project:log2ob 记录本次项目进展。
```

插件目录包含可维护的源文件；实际使用还取决于插件是否已加载，以及对应 skill 所需的工具、账号或计算环境是否就绪。

- 参与维护前读取 [AGENTS.md](AGENTS.md)，按任务进入对应插件。
- 领域约定、skill 生命周期与资源归属规则见 [CONTEXT.md](CONTEXT.md)。
- 历史目录映射与迁移记录见 [迁移日志](docs/migrations/2026-09-04-plugin-consolidation.md)。
