---
name: calc-to-spec
description: 在本次自动或协作设计模式下渐进发布完整的单份 Spec，或安全替换既有 Spec 的当前设计。
---
# Calc to Spec

围绕一个已接受 RQ 接下来要回答的具体问题设计并发布 Spec；研究推进时可逐份发布，
无需预先穷尽该 RQ 的全部 Spec。每份 Spec 自身必须完整。也可替换一个既有、尚未闭合
Spec 的当前科学设计。自动设计可自主发布；协作设计须在具体方案获批后发布。
用户明确给出的范围和约束始终有效。
`concluded` Spec 可只读引用，通常以新 Spec 承载后续判断；修改或重开它需要针对具体
变更的人工授权。
涉及 Calc Project 稳定术语或对象边界时，读取[共享领域术语](../../resources/project-context.md)。
开始工作时先加载 `$domain-research`，在讨论、起草和修订中使用其研究推理指引、术语与文档表达规则；
定位目标后提供项目根、RQ 目录及相关记录。术语的收录、确认和更新遵循 `$domain-research`。

## 流程

1. **定位目标。** 解析唯一项目，读取 `ARCHITECTURE.md` 的 `## Calculation Configuration`：
 `Data root:`、`Tracker adapter:`、`RQ location:` 和适用的 `Software profile:`，要求
 `local-markdown`。读取已接受的 `RQ.md`、相关 Spec、前序结果及用户约束。
 新建要求 RQ 为 `active`，主要判断直接服务其问题、`Boundary:` 和成功判据；替换须定位
 唯一 Spec。权威含糊、归属冲突或缺少 concluded 重开授权时停止。
 Issue 验证需求须有设计交接授权；仅“推进 Issue”不足以授权。设计保留来源 Issue 编号、
 路径，完成后向 `$calc-issue` 回传实际 Spec/Task 引用。
 查明设计依据：核对 RQ、前序结果和用户约束能确定的设计内容；仅加载当前问题需要的科学设计参考资料：VASP [设计](references/backends/vasp.md)、
 [MAE](references/backends/vasp-mae.md)、[DMFT](references/backends/dmft.md)、
 [NAMD](references/backends/namd.md)、[磁性链](references/backends/magnetic.md)、
 [能量映射](references/backends/energy-mapping.md)或[Wannier90](references/backends/wannier90.md)。
 模板提供实现基线，不提供科学数值。证据不足时自主选择 `$dev-engineering:research`
 （定向 Markdown 暂存独立 `/tmp` 路径）或 `$paper-project:literature-review`
 （保存至当前研究主线 `06-文献笔记/` 下唯一 Markdown 路径）。Spec 引用实际采用的可核对原始来源。
2. **选择设计模式与证据档位。** 定位目标后，在开始设计时一次向用户提出两个问题，
 展示已有选择和继承值；已明确回答的事项沿用，不重复询问：
   - **设计模式？** 自动设计（建议默认）：依据证据发布，关键科学缺口才访谈；
    协作设计：进入 grill 流程，具体方案获批后发布。
   - **证据档位？** 沿用当前设置（建议默认）、`light` 或 `strict`。当前设置按 Spec
   的明确设置、RQ 的 `Evidence level:`、默认 `light` 的顺序确定；保留已有严格要求，
   `strict` 只来自用户或已接受 RQ 的明确要求。


 等待用户答复后继续，沉默或预选值不视为回答。
 选择协作模式后立即进入 `$dev-engineering:grill-with-docs` 流程，讨论仍需人工判断的问题，包括
 Spec 要回答的问题、Task、依赖、验收和停止规则；
 自动设计只在现有证据仍无法决定的关键科学缺口上调用它。
 已由 RQ 或可靠证据确定的事项不重复访谈；低频假设留到出现具体迹象时处理，
 保留必须预先确定的科学有效性条件或高代价风险。
 项目共用概念交 `$dev-engineering:domain-modeling`。

3. **起草完整 Spec。** 用 [Spec 模板](references/spec-template.md)围绕一个主要判断，声明
 Task、无环依赖、条件、最低充分证据的验收和停止规则；按模板落实证据档位、字段及参数归属。
 Spec、Task、Run 各自在父对象内编号，依赖限于同一 Spec，条件依据已记录的上游结果。
 本次设计的假设与框架写入 `## 上下文`。有确定依据且不改变科学含义的实现值留给
 `$calc-execute`，Spec 显式值具有约束力。必要科学证据未齐时保持未发布。
 草稿完成后按 `$domain-research` 检查完整 Spec，清理冗余表达并核对原意，再展示批准或自动发布。
 修订后重复此检查；主要判断、Task、依赖、条件、验收和停止规则仍由本技能负责。
4. **取得发布批准。** 协作模式展示目标路径、主要判断、Task 与依赖、验收、停止规则和
 准确的 RQ 索引变更；替换还须展示旧 Run、current 选择和活动作业的影响及处置。
 用户明确批准后才可处置作业或写入设计；方案变化（包括预检发现的变更）须重新展示并获批。
 自动模式无需此批准，仍须遵守用户约束和已有执行授权。
5. **预检并写入。** 重读 RQ、目标 Spec、索引及替换证据，核对归属、ID/路径唯一、
 设计完整、目标无其他所有者占用和替换安全；冲突无法安全调和时停止。
 仍有写入者时由 `$calc-execute` 核实，协作模式按已批准方案、自动模式按已有执行授权
 取消或等待，直至无写入风险。新建写入完整 Spec 和准确的 RQ Spec 索引；替换更新同一 Spec
 及必要状态，保留物理 Run。重读核实写入结果；对象新增、状态或其他索引字段变化后，
 立即按项目 `AGENTS.md` 和[进度跟踪表契约](../../resources/progress-tracker.md)维护
 所属 RQ 目录下的 `tracker.json` 并核对一致性；缺少项目约定时交 `$calc-setup` 补齐。
 同内容重试保持幂等，差异按当前权威资料重评，不依赖旧会话提案或批准缓存。
6. **汇报与推进。** 报告 Spec、证据档位和研究前沿。仅设计或发布的委托到此结束；
 已委托推进 RQ 计算时，直接进入 `$calc-execute`。每份 Spec 完成后，只有已接受 RQ
 和结果支持下一主要判断时才继续设计。达到 RQ 成功判据、无证据支持下一判断、
 关键科学缺口未解决或触及用户边界时停止；新 RQ 的发现与创建另行讨论。

## 权威边界

此 skill 拥有 Spec 的主要判断、科学承诺、任务 DAG、条件、验收和停止规则。
`$calc-execute` 拥有 execution-owned 选择、物理 Run 和执行事实。每份 Spec 是其
Task 与 Run 记录的唯一权威；本 skill 不改变 RQ 的问题、边界、成功判据或已接受决策。
