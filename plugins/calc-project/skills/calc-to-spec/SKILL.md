---
name: calc-to-spec
description: 为一个已接受 RQ 设计并发布完整的计算 Spec 集合，或替换一个既有 Spec。
---

# Calc to Spec

负责一个 RQ 的完整新 Spec 集合，或一个待替换既有 Spec 的科学设计。新 Spec 输入恰为
一个已接受 RQ 及完整预期答复范围；替换输入恰为一个既有 Spec。输出是批准前的一份简洁
发布提案，以及仅在明确批准后生成的完整拟议集合及其汇总 RQ 索引变更。此 skill 声明任务；
它不创建任务目录或 Run，也不执行计算或提交。

## 流程

1. 解析唯一计算项目，再读取其 `ARCHITECTURE.md` 中的
   `## Calculation Configuration`。解析 `Data root:`、`Tracker adapter:`
   和 `RQ location:`；要求 adapter 为 `local-markdown`。配置命名 `Software profile:`
   时，将该精确档案作为项目能力记录读取。解析唯一 RQ，并读取其 `RQ.md`、相关已接受
   Decisions、关联证据及相关已发布 Specs。替换时，通过该 RQ 解析既有 Spec，不能将其
   局部范围的 `SPEC-NNN` 视作全局唯一。权威含糊或缺失时停止。
2. 仅加载拟议任务需要的精确科学设计参考资料：

   - VASP 物理承诺：[VASP 设计](references/backends/vasp.md)。
   - 方向性 SOC-MAE（连同 VASP 设计）：[VASP MAE 设计](references/backends/vasp-mae.md)。
   - DFT+DMFT：[DMFT 设计](references/backends/dmft.md)。
   - Hefei-NAMD/NAMDwithSOC：[NAMD 设计](references/backends/namd.md)。
   - VASP → Wannier90 → TB2J → VAMPIRE：[磁性设计](references/backends/magnetic.md)，
     以及该阶段需要科学承诺时上列 VASP 或 Wannier 参考资料。
   - 交换参数能量映射：[能量映射设计](references/backends/energy-mapping.md)。
   - 自旋分辨 Wannier 窗口：[Wannier90 设计](references/backends/wannier90.md)。
   将模板视为实现基线，绝不作为科学数值的证据。所需参考资料、项目能力或证据来源不可用时，
   停止，而非在运行时发现替代 backend 资源。
3. 起草前，在当前对话中调用 `$dev-engineering:grill-with-docs` 形成科学设计。将访谈
   产出的 Spec 范围术语和框架记录在每份受影响 Spec 的最终 `## Context`；仓库根
   `CONTEXT.md` 只保留稳定的全项目领域术语。在新 Spec 模式中，先确定回答已接受 RQ
   所需的完整、相互独立的主要判断集合，再起草任一成员。将真正未解决的 RQ 级问题交回
   `$calc-rq`；其被接受解决后，从权威 RQ 恢复完整集合设计。访谈依赖不可用时，暂停并报告。
4. 用 [Spec 模板](references/spec-template.md)起草 Spec 集合，每个成员使用一次，且在发布前
   对所有成员保持完整 Spec 草案为内部内容。每个独立主要判断对应一个 Spec，一个判断只在
   一个 Spec 内。包含回答该判断所需的任务、依赖、条件、验收准则和停止规则。`SPEC-NNN`
   仅在解析出的 RQ 内分配，`TASK-NNN` 仅在该 Spec 内，`RUN-NNN` 仅在其任务内。依赖只命名
   同一 Spec 的任务且构成无环图。条件只使用已记录的上游结果。将验收表述为任务 Purpose
   已得到回答所需的最低充分证据。把 execution-owned 选择留给 `$calc-execute`：环境和
   可执行文件路径、启动与并行机制、日志和重启控制，以及具有确定性 backend、software-profile
   或上游证据默认值且不改变科学含义的辅助参数。明确 Spec 值具有约束力。将稳定项目能力或
   配置缺口交回 `$calc-setup`。
5. 替换时，读取当前 Spec、每个已记录任务和 Run、引用的物理 Run 目录及当前调度器状态。
   已结束 Spec 不可变。可能被失效或造成不一致的活跃执行阻止替换。提案保留所有物理 Run
   目录，只覆盖当前 Spec 设计；不创建过时设计历史或修订计数器。
6. 对每个拟议成员只展示目标路径、设计摘要和精确 `RQ.md` 索引变更。新 Spec 模式中，
   将所有成员及精确汇总索引变更合并为一份完整集合提案。替换模式还应确认保留物理 Run
   目录。对展示的提案取得一次明确批准；批准不要求展示任一成员的完整 Markdown。沉默、
   历史偏好和一般性委托均不满足批准门槛。目标、科学设计、索引条目或所述替换效果的任意
   变化都会使批准失效。
7. 写入前立即重新读取 `RQ.md`、每个目标 Spec 以及用于替换的全部权威资料。预检整个已批准
   集合：要求 RQ 所有权匹配、新 Spec 目标未使用或字节完全相同、设计完整、ID 与链接唯一，
   并在适用时可安全替换。发生任一冲突即在写入前停止，而非修复另一所有者的权威资料。否则
   写入每个已批准 Spec 和精确汇总 RQ 索引变更，再重新读取所有成员及 `RQ.md` 予以确认。
   中断写入通过重读整个批准集合调和；发布相同成员和链接是幂等的，任何差异都需要新提案和批准。
8. 报告每个已发布成员或被替换的 Spec。仅在新完整 Spec 集合的每个成员及其汇总 RQ 索引变更
   都确认后，若仍有执行意图则直接进入 `$calc-execute`；绝不可只在集合前缀后交接。安全替换的
   活跃 Spec 可照常继续。携带已解析身份、路径、已批准内容和剩余意图。交接不增加提交或其他
   外部操作授权；`$calc-execute` 应用自身门槛。

## 权威边界

此 skill 拥有每份 Spec 中当前主要判断、科学承诺、任务 DAG、任务声明、条件、验收规则和
停止规则。`$calc-execute` 拥有 Spec 省略的 execution-owned 选择，并在 Run 输入和证据中
记录其实现值；它不能覆盖明确的 Spec 值。每份 Spec 是其任务与 Run 记录的唯一权威。此 skill
不实体化这些声明、不更改物理 Run 数据、不持久化完整集合状态或另一并行工作流记录，也不正式更新
RQ 结论。
