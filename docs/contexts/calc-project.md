# Calc Project 开发上下文

`plugins/calc-project` 是可安装计算工作流插件。插件领域术语由 `plugins/calc-project/skills/calc-project-structure/references/project-context.md` 统一定义，本文件只提供开发入口，不维护第二份术语表。

计算模板的正式内容位于 `research-knowledge/templates/computation/`，候选经验卡位于 `research-knowledge/candidates/cards/calc-project/`。插件负责计算模板的语义和可执行验收；候选卡不能直接作为消费输入。

修改插件结构、计算任务模型、方法工作流、集群脚本或模板消费逻辑时，先读领域术语文件；涉及共享资源时继续读取 `docs/contexts/research-knowledge.md` 及对应正式索引。
