# 计算项目管理

本上下文定义 Calc Project 组织科研计算的稳定语言。新项目以此为基线，项目可用已确认的项目语义调整定义。

## Language

**计算项目（Calculation Project）**:
围绕一个研究目标组织的计算工作整体，对应一个 `<project-root>/`。
_Avoid_: 项目目录，计算仓库

**计算项目结构（Calculation Project Structure）**:
由稳定知识、RQ 存储配置和数据根组成的项目级管理结构。
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

**RQ 存储配置**:
一个 RQ 的配置化存储约定。`local-markdown` adapter 将其存储在
`01<main-line-slug>/01-rqs/<rq-id>-<slug>/`，其中包含 `RQ.md`、已明确发布的
Specs。RQ 存储配置不是独立状态文档，也不拥有执行进度。
_Avoid_: Tracker 数据库，进度缓存，会话注册表

**研究问题（Research Question, RQ）**:
在一条研究主线内定义问题、边界、成功标准、已接受决策及已明确发布 Spec 的记录。
_Avoid_: 研究计划目录，任务列表

**进度跟踪表（Progress Tracker）**:
每个 RQ 目录下 `tracker.json` 中由智能体直接维护的该 RQ、Spec、Task、Run 派生摘要。
任一对象状态变化后立即同步所属 RQ 的表；项目 COT 汇总各表，缺失或异常时按 RQ 修复。
维护契约写在项目 `AGENTS.md`。索引可重建，不拥有科学设计或执行状态的权威。

**待探究问题（Issue）**:
计算执行中产生的、值得后续独立探究的问题对象，以问题语义跨 RQ、Spec、Task 连接计算与证据。
Issue 是执行的附加产物，可通过调研产出新 RQ 或经验；生命周期为待探究、探究中、已完成。
_Avoid_: 执行故障工单，Task，RQ 子对象

**经验（Experience）**:
探究中形成的、对以后工作有帮助的认识或做法，包含来源、适用范围和验证情况。
_Avoid_: 未标明依据的通用结论

**计算规范（Spec）**:
一个主判断的当前已发布科学设计，也是其任务目的、DAG、状态、Runs、current Run、
执行记录和闭包的唯一权威。Spec 不维护修订历史。
_Avoid_: Tracker 状态，工作流状态文件

**证据档位（Evidence Level）**:
RQ 或 Spec 对验收与可比性检查采用的 `light | strict` 设置。Spec 的明确设置优先，
否则在发布时继承 RQ；两者均缺失时为 `light`。`light` 要求足以回答 Task Purpose
的直接结果和必要交接，不默认增加独立收敛扫描、参数敏感性、重复 Run 或替代方法对照；
判断本身必需的检查始终保留。`strict` 增加与主要判断相关的增强检查，并遵循
用户或已接受 RQ 的明确要求。
_Avoid_: Run 状态，执行批准

**计算任务（Calculation Task）**:
Spec 中为支持主判断声明的可执行工作。身份、目的、依赖、条件、验收和状态由父 Spec
拥有；状态为 `pending`、`completed`、`failed` 或 `needs-review`。数据目录仅保存计算文件和最小同步配置。
_Avoid_: 独立任务元数据，目录 README 权威

**运行（Run）**:
一个任务的一次执行尝试。每个 Run 在自己的 `inputs/` 中记录实际采用的科学承诺和
执行参数，并有 `outputs/` 和 `logs/`。尚未形成需保留科学证据的当前 Run 可在选定
Spec 的执行范围内原地纠正；已接受、需比较或来源不确定的执行使用独立 Run。
_Avoid_: 计算任务，覆盖目录

**计算归属树（Calculation Ownership Tree, COT）**:
以 `RQ → Spec → Task → Run` 表示计算记录归属关系的完整层级视图。Task 间依赖属于
父 Spec 的任务 DAG，不是 COT 的父子边。
_Avoid_: 任务 DAG，执行状态注册表

**进展报告（Progress Report）**:
从当时的 RQ、Spec、Task 与 Run 权威记录生成的可再生详细视图，也称 COT Report。
报告不拥有计算事实或进度状态，删除后可从权威记录重新生成。
_Avoid_: COT 状态，进度快照权威

**计算汇报（Calculation Report）**:
围绕一个汇报主题，从一个或多个 RQ、Spec、Run 及经确认的补充来源综合计算证据的派生汇报。
阶段汇报说明当前科学证据、缺口与阶段认识；结果汇报依据已有证据回答主题下的研究问题。
计算汇报不拥有 RQ、Spec、Task 或 Run 的权威状态。
_Avoid_: COT 进展报告，权威结论记录

**汇报源数据（Report Source Data）**:
计算汇报实际消费的轻量数据副本或提取结果，并记录其权威来源与提取方式。大型计算输出仍留在
Run 或数据根，不因制作汇报而复制为汇报源数据。
_Avoid_: 权威原始数据，完整 Run 副本

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

ID 在父对象内编号且不复用：`RQ-NNN` 属于一条主线，`SPEC-NNN` 属于一个 RQ，
`TASK-NNN` 属于一个 Spec，`RUN-NNN` 属于一个任务。同父引用使用 ID，
跨层引用使用相对路径；目录名可在 ID 后附加 slug。
Issue 使用项目内唯一的 ISSUE-NNN，关联带完整归属的对象，不增加 COT 层级。
