# vibe-dft

`vibe-dft` 是一组面向科研计算、学术写作和项目日志的 Codex 插件。仓库包含四个可独立发布的插件；它们的 skill、脚本、模板和参考资料都放在各自的 `plugins/<plugin-name>/` 目录中。

## 插件

| 插件 | 用途 | 常见工作 |
| --- | --- | --- |
| [calc-project](plugins/calc-project/) | 科研计算的 RQ、Spec、执行和作业监控 | 配置项目、设计 Spec、推进 Run、监控 PBS 作业、提交前评审 |
| [paper-project](plugins/paper-project/) | 文献证据和学术写作 | 整理文献、核查引用、写作与制作科学图件 |
| [osm-project](plugins/osm-project/) | Obsidian 项目日志 | 将当前会话的进展整理为项目日志 |
| [skill-incubator](plugins/skill-incubator/) | 尚未形成独立插件边界的通用 skill | 论文润色、演示文稿、学术评价与修回材料 |

## 安装

需要使用支持 `codex plugin` 命令的 Codex CLI。仓库提供名为 `vibe-dft` 的插件市场，可从 GitHub 或本地工作树注册。

### 从 GitHub 安装与更新

如需固定版本，使用 `v0.1` 标签：

```bash
codex plugin marketplace add donkeyEEE/vibe-dft --ref v0.1
```

如需使用 `main` 上的开发版本：

```bash
codex plugin marketplace add donkeyEEE/vibe-dft --ref main
```

注册后按需安装插件：

```bash
codex plugin add calc-project@vibe-dft
codex plugin add paper-project@vibe-dft
codex plugin add osm-project@vibe-dft
codex plugin add skill-incubator@vibe-dft
codex plugin list
```

如果只做科研计算，安装 `calc-project` 即可。安装或重新安装插件后，请新建 Codex 对话，使其进入会话上下文。

更新已注册的 GitHub 市场时，运行：

```bash
codex plugin marketplace upgrade vibe-dft
codex plugin add calc-project@vibe-dft
```

第二条命令会重新安装已更新的插件。若市场固定在某个版本标签，升级仍会停留在该标签；要切换到新版本，请重新注册到目标标签或 `main`。可用 `codex plugin list --marketplace vibe-dft` 查看该市场中的插件。

### 从本地工作树安装

修改或调试本仓库时，可将仓库根目录注册为本地插件市场：

```bash
git clone https://github.com/donkeyEEE/vibe-dft.git
cd vibe-dft
codex plugin marketplace add "$(pwd)"
codex plugin add calc-project@vibe-dft
```

本地市场直接读取当前工作树。修改插件后重新执行对应的 `codex plugin add`，再新建对话验证。不要同时注册同一仓库的 GitHub 副本和本地副本，以免使用同名市场。

## Skills

插件下实际存在的 `skills/*/SKILL.md` 是该插件的 skill roster。下列链接指向对应的说明文件；标注为“仅显式调用”的 skill 会在 `agents/openai.yaml` 中禁止 Codex 自动选择。

### calc-project

| Skill | 用途 |
| --- | --- |
| [ask-lyz](plugins/calc-project/skills/ask-lyz/SKILL.md) | 显式辅助入口，用于推荐工作接口、解释项目术语或查询进度。 |
| [calc-setup](plugins/calc-project/skills/calc-setup/SKILL.md) | 初始化或维护项目结构、Tracker 配置、数据边界和集群配置。 |
| [calc-rq](plugins/calc-project/skills/calc-rq/SKILL.md) | 建立和推进研究问题（RQ），将获批答案记录为已接受决策。 |
| [calc-to-spec](plugins/calc-project/skills/calc-to-spec/SKILL.md) | 为已接受 RQ 渐进发布完整的单份 Spec，或安全替换当前设计。 |
| [calc-execute](plugins/calc-project/skills/calc-execute/SKILL.md) | 推进已就绪或活动中的 Spec，处理 Run 的准备、评审、提交、跟踪、同步与验收。 |
| [calc-report](plugins/calc-project/skills/calc-report/SKILL.md) | 根据 RQ、Spec、Run 与已有结果生成可追溯的阶段或结果汇报。 |
| [calc-review](plugins/calc-project/skills/calc-review/SKILL.md) | 对指定 prepared Run 做瞬时、只读的提交前评审。 |
| [show-cot](plugins/calc-project/skills/show-cot/SKILL.md) | 显式、只读地展示计算归属树（COT）；直接调用时可在确认后生成 HTML 进展报告，执行交接时可自主生成。 |

Calc Project 按 `RQ → Spec → Task → Run` 组织计算工作：

```text
RQ ─────────────▶ Spec ─────────────▶ Task ─────────────▶ Run
研究问题           已批准科学设计       可执行工作单元       一次具体执行尝试
  │                  │                   │                   │
calc-rq          calc-to-spec        calc-execute        calc-execute
```

