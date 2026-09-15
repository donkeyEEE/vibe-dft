---
name: show-cot
description: 展示计算项目的完整计算归属树（COT），以检查 RQ、Spec、Task 与 Run 历史。
---

# Show COT

展示一个已配置计算项目的只读计算归属树。使用调用者已解析的项目根目录；若直接调用，
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
