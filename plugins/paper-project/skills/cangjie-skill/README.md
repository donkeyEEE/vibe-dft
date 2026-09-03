# cangjie-skill

将可访问的论文、书籍、学位论文、技术报告、课堂笔记或博客等来源蒸馏为 `prl-shared` 共享库中的 ATOM CARD。

它不生成可安装 Skill，也不是摘要工具。它先理解来源、进行多视角候选提取和验证，再由 AI 提议、用户确认卡片的类型、tags 和写入动作。通用卡片写入 `/home/donk/yz-skills/research-knowledge/cards/atoms/`；物理卡片按概念、现象、理论与模型分类，并由独立物理索引导航。

每次读写共享库时，必须先读 `../prl-shared/SKILL.md`，再读 `INDEX.md`；处理物理卡时继续读取 `physics/PHYSICS_INDEX.md`。详情见 [SKILL.md](SKILL.md)。
