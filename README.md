<p align="center">
  <img src="assets/yz-skills-logo.png" alt="YZ Skills" width="460">
</p>

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
`codex plugin list --marketplace yz-skills` 查看该插件市场中的插件。插件市场如果
固定在某个版本标签，升级命令仍会保持该标签；需要使用新版时，先把插件市场重新
注册到新的标签或 `main`。

## 常用技能

下列名称链接到仓库内的 `SKILL.md`，可查看具体流程、输入要求和依赖。插件的 `skills/*/SKILL.md` 目录集合是其技能清单；标注“仅显式调用”的入口由 `agents/openai.yaml` 禁止 Codex 隐式选用。

### calc-project：科研计算

| 技能 | 功能与适用场景 |
| --- | --- |
| [ask-lyz](plugins/calc-project/skills/ask-lyz/SKILL.md) | 显式辅助入口；推荐工作接口、解释项目术语或查询进度。 |
| [calc-setup](plugins/calc-project/skills/calc-setup/SKILL.md) | 初始化或维护项目结构、Tracker 配置、数据边界和集群配置。 |
| [calc-rq](plugins/calc-project/skills/calc-rq/SKILL.md) | 建立和推进研究问题（RQ），将获批答案直接记录为已接受决策。 |
| [calc-to-spec](plugins/calc-project/skills/calc-to-spec/SKILL.md) | 为一个 RQ 设计并发布完整科学 Spec 集，或替换一份现有 Spec。 |
| [calc-execute](plugins/calc-project/skills/calc-execute/SKILL.md) | 推进整份已就绪或活动中的 Spec，管理任务、Run、提交、同步、接收与闭合。 |
| [calc-report](plugins/calc-project/skills/calc-report/SKILL.md) | 围绕主题或选定 RQ/Spec，将已有计算证据组织为阶段汇报或结果汇报 HTML。 |
| [calc-review](plugins/calc-project/skills/calc-review/SKILL.md) | 对指定的已准备 Run 快照做瞬时只读预提交评审。 |
| [show-cot](plugins/calc-project/skills/show-cot/SKILL.md) | 显式只读展示完整 COT，并可在确认后生成 HTML 进展报告。 |

六个核心工作接口可由 Codex 根据任务自动选择，也可以显式调用。`ask-lyz` 是显式路由辅助；
`show-cot` 是显式只读总览，并可按用户确认写出不拥有进度状态的派生报告。已知目标时可直接
调用对应技能，不确定应进入哪个接口或需要解释 Calc Project 术语时可使用 `ask-lyz`。

#### 主要工作流

```text
RQ ─────────────▶ Spec ─────────────▶ Task ─────────────▶ Run
研究问题           已批准科学设计       可执行工作单元       一次具体执行尝试
  │                  │                   │                   │
calc-rq          calc-to-spec        calc-execute        calc-execute
```

Calc Project 以 `RQ → Spec → Task → Run` 组织计算工作：

- **RQ（研究问题）**：在一条研究主线内记录要回答的问题、研究边界、成功标准和
  已接受决策。一个 RQ 可以发布多个分别承担不同主要判断的 Spec。
- **Spec（计算规范）**：围绕一个主要判断形成的当前已批准科学设计。它定义任务
  依赖图，并统一记录任务目的、条件、验收规则、状态、Run 和闭合结论。
- **Task（计算任务）**：Spec 中为支持主要判断而声明的可执行工作单元。Task 的
  身份、目的、依赖、条件和验收标准都由父 Spec 管理。
- **Run（运行）**：一个 Task 的一次具体执行尝试。每个 Run 在独立目录中保存实际
  输入、输出和日志。每次验证与评审固定当时的输入快照；新的尝试使用新的 Run
  编号，符合条件的当前 Run 可原地纠正。

通常先用 `calc-setup` 建立项目根目录、数据根、RQ Tracker 和集群配置，再沿主线推进：

1. 用 `calc-rq` 建立或推进 RQ；需要用户明确回答的问题在当前访谈中解决，获批答案
   直接写入 RQ 的 `## Decisions`。
2. 用 `calc-to-spec` 先识别回答 RQ 所需的全部主要判断，为每个判断设计一份 Spec，
   明确 Task、依赖、条件、验收与停止规则，并在用户批准后发布完整 Spec 集。
3. 用 `calc-execute` 推进整份已发布 Spec。它选择当前可执行的 Task，为 Task 创建或
   继续 Run，准备并验证输入、获得具体提交授权、提交作业、接收结果并按验收规则
   推进后续 Task。
4. 当全部 Task 得到明确处置后，`calc-execute` 提出 Spec 闭合；研究结论是否影响
   RQ，由后续 `calc-rq` 流程处理。

`ask-lyz` 在无法判断应使用哪个接口时提供路由建议，也可解释项目术语或查询进度。
`calc-review` 则是 Run 提交前
的瞬时只读关口：正常情况下由 `calc-execute` 对准确的已准备输入快照调用；输入、
资源或执行环境发生变化后必须重新验证和评审。它不管理 Task、Run 或 Spec 状态，
直接调用也不会产生后续提交授权。

安装插件后可以这样进入各环节：

```text
$calc-project:calc-setup 为当前目录建立计算项目配置。
$calc-project:calc-rq 为这条研究主线建立 RQ-001。
$calc-project:calc-to-spec 为 RQ-001 设计并发布回答该 RQ 所需的完整 Spec 集。
$calc-project:calc-execute 推进 SPEC-001 中当前可执行的 Task 和 Run。
```


### paper-project：文献、论文与汇报

| 技能 | 功能与适用场景 |
| --- | --- |
| [get-zotero](plugins/paper-project/skills/get-zotero/SKILL.md) | 从 Zotero Desktop 只读获取题录、索引正文或本地 PDF。 |
| [get-notes](plugins/paper-project/skills/get-notes/SKILL.md) | 将选定的 Zotero 文献整理为项目内中文研究笔记或稿件素材库。 |
| [literature-review](plugins/paper-project/skills/literature-review/SKILL.md) | 跨学术数据库开展系统文献检索、综述与证据综合。 |
| [liteparse](plugins/paper-project/skills/liteparse/SKILL.md) | 提取 PDF、Office 文档和图片中的文字、版面坐标，支持 OCR 与页面渲染。 |
| [citation-validator](plugins/paper-project/skills/citation-validator/SKILL.md) | 检查 Word 稿件中的引用是否支持对应论断，结合 Zotero 文献评估支持程度。 |
| [pr-intro](plugins/paper-project/skills/pr-intro/SKILL.md) | 撰写或重构以证据为基础的 Physical Review 论文引言。 |
| [big-paper-helper](plugins/paper-project/skills/big-paper-helper/SKILL.md) | 规划、撰写、整合或审查计算材料领域的中文学位论文。 |
| [prl-figure](plugins/paper-project/skills/prl-figure/SKILL.md) | 制作、审查和导出面向投稿的科学图件，组织多面板证据与验证结果。 |
| [yuanzhuo-skill](plugins/paper-project/skills/yuanzhuo-skill/SKILL.md) | 组织人物视角的独立分析、交叉提问与主持式圆桌讨论。 |
