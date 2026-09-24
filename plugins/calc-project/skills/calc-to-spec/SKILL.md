---
name: calc-to-spec
description: 为已接受 RQ 渐进设计并自主发布完整的单份 Spec，或安全替换既有 Spec 的当前设计。
---

# Calc to Spec

围绕一个已接受 RQ 的当前下一项主要判断设计并发布 Spec；研究推进时可逐份发布，
无需预先穷尽该 RQ 的全部 Spec。每份 Spec 自身必须完整。也可替换一个既有、尚未闭合
Spec 的当前科学设计。新建与安全替换不另设发布批准；用户明确给出的范围和约束始终有效。
`concluded` Spec 可只读引用，通常以新 Spec 承载后续判断；修改或重开它需要针对具体
变更的人工授权。
涉及 Calc Project 稳定术语或对象边界时，读取[共享领域术语](../../resources/project-context.md)。

## 流程

1. 解析唯一计算项目，读取 `ARCHITECTURE.md` 的 `## Calculation Configuration`、
   已接受的 `RQ.md`、相关已发布 Specs、前序结果和用户明确约束。新建要求 RQ 为
   `active`。读取配置的 `Data root:`、`Tracker adapter:`、`RQ location:` 和适用的
   `Software profile:`；要求 `local-markdown`。
   新建时确认当前主要判断直接服务于该 RQ 的问题、`Boundary:` 和成功判据；替换时通过
   RQ 解析唯一目标 Spec。权威含糊、所有权冲突或既有设计已 `concluded` 而缺少具体
   重开授权时停止，不猜测或覆盖。
   来自 Issue 的验证需求先核实已获设计交接授权；仅有“推进 Issue”的委托不足以
   发布或替换设计。授权后按目标 RQ 设计补充 Spec，或通过本流程安全替换为已有 Spec
   补充 Task；遵守 concluded 边界。设计中保留来源 Issue 编号与路径，完成后回传
   实际 Spec/Task 引用供 `$calc-issue` 更新关联。
2. 解析本次 Spec 的证据档位。Spec 的明确设置优先，其次继承 RQ 的 `Evidence level:`，
   两者都未设置时为 `light`。`strict` 只来自用户明确要求或已接受的 RQ 设置；
   不自行降低已接受的严格要求。发布时将生效的 `Evidence level: light | strict`
   写入 Spec，之后 RQ 档位变化不自动改动既有 Spec。
3. 仅加载当前判断需要的科学设计参考资料：VASP [设计](references/backends/vasp.md)、
   [MAE](references/backends/vasp-mae.md)、[DMFT](references/backends/dmft.md)、
   [NAMD](references/backends/namd.md)、[磁性链](references/backends/magnetic.md)、
   [能量映射](references/backends/energy-mapping.md)或[Wannier90](references/backends/wannier90.md)。
   模板只提供实现基线，不提供科学数值。项目与参考资料不足时，自主选择
   `$dev-engineering:research` 或 `$paper-project:literature-review` 补证据；前者的定向
   Markdown 暂存于独立 `/tmp` 路径，后者使用当前研究主线 `06-文献笔记/` 下唯一的
   Markdown 路径。设计只采用可核对的原始证据，并在 Spec 中引用实际使用的来源。
4. 根据已接受 RQ、结果和调研证据判断是否有关键科学缺口：只有影响主要判断、必要
   可比性或验收，且现有证据仍无法决定的选择才调用 `$dev-engineering:grill-with-docs`。
   访谈形成的 Spec 范围术语和框架写入该 Spec 的 `## 上下文`；真正需要改动 RQ 问题、
   边界或成功判据的事项交回 `$calc-rq`。没有关键缺口时自主完成设计。
5. 用 [Spec 模板](references/spec-template.md)起草当前 Spec。它围绕一个主要判断，
   完整声明 Task、无环依赖、条件、以最低充分证据表述的验收和停止规则。`SPEC-NNN`
   只在所属 RQ 内编号，`TASK-NNN` 只在所属 Spec 内编号，`RUN-NNN` 只在所属 Task
   内编号；依赖仅引用同一 Spec 中的 Task，条件只依据已记录的上游结果。
   `light` 只要求能回答
   Task Purpose 的直接结果、必要交接和判断本身必需的物理有效性；不默认增加独立
   收敛扫描、参数敏感性、重复 Run 或替代方法对照。`strict` 依主要判断加入
   相关的收敛、敏感性或对照检查，并满足用户或已接受 RQ 的明确要求，不套固定清单。
   把不改变科学含义且有确定依据的实现值留给
   `$calc-execute`；Spec 中的明确值具有约束力。缺少必要科学证据时保持未发布。
6. 替换时读取目标 Spec、全部 Task 和 Run 记录、物理 Run 目录及调度器事实。
   如仍有写入者，先经 `$calc-execute` 核实并按情况取消或等待，直至无写入风险。
   保留每个旧 Run 及其状态和产物；已有 Run 的 Task 身份须保持可追溯，若新设计
   无法容纳旧任务与 Run 记录，就另建后续 Spec。新设计使已接受证据失效时，清除相应
   `Current` 选择，将受影响 Task 恢复为 `pending`；已接受的下游 Task 按依赖变化
   置为 `needs-review`，未提交的 prepared 快照重建并重评。变更科学含义的
   下一次执行使用新 Run。替换只修改当前 Spec 设计及必要状态，不覆盖物理 Run。
7. 写入前重读 RQ、目标 Spec、现有索引和替换所需的权威证据，检查 RQ 归属、
   ID 和路径唯一、设计完整、现有目标未被其他所有者占用、替换安全。冲突先调和；
   不能安全调和则停止。新建时写入一份完整 Spec 及一条准确的 `RQ.md` Spec 索引；
   替换时更新同一 Spec。重新读取并核实写入结果；每次 Spec、Task 或 Run 状态或其他索引
   字段变化、新增对象时，立即按项目 `AGENTS.md` 直接维护所属 RQ 目录下的 `tracker.json`
   并核对一致性；遵循[进度跟踪表契约](../../resources/progress-tracker.md)。
   缺少项目约定时，规则补齐交由 `$calc-setup`。相同内容重试保持幂等，差异由
   当前权威资料重新评估，不依赖旧会话提案或批准缓存。
8. 报告发布或替换的 Spec、证据档位和本次研究前沿。若用户只要求设计或发布，
   到此结束。若用户已委托推进该 RQ 的计算，直接进入 `$calc-execute` 继续当前 Spec；
   每份 Spec 完成后，仅在已接受 RQ 和结果直接支持下一主要判断时继续发布下一份。
   达到 RQ 成功判据、无证据支持下一判断、关键科学缺口未解决或触及用户边界时停止。
   新 RQ 的发现与创建属于另一个待议问题，本流程不把它作为默认下一步。

## 权威边界

此 skill 拥有 Spec 的主要判断、科学承诺、任务 DAG、条件、验收和停止规则。
`$calc-execute` 拥有 execution-owned 选择、物理 Run 和执行事实。每份 Spec 是其
Task 与 Run 记录的唯一权威；本 skill 不改变 RQ 的问题、边界、成功判据或已接受决策。
