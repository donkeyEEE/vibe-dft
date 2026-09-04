---
name: zo2notes
description: Use when turning selected Zotero literature into Chinese project-local research notes, or when creating and maintaining a manuscript material library from one user-selected Zotero collection.
---

# Zotero 项目文献笔记（Zo2Notes）

## 路由

- 用户要为既有研究线生成问题导向的单篇阅读笔记时，执行下文的研究笔记流程。
- 用户要在修改论文前建立或更新素材库时，必须让用户明确选择 exactly one Zotero collection，然后完整读取并执行 `references/writing-material-library.md`。素材库路线不得创建或更新 `06-文献笔记/`；研究笔记路线也不得顺带创建论文写作库。

Zotero 是只读文献来源；本技能将一篇已选 Zotero 文献转为现有项目研究线中、可直接服务于研究与计算决策的中文笔记。输出是普通项目目录中的 Markdown 文件，不依赖任何特定笔记软件。笔记的归档位置由用户明确选择的 Zotero collections 决定，不建立或维护根分类索引或全局 collection 映射。

## 前置条件与边界

- 用户必须提供：已有的 `project-root`、已有的 `research-line` 目录、明确的阅读问题（优先引用研究问题卡片），以及相关 Zotero collection 的显式选择。
- `project-root` 和 `<project-root>/<research-line>` 必须已存在。若任一不存在，停止并请用户先创建或指定正确位置；不得创建项目或研究线。
- 只处理一个父级文献条目；`attachment`、`annotation` 与独立 `note` 条目不得作为导入对象，但可作为该父条目的证据来源。
- Zotero 始终只读：不得修改条目、附件、批注或 PDF。
- 导入时仅可新建 `06-文献笔记/` 下必要的目录和映射文件；不得创建其他项目结构。
- 证据顺序固定为 Zotero highlights/notes、Zotero indexed full text，最后才是原始本地 PDF 的定向核验；具体路由遵循 `references/pdf-evidence-strategy.md`。

## Zotero 访问

Zotero Desktop 必须运行，用户须在 Zotero 界面中启用本地 API。先运行只读诊断：

```bash
python3 <plugin-root>/skills/zo2notes/scripts/zotero.py doctor --json
```

自动探测成功时直接使用，不创建配置。需要自定义 host、port、mode 或附件映射时，完整读取 `references/configuration.md`：只询问无法自动判断的值，向用户展示配置路径与完整拟写内容，得到确认后才创建或修改用户配置，然后再次运行 `doctor`。连接或附件访问失败时读取 `references/troubleshooting.md`。

支持 Windows 原生、Windows Zotero + WSL Codex、macOS/Linux 原生。Zo2Notes 不修改 Zotero 设置、profile、条目或附件，也不重启 Zotero 或导入记录。

可使用随附的只读辅助命令诊断或定向取证：

```bash
python3 <plugin-root>/skills/zo2notes/scripts/zotero.py status --json
python3 <plugin-root>/skills/zo2notes/scripts/zotero.py search "<query>" --json
python3 <plugin-root>/skills/zo2notes/scripts/zotero.py children <itemKey> --json
python3 <plugin-root>/skills/zo2notes/scripts/zotero.py fulltext <attachmentKey> --out /tmp/zotero-fulltext.txt
```

仅在需要附件详情或核验原文时使用 `children` 与 `fulltext`；全文写入临时文件，正常流程不输出整篇文章。只有在 Zotero indexed full text 无法可靠表达图、表、公式、页内位置或文本层不可用时，才取得该条目的本地附件地址并使用 LiteParse 定向解析；不得扫描无关附件目录。

### VS Code 中的 PDF 证据链接

仅在 VS Code Remote WSL 且已安装 `donk.zotero-wsl` 扩展时生成可点击的 Zotero PDF 页码链接：

```markdown
[证据说明](vscode://donk.zotero-wsl/open-pdf?item=<attachmentKey>&page=<page>)
```

`item` 必须是八位大写字母或数字组成的 Zotero **附件 key**，不得使用父条目 key；`page` 是从 1 开始的 PDF 页码。其他编辑器、原生 Windows、macOS、Linux或扩展不可用时，保留附件 key 与页码作为纯文本证据定位信息。

## 项目内存储契约

每个已选且属于该条目的 Zotero collection 都有一个笔记位置：

```text
<project-root>/<research-line>/06-文献笔记/01-单篇文献/<selected Zotero collection path>/<item-key>.md
```

映射文件固定为：

```text
<project-root>/<research-line>/06-文献笔记/zotero-project-map.yaml
```

该文件只记录用户明确选为本项目相关的 collections，绝不扫描或导入所有 Zotero collections。同一条目属于多个已选 collection 时，在每个对应目录各生成一份笔记；每份笔记可围绕该分类的阅读重点撰写。未选 collection 不生成目录或笔记。

