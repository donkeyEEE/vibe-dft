# Dev Project 开发上下文

本 context 覆盖 `dev-engineering`、`dev-incubator`、`dev-misc` 和 `dev-productivity` 四个插件。

## 核心术语

**Engineering plugin**：`dev-engineering`，维护软件开发与维护工作流，中文称“工程插件”。

**Productivity plugin**：`dev-productivity`，维护构思、决策、沟通和 agent-facing 文档工作流，中文称“设计插件”。

**Issue tracker**：承载项目 issue 的工具，例如 GitHub Issues、Linear 或项目本地约定。

**Issue**：Issue tracker 中单个可追踪工作单元。

**Decision ticket**：`wayfinder` 使用的特殊子 Issue，承载需要形成决策的问题，不是实现切片。

**Triage role**：triage 状态机施加到 Issue 的规范角色标签。

## 维护边界

四个插件共享术语，但各自保有独立 manifest 和发布边界。跨插件引用必须通过实际路径或明确依赖表达；不能依赖旧 `/home/donk/plugins/dev-project` 外层仓库结构。修改 issue、triage、wayfinder 或 setup 相关 skill 时保持以上术语一致。
