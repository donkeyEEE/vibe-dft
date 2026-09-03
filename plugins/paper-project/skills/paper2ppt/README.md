# `paper2ppt` 技能

[English](README_EN.md)

`paper2ppt` 是论文到 PPT Master 素材的学术适配器。它负责阅读论文、组织证据叙事、和用户确认重点、选择并核验科学图，随后生成一个极简素材目录，并调用同一插件内置的同级 `$ppt-master` 正常 Generate 流程。

## 工作方式

1. 每次询问输出位置。
2. 通过 `paper-project:liteparse` 规范化论文。
3. 确认学术叙事、重点与关键图。
4. 确认视觉意图，但不锁定模板或页面布局。
5. 生成 `brief.md`、`paper.md`、`original/` 和可选 `images/`。
6. 将整个目录作为普通素材交给 PPT Master。

Paper2ppt 自身不包含 PPT Master 运行时，也不生成页级合同、设计规范、SVG、备注文件、QA 报告或 PPTX。同级 PPT Master 可以自由决定页数、模板、不同页面布局、SVG 实现、演讲备注、QA 和最终 PPTX。

## 交付约束

`brief.md` 记录中心信息、听众、重点、限制与图片出处；它是编辑指导，不是机器可解析的页面计划。默认要求演讲备注，不允许动画、转场、音频或视频。每张选定图片都必须记录 `Source` 与 `Preserve`。

用户修改论文重点或图像选择时回到 paper2ppt；修改模板、页面、版式、备注或 PPTX 时由 PPT Master 处理。两个内置技能保持独立职责，不共享运行时，也不自动合并项目。
