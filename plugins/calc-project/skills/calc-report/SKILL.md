---
name: calc-report
description: 从 Calc Project 的 RQ、Spec、Run 和相关结果生成可追溯的阶段汇报或结果汇报 HTML。
---

# Calc Report

围绕一个汇报主题组织已有计算证据，并在
`<project-root>/.calc-project/results-<tag>/` 生成一份 HTML 计算汇报。

1. 解析唯一计算项目。入口可以是一个或多个 RQ、可选的 Spec 限定，或自然语言汇报主题。
   主题入口只做轻量发现。根据明确措辞选择阶段汇报或结果汇报；意图实质含糊时询问。默认受众是
   熟悉领域但未跟踪日常计算的合作者。
2. 展示一份简短的范围预览，包含主题、汇报意图、候选 RQ/Spec、拟用 tag，以及需要确认的
   非 RQ/Spec 补充结果。用户可直接确认或用自然语言修改。复用已有 tag 时在同一预览中确认；
   该 tag 对应的整个 workspace 会原地重新生成。
3. 读取选定的 RQ、Spec、Task、Run 记录及其指向的结果。默认使用 current Runs 和被 Task
   接受的 Runs；历史 Run 仅在说明进展、失败、替换或比较时纳入，其他 RQ 的证据仅在确认范围内
   纳入。补充结果保留来源限制，不能单独满足 RQ 或 Spec 的验收准则。
4. 在确认的 workspace 中准备本次实际消费的轻量汇报源数据或提取结果。大型输出保留在原 Run
   或数据根。生成 `provenance.json`，记录实际消费的数据、图件和核心结论所对应的 RQ、Spec、
   Task、Run、具体来源及提取或推导，并记录可能影响理解的反证、缺口和排除项。只创建实际使用的
   `data/`、`scripts/` 与 `figures/`。
5. 复用合适的已有图件。确实需要新增或重制科学图件时，向 `$prl-figure` 提供图件要表达的结论、
   证据角色、源数据与 provenance、尺寸和 workspace 目标；绘图实现、后端、导出与视觉 QA 由
   `$prl-figure` 决定。
6. 默认调用 `$show-me`，向其提供主题、阶段或结果意图、选定科学内容、provenance、需要说明的
   证据限制和 `report.html` 目标。HTML 的叙事顺序、布局、视觉系统、生成行为与交付检查均由
   `$show-me` 决定。
7. 证据不足、陈旧、互相矛盾或仅存在于远程时仍生成汇报，在相关位置如实说明。阶段汇报呈现已有
   证据、进展、缺口和已批准的执行前沿；结果汇报直接回答主题，当前无法回答的部分明确指出所缺
   证据。完成后返回已确认的范围和可点击的 `report.html` 路径。

汇报 workspace 是可删除、可再生的派生产物，不作为 RQ、Spec、Task 或 Run 的权威记录。
