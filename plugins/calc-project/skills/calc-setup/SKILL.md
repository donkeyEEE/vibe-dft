---
name: calc-setup
description: 初始化、重组或维护一个计算项目的稳定结构、Tracker 配置、数据边界和可选集群软件配置。
---

# 计算项目配置

## 流程

1. 解析唯一项目路径，并在存在时读取其 `AGENTS.md`、`CONTEXT.md` 和 `ARCHITECTURE.md`。
   若目标有歧义，询问用户。
2. 初始化或重组时，读取[项目结构](references/project-structure.md)和
   [项目上下文](references/project-context.md)。提出准确路径与文档变更，包括
   `ARCHITECTURE.md` 的 `## Calculation Configuration` 字段。
3. 写入前取得该具体提案的批准。对未经批准的数据移动、替换或删除必须停止。保留计算数据，
   并在变更前比较既有项目文档。
4. 仅创建或更新已批准的稳定结构和配置。报告既有 RQ 与 Spec，但不得接管或修改它们。
5. 请求集群配置时，读取[集群软件配置](references/cluster-software-profiles.md)。将已审查的
   项目特定值记录在 `software-profiles.md`；用随附验证器探测每个值，并保留如实的 `verified`
   或 `unavailable` 证据。
6. 确认 sibling skill 可读取全部四个计算配置字段，检查 `git status --short`，并报告变更和
   未解决配置。

## 权威范围

此 skill 拥有稳定项目结构、数据边界、Tracker 存储配置、生成的 Agent 指针和维护的
集群/软件配置。它不创建 RQ、Spec、Task 或 Run，不进行数据同步、作业提交或可变
Run 环境验证。

已配置项目可进入 `$calc-rq`。项目配置问题路由回此处；开放式工作流选择路由至 `$ask-lyz`。
