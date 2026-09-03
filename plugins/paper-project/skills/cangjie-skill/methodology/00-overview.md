# RIA-TV++ 到 ATOM CARD 的蒸馏方法

本流程保留 RIA-TV++ 的核心：先理解来源、从多视角提取、三重验证、保留案例和边界；但交付物不再是可执行 Skill，而是共享库中的 ATOM CARD。

## 输入与输出

输入是可访问来源及用户说明的知识意图。候选先进入 `/home/donk/plugins/research-knowledge/candidates/cards/`；用户确认后，通用卡晋升到 `/home/donk/plugins/research-knowledge/cards/atoms/` 并更新
`/home/donk/plugins/research-knowledge/cards/INDEX.md`；物理卡按三类写入物理子库并更新
`/home/donk/plugins/research-knowledge/cards/physics/PHYSICS_INDEX.md`。物理卡的新增与演化另见
[08-physics-card-evolution.md](08-physics-card-evolution.md)。

## 不变量

1. **原子性**：一张卡只表达一个概念、机制、约束、步骤、证据或写作规则。
2. **可解释**：正文第一段用自己的话直接陈述原子知识。
3. **可核查**：通用候选检查证据、迁移性和非平庸性；物理候选检查来源支持、知识价值、原子性和一致性。
4. **共同决定**：AI 提议 `type` 与 tags，人类确认最终意图和类型。
5. **库优先**：每次读写共享知识前都先读 `prl-shared/SKILL.md` 和 `references/knowledge-source.yaml`，再读外部正式索引；物理请求继续读物理索引。