- **RQ（研究问题）**：在一条研究主线内记录要回答的问题、研究边界、成功标准和已接受决策。一个 RQ 可以发布多份分别承担不同主要判断的 Spec。
- **Spec（计算规范）**：围绕一个主要判断形成的当前科学设计，定义任务依赖图，并记录任务目的、条件、验收规则、状态、Run 和闭合结论。
- **Task（计算任务）**：Spec 中为支持主要判断而声明的可执行工作单元；其身份、目的、依赖、条件和验收标准由父 Spec 管理。
- **Run（运行）**：一个 Task 的一次具体执行尝试。Run 在独立目录中保存实际输入、输出和日志。每次验证与评审固定当时的输入快照；新的尝试使用新的 Run 编号，符合条件的当前 Run 可原地纠正。

通常先用 `calc-setup` 建立项目根目录、数据根、RQ Tracker 和集群配置，再依次推进：

1. 用 `calc-rq` 建立或推进 RQ，并把用户在访谈中确认的答案写入 RQ 的 `## Decisions`。
2. 用 `calc-to-spec` 为 RQ 当前有依据的主要判断设计并自主发布一份完整 Spec；后续判断可随结果渐进发布。Spec 的证据档位优先采用自身设置，否则继承 RQ，均未设置时为轻量。
3. 用 `calc-execute` 推进已发布的 Spec：选择当前可执行的 Task，创建或继续 Run，准备并验证输入，评审通过后自主提交作业，接收结果并按验收规则处理后续 Task；若出现新的科学设计需求，交回 `calc-to-spec`。
4. 全部 Task 得到明确处置后，由 `calc-execute` 提出 Spec 闭合；研究结论是否影响 RQ，则交由后续 `calc-rq` 流程处理。

无法判断入口时使用 `ask-lyz`；它也能解释项目术语或查询进度。`calc-review` 是 Run 提交前的瞬时只读关口：通常由 `calc-execute` 对准确的已准备输入快照调用。输入、资源或执行环境改变后，必须重新验证和评审。它不管理 Task、Run 或 Spec 状态，直接调用不启动执行链。

```text
$calc-project:calc-setup 为当前目录建立计算项目配置。
$calc-project:calc-rq 为这条研究主线建立 RQ-001。
$calc-project:calc-to-spec 为 RQ-001 当前有依据的下一主要判断设计并发布一份完整 Spec。
$calc-project:calc-execute 推进 SPEC-001 中当前可执行的 Task 和 Run。
```

### paper-project

| Skill | 用途 |
| --- | --- |
| [get-zotero](plugins/paper-project/skills/get-zotero/SKILL.md) | 从 Zotero Desktop 只读获取题录、索引正文或本地 PDF。 |
| [get-notes](plugins/paper-project/skills/get-notes/SKILL.md) | 将选定的 Zotero 文献整理为项目内中文研究笔记或稿件素材库。 |
| [literature-review](plugins/paper-project/skills/literature-review/SKILL.md) | 从 Web 或指定 Zotero 分类检索证据并生成 Markdown 文献综述。 |
| [liteparse](plugins/paper-project/skills/liteparse/SKILL.md) | 提取 PDF、Office 文档和图片的文字与版面坐标，支持 OCR 和页面渲染。 |
| [citation-validator](plugins/paper-project/skills/citation-validator/SKILL.md) | 检查 Word 稿件中的引用是否支持对应论断，并结合 Zotero 文献评估支持程度。 |
| [pr-intro](plugins/paper-project/skills/pr-intro/SKILL.md) | 撰写或重构以证据为基础的 Physical Review 论文引言。 |
| [big-paper-helper](plugins/paper-project/skills/big-paper-helper/SKILL.md) | 规划、撰写、整合或审查计算材料领域的中文学位论文。 |
| [prl-figure](plugins/paper-project/skills/prl-figure/SKILL.md) | 制作、审查和导出面向投稿的科学图件，组织多面板证据与验证结果。 |
| [yuanzhuo-skill](plugins/paper-project/skills/yuanzhuo-skill/SKILL.md) | 组织人物视角的独立分析、交叉提问与主持式圆桌讨论。 |

### osm-project

| Skill | 用途 |
| --- | --- |
| [log2ob](plugins/osm-project/skills/log2ob/SKILL.md) | 用户显式调用 `$log2ob`，或明确要求记录当前会话时，将项目进展整理为 Obsidian 日志。 |

### skill-incubator

| Skill | 用途 |
| --- | --- |
| [cangjie-skill](plugins/skill-incubator/skills/cangjie-skill/SKILL.md) | Cangjie 资源蒸馏工作流正在重新设计期间的显式入口。 |
| [nature-response](plugins/skill-incubator/skills/nature-response/SKILL.md) | 起草、审查或修订 Nature 风格的审稿回复、rebuttal、修回信和 LaTeX 模板。 |
| [paper2ppt](plugins/skill-incubator/skills/paper2ppt/SKILL.md) | 将论文、预印本、文章或阅读笔记整理为以证据为主线的中文演示文稿。 |
| [ppt-master](plugins/skill-incubator/skills/ppt-master/SKILL.md) | 创建、填充、重建或增强可编辑的 PPTX 演示文稿。 |
| [prl-polishing](plugins/skill-incubator/skills/prl-polishing/SKILL.md) | 按 PRL 风格润色、重构或翻译科学文本，保留证据边界，不补充未经给出的内容。 |
| [scholar-evaluation](plugins/skill-incubator/skills/scholar-evaluation/SKILL.md) | 用 ScholarEval 框架评价学术工作的问题、方法、分析和写作，并给出可执行的反馈。 |
