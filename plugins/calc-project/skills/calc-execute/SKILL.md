---
name: calc-execute
description: 执行一个选定的 ready 或 active Calc Project Spec，完成其 Runs 的准备、评审、提交、跟踪、同步与验收。
---

# Calc Execute

将一个选定的 ready 或 active Calc Project Spec 推进完成整条执行生命周期，涵盖任务推进、
Run 执行、任务验收和 Spec 闭包。

## 工作流

1. 解析执行前沿。读取选定 Spec、每个已声明 Task 与已记录 Run，以及本次调用相关的调度器、
   远程、日志和输出证据。要求 `Status: ready | active`、同一 Spec 内唯一的 Task 引用、无环依赖图、
   合法的 Task 与 Run 状态、可解析路径，且每个 Task 至多有一个 current Run。权威资料格式错误、
   相互冲突或不足以调和时停止并报告，不得擅自修复或猜测。
   仅依据实际证据调和 Spec；`submitted` 同时涵盖排队和运行中的工作，没有关联完成证据时，作业从
   调度器消失不等于 `finished`。根据依赖与 `Condition` 推导所有可运行 Task：所有 blocker 均为
   completed，且条件为 `always` 或已确定为真时，pending Task 才可运行；确定为假的条件标记为
   `failed`；含糊条件交回 `$calc-to-spec`；依据当前证据将 `needs-review` Task 保留在执行前沿。
   对已有 Run 的 Task 按该 Run 的实际状态分类：`submitted` Run 进入观察或监控，`prepared` Run
   进入验证和评审，`finished` Run 进入验收，`failed` Run 进入排障，不得直接另行分配 Run。
   持久化每项确定的状态变更，但本步骤不创建 Run，也不提交作业。
2. 在选定 Spec 的执行目标和用户明确约束内选择一个彼此独立的可运行 Task。首个 Task 开始时，将 ready
   Spec 置为 `active`。按照分类状态继续选定 Task 的已记录 Run；只有不存在需要推进的已记录 Run
   时才创建新 Run。对于异常 Task，使用[计算排障](references/calculation-troubleshooting.md)定位问题；
   它把已直接确定的执行错误路由到[简单纠错](references/simple-correction.md)，随后选择合格的
   current Run 修复，或仅在方案选定后创建新 Run。无异常的 Task 则创建新 Run。
3. 阅读 [Run 准备](references/run-preparation.md)，结合 [PBS 执行](references/pbs.md)和适用的
   backend 参考资料准备选定 Run。若稳定项目配置必须变更，先加载 `$calc-setup` 并通过该工作流修改。
   未解决的软件用法视为异常 Task，并回到计算排障；该分支负责所有 `$dev-engineering:research` 调用。
4. 验证 prepared Run，并针对 prepared 快照调用 `$calc-review`。解决执行发现，必要时重新评审。
   评审通过且复核后的输入仍是同一快照时，自主提交；遵守用户明确给出的提交、并发或资源边界。
5. 提交后记录调度器响应，并将 Spec 的 Run 行更新为 `submitted`。阅读[远程完成]
   (references/remote-completion.md)；需要等待异步作业并恢复本次执行时启动 Calculation Monitor。
   传输文件时使用[预览式同步](references/sync.md)。根据实际情况和下列定义选择 Run 状态。
6. 验收 Task、变更其 current Run、传播失效或关闭 Spec 时，阅读[任务推进]
   (references/task-advancement.md)。应用当前 Spec 中该 Task 的 Acceptance，再继续下一个可用任务。
   Spec 完成时核实闭包证据并自主结束它。若用户委托推进 RQ，且结果支持其边界内的
   下一主要判断，调用 `$calc-to-spec` 渐进发布并继续；达到 RQ 成功判据、没有有依据的
   下一判断、关键科学缺口未解决或触及用户边界时停止。RQ 本身需要变更时调用 `$calc-rq`。
   交还控制前，以已解析的项目根和本执行步骤处理的 Task、Run 调用 `$show-cot`。展示完整项目总览，
   使答复明确执行结束所在的 Task。

执行中出现有具体证据、有探究价值且超出当前 Task 正常分析与验收的发现时，
按需调用 `$calc-issue` 的记录入口，携带疑问、价值和来源，由它聚合既有问题或创建记录。
相关结果返回或新证据影响已有 Issue 时补充关联；记录后继续当前 Spec，汇报 Issue 编号。
这不是每次执行的必经步骤，不启动后续调研或新增计算；当前异常仍通过计算排障处理。

## 原则

- 每次写入 Spec、Task 或 Run 的状态变更后，立即按项目 `AGENTS.md` 直接维护
  所属 RQ 目录下的 `tracker.json` 并核对一致性，再继续执行或交接；新增对象、其他索引字段变化
  和 current Run 切换同样维护，不能推迟到执行结束。遵循
  [进度跟踪表契约](../../resources/progress-tracker.md)；缺少项目约定时，规则补齐交由 `$calc-setup`。
- 用户请求执行选定 Spec 后，按任务需要自主提交、同步、取消、调整资源或成本，以及处理执行产生的临时或失败产物；先核实目标、影响和可恢复性，记录实际动作。保留已接受的科学证据、其他 Run 和用户明确排除的对象。对用户明确限定的操作或预算遵守其边界。
- Run 正常结束且产生可供任务验收的结果时为 `finished`；未成功结束且没有完整可验收结果时为
  `failed`；执行已实际取消且不会继续运行或写入结果时为 `cancelled`。
- 科学定义或 provenance 的变更使用新 Run。若同时需要变更当前 Spec，调用
  `$calc-to-spec` 安全替换后继续；`concluded` Spec 的修改或重开仍需具体人工授权。
