---
name: calc-review
description: 将一个精确的 prepared Calc Project Run 作为瞬时、只读的提交前门禁进行评审。
---

# Calc Review

判定一个精确的 prepared Run。输入必须唯一解析到其 task、当前 Spec、完整 `inputs/` 快照、
指定的上游 handoff、预期提交环境和资源配置。直接读取这些权威资料，并在决定是否需要用户前，
通过安全的只读检查补足缺失的操作细节。

## 评审

1. 建立足以识别 Run、task、Spec、受评字节、handoff、目标环境、资源和预期产品的可复现证据。
   针对当前风险选择最清晰的证据形式；不要求固定报告 schema。评审应保持瞬时性，不写入评审缓存
   或授权标记。
2. 阅读[提交前检查](references/pre-submit.md)和 [PBS 检查](references/pbs.md)。仅加载
   prepared task 所需的 backend 检查：

   - VASP：[VASP](references/backends/vasp.md)；磁性 task 另加[磁有序]
     (references/backends/vasp-magnetic.md)。
   - DFT+DMFT：[DMFT](references/backends/dmft.md)。
   - Hefei-NAMD 或 NAMDwithSOC：[NAMD](references/backends/namd.md)。
   - Wannier90：[Wannier90](references/backends/wannier90.md)。
   - TB2J：[TB2J](references/backends/tb2j.md)。
   - VAMPIRE：[VAMPIRE](references/backends/vampire.md)。

   仅执行检查；评审步骤本身不进行准备、修复、传输、提交、取消或领域写入。
3. 快照忠实且安全地实现其 task 时返回 `pass`；每项观察都仅为信息性且提交前无需行动或选择时，
   返回 `pass_with_warnings`。对于任何可修复缺陷，说明证据和未完成行动，再将控制权交回活跃执行流。
   该执行流诊断并修复缺陷、选择安全且合格的 Run，并在提交前重新验证和评审。

## 停止条件

仅当继续操作需要下列事项之一时停止并询问用户：

- 已批准权威资料无法确定的新科学判断，包括变更的结构、磁序、科学参数、方法、携带 provenance
  的来源、验收准则或停止准则；
- 提交、扩大资源或成本、同步、取消、覆盖、删除，或当前授权范围外其他外部副作用所需的新外部授权；
- 等待、新建 Run 或其他非破坏性路径均无法安全推进时，对并发写入者的处理；或
- 安全检查无法在当前 Spec、task、Run 和指定来源中唯一识别或调和的权威对象。

尊重用户明确要求的暂停。否则沿适当的执行、配置或安全诊断路径自动继续。缺少固定格式报告、
可修复的快照缺陷、过时配置或等效技术实现之间的选择，都不是询问用户的理由。选择能够保持
已批准科学含义、风险最低、改动最小且最容易直接验证的实现。

## 瞬时边界

该判断仅适用于当前执行链中的精确快照和环境。任何输入、提交脚本、资源、handoff、目标环境或
权威 task 的变更都需要再次评审。用户直接调用仅用于诊断，不能授权未来提交。新会话中发现的
未提交 prepared Run 必须重新评审。此 skill 不授予提交授权，也不进行闭包前评审。
