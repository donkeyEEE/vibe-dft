```markdown
# <RQ title>

ID: RQ-001
Status: active
Evidence level: <light|strict> (optional)

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
`Context` 记录解释问题、Boundary、成功判据、决策和 Spec 所需的 RQ 范围内术语和框架。
