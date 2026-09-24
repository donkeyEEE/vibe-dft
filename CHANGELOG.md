# 更新日志

<!-- 新版本条目置顶，使用“## <版本号> — YYYY-MM-DD”标题，并简要列出修改内容。 -->

## 1.0.1 — 2026-09-24

- 为每个 RQ 建立独立的 `tracker.json` 派生进度表；状态写入者同步维护，缺失或损坏时按该 RQ 的权威记录重建，并提供旧项目级跟踪表迁移约定。
- 更新 `calc-project:show-cot`：枚举配置范围内的 RQ 并汇总各跟踪表；发现缺表、异常或已知未同步时修复对应 RQ，生成报告时注明各表的更新时间。
- 新增 `calc-project:calc-issue`，记录和关联值得独立探究的执行问题，支持委托调研、验证需求交接及 Issue 来源回链。
- 扩展 `calc-project:ask-lyz`：可直接解释插件术语、核心流程、各 skill 职责及 Tracker 用法，并继续提供接口推荐和进度查询。
- 将 Calc Project 领域词汇移至插件共享资源，更新各 skill 的引用路径、发布包及相关文档和测试。

## 1.0.0 — 2026-09-23

- 增强 `paper-project:get-zotero` 的 WSL 自动连接：依次探测 loopback、Linux 默认网关和 Windows WSL 虚拟接口，并保留只读 Local API 边界。
- 将自动探测设为默认且完整的连接流程，不再要求、创建或询问用户配置文件；已有配置仅作向后兼容读取。
- 补充 WSL host 发现与连接失败诊断测试，并验证 mirrored networking 下可直接访问 Windows Zotero Local API。
- 将 `paper-project:get-notes` 收敛为单一的 Zotero 文献研究笔记流程，移除论文素材库、collection 映射和项目存储状态机。

## 0.1.1 — 2026-09-21

- 从 Skill Incubator 移除 `scientific-critical-thinking`，并更新其发布元数据、文档与发行测试。
