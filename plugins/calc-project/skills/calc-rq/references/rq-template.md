```markdown
# <RQ title>

ID: RQ-001
Status: active

## 问题

Boundary: <scope, applicable conditions, and exclusions>

## 成功判据
## 规范（Spec）

- [SPEC-001: <title>](specs/SPEC-001-<slug>.md)

## 决策
```

RQ 状态为 `active | concluded`。`Spec` 仅包含每份已明确发布 Spec 的 ID、标题和
相对链接。`Decisions` 包含已接受的 RQ 决策。`Boundary` 是 `问题` 下的必填字段。
用户的具体验证要求写入成功判据或已接受决策。
RQ 范围内术语和框架由 `$domain-research` 维护在同目录的 `RQ-CONTEXT.md`。
RQ 上下文只收录本研究已确认的关键术语；项目与插件已有定义按需读取，不重复收录。
项目共用概念由 `$dev-engineering:domain-modeling` 维护在项目根 `CONTEXT.md`。
`RQ.md` 不设置 Context／上下文章节；问题、Boundary、成功判据和已接受决策仍保存在本文件。
