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

Purpose: <task purpose>

Acceptance: <acceptance condition>

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

Task 路径相对于已配置的数据根目录；Run 路径相对于其 Task。`Blocked by` 仅列出此
Spec 内的 `TASK-NNN` ID，且图必须无环。`Condition` 为 `always`，或一条基于已记录
上游结果的自然语言句子。在其依赖和条件允许前，Task 保持 pending。条件被明确判定为假或
Task 被取消时，该 Task 的状态为 `failed`；不明确之处回到 Spec 设计。

每份 Spec 有一个主要判断。记录决定科学问题、解释或可比性的参数。只有当
`$calc-execute` 具备确定性的后端、软件配置或上游证据依据，且该选择不改变科学含义时，
未写入 Spec 的参数才可由执行负责；Spec 中的显式值具有约束力。

`Acceptance` 说明 `Purpose` 已被回答所需的最小充分证据。它可以要求成功产出指定
工件或诊断，而不要求得到有利的科学结果。仅当 Task 的 Purpose 或主要判断依赖它们时，
才加入收敛、质量、比较或交接阈值。concluded Spec 在同一文件中加入以下一节：

```markdown
## 闭合（Closure）

Judgment: <final judgment>
Evidence: <accepted tasks and Runs>
RQ impact: <proposed RQ update>
```

将 `Closure` 紧接在 `Context` 前插入，使 `Context` 仍为最后一节。`RQ impact`
在 `calc-rq` 更新 RQ 前始终只是提案。
