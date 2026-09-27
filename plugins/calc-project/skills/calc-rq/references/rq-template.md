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
```

RQ 状态为 `active | concluded`。`Spec` 仅包含每份已明确发布 Spec 的 ID、标题和
相对链接。`Decisions` 包含已接受的 RQ 决策。`Boundary` 是 `问题` 下的必填字段。
`Evidence level:` 是可选的 RQ 证据档位，取值为 `light | strict`；缺失时默认为
`light`。未设置时从实际 `RQ.md` 中省略模板行。Spec 发布时解析并固定其生效档位，
RQ 后续改变不自动改写已发布 Spec。
RQ 范围内术语和框架由 `$domain-research` 维护在同目录的 `RQ-CONTEXT.md`。
RQ 上下文首次创建时以[共享领域术语](../../../resources/project-context.md)为基础，再补充 RQ 专用概念。
项目共用概念由 `$dev-engineering:domain-modeling` 维护在项目根 `CONTEXT.md`。
`RQ.md` 不设置 Context／上下文章节；问题、Boundary、成功判据和已接受决策仍保存在本文件。
