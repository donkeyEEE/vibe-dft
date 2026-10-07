# 进度记录契约

## 位置与权威

每个 RQ 在 `RQ.md` 同级保存一份 `tracker.json`，记录该 RQ 及其 Spec、Task、Run 的派生摘要。
RQ.md 与 Spec 保持权威；空项目不创建记录。记录覆盖该 RQ 的全部已发布 Spec 才算完整。
项目总览按配置的 `RQ location:` 枚举实际 RQ 目录并汇总各份记录，不保存项目级进度记录；
缺失的记录也计入覆盖范围。

## 字段

- 顶层：`schema_version: 1`、`updated_at`（含时区）和单个 `rq` 对象。
- RQ：`id`、`title`、`status`、`source`（项目相对 RQ.md 路径）、`specs` 数组。
- Spec：`id`、`title`、`status`、`source`（项目相对 Spec 路径）、`tasks` 数组。
- Task：`id`、`title`、`status`、`runs` 数组。
- Run：`id`、`status`、布尔值 `current`。

空子集合写为 `[]`。ID 仅在父范围内唯一，以 RQ 的 source 和完整父链定位条目。
状态照录权威记录，不通过子对象状态推断父对象状态，不复制科学正文或执行日志。

查询单个 RQ 只读其记录；缺失、损坏、条目异常、已知未同步或用户要求核对时，回查相应
RQ 的权威记录。写入、修复或重建时读取[维护契约](progress-tracker-maintenance.md)；
旧项目级记录的迁移由 `$calc-setup` 处理。
