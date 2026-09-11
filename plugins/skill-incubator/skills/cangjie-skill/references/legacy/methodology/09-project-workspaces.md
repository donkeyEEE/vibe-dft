# 长来源与多来源项目工作区

## 何时使用

整本书、长篇学位论文或围绕同一知识主题的多个来源采用项目模式。项目是**主题项目**，不是单来源目录；
一个项目可以逐步加入多个来源，但每条证据始终保留自己的 `source_id`。短小且不会继续扩展的单来源任务
可以使用主流程，不必创建项目。

本机推荐把项目放在独立的非 Git 数据目录中：

```text
/home/donk/plugins/knowledge-distillation/<project-id>/
```

这只是推荐路径，不是 Cangjie 的默认根目录。管理命令始终要求显式传入 `--project-root`；不得通过环境变量
或当前目录暗示项目位置。其他绝对路径只要显式传入也有效。工作区属于用户知识工程数据，不纳入 Git，且
不得进入 paper-project 插件安装包。

## 初始化与来源保全

使用随 Cangjie 分发的单一管理入口：

```bash
python <cangjie-skill>/scripts/manage_distillation_project.py init \
  --project-root /home/donk/plugins/knowledge-distillation/<project-id>/ \
  --project-id <project-id> --topic '<topic>' \
  --source-id <source-id> --source-pdf '<source.pdf>' --title '<title>' \
  --scope-file '<scope.yaml>'
```

`init` 必须复制原始 PDF 到 `sources/<source-id>/source/original.pdf`，记录原始位置与 SHA-256，随后只读取
项目内副本。项目存在时拒绝覆盖。每个来源分别维护 `source.yaml`，因此后续可以加入另一篇论文或书籍，
而不会覆盖先前来源的理解与证据。

## 解析

对 born-digital PDF 使用 LiteParse 且默认关闭 OCR：

```bash
python <cangjie-skill>/scripts/manage_distillation_project.py parse \
  --project-root /home/donk/plugins/knowledge-distillation/<project-id>/ --source-id <source-id>
```

每个来源只保留一个完整的 `parsed/document.json`。`scope.yaml` 中连续 unit 使用一基闭区间
`pdf_pages: [start, end]`；同一 unit 包含多个非连续片段时使用
`pdf_page_ranges: [[start, end], ...]`。两者不得同时出现。解析命令据此按范围顺序导出一个章节文本。
不得再保存章节选择 PDF。只有公式、表格、图像或版面无法由
结构化文本可靠表达时，才在 `screenshots/` 保存局部截图。失败时保留已验证产物；重试前核对来源哈希，
确需重建 JSON 时显式使用 `--force`。

## 抽取与证据

按 scope unit 逐章执行阶段 0–1.5，并分别维护：

- `extraction/<unit>.yaml`：已处理小节、发现的知识对象、遗漏风险与异常。
- `evidence/<unit>.yaml`：稳定 `evidence_id`、`source_id`、章节、书页、PDF 页，以及可用的 LiteParse
  text item 或 bounding box 定位。

只有 DOI、书名或课堂笔记身份而暂时缺少页码、章节或公式号时允许记录，但状态检查会报告定位警告。
书目信息只能保证来源可追溯，不能替代对原文的来源验证。

## 两层候选与综合

`candidates/by-source/` 保存忠于一个来源的候选表达，防止综合时丢失原意；
`candidates/consolidated/` 保存面向最终知识对象的跨章节、跨来源候选，并引用全部支撑它的
`evidence_id`。只有综合候选进入人工审核和正式交付。来源间存在不同解释时保留各自证据，在综合候选中
并列表达适用范围或争议，不得静默覆盖。

## 单一审核日志

`decisions/review-log.yaml` 是候选审核状态与历史的唯一事实来源。以追加记录保存 `accept`、`reject`、
`revise`、`merge`、`split` 或 `deliver`；候选当前状态由最后一条相关决定推导。候选文件不得复制
`status`。没有用户确认的综合候选不能成为正式卡片。

`project.yaml` 只维护项目与章节的粗粒度阶段：`initialized`、`parsing`、`extracting`、`reviewing`、
`delivering`、`complete` 或 `blocked`。不要把候选审核状态写入该文件。

## 状态、校验与交付

```bash
python <cangjie-skill>/scripts/manage_distillation_project.py status \
  --project-root /home/donk/plugins/knowledge-distillation/<project-id>/ --json
python <cangjie-skill>/scripts/manage_distillation_project.py validate \
  --project-root /home/donk/plugins/knowledge-distillation/<project-id>/ \
  --shared-root <prl-shared-root> --json
```

`status` 只读汇总来源、unit、证据、两层候选和审核决定。`validate` 检查路径边界、来源 SHA-256、证据
ID、候选引用、审核动作及交付映射；错误返回非零状态，缺少精确定位或尚待审核属于警告。

交付时仅将用户确认且已接受的综合候选按对应物理模板写入 `prl-shared`，并在
`delivery/manifest.yaml` 记录候选与正式卡片路径的映射。`delivery/report.md` 只提供简短人类摘要，不维护
状态。

项目只有在所有范围单元已审核或明确跳过、每个综合候选都有最终决定、每个已交付候选都有正式卡片
映射且 `validate` 无错误时，才能标记为 `complete`。
