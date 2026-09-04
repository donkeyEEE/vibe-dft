---
name: meta-versioned-graph-schema-migration
type: procedure
tags: [domain/knowledge-engineering, task/ontology-implementation, concern/maintainability]
updated_at: 2026-08-26
---

# 版本化图谱 Schema 迁移

图谱 Schema 演化应按依赖影响评估、版本化变更、双写过渡、存量回填、查询回归和受控切换执行，避免新旧标签或关系导致静默漏查。

## Procedure

变更前导出当前 Schema，并检索查询、应用代码和提示词中对旧标签、属性或关系的依赖；为新旧结构设定可区分的版本与迁移窗口；在过渡期同时写入兼容结构；分批回填存量数据并记录进度；对代表性查询、计数和业务结果运行新旧对照；确认覆盖率和回滚路径后才切换读取端并停止旧结构写入。

## Caveats

双写周期、回填批量和切换方式依赖存储引擎、数据规模与停机容忍度。迁移完成前不得假设存量数据会自动符合新 Schema。

## References

- 《本体论紫皮书》v2，第 4.6 节，PDF 第 62 页（ONT-KG-014）。
