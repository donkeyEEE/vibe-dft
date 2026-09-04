---
name: cangjie-skill
description: Developer-only workflow for distilling accessible sources into experimental paper or calculation knowledge. Its long-term write, admission, promotion, and governance model remains intentionally open.
---

# cangjie-skill — 长内容到 ATOM CARD 的蒸馏流程

> 当前仅供本仓库开发维护使用，不作为已发布插件的稳定知识写入接口。

RIA-TV++ 在此保留为理解、提取与验证的来源方法；其终点已改为 ATOM CARD，而非可执行 Skill。
其中的三重验证仍用于阻止孤立摘录、空泛常识和未经证实的推断进入插件知识。

## 使命

将书籍、论文或博客中的知识蒸馏为插件本地的实验性原子卡片或计算模板候选，而不是生成新的 Skill。
通用卡片须可被多个 skill 复用；物理卡片面向未来检索，不以当前消费者数量作为准入条件。
卡片供现有 paper-project skills 按需读取；请求 skill 自己保留任务逻辑与输出责任。
Cangjie 当前只对 paper-project 卡片保留开发写入流程；先读取
`../prl-shared/references/knowledge-source.yaml` 定位仓库，再遵循
`../prl-shared/references/admission-contract.md` 的统一准入规则。

## 输入

开始前必须确认：

1. **来源类别与文本**：通用卡接受书籍、论文或博客；物理卡还接受预印本、教材、学位论文、技术报告和课堂笔记。用户必须提供可访问的 PDF、HTML、TXT、Markdown、纯文本或可读取笔记，不能凭记忆蒸馏。物理候选还必须实际核对来源内容，不能把 DOI、书名或其他书目信息本身当作支持证据。
2. **来源元信息**：记录能够重新识别来源的现有信息；课堂笔记优先记录课程、讲授者或记录者和年份。博客只能补充已由非博客来源建立的物理卡。
3. **人类意图**：用户希望这些知识服务于什么任务，例如计算方法、物理概念、论文写作、引文检查或投稿规范。

输入是计算维护 track、运行证据或现有 `TRK-NNN` 候选时，先读
[`methodology/10-calc-track-distillation.md`](methodology/10-calc-track-distillation.md)，
将 observation、evidence、conditions and limits、candidate knowledge、冲突和建议归属整理到
`plugins/calc-project/knowledge/candidates/cards/calc-project/`。该候选区只供治理流程使用，不是正式消费输入。

AI 根据来源和人类意图提出候选 ATOM CARD 的 `name`、`type` 和 tags；物理候选还要展示
`new card`、`append source`、`revise card` 或 `split card` 拟执行动作、核心陈述和来源定位。
用户确认、删减或调整卡片类型后，才写入插件知识。
类型和写入动作不能由 AI 单方面决定。

## 长来源与多来源项目模式

处理整本书、长篇学位论文，或围绕同一主题联合抽取多个来源时，必须先读
[`methodology/09-project-workspaces.md`](methodology/09-project-workspaces.md)，以主题建立可追溯的
显式指定 `/home/donk/plugins/knowledge-distillation/<project-id>/` 工作区，再进入阶段 0。该路径是本机
推荐布局，不是代码默认值；每次调用管理脚本仍必须传入 `--project-root`。即使用户手动拆出所需章节，只要工作仍属于
同一个长来源或计划继续补充多来源，也沿用该项目。短小、单次、单来源任务可以直接执行下述阶段流程。

## 输出

当前可写目标仅为 paper-project 的开发工作树：

```text
plugins/paper-project/knowledge/
├── candidates/cards/                       # 未晋升卡片，禁止消费
├── cards/atoms/<atom-name>.md              # 正式通用 ATOM CARD
└── cards/INDEX.md                          # 正式卡片导航
```

物理卡、计算模板和计算经验的既有内容位于
`plugins/calc-project/knowledge/`。在未来知识治理模型确定前，Cangjie
可维护明确标记的开发候选或生成可审阅提案，但不晋升或改写 calc-project 正式知识。

构造候选或交付前，必须先读 `../prl-shared/SKILL.md`，再读
`../prl-shared/references/admission-contract.md` 和 `plugins/paper-project/knowledge/cards/INDEX.md`；处理物理候选时还必须读
`plugins/calc-project/knowledge/cards/physics/PHYSICS_INDEX.md`。完全遵循相应知识区域的准入、命名和索引规则。
卡片 frontmatter 只能包含 `name`、`type`、`tags`、`updated_at`。

## 流程

### 阶段 0 — 来源理解

按 `methodology/01-stage0-adler.md` 建立来源骨架、关键术语、论证结构、局限和潜在复用价值。论文要区分作者主张、证据与推断；博客要标出经验判断与可核查事实。

### 阶段 1 — 多视角提取

使用 `extractors/` 从框架、原则、案例、反例和术语五个视角形成候选池。长文按自然章节、段落或小节分块，并保留定位信息供后续正文引用。

### 阶段 1.5 — 验证与类型共决

