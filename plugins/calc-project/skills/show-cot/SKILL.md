---
name: show-cot
description: 展示计算项目的完整计算归属树（COT）；直接调用时可按用户确认生成 HTML 进展报告，执行交接时可自主生成。
---

# Show COT

展示一个已配置计算项目的计算归属树。使用调用者已解析的项目根目录；若直接调用，
则从当前目录定位唯一已配置项目。若存在歧义，请求项目位置。

读取项目的计算配置，然后读取其 RQ Tracker 权威记录：每份 `RQ.md`、它发布的 Spec，
以及每份 Spec 声明的 Task 和 Run。将整个项目渲染为稳定树：

```text
RQ-NNN <title> [<status>]
└── SPEC-NNN <title> [<status>]
    └── TASK-NNN <title> [<status>]
        └── RUN-NNN [<status>]
```

Task 之间依赖保留在 Spec 中，不绘制为 COT 边。

使用 `▶` 和粗体突出当前活跃的 Spec、Task 与 Run。

## 进展报告

在对话中展示完整 COT 后，直接调用或由进度查询进入时，询问用户是否需要 HTML 形式的
详细进展报告，并仅在本次确认后生成。由 `$calc-execute` 在交还控制前调用时，依据本次
执行的复杂度自主决定是否生成报告；无需再次询问。无论是否生成，始终展示完整文本树。

决定生成后调用 `$show-me`，根据刚读取的同一组权威记录生成单文件、离线可打开的 HTML。
报告提供机械统计、当前 `RQ → Spec → Task → Run` 路径、下一关注点、当前分支和完整 COT；
下一关注点只陈述可由状态、current 标记和显式依赖直接推导的事实。报告不作科学判断，
不解释失败原因，也不代替 owning workflow 推荐执行操作。若 `$show-me` 不可用，保留已经展示的
文本树，明确报告未生成，不改动项目文件。

将生成的报告写至：

```text
<project-root>/.calc-project/progress-report-YYYY-MM-DD.html
```

日期采用运行环境本地日期。报告生成时：

1. 确保项目根 `.gitignore` 含有等价于 `/.calc-project/` 的忽略规则；规则缺失时仅追加这一条，
   不改写其他内容。
2. 先在 `.calc-project/` 中完成并检查本次独立 HTML；确认文件可读且不依赖 CDN、远程字体或
   远程脚本后，删除该目录下既有的 `progress-report-*.html`，再将本次文件置于目标路径。
3. 删除范围只包括 `.calc-project/progress-report-*.html`。保留该目录中的其他文件，并在答复中
   返回新报告的可点击路径。

`show-cot` 对 RQ、Spec、Task、Run 及其他权威记录保持只读。进展报告是可删除、可再生的派生视图，
不拥有计算事实或进度状态。
