# vibe-dft-auto

这个仓库维护科研计算、学术写作和项目日志相关的 Codex 插件。四个插件分别发布，各自的 skill、脚本、模板和参考资料放在 `plugins/<plugin-name>/` 下。插件市场名称仍是 `vibe-dft`。

## 插件

| 插件 | 用途 | 常见工作 |
| --- | --- | --- |
| [calc-project](plugins/calc-project/) | 科研计算的 RQ、Spec、执行和作业监控 | 配置项目、设计 Spec、推进 Run、监控 PBS 作业、提交前评审 |
| [paper-project](plugins/paper-project/) | 文献证据和学术写作 | 整理文献、核查引用、写作与制作科学图件 |
| [osm-project](plugins/osm-project/) | Obsidian 项目日志 | 将当前会话的进展整理为项目日志 |
| [skill-incubator](plugins/skill-incubator/) | 尚未形成独立插件边界的通用 skill | 论文润色、演示文稿、学术评价与修回材料 |

## 安装

安装需要支持 `codex plugin` 命令的 Codex CLI。可以从 GitHub 或本地工作树注册插件市场 `vibe-dft`。

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

只做科研计算时，安装 `calc-project` 即可。安装或重新安装插件后，新建 Codex 对话以加载插件。

更新已注册的 GitHub 市场时，运行：

```bash
codex plugin marketplace upgrade vibe-dft
codex plugin add calc-project@vibe-dft
```

第二条命令会重新安装已更新的插件。固定在版本标签上的市场不会因升级切换到其他版本；需要切换时，重新注册到目标标签或 `main`。用 `codex plugin list --marketplace vibe-dft` 查看已注册市场中的插件。

### 从本地工作树安装

修改或调试本仓库时，可将仓库根目录注册为本地插件市场：

```bash
git clone https://github.com/donkeyEEE/vibe-dft.git
cd vibe-dft
codex plugin marketplace add "$(pwd)"
codex plugin add calc-project@vibe-dft
```

本地市场读取当前工作树。修改插件后，重新运行对应的 `codex plugin add`，再新建对话验证。不要同时注册本地副本和同一仓库的 GitHub 副本，两者会使用相同的市场名称。

## Skills

每个插件的 `skills/*/SKILL.md` 构成其 skill 列表。下表链接到各 skill 的说明文件。仅限显式调用的 skill 会在 `agents/openai.yaml` 中关闭自动选择。

### calc-project

| Skill | 用途 |
| --- | --- |
| [ask-lyz](plugins/calc-project/skills/ask-lyz/SKILL.md) | 显式辅助入口，用于推荐工作接口、解释项目术语或查询进度。 |
| [calc-setup](plugins/calc-project/skills/calc-setup/SKILL.md) | 初始化或维护项目结构、RQ 存储配置、数据边界和集群配置。 |
| [calc-rq](plugins/calc-project/skills/calc-rq/SKILL.md) | 建立和推进研究问题（RQ），将获批答案记录为已接受决策。 |
| [calc-to-spec](plugins/calc-project/skills/calc-to-spec/SKILL.md) | 为已接受 RQ 渐进发布完整的单份 Spec，或安全替换当前设计。 |
| [calc-execute](plugins/calc-project/skills/calc-execute/SKILL.md) | 推进已就绪或活动中的 Spec，处理 Run 的准备、评审、提交、跟踪、同步与验收。 |
| [calc-report](plugins/calc-project/skills/calc-report/SKILL.md) | 根据 RQ、Spec、Run 与已有结果生成可追溯的阶段或结果汇报。 |
| [calc-review](plugins/calc-project/skills/calc-review/SKILL.md) | 对指定 prepared Run 做瞬时、只读的提交前评审。 |
| [show-cot](plugins/calc-project/skills/show-cot/SKILL.md) | 显式、只读地展示计算归属树（COT）；直接调用时可在确认后生成 HTML 进展报告，执行交接时可自主生成。 |

Calc Project 按 `RQ → Spec → Task → Run` 组织计算工作：

```text
RQ ─────────────▶ Spec ─────────────▶ Task ─────────────▶ Run
研究问题           已发布科学设计       可执行工作单元       一次具体执行尝试
  │                  │                   │                   │
calc-rq          calc-to-spec        calc-execute        calc-execute
```

- **RQ（研究问题）**：记录一条研究主线中的问题、边界、成功标准和已接受决策。一个 RQ 可以有多份 Spec，各自回答不同的主要判断。
- **Spec（计算规范）**：针对一个主要判断制定科学设计，定义任务依赖，并记录任务目的、条件、验收规则、状态、Run 和闭合结论。
- **Task（计算任务）**：Spec 中支持主要判断的可执行工作单元。父 Spec 管理它的身份、目的、依赖、条件和验收标准。
- **Run（运行）**：一个 Task 的一次具体执行尝试。Run 在独立目录中保存实际输入、输出和日志。每次验证与评审固定当时的输入快照；新的尝试使用新的 Run 编号，符合条件的当前 Run 可原地纠正。

通常先用 `calc-setup` 建立项目根目录、数据根、RQ 存储配置和集群配置，然后推进 RQ、Spec 和 Run：

1. 用 `calc-rq` 建立或推进 RQ，并把用户在访谈中确认的答案写入 RQ 的 `## Decisions`。
2. 用 `calc-to-spec` 为 RQ 当前有依据的主要判断设计并发布一份完整 Spec。后续判断可根据结果逐份发布。证据档位优先采用 Spec 的设置，其次继承 RQ；都未设置时采用轻量档。
3. 用 `calc-execute` 推进已发布的 Spec：选择可执行的 Task，创建或继续 Run，准备并验证输入。评审通过后自主提交作业，接收结果并处理后续 Task。需要改变科学设计时，交由 `calc-to-spec`。
4. 全部 Task 都已处理且闭合证据充分时，`calc-execute` 自主结束 Spec。需要调整 RQ 时，交由后续 `calc-rq` 流程。

### Calc Project 的自主执行与人工参与

在已接受 RQ 和用户明确约束内，`calc-to-spec` 可自主发布新 Spec，也可替换未结束 Spec 的当前设计。Spec 可以随研究进展逐份发布，无需事先列齐。设计证据不足时，agent 可自行调研。默认的轻量档只要求当前判断和必要交接所需的检查；用户可在 RQ 或 Spec 中明确要求严格档。

用户委托执行选定 Spec 后，`calc-execute` 可以准备和评审 Run，提交、监控和排查作业问题，同步结果，调整资源或成本，取消过时作业，处理执行产物，并在证据充分时结束 Spec。若委托范围是推进整个 RQ，有依据的下一项判断可继续进入新 Spec。需要修改执行中的科学设计时，`calc-to-spec` 会安全替换当前设计，并保留旧 Run 证据。

若已接受 RQ、项目证据和可靠文献仍不足以解决关键科学问题，agent 会请用户参与判断。修改或重开已结束（`concluded`）的 Spec 需要针对具体变更取得授权。改变 RQ 的已接受决策、超出用户明确边界的行动也需另行处理。执行过程继续保留安全检查、提交前快照评审和证据记录。

不确定该用哪个 skill 时，可以使用 `ask-lyz`；它也能解释项目术语和查询进度。`calc-review` 通常由 `calc-execute` 在提交 Run 前调用，对已准备的输入快照做一次只读评审。输入、资源或执行环境改变后，必须重新验证和评审。直接调用 `calc-review` 不会启动执行，也不会改变 Task、Run 或 Spec 的状态。

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
