# 阶段 5 — 交付到插件本地知识

最终交付是开发工作树中插件本地知识目录的新增或更新卡片，而不是可安装 Skill。

1. 再次确认已按顺序读取 `../prl-shared/SKILL.md` 和 `plugins/paper-project/knowledge/cards/INDEX.md`；物理卡还须读取 `plugins/calc-project/knowledge/cards/physics/PHYSICS_INDEX.md`。
2. 先将 paper 候选写入 `plugins/paper-project/knowledge/candidates/cards/`；只有用户确认后才将通用卡晋升到 `plugins/paper-project/knowledge/cards/atoms/` 并同步 paper 索引。计算经验或模板只可进入 calc-project 的候选区；物理知识只交付提案，均不进入 calc 正式索引。
3. 通用卡运行 `../../prl-shared/scripts/validate_knowledge_repository.py ../../../knowledge`。向用户报告卡片名称、执行动作、type、tags、索引状态、验证结果、Git revision 和 dirty 状态；不得自动提交。
4. 不复制或 symlink 到 skills 目录，不生成 `test-prompts.json`，不接入 darwin-skill。
