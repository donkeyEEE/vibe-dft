# 计算项目结构

在已获批准的项目初始化或重组中使用本参考资料。

## 基础布局

```text
<project-root>/
├── CONTEXT.md
├── AGENTS.md
├── ARCHITECTURE.md
├── .gitignore
├── 01<main-line-slug>/
│   ├── 01-rqs/
│   ├── 02-计算规范/
│   ├── 03-计算笔记/
│   ├── 04-问题排查/
│   ├── 05-理论笔记/
│   ├── 06-文献笔记/
│   ├── 07-图表与阶段汇总/
│   └── 99-archive/
├── 02原始数据/
├── calculation_templates/
└── structures/
```

`01<main-line-slug>` 使用小写、连字符连接的研究线名称。数据根也可为
`02<slug>-原始数据/`。基础设置创建空的 `01-rqs/`、数据根、`calculation_templates/`、
`structures/` 和 `06-文献笔记/` 容器；它不填充计算模板或文献容器，后者内容由 Paper
Project 文献工作流负责。

`.gitignore` 包含 `/.calc-project/`。该隐藏目录仅按需保存进展报告，其中内容是可再生的
派生视图，不属于计算项目结构或进度权威。每个 RQ 的 `tracker.json` 与其 `RQ.md` 同级，
仅记录该 RQ 的进度；根忽略规则按共享契约排除各跟踪表。空项目初始化时不建表；
维护已有项目时，分别从各 RQ 与其已发布 Spec 建立或修复跟踪表，保留权威记录。

仅在请求配置集群时创建 `software-profiles.md`。基础设置不创建具体 RQ 目录、Spec、
任务、Run、计算输入或调度器脚本。已有 RQ 和 Spec 保持不变。

研究主线的 `04-问题排查/` 同时承载 `calc-issue` 管理的待探究问题记录；
Issue 使用项目内唯一编号，可跨主线关联 RQ、Spec、Task。首个 Issue 出现时按需创建，
具体记录及状态契约由 `$calc-issue` 所有；项目配置流程不创建具体 Issue。

## ARCHITECTURE.md 契约

记录目录职责、命名规则及 Git/集群数据边界。消费者读取下列精确章节和字段行，
不从文件名推断配置：

```markdown
## Calculation Configuration

Data root: 02原始数据/
Tracker adapter: local-markdown
RQ location: 01<main-line-slug>/01-rqs/<rq-id>-<slug>/
Software profile: software-profiles.md
```

在该文件配置前省略 `Software profile:`。`Data root:` 是选定的项目相对数据根路径。
RQ 存储配置沿用机器字段 `Tracker adapter:`，初始且唯一值为 `local-markdown`。`RQ location:` 是位置约定，
不是已创建的 RQ，也不是状态 schema。

## 生成的 AGENTS.md 契约

生成的文件应保持简洁，并指引 agent 查阅：

- 项目 `CONTEXT.md`，以了解术语和数据边界；
- 在定位 RQ、Spec、任务或 Run 前查阅 `ARCHITECTURE.md` 及其
  `## Calculation Configuration`；
- 在科学设计或执行工作前查阅选定的 `RQ.md`、选定 Spec，以及仅由该 Spec 引用的 Runs；
- Git/集群边界：文档、模板、结构、脚本和轻量结果可在本地追踪，而 HDF5、`CHGCAR`、
  `WAVECAR` 和大型计算输出保留在服务端。

生成的文件将项目操作规则保持在项目范围。Spec 是任务状态、DAG、Runs、current-Run
指定、执行进度和闭包的唯一权威。

初始化或维护项目时，按[进度跟踪表契约](../../../resources/progress-tracker.md)
将维护约定写入项目 `AGENTS.md`，保留其他项目规则；字段和重建要求以该共享契约为准。

## 项目文档

生成简洁的项目专用文档。`CONTEXT.md` 以[项目上下文](project-context.md)和已确认的
项目定义为基础。除非用户逐项批准拟议变更，否则保留已有 `CONTEXT.md`。`.gitignore`
排除编辑器/Python 缓存、HDF5、`CHGCAR`、`WAVECAR` 和其他已识别的大型计算输出。
