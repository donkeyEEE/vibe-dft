# Core principles (citation-validator)

校验学术论文 Word 文档中引用文献的合理性：对指定段落，自动识别其中的引用标记，通过 Zotero 获取每篇被引文献的摘要或全文，逐条评估该文献是否真正支撑此处声明，并按保守的支撑等级输出结构化报告。

## 核心能力

- 从 Word 文档中提取指定段落的文本（通过 liteparse）
- 自动识别段落中的引用标记：数字编号 `[1]`、作者-年份 `(Smith, 2020)`、上标等
- 对每条引用，通过 Zotero 搜索并获取文献元数据、摘要和（按需）全文
- 按五级支撑框架评估每篇文献是否真正支撑所在声明
- 输出结构化报告，标明问题引用、支撑等级和建议操作

## 默认范围

- **输入**: 一个 .docx 文件路径 + 段落范围（如 "第3段" 或 "段落1-5"）
- **引用风格**: 自动检测数字编号 `[1]`、作者-年份 `(Author, Year)`、上标等
- **Zotero 来源**: 通过 Zotero Desktop 本地 API 读取（只读，不修改）
- **评估深度**: 优先使用摘要；摘要不足时请求全文片段；不编造未读内容

## 不做什么

- 不修改 Word 文档或 Zotero 条目
- 不安装新软件或 Python 包
- 不搜索在线数据库（仅使用 Zotero 本地库中已有的文献）
- 不替用户决定是否删除引用（仅给出建议）
- 不处理非学术引用（新闻、博客、专利等）

## 支撑等级定义

五级保守支撑评估（详见 `static/core/support-grading.md`）：

| 等级 | 含义 | 可引用？ |
|------|------|----------|
| 强支撑 | 论文直接验证同一核心关系 | ✅ 是 |
| 部分支撑 | 支撑部分或更窄条件 | ⚠️ 需限定 |
| 背景支撑 | 仅支撑领域背景 | ⚠️ 仅背景句 |
| 矛盾/限制 | 与声明冲突或缩小范围 | ❌ 否 |
| 无证据 | 摘要/全文与声明无关 | ❌ 否 |

## Zotero 访问原则

- 只读访问 Zotero Desktop 本地 API
- 只通过 `get-zotero` 的只读 CLI seam 搜索和获取数据
- 验证 content artifact contract 后，优先使用 metadata 中的原始摘要
- 摘要不足时，按 `content.kind` 消费索引正文或本地 PDF artifact
- PDF artifact 的使用遵循 `references/zotero-integration.md`；不下载远端 PDF
- 如果 Zotero 中找不到某篇文献，标记为"未找到"并提示用户

## 源引用

- 支撑评估框架来自 `nature-citation` skill 的支撑分级体系
- Zotero 访问模式来自 `get-zotero` skill
- DOCX 解析通过 liteparse 完成
- 引用模式识别来自 `references/citation-patterns.md`
