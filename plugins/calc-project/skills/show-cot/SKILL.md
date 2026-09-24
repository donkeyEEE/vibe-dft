---
name: show-cot
description: 展示计算项目的完整计算归属树（COT）；直接调用时可按用户确认生成 HTML 进展报告，执行交接时可自主生成。
---

# Show COT

展示一个已配置计算项目的计算归属树。使用调用者已解析的项目根目录；若直接调用，
则从当前目录定位唯一已配置项目。若存在歧义，请求项目位置。

读取项目的计算配置，按 `RQ location:` 枚举配置范围内实际 RQ 目录，读取每个 RQ 内的
`tracker.json` 并汇总已记录进度；不保存项目级跟踪表。使用 RQ 的项目相对路径区分不同主线
内重复的 RQ ID。日常查询无需逐篇读取 RQ 或 Spec，也不要求全量扫描正文以验证索引新鲜度。
某份跟踪表缺失、损坏、条目异常、已知未同步或用户要求核对时，仅回查该 RQ.md 及其已发布
Spec 并修复该表，不能因缺少 tracker 而跳过该 RQ。读取
[进度跟踪表契约](../../resources/progress-tracker.md)处理字段与重建；项目约定缺失时，
规则补齐交由 `$calc-setup` 按其授权规则处理，本次查询可继续，不自行修改项目 `AGENTS.md`。
无法完成修复时明确展示覆盖范围和未同步 RQ，不将局部汇总称为完整项目。
将汇总结果渲染为稳定树：

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

决定生成后调用 `$show-me`，根据本次读取的同一组 RQ 跟踪表生成单文件、离线可打开的 HTML，
注明各 RQ 跟踪表的更新时间；仅为索引未包含的依赖或详细记录按需读取相关 Spec。
报告提供机械统计、当前 `RQ → Spec → Task → Run` 路径、下一关注点、当前分支和完整 COT；
下一关注点只陈述可由状态、current 标记和显式依赖直接推导的事实。报告不作科学判断，
不解释失败原因，也不代替 owning workflow 推荐执行操作。若 `$show-me` 不可用，保留已经展示的
文本树，明确报告未生成，不为报告新增或删除文件。

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