通用候选执行 `methodology/03-stage1.5-triple-verify.md` 的证据、迁移性和非平庸性检查。
物理候选改为检查来源支持、知识价值、原子性以及与现有物理卡的一致性；其中来源可追溯表示能够重新识别来源，来源验证表示 AI 已实际核对内容并确认它支持候选陈述。随后向用户展示候选卡片、AI 建议的类型、tags、拟执行动作、核心陈述与来源定位；只有获得用户确认的卡片才能继续。

一份来源可以产生一批原子候选。候选必须完整展示后，用户可逐项确认或整体接受。物理卡的新建、
追加来源、修订、争议判断、同名异义拆分和关系维护遵循
[物理卡片演化协议](methodology/08-physics-card-evolution.md)。

### 阶段 2 — 构造 ATOM CARD

先读 `../prl-shared/SKILL.md`、`../prl-shared/references/admission-contract.md` 和
`plugins/paper-project/knowledge/cards/INDEX.md`。通用卡按
`templates/ATOM_CARD.md.template` 构造；物理概念卡继续读取物理索引，并按
`templates/PHYSICS_CONCEPT_CARD.md.template` 构造；物理现象卡按
`templates/PHYSICS_PHENOMENON_CARD.md.template` 构造；物理理论与模型卡按
`templates/PHYSICS_THEORY_MODEL_CARD.md.template` 构造。每张卡只承载一个知识对象，正文首段必须直接陈述该原子知识。现象卡必须把可观察特征与解释分开；表面特征本身不能被写成唯一机制的充分证明。

理论与模型卡统一承载理论、定律、机制、模型、方程、公式和近似关系，不为这些形式增加额外 type
或层级 tag。公式使用 LaTeX；存在公式时必须定义必要变量、单位或单位制和符号约定。预测和解释仅在适用时保留，不输出空章节。公式默认与它表达的模型、定律或物理关系同卡；只有公式具有独立用途和独立适用边界时才单独成卡。

原子性限制知识对象数量，不限制解释深度。理论卡枚举多个极限、机制分支或构成部分时，每一项至少说明
定义、成立原因、物理含义和边界；不能只给名称或一句释义。只有某一项形成独立知识对象，并需要自己的
推导、关系或多来源解释时才拆卡。

附加素材完全可选。只有 SVG 或 PNG 能直接解释候选卡片的核心知识，或呈现难以用简短文字替代的观察证据时，才把它作为候选与卡片一同展示。候选须说明拟保存名称、`explanatory` 或
`evidence` 用途、替代文本和来源；获得用户确认后才保存到所属卡片的素材目录。`evidence`
素材不能替代 `Sources` 中的来源条目。素材可由其他卡片通过相对链接复用。

物理卡正文中每个关键概念首次出现时写成“中文名称（规范英文术语）”；常用缩写在同一处定义。后续优先
使用中文或已定义缩写。规范英文术语与来源原措辞不同时，在相关 `Sources` 条目的 `Supports` 中保留能够
识别该概念的最短原文短语；不为保留英文而复制整段原文。公式变量、专名和容易产生歧义的术语按需持续
保留英文。

### 阶段 3 — 纳入插件索引

先将 paper 候选写入 `plugins/paper-project/knowledge/candidates/cards/`。获得用户确认后，通用卡片平铺晋升到 `plugins/paper-project/knowledge/cards/atoms/` 并更新 paper 索引。计算经验或模板只可写入 calc-project 的 `candidates/`；物理卡停在用户可审阅提案。三者均不进入 calc-project 正式索引。

### 阶段 4 — 原子性与可用性检查

逐张检查：文件名与 `name` 一致、frontmatter 只有四个允许字段、首段只有一个原子主张、tags 可从相应索引导航、没有与现有卡片的重复或未报告冲突。物理概念卡还须包含核心陈述、定义与区分、条件与边界、关系和来源；物理现象卡须包含核心陈述、可观察特征、条件与边界、关系和来源；理论与模型卡须包含核心陈述、形式化表达、假设、条件与边界、关系和来源，并在存在公式时检查变量与单位。每个素材必须属于一张现存卡片、至少被一张卡引用且链接有效。冲突必须报告给用户，不得自行合并为未经验证的新规则。

### 阶段 5 — 交付

通用卡运行 `../prl-shared/scripts/validate_knowledge_repository.py ../../knowledge`；物理卡或计算模板运行 calc-project 的知识测试。汇报新增或更新的资源、执行动作、type、tags、索引状态、验证结果、Git revision 和 dirty 状态；不得自动提交。不要安装任何 Skill，不生成 `test-prompts.json`，也不接入 darwin-skill。

## 质量红线

1. 没有原始文本或人类意图，不得开始写卡片；只有书目信息不构成来源验证。
2. 每张卡只写一个原子知识，不能变成小型综述或 Skill。
3. 每次 paper 卡写入前都必须先读取 `prl-shared/SKILL.md`、`references/knowledge-source.yaml`、准入接口和插件内正式索引。
4. `type` 必须由 AI 建议并经用户确认；tags 必须可由相应索引导航。
5. 来源、引用和不确定性可写在正文中，但不得擅自加入额外 frontmatter 字段。
