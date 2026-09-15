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
2. 在用户声明的工作、并发和提交范围内选择一个彼此独立的可运行 Task。首个 Task 开始时，将 ready
   Spec 置为 `active`。按照分类状态继续选定 Task 的已记录 Run；只有不存在需要推进的已记录 Run
   时才创建新 Run。对于异常 Task，使用[计算排障](references/calculation-troubleshooting.md)定位问题；
   它把已直接确定的执行错误路由到[简单纠错](references/simple-correction.md)，随后选择合格的
   current Run 修复，或仅在方案选定后创建新 Run。无异常的 Task 则创建新 Run。
3. 阅读 [Run 准备](references/run-preparation.md)，结合 [PBS 执行](references/pbs.md)和适用的
   backend 参考资料准备选定 Run。若稳定项目配置必须变更，先加载 `$calc-setup` 并通过该工作流修改。
   未解决的软件用法视为异常 Task，并回到计算排障；该分支负责所有 `$dev-engineering:research` 调用。
4. 验证 prepared Run，并针对 prepared 快照调用 `$calc-review`。解决执行发现，必要时重新评审。
   仅当评审通过且提交处于用户当前授权范围内时提交。
5. 提交后记录调度器响应，并将 Spec 的 Run 行更新为 `submitted`。阅读[远程完成]
   (references/remote-completion.md)；仅在明确请求提交后监控或继续执行时启动 Calculation Monitor。
   传输文件时使用[预览式同步](references/sync.md)。根据实际情况和下列定义选择 Run 状态。
6. 验收 Task、变更其 current Run、传播失效或关闭 Spec 时，阅读[任务推进]
   (references/task-advancement.md)。应用 Spec 中该 Task 已批准的 Acceptance，再继续下一个可用任务。
   Spec 完成时提出闭包，并在用户接受后结束它。若随后必须变更 RQ，调用 `$calc-rq` 并向用户展示提案。
   交还控制前，以已解析的项目根和本执行步骤处理的 Task、Run 调用 `$show-cot`。展示完整项目总览，
   使答复明确执行结束所在的 Task。

## 原则

- 提交、同步、取消、增加资源或成本、删除，以及当前工作范围以外的覆盖都需要用户授权。
- Run 正常结束且产生可供任务验收的结果时为 `finished`；未成功结束且没有完整可验收结果时为
  `failed`；执行已实际取消且不会继续运行或写入结果时为 `cancelled`。
- 科学定义或 provenance 的变更使用新 Run。若同时需要变更 Spec，调用 `$calc-to-spec` 生成修改提案，
  询问用户是否接受，并仅在接受后继续。
