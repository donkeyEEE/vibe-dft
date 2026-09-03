# Zotero 集成参考

## 访问 Zotero

### 方式一：zotero 插件（优先）

使用全局安装的 zotero 插件脚本，该脚本默认使用 `http://127.0.0.1:23119`，原生 Windows/macOS/Linux 均可使用：

```bash
python3 <zotero-plugin>/skills/zotero/scripts/zotero.py search "query" --json
python3 <zotero-plugin>/skills/zotero/scripts/zotero.py children <itemKey> --json
python3 <zotero-plugin>/skills/zotero/scripts/zotero.py fulltext <attachmentKey> --out /tmp/fulltext.txt
```

`<zotero-plugin>` 路径：`/home/donk/.codex/plugins/cache/openai-curated-remote/zotero/0.1.2/`

### 方式二：Zo2Notes 脚本（回退）

使用 paper-project 自带的 Zo2Notes `zotero.py`。此脚本通过固定的 Windows-to-WSL bridge 访问 Zotero Desktop：

```bash
python3 <plugin-root>/skills/zo2notes/scripts/zotero.py search "query" --json
python3 <plugin-root>/skills/zo2notes/scripts/zotero.py children <itemKey> --json
python3 <plugin-root>/skills/zo2notes/scripts/zotero.py fulltext <attachmentKey> --out /tmp/fulltext.txt
```

Zo2Notes 当前使用 `http://172.30.128.1:23119`，并发送 `Host: 127.0.0.1:23119` 与 `Zotero-API-Version: 3` 请求头。

## 搜索策略

### 作者-年份引用

```bash
python3 .../zotero.py search "Smith 2020" --json
```

Zotero 会返回匹配项。从结果中选择最匹配的：
1. 优先 author 匹配 + year 匹配
2. 其次 title 与段落主题相关
3. 如果多个匹配，返回前 3 个供评估

### 数字编号引用

需要先建立编号到文献的映射（见 `references/citation-patterns.md`），然后用作者+年份搜索。

### 通过 DOI 精确查找

如果已知 DOI，可以直接查找：

```bash
python3 .../zotero.py search "10.1234/example" --json
```

## 获取摘要

搜索结果的 JSON 中通常包含 `abstractNote` 字段：

```json
{
  "key": "ABC123",
  "title": "Paper title",
  "abstractNote": "Abstract text...",
  "creators": [...],
  "year": "2020",
  "doi": "10.1234/example"
}
```

如果搜索结果不包含摘要，单独获取 item：

```bash
# 直接通过 API
curl -sS -H 'Zotero-API-Version: 3' \
  'http://127.0.0.1:23119/api/users/0/items/ABC123' | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{}).get('abstractNote',''))"
```

WSL 下如需通过 Windows 主机访问，使用：

```bash
curl -sS -H 'Host: 127.0.0.1:23119' -H 'Zotero-API-Version: 3' \
  'http://172.30.128.1:23119/api/users/0/items/ABC123' | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{}).get('abstractNote',''))"
```

## 获取全文

仅在摘要不足以判断时获取全文：

```bash
# 1. 找到 PDF 附件
python3 .../zotero.py children ABC123 --json

# 2. 从输出中找 attachment 类型，获取 key
# 3. 获取全文
python3 .../zotero.py fulltext <attachmentKey> --out /tmp/fulltext.txt
```

**注意**：
- 全文可能很大（数万字），只读取与声明相关的部分
- 如果 PDF 未索引（fulltext 为空），跳过，仅基于摘要评估
- 不下载远端 PDF

## 匹配置信度

搜索结果的匹配度分级：

| 匹配度 | 条件 | 处理 |
|--------|------|------|
| 精确匹配 | 第一作者姓氏 + 年份完全匹配 | 直接使用 |
| 高置信度 | 第一作者匹配，年份 ±1 | 使用，标注 |
| 中置信度 | 标题关键词匹配，领域匹配 | 使用，标注 |
| 低置信度 | 仅有部分关键词匹配 | 列出选项，请用户确认 |
| 无匹配 | 未找到任何结果 | 标记为"未找到" |

## Zotero 不可用时的处理

如果 Zotero Desktop 未运行或 API 不可用：

1. 提示用户启动 Zotero Desktop
2. 运行 `python3 .../zotero.py status --json`，诊断 Zotero Desktop、本地 API 与 Windows-to-WSL bridge
3. 如果 Zotero 确实不可用，生成仅含引用标记提取的部分报告，供用户手动核查
