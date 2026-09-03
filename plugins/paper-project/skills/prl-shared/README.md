# `prl-shared` — 共享知识治理

`prl-shared` 是 paper-project 内部治理 skill，不再保存共享卡片正文。正式内容位于
`references/knowledge-source.yaml` 指向的
`/home/donk/yz-skills/research-knowledge`。

本 skill 维护卡片和模板的 schema、准入规则、索引规则与验证边界；Cangjie 是唯一受支持的
正式晋升流程。消费端直接读取外部仓库的 `CONSUMER_CONTRACT.md`、正式索引和最小相关资源集。
物理卡片由 `cards/physics/PHYSICS_INDEX.md` 导航。
