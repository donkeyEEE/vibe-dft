```markdown
# <RQ title>

ID: RQ-001
Status: active
Evidence level: <light|strict> (optional)
Spec design mode: <automatic|collaborative> (optional)

## 问题

Boundary: <scope, applicable conditions, and exclusions>

## 成功判据
## 规范（Spec）

- [SPEC-001: <title>](specs/SPEC-001-<slug>.md)

## 决策
## 上下文
```

RQ 状态为 `active | concluded`。`Spec` 仅包含每份已明确发布 Spec 的 ID、标题和
相对链接。`Decisions` 包含已接受的 RQ 决策。`Boundary` 是 `问题` 下的必填字段。
`Evidence level:` 是可选的 RQ 证据档位，取值为 `light | strict`；缺失时默认为
`light`。未设置时从实际 `RQ.md` 中省略模板行。Spec 发布时解析并固定其生效档位，
RQ 后续改变不自动改写已发布 Spec。
`Spec design mode:` 是该 RQ 的工作流偏好，取值为 `automatic | collaborative`；
未设置时默认 `automatic`，但首次进入 Spec 设计前仍须让用户选择并记录。
未选择时从实际 `RQ.md` 中省略模板行。模式切换只影响后续新建或替换，
不改变已发布 Spec、已接受决策或 Run 证据。
`Context` 记录解释问题、Boundary、成功判据、决策和 Spec 所需的 RQ 范围内术语和框架。
