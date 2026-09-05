# Calculation Project Structure

Use this reference only for an approved project initialization or reorganization.

## Base layout

```text
<project-root>/
├── CONTEXT.md
├── AGENTS.md
├── ARCHITECTURE.md
├── PROJECT_PLAN.md
├── .gitignore
├── 01<main-line-slug>/
│   ├── 01-研究计划/  02-计算规范/  03-计算笔记/  04-问题排查/
│   ├── 05-理论笔记/  06-文献笔记/  07-图表与阶段汇总/  99-archive/
├── 02原始数据/
├── calculation_templates/
├── structures/
└── <METHOD>-scripts/
```

`01<main-line-slug>` is a lowercase, hyphenated research-line name. The data
directory may instead be `02<slug>-原始数据`. Create `calculation_templates/`
empty; populate it only for an explicit later task. Create `software-profiles.md`
only when requested. Base initialization creates only the empty data-directory
container; `calc-task` owns its material, calculation-line, and run directories
and its running-note updates.

Create project-root `CONTEXT.md` from [the standard project context](project-context.md).
Before writing, ask whether the user wants to invoke `matt-skills:grill-me`
to align project-specific terms. Invoke it only after agreement. Insert confirmed
project terms by topic into the single `Language` section; they may directly
replace standard definitions without an override marker. If `CONTEXT.md` already
exists, preserve it unless the user confirms the proposed changes after review.

## Generated AGENTS.md contract

Keep a generated project `AGENTS.md` concise and organize it into exactly these
four sections.

### 1. 项目概览与交接

State the current research focus, the documents that must be read before changing
inputs, project operation rules, and the Git/cluster data boundary. Before every
input-preparation, upload, submission, or synchronization operation, read the
project `CONTEXT.md`, `<data-root>/NOTE-doing.md`, the task `calc-task.yaml`, and
the task README.
`NOTE-doing.md` is the navigation index for a later Codex conversation; it never
overrides `calc-task.yaml`。谨慎调用 Superpowers：每次调用 Superpowers 插件或技能前，先征询用户是否要调用；仅系统或开发者指令要求立即调用时例外。

### 2. 术语与概念

State that project terminology and concept relationships are defined by the
project-root `CONTEXT.md`. Require it to be read before changing project
structure, task boundaries, workflow relationships, or data responsibilities.
Do not duplicate the glossary in `AGENTS.md`.

### 3. 通用工作流

- **输入准备**: create confirmed task-local inputs, submission/PBS scripts, and
  environment scripts only in `inputs/`; method workflows own method settings and
  `script-management` owns reusable template sources.
- **上传**: use `calc-sync` to inspect when needed, review a push plan, and push
  only after confirmation; do not infer task status from the upload alone.
- **提交**: use an explicit `<run-tag>`; an existing run directory refuses by
  default, while reuse or overwrite requires explicit user selection. The user
  submits formal jobs by default.
- **同步**: use `calc-sync` to inspect, review a plan, and pull only after
  confirmation; do not infer completion solely from scheduler state.

### 4. 记录更新

After task creation, verified transfer, upload/submission preparation, or a
confirmed user submission, update the applicable Task Metadata
(`calc-task.yaml`), Task Summary (README), and Task Navigation Index
(`NOTE-doing.md`) from confirmed or verified evidence. Task Metadata remains the
authority for paths, lifecycle state, and indexed files.

Base initialization also creates `06-文献笔记/` only as an empty container. The
`paper-project` plugin's `zo2notes` skill owns that container's internal
structure and literature-note storage contract. `calc-project-structure` must
not pre-create or maintain its single-paper, topic-synthesis, evidence-matrix,
or Zotero-mapping contents.
If `paper-project:zo2notes` is unavailable, leave the container empty rather
than inferring an internal layout.

## Project data boundary

- Track documents, templates, scripts, structures, and lightweight figures in Git.
  Exclude HDF5 and large VASP/DMFT outputs; retain those on the cluster and record
  their paths and metadata locally.

## Project documents

Create concise, project-specific documents rather than copying generic templates.

| File | Required content |
|---|---|
| `CONTEXT.md` | Standard baseline plus confirmed project-specific terms, kept in one `Language` section. |
| `AGENTS.md` | Current research focus; documents to read before changing inputs; project operation and data boundaries. |
| `ARCHITECTURE.md` | Directory responsibilities, naming rules, and Git/cluster data boundary. |
| `PROJECT_PLAN.md` | Research objective, current priorities, materials, calculation lines, and how evidence becomes stable project knowledge. |
| `.gitignore` | Python/editor caches plus HDF5 and large calculation outputs. |

For a workflow that crosses calculation stages, copy the root-level
`WORKFLOW.md` template in [workflow-template.md](workflow-template.md). Keep it
as a concise, human-maintained handoff record; it is not machine-parsed task
metadata. `calc-task.yaml` remains authoritative for task paths and lifecycle
state.

Do not create concrete task directories, `calc-task.yaml`, README indexes, PBS
scripts, or physical inputs as part of base initialization. Those belong to an
explicit task or their owning workflow skill.