```yaml
version: 1
selected_collections:
  - zotero_collection_key: "ABCD1234"
    zotero_path: "磁性材料/Fe3GaTe2"
    project_path: "磁性材料/Fe3GaTe2"
```

`project_path` 必须与所选 `zotero_path` 的安全相对路径一致。只在用户确认导入后，新建所需的 `06-文献笔记/01-单篇文献/...` 目录并创建或更新此映射。

## 导入流程

1. **确认研究问题卡片**：对一个新专题，在 `02-专题综合/<主题>-研究问题卡片.md` 复制 `references/研究问题卡片模板.md`，填写当前问题、必答子问题、优先证据及预期项目产出；已存在卡片时确认本条目适用的阅读问题与分类重点。
2. **确认输入**：记录阅读问题、既有项目根与研究线；展示该文献所属 collections，并确认其中哪些已选为项目分类。没有任何已选分类时，不写入。
3. **读取题录与归属**：取得父条目的 item key、题名、作者、年份、刊物、DOI、URL、摘要、附件 key 和所有 Zotero collection memberships。
4. **确认目标**：解析每个已选分类对应的笔记路径和项目映射路径。只将用户选择的 collection 写入 `selected_collections`；不创建分类索引或全局映射。
5. **提取文本证据**：先读取 highlights/notes；仅在其不足以回答阅读问题时，按需读取附件的 Zotero indexed full text。若索引覆盖完整且正文可读，以 Zotero 文本作为默认正文来源。
6. **定向核验 PDF**：只有在问题依赖图、表、复杂公式、页内位置，或 Zotero 索引缺页、乱码、阅读顺序不可靠时，才读取该条目的原始本地 PDF。数字版 PDF 使用 LiteParse JSON 与页面截图，并显式关闭 OCR；扫描件或损坏文本层才启用 OCR。只解析必要页面，产物写入临时目录，不复制 PDF 到项目。
7. **撰写笔记**：以 `references/论文精读模板.md` 为结构，围绕研究问题卡片的阅读问题给出直接回答、证据与适用条件、对项目的影响、冲突与后续验证。区分 Zotero 批注、Zotero 索引全文、原始 PDF 文本层、PDF 视觉核验和 OCR 证据；可靠页码按“VS Code 中的 PDF 证据链接”生成可点击链接，适配不可用时写成纯文本附件 key 与页码。
8. **无全文降级**：若没有附件，或 Zotero 索引与原始 PDF 都无法提供可用正文，仍生成笔记，但必须在 YAML 与正文标示：`无可用全文：仅记录元数据与摘要，未据此推断正文结论。` 必须保留原始摘要于 YAML `abstract` 字段和 `## 原始摘要` 节；此时只使用题录和原始摘要，不把摘要扩写为原文结论。
9. **验证并写入**：检查 YAML、证据来源标记、Markdown 数学分隔符（若有）、VS Code Zotero 链接中的附件 key 与页码，以及每个已选分类路径；在每个已选分类目录写入对应笔记，并更新项目映射。

## 笔记内容要求

笔记必须回答用户的阅读问题，而不是泛化摘录。正文至少包含：

- **直接回答**：对阅读问题给出可追溯的结论，或明确说明证据不足。
- **证据与条件**：区分作者主张、Zotero 批注、索引全文、原始 PDF 文本层、页面视觉核验与 OCR 证据；写明页码、材料、温度、方法、模型、计算参数或其他适用边界。
- **对项目的影响**：说明它改变、支持或限制哪些研究判断、模型选择、参数范围、计算设置、结果解释或下一步工作。
- **冲突与局限**：列出与当前项目假设、其他文献或数据不一致之处，以及证据强度不足之处。
- **后续验证**：提出可执行的验证动作，例如复现实验条件、补读特定页段、做敏感性测试、比较另一篇文献或新增计算。

## 手工维护的跨文献格式

下列内容是项目研究者手工维护的工作产物：不得在单篇导入时自动创建、自动更新或从 collection 生成。

`06-文献笔记/` 只使用 `01-单篇文献/`、`02-专题综合/` 与 `03-证据矩阵/`；后两者由研究者手工维护。

### 专题综合

```markdown
# <专题>

## 要回答的问题
<研究/计算决策问题>

## 综合判断
<直接判断、置信度与适用条件>

## 一致与冲突证据
<按结论而非按文献逐条组织，标注 item key>

## 对计算路线的影响
<参数、模型、工作流或验证优先级>

## 待验证
<可执行动作与完成判据>
```

### 证据矩阵

```markdown
| 问题/主张 | 文献 item key | 证据位置 | 条件与方法 | 支持/冲突 | 对计算的影响 | 待验证 |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |
```

## 不在范围内

- 批量 collection 导入、进度日志或自动跨文献关联。
- 创建项目、研究线、根分类索引或全局 collection 映射。
- 修改 Zotero、附件、PDF 或用户已有项目数据；把原始 PDF 或临时解析产物复制进项目。
