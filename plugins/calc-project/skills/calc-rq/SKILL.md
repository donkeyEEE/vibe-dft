---
name: calc-rq
description: 创建、检查、修订或推导一个计算研究问题，并记录其已接受决策。
---

# Calc RQ

负责 RQ 生命周期及其已接受决策。RQ 存储配置只定义存储约定；`RQ.md` 是 RQ 问题、决策及状态的唯一权威。
涉及 Calc Project 稳定术语或对象边界时，读取[共享领域术语](../../resources/project-context.md)。

1. 解析唯一计算项目。读取其 `ARCHITECTURE.md` 的 `## Calculation Configuration`，再解析配置的
   `Data root:`、`Tracker adapter:` 与 `RQ location:`。要求使用 `local-markdown` adapter。
   创建时解析唯一父主线；否则以稳定 ID 或路径解析唯一目标 RQ。无匹配或多匹配时请用户选择。
   缺失或无效配置会停止本动作，并应交由 `$calc-setup`。
2. 创建时读取已解析主线下的 sibling RQ 目录以避免 ID 冲突。既有 RQ 工作时读取所选 `RQ.md`；
   意图涉及 concluded Spec 影响时还读取相关已发布 Spec。将这些文件视为权威，而非对话摘要。
   RQ 问题与已接受决策只保存在 `RQ.md`；进度跟踪表按项目 `AGENTS.md` 的进度跟踪表约定维护。
   读取项目根 `CONTEXT.md` 和当前 RQ 目录下已有的 `RQ-CONTEXT.md`。
   创建或修改 RQ 时加载 `$domain-research`，提供项目根与目标 RQ 目录，由它维护 RQ 上下文；
   首次创建 `RQ-CONTEXT.md` 时由它自行读取共享领域术语作为基础。
   重点核对研究问题及假说／假设的表述；本技能继续负责问题推敲、已接受决策及 RQ 写入。
3. 创建或推导 RQ，或变更其 Question、Question 下的 `Boundary:` 或 Success Criterion 时，
   调用 `$dev-engineering:grill-with-docs`。若此依赖不可用，只停止该工作流并报告；不需要
   此工作流的检查和已决定 RQ 更新仍可进行。访谈形成的项目共用概念交给
   `$dev-engineering:domain-modeling` 维护于项目根 `CONTEXT.md`；RQ 范围术语交给
   `$domain-research` 维护于同目录的 `RQ-CONTEXT.md`，不写入 `RQ.md`。
   旧 RQ 内嵌上下文按需迁移：由 `domain-research` 整理至 `RQ-CONTEXT.md`，本技能在
   展示并获批的 RQ 更新中移除旧 Context／上下文章节，保持问题、决策和状态不变。在当前对话中
   解决未回答问题。用户回答后，在 `RQ.md` `## Decisions` 下提出准确新增或替换；不得单独
   持久化 RQ 访谈待答问题。执行发现的 Issue 由 `$calc-issue` 独立维护。
   来自 Issue 的新 RQ 提案读取其证据，沿用本流程批准；获批后回传实际 RQ 路径供 Issue 关联。
4. 创建时用[RQ 模板](references/rq-template.md)起草 RQ。`RQ-NNN` ID 在其父主线内稳定且未使用。
   用户可在 RQ 上明确设置 `Evidence level: light | strict`；未设置时省略该字段并默认 `light`。
   已发布 Spec 的生效档位在其发布时固定，不因后续 RQ 更新而自动变化。
5. 展示准确的拟议文件路径和完整 Markdown 变更。等待调用约定要求的所有批准：创建或推导 RQ，
   以及每次正式 RQ 更新，都需要明确批准。批准只约束已展示提案；任何变更后都要修订并重新展示。
   concluded Spec 的 Closure 影响在批准前仍是提案；报告其为已接受、已拒绝或待定。批准创建后，
   创建配置的 RQ 目录及其中的 `RQ.md` 与 `specs/`，再将已确认的 RQ 术语交给
   `$domain-research` 按需创建 `RQ-CONTEXT.md`；RQ 未获批创建前只保留术语提案。
6. 每次写入后重读 `RQ.md`；RQ 状态或其他索引字段变化、新增 RQ 时，立即直接维护
   所属 RQ 目录下的 `tracker.json` 并核对一致性。遵循项目 `AGENTS.md` 和
   [进度跟踪表契约](../../resources/progress-tracker.md)；缺少项目约定时，规则补齐交由 `$calc-setup`。
   当已接受决策足以覆盖预期回答范围，且用户未完成请求包含 Spec 设计时，
   直接进入 `$calc-to-spec`，携带已解析 RQ、路径、已接受决策和完整剩余意图，使其能设计
   当前有证据支持的下一份完整 Spec。设计模式由 `$calc-to-spec` 在本次设计入口选择，
   不在 `RQ.md` 记录设计模式；本 skill 不为该选择另设 RQ 更新或批准。
   缺少批准或配置的 RQ 存储不可用时停止。稳定配置或 Spec 设计问题
   直接调用 owning business sibling；仅在工作流选择本身仍开放时使用 `$ask-lyz`。

不得在此接口内创建或变更 Spec、Task、Run、计算输入或执行状态。sibling 交接无需另行授权，
但接收 skill 保留其拥有的所有批准和外部动作门槛。
