# 阶段 2 — 构造 ATOM CARD

写入前必须依次阅读 `../prl-shared/SKILL.md` 和 `/home/donk/plugins/research-knowledge/cards/INDEX.md`；物理候选继续阅读物理索引。

使用 `templates/ATOM_CARD.md.template`。卡片 frontmatter 只能使用：

```yaml
name: prefix-atomic-topic
type: approved-index-type
tags: [registered/tag]
updated_at: YYYY-MM-DD
```

物理概念、现象、理论与模型分别使用三个专用模板。所有卡片正文第一段必须是一个独立可理解的原子主张；不能把多个不同知识对象塞进同一张卡。来源摘录不超过满足说明目的的最小长度。
