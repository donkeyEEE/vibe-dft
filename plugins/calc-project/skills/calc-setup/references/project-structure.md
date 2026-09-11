# Calculation Project Structure

Use this reference for an approved project initialization or reorganization.

## Base layout

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

`01<main-line-slug>` uses a lowercase, hyphenated research-line name. The data
root may instead be `02<slug>-原始数据/`. Base setup creates empty `01-rqs/`,
data-root, `calculation_templates/`, `structures/`, and `06-文献笔记/`
containers. It does not populate calculation templates or the literature
container. The Paper Project literature workflow owns the latter's contents.

Create `software-profiles.md` only when cluster configuration is requested.
Base setup creates no concrete RQ directory, Decision Ticket, Spec, task, Run,
calculation input, scheduler script, or project index. Existing RQs and Specs
are reported and left unchanged.

## ARCHITECTURE.md contract

Record directory responsibilities, naming rules, and the Git/cluster data
boundary. Consumers read the following exact section and field lines; they do
not infer configuration from filenames:

```markdown
## Calculation Configuration

Data root: 02原始数据/
Tracker adapter: local-markdown
RQ location: 01<main-line-slug>/01-rqs/<rq-id>-<slug>/
Software profile: software-profiles.md
```

Omit `Software profile:` until that file is configured. `Data root:` is the
chosen project-relative data-root path. The initial and only configured Tracker
adapter is `local-markdown`. `RQ location:` is a location convention, not a
created RQ and not a state schema.

## Generated AGENTS.md contract

Keep the generated file concise. It points agents to:

- project `CONTEXT.md` for terms and data boundaries;
- `ARCHITECTURE.md` and its `## Calculation Configuration` before locating an
  RQ, Spec, task, or Run;
- the selected `RQ.md`, selected Spec, and only the Runs referenced by that Spec
  before scientific-design or execution work;
- the Git/cluster boundary: documents, templates, structures, scripts, and
  lightweight results may be tracked locally, while HDF5, `CHGCAR`, `WAVECAR`,
  and large calculation outputs remain server-side.

The generated file keeps project operation rules at project scope. The Spec is
the sole authority for task state, DAG, Runs, current-Run designation,
execution progress, and closure.

## Project documents

Generate concise project-specific documents. `CONTEXT.md` starts from
[project context](project-context.md) plus confirmed project definitions.
Preserve an existing `CONTEXT.md` unless the user approves each proposed
change. `.gitignore` excludes editor/Python caches, HDF5, `CHGCAR`, `WAVECAR`,
and other identified large calculation outputs.
