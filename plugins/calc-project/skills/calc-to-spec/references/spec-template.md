```markdown
# <Spec title>

ID: SPEC-001
Status: ready
RQ: ../RQ.md

## 判断

## 任务

### TASK-001: <title>

Status: pending
Path: <data-root-relative-task-path>
Blocked by:
Condition: always

Purpose: <本任务要回答什么，以及答案如何影响研究>

Acceptance: <什么证据足以完成该任务>

#### 运行（Run）

| Run | Status | Current | Path | Result |
|---|---|---|---|---|
| RUN-001 | prepared | no | <task-relative-run-path> | — |

## 上下文
```

`Context` 是最后一节。它记录解释判断、Task、条件、验收规则、Run 以及（如存在）
Closure 所需的 Spec 范围内术语和框架。

Spec 状态为 `ready | active | concluded`。Task 状态为 `pending | completed
| failed | needs-review`。Run 状态为 `prepared | submitted | finished | failed |
cancelled`；`submitted` 包含排队和执行。`Current` 为 `yes | no`，每个 Task 至多有
一个 current Run。

`Result` 是可扫描的执行摘要。适用时最好按“结果 → 失败原因 → 与上一 Run 的区别 → 推进”
组织，只保留简短结论。保留程序原生结果值并可引用证据路径，但不粘贴原始日志、排障过程或
详细诊断；这些内容留在 Run 日志或问题排查记录中。

Task 路径相对于已配置的数据根目录；Run 路径相对于其 Task。`Blocked by` 仅列出此
Spec 内的 `TASK-NNN` ID，且图必须无环。`Condition` 为 `always`，或一条基于已记录
上游结果的自然语言句子。在其依赖和条件允许前，Task 保持 pending。条件被明确判定为假或
Task 被取消时，该 Task 的状态为 `failed`；不明确之处回到 Spec 设计。

`判断` 节说明本 Spec 的连贯研究目标，可以包含相关的探索与判断。
研究推理由 `$domain-research` 指导，记录方法条件、影响研究判断的选择和必要比较约束。
未写入 Spec 的普通数值参数由执行负责，依据当前用途、适用计算规范和已有证据选择，记录在
Run inputs 中；选择可能改变研究判断或依据不足时返回设计。Spec 中的显式值具有约束力。

`Purpose` 说明本任务要回答什么，以及答案如何影响研究；实现步骤说明其支持的科学用途。
`Acceptance` 说明什么证据足以完成该任务。方法、参数和模型假设写在上下文中，精度与
不确定性只在需要时补充。探索任务可通过取得指定观察、工件、诊断或比较完成；完成不要求
得到有利的科学结果，也不等于机制已被证实。验证投入、定量阈值及停止规则由
`$domain-research` 根据研究目的和用户具体要求指导，实际采用的要求记录于 Spec。
concluded Spec 在同一文件中加入以下一节：

```markdown
## 闭合（Closure）

Judgment: <final judgment>
Evidence: <accepted tasks and Runs>
RQ impact: <proposed RQ update>
```

将 `Closure` 紧接在 `Context` 前插入，使 `Context` 仍为最后一节。`RQ impact`
在 `calc-rq` 更新 RQ 前始终只是提案。
