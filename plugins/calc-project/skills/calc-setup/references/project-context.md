# 计算项目管理

本上下文定义 Calc Project 组织科研计算的稳定语言。新项目以此为基线，项目可用已确认的项目语义调整定义。

## Language

**计算项目（Calculation Project）**:
围绕一个研究目标组织的计算工作整体，对应一个 `<project-root>/`。
_Avoid_: 项目目录，计算仓库

**计算项目结构（Calculation Project Structure）**:
由稳定知识、RQ Tracker 配置和数据根组成的项目级管理结构。
_Avoid_: 任务状态，Spec DAG

**计算笔记（Calculation Notes）**:
按研究主线沉淀计算规范、结果解释、问题排查和理论知识的稳定记录。
_Avoid_: RQ，Spec，Run 日志

**计算笔记结构（Calculation Notes Structure）**:
一条研究主线中按知识职责组织计算笔记的层级；`01-rqs/` 是同一主线下并列的
RQ 存储入口，不是计算笔记类别。
_Avoid_: 数据根，执行状态

**数据根（Data Root）**:
计算数据的项目级边界，对应 `02原始数据/` 或项目确认的
`02<slug>-原始数据/`。任务和 Run 路径由 Spec 引用，而非由数据根索引。
_Avoid_: Tracker，任务状态数据库

**计算线（Calculation Line）**:
数据根下按项目科研关系组织计算目录的层级；中间目录数量和含义由项目定义。
_Avoid_: RQ 主线，固定三层路径

**工作流（Workflow）**:
为一个跨阶段计算目的描述的阶段、依赖和验收关系。需要持久化时，这些关系由
Spec 的任务 DAG 表达，而不是由并行状态文档拥有。
_Avoid_: 计算线，状态文件

**RQ Tracker**:
一个 RQ 的配置化存储约定。`local-markdown` adapter 将其存储在
`01<main-line-slug>/01-rqs/<rq-id>-<slug>/`，其中包含 `RQ.md`、已明确发布的
Specs 和 Decision Tickets。Tracker 不是独立状态文档，也不拥有执行进度。
_Avoid_: Tracker 数据库，进度缓存，会话注册表

**研究问题（Research Question, RQ）**:
在一条研究主线内定义问题、边界、成功标准、已接受决策及已明确发布 Spec 的记录。
_Avoid_: 研究计划目录，任务列表

**Decision Ticket**:
RQ 决策过程中为一个未解决问题建立的临时记录；答案被接受并写入 RQ 后即完成。
_Avoid_: 计算任务，长期进度记录

**计算规范（Spec）**:
一个主判断的当前已批准科学设计，也是其任务目的、DAG、状态、Runs、current Run、
执行记录和闭包的唯一权威。Spec 不维护修订历史。
_Avoid_: Tracker 状态，工作流状态文件

**计算任务（Calculation Task）**:
Spec 中为支持主判断声明的可执行工作。身份、目的、依赖、条件、验收和状态由父 Spec
拥有；数据目录仅保存计算文件和最小同步配置。
_Avoid_: 独立任务元数据，目录 README 权威

**运行（Run）**:
一个任务的一次执行尝试。每个 Run 在自己的 `inputs/` 中记录实际采用的科学承诺和
执行参数，并有 `outputs/` 和 `logs/`。尚未形成需保留科学证据的当前 Run 可按明确授权
原地纠正；已接受、需比较或来源不确定的执行使用独立 Run。
_Avoid_: 计算任务，覆盖目录

**Run 输入（Run Inputs）**:
位于 `TASK-…/RUN-…/inputs/` 的实际执行输入，包含 `run.sh`、`run.pbs`、科学输入和
由执行阶段确定的参数；每次验证和评审针对当时完整内容的精确快照。
_Avoid_: 任务级 inputs，计算模板

**执行参数（Execution-owned Parameter）**:
Spec 未明确固定、且不改变科学问题、结果含义或可比性的实现选择。`calc-execute` 只能
依据已加载 backend 规则、软件 profile 或上游事实确定，并在 Run 输入和证据中记录。
_Avoid_: 科学承诺，Spec 覆盖

**最小同步配置（Minimal Sync Configuration）**:
任务目录中的 `calc-sync.yaml`，只配置 `local`、`server` 和 `exclude`；它是工具配置，
不是领域状态。
_Avoid_: task metadata，生命周期记录

**计算模板（Calculation Template）**:
生成 Run 输入的可复用来源资产；模板本身不是参数权威或已审核输入快照。
_Avoid_: Run 输入，Spec 科学设计

**项目计算模板（Project Calculation Template）**:
特定项目维护并确认的输入或脚本基线，位于 `calculation_templates/`。
_Avoid_: 插件计算模板，Run 输入

**插件计算模板（Plugin Calculation Template）**:
随插件发布并由明确技能路径消费的计算基线。
_Avoid_: 项目计算模板，运行时资源发现

**计算工具脚本（Calculation Utility Script）**:
辅助计算的可执行资产，不是生成科学输入的参数来源。
_Avoid_: 计算模板，任务专用脚本

**本地副本（Local Copy）**:
计算数据在本地工作环境中的受管位置。
_Avoid_: 主数据，本地任务

**远程副本（Remote Copy）**:
计算数据在计算集群中的受管位置；HDF5、`CHGCAR`、`WAVECAR` 和大输出保留于此。
_Avoid_: 主数据，远程任务

## Scoped IDs and references

ID 在父对象内编号且不复用：`RQ-NNN` 属于一条主线，`DT-NNN` 和 `SPEC-NNN`
属于一个 RQ，`TASK-NNN` 属于一个 Spec，`RUN-NNN` 属于一个任务。同父引用使用 ID，
跨层引用使用相对路径；目录名可在 ID 后附加 slug。
