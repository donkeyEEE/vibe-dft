---
name: calc-rq
description: 创建、检查、修订或推导一个计算研究问题，并记录其已接受决策。
---

# Calc RQ

负责 RQ 生命周期及其已接受决策。RQ 存储配置只定义存储约定；`RQ.md` 是 RQ 的唯一权威。
涉及 Calc Project 稳定术语或对象边界时，读取[共享领域术语](../../resources/project-context.md)。

1. 解析唯一计算项目。读取其 `ARCHITECTURE.md` 的 `## Calculation Configuration`，再解析配置的
   `Data root:`、`Tracker adapter:` 与 `RQ location:`。要求使用 `local-markdown` adapter。
   创建时解析唯一父主线；否则以稳定 ID 或路径解析唯一目标 RQ。无匹配或多匹配时请用户选择。
   缺失或无效配置会停止本动作，并应交由 `$calc-setup`。
2. 创建时读取已解析主线下的 sibling RQ 目录以避免 ID 冲突。既有 RQ 工作时读取所选 `RQ.md`；
   意图涉及 concluded Spec 影响时还读取相关已发布 Spec。将这些文件视为权威，而非对话摘要。
   RQ 问题与已接受决策只保存在 `RQ.md`；进度跟踪表按项目 `AGENTS.md` 的进度跟踪表约定维护。
3. 创建或推导 RQ，或变更其 Question、Question 下的 `Boundary:` 或 Success Criterion 时，
   调用 `$dev-engineering:grill-with-docs`。若此依赖不可用，只停止该工作流并报告；不需要
   此工作流的检查和已决定 RQ 更新仍可进行。将访谈产生的 RQ 范围术语和框架记录于
   `RQ.md` 的 `## Context`；仓库根 `CONTEXT.md` 仅保留稳定的项目级领域术语。在当前对话中
   解决未回答问题。用户回答后，在 `RQ.md` `## Decisions` 下提出准确新增或替换；不得单独
   持久化 RQ 访谈待答问题。执行发现的 Issue 由 `$calc-issue` 独立维护。
   来自 Issue 的新 RQ 提案读取其证据，沿用本流程批准；获批后回传实际 RQ 路径供 Issue 关联。
4. 创建时用[RQ 模板](references/rq-template.md)起草 RQ。`RQ-NNN` ID 在其父主线内稳定且未使用。
   用户可在 RQ 上明确设置 `Evidence level: light | strict`；未设置时省略该字段并默认 `light`。
   已发布 Spec 的生效档位在其发布时固定，不因后续 RQ 更新而自动变化。
5. 展示准确的拟议文件路径和完整 Markdown 变更。等待调用约定要求的所有批准：创建或推导 RQ，
   以及每次正式 RQ 更新，都需要明确批准。批准只约束已展示提案；任何变更后都要修订并重新展示。
   concluded Spec 的 Closure 影响在批准前仍是提案；报告其为已接受、已拒绝或待定。批准创建后，
   创建配置的 RQ 目录及其中的 `RQ.md` 与 `specs/`。
6. 每次写入后重读 `RQ.md`；RQ 状态或其他索引字段变化、新增 RQ 时，立即直接维护
   所属 RQ 目录下的 `tracker.json` 并核对一致性。遵循项目 `AGENTS.md` 和
   [进度跟踪表契约](../../resources/progress-tracker.md)；缺少项目约定时，规则补齐交由 `$calc-setup`。
   当已接受决策足以覆盖预期回答范围，且用户未完成请求包含 Spec 设计时，
   直接进入 `$calc-to-spec`，携带已解析 RQ、路径、已接受决策和完整剩余意图，使其能设计
   当前有证据支持的下一份完整 Spec。缺少批准或配置的 RQ 存储不可用时停止。稳定配置或 Spec 设计问题
   直接调用 owning business sibling；仅在工作流选择本身仍开放时使用 `$ask-lyz`。

不得在此接口内创建或变更 Spec、Task、Run、计算输入或执行状态。sibling 交接无需另行授权，
但接收 skill 保留其拥有的所有批准和外部动作门槛。
