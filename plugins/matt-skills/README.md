# Matt Skills

基于 [mattpocock/skills](https://github.com/mattpocock/skills) 选用并为 Codex 适配的个人插件，覆盖需求设计、工程交付与协作辅助。这里的流程可以按个人习惯持续改写，上游更新作为候选逐项吸收。

当前保留 22 个技能：12 个已发布、10 个停用且仅显式调用。个人精选已完成第一批五项，全部保留，其中 `grill-me` 与 `grill-with-docs` 恢复为已发布；第二批已删除三个技能，`research` 与 `prototype` 保留并维持已发布；其余批次继续确认，`ask-matt` 最后调整。

## 使用

插件加载后，统一使用 `$matt-skills:<skill-name>`，例如：

```text
$matt-skills:writing-for-agents 修改项目协作说明。
$matt-skills:code-review 审查当前分支相对 main 的变更。
$matt-skills:ask-matt 帮我选择适合当前任务的工作流程。
```

完整入口及功能见 [技能导航](skills/README.md)，当前状态事实源是 [skill-lifecycle.json](skill-lifecycle.json)。各技能的 `agents/openai.yaml` 调用策略与生命周期清单同步；停用入口仅允许用户显式调用。

## 来源与本地维护

- 上游：Matt Pocock 的 [skills 仓库](https://github.com/mattpocock/skills)。
- 初始导入：2026-08-11，revision `84fdeffd12f2ee307994d1eb6feb48173b6e0502`。
- 2026-09-02 曾从 `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` 选择性同步 `domain-modeling`、`wait-what` 和 `grilling`；这不代表全量追踪该 revision。
- Codex 适配：独立插件清单、直接位于 `skills/` 下的技能目录、`agents/openai.yaml` 调用策略，以及插件内统一的技能调用名称。
- 许可证：[MIT](LICENSE)，保留 Matt Pocock 的版权声明。

维护时先决定个人需求，再选择性吸收上游改进。技能取舍同时检查引用它的工作流，并遵守根目录 [CONTEXT.md](../../CONTEXT.md) 的生命周期规则。历史插件映射和本次迁移记录见 [迁移日志](../../docs/migrations/2026-09-04-plugin-consolidation.md)。
