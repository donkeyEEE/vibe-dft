# 阶段 5 — 交付到 ATOM CARD 共享库

最终交付是外部 `research-knowledge` 的新增或更新卡片，而不是可安装 Skill。

1. 再次确认已按顺序读取 `../prl-shared/SKILL.md` 和 `/home/donk/plugins/research-knowledge/cards/INDEX.md`；物理卡还须读取 `/home/donk/plugins/research-knowledge/cards/physics/PHYSICS_INDEX.md`。
2. 先将候选写入 `/home/donk/plugins/research-knowledge/candidates/cards/`；只有用户确认后才将通用卡晋升到 `/home/donk/plugins/research-knowledge/cards/atoms/`，将物理卡晋升到对应类别，并同步更新相应索引。
3. 运行 `../../prl-shared/scripts/validate_knowledge_repository.py /home/donk/plugins/research-knowledge`，向用户报告卡片名称、执行动作、type、tags、索引状态、验证结果、Git revision 和 dirty 状态；不得自动提交。通用卡另报告所服务的现有 skill。
4. 不复制或 symlink 到 skills 目录，不生成 `test-prompts.json`，不接入 darwin-skill。
