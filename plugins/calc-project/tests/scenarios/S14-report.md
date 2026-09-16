# S14 — Calculation reports

`S14-topic-stage-report`:

> 为界面磁性目前取得的结果生成一份阶段汇报。先预览你找到的 RQ/Spec 范围和 tag，再生成 HTML。

`S14-anchored-result-report`:

> 为 RQ-003 的 SPEC-002 和 SPEC-004 生成结果汇报；证据不足的部分也保留并说明。

`S14-existing-tag`:

> 使用已有 tag `interface-magnetism` 重新生成汇报。我知道该 workspace 会原地替换。

`S14-supplemental-and-figure`:

> 将未归属 RQ 的 comparison.csv 作为补充候选展示给我确认；如果它确实需要新图，再交给 prl-figure。HTML 默认交给 show-me。

Expected behavior:

- Topic entry previews a shallow RQ/Spec scope, intent, and tag before generation.
- Current and accepted Runs are primary evidence; material gaps, counterevidence,
  remote-only evidence, and confirmed supplemental results remain visible without
  preventing report generation.
- The workspace is `.calc-project/results-<tag>/`, contains lightweight consumed
  source data and provenance, and does not copy heavyweight Run outputs.
- New scientific figures are delegated only when materially useful. HTML generation
  is delegated to `show-me` without prescribing its narrative or layout.
