---
name: calc-setup
description: 初始化、重组或维护一个计算项目的稳定结构、RQ配置、数据边界和可选集群软件配置。
---

# 计算项目配置

## 流程

1. 解析唯一项目路径，并在存在时读取其 `AGENTS.md`、`CONTEXT.md` 和 `ARCHITECTURE.md`。
   若目标有歧义，询问用户。
2. 初始化、重组或维护时，读取[项目结构](references/project-structure.md)和
   [项目上下文](../../resources/project-context.md)。提出准确路径与文档变更，包括
   `ARCHITECTURE.md` 的 `## Calculation Configuration` 字段。
   项目根 `CONTEXT.md` 的创建与概念维护交由 `$dev-engineering:domain-modeling`，
   纳入本次项目文档提案；本技能负责结构与配置。
3. 独立初始化或维护项目时，写入前取得该具体提案的批准。由 `$calc-execute` 为选定 Spec 的
   执行所需配置调用时，在用户明确约束内自主完成变更；保留计算数据，并在变更前比较既有
   项目文档。科学设计变更交由 `$calc-to-spec` 按本次设计模式处理；已闭合 Spec 的修改仍需具体授权。
4. 在本次授权范围内创建或更新稳定结构和配置，使根 `.gitignore` 包含 `/.calc-project/`。
   读取[字段契约](../../resources/progress-tracker.md)和
   [维护契约](../../resources/progress-tracker-maintenance.md)，按项目结构参考维护项目约定，
   为每个已有 RQ 创建或修复其 `tracker.json`；无 RQ 时不创建记录。
   存在旧 `.calc-project/tracker.json` 时读取[迁移步骤](references/progress-tracker-migration.md)。
   报告既有 RQ 与 Spec，保留其权威记录。
5. 请求集群配置时，读取[集群软件配置](references/cluster-software-profiles.md)。将已审查的
   项目特定值记录在 `software-profiles.md`；用随附验证器探测每个值，并保留如实的 `verified`
   或 `unavailable` 证据。
6. 确认 sibling skill 可读取全部四个计算配置字段，检查 `git status --short`，并报告变更和
   未解决配置。

## 权威范围

此 skill 拥有稳定项目结构、数据边界、RQ配置、生成的 Agent 指针和维护的
集群/软件配置。它不创建 RQ、Spec、Task 或 Run，不进行数据同步、作业提交或可变
Run 环境验证。

已配置项目可进入 `$calc-rq`。项目配置问题路由回此处；开放式工作流选择路由至 `$ask-lyz`。
