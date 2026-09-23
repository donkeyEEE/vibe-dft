# 更新日志

<!-- 新版本条目置顶，使用“## <版本号> — YYYY-MM-DD”标题，并简要列出修改内容。 -->

## 1.0.0 — 2026-09-23

- 增强 `paper-project:get-zotero` 的 WSL 自动连接：依次探测 loopback、Linux 默认网关和 Windows WSL 虚拟接口，并保留只读 Local API 边界。
- 将自动探测设为默认且完整的连接流程，不再要求、创建或询问用户配置文件；已有配置仅作向后兼容读取。
- 补充 WSL host 发现与连接失败诊断测试，并验证 mirrored networking 下可直接访问 Windows Zotero Local API。

## 0.1.1 — 2026-09-21

- 从 Skill Incubator 移除 `scientific-critical-thinking`，并更新其发布元数据、文档与发行测试。
