# Zotero 集成参考

## 唯一获取接口

通过 Paper Project 的 `get-zotero` 只读接口定位并取得文献内容：

```bash
python3 <plugin-root>/skills/get-zotero/scripts/zotero.py search "query" --json
python3 <plugin-root>/skills/get-zotero/scripts/zotero.py content \
  <itemKey> --mode auto --out-dir <temporary-directory>
```

不直接调用 Zotero HTTP API，不导入 `get-zotero` 的 Python 模块，也不改用其他
Zotero 脚本。连接模式、主机、端口和 Windows/WSL 附件映射全部由
`get-zotero` 管理。

## 匹配策略

- 作者—年份引用：优先匹配第一作者姓氏和年份，再以标题与段落主题消歧。
- 数字编号引用：先从稿件参考文献表建立编号到文献信息的映射，再检索。
- 已知 DOI：以 DOI 精确检索。
- 多个结果仍无法消歧时，列出最匹配的三个候选供确认。
- 找不到时标记为“未找到”，不得以相似论文代替。

匹配置信度：作者与年份完全一致为精确匹配；作者一致且年份相差一年为高置信度；
仅标题关键词和领域相符为中置信度；只有部分关键词为低置信度，必须确认。

## Content artifact 验证与消费

调用 `content` 后先验证：

1. `schema_version == 1`；
2. manifest 的 `item_key` 与目标条目一致；
3. `content.kind` 是 `text-file`、`pdf-file`、`metadata-only` 或 `error`；
4. `text-file` 或 `pdf-file` 的 `path` 指向实际存在的 artifact。

按类型处理：

- `text-file`：读取与待核验主张相关的索引正文片段。
- `pdf-file`：仅在摘要和索引正文不足时定向读取必要页面，不下载或复制原 PDF。
- `metadata-only`：只依据题录与原始摘要，明确记录 `evidence_basis: abstract`。
- `error`：遵循 `code` 与 `next_step`；不得把获取失败解释为没有正文证据。

全文可能很大，只读取与声明相关的部分，不把整篇论文载入上下文。

## Zotero 不可用时

提示用户启动 Zotero Desktop，然后运行：

```bash
python3 <plugin-root>/skills/get-zotero/scripts/zotero.py doctor --json
```

若仍不可用，生成仅含引用标记提取结果的部分报告，保留待核验状态。
